"""
Value Object para valores de stake
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Union

from ...shared.value_objects.money import Money


@dataclass(frozen=True)
class StakeAmount:
    """
    Value Object imutável para representar valores de stake.
    
    Características:
    - Imutável (frozen=True)
    - Baseado no Money value object existente
    - Validações específicas para staking
    """
    
    amount: Money
    
    def __post_init__(self):
        """Validações específicas para stake"""
        if self.amount.amount <= 0:
            raise ValueError("Stake amount deve ser maior que zero")
        
        # Stake mínimo de 1000 CNB
        min_stake = Money(Decimal("1000"))
        if self.amount < min_stake:
            raise ValueError(f"Stake mínimo é {min_stake} CNB")
    
    @classmethod
    def from_cnb(cls, amount: Union[Decimal, float, int]) -> 'StakeAmount':
        """Cria StakeAmount a partir de valor em CNB"""
        return cls(Money.from_cnb(amount))
    
    @classmethod
    def from_satoshi(cls, amount: Union[Decimal, float, int]) -> 'StakeAmount':
        """Cria StakeAmount a partir de valor em satoshi"""
        return cls(Money.from_satoshi(amount))
    
    def to_cnb(self) -> Decimal:
        """Retorna valor em CNB"""
        return self.amount.to_cnb()
    
    def to_satoshi(self) -> Decimal:
        """Retorna valor em satoshi"""
        return self.amount.to_satoshi()
    
    def __add__(self, other: 'StakeAmount') -> 'StakeAmount':
        """Soma dois stake amounts"""
        return StakeAmount(self.amount + other.amount)
    
    def __sub__(self, other: 'StakeAmount') -> 'StakeAmount':
        """Subtrai dois stake amounts"""
        return StakeAmount(self.amount - other.amount)
    
    def __mul__(self, multiplier: Union[Decimal, float, int]) -> 'StakeAmount':
        """Multiplica stake amount por um fator"""
        return StakeAmount(self.amount * multiplier)
    
    def __lt__(self, other: 'StakeAmount') -> bool:
        """Comparação menor que"""
        return self.amount < other.amount
    
    def __le__(self, other: 'StakeAmount') -> bool:
        """Comparação menor ou igual"""
        return self.amount <= other.amount
    
    def __gt__(self, other: 'StakeAmount') -> bool:
        """Comparação maior que"""
        return self.amount > other.amount
    
    def __ge__(self, other: 'StakeAmount') -> bool:
        """Comparação maior ou igual"""
        return self.amount >= other.amount
    
    def __str__(self) -> str:
        return f"{self.to_cnb()} CNB"
    
    def __repr__(self) -> str:
        return f"StakeAmount({self.to_cnb()} CNB)"
