"""
Value Object para endereço de carteira
"""

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class WalletAddress:
    """
    Value Object para endereço de carteira.

    O endereço é derivado da chave pública.
    """

    value: str

    def __post_init__(self):
        """Valida o endereço"""
        if not self.value:
            raise ValueError("Wallet address cannot be empty")

        if not isinstance(self.value, str):
            raise TypeError("Wallet address must be a string")

        if len(self.value) < 10:
            raise ValueError("Wallet address too short")

    @classmethod
    def from_public_key(cls, public_key: str) -> "WalletAddress":
        """Gera endereço a partir de chave pública"""
        # Hash SHA-256 da chave pública
        hash_obj = hashlib.sha256(public_key.encode())
        address = hash_obj.hexdigest()[:40]  # Pegar primeiros 40 caracteres
        return cls(address)

    @classmethod
    def create(cls, value: str) -> "WalletAddress":
        """Factory method"""
        return cls(value)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"WalletAddress('{self.value[:8]}...')"

    def short(self, prefix: int = 6, suffix: int = 4) -> str:
        """Versão abreviada do endereço"""
        if len(self.value) <= prefix + suffix:
            return self.value
        return f"{self.value[:prefix]}...{self.value[-suffix:]}"
