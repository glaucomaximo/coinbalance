"""
Classes base para eventos de domínio
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict
from uuid import uuid4

from ..value_objects.timestamp import Timestamp


@dataclass(frozen=True)
class DomainEvent(ABC):
    """
    Classe base para todos os eventos de domínio.

    Características:
    - Imutável (frozen=True)
    - ID único
    - Timestamp de ocorrência
    - Metadados adicionais
    """

    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_on: Timestamp = field(default_factory=Timestamp.now)

    @property
    @abstractmethod
    def event_name(self) -> str:
        """Nome do evento (deve ser implementado por subclasses)"""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Serializa evento para dicionário"""
        return {
            "event_id": self.event_id,
            "event_name": self.event_name,
            "occurred_on": self.occurred_on.value,
            **self._event_data(),
        }

    @abstractmethod
    def _event_data(self) -> Dict[str, Any]:
        """Dados específicos do evento (implementado por subclasses)"""
        pass


class DomainEventHandler(ABC):
    """
    Interface para handlers de eventos de domínio.
    """

    @abstractmethod
    async def handle(self, event: DomainEvent) -> None:
        """Processa um evento de domínio"""
        pass

    @property
    @abstractmethod
    def event_type(self) -> type:
        """Tipo de evento que este handler processa"""
        pass
