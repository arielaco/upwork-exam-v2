import pytest

from jose import jwt

from fastapi import status
from fastapi.testclient import TestClient

from ..src.hex.application.use_cases.auth import ALGORITHM


# @pytest.mark.skip
@pytest.mark.order(2)
@pytest.mark.parametrize(
    ", ".join(
        [
            "username",
            "password",
            "status_code",
            "happy_path",
        ]
    ),
    [
        (
            "user_00@server-00.com",
            "password123",
            status.HTTP_200_OK,
            True,
        ),
        (
            "user_00@server-00.com",
            "123password",
            status.HTTP_401_UNAUTHORIZED,
            False,
        ),
        (
            "user_00@server-00.com",
            "",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
        (
            "user_00@server-00.com",
            "123password",
            status.HTTP_401_UNAUTHORIZED,
            False,
        ),
        (
            "user_03@server-01.xyz",
            "Pa$$w0rd123xyz",
            status.HTTP_200_OK,
            True,
        ),
        (
            "user_04@server-02.com",
            "",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
        (
            "",
            "password123",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
        (
            "",
            "",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
    ],
)
def test_login(
    client: TestClient,
    username,
    password,
    status_code,
    happy_path,
):
    response = client.post(
        "api/v1/users/login/",
        data={
            "username": username,
            "password": password,
        },
    )
    print(response.json())
    assert response.status_code == status_code
    if happy_path:
        assert "access_token" in response.json()
        assert jwt.get_unverified_header(
            response.json()["access_token"],
        ) == {
            "alg": ALGORITHM,
            "typ": "JWT",
        }
    else:
        assert "detail" in response.json()
