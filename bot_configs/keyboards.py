from .messages import *
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from .config import ConfigData


config_data = ConfigData()


# BUTTONS
agreement_agree = KeyboardButton(AGREE)
agreement_disagree = KeyboardButton(DISAGREE)

woman_gender = KeyboardButton(WOMAN)
man_gender = KeyboardButton(MAN)

get_form = InlineKeyboardMarkup(text=GET_FORM, callback_data=GET_FORM)
edit_form = InlineKeyboardMarkup(text=EDIT_FORM, callback_data=EDIT_FORM)
wall_users = InlineKeyboardMarkup(text=SHOW_USERS, callback_data=SHOW_USERS)
active_flag = InlineKeyboardMarkup(text=ACTIVE_FLAG, callback_data=ACTIVE_FLAG)
not_active_flag = InlineKeyboardMarkup(text=NOT_ACTIVE_FLAG, callback_data=NOT_ACTIVE_FLAG)
invite = InlineKeyboardMarkup(text=INVITE, callback_data=INVITE)

name_edit = InlineKeyboardMarkup(text=NAME, callback_data=NAME)
gender_edit = InlineKeyboardMarkup(text=GENDER, callback_data=GENDER)
location_edit = InlineKeyboardMarkup(text=LOCATION, callback_data=LOCATION)
description_edit = InlineKeyboardMarkup(text=DESCRIPTION, callback_data=DESCRIPTION)
link_photo_edit = InlineKeyboardMarkup(text=LINK_PHOTO, callback_data=LINK_PHOTO)

link_agreement = InlineKeyboardButton('Соглашение', url=config_data.LINK_AGR)

# KEYBOARDS
agreement_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
agreement_keyboard.add(agreement_agree, agreement_disagree)

agreement_link_keyboard = InlineKeyboardMarkup()
agreement_link_keyboard.add(link_agreement)

gender_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
gender_keyboard.add(woman_gender, man_gender)

form_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
form_keyboard.add(get_form, edit_form, wall_users, active_flag, invite)
form_keyboard_flag = ReplyKeyboardMarkup(resize_keyboard=True)
form_keyboard_flag.add(get_form, edit_form, not_active_flag, invite)

edit_keyboard = InlineKeyboardMarkup()
edit_keyboard.add(name_edit, location_edit, description_edit, link_photo_edit)


def create_inline_keyboard(to_user_id):
    love_user_ = InlineKeyboardButton(LOVE_USER, callback_data=f"*{to_user_id}")
    skip_user_ = InlineKeyboardButton(SKIP_USER, callback_data=f"&{to_user_id}")
    # pause_user_ = InlineKeyboardButton(PAUSE_USER, callback_data=PAUSE_USER)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(love_user_, skip_user_)
    return keyboard

