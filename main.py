from bot_configs import debug_manager
from bot_configs.handlers import *
from aiogram.utils import executor
from database import Base, engine
import sys

DEBUG_MODE = True

if __name__ == '__main__':
    if DEBUG_MODE:
        sys.stderr = debug_manager
    Base.metadata.create_all(engine)
    executor.start_polling(dp)
