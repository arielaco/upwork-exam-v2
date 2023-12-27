import random
import pytest

from fastapi import status
from fastapi.testclient import TestClient


random_number = random.randrange(0, 99999, 1)


@pytest.mark.skip
@pytest.mark.order(4)
@pytest.mark.parametrize(
    ", ".join(
        [
            "username",
            "password",
            "name",
            "description",
            "status_code",
            "happy_path",
        ]
    ),
    [
        (
            f"user_{random_number}@server-00.com",
            "password123",
            "user1 name1 adress1",
            "Profile test A",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            f"user_{random_number}@server-00.com",
            "password123",
            "user2 name2 adress2",
            "Profile test B",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            f"user_{random_number}@server-00.com",
            "password123",
            "user3 name3 adress3",
            "Profile test C",
            status.HTTP_201_CREATED,
            True,
        ),
    ],
)
def test_create_profile(
    client: TestClient,
    username,
    password,
    name,
    description,
    status_code,
    happy_path,
):
    client.post(
        "api/v1/users/sign-up/",
        json={
            "username": username,
            "password": password,
        },
    )
    login_response = client.post(
        "api/v1/users/login/",
        data={
            "username": username,
            "password": password,
        },
    )
    auth_token = login_response.json()["access_token"]
    create_profile_response = client.post(
        "api/v1/users/profile/",
        json={
            "name": name,
            "description": description,
        },
        headers={
            "Authorization": f"Bearer {auth_token}",
        },
    )
    assert create_profile_response.status_code == status_code
    if happy_path:
        assert "description" in create_profile_response.json()
        assert "name" in create_profile_response.json()
        assert "user" in create_profile_response.json()
        assert "username" in create_profile_response.json()["user"]
    else:
        assert "detail" in create_profile_response.json()


@pytest.mark.skip
@pytest.mark.order(5)
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
            f"user_{random_number}@server-00.com",
            "password123",
            status.HTTP_200_OK,
            True,
        ),
    ],
)
def test_get_profile(
    client: TestClient,
    username,
    password,
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
    access_token = login_response.json()["access_token"]
    print("+++++++++++++++++++++++++++++++++++++++++ auth_token")
    print(access_token)
    get_profile_response = client.get(
        "api/v1/users/profile/",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    print(get_profile_response.json())
    assert get_profile_response.status_code == status_code
    # if happy_path:
    #     assert "description" in get_profile_response.json()
    #     assert "name" in get_profile_response.json()
    #     assert "user" in get_profile_response.json()
    #     assert "username" in get_profile_response.json()["user"]
    # else:
    #     assert "detail" in get_profile_response.json()
    # assert False
