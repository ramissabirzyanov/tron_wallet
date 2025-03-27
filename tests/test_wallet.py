import pytest
from unittest.mock import patch
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_with_data_from_tron_api(test_wallet_data, mock_wallet_service, mock_repository):
    test_address = "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g"
    mock_wallet_service.get_wallet_data.return_value = test_wallet_data
    
    with (
        patch("app.core.dependencies.get_wallet_service", return_value=mock_wallet_service),
        patch("app.core.dependencies.get_db_repository", return_value=mock_repository)
    ):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/wallet_info",
                json={"address": test_address}
            )
        
            data = response.json()
            assert response.status_code == 200
            assert data["address"] == test_wallet_data["address"]
            assert data["balance"] == str(test_wallet_data["balance"]/1000000)
            assert "bandwidth" in data
            assert "energy" in data
            assert 'free','staked'in data['bandwidth']
            assert 'available' in data['energy']
            # Добавим вывод для диагностики
            print(f"add_wallet called {mock_repository.add_wallet.call_count} times.")
            print(f"Arguments passed: {mock_repository.add_wallet.call_args}")