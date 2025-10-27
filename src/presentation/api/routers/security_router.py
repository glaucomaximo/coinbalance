"""
Router de Monitoramento de Segurança - CoinBalance CNB
Endpoints para visualizar métricas e alertas de segurança
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional, List
from datetime import datetime, timedelta

from src.infrastructure.monitoring.security_monitor import security_monitor, SecurityEvent
from src.infrastructure.security.auth import get_current_user, AuthenticatedUser, require_scope

router = APIRouter(
    prefix="/security",
    tags=["Segurança"],
    responses={
        401: {"description": "Não autorizado"},
        403: {"description": "Permissão negada"},
        404: {"description": "Recurso não encontrado"},
    },
)


@router.get(
    "/events",
    summary="Listar Eventos de Segurança",
    description="Lista eventos de segurança recentes"
)
async def get_security_events(
    hours: int = Query(24, description="Horas para buscar eventos"),
    event_type: Optional[str] = Query(None, description="Tipo de evento"),
    current_user: AuthenticatedUser = Depends(require_scope("admin:security"))
) -> List[dict]:
    """Lista eventos de segurança recentes"""
    try:
        events = security_monitor.get_recent_events(hours=hours, event_type=event_type)
        
        return [
            {
                "timestamp": event.timestamp,
                "event_type": event.event_type,
                "severity": event.severity,
                "source_ip": event.source_ip,
                "user_agent": event.user_agent,
                "wallet_address": event.wallet_address,
                "description": event.description,
                "metadata": event.metadata
            }
            for event in events
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar eventos: {str(e)}"
        )


@router.get(
    "/alerts",
    summary="Listar Alertas de Segurança",
    description="Lista alertas de segurança ativos"
)
async def get_security_alerts(
    current_user: AuthenticatedUser = Depends(require_scope("admin:security"))
) -> List[dict]:
    """Lista alertas de segurança ativos"""
    try:
        alerts = security_monitor.get_active_alerts()
        
        return [
            {
                "alert_id": alert.alert_id,
                "timestamp": alert.timestamp,
                "alert_type": alert.alert_type,
                "severity": alert.severity,
                "description": alert.description,
                "affected_resources": alert.affected_resources,
                "recommended_actions": alert.recommended_actions,
                "metadata": alert.metadata
            }
            for alert in alerts
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar alertas: {str(e)}"
        )


@router.get(
    "/metrics",
    summary="Métricas de Segurança",
    description="Retorna métricas de segurança do sistema"
)
async def get_security_metrics(
    hours: int = Query(24, description="Horas para calcular métricas"),
    current_user: AuthenticatedUser = Depends(require_scope("admin:security"))
) -> dict:
    """Retorna métricas de segurança"""
    try:
        metrics = security_monitor.get_security_metrics(hours=hours)
        
        return {
            "period_hours": hours,
            "total_events": metrics["total_events"],
            "total_alerts": metrics["total_alerts"],
            "event_counts": metrics["event_counts"],
            "alert_counts": metrics["alert_counts"],
            "top_problematic_ips": metrics["top_problematic_ips"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao calcular métricas: {str(e)}"
        )


@router.get(
    "/dashboard",
    summary="Dashboard de Segurança",
    description="Dashboard com resumo de segurança"
)
async def get_security_dashboard(
    current_user: AuthenticatedUser = Depends(require_scope("admin:security"))
) -> dict:
    """Dashboard de segurança com resumo"""
    try:
        # Métricas das últimas 24 horas
        metrics_24h = security_monitor.get_security_metrics(hours=24)
        
        # Métricas das últimas 7 dias
        metrics_7d = security_monitor.get_security_metrics(hours=168)
        
        # Alertas ativos
        active_alerts = security_monitor.get_active_alerts()
        
        # Eventos críticos recentes
        critical_events = security_monitor.get_recent_events(hours=1)
        critical_events = [e for e in critical_events if e.severity in ["HIGH", "CRITICAL"]]
        
        return {
            "summary": {
                "active_alerts": len(active_alerts),
                "critical_events_last_hour": len(critical_events),
                "total_events_24h": metrics_24h["total_events"],
                "total_alerts_24h": metrics_24h["total_alerts"]
            },
            "trends": {
                "events_24h": metrics_24h["event_counts"],
                "events_7d": metrics_7d["event_counts"],
                "alerts_24h": metrics_24h["alert_counts"],
                "alerts_7d": metrics_7d["alert_counts"]
            },
            "top_threats": {
                "problematic_ips_24h": metrics_24h["top_problematic_ips"][:5],
                "problematic_ips_7d": metrics_7d["top_problematic_ips"][:5]
            },
            "recent_critical_events": [
                {
                    "timestamp": event.timestamp,
                    "type": event.event_type,
                    "severity": event.severity,
                    "description": event.description,
                    "source_ip": event.source_ip
                }
                for event in critical_events[:10]
            ],
            "active_alerts": [
                {
                    "alert_id": alert.alert_id,
                    "type": alert.alert_type,
                    "severity": alert.severity,
                    "description": alert.description,
                    "timestamp": alert.timestamp
                }
                for alert in active_alerts[:10]
            ],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar dashboard: {str(e)}"
        )


@router.post(
    "/cleanup",
    summary="Limpeza de Dados Antigos",
    description="Remove dados antigos de monitoramento"
)
async def cleanup_old_data(
    days: int = Query(30, description="Dias de dados para manter"),
    current_user: AuthenticatedUser = Depends(require_scope("admin:security"))
) -> dict:
    """Remove dados antigos de monitoramento"""
    try:
        security_monitor.cleanup_old_data(days=days)
        
        return {
            "success": True,
            "message": f"Dados anteriores a {days} dias foram removidos",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na limpeza: {str(e)}"
        )


@router.get(
    "/health",
    summary="Status do Monitoramento",
    description="Verifica se o sistema de monitoramento está funcionando"
)
async def security_monitoring_health() -> dict:
    """Verifica status do monitoramento"""
    try:
        # Testar conexão com banco
        events = security_monitor.get_recent_events(hours=1)
        alerts = security_monitor.get_active_alerts()
        
        return {
            "status": "healthy",
            "monitoring_active": True,
            "events_last_hour": len(events),
            "active_alerts": len(alerts),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "monitoring_active": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
