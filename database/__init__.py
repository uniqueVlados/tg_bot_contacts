from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bot_configs import config_data

engine = create_engine(config_data.DB_URI)
Base = declarative_base()

session_maker = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class DBContext:
    """Контекст обращения к бд (если бд нет, то создать; если есть, то вернуть ссылку на нее)"""

    def __init__(self):
        self.db = session_maker()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


def get_db():
    """Функция для получения текущей сессии к БД"""
    with DBContext() as session:
        return session
