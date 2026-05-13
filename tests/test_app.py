import pytest
from app import app, init_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    init_db()
    with app.test_client() as client:
        yield client

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Simple User Management App" in response.data

def test_add_user(client):
    response = client.post("/add", data={"name": "Ali"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Ali" in response.data