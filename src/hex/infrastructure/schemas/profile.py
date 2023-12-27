from pydantic import EmailStr
from sqlmodel import SQLModel, Field

from ...domain.models import ProfileBase
from .user import UserOut


class ProfileIn(ProfileBase):
    pass


class ProfileOut(ProfileBase):
    user: UserOut
