from sqlmodel import Session

from ...infrastructure.schemas.profile import ProfileIn, ProfileOut
from ...infrastructure.repository.db import (
    create_profile_in_db,
    get_user_by_id,
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
    print(profile_out)
    return profile_out
