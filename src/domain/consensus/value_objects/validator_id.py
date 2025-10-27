"""
Value Object para identificação de validadores
"""

from dataclasses import dataclass
from typing import Union
import uuid


@dataclass(frozen=True)
class ValidatorId:
    """
    Value Object imutável para identificação única de validadores.
    
    Características:
    - Imutável (frozen=True)
    - Identificação única baseada em UUID
    - Validação de formato
    """
    
    value: str
    
    def __post_init__(self):
        """Validação do formato do ID"""
        if not self.value:
            raise ValueError("ValidatorId não pode ser vazio")
        
        # Validar se é um UUID válido
        try:
            uuid.UUID(self.value)
        except ValueError:
            raise ValueError(f"ValidatorId deve ser um UUID válido: {self.value}")
    
    @classmethod
    def generate(cls) -> 'ValidatorId':
        """Gera um novo ValidatorId único"""
        return cls(str(uuid.uuid4()))
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"ValidatorId('{self.value}')"
