from sqlalchemy import Column, Integer, String,  ForeignKey, Date, Text
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(30))
    last_name = Column(String(30))
    gender = Column(String(1))
    love_gender = Column(String(1))
    link_photo = Column(String(50))
    description = Column(Text(200))
    location = Column(String(50))
    # is_active = Column(Boolean)
    invite_code = Column(String(10))

    likes_from = relationship("Like", back_populates="user_from", foreign_keys="Like.from_user_id")
    likes_to = relationship("Like", back_populates="user_to", foreign_keys="Like.to_user_id")
    state = relationship("State", back_populates="user", foreign_keys="State.user_id")

    def __repr__(self):
        return f"<User({self.id} {self.name},{self.last_name})>"


class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    from_user_id = Column(Integer, ForeignKey('user.id'))
    to_user_id = Column(Integer, ForeignKey('user.id'))

    user_from = relationship("User", foreign_keys=[from_user_id], back_populates="likes_from")
    user_to = relationship("User", foreign_keys=[to_user_id], back_populates="likes_to")

    def __repr__(self):
        return f"<Like({self.subject} to {self.object})>"


class State(Base):
    __tablename__ = 'like'
    tg_id = Column(Integer, nullable=False, unique=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    value = Column(String(10))
    user = relationship("User", back_populates="state")

    def __repr__(self):
        return f"<State({self.tg_id} {self.value})>"

