from ...domain.models import UserBase


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass
