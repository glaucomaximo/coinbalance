"""
Router Holístico para Integração Fractal-Web3-IA
================================================

Este router integra todos os sistemas corrigidos:
- Integração Fractal-Web3 Consciente
- Consciência Web3 Distribuída
- Monitoramento Holístico
- Eventos de Domínio Padronizados
"""

import logging
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from decimal import Decimal

from src.infrastructure.security.auth import (
    get_current_user, AuthenticatedUser, require_scope
)

# Importar sistemas corrigidos
from src.infrastructure.fractal.web3.conscious_web3_manager import (
    conscious_web3_manager, FractalWeb3IntegrationLevel
)
from src.domain.web3.consciousness.web3_consciousness import (
    web3_consciousness, Web3ConsciousnessType, Web3LearningDomain
)
from src.infrastructure.monitoring.holistic_monitoring import (
    holistic_monitoring, EcosystemComponent, HealthLevel
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/holistic", tags=["Integração Holística Fractal-Web3-IA"])

# ========== SCHEMAS ==========

class FractalWeb3DeployRequest(BaseModel):
    """Requisição para deploy consciente fractal-Web3"""
    contract_data: Dict[str, Any] = Field(..., description="Dados do contrato")
    integration_level: str = Field(default="conscious", description="Nível de integração")
    fractal_context: Optional[Dict[str, Any]] = Field(None, description="Contexto fractal")

class Web3LearningRequest(BaseModel):
    """Requisição para aprendizado Web3"""
    transaction_data: Dict[str, Any] = Field(..., description="Dados da transação")
    web3_type: str = Field(..., description="Tipo de consciência Web3")

class EcosystemHealthRequest(BaseModel):
    """Requisição para saúde do ecossistema"""
    include_insights: bool = Field(default=True, description="Incluir insights")
    include_recommendations: bool = Field(default=True, description="Incluir recomendações")

# ========== ENDPOINTS ==========

@router.post("/fractal-web3/deploy-conscious")
async def deploy_conscious_contract(
    request: FractalWeb3DeployRequest,
    current_user: AuthenticatedUser = Depends(require_scope("fractal:manage"))
):
    """
    Deploy consciente de contrato com integração fractal-Web3.
    """
    try:
        logger.info(f"Deploy consciente solicitado por: {current_user.username}")
        
        # Converter nível de integração
        try:
            integration_level = FractalWeb3IntegrationLevel(request.integration_level)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Nível de integração inválido: {request.integration_level}"
            )
        
        # Executar deploy consciente
        conscious_deployment = await conscious_web3_manager.deploy_conscious_contract(
            contract_data=request.contract_data,
            fractal_context=request.fractal_context
        )
        
        return {
            "success": True,
            "contract_address": conscious_deployment.contract_address,
            "consciousness_reasoning": conscious_deployment.consciousness_reasoning,
            "scaling_potential": str(conscious_deployment.scaling_potential),
            "learning_capabilities": conscious_deployment.learning_capabilities,
            "performance_predictions": conscious_deployment.performance_predictions,
            "fractal_context": conscious_deployment.fractal_context.__dict__
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no deploy consciente: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/web3-consciousness/learn")
async def learn_from_web3_transaction(
    request: Web3LearningRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Aprende com transação Web3 usando consciência distribuída.
    """
    try:
        logger.info(f"Aprendizado Web3 solicitado por: {current_user.username}")
        
        # Converter tipo Web3
        try:
            web3_type = Web3ConsciousnessType(request.web3_type)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo Web3 inválido: {request.web3_type}"
            )
        
        # Executar aprendizado
        learning_pattern = await web3_consciousness.learn_from_transaction(
            transaction_data=request.transaction_data,
            web3_type=web3_type
        )
        
        return {
            "success": True,
            "pattern_id": learning_pattern.pattern_id,
            "web3_domain": learning_pattern.web3_domain.value,
            "confidence": learning_pattern.confidence,
            "optimization_potential": learning_pattern.optimization_potential,
            "timestamp": learning_pattern.timestamp
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no aprendizado Web3: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/web3-consciousness/evolve-contract")
async def evolve_smart_contract(
    contract_address: str,
    current_code: str,
    performance_data: Dict[str, Any],
    current_user: AuthenticatedUser = Depends(require_scope("fractal:manage"))
):
    """
    Evolui contrato inteligente usando consciência Web3.
    """
    try:
        logger.info(f"Evolução de contrato solicitada por: {current_user.username}")
        
        # Executar evolução
        evolution_result = await web3_consciousness.evolve_smart_contract(
            contract_address=contract_address,
            current_code=current_code,
            performance_data=performance_data
        )
        
        return {
            "success": True,
            "contract_address": contract_address,
            "evolution_suggestions": evolution_result,
            "evolution_applied": evolution_result.get("evolution_result", {}).get("success", False)
        }
        
    except Exception as e:
        logger.error(f"Erro na evolução do contrato: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/web3-consciousness/optimize-gas")
async def optimize_gas_usage(
    contract_address: str,
    function_name: str,
    transaction_history: List[Dict[str, Any]],
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Otimiza uso de gas usando consciência Web3.
    """
    try:
        logger.info(f"Otimização de gas solicitada por: {current_user.username}")
        
        # Executar otimização
        gas_optimizations = await web3_consciousness.optimize_gas_usage(
            contract_address=contract_address,
            function_name=function_name,
            transaction_history=transaction_history
        )
        
        return {
            "success": True,
            "contract_address": contract_address,
            "function_name": function_name,
            "gas_optimizations": gas_optimizations,
            "total_potential_savings": gas_optimizations.get("total_potential_savings", 0)
        }
        
    except Exception as e:
        logger.error(f"Erro na otimização de gas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/ecosystem/health")
async def get_ecosystem_health(
    include_insights: bool = True,
    include_recommendations: bool = True,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna saúde holística do ecossistema.
    """
    try:
        logger.info(f"Saúde do ecossistema solicitada por: {current_user.username}")
        
        # Obter saúde do ecossistema
        health_report = await holistic_monitoring.get_ecosystem_health()
        
        # Adicionar insights se solicitado
        if include_insights:
            insights = await holistic_monitoring.get_ecosystem_insights(limit=10)
            health_report["recent_insights"] = insights
        
        # Adicionar recomendações se solicitado
        if include_recommendations:
            recommendations = await holistic_monitoring.generate_optimization_recommendations()
            health_report["optimization_recommendations"] = recommendations
        
        return health_report
        
    except Exception as e:
        logger.error(f"Erro ao obter saúde do ecossistema: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/ecosystem/component/{component}")
async def get_component_health(
    component: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna saúde de um componente específico.
    """
    try:
        logger.info(f"Saúde do componente {component} solicitada por: {current_user.username}")
        
        # Converter string para enum
        try:
            component_enum = EcosystemComponent(component)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Componente inválido: {component}"
            )
        
        # Obter saúde do componente
        component_health = await holistic_monitoring.get_component_health(component_enum)
        
        return component_health
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter saúde do componente {component}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/ecosystem/insights")
async def get_ecosystem_insights(
    limit: int = 20,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna insights do ecossistema.
    """
    try:
        logger.info(f"Insights do ecossistema solicitados por: {current_user.username}")
        
        # Obter insights
        insights = await holistic_monitoring.get_ecosystem_insights(limit=limit)
        
        return {
            "success": True,
            "insights": insights,
            "total_count": len(insights)
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter insights do ecossistema: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/ecosystem/alerts/correlated")
async def get_correlated_alerts(
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:advanced"))
):
    """
    Retorna alertas correlacionados do ecossistema.
    """
    try:
        logger.info(f"Alertas correlacionados solicitados por: {current_user.username}")
        
        # Obter alertas correlacionados
        correlated_alerts = await holistic_monitoring.get_correlated_alerts()
        
        return {
            "success": True,
            "correlated_alerts": correlated_alerts,
            "total_groups": len(correlated_alerts)
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter alertas correlacionados: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/ecosystem/recommendations")
async def get_optimization_recommendations(
    priority: Optional[str] = None,
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:advanced"))
):
    """
    Retorna recomendações de otimização do ecossistema.
    """
    try:
        logger.info(f"Recomendações de otimização solicitadas por: {current_user.username}")
        
        # Obter recomendações
        recommendations = await holistic_monitoring.generate_optimization_recommendations()
        
        # Filtrar por prioridade se especificado
        if priority:
            recommendations = [r for r in recommendations if r.get("priority") == priority]
        
        return {
            "success": True,
            "recommendations": recommendations,
            "total_count": len(recommendations),
            "priority_filter": priority
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter recomendações de otimização: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/web3-consciousness/status")
async def get_web3_consciousness_status(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna status da consciência Web3.
    """
    try:
        logger.info(f"Status da consciência Web3 solicitado por: {current_user.username}")
        
        # Obter status da consciência Web3
        consciousness_status = await web3_consciousness.get_web3_consciousness_status()
        
        return {
            "success": True,
            "consciousness_status": consciousness_status
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter status da consciência Web3: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/fractal-web3/health")
async def get_fractal_web3_health(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna saúde da integração fractal-Web3.
    """
    try:
        logger.info(f"Saúde fractal-Web3 solicitada por: {current_user.username}")
        
        # Obter saúde da integração fractal-Web3
        fractal_web3_health = await conscious_web3_manager.get_fractal_web3_health()
        
        return {
            "success": True,
            "fractal_web3_health": fractal_web3_health
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter saúde fractal-Web3: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/web3-consciousness/predict-market")
async def predict_market_behavior(
    market_data: Dict[str, Any],
    web3_context: Dict[str, Any],
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:advanced"))
):
    """
    Prediz comportamento de mercado usando consciência Web3.
    """
    try:
        logger.info(f"Predição de mercado solicitada por: {current_user.username}")
        
        # Executar predição
        predictions = await web3_consciousness.predict_market_behavior(
            market_data=market_data,
            web3_context=web3_context
        )
        
        return {
            "success": True,
            "market_predictions": predictions,
            "confidence": predictions.get("confidence", 0.5),
            "time_horizon": predictions.get("time_horizon", "24h")
        }
        
    except Exception as e:
        logger.error(f"Erro na predição de mercado: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/web3-consciousness/detect-security")
async def detect_security_threats(
    transaction_data: Dict[str, Any],
    contract_code: str,
    current_user: AuthenticatedUser = Depends(require_scope("security:override"))
):
    """
    Detecta ameaças de segurança usando consciência Web3.
    """
    try:
        logger.info(f"Detecção de segurança solicitada por: {current_user.username}")
        
        # Executar detecção de segurança
        security_analysis = await web3_consciousness.detect_security_threats(
            transaction_data=transaction_data,
            contract_code=contract_code
        )
        
        return {
            "success": True,
            "security_analysis": security_analysis,
            "threat_level": security_analysis.get("threat_level", "low"),
            "total_issues": security_analysis.get("total_issues", 0)
        }
        
    except Exception as e:
        logger.error(f"Erro na detecção de segurança: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
