"""
Serviço DeFi Sustentável - Economia da Consciência
"""

from decimal import Decimal
from typing import List, Dict, Optional
from dataclasses import dataclass

from ..entities.sustainable_defi_product import (
    SustainableDeFiProduct, 
    DeFiProductType, 
    SustainabilityRating
)
from ...shared.value_objects.money import Money
from ...shared.value_objects.wallet_address import WalletAddress
from ...shared.value_objects.timestamp import Timestamp


@dataclass(frozen=True)
class StakePosition:
    """Posição de stake em produto DeFi sustentável"""
    
    position_id: str
    staker_address: WalletAddress
    product_id: str
    staked_amount: Money
    apy_rate: Decimal
    start_timestamp: Timestamp
    end_timestamp: Timestamp
    is_active: bool = True
    
    def calculate_current_rewards(self) -> Money:
        """Calcula recompensas acumuladas até agora"""
        if not self.is_active:
            return Money(Decimal("0"))
        
        current_time = Timestamp.now()
        if current_time.value <= self.start_timestamp.value:
            return Money(Decimal("0"))
        
        # Calcular tempo decorrido
        elapsed_seconds = current_time.value - self.start_timestamp.value
        elapsed_days = Decimal(elapsed_seconds) / Decimal("86400")  # segundos por dia
        
        # Calcular recompensas
        daily_rate = self.apy_rate / Decimal("365")
        rewards = self.staked_amount.to_cnb() * daily_rate * elapsed_days
        
        return Money(rewards)


