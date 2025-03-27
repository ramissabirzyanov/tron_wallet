from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class WalletInfoRequest(BaseModel):
    address: str


class WalletInfoResponse(BaseModel):
    address: str
    balance: Decimal
    bandwidth: dict
    energy: dict
    timestamp: datetime = datetime.now()

    class Config:
        from_attributes = True
