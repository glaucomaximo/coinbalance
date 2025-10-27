"""
Queries para o domínio de transações
"""

from dataclasses import dataclass
from typing import Optional, List
from decimal import Decimal

from src.domain.shared.value_objects.wallet_address import WalletAddress


@dataclass(frozen=True)
class GetTransactionQuery:
    """
    Query para buscar uma transação por ID.
    """
    
    transaction_id: str
    
    def __post_init__(self):
        """Validações da query"""
        if not self.transaction_id:
            raise ValueError("Transaction ID is required")


@dataclass(frozen=True)
class GetTransactionsByAddressQuery:
    """
    Query para buscar transações de um endereço.
    """
    
    address: WalletAddress
    limit: int = 50
    offset: int = 0
    
    def __post_init__(self):
        """Validações da query"""
        if not self.address:
            raise ValueError("Address is required")
        
        if self.limit <= 0:
            raise ValueError("Limit must be positive")
        
        if self.offset < 0:
            raise ValueError("Offset must be non-negative")


@dataclass(frozen=True)
class GetPendingTransactionsQuery:
    """
    Query para buscar transações pendentes.
    """
    
    limit: int = 100
    offset: int = 0
    
    def __post_init__(self):
        """Validações da query"""
        if self.limit <= 0:
            raise ValueError("Limit must be positive")
        
        if self.offset < 0:
            raise ValueError("Offset must be non-negative")


@dataclass(frozen=True)
class GetTransactionStatsQuery:
    """
    Query para buscar estatísticas de transações.
    """
    
    address: Optional[WalletAddress] = None
    
    def __post_init__(self):
        """Validações da query"""
        # Address é opcional para estatísticas globais
        pass
