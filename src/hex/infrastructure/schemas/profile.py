from sqlmodel import SQLModel

from ...domain.models import ProfileBase
from ...infrastructure.repository.tables import Profile
from .user import UserOut


class ProfileIn(ProfileBase):
    pass


class ProfileOut(ProfileBase):
    user: UserOut


class UserProfilesOut(SQLModel):
    user: UserOut
    profiles: list[Profile]


class OtherProfilesOut(SQLModel):
    profiles: list[Profile]
