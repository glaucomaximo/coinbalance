"""
Evento de domínio: ValidatorRegistered
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ...shared.domain_events.base import DomainEvent
from ..value_objects.validator_id import ValidatorId
from ..value_objects.stake_amount import StakeAmount
from ...shared.value_objects.wallet_address import WalletAddress
from ...shared.value_objects.timestamp import Timestamp

if TYPE_CHECKING:
    pass


@dataclass(frozen=True)
class ValidatorRegistered(DomainEvent):
    """
    Evento disparado quando um novo validador é registrado.
    
    Este evento é usado para:
    - Notificar outros sistemas sobre novo validador
    - Atualizar índices de validadores
    - Registrar métricas de staking
    """
    
    validator_id: ValidatorId = field()
    wallet_address: WalletAddress = field()
    stake_amount: StakeAmount = field()
    timestamp: Timestamp = field(default_factory=Timestamp.now)
    
    @property
    def event_type(self) -> str:
        return "validator.registered"
    
    @property
    def aggregate_id(self) -> str:
        return str(self.validator_id)
    
    def to_dict(self) -> dict:
        return {
            "event_type": self.event_type,
            "validator_id": str(self.validator_id),
            "wallet_address": str(self.wallet_address),
            "stake_amount_cnb": float(self.stake_amount.to_cnb()),
            "timestamp": float(self.timestamp.value)
        }
