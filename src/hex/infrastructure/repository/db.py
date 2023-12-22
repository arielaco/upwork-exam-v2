from ..schemas.user import UserIn

from .security import fake_password_hasher
from .tables import UserInDB


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(
        **user_in.model_dump(),
        hashed_password=hashed_password,
    )
    print("User saved! ..not really")
    return user_in_db
