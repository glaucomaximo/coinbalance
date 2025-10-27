"""
Interface do repositório de transações
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal

from ..entities.transaction import Transaction
from ..value_objects.transaction_id import TransactionId
from ...shared.value_objects.wallet_address import WalletAddress
from ...shared.value_objects.timestamp import Timestamp


class TransactionRepository(ABC):
    """
    Interface para repositório de transações.
    
    Define contratos para persistência de transações seguindo
    os princípios de Clean Architecture.
    """
    
    @abstractmethod
    async def save(self, transaction: Transaction) -> None:
        """
        Salva uma transação no repositório.
        
        Args:
            transaction: Transação a ser salva
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, transaction_id: TransactionId) -> Optional[Transaction]:
        """
        Busca uma transação por ID.
        
        Args:
            transaction_id: ID da transação
            
        Returns:
            Transação encontrada ou None
        """
        pass
    
    @abstractmethod
    async def find_by_hash(self, transaction_hash: str) -> Optional[Transaction]:
        """
        Busca uma transação por hash.
        
        Args:
            transaction_hash: Hash da transação
            
        Returns:
            Transação encontrada ou None
        """
        pass
    
    @abstractmethod
    async def find_by_address(
        self, 
        address: WalletAddress, 
        limit: int = 50,
        offset: int = 0
    ) -> List[Transaction]:
        """
        Busca transações relacionadas a um endereço.
        
        Args:
            address: Endereço da carteira
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            Lista de transações
        """
        pass
    
    @abstractmethod
    async def find_pending_transactions(self) -> List[Transaction]:
        """
        Busca todas as transações pendentes.
        
        Returns:
            Lista de transações pendentes
        """
        pass
    
    @abstractmethod
    async def find_by_block_height(self, block_height: int) -> List[Transaction]:
        """
        Busca transações de um bloco específico.
        
        Args:
            block_height: Altura do bloco
            
        Returns:
            Lista de transações do bloco
        """
        pass
    
    @abstractmethod
    async def count_by_address(self, address: WalletAddress) -> int:
        """
        Conta o número de transações de um endereço.
        
        Args:
            address: Endereço da carteira
            
        Returns:
            Número de transações
        """
        pass
    
    @abstractmethod
    async def get_total_volume(self) -> Decimal:
        """
        Retorna o volume total de transações.
        
        Returns:
            Volume total em CNB
        """
        pass
    
    @abstractmethod
    async def get_transaction_stats(self) -> dict:
        """
        Retorna estatísticas das transações.
        
        Returns:
            Dicionário com estatísticas
        """
        pass
