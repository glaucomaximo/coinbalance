"""
Serviço de Impacto Social ESG - Economia da Consciência
"""

from decimal import Decimal
from typing import List, Dict, Optional
from dataclasses import dataclass

from ..entities.impact_project import ImpactProject, ImpactCategory, ProjectStatus
from ...shared.value_objects.money import Money
from ...shared.value_objects.wallet_address import WalletAddress


@dataclass(frozen=True)
class ImpactMetrics:
    """
    Métricas de impacto social ESG.
    
    Características Disruptivas:
    - Mensuração quantificável de impacto
    - Transparência total via blockchain
    - Incentivos alinhados com propósito
    - Recompensas baseadas em impacto real
    """
    
    # Environmental Impact
    carbon_offset_kg: Decimal
    renewable_energy_mwh: Decimal
    trees_planted: int
    waste_reduced_kg: Decimal
    
    # Social Impact
    lives_impacted: int
    jobs_created: int
    education_hours: Decimal
    healthcare_access: int
    
    # Governance Impact
    transparency_score: Decimal  # 0-100
    community_participation: int
    democratic_decisions: int
    
    # Economic Impact
    local_economy_boost: Money
    financial_inclusion: int
    microfinance_loans: int
    
    @classmethod
    def calculate_total_impact_score(cls, metrics: "ImpactMetrics") -> Decimal:
        """Calcula score total de impacto (0-1000)"""
        environmental_score = (
            metrics.carbon_offset_kg * Decimal("0.1") +
            metrics.renewable_energy_mwh * Decimal("5") +
            metrics.trees_planted * Decimal("0.5") +
            metrics.waste_reduced_kg * Decimal("0.01")
        )
        
        social_score = (
            metrics.lives_impacted * Decimal("2") +
            metrics.jobs_created * Decimal("10") +
            metrics.education_hours * Decimal("0.1") +
            metrics.healthcare_access * Decimal("5")
        )
        
        governance_score = (
            metrics.transparency_score * Decimal("2") +
            metrics.community_participation * Decimal("0.5") +
            metrics.democratic_decisions * Decimal("1")
        )
        
        economic_score = (
            metrics.local_economy_boost.to_cnb() * Decimal("0.01") +
            metrics.financial_inclusion * Decimal("3") +
            metrics.microfinance_loans * Decimal("2")
        )
        
        total_score = environmental_score + social_score + governance_score + economic_score
        return min(total_score, Decimal("1000"))  # Cap at 1000


