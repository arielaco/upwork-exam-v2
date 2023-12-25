import logging

from pydantic import EmailStr
from sqlmodel import Session, select

from ...application.exceptions import EMAIL_ALREADY_USED_EXCEPTION
from ...infrastructure.repository.tables import UserInDB


def check_email_in_use(session: Session, email: EmailStr):
    statement = select(UserInDB).where(UserInDB.username == email)
    users_with_same_username = session.exec(statement).all()
    if len(users_with_same_username) > 0:
        logging.error("This email is already in use.")
        raise EMAIL_ALREADY_USED_EXCEPTION
