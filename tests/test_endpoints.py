import pytest

from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from fastapi import status
from fastapi.testclient import TestClient

from ..src.main import app
from ..src.hex.infrastructure.repository.sqlite3 import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
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
        (
            "user_07",
            "password123",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
    ],
)
def test_create_user(
    client: TestClient,
    username,
    password,
    status_code,
    happy_path,
):
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
            "user_00@server_00.com",
            "password123",
            status.HTTP_200_OK,
            True,
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
