from sqlmodel import Session, select

from ..schemas.user import UserIn
from .tables import UserInDB


def create_user_in_db(session: Session, user_in: UserIn, hashed_password: str):
    user_in_db = UserInDB(
        **user_in.model_dump(),
        hashed_password=hashed_password,
    )
    session.add(user_in_db)
    session.commit()
    session.close()
    return user_in_db


def get_user_by_username(session: Session, username: str):
    statement = select(UserInDB).where(UserInDB.username == username)
    results = session.exec(statement)
    user = results.first()
    if not user:
        return False
    return user
