import pika
from starlette.testclient import TestClient


def test_errand():
    with TestClient(app) as client:
        response = client.post("/channel", json={})
        assert response.status_code == 400