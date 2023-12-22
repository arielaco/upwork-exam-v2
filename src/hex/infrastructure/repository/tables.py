from sqlmodel import Field

from ...domain.models import UserBase


class UserInDB(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
