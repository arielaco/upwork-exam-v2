from ...infrastructure.schemas.user import UserIn
from ...infrastructure.repository.db import fake_save_user


def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return {"response": "User created"}
