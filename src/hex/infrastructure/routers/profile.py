from typing import Annotated

from sqlmodel import Session

from fastapi import APIRouter, status, Depends

from ...application.use_cases.auth import get_current_user
from ...application.use_cases.profile import create_profile
from ...infrastructure.schemas.profile import ProfileIn, ProfileOut
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
    response = create_profile(session, current_user.id, profile_in)
    return response


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    # response_model=ProfileOut,
)
async def get_profile_endpoint(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_user)],
):
    # response = authenticate_user(
    #     session,
    #     form_data.username,
    #     form_data.password,
    # )
    return {}
