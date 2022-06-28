from . import dp
from aiogram import types
from .states import *
from database.operations import *
from . import cities, bot
from .keyboards import *
from .messages import *


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


@dp.message_handler(commands=['form'])
async def get_form_(message: types.Message):
    user_id = message.from_user.id
    user = get_user_by_tg_id(user_id)
    set_user_state(user_id, WAIT_FOR_ACTION)
    await message.answer(f"{user.name}\n{user.location}\n-------------\n{user.description}")
    await bot.send_photo(user_id, user.link_photo)


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
        await message.answer(AGREEMENT_ACCEPTED, reply_markup=types.ReplyKeyboardRemove())
        await message.answer(CREATE_ACCOUNT)
        set_user_state(user_id, NAME_INPUT)
    elif answer_ == DISAGREE:
        await message.answer(AGREEMENT_NOT_ACCEPTED)
        await message.answer(AGREEMENT_MESSAGE, reply_markup=agreement_keyboard)
    else:
        await message.answer(ERROR_KEYBOARD)
        await message.answer(AGREEMENT_MESSAGE, reply_markup=agreement_keyboard)


def check_name(name):
    bad_symbols = {'\n', '\t', '\r', ',', '.', '/', '>', '<', '\\', '|', ':',
                   ';', '\'', '"', '`', '~', '!', '@', '#', '$', '%', '^', '&',
                   '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', '?', '№'}
    if bad_symbols & set(name) or len(name) > 30:
        return False
    return True


async def handle_name_input(message: types.Message, user_id, name):
    user = get_user_by_tg_id(user_id)
    if not check_name(name):
        await message.answer(NAME_ERROR, reply_markup=types.ReplyKeyboardRemove())
        return
    state = GENDER_INPUT
    ans = NAME_ACCEPTED
    keyboard = gender_keyboard
    if user and user.name:
        state = WAIT_FOR_ACTION
        ans = NEW_NAME_EDIT
        keyboard = types.ReplyKeyboardRemove()
    set_user_name(user_id, name)
    set_user_state(user_id, state)
    await message.answer(ans, reply_markup=keyboard)


def check_gender(gender):
    return gender == WOMAN or gender == MAN


async def handle_gender(message: types.Message, user_id, gender):
    user = get_user_by_tg_id(user_id)
    if not check_gender(gender):
        await message.answer(ERROR_KEYBOARD, reply_markup=gender_keyboard)
        return
    state = DESCRIPTION_INPUT
    ans = GENDER_ACCEPTED
    if user and user.gender:
        state = WAIT_FOR_ACTION
        ans = NEW_GENDER_EDIT
    set_user_gender(user_id, gender)
    set_user_state(user_id, state)
    await message.answer(ans, reply_markup=types.ReplyKeyboardRemove())


def check_description(desc):
    return len(desc) < 200


async def handle_description_input(message: types.Message, user_id, description):
    user = get_user_by_tg_id(user_id)
    if not check_description(description):
        await message.answer(DESC_ERROR, reply_markup=types.ReplyKeyboardRemove())
        return
    state = LOCATION_INPUT
    ans = DESK_ACCEPTED
    if user and user.description:
        state = WAIT_FOR_ACTION
        ans = NEW_DESCRIPTION_EDIT
    set_user_description(user_id, description)
    set_user_state(user_id, state)
    await message.answer(ans, reply_markup=types.ReplyKeyboardRemove())


async def handle_location_input(message: types.Message, user_id, location):
    user = get_user_by_tg_id(user_id)
    if not cities.check_location(location.capitalize()):
        await message.answer(LOCATION_ERROR, reply_markup=types.ReplyKeyboardRemove())
        return
    state = LINK_PHOTO_INPUT
    ans = LOCATION_ACCEPTED
    if user and user.location:
        state = WAIT_FOR_ACTION
        ans = NEW_LOCATION_EDIT
    set_user_location(user_id, location)
    set_user_state(user_id, state)
    await message.answer(ans, reply_markup=types.ReplyKeyboardRemove())


# обработчик текстовых сообщений
@dp.message_handler()
async def handle_messages(message: types.Message):
    user_id = message.from_user.id
    state = get_user_state(user_id)
    text = message.text

    handle_functions = {NEED_INVITE: handle_invite_code,
                        NEED_AGREEMENT: handle_agreement,
                        NAME_INPUT: handle_name_input,
                        GENDER_INPUT: handle_gender,
                        DESCRIPTION_INPUT: handle_description_input,
                        LOCATION_INPUT: handle_location_input,
                        }

    function = handle_functions.get(state)
    if function:
        await function(message, user_id, text)


# Обработчик для получения фото
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    user_id = str(message.from_user.id)
    photo_id = message.photo[0].file_id
    user = get_user_by_tg_id(user_id)
    state = LINK_PHOTO_INPUT
    ans = PHOTO_ACCEPTED
    if user and user.link_photo:
        state = WAIT_FOR_ACTION
        ans = NEW_LINK_PHOTO_EDIT

    set_user_link_photo(user_id, photo_id)
    await message.answer(ans, reply_markup=types.ReplyKeyboardRemove())
    set_user_state(user_id, state)

    await message.answer(f"{user.name}\n{user.location}\n-------------\n{user.description}")
    await bot.send_photo(user_id, user.link_photo)
    await message.answer("Выберите действие ниже", reply_markup=form_keyboard)


# Обработчик для inline-кнопок
@dp.callback_query_handler()
async def call_back_data(callback: types.CallbackQuery):
    data = callback.data
    user_id = callback.from_user.id

    if data == GET_FORM:
        await callback.message.answer(f"Анкета подтверждена", reply_markup=types.ReplyKeyboardRemove())
    elif data == EDIT_FORM:
        set_user_state(user_id, WAIT_FOR_ACTION)
        await callback.message.answer(FORM_INFO, reply_markup=edit_keyboard)

    elif data == NAME:
        set_user_state(user_id, NAME_INPUT)
        await callback.message.answer(NEW_NAME, reply_markup=types.ReplyKeyboardRemove())
    elif data == GENDER:
        set_user_state(user_id, GENDER_INPUT)
        await callback.message.answer(NEW_GENDER, reply_markup=types.ReplyKeyboardRemove())
    elif data == LOCATION:
        set_user_state(user_id, LOCATION_INPUT)
        await callback.message.answer(NEW_LOCATION, reply_markup=types.ReplyKeyboardRemove())
    elif data == DESCRIPTION:
        set_user_state(user_id, DESCRIPTION_INPUT)
        await callback.message.answer(NEW_DESCRIPTION, reply_markup=types.ReplyKeyboardRemove())
    elif data == LINK_PHOTO:
        set_user_state(user_id, LOCATION_INPUT)
        await callback.message.answer(NEW_LINK_PHOTO, reply_markup=types.ReplyKeyboardRemove())
