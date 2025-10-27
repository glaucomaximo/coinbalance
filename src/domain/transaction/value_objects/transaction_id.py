"""
Value Objects para o domínio de transações
"""

from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
import uuid

from ...shared.value_objects.money import Money


@dataclass(frozen=True)
class TransactionId:
    """
    Value Object para identificação única de transações.
    
    Garante que cada transação tenha um ID único e imutável.
    """
    
    value: str
    
    def __post_init__(self):
        """Validação do ID"""
        if not self.value:
            raise ValueError("Transaction ID cannot be empty")
        
        if len(self.value) < 10:
            raise ValueError("Transaction ID must be at least 10 characters")
    
    @classmethod
    def generate(cls) -> "TransactionId":
        """Gera um novo ID único"""
        return cls(str(uuid.uuid4()))
    
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class TransactionAmount:
    """
    Value Object para valores de transação.
    
    Encapsula o valor monetário de uma transação com validações.
    """
    
    value: Money
    
    def __post_init__(self):
        """Validação do valor"""
        if self.value.value <= 0:
            raise ValueError("Transaction amount must be positive")
        
        if self.value.value > Decimal("21000000"):  # Max supply
            raise ValueError("Transaction amount exceeds maximum supply")
    
    def to_cnb(self) -> Decimal:
        """Retorna valor em CNB"""
        return self.value.value
    
    def to_satoshi(self) -> int:
        """Retorna valor em satoshis"""
        return int(self.value.value * Decimal("100000000"))
    
    def __str__(self) -> str:
        return f"{self.value.value} CNB"


@dataclass(frozen=True)
class TransactionFee:
    """
    Value Object para taxas de transação.
    
    Encapsula a taxa cobrada por uma transação.
    """
    
    value: Money
    
    def __post_init__(self):
        """Validação da taxa"""
        if self.value.value < 0:
            raise ValueError("Transaction fee cannot be negative")
        
        if self.value.value > Decimal("1000"):  # Max fee
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
