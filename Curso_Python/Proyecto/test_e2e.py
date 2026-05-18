from api import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_create_and_get_orders():
    response = client.post("/orders?id=1&total=100")
    assert response.status_code == 200

    response = client.get("/orders")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data[0]["id"] == 1
    assert data[0]["total"] == 100
