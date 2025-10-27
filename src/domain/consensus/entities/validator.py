"""
Entidade Validator - Representa um validador no sistema PoS
"""

from dataclasses import dataclass, field
from typing import List, Optional
from decimal import Decimal

from ..value_objects.validator_id import ValidatorId
from ..value_objects.stake_amount import StakeAmount
from ...shared.value_objects.wallet_address import WalletAddress
from ...shared.value_objects.timestamp import Timestamp
from ...shared.domain_events.base import DomainEvent


@dataclass
class Validator:
    """
    Entidade Validator - Representa um validador no sistema PoS/DPoS.
    
    Responsabilidades:
    - Participar do consenso
    - Manter stake depositado
    - Validar blocos
    - Receber recompensas
    
    Invariantes:
    - Stake deve ser maior que mínimo
    - Status deve ser consistente
    - Endereço deve ser único
    """
    
    # Identity
    id: ValidatorId
    wallet_address: WalletAddress
    
    # Attributes
    stake_amount: StakeAmount
    is_active: bool
    created_at: Timestamp
    updated_at: Timestamp
    
    # Performance metrics
    blocks_validated: int = 0
    total_rewards: Decimal = Decimal("0")
    last_validation_at: Optional[Timestamp] = None
    
    # Metadata
    metadata: dict = field(default_factory=dict)
    
    # Domain Events (não persistidos)
    _events: List[DomainEvent] = field(default_factory=list, init=False, repr=False)
    
    @classmethod
    def create(
        cls,
        wallet_address: WalletAddress,
        stake_amount: StakeAmount,
        metadata: Optional[dict] = None
    ) -> 'Validator':
        """
        Factory method para criar um novo validador.
        
        Args:
            wallet_address: Endereço da carteira do validador
            stake_amount: Quantidade de CNB em stake
            metadata: Metadados adicionais
            
        Returns:
            Nova instância de Validator
            
        Raises:
            ValueError: Se os parâmetros forem inválidos
        """
        now = Timestamp.now()
        
        validator = cls(
            id=ValidatorId.generate(),
            wallet_address=wallet_address,
            stake_amount=stake_amount,
            is_active=True,
            created_at=now,
            updated_at=now,
            metadata=metadata or {}
        )
        
        # Adicionar evento de domínio
        # validator._add_event(ValidatorRegistered(
        #     validator_id=validator.id,
        #     wallet_address=wallet_address,
        #     stake_amount=stake_amount,
        #     timestamp=now
        # ))
        
        return validator
    
    def increase_stake(self, additional_stake: StakeAmount) -> None:
        """
        Aumenta o stake do validador.
        
        Args:
            additional_stake: Quantidade adicional para stake
            
        Raises:
            ValueError: Se o valor for inválido
        """
        if additional_stake.amount.amount <= 0:
            raise ValueError("Stake adicional deve ser maior que zero")
        
        old_stake = self.stake_amount
        self.stake_amount = self.stake_amount + additional_stake
        self.updated_at = Timestamp.now()
        
        # Adicionar evento de domínio
        # self._add_event(StakeIncreased(
        #     validator_id=self.id,
        #     old_amount=old_stake,
        #     new_amount=self.stake_amount,
        #     timestamp=self.updated_at
        # ))
    
    def decrease_stake(self, stake_to_remove: StakeAmount) -> None:
        """
        Diminui o stake do validador.
        
        Args:
            stake_to_remove: Quantidade a remover do stake
            
        Raises:
            ValueError: Se o valor for inválido ou resultar em stake insuficiente
        """
        if stake_to_remove.amount.amount <= 0:
            raise ValueError("Stake a remover deve ser maior que zero")
        
        new_stake = self.stake_amount - stake_to_remove
        
        # Verificar se ainda atende ao mínimo
        min_stake = StakeAmount.from_cnb(1000)
        if new_stake < min_stake:
            raise ValueError(f"Stake resultante deve ser pelo menos {min_stake}")
        
        old_stake = self.stake_amount
        self.stake_amount = new_stake
        self.updated_at = Timestamp.now()
        
        # Adicionar evento de domínio
        # self._add_event(StakeDecreased(
        #     validator_id=self.id,
        #     old_amount=old_stake,
        #     new_amount=self.stake_amount,
        #     timestamp=self.updated_at
        # ))
    
    def deactivate(self) -> None:
        """Desativa o validador"""
        if not self.is_active:
            raise ValueError("Validador já está desativado")
        
        self.is_active = False
        self.updated_at = Timestamp.now()
        
        # Adicionar evento de domínio
        # self._add_event(ValidatorDeactivated(
        #     validator_id=self.id,
        #     timestamp=self.updated_at
        # ))
    
    def activate(self) -> None:
        """Reativa o validador"""
        if self.is_active:
            raise ValueError("Validador já está ativo")
        
        self.is_active = True
        self.updated_at = Timestamp.now()
        
        # Adicionar evento de domínio
        # self._add_event(ValidatorActivated(
        #     validator_id=self.id,
        #     timestamp=self.updated_at
        # ))
    
    def record_block_validation(self) -> None:
        """Registra validação de um bloco"""
        self.blocks_validated += 1
        self.last_validation_at = Timestamp.now()
        self.updated_at = self.last_validation_at
    
    def add_rewards(self, reward_amount: Decimal) -> None:
        """
        Adiciona recompensas ao validador.
        
        Args:
            reward_amount: Quantidade de recompensa em CNB
        """
        if reward_amount <= 0:
            raise ValueError("Recompensa deve ser positiva")
        
        self.total_rewards += reward_amount
        self.updated_at = Timestamp.now()
        
        # Adicionar evento de domínio
        # self._add_event(RewardsAdded(
        #     validator_id=self.id,
        #     amount=reward_amount,
        #     total_rewards=self.total_rewards,
        #     timestamp=self.updated_at
        # ))
    
    def get_staking_power(self) -> Decimal:
        """
        Calcula o poder de staking do validador.
        
        Por enquanto, é proporcional ao stake depositado.
        Futuramente será influenciado pelo C-Score.
        
        Returns:
            Poder de staking como Decimal
        """
        return self.stake_amount.to_cnb()
    
    def _add_event(self, event: DomainEvent) -> None:
        """Adiciona evento de domínio"""
        self._events.append(event)
    
    def get_events(self) -> List[DomainEvent]:
        """Retorna eventos de domínio pendentes"""
        return self._events.copy()
    
    def clear_events(self) -> None:
        """Limpa eventos de domínio"""
        self._events.clear()


# Importar eventos de domínio (serão criados em seguida)
# from ..events.validator_registered import ValidatorRegistered
# from ..events.stake_increased import StakeIncreased
# from ..events.stake_decreased import StakeDecreased
# from ..events.validator_deactivated import ValidatorDeactivated
# from ..events.validator_activated import ValidatorActivated
# from ..events.rewards_added import RewardsAdded
