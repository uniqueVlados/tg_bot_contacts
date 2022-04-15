from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from .config import ConfigData


config_data = ConfigData()
bot = Bot(token=config_data.BOT_TOKEN)
dp = Dispatcher(bot)
