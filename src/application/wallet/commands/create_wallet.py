"""
Use Case: Criar Carteira (Command - CQRS)
"""

from dataclasses import dataclass
from typing import Optional

from ...common.interfaces.use_case import UseCase
from src.domain.wallet.entities.wallet import Wallet
from src.domain.wallet.repositories.wallet_repository import WalletRepository
from src.domain.shared.exceptions import DuplicateEntityError
from src.domain.shared.domain_events.dispatcher import get_event_dispatcher


@dataclass
class CreateWalletCommand:
    """
    Command para criar uma nova carteira.

    Este é o DTO (Data Transfer Object) que transfere dados
    da camada de apresentação para a aplicação.
    """

    name: str
    password: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class CreateWalletResult:
    """Resultado da criação de carteira"""

    address: str
    name: str
    public_key: str
    balance: float
    created_at: float


class CreateWalletCommandHandler(UseCase[CreateWalletCommand, CreateWalletResult]):
    """
    Handler para o comando de criar carteira.

    Responsabilidades:
    - Validar dados de entrada
    - Verificar se carteira já existe
    - Criar entidade de domínio
    - Persistir via repository
    - Despachar eventos de domínio
    """

    def __init__(self, wallet_repository: WalletRepository):
        self.wallet_repository = wallet_repository
        self.event_dispatcher = get_event_dispatcher()

    async def execute(self, command: CreateWalletCommand) -> CreateWalletResult:
        """Executa a criação de carteira"""

        # 1. Verificar se já existe carteira com o mesmo nome
        existing = await self.wallet_repository.find_by_name(command.name)
        if existing:
            raise DuplicateEntityError(
                f"Wallet with name '{command.name}' already exists",
                code="WALLET_NAME_ALREADY_EXISTS",
            )

        # 2. Criar entidade de domínio (Aggregate Root)
        wallet = Wallet.create(
            name=command.name, password=command.password, metadata=command.metadata
        )

        # 3. Persistir via repository
        await self.wallet_repository.save(wallet)

        # 4. Despachar eventos de domínio
        for event in wallet.get_events():
            await self.event_dispatcher.dispatch(event)

        wallet.clear_events()

        # 5. Retornar resultado
        return CreateWalletResult(
            address=wallet.address.value,
            name=wallet.name,
            public_key=wallet.public_key.value,
            balance=float(wallet.balance.to_cnb()),
            created_at=wallet.created_at.value,
        )
