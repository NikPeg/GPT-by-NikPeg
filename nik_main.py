import asyncio
import logging

from aiogram import executor
import messages
import config
from handlers.users.feedback import start_feed_back, check_subscriptions
from loader import bot, dp
from utils.bot_start_func.set_bot_commands import set_default_commands

logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher):
    await bot.send_message(config.ADMIN_ID, messages.BOT_STARTED.format(config.INSTANCE_NAME))
    await set_default_commands(dispatcher)
    asyncio.create_task(start_feed_back())
    # asyncio.create_task(check_subscriptions())


TRY_POLLING_PERIOD = 60 * 5


async def try_polling():
    while True:
        try:
            executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
        except Exception as e:
            print(e)
        await asyncio.sleep(TRY_POLLING_PERIOD)


if __name__ == '__main__':
    asyncio.run(try_polling())
