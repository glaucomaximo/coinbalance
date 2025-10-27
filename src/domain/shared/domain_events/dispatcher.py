"""
Dispatcher de eventos de domínio
"""

import logging
from typing import Dict, List, Type

from .base import DomainEvent, DomainEventHandler

logger = logging.getLogger(__name__)


class EventDispatcher:
    """
    Dispatcher para eventos de domínio.

    Implementa o padrão Observer para propagar eventos
    através do sistema.
    """

    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], List[DomainEventHandler]] = {}
        self._events_queue: List[DomainEvent] = []

    def register(
        self, event_type: Type[DomainEvent], handler: DomainEventHandler
    ) -> None:
        """Registra um handler para um tipo de evento"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []

        self._handlers[event_type].append(handler)
        logger.info(
            f"Registered handler {handler.__class__.__name__} for event {event_type.__name__}"
        )

    def unregister(
        self, event_type: Type[DomainEvent], handler: DomainEventHandler
    ) -> None:
        """Remove um handler"""
        if event_type in self._handlers:
            self._handlers[event_type].remove(handler)

    async def dispatch(self, event: DomainEvent) -> None:
        """Despacha um evento para todos os handlers registrados"""
        event_type = type(event)

        if event_type not in self._handlers:
            logger.debug(f"No handlers registered for event {event_type.__name__}")
            return

        logger.info(f"Dispatching event {event_type.__name__} (ID: {event.event_id})")

        for handler in self._handlers[event_type]:
            try:
                await handler.handle(event)
                logger.debug(
                    f"Handler {handler.__class__.__name__} processed event successfully"
                )
            except Exception as e:
                logger.error(
                    f"Error in handler {handler.__class__.__name__}: {str(e)}",
                    exc_info=True,
                )

    def queue_event(self, event: DomainEvent) -> None:
        """Adiciona evento à fila para processamento posterior"""
        self._events_queue.append(event)

    async def dispatch_queued_events(self) -> None:
        """Processa todos os eventos na fila"""
        events = self._events_queue.copy()
        self._events_queue.clear()

        for event in events:
            await self.dispatch(event)

    def clear_handlers(self) -> None:
        """Remove todos os handlers (útil para testes)"""
        self._handlers.clear()

    def clear_queue(self) -> None:
        """Limpa a fila de eventos"""
        self._events_queue.clear()


# Singleton global para uso em toda a aplicação
_event_dispatcher = EventDispatcher()


def get_event_dispatcher() -> EventDispatcher:
    """Retorna a instância global do EventDispatcher"""
    return _event_dispatcher
