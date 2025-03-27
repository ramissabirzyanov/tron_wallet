from decimal import Decimal
from datetime import datetime
from app.db.base import Base

from sqlalchemy import Integer, String, DateTime, JSON, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column


class Wallet(Base):
    __tablename__ = "wallet_queries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    address: Mapped[str] = mapped_column(String, index=True, unique=True)
    balance: Mapped[Decimal] = mapped_column(DECIMAL)
    bandwidth: Mapped[JSON] = mapped_column(JSON)
    energy: Mapped[JSON] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(DateTime)
