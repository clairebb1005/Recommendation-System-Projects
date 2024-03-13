from fastapi.testclient import TestClient
from app import app

import pytest


@pytest.fixture
def client():
    client = TestClient(app)
    return client


def test_get_root(client):
    response = client.get("/")
    print(response)
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Book Recommendation API!"}

