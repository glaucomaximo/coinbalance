"""
Value Object para saldo da carteira
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Union

from src.domain.shared.value_objects.money import Money


@dataclass(frozen=True)
class Balance:
    """
    Value Object para saldo da carteira.

    Encapsula Money e adiciona semântica de saldo.
    """

    amount: Money

    def __post_init__(self):
        """Valida o saldo"""
        if not isinstance(self.amount, Money):
            # Tenta converter para Money
            object.__setattr__(self, "amount", Money.from_cnb(self.amount))

    @classmethod
    def zero(cls) -> "Balance":
        """Cria saldo zero"""
        return cls(Money.zero())

    @classmethod
    def from_cnb(cls, amount: Union[float, int, str, Decimal]) -> "Balance":
        """Cria saldo a partir de CNB"""
        return cls(Money.from_cnb(amount))

    @classmethod
    def from_satoshi(cls, amount: Union[int, str, Decimal]) -> "Balance":
        """Cria saldo a partir de satoshis"""
        return cls(Money.from_satoshi(amount))

    def add(self, money: Money) -> "Balance":
        """Adiciona valor ao saldo"""
        return Balance(self.amount + money)

    def subtract(self, money: Money) -> "Balance":
        """Subtrai valor do saldo"""
        new_amount = self.amount - money
        
        # Validar que o resultado não seja negativo
        if new_amount.to_cnb() < 0:
            raise ValueError(f"Cannot subtract {money.to_cnb()} CNB from balance of {self.amount.to_cnb()} CNB")
        
        return Balance(new_amount)

    def is_sufficient_for(self, money: Money) -> bool:
        """Verifica se o saldo é suficiente"""
        return self.amount >= money

    def is_zero(self) -> bool:
        """Verifica se o saldo é zero"""
        return self.amount.is_zero()

    def is_positive(self) -> bool:
        """Verifica se o saldo é positivo"""
        return self.amount.is_positive()

    def to_cnb(self) -> Decimal:
        """Retorna valor em CNB"""
        return self.amount.to_cnb()

    def to_satoshi(self) -> int:
        """Retorna valor em satoshis"""
        return self.amount.to_satoshi()

    def __str__(self) -> str:
        return str(self.amount)

    def __repr__(self) -> str:
        return f"Balance({repr(self.amount)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Balance):
            return False
        return self.amount == other.amount

    def __lt__(self, other: "Balance") -> bool:
        if not isinstance(other, Balance):
            raise TypeError(f"Cannot compare Balance with {type(other)}")
        return self.amount < other.amount

    def __le__(self, other: "Balance") -> bool:
        return self == other or self < other

    def __gt__(self, other: "Balance") -> bool:
        if not isinstance(other, Balance):
            raise TypeError(f"Cannot compare Balance with {type(other)}")
        return self.amount > other.amount

    def __ge__(self, other: "Balance") -> bool:
        return self == other or self > other
