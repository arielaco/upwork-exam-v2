from sqlmodel import Session
from fastapi import HTTPException

from ...infrastructure.schemas.user import UserIn
from ...infrastructure.repository.db import save_user, login_user


def create_user(session: Session, user_in: UserIn):
    save_user(session, user_in)
    return {"response": "User created"}


def login(user_in: UserIn):
    token_jwt = login_user(user_in)
    data = {
        "username": "user_00@server_00.com",
        "password": "password123",
    }
    if user_in.model_dump() == data:
        return {"token": token_jwt}
    else:
        return HTTPException(status_code=404, detail="User not found")
