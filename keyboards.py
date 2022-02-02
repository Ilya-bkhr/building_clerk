from telegram import (InlineKeyboardMarkup, KeyboardButton,
                      ReplyKeyboardMarkup, InlineKeyboardButton)

from config import  MAIN_KEYBOARD

def main_keyboard():
    keyboard = ReplyKeyboardMarkup([
        [KeyboardButton(MAIN_KEYBOARD['MAKE_REPORT'])],
        [KeyboardButton(MAIN_KEYBOARD['COSTS']), KeyboardButton(MAIN_KEYBOARD['ENTRIES'])],
        [KeyboardButton(MAIN_KEYBOARD['BALANCE'])],
        [KeyboardButton(MAIN_KEYBOARD['TOP_UP'])]
        ])
    return keyboard


def period_keyboard():
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('Неделя', callback_data='7'),
         InlineKeyboardButton('Месяц', callback_data='30')],
        [InlineKeyboardButton('2 месяца', callback_data='60')]
        ])
    return keyboard
