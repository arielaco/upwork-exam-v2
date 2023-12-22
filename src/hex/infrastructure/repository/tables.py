from ...domain.models import UserBase


class UserInDB(UserBase):
    hashed_password: str
