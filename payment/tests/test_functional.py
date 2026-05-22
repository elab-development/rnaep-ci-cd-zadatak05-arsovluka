from fastapi.testclient import TestClient
from unittest.mock import patch

from payment.main import app


client = TestClient(app)


def test_get_order_not_found():
    with patch("payment.main.Order.get", side_effect=Exception()):
        response = client.get("/orders/non-existing-id")

    assert response.status_code in [404, 500]


