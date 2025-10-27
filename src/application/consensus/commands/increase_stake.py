"""
Comando para aumentar stake de um validador
"""

from dataclasses import dataclass

from src.domain.consensus.value_objects.validator_id import ValidatorId
from src.domain.consensus.value_objects.stake_amount import StakeAmount


@dataclass(frozen=True)
class IncreaseStakeCommand:
    """
    Comando para aumentar o stake de um validador.
    
    Este comando encapsula os dados necessários
    para aumentar o stake de um validador existente.
    """
    
    validator_id: ValidatorId
    additional_stake: StakeAmount
    
    def __post_init__(self):
        """Validações do comando"""
        if not self.validator_id:
            raise ValueError("Validator ID é obrigatório")
        
        if not self.additional_stake:
            raise ValueError("Additional stake é obrigatório")
