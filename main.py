from bot_configs.handlers import *
from aiogram.utils import executor
from bot_configs import dp


if __name__ == '__main__':
    executor.start_polling(dp)
