"""
Serviço de Política Monetária CNB - ESG-compliant
"""

from decimal import Decimal
from typing import Dict, Optional
from dataclasses import dataclass

from ..value_objects.consensus_round import ConsensusRound
from ...shared.value_objects.money import Money
from ...shared.config.blockchain_config import BlockchainConfig


@dataclass(frozen=True)
class MonetaryPolicy:
    """
    Política monetária ESG-compliant para CNB.
    
    Características:
    - Supply inicial: 21M CNB (como Bitcoin)
    - Inflação controlada: 2% ao ano
    - Deflação gradual após 10 anos
    - Recompensas para stakers: 15% do total
    """
    
    # Parâmetros da política monetária (usando configurações centralizadas)
    INITIAL_SUPPLY: Decimal = BlockchainConfig.INITIAL_SUPPLY
    ANNUAL_INFLATION_RATE: Decimal = BlockchainConfig.ANNUAL_INFLATION_RATE
    STAKING_REWARD_RATE: Decimal = BlockchainConfig.STAKING_REWARD_RATE
    BLOCKS_PER_YEAR: int = BlockchainConfig.BLOCKS_PER_YEAR
    HALVING_INTERVAL_YEARS: int = BlockchainConfig.HALVING_INTERVAL_YEARS
    
    @classmethod
    def calculate_current_supply(cls, block_height: int) -> Money:
        """
        Calcula o supply atual de CNB baseado na altura do bloco.
        
        Args:
            block_height: Altura atual do bloco
            
        Returns:
            Supply atual em CNB
        """
        years_passed = Decimal(block_height) / Decimal(cls.BLOCKS_PER_YEAR)
        
        # Calcular supply com inflação anual
        if years_passed <= 10:
            # Primeiros 10 anos: inflação de 2% ao ano
            supply = cls.INITIAL_SUPPLY * (Decimal("1") + cls.ANNUAL_INFLATION_RATE) ** years_passed
        else:
            # Após 10 anos: deflação gradual
            base_supply = cls.INITIAL_SUPPLY * (Decimal("1") + cls.ANNUAL_INFLATION_RATE) ** Decimal("10")
            halving_cycles = (years_passed - Decimal("10")) // Decimal(str(cls.HALVING_INTERVAL_YEARS))
            supply = base_supply / (Decimal("2") ** halving_cycles)
        
        return Money(supply)
    
    @classmethod
    def calculate_block_reward(cls, block_height: int) -> Money:
        """
        Calcula a recompensa por bloco baseada na altura.
        
        Args:
            block_height: Altura do bloco
            
        Returns:
            Recompensa do bloco em CNB
        """
        years_passed = Decimal(block_height) / Decimal(cls.BLOCKS_PER_YEAR)
        
        if years_passed <= 10:
            # Primeiros 10 anos: recompensa baseada na inflação
            annual_reward = cls.INITIAL_SUPPLY * cls.ANNUAL_INFLATION_RATE
            block_reward = annual_reward / Decimal(cls.BLOCKS_PER_YEAR)
        else:
            # Após 10 anos: recompensa reduzida pela metade a cada 10 anos
            halving_cycles = (years_passed - Decimal("10")) // Decimal(str(cls.HALVING_INTERVAL_YEARS))
            base_reward = cls.INITIAL_SUPPLY * cls.ANNUAL_INFLATION_RATE / Decimal(cls.BLOCKS_PER_YEAR)
            block_reward = base_reward / (Decimal("2") ** halving_cycles)
        
        return Money(block_reward)
    
    @classmethod
    def calculate_staking_reward(cls, block_height: int) -> Money:
        """
        Calcula a recompensa para stakers.
        
        Args:
            block_height: Altura do bloco
            
        Returns:
            Recompensa para stakers em CNB
        """
        block_reward = cls.calculate_block_reward(block_height)
        staking_reward = block_reward * cls.STAKING_REWARD_RATE
        
        return staking_reward
    
    @classmethod
    def get_policy_stats(cls, block_height: int) -> Dict[str, float]:
        """
        Retorna estatísticas da política monetária.
        
        Args:
            block_height: Altura atual do bloco
            
        Returns:
            Dicionário com estatísticas
        """
        current_supply = cls.calculate_current_supply(block_height)
        block_reward = cls.calculate_block_reward(block_height)
        staking_reward = cls.calculate_staking_reward(block_height)
        
        years_passed = float(Decimal(block_height) / Decimal(cls.BLOCKS_PER_YEAR))
        
        return {
            "block_height": block_height,
            "years_passed": years_passed,
            "current_supply_cnb": float(current_supply.to_cnb()),
            "block_reward_cnb": float(block_reward.to_cnb()),
            "staking_reward_cnb": float(staking_reward.to_cnb()),
            "annual_inflation_rate": float(cls.ANNUAL_INFLATION_RATE),
            "staking_reward_rate": float(cls.STAKING_REWARD_RATE),
            "initial_supply_cnb": float(cls.INITIAL_SUPPLY)
        }


class MonetaryPolicyService:
    """
    Serviço para gerenciar a política monetária CNB.
    
    Responsabilidades:
    - Calcular supply atual
    - Calcular recompensas
    - Aplicar política ESG
    - Monitorar inflação
    """
    
    def __init__(self):
        self.policy = MonetaryPolicy()
        self.current_block_height = 0
    
    def set_block_height(self, block_height: int) -> None:
        """
        Define a altura atual do bloco.
        
        Args:
            block_height: Altura do bloco
        """
        self.current_block_height = block_height
    
    def get_current_supply(self) -> Money:
        """
        Retorna o supply atual de CNB.
        
        Returns:
            Supply atual
        """
        return self.policy.calculate_current_supply(self.current_block_height)
    
    def get_block_reward(self) -> Money:
        """
        Retorna a recompensa do bloco atual.
        
        Returns:
            Recompensa do bloco
        """
        return self.policy.calculate_block_reward(self.current_block_height)
    
    def get_staking_reward(self) -> Money:
        """
        Retorna a recompensa para stakers do bloco atual.
        
        Returns:
            Recompensa para stakers
        """
        return self.policy.calculate_staking_reward(self.current_block_height)
    
    def get_policy_stats(self) -> Dict[str, float]:
        """
        Retorna estatísticas da política monetária atual.
        
        Returns:
            Estatísticas da política
        """
        return self.policy.get_policy_stats(self.current_block_height)
    
    def is_inflation_phase(self) -> bool:
        """
        Verifica se estamos na fase de inflação.
        
        Returns:
            True se estivermos na fase de inflação
        """
        years_passed = Decimal(self.current_block_height) / Decimal(self.policy.BLOCKS_PER_YEAR)
        return years_passed <= Decimal("10")
    
    def get_next_halving_block(self) -> int:
        """
        Retorna a altura do próximo halving.
        
        Returns:
            Altura do próximo halving
        """
        years_passed = Decimal(self.current_block_height) / Decimal(self.policy.BLOCKS_PER_YEAR)
        
        if years_passed <= Decimal("10"):
            # Primeiro halving será no ano 10
            return int(Decimal("10") * Decimal(self.policy.BLOCKS_PER_YEAR))
        else:
            # Próximo halving será no próximo ciclo de 10 anos
            next_halving_year = ((years_passed - Decimal("10")) // Decimal(str(self.policy.HALVING_INTERVAL_YEARS)) + Decimal("1")) * Decimal(str(self.policy.HALVING_INTERVAL_YEARS)) + Decimal("10")
            return int(next_halving_year * Decimal(self.policy.BLOCKS_PER_YEAR))
