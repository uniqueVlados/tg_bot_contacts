import secrets

from database.models import User, Like, State
from . import get_db


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


def set_user_state(tg_user_id: int, value: str):
    """ Устанавливает состояние пользователя """
    db = get_db()
    state = db.query(State).filter(State.tg_id == tg_user_id).first()
    if not state:
        state = State(tg_id=tg_user_id, value=value)
        db.add(state)

    state.value = value
    db.commit()


def get_all_users():
    """ Получает всех пользователей из бд """
    db = get_db()
    return db.query(User).all()


def create_invite_code():
    """ Создает код приглашения для пользователя """
    alp = "ERTYUIOPASDFGHJKLZXCVBNM1234567890"
    return ''.join(secrets.choice(alp) for i in range(8))


def check_invite_code(invite_code: str):
    """ Проверяет код приглашения"""
    db = get_db()
    return bool(db.query(User.invite_code == invite_code).first())


def set_user_name(user_id, name):
    """ Устанавливает имя пользователя """
    db = get_db()
    user = get_user_by_tg_id(user_id)
    if not user:
        user = User(name=name, invite_code=create_invite_code())
        db.add(user)

    user.name = name
    db.commit()


def set_user_gender(user_id, gender):
    """ Устанавливает пол пользователю """
    db = get_db()
    user = get_user_by_tg_id(user_id)
    user.gender = gender
    db.commit()


def set_user_description(user_id, description):
    """ Устанавливает описание пользователю """
    db = get_db()
    user = get_user_by_tg_id(user_id)
    user.description = description
    db.commit()



def set_user_location(user_id, location):
    """ Устанавливает описание пользователю """
    db = get_db()
    user = get_user_by_tg_id(user_id)
    user.location = location
    db.commit()

