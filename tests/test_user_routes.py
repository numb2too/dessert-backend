import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_get_user_success(client):
    res = client.get("/api/users/1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["name"] == "Alice"

def test_get_user_not_found(client):
    res = client.get("/api/users/999")
    assert res.status_code == 404

def test_add_user(client):
    res = client.post(
        "/api/users/",
        json={"name": "Tony", "email": "tony@test.com"},
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["name"] == "Tony"
