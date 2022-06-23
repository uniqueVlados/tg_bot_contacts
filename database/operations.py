from . import get_db
from database.models import User, Like, State


def create_like(from_user_id: int, to_user_id: int):
    """Создает лайк между пользователями """
    like = Like(from_user_id=from_user_id, to_user_id=to_user_id)
    db = get_db()
    db.add(like)
    db.commit()


def get_all_likes():
    """ Получает всех пользователей из бд"""
    db = get_db()
    return db.query(Like).all()


def get_liked_users(user_id: int):
    """ Возвращает все пользователей, которых лайкнул пользователь """
    db = get_db()
    return db.query(Like).filter(Like.from_user_id == user_id).all()


def get_user_likes(user_id: int):
    """ Возвращает все пользователей, которые лайкнули пользователя """
    db = get_db()
    return db.query(Like).filter(Like.to_user_id == user_id).all()


def create_user(params):
    """ Создает пользователя в бд """
    user = User(**params)
    db = get_db()
    db.add(user)

    state = db.query(State).filter(State.user_id == user.id).first()
    state.user_id = user.id

    db.commit()

