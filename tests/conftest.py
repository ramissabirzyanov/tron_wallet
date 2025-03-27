import requests
import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def test_wallet_data():
    """Фикстура для получения реальных данных кошелька"""

    url = "https://api.shasta.trongrid.io/wallet/getaccount"
    payload = {
        "address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
        "visible": True
    }
    headers = {"accept": "application/json", "content-type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    return data

@pytest.fixture
def mock_wallet_service():
    service = AsyncMock()
    service.get_wallet_data = AsyncMock()
    return service

@pytest.fixture
def mock_repository():
    repo = AsyncMock()
    repo.add_wallet = AsyncMock()
    repo.get_last_wallets = AsyncMock(return_value=[])
    return repo

@pytest.fixture
def unit_test_mock_wallet():
    wallet_data = {
        "address": "MockAddress",
        "balance": 100.0,
        "timestamp": "2025-03-27T00:00:00",
        "bandwidth": {
            "free": {"limit": 1000, "used": 100, "available": 900},
            "staked": {"limit": 5000, "used": 1000, "available": 4000}
        },
        "energy": {"limit": 10000, "used": 2000, "available": 8000}
    }

    return wallet_data
