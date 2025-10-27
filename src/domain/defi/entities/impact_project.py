"""
Entidade ImpactProject - Projetos de Impacto Social ESG
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from decimal import Decimal
from enum import Enum

from ...shared.value_objects.money import Money
from ...shared.value_objects.timestamp import Timestamp
from ...shared.value_objects.wallet_address import WalletAddress
from ...shared.domain_events.base import DomainEvent


class ImpactCategory(Enum):
    """Categorias de impacto social"""
    ENVIRONMENTAL = "environmental"  # Ambiental
    SOCIAL = "social"               # Social
    GOVERNANCE = "governance"       # Governança
    EDUCATION = "education"          # Educação
    HEALTHCARE = "healthcare"       # Saúde
    SUSTAINABILITY = "sustainability"  # Sustentabilidade


class ProjectStatus(Enum):
    """Status do projeto"""
    PROPOSED = "proposed"           # Proposto
    APPROVED = "approved"           # Aprovado
    FUNDED = "funded"               # Financiado
    IN_PROGRESS = "in_progress"     # Em andamento
    COMPLETED = "completed"         # Concluído
    CANCELLED = "cancelled"         # Cancelado


@dataclass
class ImpactProject:
    """
    Entidade ImpactProject - Aggregate Root.
    
    Representa um projeto de impacto social que pode ser financiado
    através da economia da consciência CNB.
    
    Características Disruptivas:
    - Financiamento através de CNB
    - Transparência total via blockchain
    - Governança participativa
    - Impacto mensurável e verificável
    - Recompensas para financiadores
    """
    
    # Identity
    project_id: str
    name: str
    description: str
    
    # Impact Details
    category: ImpactCategory
    impact_description: str
    expected_outcomes: List[str]
    target_beneficiaries: int
    
    # Financial
    funding_goal: Money
    proposer_address: WalletAddress
    current_funding: Money = Money(Decimal("0"))
    minimum_contribution: Money = Money(Decimal("1"))  # 1 CNB mínimo
    
    # Timeline
    start_date: Optional[Timestamp] = None
    end_date: Optional[Timestamp] = None
    estimated_duration_days: int = 90
    
    # Status
    status: ProjectStatus = ProjectStatus.PROPOSED
    approval_votes: int = 0
    rejection_votes: int = 0
    
    # Governance
    approvers: List[WalletAddress] = field(default_factory=list)
    contributors: Dict[str, Money] = field(default_factory=dict)  # address -> amount
    
    # Impact Metrics
    impact_score: Decimal = Decimal("0")  # 0-100
    carbon_offset_kg: Decimal = Decimal("0")
    lives_impacted: int = 0
    
    # Domain Events
    _events: List[DomainEvent] = field(default_factory=list, init=False, repr=False)
    
    def __post_init__(self):
        """Validação após inicialização"""
        self._validate()
    
    def _validate(self):
        """Valida invariantes do domínio"""
        if self.funding_goal.to_cnb() <= 0:
            raise ValueError("Funding goal must be positive")
        if self.minimum_contribution.to_cnb() <= 0:
            raise ValueError("Minimum contribution must be positive")
        if self.target_beneficiaries <= 0:
            raise ValueError("Target beneficiaries must be positive")
    
    @classmethod
    def create_project(
        cls,
        project_id: str,
        name: str,
        description: str,
        category: ImpactCategory,
        impact_description: str,
        expected_outcomes: List[str],
        target_beneficiaries: int,
        funding_goal: Money,
        proposer_address: WalletAddress,
        estimated_duration_days: int = 90
    ) -> "ImpactProject":
        """Factory method para criar um novo projeto de impacto"""
        project = cls(
            project_id=project_id,
            name=name,
            description=description,
            category=category,
            impact_description=impact_description,
            expected_outcomes=expected_outcomes,
            target_beneficiaries=target_beneficiaries,
            funding_goal=funding_goal,
            proposer_address=proposer_address,
            estimated_duration_days=estimated_duration_days
        )
        
        # TODO: Dispatch ProjectCreatedEvent
        return project
    
    def approve_project(self, approver_address: WalletAddress) -> None:
        """Aprova o projeto para financiamento"""
        if self.status != ProjectStatus.PROPOSED:
            raise ValueError("Only proposed projects can be approved")
        
        if approver_address in self.approvers:
            raise ValueError("Approver has already voted")
        
        self.approvers.append(approver_address)
        self.approval_votes += 1
        
        # Se atingir 5 aprovações, aprovar o projeto
        if self.approval_votes >= 5:
            self.status = ProjectStatus.APPROVED
            # TODO: Dispatch ProjectApprovedEvent
    
    def contribute(self, contributor_address: WalletAddress, amount: Money) -> None:
        """Contribui para o financiamento do projeto"""
        if self.status not in [ProjectStatus.APPROVED, ProjectStatus.FUNDED]:
            raise ValueError("Project must be approved to receive contributions")
        
        if amount.to_cnb() < self.minimum_contribution.to_cnb():
            raise ValueError(f"Contribution must be at least {self.minimum_contribution.to_cnb()} CNB")
        
        # Adicionar contribuição
        if str(contributor_address) in self.contributors:
            self.contributors[str(contributor_address)] += amount
        else:
            self.contributors[str(contributor_address)] = amount
        
        self.current_funding += amount
        
        # Verificar se atingiu a meta
        if self.current_funding >= self.funding_goal:
            self.status = ProjectStatus.FUNDED
            # TODO: Dispatch ProjectFundedEvent
    
    def start_project(self) -> None:
        """Inicia a execução do projeto"""
        if self.status != ProjectStatus.FUNDED:
            raise ValueError("Project must be funded to start")
        
        self.status = ProjectStatus.IN_PROGRESS
        self.start_date = Timestamp.now()
        # TODO: Dispatch ProjectStartedEvent
    
    def complete_project(self, impact_score: Decimal, carbon_offset_kg: Decimal, lives_impacted: int) -> None:
        """Marca o projeto como concluído com métricas de impacto"""
        if self.status != ProjectStatus.IN_PROGRESS:
            raise ValueError("Project must be in progress to complete")
        
        self.status = ProjectStatus.COMPLETED
        self.end_date = Timestamp.now()
        self.impact_score = impact_score
        self.carbon_offset_kg = carbon_offset_kg
        self.lives_impacted = lives_impacted
        
        # TODO: Dispatch ProjectCompletedEvent
    
    def calculate_impact_multiplier(self) -> Decimal:
        """Calcula o multiplicador de impacto baseado na categoria e score"""
        base_multiplier = Decimal("1.0")
        
        # Multiplicadores por categoria
        category_multipliers = {
            ImpactCategory.ENVIRONMENTAL: Decimal("1.5"),
            ImpactCategory.SOCIAL: Decimal("1.3"),
            ImpactCategory.GOVERNANCE: Decimal("1.2"),
            ImpactCategory.EDUCATION: Decimal("1.4"),
            ImpactCategory.HEALTHCARE: Decimal("1.6"),
            ImpactCategory.SUSTAINABILITY: Decimal("1.7")
        }
        
        category_multiplier = category_multipliers.get(self.category, Decimal("1.0"))
        impact_multiplier = Decimal(self.impact_score) / Decimal("100")
        
        return base_multiplier * category_multiplier * impact_multiplier
    
    def calculate_contributor_rewards(self) -> Dict[str, Money]:
        """Calcula recompensas para contribuidores baseadas no impacto"""
        if self.status != ProjectStatus.COMPLETED:
            return {}
        
        impact_multiplier = self.calculate_impact_multiplier()
        total_rewards = self.current_funding * impact_multiplier
        total_contributions = sum(self.contributors.values())
        
        rewards = {}
        for contributor, contribution in self.contributors.items():
            contribution_ratio = contribution / total_contributions
            reward = total_rewards * contribution_ratio
            rewards[contributor] = reward
        
        return rewards
    
    def get_funding_progress(self) -> Decimal:
        """Retorna o progresso do financiamento (0-100)"""
        if self.funding_goal.to_cnb() == 0:
            return Decimal("0")
        
        progress = (self.current_funding.to_cnb() / self.funding_goal.to_cnb()) * Decimal("100")
        return min(progress, Decimal("100"))
    
    def is_fundable(self) -> bool:
        """Verifica se o projeto pode receber financiamento"""
        return self.status in [ProjectStatus.APPROVED, ProjectStatus.FUNDED]
    
    def get_events(self) -> List[DomainEvent]:
        """Retorna eventos de domínio"""
        return self._events.copy()
    
    def clear_events(self) -> None:
        """Limpa eventos de domínio"""
        self._events.clear()
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "impact_description": self.impact_description,
            "expected_outcomes": self.expected_outcomes,
            "target_beneficiaries": self.target_beneficiaries,
            "funding_goal": float(self.funding_goal.to_cnb()),
            "current_funding": float(self.current_funding.to_cnb()),
            "minimum_contribution": float(self.minimum_contribution.to_cnb()),
            "status": self.status.value,
            "approval_votes": self.approval_votes,
            "rejection_votes": self.rejection_votes,
            "proposer_address": str(self.proposer_address),
            "contributors_count": len(self.contributors),
            "impact_score": float(self.impact_score),
            "carbon_offset_kg": float(self.carbon_offset_kg),
            "lives_impacted": self.lives_impacted,
            "funding_progress": float(self.get_funding_progress())
        }
