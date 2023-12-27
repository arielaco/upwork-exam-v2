from sqlmodel import Relationship, Field

from ...domain.models import UserBase, ProfileBase


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

    profiles: list["Profile"] = Relationship(back_populates="user")


class Profile(ProfileBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="profiles")
