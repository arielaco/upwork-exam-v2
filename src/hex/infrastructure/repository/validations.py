from sqlmodel import Session, select
from fastapi import HTTPException, status

from ...infrastructure.repository.tables import UserInDB


def check_if_email_is_in_use(session: Session, user_in_db: UserInDB):
    stmt = select(UserInDB).where(
        UserInDB.username == user_in_db.username,
    )
    users_with_same_username = session.exec(stmt).all()
    if len(users_with_same_username) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already in use.",
        )
