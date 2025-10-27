"""
Entidade SustainableDeFi - DeFi Sustentável e ESG-Compliant
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from decimal import Decimal
from enum import Enum

from ...shared.value_objects.money import Money
from ...shared.value_objects.timestamp import Timestamp
from ...shared.value_objects.wallet_address import WalletAddress
from ...shared.domain_events.base import DomainEvent


class DeFiProductType(Enum):
    """Tipos de produtos DeFi sustentáveis"""
    GREEN_STAKING = "green_staking"           # Staking verde
    IMPACT_LENDING = "impact_lending"         # Empréstimos com impacto
    SUSTAINABLE_YIELD = "sustainable_yield"    # Yield sustentável
    CARBON_OFFSET_POOL = "carbon_offset_pool"  # Pool de compensação de carbono
    SOCIAL_BONDS = "social_bonds"             # Títulos sociais
    IMPACT_FARMING = "impact_farming"         # Farming de impacto


class SustainabilityRating(Enum):
    """Classificação de sustentabilidade"""
    AAA = "AAA"  # Excelente
    AA = "AA"    # Muito bom
    A = "A"      # Bom
    BBB = "BBB"  # Satisfatório
    BB = "BB"    # Regular
    B = "B"      # Ruim
    CCC = "CCC"  # Muito ruim


@dataclass
class SustainableDeFiProduct:
    """
    Entidade SustainableDeFiProduct - Aggregate Root.
    
    Representa um produto DeFi sustentável que gera retornos
    enquanto promove impacto social e ambiental positivo.
    
    Características Disruptivas:
    - Retornos alinhados com impacto ESG
    - Transparência total via blockchain
    - Governança participativa
    - Métricas de sustentabilidade verificáveis
    - Incentivos para comportamento sustentável
    """
    
    # Identity
    product_id: str
    name: str
    description: str
    product_type: DeFiProductType
    
    # Financial Parameters
    apy_rate: Decimal  # Annual Percentage Yield
    minimum_stake: Money
    maximum_stake: Money
    lock_period_days: int
    
    # Sustainability Parameters
    sustainability_rating: SustainabilityRating
    carbon_offset_per_cnb: Decimal  # kg CO2 offset per CNB staked
    social_impact_multiplier: Decimal  # Multiplicador de impacto social
    environmental_impact_score: Decimal  # 0-100
    
    # Current State
    total_staked: Money = Money(Decimal("0"))
    active_stakers: int = 0
    total_rewards_distributed: Money = Money(Decimal("0"))
    total_carbon_offset: Decimal = Decimal("0")
    
    # Status
    is_active: bool = True
    created_at: Timestamp = field(default_factory=Timestamp.now)
    
    # Domain Events
    _events: List[DomainEvent] = field(default_factory=list, init=False, repr=False)
    
    def __post_init__(self):
        """Validação após inicialização"""
        self._validate()
    
    def _validate(self):
        """Valida invariantes do domínio"""
        if self.apy_rate <= 0:
            raise ValueError("APY rate must be positive")
        if self.minimum_stake.to_cnb() <= 0:
            raise ValueError("Minimum stake must be positive")
        if self.maximum_stake.to_cnb() <= self.minimum_stake.to_cnb():
            raise ValueError("Maximum stake must be greater than minimum stake")
        if self.lock_period_days <= 0:
            raise ValueError("Lock period must be positive")
        if self.carbon_offset_per_cnb < 0:
            raise ValueError("Carbon offset per CNB must be non-negative")
        if self.social_impact_multiplier < 0:
            raise ValueError("Social impact multiplier must be non-negative")
    
    @classmethod
    def create_green_staking(
        cls,
        product_id: str,
        name: str,
        description: str,
        apy_rate: Decimal,
        minimum_stake: Money,
        maximum_stake: Money,
        lock_period_days: int,
        carbon_offset_per_cnb: Decimal,
        environmental_impact_score: Decimal
    ) -> "SustainableDeFiProduct":
        """Cria um produto de staking verde"""
        return cls(
            product_id=product_id,
            name=name,
            description=description,
            product_type=DeFiProductType.GREEN_STAKING,
            apy_rate=apy_rate,
            minimum_stake=minimum_stake,
            maximum_stake=maximum_stake,
            lock_period_days=lock_period_days,
            sustainability_rating=SustainabilityRating.AAA,
            carbon_offset_per_cnb=carbon_offset_per_cnb,
            social_impact_multiplier=Decimal("1.0"),
            environmental_impact_score=environmental_impact_score
        )
    
    @classmethod
    def create_impact_lending(
        cls,
        product_id: str,
        name: str,
        description: str,
        apy_rate: Decimal,
        minimum_stake: Money,
        maximum_stake: Money,
        lock_period_days: int,
        social_impact_multiplier: Decimal
    ) -> "SustainableDeFiProduct":
        """Cria um produto de empréstimo com impacto social"""
        return cls(
            product_id=product_id,
            name=name,
            description=description,
            product_type=DeFiProductType.IMPACT_LENDING,
            apy_rate=apy_rate,
            minimum_stake=minimum_stake,
            maximum_stake=maximum_stake,
            lock_period_days=lock_period_days,
            sustainability_rating=SustainabilityRating.AA,
            carbon_offset_per_cnb=Decimal("0"),
            social_impact_multiplier=social_impact_multiplier,
            environmental_impact_score=Decimal("50")
        )
    
    def calculate_sustainable_apy(self, staked_amount: Money) -> Decimal:
        """Calcula APY considerando impacto sustentável"""
        base_apy = Decimal(str(self.apy_rate))
        
        # Bonus por impacto ambiental
        environmental_bonus = (Decimal(str(self.environmental_impact_score)) / Decimal("100")) * Decimal("0.02")  # Até 2% bonus
        
        # Bonus por impacto social
        social_bonus = (self.social_impact_multiplier - Decimal("1")) * Decimal("0.01")  # Até 1% bonus
        
        # Bonus por quantidade staked (incentivo para maiores stakes)
        stake_bonus = min(staked_amount.to_cnb() / Decimal("1000"), Decimal("0.01"))  # Até 1% bonus
        
        total_apy = base_apy + environmental_bonus + social_bonus + stake_bonus
        return min(total_apy, Decimal("0.50"))  # Cap at 50% APY
    
    def calculate_carbon_offset(self, staked_amount: Money) -> Decimal:
        """Calcula compensação de carbono baseada no stake"""
        return staked_amount.to_cnb() * Decimal(str(self.carbon_offset_per_cnb))
    
    def calculate_social_impact(self, staked_amount: Money) -> Decimal:
        """Calcula impacto social baseado no stake"""
        return staked_amount.to_cnb() * self.social_impact_multiplier
    
    def get_sustainability_score(self) -> Decimal:
        """Calcula score total de sustentabilidade (0-100)"""
        environmental_score = Decimal(str(self.environmental_impact_score))
        social_score = min(self.social_impact_multiplier * Decimal("20"), Decimal("50"))
        carbon_score = min(Decimal(str(self.carbon_offset_per_cnb)) * Decimal("10"), Decimal("30"))
        
        return min(environmental_score + social_score + carbon_score, Decimal("100"))
    
    def is_eligible_for_stake(self, amount: Money) -> bool:
        """Verifica se o valor é elegível para stake"""
        return (self.minimum_stake <= amount <= self.maximum_stake and 
                self.is_active)
    
    def get_events(self) -> List[DomainEvent]:
        """Retorna eventos de domínio"""
        return self._events.copy()
    
    def clear_events(self) -> None:
        """Limpa eventos de domínio"""
        self._events.clear()
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "product_type": self.product_type.value,
            "apy_rate": float(self.apy_rate),
            "minimum_stake": float(self.minimum_stake.to_cnb()),
            "maximum_stake": float(self.maximum_stake.to_cnb()),
            "lock_period_days": self.lock_period_days,
            "sustainability_rating": self.sustainability_rating.value,
            "carbon_offset_per_cnb": float(self.carbon_offset_per_cnb),
            "social_impact_multiplier": float(self.social_impact_multiplier),
            "environmental_impact_score": float(self.environmental_impact_score),
            "total_staked": float(self.total_staked.to_cnb()),
            "active_stakers": self.active_stakers,
            "total_rewards_distributed": float(self.total_rewards_distributed.to_cnb()),
            "total_carbon_offset": float(self.total_carbon_offset),
            "is_active": self.is_active,
            "sustainability_score": float(self.get_sustainability_score())
        }
