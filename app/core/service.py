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

            bandwidth_free_limit = resource_info.get("freeNetLimit", 0)
            bandwidth_total_limit = resource_info.get("TotalNetLimit", 0)

            energy_total_limit = resource_info.get("TotalEnergyLimit", 0)
            energy_used = resource_info.get("energyUsed", 0)

            wallet_data = {
                "wallet_address": wallet_address,
                "trx_balance": balance,
                "bandwidth": {
                    "free_limit": bandwidth_free_limit,
                    "total_limit": bandwidth_total_limit,
                },
                "energy": {
                    "limit": energy_total_limit,
                    "used": energy_used,
                }
            }

            return wallet_data

        except AddressNotFound:
            return {"error": "Wallet address not found"}
