from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, MetaData, ForeignKey, Date, Boolean
from . import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(128))
    last_name = Column(String(128))
    link_photo = Column(String(128))
    description = Column(String(128))
    location = Column(String(128))
    last_use = Column(Date)
    is_active = Column(Boolean)

    def __repr__(self):
        return f"<User({self.name},{self.last_name})>"