"""
Use Case: Obter Carteira (Query - CQRS)
"""

from dataclasses import dataclass

from ...common.interfaces.use_case import UseCase
from src.domain.wallet.repositories.wallet_repository import WalletRepository
from src.domain.wallet.value_objects.wallet_address import WalletAddress
from src.domain.shared.exceptions import EntityNotFoundError


@dataclass
class GetWalletQuery:
    """Query para obter uma carteira"""

    address: str


@dataclass
class GetWalletResult:
    """Resultado da consulta de carteira"""

    address: str
    name: str
    public_key: str
    balance_cnb: float
    balance_satoshi: int
    created_at: float
    updated_at: float
    is_active: bool
    metadata: dict


class GetWalletQueryHandler(UseCase[GetWalletQuery, GetWalletResult]):
    """
    Handler para query de obter carteira.

    Responsabilidades:
    - Buscar carteira via repository
    - Retornar dados formatados
    """

    def __init__(self, wallet_repository: WalletRepository):
        self.wallet_repository = wallet_repository

    async def execute(self, query: GetWalletQuery) -> GetWalletResult:
        """Executa a busca de carteira"""

        # 1. Criar value object de endereço
        address = WalletAddress.create(query.address)

        # 2. Buscar no repository
        wallet = await self.wallet_repository.find_by_address(address)

        if not wallet:
            raise EntityNotFoundError(
                f"Wallet with address '{query.address}' not found",
                code="WALLET_NOT_FOUND",
            )

        # 3. Retornar resultado
        return GetWalletResult(
            address=wallet.address.value,
            name=wallet.name,
            public_key=wallet.public_key.value,
            balance_cnb=float(wallet.balance.to_cnb()),
            balance_satoshi=wallet.balance.to_satoshi(),
            created_at=wallet.created_at.value,
            updated_at=wallet.updated_at.value,
            is_active=wallet.is_active,
            metadata=wallet.metadata,
        )
