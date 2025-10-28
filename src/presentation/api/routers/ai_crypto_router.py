"""
API Router para Criação de Criptomoedas com IA
"""

import logging
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from decimal import Decimal

from src.infrastructure.security.auth_manager import (
    auth_manager, UserRole, Permission, get_auth_manager
)
from src.infrastructure.security.auth import (
    get_current_user, AuthenticatedUser, require_scope
)
from src.domain.ai_crypto_creation.entities.crypto_intelligence import (
    crypto_intelligence, CryptoPurpose, EconomicModel, ConsensusType
)
from src.domain.ai_crypto_creation.services.autonomous_economy import (
    autonomous_economy, DecisionType, EconomicPhase
)
from src.domain.ai_crypto_creation.services.token_factory import (
    ai_token_factory, TokenCategory, TokenStandard
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai-crypto", tags=["AI Crypto Creation"])

# ========== SCHEMAS ==========

class CreateCryptoRequest(BaseModel):
    """Requisição para criação de criptomoeda"""
    purpose: str = Field(..., description="Propósito da criptomoeda")
    target_market: str = Field(..., description="Mercado alvo")
    custom_requirements: Optional[Dict[str, Any]] = Field(None, description="Requisitos customizados")

class CryptoSpecificationResponse(BaseModel):
    """Resposta com especificação de criptomoeda"""
    crypto_id: str
    name: str
    symbol: str
    purpose: str
    description: str
    consensus_type: str
    tokenomics: Dict[str, Any]
    features: List[str]
    target_market: str
    use_cases: List[str]
    ai_reasoning: str
    created_at: float

class MarketAnalysisRequest(BaseModel):
    """Requisição para análise de mercado"""
    purpose: str
    target_market: str

class MarketAnalysisResponse(BaseModel):
    """Resposta com análise de mercado"""
    market_demand: float
    competition_level: float
    innovation_potential: float
    adoption_probability: float
    economic_viability: float
    recommended_action: str
    confidence_score: float

class EconomicDecisionResponse(BaseModel):
    """Resposta com decisão econômica"""
    decision_id: str
    decision_type: str
    reasoning: str
    expected_outcome: str
    confidence: float
    impact_assessment: Dict[str, float]
    execution_plan: List[str]
    created_at: float

class EcosystemHealthResponse(BaseModel):
    """Resposta com saúde do ecossistema"""
    overall_score: float
    liquidity_score: float
    adoption_score: float
    innovation_score: float
    stability_score: float
    growth_potential: float
    risk_level: str
    recommendations: List[str]

class TokenGenerationRequest(BaseModel):
    """Requisição para geração de token"""
    purpose: str
    target_audience: str
    requirements: Optional[Dict[str, Any]] = None
    constraints: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None

class TokenTemplateResponse(BaseModel):
    """Resposta com template de token"""
    template_id: str
    name: str
    symbol: str
    category: str
    standard: str
    description: str
    features: List[str]
    use_cases: List[str]
    tokenomics: Dict[str, Any]
    smart_contract_code: str
    deployment_instructions: List[str]
    confidence_score: float
    created_at: float

# ========== ENDPOINTS ==========

@router.post("/create", response_model=CryptoSpecificationResponse)
async def create_cryptocurrency(
    request: CreateCryptoRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Cria uma nova criptomoeda usando IA.
    
    Args:
        request: Dados para criação da criptomoeda
        current_user: Usuário autenticado
        
    Returns:
        Especificação da nova criptomoeda
    """
    try:
        logger.info(f"Criando criptomoeda: {request.purpose} para {request.target_market}")
        
        # Converter string para enum
        try:
            purpose_enum = CryptoPurpose(request.purpose.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Propósito inválido: {request.purpose}"
            )
        
        # Criar criptomoeda
        specification = crypto_intelligence.create_new_cryptocurrency(
            purpose=purpose_enum,
            target_market=request.target_market,
            custom_requirements=request.custom_requirements
        )
        
        return CryptoSpecificationResponse(
            crypto_id=specification.crypto_id,
            name=specification.name,
            symbol=specification.symbol,
            purpose=specification.purpose.value,
            description=specification.description,
            consensus_type=specification.consensus_type.value,
            tokenomics={
                "total_supply": str(specification.tokenomics.total_supply),
                "inflation_rate": str(specification.tokenomics.inflation_rate),
                "economic_model": specification.tokenomics.economic_model.value,
                "staking_reward_rate": str(specification.tokenomics.staking_reward_rate)
            },
            features=specification.features,
            target_market=specification.target_market,
            use_cases=specification.use_cases,
            ai_reasoning=specification.ai_reasoning,
            created_at=specification.created_at
        )
        
    except Exception as e:
        logger.error(f"Erro ao criar criptomoeda: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/analyze-market", response_model=MarketAnalysisResponse)
async def analyze_market_opportunity(
    request: MarketAnalysisRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Analisa oportunidade de mercado para nova criptomoeda.
    
    Args:
        request: Dados para análise de mercado
        current_user: Usuário autenticado
        
    Returns:
        Análise de mercado
    """
    try:
        logger.info(f"Analisando mercado: {request.purpose} em {request.target_market}")
        
        # Converter string para enum
        try:
            purpose_enum = CryptoPurpose(request.purpose.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Propósito inválido: {request.purpose}"
            )
        
        # Analisar mercado
        analysis = crypto_intelligence.analyze_market_opportunity(
            purpose=purpose_enum,
            target_market=request.target_market
        )
        
        return MarketAnalysisResponse(
            market_demand=analysis.market_demand,
            competition_level=analysis.competition_level,
            innovation_potential=analysis.innovation_potential,
            adoption_probability=analysis.adoption_probability,
            economic_viability=analysis.economic_viability,
            recommended_action=analysis.recommended_action,
            confidence_score=analysis.confidence_score
        )
        
    except Exception as e:
        logger.error(f"Erro ao analisar mercado: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/created-cryptos")
async def get_created_cryptocurrencies(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna lista de criptomoedas criadas pela IA.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        Lista de criptomoedas criadas
    """
    try:
        logger.info("Listando criptomoedas criadas")
        
        cryptos = crypto_intelligence.get_created_cryptos()
        
        return {
            "cryptocurrencies": [
                {
                    "crypto_id": crypto.crypto_id,
                    "name": crypto.name,
                    "symbol": crypto.symbol,
                    "purpose": crypto.purpose.value,
                    "target_market": crypto.target_market,
                    "created_at": crypto.created_at
                }
                for crypto in cryptos
            ],
            "total": len(cryptos)
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar criptomoedas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/ai-decisions")
async def get_ai_decisions(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna histórico de decisões da IA.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        Histórico de decisões
    """
    try:
        logger.info("Listando decisões da IA")
        
        decisions = crypto_intelligence.get_ai_decisions()
        
        return {
            "decisions": decisions,
            "total": len(decisions)
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar decisões: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# ========== ECONOMIA AUTÔNOMA ==========

@router.get("/ecosystem-health", response_model=EcosystemHealthResponse)
async def get_ecosystem_health(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna saúde atual do ecossistema econômico.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        Saúde do ecossistema
    """
    try:
        logger.info("Verificando saúde do ecossistema")
        
        health = autonomous_economy.monitor_ecosystem_health()
        
        return EcosystemHealthResponse(
            overall_score=health.overall_score,
            liquidity_score=health.liquidity_score,
            adoption_score=health.adoption_score,
            innovation_score=health.innovation_score,
            stability_score=health.stability_score,
            growth_potential=health.growth_potential,
            risk_level=health.risk_level,
            recommendations=health.recommendations
        )
        
    except Exception as e:
        logger.error(f"Erro ao verificar saúde do ecossistema: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/make-decision", response_model=EconomicDecisionResponse)
async def make_autonomous_decision(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Toma decisão econômica autônoma.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        Decisão econômica
    """
    try:
        logger.info("Tomando decisão econômica autônoma")
        
        decision = autonomous_economy.make_autonomous_decision()
        
        if not decision:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="Nenhuma decisão necessária no momento"
            )
        
        return EconomicDecisionResponse(
            decision_id=decision.decision_id,
            decision_type=decision.decision_type.value,
            reasoning=decision.reasoning,
            expected_outcome=decision.expected_outcome,
            confidence=decision.confidence,
            impact_assessment=decision.impact_assessment,
            execution_plan=decision.execution_plan,
            created_at=decision.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao tomar decisão: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/execute-decision/{decision_id}")
async def execute_decision(
    decision_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Executa decisão econômica.
    
    Args:
        decision_id: ID da decisão
        current_user: Usuário autenticado
        
    Returns:
        Resultado da execução
    """
    try:
        logger.info(f"Executando decisão: {decision_id}")
        
        # Buscar decisão (simulação - em produção seria busca real)
        decisions = autonomous_economy.decisions_history
        decision = next((d for d in decisions if d.decision_id == decision_id), None)
        
        if not decision:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Decisão não encontrada"
            )
        
        # Executar decisão
        result = autonomous_economy.execute_decision(decision)
        
        return {
            "decision_id": decision_id,
            "status": "executed",
            "result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao executar decisão: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/ecosystem-status")
async def get_ecosystem_status(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna status atual do ecossistema.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        Status do ecossistema
    """
    try:
        logger.info("Obtendo status do ecossistema")
        
        status = autonomous_economy.get_ecosystem_status()
        
        return status
        
    except Exception as e:
        logger.error(f"Erro ao obter status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# ========== FÁBRICA DE TOKENS ==========

@router.post("/generate-token", response_model=TokenTemplateResponse)
async def generate_token(
    request: TokenGenerationRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Gera token personalizado usando IA.
    
    Args:
        request: Dados para geração do token
        current_user: Usuário autenticado
        
    Returns:
        Template do token gerado
    """
    try:
        logger.info(f"Gerando token: {request.purpose} para {request.target_audience}")
        
        # Criar requisição de geração
        generation_request = ai_token_factory.create_generation_request(
            purpose=request.purpose,
            target_audience=request.target_audience,
            requirements=request.requirements,
            constraints=request.constraints,
            preferences=request.preferences
        )
        
        # Gerar token
        template = ai_token_factory.generate_token(generation_request)
        
        return TokenTemplateResponse(
            template_id=template.template_id,
            name=template.name,
            symbol=template.symbol,
            category=template.category.value,
            standard=template.standard.value,
            description=template.description,
            features=template.features,
            use_cases=template.use_cases,
            tokenomics=template.tokenomics,
            smart_contract_code=template.smart_contract_code,
            deployment_instructions=template.deployment_instructions,
            confidence_score=template.confidence_score,
            created_at=template.created_at
        )
        
    except Exception as e:
        logger.error(f"Erro ao gerar token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/token-templates")
async def get_token_templates(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna lista de templates de tokens gerados.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        Lista de templates
    """
    try:
        logger.info("Listando templates de tokens")
        
        templates = ai_token_factory.list_token_templates()
        
        return {
            "templates": [
                {
                    "template_id": template.template_id,
                    "name": template.name,
                    "symbol": template.symbol,
                    "category": template.category.value,
                    "standard": template.standard.value,
                    "confidence_score": template.confidence_score,
                    "created_at": template.created_at
                }
                for template in templates
            ],
            "total": len(templates)
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/token-template/{template_id}")
async def get_token_template(
    template_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna template específico de token.
    
    Args:
        template_id: ID do template
        current_user: Usuário autenticado
        
    Returns:
        Template do token
    """
    try:
        logger.info(f"Obtendo template: {template_id}")
        
        template = ai_token_factory.get_token_template(template_id)
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template não encontrado"
            )
        
        return TokenTemplateResponse(
            template_id=template.template_id,
            name=template.name,
            symbol=template.symbol,
            category=template.category.value,
            standard=template.standard.value,
            description=template.description,
            features=template.features,
            use_cases=template.use_cases,
            tokenomics=template.tokenomics,
            smart_contract_code=template.smart_contract_code,
            deployment_instructions=template.deployment_instructions,
            confidence_score=template.confidence_score,
            created_at=template.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
