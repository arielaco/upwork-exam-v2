from datetime import timedelta
from typing import Annotated

from sqlmodel import Session

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ...infrastructure.repository.tables import UserInDB
from ...application.exceptions import (
    INCORRECT_USERNAME_OR_PASSWORD_EXCEPTION,
)
from ...domain.models import UserBase
from ...application.use_cases.user import create_user
from ...application.use_cases.auth import (
    authenticate_user,
    get_current_user,
)
from ...infrastructure.repository.sqlite3 import get_session
from ..schemas.user import UserIn, Token


router = APIRouter(prefix="/users")


@router.post(
    "/sign-up/",
    status_code=status.HTTP_201_CREATED,
)
async def create_user_endpoint(
    *,
    session: Session = Depends(get_session),
    user_in: UserIn,
):
    response = create_user(session, user_in)
    return response


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    response_model=Token,
)
async def login_for_access_token(
    *,
    session: Session = Depends(get_session),
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    response = authenticate_user(
        session,
        form_data.username,
        form_data.password,
    )
    return response


# @router.post(
#     "/delete/",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def read_users_me(
#     current_user: Annotated[UserInDB, Depends(get_current_user)]
# ):
#     return current_user
