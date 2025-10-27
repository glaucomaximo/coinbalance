"""
Evento de domínio: RewardsAdded
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from decimal import Decimal

from ...shared.domain_events.base import DomainEvent
from ..value_objects.validator_id import ValidatorId
from ...shared.value_objects.timestamp import Timestamp

if TYPE_CHECKING:
    pass


@dataclass(frozen=True)
class RewardsAdded(DomainEvent):
    """
    Evento disparado quando recompensas são adicionadas a um validador.
    
    Este evento é usado para:
    - Registrar histórico de recompensas
    - Notificar sistemas de pagamento
    - Atualizar métricas de performance
    """
    
    validator_id: ValidatorId = field()
    amount: Decimal = field()
    total_rewards: Decimal = field()
    timestamp: Timestamp = field(default_factory=Timestamp.now)
    
    @property
    def event_type(self) -> str:
        return "rewards.added"
    
    @property
    def aggregate_id(self) -> str:
        return str(self.validator_id)
    
    def to_dict(self) -> dict:
        return {
            "event_type": self.event_type,
            "validator_id": str(self.validator_id),
            "amount_cnb": float(self.amount),
            "total_rewards_cnb": float(self.total_rewards),
            "timestamp": float(self.timestamp.value)
        }
