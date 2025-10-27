"""
Router para Sistema de Arquitetura Fractal Consciente
====================================================

Endpoints para acesso ao sistema de arquitetura fractal, fornecendo
controle e monitoramento de fractais, replicação, escala e auto-organização.
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional, List, Dict, Any
from decimal import Decimal
import time

from src.infrastructure.fractal.fractal_core import fractal_core, FractalType, FractalState, FractalDimension
from src.infrastructure.fractal.fractal_replication import fractal_replication, ReplicationStrategy, ReplicationTrigger
from src.infrastructure.fractal.infinite_scaler import infinite_fractal_scaler, ScalingDimension, ScalingTrigger
from src.infrastructure.fractal.self_organization import fractal_self_organization, EmergenceType, OrganizationPattern
from src.infrastructure.security.auth import get_current_user, AuthenticatedUser, require_scope


router = APIRouter(
    prefix="/fractal",
    tags=["Arquitetura Fractal Consciente"],
    responses={
        401: {"description": "Não autorizado"},
        403: {"description": "Permissão negada"},
        500: {"description": "Erro interno do servidor"},
    },
)


# ========== ENDPOINTS DO NÚCLEO FRACTAL ==========

@router.get(
    "/nucleo/hierarquia",
    summary="Hierarquia Fractal",
    description="Retorna hierarquia completa dos fractais do sistema"
)
async def get_fractal_hierarchy(
    current_user: AuthenticatedUser = Depends(require_scope("fractal:read"))
) -> Dict[str, Any]:
    """Retorna hierarquia fractal"""
    try:
        hierarchy = fractal_core.get_fractal_hierarchy()
        
        return {
            "success": True,
            "data": hierarchy,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter hierarquia fractal: {str(e)}"
        )


@router.get(
    "/nucleo/analytics",
    summary="Analytics Fractais",
    description="Retorna analytics detalhados dos fractais"
)
async def get_fractal_analytics(
    current_user: AuthenticatedUser = Depends(require_scope("fractal:read"))
) -> Dict[str, Any]:
    """Retorna analytics dos fractais"""
    try:
        analytics = fractal_core.get_fractal_analytics()
        
        return {
            "success": True,
            "data": analytics,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter analytics fractais: {str(e)}"
        )


@router.post(
    "/nucleo/criar-instancia",
    summary="Criar Instância Fractal",
    description="Cria nova instância fractal"
)
async def create_fractal_instance(
    pattern_id: str,
    parent_id: Optional[str] = None,
    initial_context: Optional[Dict[str, Any]] = None,
    current_user: AuthenticatedUser = Depends(require_scope("fractal:write"))
) -> Dict[str, Any]:
    """Cria nova instância fractal"""
    try:
        instance = fractal_core.create_fractal_instance(
            pattern_id, parent_id, initial_context or {}
        )
        
        return {
            "success": True,
            "data": {
                "id": instance.id,
                "pattern_id": instance.pattern_id,
                "parent_id": instance.parent_id,
                "state": instance.state.value,
                "consciousness_level": float(instance.consciousness_level),
                "energy_level": float(instance.energy_level),
                "scaling_level": instance.scaling_level,
                "created_at": instance.created_at
            },
            "message": "Instância fractal criada com sucesso"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar instância fractal: {str(e)}"
        )


@router.post(
    "/nucleo/replicar/{fractal_id}",
    summary="Replicar Fractal",
    description="Replica um fractal baseado em suas regras"
)
async def replicate_fractal(
    fractal_id: str,
    context: Optional[Dict[str, Any]] = None,
    current_user: AuthenticatedUser = Depends(require_scope("fractal:write"))
) -> Dict[str, Any]:
    """Replica um fractal"""
    try:
        new_instance = fractal_core.replicate_fractal(fractal_id, context or {})
        
        if new_instance:
            return {
                "success": True,
                "data": {
                    "source_id": fractal_id,
                    "new_instance_id": new_instance.id,
                    "pattern_id": new_instance.pattern_id,
                    "consciousness_level": float(new_instance.consciousness_level)
                },
                "message": "Fractal replicado com sucesso"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não foi possível replicar o fractal"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao replicar fractal: {str(e)}"
        )


@router.post(
    "/nucleo/escalar/{fractal_id}",
    summary="Escalar Fractal",
    description="Escala um fractal para nova dimensão"
)
async def scale_fractal(
    fractal_id: str,
    scale_factor: float,
    current_user: AuthenticatedUser = Depends(require_scope("fractal:write"))
) -> Dict[str, Any]:
    """Escala um fractal"""
    try:
        success = fractal_core.scale_fractal(fractal_id, Decimal(str(scale_factor)))
        
        if success:
            return {
                "success": True,
                "data": {
                    "fractal_id": fractal_id,
                    "scale_factor": scale_factor
                },
                "message": "Fractal escalado com sucesso"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não foi possível escalar o fractal"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao escalar fractal: {str(e)}"
        )


# ========== ENDPOINTS DE REPLICAÇÃO ==========

@router.get(
    "/replicacao/analytics",
    summary="Analytics de Replicação",
    description="Retorna analytics de replicação fractal"
)
async def get_replication_analytics(
    current_user: AuthenticatedUser = Depends(require_scope("fractal:read"))
) -> Dict[str, Any]:
    """Retorna analytics de replicação"""
    try:
        analytics = fractal_replication.get_replication_analytics()
        
        return {
            "success": True,
            "data": analytics,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter analytics de replicação: {str(e)}"
        )


@router.post(
    "/replicacao/executar/{fractal_id}",
    summary="Executar Replicação",
    description="Executa replicação de um fractal"
)
async def execute_replication(
    fractal_id: str,
    rule_id: str,
    current_user: AuthenticatedUser = Depends(require_scope("fractal:write"))
) -> Dict[str, Any]:
    """Executa replicação"""
    try:
        if rule_id not in fractal_replication.replication_rules:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Regra de replicação não encontrada"
            )
        
        rule = fractal_replication.replication_rules[rule_id]
        event = fractal_replication.execute_replication(fractal_id, rule)
        
        if event:
            return {
                "success": True,
                "data": {
                    "event_id": event.id,
                    "source_fractal": event.source_fractal_id,
                    "target_fractal": event.target_fractal_id,
                    "strategy": event.strategy.value,
                    "trigger": event.trigger.value,
                    "success": event.success,
                    "energy_cost": float(event.energy_cost),
                    "consciousness_gained": float(event.consciousness_gained)
                },
                "message": "Replicação executada com sucesso"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não foi possível executar a replicação"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao executar replicação: {str(e)}"
        )


@router.put(
    "/replicacao/orcamento",
    summary="Atualizar Orçamento de Replicação",
    description="Atualiza orçamentos de energia e consciência para replicação"
)
async def update_replication_budget(
    energy_budget: float,
    consciousness_budget: float,
    current_user: AuthenticatedUser = Depends(require_scope("fractal:admin"))
) -> Dict[str, Any]:
    """Atualiza orçamento de replicação"""
    try:
        fractal_replication.update_resource_budgets(
            Decimal(str(energy_budget)), 
            Decimal(str(consciousness_budget))
        )
        
        return {
            "success": True,
            "data": {
                "energy_budget": energy_budget,
                "consciousness_budget": consciousness_budget
            },
            "message": "Orçamento de replicação atualizado com sucesso"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar orçamento: {str(e)}"
        )


# ========== ENDPOINTS DE ESCALA INFINITA ==========

@router.get(
    "/escala/analytics",
    summary="Analytics de Escala",
    description="Retorna analytics de escala fractal infinita"
)
async def get_scaling_analytics(
    current_user: AuthenticatedUser = Depends(require_scope("fractal:read"))
) -> Dict[str, Any]:
    """Retorna analytics de escala"""
    try:
        analytics = infinite_fractal_scaler.get_scaling_analytics()
        
        return {
            "success": True,
            "data": analytics,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter analytics de escala: {str(e)}"
        )


@router.post(
    "/escala/executar/{fractal_id}",
    summary="Executar Escala",
    description="Executa escala de um fractal"
)
async def execute_scaling(
    fractal_id: str,
    rule_id: str,
    current_user: AuthenticatedUser = Depends(require_scope("fractal:write"))
) -> Dict[str, Any]:
    """Executa escala"""
    try:
        if rule_id not in infinite_fractal_scaler.scaling_rules:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Regra de escala não encontrada"
            )
        
        rule = infinite_fractal_scaler.scaling_rules[rule_id]
        event = infinite_fractal_scaler.execute_scaling(fractal_id, rule)
        
        if event:
            return {
                "success": True,
                "data": {
                    "event_id": event.id,
                    "fractal_id": event.fractal_id,
                    "dimension": event.dimension.value,
                    "trigger": event.trigger.value,
                    "scaling_factor": float(event.scaling_factor),
                    "success": event.success,
                    "energy_cost": float(event.energy_cost),
                    "performance_improvement": float(event.performance_improvement)
                },
                "message": "Escala executada com sucesso"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não foi possível executar a escala"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao executar escala: {str(e)}"
        )


@router.put(
    "/escala/orcamento",
    summary="Atualizar Orçamento de Escala",
    description="Atualiza orçamentos de energia e consciência para escala"
)
async def update_scaling_budget(
    energy_budget: float,
    consciousness_budget: float,
    current_user: AuthenticatedUser = Depends(require_scope("fractal:admin"))
) -> Dict[str, Any]:
    """Atualiza orçamento de escala"""
    try:
        infinite_fractal_scaler.update_scaling_budgets(
            Decimal(str(energy_budget)), 
            Decimal(str(consciousness_budget))
        )
        
        return {
            "success": True,
            "data": {
                "energy_budget": energy_budget,
                "consciousness_budget": consciousness_budget
            },
            "message": "Orçamento de escala atualizado com sucesso"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar orçamento: {str(e)}"
        )


# ========== ENDPOINTS DE AUTO-ORGANIZAÇÃO ==========

@router.get(
    "/auto-organizacao/analytics",
    summary="Analytics de Auto-Organização",
    description="Retorna analytics de auto-organização e emergência"
)
async def get_self_organization_analytics(
    current_user: AuthenticatedUser = Depends(require_scope("fractal:read"))
) -> Dict[str, Any]:
    """Retorna analytics de auto-organização"""
    try:
        analytics = fractal_self_organization.get_emergence_analytics()
        
        return {
            "success": True,
            "data": analytics,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter analytics de auto-organização: {str(e)}"
        )


@router.get(
    "/auto-organizacao/estruturas",
    summary="Estruturas Organizacionais",
    description="Retorna estruturas organizacionais emergentes"
)
async def get_organization_structures(
    limit: int = Query(20, ge=1, le=100, description="Número máximo de estruturas"),
    current_user: AuthenticatedUser = Depends(require_scope("fractal:read"))
) -> Dict[str, Any]:
    """Retorna estruturas organizacionais"""
    try:
        structures = list(fractal_self_organization.organization_structures.values())
        limited_structures = structures[:limit]
        
        return {
            "success": True,
            "data": {
                "structures": limited_structures,
                "total_count": len(structures),
                "returned_count": len(limited_structures)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter estruturas organizacionais: {str(e)}"
        )


@router.post(
    "/auto-organizacao/emergencia",
    summary="Forçar Emergência",
    description="Força emergência de um grupo de fractais (apenas admin)"
)
async def force_emergence(
    group_fractals: List[str],
    rule_id: str,
    current_user: AuthenticatedUser = Depends(require_scope("fractal:admin"))
) -> Dict[str, Any]:
    """Força emergência de um grupo"""
    try:
        if rule_id not in fractal_self_organization.emergence_rules:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Regra de emergência não encontrada"
            )
        
        rule = fractal_self_organization.emergence_rules[rule_id]
        event = fractal_self_organization.execute_emergence(group_fractals, rule)
        
        if event:
            return {
                "success": True,
                "data": {
                    "event_id": event.id,
                    "emergence_type": event.emergence_type.value,
                    "organization_pattern": event.organization_pattern.value,
                    "participating_fractals": event.participating_fractals,
                    "consciousness_level": float(event.consciousness_level),
                    "success": event.success
                },
                "message": "Emergência executada com sucesso"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não foi possível executar a emergência"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao executar emergência: {str(e)}"
        )


# ========== ENDPOINTS DE DASHBOARD UNIFICADO ==========

@router.get(
    "/dashboard",
    summary="Dashboard Fractal Unificado",
    description="Retorna dashboard completo do sistema fractal"
)
async def get_fractal_dashboard(
    current_user: AuthenticatedUser = Depends(require_scope("fractal:read"))
) -> Dict[str, Any]:
    """Retorna dashboard fractal unificado"""
    try:
        # Coleta dados de todos os sistemas
        hierarchy = fractal_core.get_fractal_hierarchy()
        core_analytics = fractal_core.get_fractal_analytics()
        replication_analytics = fractal_replication.get_replication_analytics()
        scaling_analytics = infinite_fractal_scaler.get_scaling_analytics()
        organization_analytics = fractal_self_organization.get_emergence_analytics()
        
        dashboard = {
            "hierarchy": hierarchy,
            "core_analytics": core_analytics,
            "replication_analytics": replication_analytics,
            "scaling_analytics": scaling_analytics,
            "organization_analytics": organization_analytics,
            "system_status": {
                "total_fractals": len(fractal_core.fractal_instances),
                "total_patterns": len(fractal_core.fractal_patterns),
                "total_connections": len(fractal_core.fractal_connections),
                "active_replications": len(fractal_replication.active_replications),
                "active_scaling": len(infinite_fractal_scaler.active_scaling),
                "organization_structures": len(fractal_self_organization.organization_structures)
            },
            "timestamp": time.time()
        }
        
        return {
            "success": True,
            "data": dashboard
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter dashboard fractal: {str(e)}"
        )


# ========== ENDPOINTS DE CONFIGURAÇÃO ==========

@router.get(
    "/configuracao/regras",
    summary="Regras do Sistema",
    description="Retorna todas as regras configuradas no sistema fractal"
)
async def get_system_rules(
    current_user: AuthenticatedUser = Depends(require_scope("fractal:read"))
) -> Dict[str, Any]:
    """Retorna regras do sistema"""
    try:
        rules = {
            "replication_rules": [
                {
                    "id": rule.id,
                    "name": rule.name,
                    "trigger": rule.trigger.value,
                    "strategy": rule.strategy.value,
                    "enabled": rule.enabled,
                    "priority": rule.priority
                }
                for rule in fractal_replication.replication_rules.values()
            ],
            "scaling_rules": [
                {
                    "id": rule.id,
                    "name": rule.name,
                    "dimension": rule.dimension.value,
                    "trigger": rule.trigger.value,
                    "enabled": rule.enabled,
                    "priority": rule.priority
                }
                for rule in infinite_fractal_scaler.scaling_rules.values()
            ],
            "emergence_rules": [
                {
                    "id": rule.id,
                    "name": rule.name,
                    "emergence_type": rule.emergence_type.value,
                    "organization_pattern": rule.organization_pattern.value,
                    "enabled": rule.enabled,
                    "priority": rule.priority
                }
                for rule in fractal_self_organization.emergence_rules.values()
            ]
        }
        
        return {
            "success": True,
            "data": rules
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter regras do sistema: {str(e)}"
        )


@router.get(
    "/status",
    summary="Status do Sistema Fractal",
    description="Retorna status geral do sistema fractal"
)
async def get_fractal_system_status(
    current_user: AuthenticatedUser = Depends(require_scope("fractal:read"))
) -> Dict[str, Any]:
    """Retorna status do sistema fractal"""
    try:
        status = {
            "fractal_core": {
                "status": "active",
                "fractal_instances": len(fractal_core.fractal_instances),
                "fractal_patterns": len(fractal_core.fractal_patterns),
                "fractal_connections": len(fractal_core.fractal_connections)
            },
            "replication_system": {
                "status": "active",
                "replication_rules": len(fractal_replication.replication_rules),
                "replication_events": len(fractal_replication.replication_events),
                "active_replications": len(fractal_replication.active_replications)
            },
            "scaling_system": {
                "status": "active",
                "scaling_rules": len(infinite_fractal_scaler.scaling_rules),
                "scaling_events": len(infinite_fractal_scaler.scaling_events),
                "active_scaling": len(infinite_fractal_scaler.active_scaling)
            },
            "self_organization": {
                "status": "active",
                "emergence_rules": len(fractal_self_organization.emergence_rules),
                "emergence_events": len(fractal_self_organization.emergence_events),
                "organization_structures": len(fractal_self_organization.organization_structures)
            },
            "timestamp": time.time()
        }
        
        return {
            "success": True,
            "data": status
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter status do sistema: {str(e)}"
        )
