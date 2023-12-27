from sqlmodel import Session, select

from ..schemas.profile import ProfileIn
from ..schemas.user import UserIn
from .tables import User, Profile


def create_user_in_db(session: Session, user_in: UserIn, hashed_password: str):
    user = User(
        **user_in.model_dump(),
        hashed_password=hashed_password,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()
    return user


def get_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    user = results.first()
    if not user:
        return False
    return user


def get_user_by_id(session: Session, user_id: int):
    statement = select(User).where(User.id == user_id)
    results = session.exec(statement)
    user = results.first()
    if not user:
        return False
    return user


def delete_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    user = results.first()
    session.delete(user)
    session.commit()
    session.close()
    return results


def create_profile_in_db(session: Session, user_id: int, profile_in: ProfileIn):
    profile = Profile(
        **profile_in.model_dump(),
        user_id=user_id,
    )
    session.add(profile)
    session.commit()
    session.refresh(profile)
    session.close()
    return profile
