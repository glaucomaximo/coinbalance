"""
Value Object para hashes criptográficos
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class HashValue:
    """
    Value Object imutável para representar hashes criptográficos.

    Características:
    - Imutável (frozen=True)
    - Validação de formato SHA-256
    - Comparação por valor
    """

    value: str

    # Padrão SHA-256 (64 caracteres hexadecimais)
    SHA256_PATTERN = re.compile(r"^[a-fA-F0-9]{64}$")

    def __post_init__(self):
        """Valida o hash após inicialização"""
        if not self.value:
            raise ValueError("Hash cannot be empty")

        if not isinstance(self.value, str):
            raise TypeError("Hash must be a string")

        if not self.is_valid_sha256(self.value):
            raise ValueError(f"Invalid SHA-256 hash format: {self.value}")

    @classmethod
    def is_valid_sha256(cls, value: str) -> bool:
        """Valida formato SHA-256"""
        if not value:
            return False
        return bool(cls.SHA256_PATTERN.match(value))

    @classmethod
    def create(cls, value: str) -> "HashValue":
        """Factory method para criar HashValue"""
        return cls(value.lower())

    @classmethod
    def try_create(cls, value: str) -> Optional["HashValue"]:
        """Tenta criar HashValue, retorna None se inválido"""
        try:
            return cls(value)
        except (ValueError, TypeError):
            return None

    def starts_with_zeros(self, count: int) -> bool:
        """Verifica se o hash começa com N zeros (para mining)"""
        return self.value.startswith("0" * count)

    def difficulty(self) -> int:
        """Retorna quantos zeros no início do hash"""
        count = 0
        for char in self.value:
            if char == "0":
                count += 1
            else:
                break
        return count

    def __str__(self) -> str:
        """Representação string"""
        return self.value

    def __repr__(self) -> str:
        """Representação para debug"""
        return f"HashValue('{self.value[:16]}...')"

    def __hash__(self) -> int:
        """Hash para uso em sets e dicts"""
        return hash(self.value)

    def short(self, length: int = 8) -> str:
        """Retorna versão abreviada do hash"""
        return f"{self.value[:length]}..."
