import asyncio

from tronpy import Tron
from tronpy.exceptions import AddressNotFound


class WalletService:
    def __init__(self, network: str = "shasta"):
        self.client = Tron(network=network)

    async def is_valid_tron_address(self, wallet_address: str):
        if await asyncio.to_thread(self.client.is_address, wallet_address):
            return True
        raise ValueError(f"Неверный TRON-адрес: {wallet_address}")

    async def get_wallet_data(self, wallet_address: str):
        """ Получает баланс, bandwidth и energy, включая использованные и лимиты """
        try:
            await self.is_valid_tron_address(wallet_address)
            account, resource_info = await asyncio.gather(
                asyncio.to_thread(self.client.get_account, wallet_address),
                asyncio.to_thread(self.client.get_account_resource, wallet_address)
            )
            balance = account.get("balance", 0) / 1_000_000

            bandwidth_limit = resource_info.get("freeNetLimit", 0)
            bandwidth_used = resource_info.get("freeNetUsed", 0)
            bandwidth_available = max(bandwidth_limit - bandwidth_used, 0)

            energy_limit = resource_info.get("energyLimit", 0)
            energy_used = resource_info.get("energyUsed", 0)
            energy_available = max(energy_limit - energy_used, 0)

            wallet_data = {
                "wallet_address": wallet_address,
                "trx_balance": balance,
                "bandwidth": {
                    "limit": bandwidth_limit,
                    "used": bandwidth_used,
                    "available": bandwidth_available
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
