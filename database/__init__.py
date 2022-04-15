from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from bot_configs import config_data

db = create_engine(config_data.DATABASE_PATH)
Base = declarative_base()


if __name__ == "__main__":
    Base.metadata.create_all(db)
