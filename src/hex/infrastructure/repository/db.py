from sqlmodel import Session, select

from ..schemas.user import UserIn

from .security import fake_password_hasher
from .tables import UserInDB
from .validations import check_if_email_is_in_use


def user_save(session: Session, user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(
        **user_in.model_dump(),
        hashed_password=hashed_password,
    )
    check_if_email_is_in_use(session, user_in_db)
    session.add(user_in_db)
    session.commit()
    session.close()
    return user_in_db


def user_get(session: Session):
    users_in_db = session.exec(select(UserInDB)).all()
    print(users_in_db)
    return users_in_db


def login_user(user_in: UserIn):
    return "jwt"
