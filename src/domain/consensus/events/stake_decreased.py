"""
Evento de domínio: StakeDecreased
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ...shared.domain_events.base import DomainEvent
from ..value_objects.validator_id import ValidatorId
from ..value_objects.stake_amount import StakeAmount
from ...shared.value_objects.timestamp import Timestamp

if TYPE_CHECKING:
    pass


@dataclass(frozen=True)
class StakeDecreased(DomainEvent):
    """
    Evento disparado quando o stake de um validador é diminuído.
    
    Este evento é usado para:
    - Atualizar índices de poder de staking
    - Notificar mudanças no consenso
    - Registrar histórico de stake
    """
    
    validator_id: ValidatorId = field()
    old_amount: StakeAmount = field()
    new_amount: StakeAmount = field()
    timestamp: Timestamp = field(default_factory=Timestamp.now)
    
    @property
    def event_type(self) -> str:
        return "stake.decreased"
    
    @property
    def aggregate_id(self) -> str:
        return str(self.validator_id)
    
    def to_dict(self) -> dict:
        return {
            "event_type": self.event_type,
            "validator_id": str(self.validator_id),
            "old_amount_cnb": float(self.old_amount.to_cnb()),
            "new_amount_cnb": float(self.new_amount.to_cnb()),
            "decrease_cnb": float(self.old_amount.to_cnb() - self.new_amount.to_cnb()),
            "timestamp": float(self.timestamp.value)
        }
