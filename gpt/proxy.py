import base64
import time
from pathlib import Path

import openai
from openai import AsyncOpenAI
from openai.types.beta import FileSearchToolParam
from openai.types.beta.threads.message_create_params import Attachment
from tenacity import retry, stop_after_attempt, wait_fixed

from .models import *
from .prompts import PROMPT

try:
    from config import ASSISTANT_ID
except ImportError:
    ASSISTANT_ID = None
except AttributeError:
    ASSISTANT_ID = None


class GPTProxy:
    def __init__(self, token, model="gpt-3.5-turbo", bot=None):
        self.client = openai.OpenAI(api_key=token)
        self.model = model
        self.assistant_id = ASSISTANT_ID or self.create_assistant("NikPeg bot", PROMPT, True)
        self.bot = bot
        self.aclient = AsyncOpenAI(api_key=token)

    def upload_file(self, path, purpose="assistants"):
        result = self.client.files.create(
            file=open(path, "rb"),
            purpose=purpose,
        )
        return result.id

    def create_assistant(self, name, instructions="", code_interpreter=False):
        assistant = self.client.beta.assistants.create(
            model=self.model,
            name=name,
            instructions=instructions,
            tools=[{"type": "code_interpreter"}] if code_interpreter else [],
        )
        print("assistant_id:", assistant.id)
        return assistant.id

    async def add_message(self, thread_id, user_question="", photo_paths=None, file_paths=None):
        async def create_message():
            message = await self.aclient.beta.threads.messages.create(
                thread_id=thread_id,
                content=[
                    {
                        "text": user_question,
                        "type": "text",
                    },
                ] if user_question else [] + [
                    {
                        "type": "image_file",
                        "image_file": {
                            "file_id": self.upload_file(path),
                            "detail": "low",
                        }
                    } for path in photo_paths
                ],
                role="user",
                attachments=[Attachment(file_id=file_id, tools=["file_search"]) for file_id in file_paths],
            )
            return message

        if photo_paths is None:
            photo_paths = []
        if file_paths is None:
            file_paths = []
        # for i in range(5):
        #     try:
        message = await create_message()
        return message
            # except openai.BadRequestError:
            #     last_run = await self.last_run(thread_id)
            #     if last_run:
            #         await self.cancel_run(thread_id, last_run)

    def create_thread(self):
        thread = self.client.beta.threads.create()
        return thread.id

    async def last_run(self, thread_id):
        runs = await self.aclient.beta.threads.runs.list(thread_id, order="desc", limit=1)
        if runs.data:
            return runs.data[0].id
        return None

    async def cancel_run(self, thread_id, run_id):
        try:
            await self.aclient.beta.threads.runs.cancel(
                thread_id=thread_id,
                run_id=run_id,
            )
        except openai.BadRequestError:
            return

    async def create_run(self, thread_id):
        for i in range(5):
            try:
                run = await self.aclient.beta.threads.runs.create(
                    thread_id=thread_id,
                    assistant_id=self.assistant_id,
                )
                return run.id
            except openai.BadRequestError:
                last_run = await self.last_run(thread_id)
                if last_run:
                    await self.cancel_run(thread_id, last_run)
        return None

    async def get_answer(self, thread_id, func, run_id):
        while True:
            await func()
            run_info = await self.aclient.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            print("STATUS", run_info.status)
            if run_info.completed_at:
                break
            if run_info.status not in {"in_progress", "queued"}:
                return run_info.last_error.message
            time.sleep(1)
        messages = await self.aclient.beta.threads.messages.list(thread_id)
        assistant_messages = []
        for message_data in messages.data:
            if message_data.role == "assistant":
                assistant_messages.append(message_data.content[0].text.value)
            else:
                break
        return "".join(assistant_messages[::-1])
