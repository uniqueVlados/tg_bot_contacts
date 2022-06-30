from . import dp
from aiogram import types
from .states import *
from database.operations import *
from . import cities, bot
from .keyboards import *
from .messages import *


# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------КОМАНДЫ--------------------------------------------------------------
@dp.message_handler(commands=['start'])
async def start_(message: types.Message):
    user_id = message.from_user.id
    reply_text = WELCOME_HAS_ACCOUNT
    user_new_state = WAIT_FOR_ACTION

    has_account = check_user_account(user_id)
    if not has_account:
        reply_text = WELCOME
        user_new_state = NEED_INVITE

    await message.answer(reply_text, reply_markup=types.ReplyKeyboardRemove())
    set_user_state(user_id, user_new_state)


@dp.message_handler(commands=['form'])
async def get_form_(message: types.Message):
    user_id = message.from_user.id
    user = get_user_by_tg_id(user_id)
    set_user_state(user_id, WAIT_FOR_ACTION)
    await message.answer(f"{user.name}\n{user.location}\n-------------\n{user.description}")
    await bot.send_photo(user_id, user.link_photo)


@dp.message_handler(commands=['keyboard'])
async def get_keyboard(message: types.Message):
    user_id = message.from_user.id
    if get_user_state(user_id) == "WAIT_FOR_ACTION":
        await message.answer(f"Клавиатура на месте", reply_markup=get_keyboard(user_id))
# ----------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------АНКЕТА---------------------------------------------------------------
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
        await message.answer("Прочитать приглашение по ссылке", reply_markup=agreement_link_keyboard)


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

    # state = GENDER_INPUT
    state = DESCRIPTION_INPUT
    ans = NAME_ACCEPTED
    keyboard = None

    if user and user.name:
        state = WAIT_FOR_ACTION
        ans = NEW_NAME_EDIT
        keyboard = get_keyboard(user_id)

    set_user_name(user_id, name)
    set_user_nickname(user_id, message.from_user.username)
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
    keyboard = types.ReplyKeyboardRemove()

    if user and user.gender:
        state = WAIT_FOR_ACTION
        ans = NEW_GENDER_EDIT
        keyboard = get_keyboard(user_id)

    set_user_gender(user_id, gender)
    set_user_state(user_id, state)
    await message.answer(ans, reply_markup=keyboard)


def check_description(desc):
    return len(desc) < 200


async def handle_description_input(message: types.Message, user_id, description):
    user = get_user_by_tg_id(user_id)
    if not check_description(description):
        await message.answer(DESC_ERROR, reply_markup=types.ReplyKeyboardRemove())
        return

    state = LOCATION_INPUT
    ans = DESK_ACCEPTED
    keyboard = types.ReplyKeyboardRemove()

    if user and user.description:
        state = WAIT_FOR_ACTION
        ans = NEW_DESCRIPTION_EDIT
        keyboard = get_keyboard(user_id)

    set_user_description(user_id, description)
    set_user_state(user_id, state)
    await message.answer(ans, reply_markup=keyboard)


async def handle_location_input(message: types.Message, user_id, location):
    user = get_user_by_tg_id(user_id)
    if not cities.check_location(location.capitalize()):
        await message.answer(LOCATION_ERROR, reply_markup=types.ReplyKeyboardRemove())
        return

    state = LINK_PHOTO_INPUT
    ans = LOCATION_ACCEPTED
    keyboard = types.ReplyKeyboardRemove()

    if user and user.location:
        state = WAIT_FOR_ACTION
        ans = NEW_LOCATION_EDIT
        keyboard = form_keyboard

    set_user_location(user_id, location)
    set_user_state(user_id, state)
    await message.answer(ans, reply_markup=keyboard)


def get_keyboard(user_id):
    if get_active(user_id):
        return form_keyboard
    return form_keyboard_flag


async def handle_actions(message: types.Message, user_id, text):
    if text == GET_FORM:
        user = get_user_by_tg_id(user_id)
        if not user:
            await message.answer(ERROR_KEYBOARD)
            return
        await bot.send_photo(user_id, user.link_photo)
        await message.answer(f"{user.name}\n{user.location}\n-------------\n{user.description}")

    elif text == EDIT_FORM:
        set_user_state(user_id, WAIT_FOR_ACTION)
        await message.answer(FORM_INFO, reply_markup=edit_keyboard)

    elif text == SHOW_USERS:
        current_user = get_next_show_user(user_id)
        if not current_user:
            await message.answer(NOT_ENOUGH_USERS)
            return

        await bot.send_photo(user_id, current_user.link_photo)
        await message.answer(f"{current_user.name}\n{current_user.location}\n-------------\n{current_user.description}")
        await message.answer("Выберите действие ниже", reply_markup=create_inline_keyboard(current_user.id))

    elif text == INVITE:
        await message.answer(get_invite_code(user_id))
    elif text == ACTIVE_FLAG:
        change_active(user_id)
        await message.answer("Анкета скрыта", reply_markup=get_keyboard(user_id))
    elif text == NOT_ACTIVE_FLAG:
        change_active(user_id)
        await message.answer("Анкета открыта", reply_markup=get_keyboard(user_id))

