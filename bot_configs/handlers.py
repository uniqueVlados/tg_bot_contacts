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

    await message.reply(reply_text)
    set_user_state(user_id, user_new_state)


async def handle_invite_code(message, params):
    answer = NOT_CHECK_INVITE
    if check_invite_code(params["invite"]):
        answer = CHECK_INVITE
        set_user_state(message.from_user.id, WAIT_FOR_ACTION)
    await message.reply(answer)


@dp.message_handler()
async def handle_messages(message: types.Message):
    user_id = message.from_user.id
    state = get_user_state(user_id)



