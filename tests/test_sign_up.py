import pytest

from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.order(1)
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
            status.HTTP_201_CREATED,
            True,
        ),
        (
            "user_01@server-00.com",
            "password123",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            "user_02@server-00.com",
            "123password",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            "user_03@server-01.xyz",
            "Pa$$w0rd123xyz",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            "user_04@server-01.xyz",
            "123",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
        (
            "user_05@server-02.com",
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
        (
            "user_08",
            "password123",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
        (
            "user_00@server-00.com",
            "password123",
            status.HTTP_400_BAD_REQUEST,
            False,
        ),
    ],
)
# @pytest.mark.skip
def test_create_user(
    client: TestClient,
    username,
    password,
    status_code,
    happy_path,
):
    response = client.post(
        "api/v1/users/sign-up/",
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
    else:
        assert "detail" in response.json()
