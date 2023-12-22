import pytest

from fastapi import status
from fastapi.testclient import TestClient

from ..src.main import app


@pytest.mark.parametrize(
    "username, password, status_code, happy_path",
    [
        (
            "user_00@server_00.com",
            "password123",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            "user_01@server_00.com",
            "password123",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            "user_02@server_00.com",
            "123password",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            "user_03@server_01.xyz",
            "Pa$$w0rd123xyz",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            "user_04@server_00.com",
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
def test_create_user(username, password, status_code, happy_path):
    client = TestClient(app)
    response = client.post(
        "api/v1/sign-up/",
        json={
            "username": username,
            "password": password,
        },
    )
    assert response.status_code == status_code
    if happy_path:
        assert response.json() == {
            "response": "User created",
        }


@pytest.mark.parametrize(
    "username, password, status_code, happy_path",
    [
        (
            "user_00@server_00.com",
            "password123",
            status.HTTP_200_OK,
            True,
        ),
    ],
)
def test_login(username, password, status_code, happy_path):
    client = TestClient(app)
    response = client.post(
        "api/v1/login/",
        json={
            "username": username,
            "password": password,
        },
    )
    if happy_path:
        assert response.status_code == status_code
        assert response.json() == {
            "token": "jwt",
        }
