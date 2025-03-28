import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repository import DB_Repository


@pytest.fixture(scope="session")
def mock_db_session():
    """
    Мокаем сессию базы данных (AsyncSession) для тестов.
    Эта фикстура создаёт и настраивает mock-объект для работы с сессией базы данных.
    """
    session = AsyncMock(spec=AsyncSession)
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    return session


@pytest.fixture
def mock_repository(mock_db_session):
    """
    Мокаем репозиторий для работы с базой данных.
    Эта фикстура создаёт объект репозитория DB_Repository с замоканной сессией базы данных.
    """
    repo = DB_Repository(mock_db_session)
    return repo


@pytest.fixture
def test_wallet_data():
    """
    Мокаем данные кошелька для тестов.
    Эта фикстура возвращает фиктивные данные кошелька в виде словаря,
    которые могут быть использованы в тестах.
    """
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
