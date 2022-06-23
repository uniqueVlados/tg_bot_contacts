from bot_configs.handlers import *
from aiogram.utils import executor
from database import Base, engine


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    executor.start_polling(dp)
