import base64
import time
from pathlib import Path

import openai
from openai import AsyncOpenAI
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

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    async def add_message(self, thread_id, user_question, file_paths=None):
        if file_paths is None:
            file_paths = []
        file_ids = []
        for path in file_paths:
            file_ids.append(self.client.files.create(
                file=Path(path),
                purpose="assistants",
            ).id)
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
                                "file_id": file_id,
                                "detail": "low",
                            }
                        } for file_id in file_ids
                    ],
            role="user",
            # attachments=[Attachment(file_id=file_id, tools=FileSearchToolParam) for file_id in file_ids],
        )
        return message

    def create_thread(self):
        thread = self.client.beta.threads.create()
        return thread.id

    async def cancel_run(self, thread_id, run_id):
        run_info = await self.aclient.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run_info.completed_at:
            print("NOTHING TO CANCEL!")
            return
        print("CANCELLING")
        await self.aclient.beta.threads.runs.cancel(
            thread_id=thread_id,
            run_id=run_id,
        )

    async def create_run(self, thread_id):
        run = await self.aclient.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
        )
        return run.id
        # return None

    async def get_answer(self, thread_id, func, run_id):
        while True:
            await func()
            run_info = await self.aclient.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            print("STATUS", run_info.status)
            if run_info.completed_at:
                break
            if run_info.status:
                print("RUN WAS CANCELLED!")
                return None
            time.sleep(1)
        messages = await self.aclient.beta.threads.messages.list(thread_id)
        assistant_messages = []
        for message_data in messages.data:
            if message_data.role == "assistant":
                assistant_messages.append(message_data.content[0].text.value)
            else:
                break
        return "".join(assistant_messages[::-1])

    @retry(wait=wait_fixed(21), stop=stop_after_attempt(5))
    def ask(self, request, context=None):
        if context is None:
            context = []
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    MessageDTO(Role.SYSTEM, prompts.BIG_KPT).as_dict(),
                    *[message.as_dict() for message in context],
                    MessageDTO.from_user(request).as_dict(),
                ]
            )

            return completion.choices[0].message.content
        except Exception as e:
            raise e
