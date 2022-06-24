from database.operations import *
from . import dp
from .messages import *
from aiogram import types
from states import *


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
        await message.answer(agreement_mess, reply_markup=agreement_keyboard)  # TODO: создать agreement_keyboard


async def handle_name_input(message: types.Message, user_id, name):
    bad_symbols = {' ', '\n', '\t', '\r', ',', '.', '/', '>', '<', '\\', '|', ':',
                   ';', '\'', '"', '`', '~', '!', '@', '#', '$', '%', '^', '&',
                   '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', '?', '№'}
    if bad_symbols & set(name):
        await message.answer(NAME_ERROR)
        return

    await message.answer(NAME_ACCEPTED)
    set_user_state(user_id, LAST_NAME_INPUT)

# все остальные обработчики. Все обработчики принимают 3 параметра: message, user_id, text


# обработчик текстовых сообщений
@dp.message_handler()
async def handle_messages(message: types.Message):
    user_id = message.from_user.id
    state = get_user_state(user_id)
    text = message.text

    handle_functions = {NEED_INVITE: handle_invite_code,
                        # добавить все остальные состояния
                        }

    function = handle_functions.get(state)
    if function:
        await function(message, user_id, text)


# Обработчик для inline-кнопок
@dp.callback_query_handler()
async def call_back_data(callback: types.CallbackQuery):
    data = callback.data
    user_id = callback.from_user.id

    if data == AGREE:
        set_user_state(user_id, WAIT_FOR_ACTION)
        await callback.message.answer(AGREEMENT_ACCEPTED)
        await callback.message.answer(CREATE_ACCOUNT)
        set_user_state(callback.from_user.id, NAME_INPUT)

    elif data == DISAGREE:
        await callback.message.answer(AGREEMENT_NOT_ACCEPTED)
        await callback.message.answer(AGREEMENT_MESSAGE, reply_markup=agreement_keyboard)  # TODO: создать agreement_keyboard



