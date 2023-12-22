from fastapi import HTTPException
from ...infrastructure.schemas.user import UserIn
from ...infrastructure.repository.db import fake_save_user, login_user


def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    data = {
        "username": "user_00@server_00.com",
        "password": "password123",
    }
    if user_in.model_dump() == data:
        return {"response": "User created"}
    else:
        return HTTPException(status_code=404, detail="User not found")


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
