from .messages import *
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from .config import ConfigData


config_data = ConfigData()


# BUTTONS
menu1 = KeyboardButton(MENU_1)
menu2 = KeyboardButton(MENU_2)
menu3 = KeyboardButton(MENU_3)
menu4 = KeyboardButton(MENU_4)

agreement_agree = KeyboardButton(AGREE)
agreement_disagree = KeyboardButton(DISAGREE)

woman_gender = KeyboardButton(WOMAN)
man_gender = KeyboardButton(MAN)

get_form = InlineKeyboardMarkup(text=GET_FORM, callback_data=GET_FORM)
edit_form = InlineKeyboardMarkup(text=EDIT_FORM, callback_data=EDIT_FORM)
wall_users = InlineKeyboardMarkup(text=WALL_USERS, callback_data=WALL_USERS)

name_edit = InlineKeyboardMarkup(text=NAME, callback_data=NAME)
gender_edit = InlineKeyboardMarkup(text=GENDER, callback_data=GENDER)
location_edit = InlineKeyboardMarkup(text=LOCATION, callback_data=LOCATION)
description_edit = InlineKeyboardMarkup(text=DESCRIPTION, callback_data=DESCRIPTION)
link_photo_edit = InlineKeyboardMarkup(text=LINK_PHOTO, callback_data=LINK_PHOTO)

# in_btn_1 = KeyboardButton(SHOW)
# in_btn_2 = KeyboardButton(DONT_SHOW)

love_user = KeyboardButton(LOVE_USER)
skip_user = KeyboardButton(SKIP_USER)
pause_user = KeyboardButton(PAUSE_USER)

link_agreement = InlineKeyboardButton('Соглашение', url=config_data.LINK_AGR)

# KEYBOARDS
menu = ReplyKeyboardMarkup()
menu.add(menu1, menu2, menu3, menu4)

agreement_keyboard = ReplyKeyboardMarkup()
agreement_keyboard.add(agreement_agree, agreement_disagree)

agreement_link_keyboard = InlineKeyboardMarkup()
agreement_link_keyboard.add(link_agreement)

gender_keyboard = ReplyKeyboardMarkup()
gender_keyboard.add(woman_gender, man_gender)

form_keyboard = InlineKeyboardMarkup()
form_keyboard.add(get_form, edit_form, wall_users)

edit_keyboard = InlineKeyboardMarkup()
edit_keyboard.add(name_edit, gender_edit, location_edit, description_edit, link_photo_edit)


user_keyboard = ReplyKeyboardMarkup()
user_keyboard.add(love_user, skip_user, pause_user)

# in_k = InlineKeyboardMarkup()
# in_k.add(in_btn_1, in_btn_2)

