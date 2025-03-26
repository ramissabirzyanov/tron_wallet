from datetime import datetime, timezone
from app.db.base import Base

from sqlalchemy import Integer, String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column


class Wallet(Base):
    __tablename__ = "wallet_queries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    address: Mapped[str] = mapped_column(String, index=True)
    balance: Mapped[int] = mapped_column(Integer)
    bandwidth: Mapped[JSON] = mapped_column(JSON)
    energy: Mapped[JSON] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