class SustainableDeFiService:
    """
    Serviço DeFi Sustentável.
    
    Responsabilidades:
    - Gerenciar produtos DeFi sustentáveis
    - Facilitar staking com impacto ESG
    - Calcular recompensas baseadas em sustentabilidade
    - Promover economia da consciência
    """
    
    def __init__(self):
        self.products: List[SustainableDeFiProduct] = []
        self.stake_positions: List[StakePosition] = []
        self.total_volume_staked = Money(Decimal("0"))
        self.total_carbon_offset = Decimal("0")
        self.total_social_impact = Decimal("0")
    
    def create_green_staking_product(
        self,
        product_id: str,
        name: str,
        description: str,
        apy_rate: Decimal,
        minimum_stake: Money,
        maximum_stake: Money,
        lock_period_days: int,
        carbon_offset_per_cnb: Decimal,
        environmental_impact_score: Decimal
    ) -> SustainableDeFiProduct:
        """Cria um produto de staking verde"""
        product = SustainableDeFiProduct.create_green_staking(
            product_id=product_id,
            name=name,
            description=description,
            apy_rate=apy_rate,
            minimum_stake=minimum_stake,
            maximum_stake=maximum_stake,
            lock_period_days=lock_period_days,
            carbon_offset_per_cnb=carbon_offset_per_cnb,
            environmental_impact_score=environmental_impact_score
        )
        
        self.products.append(product)
        return product
    
    def create_impact_lending_product(
        self,
        product_id: str,
        name: str,
        description: str,
        apy_rate: Decimal,
        minimum_stake: Money,
        maximum_stake: Money,
        lock_period_days: int,
        social_impact_multiplier: Decimal
    ) -> SustainableDeFiProduct:
        """Cria um produto de empréstimo com impacto social"""
        product = SustainableDeFiProduct.create_impact_lending(
            product_id=product_id,
            name=name,
            description=description,
            apy_rate=apy_rate,
            minimum_stake=minimum_stake,
            maximum_stake=maximum_stake,
            lock_period_days=lock_period_days,
            social_impact_multiplier=social_impact_multiplier
        )
        
        self.products.append(product)
        return product
    
    def stake_in_product(
        self,
        staker_address: WalletAddress,
        product_id: str,
        amount: Money
    ) -> Optional[StakePosition]:
        """Stake em um produto DeFi sustentável"""
        product = self._find_product_by_id(product_id)
        if not product:
            return None
        
        if not product.is_eligible_for_stake(amount):
            return None
        
        # Criar posição de stake
        position_id = f"{product_id}_{staker_address}_{Timestamp.now().value}"
        start_time = Timestamp.now()
        end_time = Timestamp(start_time.value + (product.lock_period_days * 86400))
        
        position = StakePosition(
            position_id=position_id,
            staker_address=staker_address,
            product_id=product_id,
            staked_amount=amount,
            apy_rate=product.calculate_sustainable_apy(amount),
            start_timestamp=start_time,
            end_timestamp=end_time
        )
        
        self.stake_positions.append(position)
        
        # Atualizar estatísticas do produto
        product.total_staked += amount
        product.active_stakers += 1
        
        # Atualizar estatísticas globais
        self.total_volume_staked += amount
        self.total_carbon_offset += product.calculate_carbon_offset(amount)
        self.total_social_impact += product.calculate_social_impact(amount)
        
        return position
    
    def unstake_from_product(self, position_id: str) -> Optional[Money]:
        """Remove stake de um produto"""
        position = self._find_position_by_id(position_id)
        if not position or not position.is_active:
            return None
        
        # Verificar se o período de lock terminou
        current_time = Timestamp.now()
        if current_time.value < position.end_timestamp.value:
            return None  # Ainda no período de lock
        
        # Calcular recompensas finais
        final_rewards = position.calculate_current_rewards()
        
        # Marcar posição como inativa
        position.is_active = False
        
        # Atualizar estatísticas do produto
        product = self._find_product_by_id(position.product_id)
        if product:
            product.total_staked -= position.staked_amount
            product.active_stakers -= 1
            product.total_rewards_distributed += final_rewards
        
        # Atualizar estatísticas globais
        self.total_volume_staked -= position.staked_amount
        
        return final_rewards
    
    def get_active_products(self) -> List[SustainableDeFiProduct]:
        """Retorna produtos ativos"""
        return [p for p in self.products if p.is_active]
    
    def get_products_by_type(self, product_type: DeFiProductType) -> List[SustainableDeFiProduct]:
        """Retorna produtos por tipo"""
        return [p for p in self.products if p.product_type == product_type and p.is_active]
    
    def get_top_sustainability_products(self, limit: int = 5) -> List[SustainableDeFiProduct]:
        """Retorna produtos com maior score de sustentabilidade"""
        active_products = self.get_active_products()
        sorted_products = sorted(
            active_products, 
            key=lambda p: p.get_sustainability_score(), 
            reverse=True
        )
        return sorted_products[:limit]
    
    def get_staker_positions(self, staker_address: WalletAddress) -> List[StakePosition]:
        """Retorna posições de stake de um usuário"""
        return [
            p for p in self.stake_positions 
            if p.staker_address == staker_address and p.is_active
        ]
    
    def calculate_total_rewards(self, staker_address: WalletAddress) -> Money:
        """Calcula total de recompensas de um staker"""
        positions = self.get_staker_positions(staker_address)
        total_rewards = Money(Decimal("0"))
        
        for position in positions:
            rewards = position.calculate_current_rewards()
            total_rewards += rewards
        
        return total_rewards
    
    def get_defi_statistics(self) -> Dict[str, float]:
        """Retorna estatísticas do DeFi sustentável"""
        active_products = len(self.get_active_products())
        total_stakers = len(set(p.staker_address for p in self.stake_positions if p.is_active))
        total_rewards_distributed = sum(p.total_rewards_distributed.to_cnb() for p in self.products)
        
        # Calcular APY médio ponderado
        if self.total_volume_staked.to_cnb() > 0:
            weighted_apy = sum(
                Decimal(str(p.apy_rate)) * p.total_staked.to_cnb() 
                for p in self.products if p.is_active
            ) / self.total_volume_staked.to_cnb()
        else:
            weighted_apy = Decimal("0")
        
        return {
            "active_products": active_products,
            "total_stakers": total_stakers,
            "total_volume_staked_cnb": float(self.total_volume_staked.to_cnb()),
            "total_rewards_distributed_cnb": float(total_rewards_distributed),
            "total_carbon_offset_kg": float(self.total_carbon_offset),
            "total_social_impact": float(self.total_social_impact),
            "average_weighted_apy": float(weighted_apy),
            "products_by_type": {
                product_type.value: len(self.get_products_by_type(product_type))
                for product_type in DeFiProductType
            }
        }
    
    def get_sustainability_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Retorna ranking de stakers por impacto sustentável"""
        staker_stats = {}
        
        for position in self.stake_positions:
            if not position.is_active:
                continue
            
            staker_addr = str(position.staker_address)
            if staker_addr not in staker_stats:
                staker_stats[staker_addr] = {
                    "address": staker_addr,
                    "total_staked": Money(Decimal("0")),
                    "total_carbon_offset": Decimal("0"),
                    "total_social_impact": Decimal("0"),
                    "sustainability_score": Decimal("0")
                }
            
            product = self._find_product_by_id(position.product_id)
            if product:
                staker_stats[staker_addr]["total_staked"] += position.staked_amount
                staker_stats[staker_addr]["total_carbon_offset"] += product.calculate_carbon_offset(position.staked_amount)
                staker_stats[staker_addr]["total_social_impact"] += product.calculate_social_impact(position.staked_amount)
        
        # Calcular score de sustentabilidade para cada staker
        for staker_addr, stats in staker_stats.items():
            carbon_score = min(stats["total_carbon_offset"] * Decimal("0.1"), Decimal("50"))
            social_score = min(stats["total_social_impact"] * Decimal("0.05"), Decimal("30"))
            stake_score = min(stats["total_staked"].to_cnb() / Decimal("100"), Decimal("20"))
            
            stats["sustainability_score"] = carbon_score + social_score + stake_score
        
        # Ordenar por score de sustentabilidade
        sorted_stakers = sorted(
            staker_stats.values(),
            key=lambda x: x["sustainability_score"],
            reverse=True
        )
        
        return [
            {
                "address": staker["address"],
                "total_staked_cnb": float(staker["total_staked"].to_cnb()),
                "total_carbon_offset_kg": float(staker["total_carbon_offset"]),
                "total_social_impact": float(staker["total_social_impact"]),
                "sustainability_score": float(staker["sustainability_score"])
            }
            for staker in sorted_stakers[:limit]
        ]
    
    def _find_product_by_id(self, product_id: str) -> Optional[SustainableDeFiProduct]:
        """Busca produto por ID"""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    
    def _find_position_by_id(self, position_id: str) -> Optional[StakePosition]:
        """Busca posição por ID"""
        for position in self.stake_positions:
            if position.position_id == position_id:
                return position
        return None
