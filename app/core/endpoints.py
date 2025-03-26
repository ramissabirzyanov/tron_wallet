from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import WalletInfoRequest, WalletInfoResponse
from app.db.session import get_db


router = APIRouter(prefix='api')


@router.post('/wallet', response_model=WalletInfoResponse)
async def get_wallet_info(
    request: WalletInfoRequest,
    session: Depends(),
    db: Depends(get_db)
):
    pass
