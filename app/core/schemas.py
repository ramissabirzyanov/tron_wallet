from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class WalletInfoRequest(BaseModel):
    wallet_address: str


class WalletInfoResponse(BaseModel):
    wallet_address: str
    trx_balance: Decimal
    bandwidth: dict
    energy: dict
    query_time: datetime = datetime.now()

    class Config:
        from_attributes = True
