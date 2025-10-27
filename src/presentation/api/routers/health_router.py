"""
Router para Health Checks e Metrics
"""

from fastapi import APIRouter, status
import time
import psutil

from src.infrastructure.config.settings import settings


router = APIRouter(tags=["Health & Monitoring"])


@router.get("/", summary="Status da API", description="Retorna status básico da API")
async def root():
    """Endpoint raiz com informações básicas"""
    return {
        "status": "online",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": time.time(),
    }


@router.get(
    "/health/live",
    status_code=status.HTTP_200_OK,
    summary="Liveness Probe",
    description="Verifica se a aplicação está viva (para Kubernetes)",
)
async def liveness():
    """
    Liveness probe para Kubernetes.

    Retorna 200 se a aplicação está rodando.
    """
    return {"status": "alive", "timestamp": time.time()}


@router.get(
    "/health/ready",
    summary="Readiness Probe",
    description="Verifica se a aplicação está pronta para receber tráfego",
)
async def readiness():
    """
    Readiness probe para Kubernetes.

    Verifica dependências (database, etc) antes de aceitar tráfego.
    """
    # TODO: Verificar database, redis, etc
    healthy = True

    return {
        "status": "ready" if healthy else "not_ready",
        "timestamp": time.time(),
        "checks": {"database": "ok", "cache": "ok"},  # TODO: implementar check real
    }


@router.get(
    "/health/simple",
    summary="Health Check Simples",
    description="Health check simplificado para load balancers",
)
async def health_simple():
    """Health check simples e rápido"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": time.time(),
    }


@router.get(
    "/metrics",
    summary="Métricas do Sistema",
    description="Retorna métricas detalhadas da aplicação",
)
async def metrics():
    """
    Retorna métricas da aplicação.

    Útil para monitoring com Prometheus/Grafana.
    """
    return {
        "timestamp": time.time(),
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "system": {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_used_mb": psutil.virtual_memory().used / 1024 / 1024,
            "memory_total_mb": psutil.virtual_memory().total / 1024 / 1024,
        },
        "config": {
            "debug": settings.DEBUG,
            "workers": settings.API_WORKERS,
            "rate_limit_enabled": settings.RATE_LIMIT_ENABLED,
        },
    }


@router.get(
    "/info",
    summary="Informações da API",
    description="Retorna informações completas sobre a API",
)
async def info():
    """Informações detalhadas da API"""
    return {
        "app": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "description": settings.APP_DESCRIPTION,
            "environment": settings.ENVIRONMENT,
        },
        "architecture": {
            "pattern": "Domain-Driven Design (DDD)",
            "principles": ["SOLID", "Clean Architecture", "Hexagonal Architecture"],
            "cqrs": True,
            "event_driven": True,
        },
        "features": {
            "defi": settings.FEATURE_DEFI,
            "governance": settings.FEATURE_GOVERNANCE,
            "nft": settings.FEATURE_NFT,
            "smart_contracts": settings.FEATURE_SMART_CONTRACTS,
        },
        "blockchain": {
            "mining_difficulty": settings.MINING_DIFFICULTY,
            "block_reward": settings.BLOCK_REWARD,
            "total_supply": settings.TOTAL_SUPPLY,
        },
        "timestamp": time.time(),
    }
