"""
Sistema de eventos de domínio
"""

from .base import DomainEvent, DomainEventHandler
from .dispatcher import EventDispatcher

__all__ = ["DomainEvent", "DomainEventHandler", "EventDispatcher"]
