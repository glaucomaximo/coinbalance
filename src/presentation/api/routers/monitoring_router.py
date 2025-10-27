"""
Router para Sistema de Monitoramento Consciente
==============================================

Endpoints para acesso ao sistema de monitoramento consciente unificado,
fornecendo dashboards, alertas, insights e métricas em tempo real.
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import time

from src.infrastructure.monitoring.unified_monitoring import unified_monitoring
from src.infrastructure.monitoring.conscious_monitoring import conscious_monitoring
from src.infrastructure.monitoring.security_monitor import security_monitor
from src.infrastructure.monitoring.performance_monitor import performance_monitor
from src.infrastructure.security.auth import get_current_user, AuthenticatedUser, require_scope


router = APIRouter(
    prefix="/monitoramento",
    tags=["Monitoramento Consciente"],
    responses={
        401: {"description": "Não autorizado"},
        403: {"description": "Permissão negada"},
        500: {"description": "Erro interno do servidor"},
    },
)


@router.get(
    "/dashboard",
    summary="Dashboard Unificado",
    description="Retorna dashboard completo com todos os dados de monitoramento"
)
async def get_unified_dashboard(
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:read"))
) -> Dict[str, Any]:
    """Retorna dashboard unificado de monitoramento"""
    try:
        dashboard = unified_monitoring.get_unified_dashboard()
        return {
            "success": True,
            "data": dashboard,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter dashboard: {str(e)}"
        )


@router.get(
    "/saude-sistema",
    summary="Saúde do Sistema",
    description="Retorna status de saúde geral do sistema"
)
async def get_system_health(
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:read"))
) -> Dict[str, Any]:
    """Retorna saúde geral do sistema"""
    try:
        dashboard = unified_monitoring.get_unified_dashboard()
        overall_health = dashboard.get("overall_health", {})
        
        return {
            "success": True,
            "data": {
                "overall_score": overall_health.get("overall_score", 0.0),
                "status": overall_health.get("status", "unknown"),
                "conscious_score": overall_health.get("conscious_score", 0.0),
                "security_score": overall_health.get("security_score", 0.0),
                "performance_score": overall_health.get("performance_score", 0.0),
                "timestamp": overall_health.get("timestamp", time.time())
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter saúde do sistema: {str(e)}"
        )


@router.get(
    "/alertas",
    summary="Alertas Ativos",
    description="Retorna alertas ativos de todos os sistemas"
)
async def get_active_alerts(
    limit: int = Query(50, ge=1, le=100, description="Número máximo de alertas"),
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:read"))
) -> Dict[str, Any]:
    """Retorna alertas ativos"""
    try:
        dashboard = unified_monitoring.get_unified_dashboard()
        alerts = dashboard.get("unified_alerts", [])
        
        # Limita número de alertas
        limited_alerts = alerts[:limit]
        
        return {
            "success": True,
            "data": {
                "alerts": limited_alerts,
                "total_count": len(alerts),
                "returned_count": len(limited_alerts)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter alertas: {str(e)}"
        )


@router.post(
    "/alertas/{alert_id}/resolver",
    summary="Resolver Alerta",
    description="Marca um alerta como resolvido"
)
async def resolve_alert(
    alert_id: str,
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:write"))
) -> Dict[str, Any]:
    """Resolve um alerta"""
    try:
        success = unified_monitoring.resolve_alert(alert_id)
        
        if success:
            return {
                "success": True,
                "message": f"Alerta {alert_id} resolvido com sucesso"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alerta não encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao resolver alerta: {str(e)}"
        )


@router.get(
    "/insights",
    summary="Insights do Sistema",
    description="Retorna insights inteligentes gerados pelo sistema"
)
async def get_system_insights(
    limit: int = Query(20, ge=1, le=50, description="Número máximo de insights"),
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:read"))
) -> Dict[str, Any]:
    """Retorna insights do sistema"""
    try:
        dashboard = unified_monitoring.get_unified_dashboard()
        insights = dashboard.get("system_insights", [])
        
        # Limita número de insights
        limited_insights = insights[:limit]
        
        return {
            "success": True,
            "data": {
                "insights": limited_insights,
                "total_count": len(insights),
                "returned_count": len(limited_insights)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter insights: {str(e)}"
        )


@router.get(
    "/recomendacoes",
    summary="Recomendações do Sistema",
    description="Retorna recomendações gerais para melhoria do sistema"
)
async def get_system_recommendations(
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:read"))
) -> Dict[str, Any]:
    """Retorna recomendações do sistema"""
    try:
        recommendations = unified_monitoring.get_system_recommendations()
        
        return {
            "success": True,
            "data": {
                "recommendations": recommendations,
                "count": len(recommendations),
                "timestamp": time.time()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter recomendações: {str(e)}"
        )


# ========== ENDPOINTS ESPECÍFICOS POR SISTEMA ==========

@router.get(
    "/consciente",
    summary="Monitoramento Consciente",
    description="Retorna dados específicos do sistema de monitoramento consciente"
)
async def get_conscious_monitoring(
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:read"))
) -> Dict[str, Any]:
    """Retorna dados do monitoramento consciente"""
    try:
        dashboard = conscious_monitoring.get_monitoring_dashboard()
        
        return {
            "success": True,
            "data": dashboard
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter dados conscientes: {str(e)}"
        )


@router.get(
    "/seguranca",
    summary="Monitoramento de Segurança",
    description="Retorna dados específicos do sistema de monitoramento de segurança"
)
async def get_security_monitoring(
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:read"))
) -> Dict[str, Any]:
    """Retorna dados do monitoramento de segurança"""
    try:
        dashboard = security_monitor.get_security_dashboard()
        
        return {
            "success": True,
            "data": dashboard
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter dados de segurança: {str(e)}"
        )


@router.get(
    "/performance",
    summary="Monitoramento de Performance",
    description="Retorna dados específicos do sistema de monitoramento de performance"
)
async def get_performance_monitoring(
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:read"))
) -> Dict[str, Any]:
    """Retorna dados do monitoramento de performance"""
    try:
        dashboard = performance_monitor.get_performance_dashboard()
        
        return {
            "success": True,
            "data": dashboard
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter dados de performance: {str(e)}"
        )


# ========== ENDPOINTS DE MÉTRICAS ESPECÍFICAS ==========

@router.get(
    "/metricas/{metric_id}",
    summary="Métrica Específica",
    description="Retorna dados detalhados de uma métrica específica"
)
async def get_metric_details(
    metric_id: str,
    hours: int = Query(24, ge=1, le=168, description="Horas de histórico"),
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:read"))
) -> Dict[str, Any]:
    """Retorna detalhes de uma métrica específica"""
    try:
        insights = conscious_monitoring.get_metric_insights(metric_id)
        
        if not insights:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Métrica não encontrada"
            )
        
        return {
            "success": True,
            "data": insights
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter métrica: {str(e)}"
        )


@router.get(
    "/performance/tendencias/{metric}",
    summary="Tendências de Performance",
    description="Retorna tendências de uma métrica de performance"
)
async def get_performance_trends(
    metric: str,
    hours: int = Query(24, ge=1, le=168, description="Horas de histórico"),
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:read"))
) -> Dict[str, Any]:
    """Retorna tendências de performance"""
    try:
        from src.infrastructure.monitoring.performance_monitor import PerformanceMetric
        
        # Converte string para enum
        try:
            metric_enum = PerformanceMetric(metric)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Métrica inválida: {metric}"
            )
        
        trends = performance_monitor.get_metric_trends(metric_enum, hours)
        
        return {
            "success": True,
            "data": trends
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter tendências: {str(e)}"
        )


# ========== ENDPOINTS DE CONFIGURAÇÃO ==========

@router.post(
    "/configurar-threshold",
    summary="Configurar Threshold",
    description="Configura threshold para alertas (apenas admin)"
)
async def configure_threshold(
    metric_id: str,
    threshold_value: float,
    current_user: AuthenticatedUser = Depends(require_scope("admin:monitoring"))
) -> Dict[str, Any]:
    """Configura threshold para uma métrica"""
    try:
        # Em uma implementação real, isso seria persistido
        # Por enquanto, apenas retorna sucesso
        
        return {
            "success": True,
            "message": f"Threshold configurado para {metric_id}: {threshold_value}",
            "data": {
                "metric_id": metric_id,
                "threshold_value": threshold_value,
                "configured_by": current_user.wallet_address,
                "timestamp": time.time()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao configurar threshold: {str(e)}"
        )


@router.get(
    "/status",
    summary="Status dos Sistemas",
    description="Retorna status de todos os sistemas de monitoramento"
)
async def get_monitoring_status(
    current_user: AuthenticatedUser = Depends(require_scope("monitoring:read"))
) -> Dict[str, Any]:
    """Retorna status dos sistemas de monitoramento"""
    try:
        return {
            "success": True,
            "data": {
                "conscious_monitoring": {
                    "status": "active",
                    "metrics_count": len(conscious_monitoring.metrics),
                    "alerts_count": len(conscious_monitoring.alerts)
                },
                "security_monitoring": {
                    "status": "active",
                    "incidents_count": len(security_monitor.incidents),
                    "patterns_count": len(security_monitor.patterns)
                },
                "performance_monitoring": {
                    "status": "active",
                    "rules_count": len(performance_monitor.optimization_rules),
                    "optimizations_count": len(performance_monitor.optimization_history)
                },
                "unified_monitoring": {
                    "status": "active",
                    "correlation_rules_count": len(unified_monitoring.correlation_rules),
                    "insights_count": len(unified_monitoring.system_insights)
                },
                "timestamp": time.time()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter status: {str(e)}"
        )
