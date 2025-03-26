from pydantic import BaseModel
from datetime import datetime


class WalletInfoRequest(BaseModel):
    wallet_address: str

class WalletInfoResponse(BaseModel):
    wallet_address: str
    trx_balance: int
    bandwidth: int
    energy: int
    query_time: datetime

    class Config:
        from_attributes = True
