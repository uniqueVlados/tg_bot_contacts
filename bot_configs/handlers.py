from database.operations import *
from . import dp
from .keyboards import agreement_keyboard, agreement_link_keyboard, gender_keyboard, love_gender_keyboard
from .messages import *
from aiogram import types
from states import *
from parse_cities import Cities
from .config import ConfigData
from database.operations import *
from . import cities, bot


@dp.message_handler(commands=['start'])
async def start_(message: types.Message):
    user_id = message.from_user.id

    reply_text = WELCOME_HAS_ACCOUNT
    user_new_state = WAIT_FOR_ACTION

    has_account = check_user_account(user_id)
    if not has_account:
        reply_text = WELCOME
        user_new_state = NEED_INVITE

    await message.answer(reply_text)
    set_user_state(user_id, user_new_state)


async def handle_invite_code(message: types.Message, user_id, invite_code):
    agreement_mess = None
    answer = NOT_CHECK_INVITE
    if check_invite_code(invite_code):
        answer = CHECK_INVITE
        set_user_state(user_id, NEED_AGREEMENT)
        agreement_mess = AGREEMENT_MESSAGE

    await message.answer(answer)

    if agreement_mess:
        await message.answer(agreement_mess, reply_markup=agreement_keyboard)
        await message.answer(SHOW, reply_markup=agreement_link_keyboard)


async def handle_agreement(message: types.Message, user_id, answer_):
    if answer_ == AGREE:
        await message.answer(AGREEMENT_ACCEPTED)
        await message.answer(CREATE_ACCOUNT)
        set_user_state(user_id, NAME_INPUT)
    elif answer_ == DISAGREE:
        await message.answer(AGREEMENT_NOT_ACCEPTED)
        await message.answer(AGREEMENT_MESSAGE, reply_markup=agreement_keyboard)
    else:
        await message.answer(ERROR_KEYBOARD)
        await message.answer(AGREEMENT_MESSAGE, reply_markup=agreement_keyboard)


async def handle_name_input(message: types.Message, user_id, name):
    bad_symbols = {' ', '\n', '\t', '\r', ',', '.', '/', '>', '<', '\\', '|', ':',
                   ';', '\'', '"', '`', '~', '!', '@', '#', '$', '%', '^', '&',
                   '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', '?', '№'}
    if bad_symbols & set(name) and len(name) > 30:
        await message.answer(NAME_ERROR, reply_markup=types.ReplyKeyboardRemove())
    else:
        set_user_name(user_id, name)
        await message.answer(NAME_ACCEPTED, reply_markup=gender_keyboard)
        set_user_state(user_id, GENDER)


async def handle_gender(message: types.Message, user_id, gender):
    if gender == WOMAN or gender == MAN:
        set_user_gender(user_id, gender)
        await message.answer(GENDER_ACCEPTED, reply_markup=types.ReplyKeyboardRemove())
        set_user_state(user_id, LOVE_GENDER)
    else:
        await message.answer(ERROR_KEYBOARD, reply_markup=gender_keyboard)


async def handle_description_input(message: types.Message, user_id, description):
    if len(description) > 200:
        await message.answer(DESC_ERROR, reply_markup=types.ReplyKeyboardRemove())
    else:
        set_user_description(user_id, description)
        await message.answer(DESK_ACCEPTED, reply_markup=types.ReplyKeyboardRemove())
        set_user_state(user_id, LOCATION)


def check_location(city):
    return city in cities


async def handle_location_input(message: types.Message, user_id, location):
    if check_location(location.capitalize()):
        set_user_location(user_id, location)
        await message.answer(LOCATION_ACCEPTED, reply_markup=types.ReplyKeyboardRemove())
        set_user_state(user_id, LINK_PHOTO)
    else:
        await message.answer(LOCATION_ERROR, reply_markup=types.ReplyKeyboardRemove())


# обработчик текстовых сообщений
@dp.message_handler()
async def handle_messages(message: types.Message):
    user_id = message.from_user.id
    state = get_user_state(user_id)
    text = message.text

    handle_functions = {NEED_INVITE: handle_invite_code,
                        NEED_AGREEMENT: handle_agreement,
                        NAME_INPUT: handle_name_input,
                        GENDER: handle_gender,
                        DESCRIPTION: handle_description_input,
                        LOCATION: handle_location_input,
                        }

    function = handle_functions.get(state)
    if function:
        await function(message, user_id, text)


# Обработчик для получения фото
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    user_id = str(message.from_user.id)
    if get_user_state(user_id) == LINK_PHOTO:
        await message.answer(PHOTO__ACCEPTED, reply_markup=types.ReplyKeyboardRemove())
        await bot.get_file(message.photo[-1].download(user_id + ".jpg"))
    else:
        await message.answer(PHOTO_ERROR, reply_markup=types.ReplyKeyboardRemove())



# Обработчик для inline-кнопок
# @dp.callback_query_handler()
# async def call_back_data(callback: types.CallbackQuery):
#     data = callback.data
#     user_id = callback.from_user.id
#
#     if data == AGREE:
#         set_user_state(user_id, WAIT_FOR_ACTION)
#         await callback.message.answer(AGREEMENT_ACCEPTED)
#         await callback.message.answer(CREATE_ACCOUNT)
#         set_user_state(callback.from_user.id, NAME_INPUT)
#
#     elif data == DISAGREE:
#         await callback.message.answer(AGREEMENT_NOT_ACCEPTED)
#         await callback.message.answer(AGREEMENT_MESSAGE, reply_markup=agreement_keyboard)
