from aiogram.types import ParseMode
from config import ADMIN_ID

import messages
from database.message_db import add_new_message
from database.session_db import get_thread_id
from loader import bot, gpt
from utils.bot_utils import send_big_message
from utils.formatting import markdown_to_html

TYPING_ACTION = "typing"


async def create_user_req(user_id, user_name, request_text):
    async def typing():
        await bot.send_chat_action(user_id, TYPING_ACTION)

    await typing()
    try:
        await send_big_message(
            bot,
            ADMIN_ID,
            messages.MESSAGE_SENT.format(user_id, user_name, request_text),
        )
    except Exception as e:
        await send_big_message(
            bot,
            ADMIN_ID,
            messages.PARSING_ERROR.format(e),
        )
    thread_id = get_thread_id(user_id)
    await typing()
    await gpt.add_message(thread_id, request_text)
    await typing()
    bot_answer = await gpt.get_answer(thread_id, typing)
    try:
        await send_big_message(bot, user_id, markdown_to_html(bot_answer), parse_mode=ParseMode.HTML)
    except Exception as e:
        await send_big_message(bot, user_id, bot_answer)
        await send_big_message(
            bot,
            ADMIN_ID,
            messages.PARSING_ERROR.format(e),
        )
    await send_big_message(
        bot,
        ADMIN_ID,
        messages.BOT_ANSWERED.format(user_id, user_name, bot_answer),
    )
    add_new_message(user_id, request_text, bot_answer)
