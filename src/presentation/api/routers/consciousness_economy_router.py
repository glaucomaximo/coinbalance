"""
Router para Economia da Consciência - Modelo Disruptivo CNB
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from decimal import Decimal

from src.domain.defi.services.impact_social_service import ImpactSocialService, ImpactCategory
from src.domain.defi.services.sustainable_defi_service import SustainableDeFiService, DeFiProductType
from src.domain.defi.services.governance_service import GovernanceService, ProposalType, VoteChoice
from src.domain.defi.entities.impact_project import ProjectStatus
from src.domain.defi.entities.sustainable_defi_product import SustainabilityRating
from src.domain.defi.entities.governance_proposal import ProposalStatus
from src.domain.shared.value_objects.wallet_address import WalletAddress
from src.domain.shared.value_objects.money import Money

router = APIRouter(prefix="/economia-consciencia", tags=["Economia da Consciência"])

# Dependencies
def get_impact_service() -> ImpactSocialService:
    """Dependency para o serviço de impacto social"""
    return ImpactSocialService()

def get_defi_service() -> SustainableDeFiService:
    """Dependency para o serviço DeFi sustentável"""
    return SustainableDeFiService()

def get_governance_service() -> GovernanceService:
    """Dependency para o serviço de governança"""
    return GovernanceService()

# Schemas
class ImpactProjectRequest(BaseModel):
    """Request para criar projeto de impacto"""
    project_id: str = Field(..., description="ID único do projeto")
    name: str = Field(..., min_length=1, max_length=200, description="Nome do projeto")
    description: str = Field(..., min_length=1, max_length=1000, description="Descrição do projeto")
    category: str = Field(..., description="Categoria de impacto")
    impact_description: str = Field(..., description="Descrição do impacto")
    expected_outcomes: List[str] = Field(..., description="Resultados esperados")
    target_beneficiaries: int = Field(..., gt=0, description="Número de beneficiários")
    funding_goal: Decimal = Field(..., gt=0, description="Meta de financiamento em CNB")
    proposer_address: str = Field(..., description="Endereço do proponente")

class DeFiProductRequest(BaseModel):
    """Request para criar produto DeFi sustentável"""
    product_id: str = Field(..., description="ID único do produto")
    name: str = Field(..., description="Nome do produto")
    description: str = Field(..., description="Descrição do produto")
    product_type: str = Field(..., description="Tipo do produto")
    apy_rate: Decimal = Field(..., gt=0, le=1, description="Taxa APY (0-100%)")
    minimum_stake: Decimal = Field(..., gt=0, description="Stake mínimo em CNB")
    maximum_stake: Decimal = Field(..., gt=0, description="Stake máximo em CNB")
    lock_period_days: int = Field(..., gt=0, description="Período de lock em dias")
    carbon_offset_per_cnb: Decimal = Field(..., ge=0, description="Compensação de carbono por CNB")
    environmental_impact_score: Decimal = Field(..., ge=0, le=100, description="Score de impacto ambiental")

class GovernanceProposalRequest(BaseModel):
    """Request para criar proposta de governança"""
    proposal_id: str = Field(..., description="ID único da proposta")
    title: str = Field(..., description="Título da proposta")
    description: str = Field(..., description="Descrição da proposta")
    proposal_type: str = Field(..., description="Tipo da proposta")
    detailed_description: str = Field(..., description="Descrição detalhada")
    implementation_plan: str = Field(..., description="Plano de implementação")
    expected_outcomes: List[str] = Field(..., description="Resultados esperados")
    risks_and_mitigations: str = Field(..., description="Riscos e mitigações")
    voting_duration_days: int = Field(..., gt=0, le=30, description="Duração da votação em dias")
    quorum_threshold: Decimal = Field(..., gt=0, le=100, description="Limiar de quorum (%)")
    approval_threshold: Decimal = Field(..., gt=0, le=100, description="Limiar de aprovação (%)")
    proposer_address: str = Field(..., description="Endereço do proponente")
    treasury_impact: Decimal = Field(default=0, description="Impacto no tesouro em CNB")

class VoteRequest(BaseModel):
    """Request para votar em proposta"""
    proposal_id: str = Field(..., description="ID da proposta")
    voter_address: str = Field(..., description="Endereço do votante")
    vote_choice: str = Field(..., description="Escolha do voto (yes/no/abstain)")
    voting_power: Decimal = Field(..., gt=0, description="Poder de voto baseado em CNB")

# ========== IMPACTO SOCIAL ESG ==========

@router.get(
    "/impacto/projetos",
    summary="Listar Projetos de Impacto",
    description="Lista todos os projetos de impacto social ESG"
)
async def list_impact_projects(
    category: Optional[str] = None,
    status: Optional[str] = None,
    impact_service: ImpactSocialService = Depends(get_impact_service)
):
    """Lista projetos de impacto social"""
    if category:
        try:
            impact_category = ImpactCategory(category)
            projects = impact_service.get_projects_by_category(impact_category)
        except ValueError:
            raise HTTPException(status_code=400, detail="Categoria inválida")
    else:
        projects = impact_service.get_active_projects() + impact_service.get_completed_projects()
    
    if status:
        try:
            project_status = ProjectStatus(status)
            projects = [p for p in projects if p.status == project_status]
        except ValueError:
            raise HTTPException(status_code=400, detail="Status inválido")
    
    return [project.to_dict() for project in projects]

@router.post(
    "/impacto/projetos",
    status_code=status.HTTP_201_CREATED,
    summary="Criar Projeto de Impacto",
    description="Cria um novo projeto de impacto social ESG"
)
async def create_impact_project(
    request: ImpactProjectRequest,
    impact_service: ImpactSocialService = Depends(get_impact_service)
):
    """Cria um novo projeto de impacto social"""
    try:
        category = ImpactCategory(request.category)
        proposer_address = WalletAddress(request.proposer_address)
        funding_goal = Money(request.funding_goal)
        
        project = impact_service.propose_project(
            project_id=request.project_id,
            name=request.name,
            description=request.description,
            category=category,
            impact_description=request.impact_description,
            expected_outcomes=request.expected_outcomes,
            target_beneficiaries=request.target_beneficiaries,
            funding_goal=funding_goal,
            proposer_address=proposer_address
        )
        
        return {
            "success": True,
            "message": "Projeto de impacto criado com sucesso",
            "project": project.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/impacto/estatisticas",
    summary="Estatísticas de Impacto",
    description="Retorna estatísticas globais de impacto social ESG"
)
async def get_impact_statistics(
    impact_service: ImpactSocialService = Depends(get_impact_service)
):
    """Retorna estatísticas de impacto social"""
    return impact_service.get_impact_statistics()

# ========== DEFI SUSTENTÁVEL ==========

@router.get(
    "/defi/produtos",
    summary="Listar Produtos DeFi Sustentáveis",
    description="Lista produtos DeFi com foco em sustentabilidade"
)
async def list_defi_products(
    product_type: Optional[str] = None,
    defi_service: SustainableDeFiService = Depends(get_defi_service)
):
    """Lista produtos DeFi sustentáveis"""
    if product_type:
        try:
            defi_type = DeFiProductType(product_type)
            products = defi_service.get_products_by_type(defi_type)
        except ValueError:
            raise HTTPException(status_code=400, detail="Tipo de produto inválido")
    else:
        products = defi_service.get_active_products()
    
    return [product.to_dict() for product in products]

@router.post(
    "/defi/produtos/staking-verde",
    status_code=status.HTTP_201_CREATED,
    summary="Criar Produto de Staking Verde",
    description="Cria um produto de staking com compensação de carbono"
)
async def create_green_staking_product(
    request: DeFiProductRequest,
    defi_service: SustainableDeFiService = Depends(get_defi_service)
):
    """Cria um produto de staking verde"""
    try:
        product = defi_service.create_green_staking_product(
            product_id=request.product_id,
            name=request.name,
            description=request.description,
            apy_rate=request.apy_rate,
            minimum_stake=Money(request.minimum_stake),
            maximum_stake=Money(request.maximum_stake),
            lock_period_days=request.lock_period_days,
            carbon_offset_per_cnb=request.carbon_offset_per_cnb,
            environmental_impact_score=request.environmental_impact_score
        )
        
        return {
            "success": True,
            "message": "Produto de staking verde criado com sucesso",
            "product": product.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/defi/ranking-sustentabilidade",
    summary="Ranking de Sustentabilidade",
    description="Retorna ranking de produtos por sustentabilidade"
)
async def get_sustainability_ranking(
    limit: int = 10,
    defi_service: SustainableDeFiService = Depends(get_defi_service)
):
    """Retorna ranking de produtos por sustentabilidade"""
    products = defi_service.get_top_sustainability_products(limit)
    return [product.to_dict() for product in products]

@router.get(
    "/defi/estatisticas",
    summary="Estatísticas DeFi Sustentável",
    description="Retorna estatísticas do DeFi sustentável"
)
async def get_defi_statistics(
    defi_service: SustainableDeFiService = Depends(get_defi_service)
):
    """Retorna estatísticas do DeFi sustentável"""
    return defi_service.get_defi_statistics()

# ========== GOVERNANÇA PARTICIPATIVA ==========

@router.get(
    "/governanca/propostas",
    summary="Listar Propostas de Governança",
    description="Lista propostas de governança participativa"
)
async def list_governance_proposals(
    status: Optional[str] = None,
    proposal_type: Optional[str] = None,
    governance_service: GovernanceService = Depends(get_governance_service)
):
    """Lista propostas de governança"""
    if status:
        try:
            proposal_status = ProposalStatus(status)
            proposals = governance_service.get_proposals_by_status(proposal_status)
        except ValueError:
            raise HTTPException(status_code=400, detail="Status inválido")
    elif proposal_type:
        try:
            prop_type = ProposalType(proposal_type)
            proposals = governance_service.get_proposals_by_type(prop_type)
        except ValueError:
            raise HTTPException(status_code=400, detail="Tipo de proposta inválido")
    else:
        proposals = governance_service.proposals
    
    return [proposal.to_dict() for proposal in proposals]

@router.post(
    "/governanca/propostas",
    status_code=status.HTTP_201_CREATED,
    summary="Criar Proposta de Governança",
    description="Cria uma nova proposta de governança participativa"
)
async def create_governance_proposal(
    request: GovernanceProposalRequest,
    governance_service: GovernanceService = Depends(get_governance_service)
):
    """Cria uma nova proposta de governança"""
    try:
        proposal_type = ProposalType(request.proposal_type)
        proposer_address = WalletAddress(request.proposer_address)
        treasury_impact = Money(request.treasury_impact)
        
        proposal = governance_service.create_proposal(
            proposal_id=request.proposal_id,
            title=request.title,
            description=request.description,
            proposal_type=proposal_type,
            detailed_description=request.detailed_description,
            implementation_plan=request.implementation_plan,
            expected_outcomes=request.expected_outcomes,
            risks_and_mitigations=request.risks_and_mitigations,
            voting_duration_days=request.voting_duration_days,
            quorum_threshold=request.quorum_threshold,
            approval_threshold=request.approval_threshold,
            proposer_address=proposer_address,
            treasury_impact=treasury_impact
        )
        
        return {
            "success": True,
            "message": "Proposta de governança criada com sucesso",
            "proposal": proposal.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post(
    "/governanca/votar",
    summary="Votar em Proposta",
    description="Vota em uma proposta de governança"
)
async def vote_on_proposal(
    request: VoteRequest,
    governance_service: GovernanceService = Depends(get_governance_service)
):
    """Vota em uma proposta de governança"""
    try:
        voter_address = WalletAddress(request.voter_address)
        vote_choice = VoteChoice(request.vote_choice)
        
        success = governance_service.vote_on_proposal(
            proposal_id=request.proposal_id,
            voter_address=voter_address,
            vote_choice=vote_choice,
            voting_power=request.voting_power
        )
        
        if success:
            return {
                "success": True,
                "message": "Voto registrado com sucesso"
            }
        else:
            raise HTTPException(status_code=400, detail="Falha ao registrar voto")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/governanca/estatisticas",
    summary="Estatísticas de Governança",
    description="Retorna estatísticas de governança participativa"
)
async def get_governance_statistics(
    governance_service: GovernanceService = Depends(get_governance_service)
):
    """Retorna estatísticas de governança"""
    return governance_service.get_proposal_statistics()

@router.get(
    "/governanca/tesouro",
    summary="Saldo do Tesouro",
    description="Retorna saldo atual do tesouro comunitário"
)
async def get_treasury_balance(
    governance_service: GovernanceService = Depends(get_governance_service)
):
    """Retorna saldo do tesouro"""
    balance = governance_service.get_treasury_balance()
    return {
        "treasury_balance_cnb": float(balance.to_cnb()),
        "treasury_balance_satoshi": balance.to_satoshi()
    }

# ========== DASHBOARD ECONÔMIA DA CONSCIÊNCIA ==========

@router.get(
    "/dashboard",
    summary="Dashboard Economia da Consciência",
    description="Retorna visão geral da economia da consciência CNB"
)
async def get_consciousness_economy_dashboard(
    impact_service: ImpactSocialService = Depends(get_impact_service),
    defi_service: SustainableDeFiService = Depends(get_defi_service),
    governance_service: GovernanceService = Depends(get_governance_service)
):
    """Dashboard completo da economia da consciência"""
    impact_stats = impact_service.get_impact_statistics()
    defi_stats = defi_service.get_defi_statistics()
    governance_stats = governance_service.get_proposal_statistics()
    
    # Calcular score geral de consciência
    consciousness_score = (
        impact_stats.get("average_impact_score", 0) * 0.4 +
        defi_stats.get("average_weighted_apy", 0) * 0.3 +
        governance_stats.get("community_engagement_score", 0) * 0.3
    )
    
    return {
        "consciousness_economy_score": consciousness_score,
        "impact_social": impact_stats,
        "defi_sustentavel": defi_stats,
        "governanca_participativa": governance_stats,
        "total_carbon_offset_kg": impact_stats.get("total_carbon_offset_kg", 0) + defi_stats.get("total_carbon_offset_kg", 0),
        "total_lives_impacted": impact_stats.get("total_lives_impacted", 0),
        "total_volume_sustentavel_cnb": defi_stats.get("total_volume_staked_cnb", 0),
        "treasury_balance_cnb": governance_stats.get("treasury_balance_cnb", 0)
    }
