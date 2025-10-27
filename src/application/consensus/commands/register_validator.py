"""
Comando para registrar validador no sistema de consenso
"""

from dataclasses import dataclass
from typing import Optional

from src.domain.shared.value_objects.wallet_address import WalletAddress
from src.domain.consensus.value_objects.stake_amount import StakeAmount


@dataclass(frozen=True)
class RegisterValidatorCommand:
    """
    Comando para registrar um novo validador.
    
    Este comando encapsula todos os dados necessários
    para registrar um validador no sistema de consenso.
    """
    
    wallet_address: WalletAddress
    stake_amount: StakeAmount
    metadata: Optional[dict] = None
    
    def __post_init__(self):
        """Validações do comando"""
        if not self.wallet_address:
            raise ValueError("Wallet address é obrigatório")
        
        if not self.stake_amount:
            raise ValueError("Stake amount é obrigatório")
