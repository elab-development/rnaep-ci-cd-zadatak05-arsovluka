from unittest.mock import patch, MagicMock
from payment.main import Order


def test_order_model_creation():
    with patch.object(Order, "save") as mock_save:

        order = Order(
            product_id="abc123",
            price=50,
            fee=10,
            total=60,
            quantity=1,
            status="pending"
        )

        order.save()

        mock_save.assert_called_once()

        assert order.product_id == "abc123"
        assert order.total == 60
        assert order.status == "pending"


