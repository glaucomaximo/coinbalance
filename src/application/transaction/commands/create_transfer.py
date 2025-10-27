"""
Comandos para o domínio de transações
"""

from dataclasses import dataclass
from typing import Optional

from src.domain.shared.value_objects.wallet_address import WalletAddress
from src.domain.shared.value_objects.money import Money


@dataclass(frozen=True)
class CreateTransferCommand:
    """
    Comando para criar uma transação de transferência.
    """
    
    from_address: WalletAddress
    to_address: WalletAddress
    amount: Money
    fee: Money
    memo: Optional[str] = None
    metadata: Optional[dict] = None
    
    def __post_init__(self):
        """Validações do comando"""
        if not self.from_address:
            raise ValueError("From address is required")
        
        if not self.to_address:
            raise ValueError("To address is required")
        
        if self.from_address == self.to_address:
            raise ValueError("Cannot send to same address")
        
        if self.amount.value <= 0:
            raise ValueError("Amount must be positive")
        
        if self.fee.value < 0:
            raise ValueError("Fee cannot be negative")


@dataclass(frozen=True)
class CreateStakeCommand:
    """
    Comando para criar uma transação de staking.
    """
    
    wallet_address: WalletAddress
    amount: Money
    fee: Money
    metadata: Optional[dict] = None
    
    def __post_init__(self):
        """Validações do comando"""
        if not self.wallet_address:
            raise ValueError("Wallet address is required")
        
        if self.amount.value <= 0:
            raise ValueError("Amount must be positive")
        
        if self.fee.value < 0:
            raise ValueError("Fee cannot be negative")


@dataclass(frozen=True)
class ConfirmTransactionCommand:
    """
    Comando para confirmar uma transação.
    """
    
    transaction_id: str
    block_height: int
    transaction_hash: str
    
    def __post_init__(self):
        """Validações do comando"""
        if not self.transaction_id:
            raise ValueError("Transaction ID is required")
        
        if not self.transaction_hash:
            raise ValueError("Transaction hash is required")
        
        if self.block_height < 0:
            raise ValueError("Block height must be non-negative")


@dataclass(frozen=True)
class FailTransactionCommand:
    """
    Comando para marcar uma transação como falhada.
    """
    
    transaction_id: str
    reason: str
    
    def __post_init__(self):
        """Validações do comando"""
        if not self.transaction_id:
            raise ValueError("Transaction ID is required")
        
        if not self.reason:
            raise ValueError("Failure reason is required")
