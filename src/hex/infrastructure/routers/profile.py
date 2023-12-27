from typing import Annotated

from sqlmodel import Session

from fastapi import APIRouter, status, Depends

from ...infrastructure.schemas.profile import (
    ProfileIn,
    ProfileOut,
    UserProfilesOut,
)
from ...application.use_cases.auth import get_current_user
from ...application.use_cases.profile import create_profile, get_profiles
from ...infrastructure.repository.tables import User
from ...infrastructure.repository.sqlite3 import get_session


router = APIRouter(prefix="/profile")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProfileOut,
)
async def create_profile_endpoint(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_user)],
    profile_in: ProfileIn,
):
    response = create_profile(
        session,
        current_user.id,
        profile_in,
    )
    return response


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserProfilesOut,
)
async def get_profile_endpoint(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_user)],
):
    profiles = get_profiles(session, current_user)
    response = UserProfilesOut(user=current_user, profiles=profiles)
    return response
