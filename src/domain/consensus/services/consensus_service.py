"""
Serviço de Consenso PoS/DPoS Otimizado
"""

import random
import threading
from typing import List, Optional, Dict, Any
from decimal import Decimal

from ..entities.validator import Validator
from ..value_objects.validator_id import ValidatorId
from ..value_objects.consensus_round import ConsensusRound
from ...shared.value_objects.wallet_address import WalletAddress
from ...shared.value_objects.timestamp import Timestamp
from ...shared.config.blockchain_config import BlockchainConfig
from .optimized_consensus_service import OptimizedConsensusService


class ConsensusService:
    """
    Serviço principal para gerenciar o consenso PoS/DPoS.
    
    Usa sistema otimizado para evitar problemas de performance O(N²).
    """
    
    def __init__(self):
        # Usar serviço otimizado
        self._optimized_service = OptimizedConsensusService()
        self.active_validators: List[Validator] = []
        self.current_round: Optional[ConsensusRound] = None
        self.block_time_seconds = BlockchainConfig.BLOCK_TIME_SECONDS
        self._lock = threading.RLock()
    
    def register_validator(self, validator: Validator) -> None:
        """Registra validador no sistema"""
        with self._lock:
            self._optimized_service.add_validator(validator)
            if validator not in self.active_validators:
                self.active_validators.append(validator)
    
    def add_validator(self, validator: Validator) -> None:
        """Adiciona validador ao sistema"""
        self.register_validator(validator)
    
    def remove_validator(self, validator_id: ValidatorId) -> None:
        """Remove validador do sistema"""
        with self._lock:
            self._optimized_service.remove_validator(validator_id)
            self.active_validators = [v for v in self.active_validators if v.id != validator_id]
    
    def select_validator_for_round(self, round_number: int) -> Optional[Validator]:
        """
        Seleciona validador para uma rodada específica usando sistema otimizado.
        
        Complexidade: O(log N) em vez de O(N²)
        """
        return self._optimized_service.select_validator_for_round(round_number)
    
    def validate_block(self, validator: Validator, block_data: dict) -> bool:
        """Valida bloco usando validador"""
        return self._optimized_service.validate_block(validator, block_data)
    
    def calculate_rewards(self, validator: Validator, block_height: int) -> Decimal:
        """Calcula recompensas para um validador"""
        # Recompensa base por bloco validado
        base_reward = Decimal("0.1")  # 0.1 CNB por bloco
        
        # Multiplicador baseado no stake
        stake_multiplier = min(validator.get_staking_power() / Decimal("10000"), Decimal("2.0"))
        
        # Multiplicador baseado na performance
        performance_multiplier = Decimal("1.0")
        if validator.blocks_validated > 0:
            performance_multiplier = Decimal("1.1")
        
        # Calcular recompensa final
        total_reward = base_reward * stake_multiplier * performance_multiplier
        
        return total_reward
    
    def start_new_round(self) -> ConsensusRound:
        """Inicia uma nova rodada de consenso"""
        if self.current_round is None:
            round_number = 0
        else:
            round_number = self.current_round.number + 1
        
        self.current_round = ConsensusRound.create(
            number=round_number,
            timestamp=Timestamp.now().value
        )
        
        return self.current_round
    
    def get_consensus_stats(self) -> dict:
        """Retorna estatísticas do consenso"""
        stats = self._optimized_service.get_consensus_stats()
        stats.update({
            "total_validators": len(self.active_validators),
            "current_round": self.current_round.number if self.current_round else 0,
            "min_stake_cnb": float(BlockchainConfig.MIN_STAKE_FOR_VALIDATION)
        })
        return stats
    
    def get_top_validators(self, limit: int = 10) -> List[Validator]:
        """Retorna os top N validadores por stake"""
        return self._optimized_service.validator_selector.get_top_validators(limit)
    
    def get_total_stake(self) -> Decimal:
        """Retorna stake total"""
        return self._optimized_service.validator_selector.get_total_stake()
    
    def clear_selection_cache(self) -> None:
        """Limpa cache de seleções"""
        self._optimized_service.validator_selector.clear_cache()
    
    def _sort_validators_by_stake(self) -> None:
        """Ordena validadores por poder de staking (usando sistema otimizado)"""
        # O sistema otimizado já mantém validadores ordenados
        pass
    
    def _validate_previous_hash(self, previous_hash: str) -> bool:
        """Valida o hash do bloco anterior"""
        return len(previous_hash) == 64 and all(c in "0123456789abcdef" for c in previous_hash)
    
    def _validate_transactions(self, transactions: List[dict]) -> bool:
        """Valida uma lista de transações"""
        for tx in transactions:
            required_fields = ["from", "to", "amount", "signature"]
            for field in required_fields:
                if field not in tx:
                    return False
        return True