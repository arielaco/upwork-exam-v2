from sqlmodel import Session

from ...infrastructure.repository.tables import Profile, User
from ...infrastructure.schemas.profile import (
    ProfileIn,
    ProfileOut,
    UserProfilesOut,
)
from ...infrastructure.repository.db import (
    create_profile_in_db,
    get_user_by_id,
    get_profiles_by_user_id,
)


def create_profile(
    session: Session,
    user_id: int,
    profile_in: ProfileIn,
) -> ProfileOut:
    profile = create_profile_in_db(session, user_id, profile_in)
    user = get_user_by_id(session, user_id)
    profile_out = ProfileOut(
        name=profile.name,
        description=profile.description,
        user=user,
    )
    return profile_out


def get_profiles(session: Session, user: User) -> list[Profile]:
    profiles = get_profiles_by_user_id(session, user.id)
    return [profile for profile in profiles]
