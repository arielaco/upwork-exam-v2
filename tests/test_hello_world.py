from fastapi.testclient import TestClient

from ..src.main import app


def test_create_user():
    client = TestClient(app)
    url_path = "hello/"
    response = client.get(url_path)
    assert response.status_code == 200
