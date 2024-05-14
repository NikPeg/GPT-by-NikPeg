import asyncio

import openai
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup, default_state
from cloudpayments import Currency

import config
from config import ADMIN_ID

import buttons
import messages
import payments
from database.payment_db import check_subscribed, subscribe
from database.promo_db import check_promo
from database.sentence_db import random_sentence
from database.session_db import create_new_session
from database.user_db import add_new_user, update_sale
from handlers.admin.commands import unsubscribe_message_handler
from handlers.common import create_user_req
from keyboards.keyboards import start_markup, return_markup, payment_markup
from loader import dp, bot, client
from messages import HELP, START, PROMPT, NEW_PROMPT


class UserState(StatesGroup):
    gpt_request = State()
    feedback = State()
    payment = State()
    promo = State()


@dp.message_handler(commands=['start'], state="*")
async def start_command_handler(message: types.Message):
    add_new_user(message.chat.id, message.chat.username)
    await bot.send_message(message.chat.id, START, reply_markup=start_markup())
    await bot.send_message(message.chat.id, PROMPT.format(random_sentence()))
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(message.chat.id, message.chat.username, message.text),
    )
    await UserState.gpt_request.set()


@dp.callback_query_handler(text='info', state="*")
async def info_handler(call: types.CallbackQuery):
    await call.message.edit_text(HELP.format(config.PRICE), reply_markup=return_markup())
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(call.message.chat.id, call.message.chat.username, buttons.ABOUT.text),
    )


@dp.callback_query_handler(text='return', state="*")
async def return_handler(call: types.CallbackQuery):
    await call.message.edit_text(START, reply_markup=start_markup())
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(call.message.chat.id, call.message.chat.username, buttons.BACK.text),
    )


SUBSCRIPTION_CHECKS_COUNT = 300


@dp.callback_query_handler(text='payment', state="*")
async def payment_handler(call: types.CallbackQuery):
    link = client.create_order(
        config.PRICE,
        Currency.RUB,
        messages.PAYMENT_DESCRIPTION,
        account_id=call.message.chat.id,
        subscription_behavior=payments.SubscriptionBehavior.MONTHLY,
    ).url
    await call.message.edit_text(messages.PAYMENT_LINK.format(link), reply_markup=return_markup())
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(call.message.chat.id, call.message.chat.username, buttons.PAYMENT.text),
    )
    await UserState.payment.set()
    for i in range(SUBSCRIPTION_CHECKS_COUNT):
        for sub in client.list_subscriptions(call.message.chat.id):
            if sub.status == payments.SubscriptionStatus.ACTIVE.value:
                await UserState.gpt_request.set()
                subscribe(call.message.chat.id)
                await bot.send_message(call.message.chat.id, messages.PAYMENT_THANK, reply_markup=return_markup())
                await bot.send_message(
                    ADMIN_ID,
                    messages.USER_PAID.format(call.message.chat.id, call.message.chat.username),
                )
                return
            await asyncio.sleep(10)


@dp.message_handler(state=UserState.payment)
async def paid_handler(message: types.Message):
    if message.chat.id == ADMIN_ID:
        if message.text == '/unsubscribe':
            return await unsubscribe_message_handler(message)
    for sub in client.list_subscriptions(message.chat.id):
        if sub.status == payments.SubscriptionStatus.ACTIVE.value:
            await UserState.gpt_request.set()
            subscribe(message.chat.id)
            await bot.send_message(message.chat.id, messages.PAYMENT_THANK, reply_markup=return_markup())
            await bot.send_message(
                ADMIN_ID,
                messages.USER_PAID.format(message.chat.id, message.chat.username),
            )
            return
    await bot.send_message(message.chat.id, messages.PAYMENT_PROCESS, reply_markup=payment_markup())
    await bot.send_message(
        ADMIN_ID,
        messages.MESSAGE_SENT.format(message.chat.id, message.chat.username, message.text),
    )


@dp.message_handler(commands=['help'], state="*")
async def help_message_handler(message: types.Message):
    await bot.send_message(message.chat.id, HELP.format(config.PRICE))
    await bot.send_message(message.chat.id, PROMPT.format(random_sentence()))
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(message.chat.id, message.chat.username, message.text),
    )


@dp.message_handler(commands=['new'], state="*")
async def help_message_handler(message: types.Message):
    await bot.send_message(message.chat.id, NEW_PROMPT.format(random_sentence()))
    create_new_session(message.chat.id)
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(message.chat.id, message.chat.username, message.text),
    )
    await UserState.gpt_request.set()

@dp.callback_query_handler(text='promo', state="*")
async def promo_message_handler(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.message.chat.id, messages.PROMO_PROMPT, reply_markup=return_markup())
    await bot.send_message(
        ADMIN_ID,
        messages.BUTTON_PRESSED.format(call.message.chat.id, call.message.chat.username, buttons.PROMO.text),
    )
    await UserState.promo.set()


@dp.message_handler(state=UserState.promo)
async def promo_message_handler(message: types.Message):
    promo = message.text
    await bot.send_message(
        ADMIN_ID,
        messages.ENTERED_PROMO.format(message.chat.id, message.chat.username, promo),
    )
    sale = check_promo(promo)
    if sale:
        update_sale(message.chat.id, sale)
        await bot.send_message(message.chat.id, messages.REAL_PROMO.format(sale), reply_markup=return_markup())
    else:
        await bot.send_message(message.chat.id, messages.WRONG_PROMO, reply_markup=return_markup())
    await UserState.gpt_request.set()


@dp.message_handler(state=UserState.gpt_request)
@dp.message_handler(state=default_state)
async def user_gpt_req_handler(message: types.Message):
    if message.chat.id == ADMIN_ID:
        if message.text == '/unsubscribe':
            return await unsubscribe_message_handler(message)

    if not check_subscribed(message.chat.id):
        await bot.send_message(
            message.chat.id,
            messages.EXPIRED_PAYMENT.format(config.PRICE),
            reply_markup=payment_markup(),
        )
        await bot.send_message(ADMIN_ID,
                               messages.USER_EXPIRED_PAYMENT.format(message.chat.id, message.chat.username))
        return

    request_text = message.text
    try:
        await asyncio.create_task(create_user_req(message.chat.id, message.chat.username, request_text))
    except openai.BadRequestError as e:
        await bot.send_message(message.chat.id, messages.WAIT)
        await bot.send_message(ADMIN_ID, messages.WAIT + e)
    except Exception as e:
        await bot.send_message(ADMIN_ID, messages.UNKNOWN_ERROR.format(str(e)))
