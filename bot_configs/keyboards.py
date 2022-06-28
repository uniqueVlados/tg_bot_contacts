from messages import *
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

get_form = InlineKeyboardMarkup(GET_FORM)
edit_form = InlineKeyboardMarkup(EDIT_FORM)

name_edit = InlineKeyboardMarkup(CHANGE + NAME)
gender_edit = InlineKeyboardMarkup(CHANGE + GENDER)
location_edit = InlineKeyboardMarkup(CHANGE + LOCATION)
description_edit = InlineKeyboardMarkup(CHANGE + DESCRIPTION)
link_photo_edit = InlineKeyboardMarkup(CHANGE + LINK_PHOTO)

# in_btn_1 = KeyboardButton(SHOW)
# in_btn_2 = KeyboardButton(DONT_SHOW)

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
form_keyboard.add(get_form, edit_form)

edit_keyboard = InlineKeyboardMarkup()
edit_keyboard.add(name_edit, gender_edit, location_edit, description_edit, link_photo_edit)

# in_k = InlineKeyboardMarkup()
# in_k.add(in_btn_1, in_btn_2)

