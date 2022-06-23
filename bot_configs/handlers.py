from database.operations import create_like
from . import dp
from .messages import *
from aiogram import types


@dp.message_handler(commands=['start'])
async def start_(message: types.Message):
    await message.reply(WELCOME)
    create_like()
