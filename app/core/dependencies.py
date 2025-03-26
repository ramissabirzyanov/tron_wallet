from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.service import WalletService
from app.db.repository import DB_Repository
from app.db.session import get_db


def get_wallet_service() -> WalletService:
    return WalletService()


def get_db_repository(db: AsyncSession = Depends(get_db)) -> DB_Repository:
    return DB_Repository(db)
