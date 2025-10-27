"""
Evento: Carteira Criada
"""

from dataclasses import dataclass, field
from typing import Dict, Any
from uuid import uuid4

from ...shared.value_objects.timestamp import Timestamp


@dataclass(frozen=True)
class WalletCreated:
    """
    Evento disparado quando uma nova carteira é criada.
    """

    wallet_address: str
    wallet_name: str
    public_key: str
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_on: Timestamp = field(default_factory=Timestamp.now)

    @property
    def event_name(self) -> str:
        return "wallet.created"

    def to_dict(self) -> Dict[str, Any]:
        """Serializa evento para dicionário"""
        return {
            "event_id": self.event_id,
            "event_name": self.event_name,
            "occurred_on": self.occurred_on.value,
            "wallet_address": self.wallet_address,
            "wallet_name": self.wallet_name,
            "public_key": self.public_key,
        }
