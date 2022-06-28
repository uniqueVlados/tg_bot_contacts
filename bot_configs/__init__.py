from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from .config import ConfigData
from parse_cities import Cities

config_data = ConfigData()
bot = Bot(token=config_data.BOT_TOKEN)
dp = Dispatcher(bot)
cities = Cities(config_data.FILENAME_CITIES)
