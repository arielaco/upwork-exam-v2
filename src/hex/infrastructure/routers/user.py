from fastapi import APIRouter, status

from ..schemas.user import UserIn

from ...application.use_cases.user import create_user, login


router = APIRouter()


@router.post(
    "/sign-up/",
    status_code=status.HTTP_201_CREATED,
)
async def create_user_endpoint(user_in: UserIn):
    response = create_user(user_in)
    return response


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
)
async def login_endpoint(user_in: UserIn):
    response = login(user_in)
    return response
