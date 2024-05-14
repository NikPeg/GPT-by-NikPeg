from aiogram.types import ParseMode
from utils.formatting import markdown_to_html, screen_symbols, screen_markdownv2_symbols

from config import ADMIN_ID

MAX_MESSAGE_LENGTH = 4096


async def send_big_message(bot, user_id, text):
    print(text)
    for i in range(0, len(text), MAX_MESSAGE_LENGTH):
        text_part = text[i:i + MAX_MESSAGE_LENGTH]
        screened = screen_markdownv2_symbols(text_part)
        for parse_mode in [ParseMode.MARKDOWN_V2, ParseMode.MARKDOWN, ParseMode.HTML]:
            try:
                await bot.send_message(user_id, screened, parse_mode=parse_mode)
                break
            except Exception as e:
                await bot.send_message(ADMIN_ID, e)
                print(e)
        else:
            try:
                await bot.send_message(user_id, markdown_to_html(text_part), parse_mode=ParseMode.HTML)
                continue
            except Exception as e:
                await bot.send_message(ADMIN_ID, e)
                print(e)
            try:
                await bot.send_message(user_id, screen_symbols(text_part))
                continue
            except Exception as e:
                await bot.send_message(ADMIN_ID, e)
                print(e)
