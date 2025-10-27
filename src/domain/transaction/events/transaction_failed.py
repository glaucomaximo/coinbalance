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
