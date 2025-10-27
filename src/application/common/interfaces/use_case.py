"""
Interface base para Use Cases
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# Tipos genéricos para entrada e saída
TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")


class UseCase(ABC, Generic[TRequest, TResponse]):
    """
    Interface base para todos os Use Cases.

    Segue o padrão Command/Query Responsibility Segregation (CQRS).
    Cada Use Case deve ter uma única responsabilidade bem definida.
    """

    @abstractmethod
    async def execute(self, request: TRequest) -> TResponse:
        """
        Executa o use case.

        Args:
            request: Dados de entrada

        Returns:
            Resultado da operação
        """
        pass
