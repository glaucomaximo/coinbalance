"""
Entidade Transaction - Aggregate Root do domínio de transações
"""

from dataclasses import dataclass, field
from typing import Optional, List
from decimal import Decimal
from enum import Enum

from ..value_objects.transaction_id import TransactionId
from ..value_objects.transaction_amount import TransactionAmount
from ..value_objects.transaction_fee import TransactionFee
from ...shared.value_objects.wallet_address import WalletAddress
from ...shared.value_objects.timestamp import Timestamp
from ...shared.value_objects.money import Money
from ...shared.exceptions import ValidationError, InsufficientFundsError
from ...shared.domain_events.base import DomainEvent


class TransactionStatus(Enum):
    """Status possíveis de uma transação"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TransactionType(Enum):
    """Tipos de transação"""
    TRANSFER = "transfer"
    STAKE = "stake"
    UNSTAKE = "unstake"
    REWARD = "reward"
    FEE = "fee"
    GENESIS = "genesis"


@dataclass
class Transaction:
    """
    Entidade Transaction - Aggregate Root.
    
    Representa uma transação na blockchain que pode:
    - Transferir CNB entre carteiras
    - Registrar operações de staking
    - Processar recompensas
    - Cobrar taxas
    
    Invariantes:
    - Valor deve ser positivo
    - Remetente deve ter saldo suficiente
    - Taxa deve ser válida
    - Status deve ser consistente
    """
    
    # Identity
    id: TransactionId
    
    # Participants
    from_address: Optional[WalletAddress]
    to_address: WalletAddress
    
    # Transaction details
    amount: TransactionAmount
    fee: TransactionFee
    transaction_type: TransactionType
    status: TransactionStatus
    
    # Timestamps
    created_at: Timestamp
    confirmed_at: Optional[Timestamp] = None
    
    # Blockchain data
    block_height: Optional[int] = None
    transaction_hash: Optional[str] = None
    
    # Metadata
    memo: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    
    # Domain Events (não persistidos)
    _events: List[DomainEvent] = field(default_factory=list, init=False, repr=False)
    
    def __post_init__(self):
        """Validação após inicialização"""
        self._validate()
    
    def _validate(self):
        """Valida invariantes do domínio"""
        if not self.to_address:
            raise ValidationError("Destination address is required")
        
        if self.from_address == self.to_address:
            raise ValidationError("Cannot send to same address")
        
        if self.amount.value.to_cnb() <= 0:
            raise ValidationError("Transaction amount must be positive")
        
        if self.fee.value.to_cnb() < 0:
            raise ValidationError("Transaction fee cannot be negative")
        
        if self.status == TransactionStatus.CONFIRMED and not self.confirmed_at:
            raise ValidationError("Confirmed transactions must have confirmation timestamp")
    
    @classmethod
    def create_transfer(
        cls,
        from_address: WalletAddress,
        to_address: WalletAddress,
        amount: Money,
        fee: Money,
        memo: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> "Transaction":
        """
        Cria uma nova transação de transferência.
        
        Args:
            from_address: Endereço do remetente
            to_address: Endereço do destinatário
            amount: Valor a ser transferido
            fee: Taxa da transação
            memo: Memo opcional
            metadata: Metadados adicionais
            
        Returns:
            Nova transação de transferência
        """
        transaction = cls(
            id=TransactionId.generate(),
            from_address=from_address,
            to_address=to_address,
            amount=TransactionAmount(amount),
            fee=TransactionFee(fee),
            transaction_type=TransactionType.TRANSFER,
            status=TransactionStatus.PENDING,
            created_at=Timestamp.now(),
            memo=memo,
            metadata=metadata or {}
        )
        
        # Adicionar evento de domínio
        from ..events.transaction_created import TransactionCreated
        transaction._events.append(TransactionCreated(
            transaction_id=transaction.id,
            from_address=from_address,
            to_address=to_address,
            amount=amount,
            transaction_type=TransactionType.TRANSFER
        ))
        
        return transaction
    
    @classmethod
    def create_stake(
        cls,
        wallet_address: WalletAddress,
        amount: Money,
        fee: Money,
        metadata: Optional[dict] = None
    ) -> "Transaction":
        """
        Cria uma nova transação de staking.
        
        Args:
            wallet_address: Endereço da carteira
            amount: Valor para stake
            fee: Taxa da transação
            metadata: Metadados adicionais
            
        Returns:
            Nova transação de staking
        """
        transaction = cls(
            id=TransactionId.generate(),
            from_address=wallet_address,
            to_address=wallet_address,  # Staking é para a mesma carteira
            amount=TransactionAmount(amount),
            fee=TransactionFee(fee),
            transaction_type=TransactionType.STAKE,
            status=TransactionStatus.PENDING,
            created_at=Timestamp.now(),
            metadata=metadata or {}
        )
        
        # Adicionar evento de domínio
        from ..events.transaction_created import TransactionCreated
        transaction._events.append(TransactionCreated(
            transaction_id=transaction.id,
            from_address=wallet_address,
            to_address=wallet_address,
            amount=amount,
            transaction_type=TransactionType.STAKE
        ))
        
        return transaction
    
    @classmethod
    def create_reward(
        cls,
        validator_address: WalletAddress,
        amount: Money,
        block_height: int,
        metadata: Optional[dict] = None
    ) -> "Transaction":
        """
        Cria uma nova transação de recompensa.
        
        Args:
            validator_address: Endereço do validador
            amount: Valor da recompensa
            block_height: Altura do bloco
            metadata: Metadados adicionais
            
        Returns:
            Nova transação de recompensa
        """
        transaction = cls(
            id=TransactionId.generate(),
            from_address=None,  # Recompensas vêm do sistema
            to_address=validator_address,
            amount=TransactionAmount(amount),
            fee=TransactionFee(Money(Decimal("0"))),  # Recompensas não têm taxa
            transaction_type=TransactionType.REWARD,
            status=TransactionStatus.CONFIRMED,  # Recompensas são confirmadas automaticamente
            created_at=Timestamp.now(),
            confirmed_at=Timestamp.now(),
            block_height=block_height,
            metadata=metadata or {}
        )
        
        return transaction
    
    def confirm(self, block_height: int, transaction_hash: str) -> None:
        """
        Confirma a transação.
        
        Args:
            block_height: Altura do bloco onde foi confirmada
            transaction_hash: Hash da transação no blockchain
        """
        if self.status != TransactionStatus.PENDING:
            raise ValidationError(f"Cannot confirm transaction with status {self.status}")
        
        self.status = TransactionStatus.CONFIRMED
        self.confirmed_at = Timestamp.now()
        self.block_height = block_height
        self.transaction_hash = transaction_hash
        
        # Adicionar evento de domínio
        from ..events.transaction_confirmed import TransactionConfirmed
        self._events.append(TransactionConfirmed(
            transaction_id=self.id,
            block_height=block_height,
            transaction_hash=transaction_hash
        ))
    
    def fail(self, reason: str) -> None:
        """
        Marca a transação como falhada.
        
        Args:
            reason: Motivo da falha
        """
        if self.status != TransactionStatus.PENDING:
            raise ValidationError(f"Cannot fail transaction with status {self.status}")
        
        self.status = TransactionStatus.FAILED
        self.metadata["failure_reason"] = reason
        
        # Adicionar evento de domínio
        from ..events.transaction_failed import TransactionFailed
        self._events.append(TransactionFailed(
            transaction_id=self.id,
            reason=reason
        ))
    
    def cancel(self, reason: str) -> None:
        """
        Cancela a transação.
        
        Args:
            reason: Motivo do cancelamento
        """
        if self.status not in [TransactionStatus.PENDING]:
            raise ValidationError(f"Cannot cancel transaction with status {self.status}")
        
        self.status = TransactionStatus.CANCELLED
        self.metadata["cancellation_reason"] = reason
        
        # Adicionar evento de domínio
        from ..events.transaction_cancelled import TransactionCancelled
        self._events.append(TransactionCancelled(
            transaction_id=self.id,
            reason=reason
        ))
    
    def get_total_amount(self) -> Money:
        """Retorna o valor total (amount + fee)"""
        return self.amount.value + self.fee.value
    
    def is_confirmed(self) -> bool:
        """Verifica se a transação está confirmada"""
        return self.status == TransactionStatus.CONFIRMED
    
    def is_pending(self) -> bool:
        """Verifica se a transação está pendente"""
        return self.status == TransactionStatus.PENDING
    
    def is_valid(self) -> bool:
        """
        Valida se a transação é válida.
        
        Returns:
            True se a transação for válida, False caso contrário
        """
        try:
            # Validar endereço de destino
            if not self.to_address:
                return False
            
            # Validar que não está enviando para o mesmo endereço (exceto para staking)
            if (self.from_address and 
                self.from_address == self.to_address and 
                self.transaction_type != TransactionType.STAKE):
                return False
            
            # Validar valor positivo
            if self.amount.value.to_cnb() <= 0:
                return False
            
            # Validar taxa não negativa
            if self.fee.value.to_cnb() < 0:
                return False
            
            # Validar timestamp de criação
            if not self.created_at:
                return False
            
            # Validar que transações confirmadas têm timestamp de confirmação
            if (self.status == TransactionStatus.CONFIRMED and 
                not self.confirmed_at):
                return False
            
            # Validar que transações confirmadas têm altura de bloco
            if (self.status == TransactionStatus.CONFIRMED and 
                self.block_height is None):
                return False
            
            # Validar hash da transação se existir
            if self.transaction_hash and len(self.transaction_hash) < 10:
                return False
            
            return True
            
        except Exception:
            return False
    
    def get_events(self) -> List[DomainEvent]:
        """Retorna eventos de domínio pendentes"""
        return self._events.copy()
    
    def clear_events(self) -> None:
        """Limpa eventos de domínio processados"""
        self._events.clear()
