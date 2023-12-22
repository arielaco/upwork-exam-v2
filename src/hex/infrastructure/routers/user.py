from sqlmodel import Session
from fastapi import APIRouter, status, Depends

from ...application.use_cases.user import create_user, login
from ...infrastructure.repository.sqlite3 import get_session

from ..schemas.user import UserIn


router = APIRouter()


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
)
async def login_endpoint(user_in: UserIn):
    response = login(user_in)
    return response
