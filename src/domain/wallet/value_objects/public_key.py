"""
Value Object para chave pública
"""

from dataclasses import dataclass
import hashlib


@dataclass(frozen=True)
class PublicKey:
    """
    Value Object para chave pública.

    A chave pública é derivada da chave privada.
    """

    value: str

    def __post_init__(self):
        """Valida a chave pública"""
        if not self.value:
            raise ValueError("Public key cannot be empty")

        if not isinstance(self.value, str):
            raise TypeError("Public key must be a string")

        if len(self.value) < 32:
            raise ValueError("Public key too short")

    @classmethod
    def from_private_key(cls, private_key: str) -> "PublicKey":
        """
        Deriva chave pública da chave privada.

        Nota: Esta é uma implementação simplificada.
        Em produção, use criptografia de curva elíptica (ECDSA).
        """
        # Hash SHA-256 da chave privada como chave pública
        # Em produção, use ECDSA para derivar a chave pública
        hash_obj = hashlib.sha256(private_key.encode())
        public_key = hash_obj.hexdigest()
        return cls(public_key)

    @classmethod
    def create(cls, value: str) -> "PublicKey":
        """Factory method"""
        return cls(value)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"PublicKey('{self.value[:16]}...')"

    def short(self, length: int = 8) -> str:
        """Versão abreviada da chave"""
        return f"{self.value[:length]}..."
