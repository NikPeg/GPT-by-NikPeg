from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import config

FEEDBACK = InlineKeyboardButton(text='👌Оставить отзыв', callback_data='give_feedback')
ABOUT = InlineKeyboardButton(text='ℹ️Узнать о боте', callback_data='info')
SOS = InlineKeyboardButton(text='🆘Поддержка', url=config.SOS_URL)
BACK = InlineKeyboardButton(text='👈Назад', callback_data='return')
PAYMENT = InlineKeyboardButton(text='🫰Оформить подписку', callback_data='payment')
