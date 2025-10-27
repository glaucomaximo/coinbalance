"""
Value Object para timestamps
"""

from dataclasses import dataclass
from datetime import datetime
from time import time
from typing import Union


@dataclass(frozen=True)
class Timestamp:
    """
    Value Object imutável para representar timestamps.

    Características:
    - Imutável (frozen=True)
    - Precisão em segundos (float)
    - Conversões para datetime
    """

    value: float

    def __post_init__(self):
        """Valida o timestamp após inicialização"""
        if not isinstance(self.value, (int, float)):
            raise TypeError("Timestamp must be a number")

        if self.value < 0:
            raise ValueError("Timestamp cannot be negative")

        # Normalizar para float
        if not isinstance(self.value, float):
            object.__setattr__(self, "value", float(self.value))

    @classmethod
    def now(cls) -> "Timestamp":
        """Cria Timestamp com o tempo atual"""
        return cls(time())

    @classmethod
    def from_datetime(cls, dt: datetime) -> "Timestamp":
        """Cria Timestamp a partir de datetime"""
        return cls(dt.timestamp())

    @classmethod
    def from_seconds(cls, seconds: Union[int, float]) -> "Timestamp":
        """Cria Timestamp a partir de segundos"""
        return cls(float(seconds))

    def to_datetime(self) -> datetime:
        """Converte para datetime"""
        return datetime.fromtimestamp(self.value)

    def to_iso(self) -> str:
        """Converte para string ISO 8601"""
        return self.to_datetime().isoformat()

    def __str__(self) -> str:
        """Representação string"""
        return self.to_iso()

    def __repr__(self) -> str:
        """Representação para debug"""
        return f"Timestamp({self.value})"

    def __hash__(self) -> int:
        """Hash para uso em sets e dicts"""
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        """Compara igualdade"""
        if not isinstance(other, Timestamp):
            return False
        return self.value == other.value

    def __lt__(self, other: "Timestamp") -> bool:
        """Menor que"""
        if not isinstance(other, Timestamp):
            raise TypeError(f"Cannot compare Timestamp with {type(other)}")
        return self.value < other.value

    def __le__(self, other: "Timestamp") -> bool:
        """Menor ou igual"""
        return self == other or self < other

    def __gt__(self, other: "Timestamp") -> bool:
        """Maior que"""
        if not isinstance(other, Timestamp):
            raise TypeError(f"Cannot compare Timestamp with {type(other)}")
        return self.value > other.value

    def __ge__(self, other: "Timestamp") -> bool:
        """Maior ou igual"""
        return self == other or self > other

    def difference(self, other: "Timestamp") -> float:
        """Retorna diferença em segundos"""
        return abs(self.value - other.value)
