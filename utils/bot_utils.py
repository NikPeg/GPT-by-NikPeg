from aiogram.types import ParseMode
from utils.formatting import markdown_to_html

import messages
from config import ADMIN_ID

MAX_MESSAGE_LENGTH = 4096


async def send_big_message(bot, user_id, text):
    print(text)
    for i in range(0, len(text), MAX_MESSAGE_LENGTH):
        err = None
        try:
            await bot.send_message(user_id, markdown_to_html(text[i:i + MAX_MESSAGE_LENGTH]), parse_mode=ParseMode.HTML)
            continue
        except Exception as e:
            await bot.send_message(ADMIN_ID, e)
            print(e)
            err = e
        for parse_mode in [ParseMode.MARKDOWN_V2, ParseMode.MARKDOWN, ParseMode.HTML]:
            try:
                await bot.send_message(user_id, text[i:i + MAX_MESSAGE_LENGTH], parse_mode=parse_mode)
                break
            except Exception as e:
                await bot.send_message(ADMIN_ID, e)
                print(e)
                err = e
        else:
            try:
                await bot.send_message(user_id, text[i:i + MAX_MESSAGE_LENGTH])
                break
            except Exception as e:
                await bot.send_message(ADMIN_ID, e)
                print(e)
                err = e
