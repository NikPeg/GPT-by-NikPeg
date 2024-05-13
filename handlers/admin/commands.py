import asyncio

import openai
from aiogram import types
from config import ADMIN_ID

import messages
from database.payment_db import unsubscribe
from database.user_db import get_all_users
from handlers.common import create_user_req
from loader import dp, bot, client
from payments import SubscriptionStatus


@dp.message_handler(commands=['answer'], state="*")
async def answer_message_handler(message: types.Message):
    if message.chat.id != ADMIN_ID:
        return
    if not message.reply_to_message:
        await bot.send_message(ADMIN_ID, messages.WRONG_MESSAGE)
        return
    user_id = int(message.reply_to_message.text.split()[1])
    username = message.reply_to_message.text.split()[4][1:]
    request_text = " ".join(message.reply_to_message.text.split()[7:])
    try:
        await asyncio.create_task(create_user_req(user_id, username, request_text))
    except openai.BadRequestError as e:
        await bot.send_message(message.chat.id, messages.WAIT)
        await bot.send_message(ADMIN_ID, messages.WAIT + e)
    except Exception as e:
        await bot.send_message(ADMIN_ID, messages.UNKNOWN_ERROR.format(e))


@dp.message_handler(commands=['post'], state="*")
async def post_message_handler(message: types.Message):
    if message.chat.id != ADMIN_ID:
        return
    post_text = message.text[len("/post "):]
    await bot.send_message(ADMIN_ID, messages.POST_MESSAGE.format(post_text))
    for user_id, username in get_all_users():
        try:
            await bot.send_message(user_id, post_text)
        except Exception as e:
            await bot.send_message(ADMIN_ID, messages.POST_ERROR.format(user_id, username, e))
        await bot.send_message(ADMIN_ID, messages.POST_SUCCESS.format(user_id, username))


async def unsubscribe_message_handler(message: types.Message):
    if message.chat.id != ADMIN_ID:
        return
    if not message.reply_to_message:
        await bot.send_message(ADMIN_ID, messages.WRONG_MESSAGE)
        return
    user_id = int(message.reply_to_message.text.split()[1])
    username = message.reply_to_message.text.split()[4][1:]
    await bot.send_message(ADMIN_ID, messages.UNSUBSCRIBING.format(user_id, username))
    for sub in client.list_subscriptions(user_id):
        if sub.status == SubscriptionStatus.ACTIVE.value:
            try:
                client.cancel_subscription(sub.id)
            except Exception as e:
                await bot.send_message(ADMIN_ID, e)
            unsubscribe(user_id)
            await bot.send_message(ADMIN_ID, messages.UNSUBSCRIBED.format(user_id, username))
