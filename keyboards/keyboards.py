from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import buttons


def feedback_markup():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.insert(buttons.FEEDBACK)
    return markup


def start_markup():
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.insert(buttons.PROMO)
    markup.add(buttons.ABOUT, buttons.SOS)
    return markup


def return_markup():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(buttons.BACK)
    return markup


def payment_markup():
    markup = InlineKeyboardMarkup(row_width=True)
    # markup.add(buttons.PAYMENT)
    markup.add(buttons.BACK)
    return markup
