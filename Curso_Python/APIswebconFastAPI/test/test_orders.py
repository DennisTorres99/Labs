from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def get_token():
    response = client.post(
        "/login",
        json={"username": "dennis", "password": "1234"},
    )
    return response.json()["access_token"]


def test_login():
    response = client.post(
        "/login",
        json={"username": "dennis", "password": "1234"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_order():
    token = get_token()

    response = client.post(
        "/orders/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "description": "Orden Test",
            "items": [{"name": "Item1", "quantity": 2}],
        },
    )

    assert response.status_code == 200
    assert response.json()["description"] == "Orden Test"


def test_get_orders():
    token = get_token()

    response = client.get(
        "/orders/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_orders_requires_auth():
    response = client.get("/orders/")

    assert response.status_code in (401, 403)
