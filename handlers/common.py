from config import ADMIN_ID

import messages
from database.message_db import add_new_message
from database.session_db import get_thread_id, get_run_id, set_run_id
from loader import bot, gpt
from utils.bot_utils import send_big_message

TYPING_ACTION = "typing"


async def create_user_req(user_id, user_name, request_text, file_paths=None):
    async def typing():
        await bot.send_chat_action(user_id, TYPING_ACTION)

    await typing()
    await bot.send_message(ADMIN_ID, messages.MESSAGE_SENT.format(user_id, user_name))
    await send_big_message(bot, ADMIN_ID, request_text)
    thread_id = get_thread_id(user_id)
    await typing()
    current_run = get_run_id(user_id)
    await bot.send_message(ADMIN_ID, "CURRENT RUN " + str(current_run))
    if current_run:
        await bot.send_message(ADMIN_ID, "CANCELLING RUN " + str(current_run))
        await gpt.cancel_run(thread_id, current_run)
    await typing()
    await bot.send_message(ADMIN_ID, "ADDING MESSAGE")
    await gpt.add_message(thread_id, request_text, file_paths)
    await typing()
    await bot.send_message(ADMIN_ID, "CREATING NEW RUN")
    run_id = await gpt.create_run(thread_id)
    await bot.send_message(ADMIN_ID, "NEW RUN " + str(run_id))
    await typing()
    set_run_id(user_id, run_id)
    await bot.send_message(ADMIN_ID, "SET RUN IN DB")
    await bot.send_message(ADMIN_ID, "GETTING ANSWER")
    bot_answer = await gpt.get_answer(thread_id, typing, run_id)
    if not bot_answer:
        return
    await send_big_message(bot, user_id, bot_answer)
    await bot.send_message(ADMIN_ID, messages.BOT_ANSWERED.format(user_id, user_name))
    await send_big_message(bot, ADMIN_ID, bot_answer)
    add_new_message(user_id, request_text, bot_answer)
