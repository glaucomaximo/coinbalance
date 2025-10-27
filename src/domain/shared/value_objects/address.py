"""
Value Object para endereços (wallet address, contract address, etc.)
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Address:
    """
    Value Object imutável para representar endereços.

    Características:
    - Imutável (frozen=True)
    - Validação de formato
    - Comparação por valor
    """

    value: str

    # Padrão de validação (ajuste conforme necessário)
    PATTERN = re.compile(r"^[A-Za-z0-9_-]{10,64}$")

    def __post_init__(self):
        """Valida o endereço após inicialização"""
        if not self.value:
            raise ValueError("Address cannot be empty")

        if not isinstance(self.value, str):
            raise TypeError("Address must be a string")

        if not self.is_valid(self.value):
            raise ValueError(f"Invalid address format: {self.value}")

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Valida formato do endereço"""
        if not value:
            return False
        return bool(cls.PATTERN.match(value))

    @classmethod
    def create(cls, value: str) -> "Address":
        """Factory method para criar Address"""
        return cls(value)

    @classmethod
    def try_create(cls, value: str) -> Optional["Address"]:
        """Tenta criar Address, retorna None se inválido"""
        try:
            return cls(value)
        except (ValueError, TypeError):
            return None

    def __str__(self) -> str:
        """Representação string"""
        return self.value

    def __repr__(self) -> str:
        """Representação para debug"""
        return f"Address('{self.value}')"

    def __hash__(self) -> int:
        """Hash para uso em sets e dicts"""
        return hash(self.value)

    def short(self, prefix: int = 6, suffix: int = 4) -> str:
        """Retorna versão abreviada do endereço"""
        if len(self.value) <= prefix + suffix:
            return self.value
        return f"{self.value[:prefix]}...{self.value[-suffix:]}"
