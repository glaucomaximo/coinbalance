"""
Eventos de domínio para transações
"""

from dataclasses import dataclass
from typing import Optional

from ...shared.domain_events.base import DomainEvent
from ...shared.value_objects.wallet_address import WalletAddress
from ...shared.value_objects.money import Money
from ..value_objects.transaction_id import TransactionId
from ..entities.transaction import TransactionType


@dataclass(frozen=True)
class TransactionCreated(DomainEvent):
    """
    Evento disparado quando uma nova transação é criada.
    """
    
    transaction_id: TransactionId
    from_address: Optional[WalletAddress]
    to_address: WalletAddress
    amount: Money
    transaction_type: TransactionType
    
    @property
    def event_name(self) -> str:
        return "TransactionCreated"
    
    def _event_data(self) -> dict:
        return {
            "transaction_id": str(self.transaction_id),
            "from_address": str(self.from_address) if self.from_address else None,
            "to_address": str(self.to_address),
            "amount": str(self.amount.value),
            "transaction_type": self.transaction_type.value,
        }


@dataclass(frozen=True)
class TransactionConfirmed(DomainEvent):
    """
    Evento disparado quando uma transação é confirmada no blockchain.
    """
    
    transaction_id: TransactionId
    block_height: int
    transaction_hash: str
    
    @property
    def event_name(self) -> str:
        return "TransactionConfirmed"
    
    def _event_data(self) -> dict:
        return {
            "transaction_id": str(self.transaction_id),
            "block_height": self.block_height,
            "transaction_hash": self.transaction_hash,
        }


@dataclass(frozen=True)
class TransactionFailed(DomainEvent):
    """
    Evento disparado quando uma transação falha.
    """
    
    transaction_id: TransactionId
    reason: str
    
    @property
    def event_name(self) -> str:
        return "TransactionFailed"
    
    def _event_data(self) -> dict:
        return {
            "transaction_id": str(self.transaction_id),
            "reason": self.reason,
        }


@dataclass(frozen=True)
class TransactionCancelled(DomainEvent):
    """
    Evento disparado quando uma transação é cancelada.
    """
    
    transaction_id: TransactionId
    reason: str
    
    @property
    def event_name(self) -> str:
        return "TransactionCancelled"
    
    def _event_data(self) -> dict:
        return {
            "transaction_id": str(self.transaction_id),
            "reason": self.reason,
        }
