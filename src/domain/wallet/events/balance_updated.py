"""
Evento: Saldo Atualizado
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any
from uuid import uuid4

from ...shared.value_objects.timestamp import Timestamp


@dataclass(frozen=True)
class BalanceUpdated:
    """
    Evento disparado quando o saldo de uma carteira é atualizado.
    """

    wallet_address: str
    old_balance: Decimal
    new_balance: Decimal
    amount: Decimal
    operation: str  # "credit" ou "debit"
    reason: str
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_on: Timestamp = field(default_factory=Timestamp.now)

    @property
    def event_name(self) -> str:
        return "wallet.balance_updated"

    def to_dict(self) -> Dict[str, Any]:
        """Serializa evento para dicionário"""
        return {
            "event_id": self.event_id,
            "event_name": self.event_name,
            "occurred_on": self.occurred_on.value,
            "wallet_address": self.wallet_address,
            "old_balance": float(self.old_balance),
            "new_balance": float(self.new_balance),
            "amount": float(self.amount),
            "operation": self.operation,
            "reason": self.reason,
        }
