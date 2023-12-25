import pytest

from jose import jwt
from sqlmodel import Session, SQLModel, create_engine

from fastapi import status
from fastapi.testclient import TestClient

from ..src.main import app
from ..src.hex.application.use_cases.auth import ALGORITHM
from ..src.hex.infrastructure.repository.sqlite3 import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///testing.db",
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


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
