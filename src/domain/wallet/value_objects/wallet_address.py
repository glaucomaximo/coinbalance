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

        # Validação mais rigorosa para endereços de carteira
        if len(self.value) < 26:  # Bitcoin-like addresses are typically 26-35 chars
            raise ValueError("Wallet address too short (minimum 26 characters)")

        if len(self.value) > 62:  # Maximum reasonable length
            raise ValueError("Wallet address too long (maximum 62 characters)")

        # Verificar se contém apenas caracteres válidos (base58-like)
        valid_chars = set("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
        if not all(c in valid_chars for c in self.value):
            raise ValueError("Wallet address contains invalid characters")

        # Verificar se não é apenas caracteres repetidos
        if len(set(self.value)) < 3:
            raise ValueError("Wallet address appears to be invalid (too few unique characters)")

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
