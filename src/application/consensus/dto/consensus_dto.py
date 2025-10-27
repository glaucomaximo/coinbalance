"""
DTOs para o domínio de consenso
"""

from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

from src.domain.consensus.value_objects.validator_id import ValidatorId
from src.domain.shared.value_objects.wallet_address import WalletAddress
from src.domain.shared.value_objects.timestamp import Timestamp


@dataclass(frozen=True)
class ValidatorDTO:
    """
    DTO para representar um validador.
    
    Usado para transferir dados de validador entre camadas
    sem expor a entidade de domínio diretamente.
    """
    
    id: ValidatorId
    wallet_address: WalletAddress
    stake_amount_cnb: Decimal
    is_active: bool
    blocks_validated: int
    total_rewards_cnb: Decimal
    created_at: Timestamp
    updated_at: Timestamp
    last_validation_at: Optional[Timestamp] = None
    
    @property
    def staking_power(self) -> Decimal:
        """Retorna o poder de staking"""
        return self.stake_amount_cnb


@dataclass(frozen=True)
class ConsensusStatsDTO:
    """
    DTO para estatísticas do sistema de consenso.
    """
    
    total_validators: int
    total_stake_cnb: Decimal
    current_round: int
    block_time_seconds: int
    min_stake_cnb: Decimal


@dataclass(frozen=True)
class StakeReceiptDTO:
    """
    DTO para recibo de operação de stake.
    """
    
    validator_id: ValidatorId
    operation_type: str  # "register", "increase", "decrease"
    amount_cnb: Decimal
    new_total_stake_cnb: Decimal
    timestamp: Timestamp
