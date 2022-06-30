import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean, func
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    nickname = Column(String(20))
    name = Column(String(30))
    gender = Column(String(1))
    link_photo = Column(String(50))
    description = Column(Text(200))
    location = Column(String(50))
    invite_code = Column(String(8))
    show_user_id = Column(Integer, ForeignKey("user.id"))
    is_active = Column(Boolean, default=True)

    likes_from = relationship("Like", back_populates="user_from", foreign_keys="Like.from_user_id")
    likes_to = relationship("Like", back_populates="user_to", foreign_keys="Like.to_user_id")
    state = relationship("State", back_populates="user", foreign_keys="State.user_id", uselist=False)

    def __repr__(self):
        return f"<User({self.id} {self.name})>"


class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    from_user_id = Column(Integer, ForeignKey('user.id'))
    to_user_id = Column(Integer, ForeignKey('user.id'))

    user_from = relationship("User", foreign_keys=[from_user_id], back_populates="likes_from", uselist=False)
    user_to = relationship("User", foreign_keys=[to_user_id], back_populates="likes_to", uselist=False)

    def __repr__(self):
        return f"<Like({self.from_user_id} to {self.to_user_id})>"


class Dislike(Base):
    __tablename__ = 'dislike'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    from_user_id = Column(Integer, ForeignKey('user.id'))
    to_user_id = Column(Integer, ForeignKey('user.id'))
    date = Column(Date, default=func.now())
    date_to_delete = Column(Date, default=func.now() + datetime.timedelta(days=14))

    user_from = relationship("User", foreign_keys=[from_user_id], back_populates="likes_from", uselist=False)
    user_to = relationship("User", foreign_keys=[to_user_id], back_populates="likes_to", uselist=False)

    def __repr__(self):
        return f"<Dislike({self.subject} to {self.object})>"


class State(Base):
    __tablename__ = 'state'

    tg_id = Column(String(9), nullable=False, unique=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    value = Column(String(10))

    user = relationship("User", back_populates="state", uselist=False)

    def __repr__(self):
        return f"<State({self.tg_id} {self.value})>"

