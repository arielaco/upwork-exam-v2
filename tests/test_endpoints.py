import pytest

from fastapi import status
from fastapi.testclient import TestClient

from ..src.main import app


@pytest.mark.parametrize(
    "username, password, status_code, happy_path",
    [
        (
            "user@server.com",
            "password123",
            status.HTTP_201_CREATED,
            True,
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
    if happy_path:
        assert response.status_code == status_code
        assert response.json() == {
            "response": "User created",
        }


@pytest.mark.parametrize(
    "username, password, status_code, happy_path",
    [
        (
            "user@server.com",
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
