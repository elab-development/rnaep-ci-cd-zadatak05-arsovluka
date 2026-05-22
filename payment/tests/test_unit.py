from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from payment.main import create_order


@pytest.mark.asyncio
async def test_create_order_calculates_total_and_fee():
    body = {
        "id": "product-1",
        "quantity": 2
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "price": 100
    }

    with patch("payment.main.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )

        with patch("payment.main.Order") as mock_order:
            order_instance = MagicMock()
            mock_order.return_value = order_instance

            background_tasks = MagicMock()

            result = await create_order(body, background_tasks)

            mock_order.assert_called_once_with(
                product_id="product-1",
                price=100,
                fee=20.0,
                total=240.0,
                quantity=2,
                status="pending"
            )

            order_instance.save.assert_called_once()
            background_tasks.add_task.assert_called_once()

            assert result == order_instance

