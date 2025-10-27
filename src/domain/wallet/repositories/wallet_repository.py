"""
Repository Interface (Port) para Wallet

Este é o PORT no padrão Hexagonal Architecture.
A implementação concreta (ADAPTER) fica na camada de Infrastructure.
"""

from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.wallet import Wallet
from ..value_objects.wallet_address import WalletAddress


class WalletRepository(ABC):
    """
    Interface abstrata para repositório de carteiras.

    Define o contrato que as implementações concretas devem seguir.
    Segue os princípios:
    - Dependency Inversion Principle (SOLID)
    - Hexagonal Architecture (Ports & Adapters)
    """

    @abstractmethod
    async def save(self, wallet: Wallet) -> None:
        """
        Salva ou atualiza uma carteira.

        Args:
            wallet: Carteira a ser salva
        """
        pass

    @abstractmethod
    async def find_by_address(self, address: WalletAddress) -> Optional[Wallet]:
        """
        Busca carteira por endereço.

        Args:
            address: Endereço da carteira

        Returns:
            Carteira encontrada ou None
        """
        pass

    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[Wallet]:
        """
        Busca carteira por nome.

        Args:
            name: Nome da carteira

        Returns:
            Carteira encontrada ou None
        """
        pass

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Wallet]:
        """
        Lista todas as carteiras.

        Args:
            skip: Número de registros a pular (paginação)
            limit: Número máximo de registros a retornar

        Returns:
            Lista de carteiras
        """
        pass

    @abstractmethod
    async def find_active(self, skip: int = 0, limit: int = 100) -> List[Wallet]:
        """
        Lista carteiras ativas.

        Args:
            skip: Número de registros a pular (paginação)
            limit: Número máximo de registros a retornar

        Returns:
            Lista de carteiras ativas
        """
        pass

    @abstractmethod
    async def exists(self, address: WalletAddress) -> bool:
        """
        Verifica se carteira existe.

        Args:
            address: Endereço da carteira

        Returns:
            True se existe, False caso contrário
        """
        pass

    @abstractmethod
    async def delete(self, address: WalletAddress) -> None:
        """
        Remove uma carteira.

        Args:
            address: Endereço da carteira
        """
        pass

    @abstractmethod
    async def count(self) -> int:
        """
        Conta total de carteiras.

        Returns:
            Número total de carteiras
        """
        pass
