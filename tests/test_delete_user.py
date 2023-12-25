import pytest

from jose import jwt

from fastapi import status
from fastapi.testclient import TestClient

from ..src.hex.application.use_cases.auth import ALGORITHM


# @pytest.mark.skip
@pytest.mark.order(3)
@pytest.mark.parametrize(
    ", ".join(
        [
            "username",
            "password",
            "with_token",
            "status_code",
            "happy_path",
        ]
    ),
    [
        (
            "user_00@server-00.com",
            "password123",
            True,
            status.HTTP_200_OK,
            True,
        ),
        (
            "user_00@server-00.com",
            "password123",
            False,
            status.HTTP_401_UNAUTHORIZED,
            False,
        ),
        (
            "user_01@server-00.com",
            "password123",
            True,
            status.HTTP_200_OK,
            True,
        ),
        (
            "user_02@server-00.com",
            "123password",
            True,
            status.HTTP_200_OK,
            True,
        ),
        (
            "user_03@server-01.xyz",
            "Pa$$w0rd123xyz",
            True,
            status.HTTP_200_OK,
            True,
        ),
    ],
)
def test_delete_user(
    client: TestClient,
    username,
    password,
    with_token,
    status_code,
    happy_path,
):
    login_response = client.post(
        "api/v1/users/login/",
        data={
            "username": username,
            "password": password,
        },
    )
    if with_token:
        headers = {
            "Authorization": " ".join(
                [
                    "Bearer",
                    login_response.json()["access_token"],
                ]
            )
        }
    else:
        headers = {}
    response = client.post(
        "api/v1/users/delete/",
        json={
            "username": username,
            "password": password,
        },
        headers=headers,
    )
    assert response.status_code == status_code
    if happy_path:
        assert "response" in response.json()
    else:
        assert "detail" in response.json()
