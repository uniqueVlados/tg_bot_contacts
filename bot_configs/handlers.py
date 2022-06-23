from database.operations import create_like
from . import dp
from .messages import *
from aiogram import types
from states import *


@dp.message_handler(commands=['start'])
async def start_(message: types.Message):
    user_id = message.from_user.id

    has_account = check_user_account(user_id)
    if not has_account:
        reply_text = WELCOME
        user_new_state = NEED_INVITE

    reply_text = WELCOME_HAS_ACCOUNT
    user_new_state = WAIT_FOR_ACTION

    await message.reply(reply_text)
    change_user_state(user_id, user_new_state)


