"""
Value Object para chave privada
"""

from dataclasses import dataclass
import secrets


@dataclass(frozen=True)
class PrivateKey:
    """
    Value Object para chave privada.

    ATENÇÃO: Chaves privadas são extremamente sensíveis!
    Nunca devem ser logadas ou expostas.
    """

    value: str

    def __post_init__(self):
        """Valida a chave privada"""
        if not self.value:
            raise ValueError("Private key cannot be empty")

        if not isinstance(self.value, str):
            raise TypeError("Private key must be a string")

        if len(self.value) < 32:
            raise ValueError("Private key too short (minimum 32 characters)")

    @classmethod
    def generate(cls) -> "PrivateKey":
        """Gera uma nova chave privada segura"""
        # Gera 32 bytes aleatórios (256 bits)
        random_bytes = secrets.token_bytes(32)
        private_key = random_bytes.hex()
        return cls(private_key)

    @classmethod
    def from_string(cls, value: str) -> "PrivateKey":
        """Cria a partir de string"""
        return cls(value)

    def __str__(self) -> str:
        """Nunca exibe a chave completa"""
        return "***PRIVATE_KEY***"

    def __repr__(self) -> str:
        """Nunca exibe a chave completa"""
        return "PrivateKey(***HIDDEN***)"

    def __hash__(self) -> int:
        """Hash para uso em sets e dicts"""
        return hash(self.value)

    def reveal(self) -> str:
        """
        Revela a chave privada.

        Use apenas quando absolutamente necessário e com extremo cuidado!
        """
        return self.value
