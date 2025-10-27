"""
Value Object para valores monetários
Garante precisão decimal e conversões seguras entre unidades
"""

from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Money:
    """
    Value Object imutável para representar valores monetários.

    Características:
    - Imutável (frozen=True)
    - Precisão decimal de 8 casas (como Bitcoin)
    - Suporte a múltiplas unidades (CNB, satoshi, mCNB)
    - Operações aritméticas seguras
    """

    amount: Decimal

    # Constantes de conversão
    SATOSHI_PER_CNB = Decimal("100000000")  # 10^8
    MCNB_PER_CNB = Decimal("1000000")  # 10^6
    DECIMAL_PLACES = 8

    def __post_init__(self):
        """Valida e normaliza o valor após inicialização"""
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))

        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")

        # Normalizar para 8 casas decimais
        object.__setattr__(
            self,
            "amount",
            self.amount.quantize(Decimal("0.00000001"), rounding=ROUND_HALF_UP),
        )

    @classmethod
    def from_cnb(cls, amount: Union[float, int, str, Decimal]) -> "Money":
        """Cria Money a partir de CNB"""
        return cls(Decimal(str(amount)))

    @classmethod
    def from_satoshi(cls, amount: Union[int, str, Decimal]) -> "Money":
        """Cria Money a partir de satoshis"""
        return cls(Decimal(str(amount)) / cls.SATOSHI_PER_CNB)

    @classmethod
    def from_mcnb(cls, amount: Union[float, int, str, Decimal]) -> "Money":
        """Cria Money a partir de mCNB"""
        return cls(Decimal(str(amount)) / cls.MCNB_PER_CNB)

    @classmethod
    def zero(cls) -> "Money":
        """Retorna Money com valor zero"""
        return cls(Decimal("0"))

    def to_cnb(self) -> Decimal:
        """Retorna valor em CNB"""
        return self.amount

    def to_satoshi(self) -> int:
        """Retorna valor em satoshis (inteiro)"""
        return int(self.amount * self.SATOSHI_PER_CNB)

    def to_mcnb(self) -> Decimal:
        """Retorna valor em mCNB"""
        return self.amount * self.MCNB_PER_CNB

    def format_cnb(self) -> str:
        """Formata valor como string CNB"""
        return f"{self.amount:.8f} CNB"

    def format_satoshi(self) -> str:
        """Formata valor como string satoshi"""
        return f"{self.to_satoshi()} sat"

    def format_mcnb(self) -> str:
        """Formata valor como string mCNB"""
        return f"{self.to_mcnb():.6f} mCNB"

    # Operações aritméticas

    def __add__(self, other: "Money") -> "Money":
        """Soma dois valores Money"""
        if not isinstance(other, Money):
            raise TypeError(f"Cannot add Money with {type(other)}")
        return Money(self.amount + other.amount)

    def __sub__(self, other: "Money") -> "Money":
        """Subtrai dois valores Money"""
        if not isinstance(other, Money):
            raise TypeError(f"Cannot subtract {type(other)} from Money")
        result = self.amount - other.amount
        if result < 0:
            raise ValueError("Resulting amount cannot be negative")
        return Money(result)

    def __mul__(self, multiplier: Union[int, float, Decimal]) -> "Money":
        """Multiplica Money por um número"""
        return Money(self.amount * Decimal(str(multiplier)))

    def __truediv__(self, divisor: Union[int, float, Decimal]) -> "Money":
        """Divide Money por um número"""
        if divisor == 0:
            raise ValueError("Cannot divide by zero")
        return Money(self.amount / Decimal(str(divisor)))

    # Comparações

    def __eq__(self, other: object) -> bool:
        """Compara igualdade"""
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount

    def __lt__(self, other: "Money") -> bool:
        """Menor que"""
        if not isinstance(other, Money):
            raise TypeError(f"Cannot compare Money with {type(other)}")
        return self.amount < other.amount

    def __le__(self, other: "Money") -> bool:
        """Menor ou igual"""
        return self == other or self < other

    def __gt__(self, other: "Money") -> bool:
        """Maior que"""
        if not isinstance(other, Money):
            raise TypeError(f"Cannot compare Money with {type(other)}")
        return self.amount > other.amount

    def __ge__(self, other: "Money") -> bool:
        """Maior ou igual"""
        return self == other or self > other

    def is_zero(self) -> bool:
        """Verifica se o valor é zero"""
        return self.amount == Decimal("0")

    def is_positive(self) -> bool:
        """Verifica se o valor é positivo"""
        return self.amount > Decimal("0")

    def __str__(self) -> str:
        """Representação string"""
        return self.format_cnb()

    def __repr__(self) -> str:
        """Representação para debug"""
        return f"Money(amount=Decimal('{self.amount}'))"

    def __hash__(self) -> int:
        """Hash para uso em sets e dicts"""
        return hash(self.amount)
