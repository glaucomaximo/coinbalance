"""
Value Object para rodadas de consenso
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Union


@dataclass(frozen=True)
class ConsensusRound:
    """
    Value Object imutável para representar rodadas de consenso.
    
    Características:
    - Imutável (frozen=True)
    - Número sequencial de rodadas
    - Timestamp da rodada
    """
    
    number: int
    timestamp: Decimal  # Unix timestamp
    
    def __post_init__(self):
        """Validações da rodada de consenso"""
        if self.number < 0:
            raise ValueError("Número da rodada deve ser não-negativo")
        
        if self.timestamp <= 0:
            raise ValueError("Timestamp deve ser positivo")
    
    @classmethod
    def create(cls, number: int, timestamp: Union[Decimal, float, int]) -> 'ConsensusRound':
        """Cria uma nova rodada de consenso"""
        return cls(
            number=number,
            timestamp=Decimal(str(timestamp))
        )
    
    def next_round(self, timestamp: Union[Decimal, float, int]) -> 'ConsensusRound':
        """Cria a próxima rodada"""
        return ConsensusRound(
            number=self.number + 1,
            timestamp=Decimal(str(timestamp))
        )
    
    def __str__(self) -> str:
        return f"Round {self.number}"
    
    def __repr__(self) -> str:
        return f"ConsensusRound(number={self.number}, timestamp={self.timestamp})"
