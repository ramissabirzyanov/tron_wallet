import asyncio
from datetime import datetime
from typing import Optional

from tronpy import Tron
from tronpy.exceptions import AddressNotFound

from app.core.settings import settings


class WalletService:
    """
    Сервис для работы с кошельками.
    Этот класс предоставляет методы для проверки действительности адресов кошельков,
    получения данных о кошельке, таких как баланс, лимиты и использование bandwidth и энергии.
    """

    def __init__(self, network: str = settings.TRON_NETWORK):
        """
        Инициализирует сервис с указанной сетью TRON.
        """
        self.client = Tron(network=network)

    async def is_valid_tron_address(self, wallet_address: str) -> bool:
        """
        Проверяет, является ли указанный адрес валидным адресом TRON.
        """
        if await asyncio.to_thread(self.client.is_address, wallet_address):
            return True
        raise ValueError(f"Неверный TRON-адрес: {wallet_address}")

    async def get_wallet_data(self, wallet_address: str) -> Optional[dict]:
        """ Получает данные о кошельке, включая баланс, bandwidth и energy,
        а также их лимиты и использование.
        Метод собирает информацию о кошельке с помощью библиотеки tronpy и
        возвращает структурированные данные, включая баланс и ресурсы.
        """
        try:
            await self.is_valid_tron_address(wallet_address)
            account, resource_info = await asyncio.gather(
                asyncio.to_thread(self.client.get_account, wallet_address),
                asyncio.to_thread(self.client.get_account_resource, wallet_address)
            )
            balance = account.get("balance", 0) / 1_000_000

            free_bandwidth_limit = resource_info.get("freeNetLimit", 0)
            free_bandwidth_used = resource_info.get("freeNetUsed", 0)
            free_bandwidth_available = max(free_bandwidth_limit - free_bandwidth_used, 0)

            staked_bandwidth_limit = resource_info.get("NetLimit", 0)
            staked_bandwidth_used = resource_info.get("NetUsed", 0)
            staked_bandwidth_available = max(staked_bandwidth_limit - staked_bandwidth_used, 0)

            energy_limit = resource_info.get("energyLimit", 0)
            energy_used = resource_info.get("energyUsed", 0)
            energy_available = max(energy_limit - energy_used, 0)

            wallet_data = {
                "address": wallet_address,
                "balance": balance,
                "timestamp": datetime.now(),
                "bandwidth": {
                    "free": {
                        "limit": free_bandwidth_limit,
                        "used": free_bandwidth_used,
                        "available": free_bandwidth_available
                    },
                    "staked": {
                        "limit": staked_bandwidth_limit,
                        "used": staked_bandwidth_used,
                        "available": staked_bandwidth_available
                    }
                },
                "energy": {
                    "limit": energy_limit,
                    "used": energy_used,
                    "available": energy_available
                }
            }

            return wallet_data

        except AddressNotFound:
            return {"error": "Wallet address not found"}
