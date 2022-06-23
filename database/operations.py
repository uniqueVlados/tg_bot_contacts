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


def check_user_account(tg_user_id: int):
    """ Проверяет наличие аккаунта пользователя """
    db = get_db()
    state = db.query(State).filter(State.tg_id == tg_user_id).first()
    if state is None or state.user is None:
        return False

    return True


def get_user_by_tg_id(tg_user_id: int):
    """ Получает пользователя по его tg_id """
    db = get_db()
    state = db.query(State).filter(State.tg_id == tg_user_id).first()
    if state is None or state.user is None:
        return None

    return state.user


def get_user_by_id(user_id: int):
    """ Получает пользователя по его id """
    db = get_db()
    return db.query(User).filter(User.id == user_id).first()


def get_user_state(tg_user_id: int):
    """ Получает состояние пользователя """
    db = get_db()
    state = db.query(State).filter(State.tg_id == tg_user_id).first()

    if not state:
        return None

    return state.value


