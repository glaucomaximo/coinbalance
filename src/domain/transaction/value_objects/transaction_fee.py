"""
Value Objects para o domínio de transações
"""

from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
import uuid

from ...shared.value_objects.money import Money


@dataclass(frozen=True)
class TransactionFee:
    """
    Value Object para taxas de transação.
    
    Encapsula a taxa cobrada por uma transação.
    """
    
    value: Money
    
    def __post_init__(self):
        """Validação da taxa"""
        if self.value.to_cnb() < 0:
            raise ValueError("Transaction fee cannot be negative")
        
        if self.value.to_cnb() > Decimal("1000"):  # Max fee
            raise ValueError("Transaction fee too high")
    
    def to_cnb(self) -> Decimal:
        """Retorna taxa em CNB"""
        return self.value.value
    
    def to_satoshi(self) -> int:
        """Retorna taxa em satoshis"""
        return int(self.value.value * Decimal("100000000"))
    
    def is_zero(self) -> bool:
        """Verifica se a taxa é zero"""
        return self.value.value == Decimal("0")
    
    def __str__(self) -> str:
        return f"{self.value.value} CNB"
