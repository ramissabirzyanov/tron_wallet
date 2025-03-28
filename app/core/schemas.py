from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(
        from_attributes=True
    )
