"""
Evento de domínio: ValidatorDeactivated
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ...shared.domain_events.base import DomainEvent
from ..value_objects.validator_id import ValidatorId
from ...shared.value_objects.timestamp import Timestamp

if TYPE_CHECKING:
    pass


@dataclass(frozen=True)
class ValidatorDeactivated(DomainEvent):
    """
    Evento disparado quando um validador é desativado.
    
    Este evento é usado para:
    - Remover validador do pool de consenso
    - Notificar sistemas dependentes
    - Registrar histórico de status
    """
    
    validator_id: ValidatorId = field()
    timestamp: Timestamp = field(default_factory=Timestamp.now)
    
    @property
    def event_type(self) -> str:
        return "validator.deactivated"
    
    @property
    def aggregate_id(self) -> str:
        return str(self.validator_id)
    
    def to_dict(self) -> dict:
        return {
            "event_type": self.event_type,
            "validator_id": str(self.validator_id),
            "timestamp": float(self.timestamp.value)
        }
