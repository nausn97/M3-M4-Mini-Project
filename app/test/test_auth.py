from starlette import status
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_user():
    response = client.get('/auth/user')
    assert response.status_code == status.HTTP_200_OK