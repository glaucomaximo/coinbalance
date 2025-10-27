"""
Entidade Wallet - Aggregate Root do domínio de carteiras
"""

from dataclasses import dataclass, field
from typing import Optional, List

from ..value_objects.wallet_address import WalletAddress
from ..value_objects.private_key import PrivateKey
from ..value_objects.public_key import PublicKey
from ..value_objects.balance import Balance
from ...shared.value_objects.timestamp import Timestamp
from ...shared.value_objects.money import Money
from ...shared.exceptions import InsufficientFundsError, ValidationError
from ...shared.domain_events.base import DomainEvent


@dataclass
class Wallet:
    """
    Entidade Wallet - Aggregate Root.

    Representa uma carteira digital que pode:
    - Armazenar saldo
    - Enviar e receber transações
    - Ser identificada por um endereço único

    Invariantes:
    - Saldo nunca pode ser negativo
    - Endereço deve ser único
    - Chaves privadas são imutáveis após criação
    """

    # Identity
    address: WalletAddress

    # Attributes
    name: str
    public_key: PublicKey
    private_key: PrivateKey
    balance: Balance
    created_at: Timestamp
    updated_at: Timestamp

    # Metadata
    is_active: bool = True
    metadata: dict = field(default_factory=dict)

    # Domain Events (não persistidos)
    _events: List[DomainEvent] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self):
        """Validação após inicialização"""
        self._validate()

    def _validate(self):
        """Valida invariantes do domínio"""
        if not self.name:
            raise ValidationError("Wallet name cannot be empty")

        if len(self.name) > 100:
            raise ValidationError("Wallet name too long (max 100 characters)")

        if not self.is_active and not self.balance.is_zero():
            raise ValidationError("Cannot deactivate wallet with non-zero balance")

    @classmethod
    def create(
        cls, name: str, password: Optional[str] = None, metadata: Optional[dict] = None
    ) -> "Wallet":
        """
        Factory method para criar uma nova carteira.

        Args:
            name: Nome da carteira
            password: Senha para criptografar a chave privada (opcional)
            metadata: Metadados adicionais

        Returns:
            Nova instância de Wallet
        """
        # Gerar chaves
        private_key = PrivateKey.generate()
        public_key = PublicKey.from_private_key(private_key.reveal())
        address = WalletAddress.from_public_key(public_key.value)

        # Criar carteira
        now = Timestamp.now()
        wallet = cls(
            address=address,
            name=name,
            public_key=public_key,
            private_key=private_key,
            balance=Balance.zero(),
            created_at=now,
            updated_at=now,
            metadata=metadata or {},
        )

        # Adicionar evento de domínio
        from ..events.wallet_created import WalletCreated

        wallet._add_event(
            WalletCreated(
                wallet_address=address.value,
                wallet_name=name,
                public_key=public_key.value,
            )
        )

        return wallet

    # ========== BALANCE OPERATIONS ==========

    def credit(self, amount: Money, reason: str = "Credit") -> None:
        """
        Credita valor na carteira.

        Args:
            amount: Valor a ser creditado
            reason: Motivo do crédito
        """
        if not amount.is_positive():
            raise ValidationError("Credit amount must be positive")

        old_balance = self.balance
        self.balance = self.balance.add(amount)
        self.updated_at = Timestamp.now()

        # Evento de domínio
        from ..events.balance_updated import BalanceUpdated

        self._add_event(
            BalanceUpdated(
                wallet_address=self.address.value,
                old_balance=old_balance.to_cnb(),
                new_balance=self.balance.to_cnb(),
                amount=amount.to_cnb(),
                operation="credit",
                reason=reason,
            )
        )

    def debit(self, amount: Money, reason: str = "Debit") -> None:
        """
        Debita valor da carteira.

        Args:
            amount: Valor a ser debitado
            reason: Motivo do débito

        Raises:
            InsufficientFundsError: Se saldo insuficiente
        """
        if not amount.is_positive():
            raise ValidationError("Debit amount must be positive")

        if not self.has_sufficient_balance(amount):
            raise InsufficientFundsError(
                f"Insufficient balance: {self.balance} < {amount}"
            )

        old_balance = self.balance
        self.balance = self.balance.subtract(amount)
        self.updated_at = Timestamp.now()

        # Evento de domínio
        from ..events.balance_updated import BalanceUpdated

        self._add_event(
            BalanceUpdated(
                wallet_address=self.address.value,
                old_balance=old_balance.to_cnb(),
                new_balance=self.balance.to_cnb(),
                amount=amount.to_cnb(),
                operation="debit",
                reason=reason,
            )
        )

    def has_sufficient_balance(self, amount: Money) -> bool:
        """Verifica se tem saldo suficiente"""
        return self.balance.is_sufficient_for(amount)

    # ========== WALLET MANAGEMENT ==========

    def activate(self) -> None:
        """Ativa a carteira"""
        if self.is_active:
            return

        self.is_active = True
        self.updated_at = Timestamp.now()

    def deactivate(self) -> None:
        """
        Desativa a carteira.

        Raises:
            ValidationError: Se carteira tem saldo
        """
        if not self.balance.is_zero():
            raise ValidationError("Cannot deactivate wallet with non-zero balance")

        self.is_active = False
        self.updated_at = Timestamp.now()

    def update_metadata(self, key: str, value: any) -> None:
        """Atualiza metadados"""
        self.metadata[key] = value
        self.updated_at = Timestamp.now()

    # ========== DOMAIN EVENTS ==========

    def _add_event(self, event: DomainEvent) -> None:
        """Adiciona evento de domínio"""
        self._events.append(event)

    def get_events(self) -> List[DomainEvent]:
        """Retorna eventos de domínio"""
        return self._events.copy()

    def clear_events(self) -> None:
        """Limpa eventos de domínio"""
        self._events.clear()

    # ========== IDENTITY ==========

    def __eq__(self, other: object) -> bool:
        """Igualdade baseada no endereço (identity)"""
        if not isinstance(other, Wallet):
            return False
        return self.address == other.address

    def __hash__(self) -> int:
        """Hash baseado no endereço"""
        return hash(self.address)

    def __str__(self) -> str:
        return f"Wallet({self.name}, {self.address.short()}, {self.balance})"

    def __repr__(self) -> str:
        return (
            f"Wallet(address={repr(self.address)}, "
            f"name='{self.name}', "
            f"balance={repr(self.balance)})"
        )

    # ========== SERIALIZATION ==========

    def to_dict(self, include_private_key: bool = False) -> dict:
        """
        Serializa carteira para dicionário.

        Args:
            include_private_key: Se deve incluir a chave privada (PERIGO!)
        """
        data = {
            "address": self.address.value,
            "name": self.name,
            "public_key": self.public_key.value,
            "balance": {
                "cnb": float(self.balance.to_cnb()),
                "satoshi": self.balance.to_satoshi(),
            },
            "created_at": self.created_at.value,
            "updated_at": self.updated_at.value,
            "is_active": self.is_active,
            "metadata": self.metadata,
        }

        if include_private_key:
            # ATENÇÃO: Nunca use isso em produção sem criptografia!
            data["private_key"] = self.private_key.reveal()

        return data
