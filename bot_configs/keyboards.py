from messages import *
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

# BUTTONS
menu1 = KeyboardButton(MENU_1)
menu2 = KeyboardButton(MENU_2)
menu3 = KeyboardButton(MENU_3)
menu4 = KeyboardButton(MENU_4)

# KEYBOARDS
menu = ReplyKeyboardMarkup() #
menu.add(menu1, menu2, menu3, menu4)


in_btn_1 = KeyboardButton(SHOW)
in_btn_2 = KeyboardButton(DONT_SHOW)
in_k = InlineKeyboardMarkup()
in_k.add(in_btn_1, in_btn_2)

