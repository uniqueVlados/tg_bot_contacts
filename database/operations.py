import secrets
from datetime import datetime

from database.models import User, Like, State, Dislike
from . import get_db


def check_like(from_user_id: int, to_user_id: int):
    """ Проверяет лайк на взаимность между пользователями """
    db = get_db()

    mutual_like = db.query(Like).filter((Like.from_user_id == to_user_id) & (Like.to_user_id == from_user_id)).first()
    if mutual_like:
        return True

    return False


def get_all_likes():
    """ Получает всех пользователей из бд"""
    db = get_db()
    return db.query(Like).all()


def get_liked_users(user_id: int):
    """ Возвращает всех пользователей, которых лайкнул пользователь """
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
    alp = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    return ''.join(secrets.choice(alp) for i in range(8))


def check_invite_code(invite_code: str):
    """ Проверяет код приглашения"""
    db = get_db()
    if len(invite_code) != 8:
        return False
    return bool(db.query(User).filter(User.invite_code == invite_code).first())


def set_user_name(user_id, name):
    """ Устанавливает имя пользователя """
    db = get_db()
    user = get_user_by_tg_id(user_id)
    if not user:
        user = User(name=name, invite_code=create_invite_code())
        db.add(user)
        db.commit()
        state = db.query(State).filter(State.tg_id == user_id).first()
        state.user_id = user.id

    user.name = name
    db.commit()


def set_user_gender(user_id, gender):
    """ Устанавливает пол пользователю """
    db = get_db()
    user = get_user_by_tg_id(user_id)
    user.gender = gender
    db.commit()


def set_user_nickname(user_id, nickname):
    """ Устанавливает пол пользователю """
    db = get_db()
    user = get_user_by_tg_id(user_id)
    user.nickname = nickname
    db.commit()


def set_user_description(user_id, description):
    """ Устанавливает описание пользователю """
    db = get_db()
    user = get_user_by_tg_id(user_id)
    user.description = description
    db.commit()


def set_user_location(user_id, location):
    """ Устанавливает местоположение пользователю """
    db = get_db()
    user = get_user_by_tg_id(user_id)
    user.location = location
    db.commit()


def set_user_link_photo(user_id, link):
    """ Устанавливает описание пользователю """
    db = get_db()
    user = get_user_by_tg_id(user_id)
    if not user.link_photo:
        user.is_active = True
    user.link_photo = link
    db.commit()


# def get_next_show_user(user_id: int):
#     """ Получает следующего пользователя для показа """
#     db = get_db()
#     all_users_count = db.query(User).count()
#     all_active_users = db.query(User).filter(User.is_active == True).count()
#
#     if all_users_count < 4:
#         return None
#
#     user = get_user_by_tg_id(user_id)
#     if not user.show_user_id:
#         user.show_user_id = 1
#
#     next_user = db.query(User).filter(User.id == user.show_user_id).first()
#
#     counter = 0
#     user.show_user_id += 1
#     if user.show_user_id > all_users_count - 1:
#         user.show_user_id = 1
#
#     while (not db.query(User).filter(User.id == user.show_user_id).first().is_active
#            or user.show_user_id == user.id) \
#             or get_dislike(user_id, db.query(State).filter(State.user_id == user.show_user_id).first().tg_id) \
#             or get_like(user_id, db.query(State).filter(State.user_id == user.show_user_id).first().tg_id):
#         user.show_user_id += 1
#
#         if user.show_user_id > all_users_count - 1:
#             user.show_user_id = 1
#
#         counter += 1
#         if counter >= all_users_count:
#             return None
#
#     # if user.show_user_id == user.id:
#     #     user.show_user_id += 1
#     #
#     # if user.show_user_id > all_users_count - 1:
#     #     user.show_user_id = 1
#
#     db.commit()
#     return next_user


def get_next_show_user(user_id: int):
    """ Получает следующего пользователя для показа """
    db = get_db()
    user = get_user_by_tg_id(user_id)
    next_user_id = user.show_user_id

    # Получаем всех активных пользователей
    next_active_users = db.query(User).filter((User.is_active == True) &
                                              (User.id != user.id)).all()

    next_active_users = list(filter(lambda user_: user_.id > next_user_id and user_.id != user.id, next_active_users)) + \
                        list(filter(lambda user_: user_.id < next_user_id and user_.id != user.id, next_active_users))

    if not next_active_users:
        return None

    for next_user in next_active_users:
        if not get_dislike(user_id, next_user.state.tg_id) \
                and not get_like(user_id, next_user.state.tg_id):
            user.show_user_id = next_user.id
            return next_user

    return None


def change_active(user_id):
    db = get_db()
    user = get_user_by_tg_id(user_id)
    user.is_active = not user.is_active
    db.commit()


def get_active(user_id):
    user = get_user_by_tg_id(user_id)
    return user and user.is_active


def get_invite_code(user_id):
    user = get_user_by_tg_id(user_id)
    return user.invite_code


def create_dislike(from_user_id, to_user_id):
    """ Дизлайк для пользователя"""
    db = get_db()
    has_like = db.query(Dislike).filter((Dislike.from_user_id == from_user_id) & (Dislike.to_user_id == to_user_id)).first()
    if has_like:
        return True

    dislike = Dislike(from_user_id=from_user_id, to_user_id=to_user_id)
    db.add(dislike)
    db.commit()


def create_like(from_user_id, to_user_id):
    """ Дизлайк для пользователя"""
    db = get_db()
    has_like = db.query(Like).filter((Like.from_user_id == from_user_id) & (Like.to_user_id == to_user_id)).first()
    if has_like:
        return True

    like = Like(from_user_id=from_user_id, to_user_id=to_user_id)
    db.add(like)
    db.commit()


def get_dislike(from_user_id, to_user_id):
    """" Получает дизлайк """
    db = get_db()
    dislike = db.query(Dislike).filter((Dislike.from_user_id == from_user_id) & (Dislike.to_user_id == to_user_id)).first()
    if dislike and dislike.date_to_delete < datetime.now().date():
        db.delete(dislike)
        db.commit()
        return None

    return bool(dislike)


def get_like(from_user_id, to_user_id):
    """" Получает лайк """
    db = get_db()
    like = db.query(Like).filter((Like.from_user_id == from_user_id) & (Like.to_user_id == to_user_id)).first()
    if like and like.date_to_delete < datetime.now().date():
        db.delete(like)
        db.commit()
        return None

    return bool(like)
