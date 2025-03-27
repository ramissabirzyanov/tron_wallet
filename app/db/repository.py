from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert

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
        try:
            query = insert(Wallet).values(**wallet_data).on_conflict_do_update(
                index_elements=["address"],
                set_={
                    "balance": wallet_data["balance"],
                    "bandwidth": wallet_data["bandwidth"],
                    "energy": wallet_data["energy"],
                    "timestamp": wallet_data["timestamp"],
                }
            )
        except KeyError:
            raise KeyError("Check wallet_data")
        await self.db.execute(query)
        await self.db.commit()
