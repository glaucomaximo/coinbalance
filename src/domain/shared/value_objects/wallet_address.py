"""
Value Object para endereços de carteira
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class WalletAddress:
    """
    Value Object imutável para representar endereços de carteira.

    Características:
    - Imutável (frozen=True)
    - Validação de formato
    - Comparação por valor
    """

    value: str

    def __post_init__(self):
        """Validação do formato do endereço"""
        if not self.value:
            raise ValueError("Endereço de carteira não pode ser vazio")
        
        # Validação básica de formato (pode ser expandida)
        if len(self.value) < 10:
            raise ValueError("Endereço de carteira muito curto")
        
        if len(self.value) > 100:
            raise ValueError("Endereço de carteira muito longo")
    
    @classmethod
    def from_string(cls, address_str: str) -> 'WalletAddress':
        """Cria WalletAddress a partir de string"""
        return cls(address_str)
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"WalletAddress('{self.value}')"