# ----------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------ОБРАБОТЧИК ТЕКСТА----------------------------------------------------
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
                        WAIT_FOR_ACTION: handle_actions,
                        }

    function = handle_functions.get(state)
    if function:
        await function(message, user_id, text)
# ----------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------ОБРАБОТЧИК ФОТО------------------------------------------------------
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    user_id = str(message.from_user.id)
    photo_id = message.photo[0].file_id
    user = get_user_by_tg_id(user_id)
    state = WAIT_FOR_ACTION
    ans = PHOTO_ACCEPTED
    keyboard = types.ReplyKeyboardRemove()

    if user and user.link_photo:
        state = WAIT_FOR_ACTION
        ans = NEW_LINK_PHOTO_EDIT
        keyboard = form_keyboard

    set_user_link_photo(user_id, photo_id)
    await message.answer(ans, reply_markup=keyboard)
    set_user_state(user_id, state)

    await bot.send_photo(user_id, user.link_photo)
    await message.answer(f"{user.name}\n{user.location}\n-------------\n{user.description}")
    await message.answer("Выберите действие ниже", reply_markup=form_keyboard)
# ----------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------ОБРАБОТЧИК INLINE_BUTTON---------------------------------------------
@dp.callback_query_handler()
async def call_back_data(callback: types.CallbackQuery):
    data = callback.data
    user_id = callback.from_user.id

    if data[0] == "*":
        user = get_user_by_id(data[1:])
        tg_user = user.state

        if check_like(user_id, tg_user.tg_id):
            # await callback.message.answer(f"{MEETING}\n@{user.nickname}")
            await bot.edit_message_reply_markup(
                chat_id=callback.from_user.id,
                message_id=callback.message.message_id,
                reply_markup=None
            )
            await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id, text=f"{MEETING}\n@{user.nickname}")
            await bot.send_message(tg_user.tg_id, f"{MEETING}\n@{callback.from_user.username}")
        else:
            await bot.edit_message_reply_markup(
                chat_id=callback.from_user.id,
                message_id=callback.message.message_id,
                reply_markup=None
            )
            await bot.edit_message_text(chat_id=user_id,  message_id=callback.message.message_id, text=WAIT_FOR_LIKE)
           # await callback.message.answer(WAIT_FOR_LIKE)

        current_user = get_next_show_user(user_id)
        if not current_user:
            await callback.answer(NOT_ENOUGH_USERS)
            return

        await bot.send_photo(user_id, current_user.link_photo)
        await callback.message.answer(f"{current_user.name}\n{current_user.location}\n-------------\n{current_user.description}")
        await callback.message.answer("Выберите действие ниже", reply_markup=create_inline_keyboard(current_user.id))


    elif data[0] == "&":
        user = get_user_by_id(data[1:])
        tg_user = user.state
        create_dislike(user_id, tg_user.tg_id)
        await bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None
        )
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id, text=SKIP_USER_MESSAGE)
        # await callback.message.answer(SKIP_USER_MESSAGE)
        current_user = get_next_show_user(user_id)

        if not current_user:
            await callback.answer(NOT_ENOUGH_USERS)
            return

        await bot.send_photo(user_id, current_user.link_photo)
        await callback.message.answer(
            f"{current_user.name}\n{current_user.location}\n-------------\n{current_user.description}")
        await callback.message.answer("Выберите действие ниже", reply_markup=create_inline_keyboard(current_user.id))


    else:
        actions = {NAME: (NAME_INPUT, NEW_NAME),
                   GENDER: (GENDER_INPUT, NEW_GENDER),
                   LOCATION: (LOCATION_INPUT, NEW_LOCATION),
                   DESCRIPTION: (DESCRIPTION_INPUT, NEW_DESCRIPTION),
                   LINK_PHOTO: (LINK_PHOTO_INPUT, NEW_LINK_PHOTO)}
        state, ans = actions.get(data)
        set_user_state(user_id, state)

        keyboard = types.ReplyKeyboardRemove() if data != GENDER else gender_keyboard
        await callback.message.answer(ans, reply_markup=keyboard)

    await callback.answer()


# @dp.callback_query_handler(text=LOVE_USER)
# async def call_main_menu(callback: types.CallbackQuery):
#     await bot.edit_message_reply_markup(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         reply_markup=None
#     )
