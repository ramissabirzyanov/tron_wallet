from fastapi import APIRouter, Depends, HTTPException, status

from app.core.schemas import WalletInfoRequest, WalletInfoResponse
from app.core.service import WalletService
from app.db.repository import DB_Repository
from app.core.dependencies import get_db_repository, get_wallet_service


router = APIRouter(prefix='/api')


@router.post('/wallet_info', response_model=WalletInfoResponse)
async def get_wallet_info(
    request: WalletInfoRequest,
    db_repo: DB_Repository = Depends(get_db_repository),
    wallet_service: WalletService = Depends(get_wallet_service)
):
    """
    Получение информации о кошельке и его сохранение в базе данных.
    Эта функция обрабатывает POST-запрос, получая данные о кошельке по адресу.
    Сначала она запрашивает информацию о кошельке через сервис `WalletService`,
    а затем сохраняет данные в базе данных с помощью репозитория `DB_Repository`.
    """
    wallet_data = await wallet_service.get_wallet_data(request.address)
    if not wallet_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='check wallet address')
    await db_repo.add_wallet(wallet_data)
    return wallet_data


@router.get('/wallets', response_model=list[WalletInfoResponse])
async def get_last_wallets(
    db_repo: DB_Repository = Depends(get_db_repository)
):
    """
    Получение списка последних записей о кошельках.
    """
    wallets = await db_repo.get_last_wallets()
    return [
        WalletInfoResponse(
            address=w.address,
            balance=w.balance,
            bandwidth=w.bandwidth,
            energy=w.energy,
            query_time=w.timestamp
        ) for w in wallets
    ]
