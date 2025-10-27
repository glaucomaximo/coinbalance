"""
Serviço de Consenso - Implementa algoritmo PoS/DPoS
"""

from typing import List, Optional
from decimal import Decimal
import random

from ..entities.validator import Validator
from ..value_objects.consensus_round import ConsensusRound
from ..value_objects.validator_id import ValidatorId
from ...shared.value_objects.timestamp import Timestamp


class ConsensusService:
    """
    Serviço principal para gerenciar o consenso PoS/DPoS.
    
    Responsabilidades:
    - Selecionar validadores para cada rodada
    - Coordenar processo de validação
    - Calcular recompensas
    - Gerenciar política monetária
    """
    
    def __init__(self):
        self.active_validators: List[Validator] = []
        self.current_round: Optional[ConsensusRound] = None
        self.block_time_seconds = 5  # Tempo entre blocos
    
    def register_validator(self, validator: Validator) -> None:
        """
        Registra um novo validador no sistema de consenso.
        
        Args:
            validator: Validador a ser registrado
        """
        if validator.is_active:
            self.active_validators.append(validator)
            self._sort_validators_by_stake()
    
    def remove_validator(self, validator_id: ValidatorId) -> None:
        """
        Remove um validador do sistema de consenso.
        
        Args:
            validator_id: ID do validador a ser removido
        """
        self.active_validators = [
            v for v in self.active_validators 
            if v.id != validator_id
        ]
    
    def select_validator_for_round(self, round_number: int) -> Optional[Validator]:
        """
        Seleciona um validador para uma rodada específica.
        
        Algoritmo de seleção:
        1. Ordena validadores por poder de staking
        2. Aplica seleção probabilística ponderada
        3. Considera performance histórica
        
        Args:
            round_number: Número da rodada
            
        Returns:
            Validador selecionado ou None se não houver validadores
        """
        if not self.active_validators:
            return None
        
        # Ordenar por poder de staking (maior primeiro)
        sorted_validators = sorted(
            self.active_validators,
            key=lambda v: v.get_staking_power(),
            reverse=True
        )
        
        # Seleção probabilística ponderada
        total_stake = sum(v.get_staking_power() for v in sorted_validators)
        
        if total_stake == 0:
            return None
        
        # Usar round_number como seed para determinismo
        random.seed(round_number)
        
        # Seleção ponderada por stake
        target = random.uniform(0, float(total_stake))
        current_sum = Decimal("0")
        
        for validator in sorted_validators:
            current_sum += validator.get_staking_power()
            if current_sum >= Decimal(str(target)):
                return validator
        
        # Fallback para o validador com maior stake
        return sorted_validators[0]
    
    def validate_block(self, validator: Validator, block_data: dict) -> bool:
        """
        Valida um bloco usando o validador selecionado.
        
        Args:
            validator: Validador responsável pela validação
            block_data: Dados do bloco a ser validado
            
        Returns:
            True se o bloco for válido, False caso contrário
        """
        # Verificar se o validador está ativo
        if not validator.is_active:
            return False
        
        # Verificar se o validador tem stake suficiente
        min_stake = Decimal("1000")  # 1000 CNB mínimo
        if validator.get_staking_power() < min_stake:
            return False
        
        # Simular validação (em implementação real, seria mais complexa)
        try:
            # Validar estrutura do bloco
            required_fields = ["hash", "previous_hash", "transactions", "timestamp"]
            for field in required_fields:
                if field not in block_data:
                    return False
            
            # Validar hash do bloco anterior
            if not self._validate_previous_hash(block_data["previous_hash"]):
                return False
            
            # Validar transações
            if not self._validate_transactions(block_data["transactions"]):
                return False
            
            # Registrar validação bem-sucedida
            validator.record_block_validation()
            
            return True
            
        except Exception:
            return False
    
    def calculate_rewards(self, validator: Validator, block_height: int) -> Decimal:
        """
        Calcula recompensas para um validador baseado na performance.
        
        Args:
            validator: Validador que receberá recompensas
            block_height: Altura do bloco atual
            
        Returns:
            Quantidade de recompensas em CNB
        """
        # Recompensa base por bloco validado
        base_reward = Decimal("0.1")  # 0.1 CNB por bloco
        
        # Multiplicador baseado no stake
        stake_multiplier = min(validator.get_staking_power() / Decimal("10000"), Decimal("2.0"))
        
        # Multiplicador baseado na performance
        performance_multiplier = Decimal("1.0")
        if validator.blocks_validated > 0:
            # Incentivar validadores consistentes
            performance_multiplier = Decimal("1.1")
        
        # Calcular recompensa final
        total_reward = base_reward * stake_multiplier * performance_multiplier
        
        return total_reward
    
    def start_new_round(self) -> ConsensusRound:
        """
        Inicia uma nova rodada de consenso.
        
        Returns:
            Nova rodada de consenso
        """
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
        """
        Retorna estatísticas do sistema de consenso.
        
        Returns:
            Dicionário com estatísticas
        """
        total_validators = len(self.active_validators)
        total_stake = sum(v.get_staking_power() for v in self.active_validators)
        
        return {
            "total_validators": total_validators,
            "total_stake_cnb": float(total_stake),
            "current_round": self.current_round.number if self.current_round else 0,
            "block_time_seconds": self.block_time_seconds,
            "min_stake_cnb": 1000.0
        }
    
    def _sort_validators_by_stake(self) -> None:
        """Ordena validadores por poder de staking"""
        self.active_validators.sort(
            key=lambda v: v.get_staking_power(),
            reverse=True
        )
    
    def _validate_previous_hash(self, previous_hash: str) -> bool:
        """
        Valida o hash do bloco anterior.
        
        Args:
            previous_hash: Hash do bloco anterior
            
        Returns:
            True se o hash for válido
        """
        # Implementação simplificada
        return len(previous_hash) == 64 and all(c in "0123456789abcdef" for c in previous_hash)
    
    def _validate_transactions(self, transactions: List[dict]) -> bool:
        """
        Valida uma lista de transações.
        
        Args:
            transactions: Lista de transações
            
        Returns:
            True se todas as transações forem válidas
        """
        # Implementação simplificada
        for tx in transactions:
            required_fields = ["from", "to", "amount", "signature"]
            for field in required_fields:
                if field not in tx:
                    return False
        
        return True
