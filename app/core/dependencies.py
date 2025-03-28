from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.service import WalletService
from app.db.repository import DB_Repository
from app.db.session import get_db


def get_wallet_service() -> WalletService:
    """
    Возвращает экземпляр сервиса для работы с кошельками.
    Используется для внедрения зависимости в FastAPI, чтобы предоставить
    экземпляр сервиса WalletService в маршрутах
    """
    return WalletService()


def get_db_repository(db: AsyncSession = Depends(get_db)) -> DB_Repository:
    """
    Возвращает экземпляр репозитория для работы с базой данных.

    """
    return DB_Repository(db)
