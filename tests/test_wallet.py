import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.repository import DB_Repository


@pytest.mark.asyncio
async def test_with_data_from_tron_api():
    """
    Тестируем API метод /api/wallet_info, который получает информацию о кошельке
    с Tron-сети по указанному адресу. Данные для корректности запроса взяты с API Tron.
    """
    test_address = "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/wallet_info",
            json={"address": test_address}
        )
        data = response.json()
        assert response.status_code == 200
        assert data["address"] == test_address
        assert data["balance"] == str(12818721520 / 1000000)
        assert "bandwidth" in data
        assert "energy" in data
        assert 'free', 'staked' in data['bandwidth']
        assert 'available' in data['energy']


@pytest.mark.asyncio
async def test_unit_add_wallet_to_db(mock_db_session, test_wallet_data):
    """Тестируем метод add_wallet отдельно, без FastAPI"""
    repo = DB_Repository(mock_db_session)

    await repo.add_wallet(test_wallet_data)
    sql_call = mock_db_session.execute.call_args[0][0]

    assert mock_db_session.execute.call_count == 1
    assert mock_db_session.commit.call_count == 1
    assert sql_call.table.name == "wallet_queries"
