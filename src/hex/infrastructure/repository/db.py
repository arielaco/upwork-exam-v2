from sqlmodel import Session

from ..schemas.user import UserIn

from .security import fake_password_hasher
from .tables import UserInDB


def save_user(session: Session, user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(
        **user_in.model_dump(),
        hashed_password=hashed_password,
    )
    session.add(user_in_db)
    session.commit()
    session.close()
    return user_in_db


def login_user(user_in: UserIn):
    return "jwt"
