from sqlmodel import Field

from fastapi import HTTPException

from ...domain.models import UserBase


class UserIn(UserBase):
    password: str = Field(min_length=8, max_length=20)


class UserOut(UserBase):
    pass
