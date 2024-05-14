from aiogram.types import ParseMode

import messages
from config import ADMIN_ID

MAX_MESSAGE_LENGTH = 4096


async def send_big_message(bot, user_id, text):
    for i in range(0, len(text), MAX_MESSAGE_LENGTH):
        err = None
        for parse_mode in [ParseMode.MARKDOWN_V2, ParseMode.HTML, ParseMode.MARKDOWN]:
            try:
                await bot.send_message(user_id, text[i:i + MAX_MESSAGE_LENGTH], parse_mode=parse_mode)
                break
            except Exception as e:
                err = e
        else:
            await send_big_message(
                bot,
                ADMIN_ID,
                messages.PARSING_ERROR.format(err),
            )
