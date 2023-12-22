from fastapi.testclient import TestClient

from ..src.main import app


def test_create_user():
    client = TestClient(app)
    response = client.post(
        "api/v1/sign-up/",
        json={
            "username": "user@server.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "response": "User created",
    }


def test_login():
    client = TestClient(app)
    response = client.post(
        "api/v1/login/",
        json={
            "username": "user@server.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "token": "jwt",
    }