class ImpactSocialService:
    """
    Serviço de Impacto Social ESG.
    
    Responsabilidades:
    - Gerenciar projetos de impacto
    - Calcular métricas ESG
    - Distribuir recompensas baseadas em impacto
    - Facilitar governança participativa
    """
    
    def __init__(self):
        self.active_projects: List[ImpactProject] = []
        self.completed_projects: List[ImpactProject] = []
        self.total_impact_metrics = ImpactMetrics(
            carbon_offset_kg=Decimal("0"),
            renewable_energy_mwh=Decimal("0"),
            trees_planted=0,
            waste_reduced_kg=Decimal("0"),
            lives_impacted=0,
            jobs_created=0,
            education_hours=Decimal("0"),
            healthcare_access=0,
            transparency_score=Decimal("100"),  # Blockchain = transparência máxima
            community_participation=0,
            democratic_decisions=0,
            local_economy_boost=Money(Decimal("0")),
            financial_inclusion=0,
            microfinance_loans=0
        )
    
    def propose_project(
        self,
        project_id: str,
        name: str,
        description: str,
        category: ImpactCategory,
        impact_description: str,
        expected_outcomes: List[str],
        target_beneficiaries: int,
        funding_goal: Money,
        proposer_address: WalletAddress
    ) -> ImpactProject:
        """Propoe um novo projeto de impacto social"""
        project = ImpactProject.create_project(
            project_id=project_id,
            name=name,
            description=description,
            category=category,
            impact_description=impact_description,
            expected_outcomes=expected_outcomes,
            target_beneficiaries=target_beneficiaries,
            funding_goal=funding_goal,
            proposer_address=proposer_address
        )
        
        self.active_projects.append(project)
        return project
    
    def approve_project(self, project_id: str, approver_address: WalletAddress) -> bool:
        """Aprova um projeto para financiamento"""
        project = self._find_project_by_id(project_id)
        if not project:
            return False
        
        try:
            project.approve_project(approver_address)
            return True
        except ValueError:
            return False
    
    def contribute_to_project(
        self,
        project_id: str,
        contributor_address: WalletAddress,
        amount: Money
    ) -> bool:
        """Contribui para um projeto de impacto"""
        project = self._find_project_by_id(project_id)
        if not project:
            return False
        
        try:
            project.contribute(contributor_address, amount)
            return True
        except ValueError:
            return False
    
    def complete_project(
        self,
        project_id: str,
        impact_score: Decimal,
        carbon_offset_kg: Decimal,
        lives_impacted: int,
        additional_metrics: Optional[Dict] = None
    ) -> bool:
        """Marca um projeto como concluído com métricas de impacto"""
        project = self._find_project_by_id(project_id)
        if not project:
            return False
        
        try:
            project.complete_project(impact_score, carbon_offset_kg, lives_impacted)
            
            # Mover para projetos concluídos
            self.active_projects.remove(project)
            self.completed_projects.append(project)
            
            # Atualizar métricas globais
            self._update_global_metrics(project, additional_metrics)
            
            return True
        except ValueError:
            return False
    
    def get_project_by_id(self, project_id: str) -> Optional[ImpactProject]:
        """Busca um projeto por ID"""
        return self._find_project_by_id(project_id)
    
    def get_active_projects(self) -> List[ImpactProject]:
        """Retorna projetos ativos"""
        return self.active_projects.copy()
    
    def get_completed_projects(self) -> List[ImpactProject]:
        """Retorna projetos concluídos"""
        return self.completed_projects.copy()
    
    def get_projects_by_category(self, category: ImpactCategory) -> List[ImpactProject]:
        """Retorna projetos por categoria"""
        all_projects = self.active_projects + self.completed_projects
        return [p for p in all_projects if p.category == category]
    
    def get_impact_statistics(self) -> Dict[str, float]:
        """Retorna estatísticas de impacto"""
        total_projects = len(self.active_projects) + len(self.completed_projects)
        completed_projects = len(self.completed_projects)
        total_funding = sum(p.current_funding.to_cnb() for p in self.active_projects + self.completed_projects)
        total_lives_impacted = sum(p.lives_impacted for p in self.completed_projects)
        total_carbon_offset = sum(p.carbon_offset_kg for p in self.completed_projects)
        
        return {
            "total_projects": total_projects,
            "completed_projects": completed_projects,
            "active_projects": len(self.active_projects),
            "total_funding_cnb": float(total_funding),
            "total_lives_impacted": total_lives_impacted,
            "total_carbon_offset_kg": float(total_carbon_offset),
            "average_impact_score": float(sum(p.impact_score for p in self.completed_projects) / max(completed_projects, 1)),
            "projects_by_category": {
                category.value: len(self.get_projects_by_category(category))
                for category in ImpactCategory
            }
        }
    
    def calculate_impact_rewards(self, project_id: str) -> Dict[str, float]:
        """Calcula recompensas baseadas em impacto para um projeto"""
        project = self._find_project_by_id(project_id)
        if not project or project.status != ProjectStatus.COMPLETED:
            return {}
        
        rewards = project.calculate_contributor_rewards()
        return {
            contributor: float(reward.to_cnb())
            for contributor, reward in rewards.items()
        }
    
    def get_global_impact_score(self) -> Decimal:
        """Calcula score global de impacto da plataforma"""
        return ImpactMetrics.calculate_total_impact_score(self.total_impact_metrics)
    
    def _find_project_by_id(self, project_id: str) -> Optional[ImpactProject]:
        """Busca projeto por ID em projetos ativos e concluídos"""
        for project in self.active_projects + self.completed_projects:
            if project.project_id == project_id:
                return project
        return None
    
    def _update_global_metrics(self, project: ImpactProject, additional_metrics: Optional[Dict] = None):
        """Atualiza métricas globais com dados do projeto concluído"""
        # Atualizar métricas básicas
        self.total_impact_metrics = ImpactMetrics(
            carbon_offset_kg=self.total_impact_metrics.carbon_offset_kg + project.carbon_offset_kg,
            renewable_energy_mwh=self.total_impact_metrics.renewable_energy_mwh,
            trees_planted=self.total_impact_metrics.trees_planted,
            waste_reduced_kg=self.total_impact_metrics.waste_reduced_kg,
            lives_impacted=self.total_impact_metrics.lives_impacted + project.lives_impacted,
            jobs_created=self.total_impact_metrics.jobs_created,
            education_hours=self.total_impact_metrics.education_hours,
            healthcare_access=self.total_impact_metrics.healthcare_access,
            transparency_score=self.total_impact_metrics.transparency_score,
            community_participation=self.total_impact_metrics.community_participation + 1,  # +1 projeto
            democratic_decisions=self.total_impact_metrics.democratic_decisions + project.approval_votes,
            local_economy_boost=self.total_impact_metrics.local_economy_boost + project.current_funding,
            financial_inclusion=self.total_impact_metrics.financial_inclusion + len(project.contributors),
            microfinance_loans=self.total_impact_metrics.microfinance_loans
        )
        
        # Atualizar métricas adicionais se fornecidas
        if additional_metrics:
            # TODO: Implementar atualização de métricas específicas por categoria
            pass
