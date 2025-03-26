from sqlalchemy.future import select

from app.db.session import AsyncSession
from app.core.models import Wallet


class DB_Repository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_last_wallets(self, skip: int = 0, limit: int = 10):
        """ Получает список последних записей с пагинацией """
        query = select(Wallet).order_by(Wallet.timestamp.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def add_wallet(self, wallet_data: dict) -> Wallet:
        """Добавляет запрос кошелька в БД"""
        wallet = Wallet(
            address=wallet_data["wallet_address"],
            balance=wallet_data["trx_balance"],
            bandwidth=wallet_data["bandwidth"],
            energy=wallet_data["energy"],
        )
        self.db.add(wallet)
        await self.db.commit()
        await self.db.refresh(wallet)
        return wallet
