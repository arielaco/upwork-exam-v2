from pydantic import EmailStr
from sqlmodel import Field

from ...domain.models import UserBase


class UserIn(UserBase):
    username: EmailStr = Field(unique=True)
    password: str = Field(min_length=8, max_length=20)


class UserOut(UserBase):
    pass
