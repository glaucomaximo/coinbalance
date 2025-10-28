"""
Blockchain Performance Router - Roteador de Performance da Blockchain
=====================================================================

Este router expõe endpoints para monitoramento e otimização de performance
da blockchain, incluindo estatísticas detalhadas e otimizações automáticas.

EVOLUÇÃO: Endpoints para monitoramento de performance da blockchain otimizada.
"""

import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from decimal import Decimal

from src.infrastructure.security.auth import (
    get_current_user, AuthenticatedUser, require_scope
)
from src.domain.blockchain.entities.blockchain import Blockchain
from src.domain.blockchain.infrastructure.blockchain_index import (
    blockchain_index, transaction_pool
)
from src.domain.blockchain.infrastructure.parallel_miner import parallel_miner
from src.domain.blockchain.infrastructure.incremental_validator import incremental_validator
from src.domain.blockchain.infrastructure.blockchain_tree import blockchain_tree
from src.domain.blockchain.infrastructure.distributed_cache import distributed_cache
from src.domain.blockchain.infrastructure.network_optimizer import network_optimizer
from src.domain.blockchain.infrastructure.horizontal_scaler import horizontal_scaler
from src.domain.blockchain.infrastructure.real_time_monitor import real_time_monitor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/blockchain-performance", tags=["Blockchain Performance"])

# ========== SCHEMAS ==========

class PerformanceStatisticsResponse(BaseModel):
    """Resposta com estatísticas de performance"""
    blockchain: Dict[str, Any]
    index_performance: Dict[str, Any]
    transaction_pool: Dict[str, Any]
    timestamp: float

class OptimizationRequest(BaseModel):
    """Requisição para otimização de performance"""
    cleanup_cache: bool = Field(True, description="Limpar cache expirado")
    cleanup_transactions: bool = Field(True, description="Limpar transações expiradas")
    force_optimization: bool = Field(False, description="Forçar otimização completa")

class OptimizationResponse(BaseModel):
    """Resposta de otimização"""
    success: bool
    optimizations_applied: List[str]
    cache_cleanup: int
    transaction_cleanup: int
    timestamp: float
    error: Optional[str] = None

class CacheStatisticsResponse(BaseModel):
    """Estatísticas do cache"""
    index_size: int
    cache_size: int
    validation_cache_size: int
    hash_lookups: int
    height_lookups: int
    cache_hits: int
    cache_misses: int
    cache_hit_rate: float
    validations_cached: int
    validations_computed: int
    validation_cache_hit_rate: float

class TransactionPoolStatisticsResponse(BaseModel):
    """Estatísticas do pool de transações"""
    pool_size: int
    max_pool_size: int
    unique_addresses: int
    transactions_added: int
    transactions_removed: int
    duplicate_rejections: int
    expired_cleanups: int
    min_fee_threshold: float
    transaction_ttl: int

# ========== ENDPOINTS ==========

@router.get("/statistics", response_model=PerformanceStatisticsResponse, status_code=status.HTTP_200_OK)
async def get_performance_statistics(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna estatísticas detalhadas de performance da blockchain.
    
    EVOLUÇÃO: Estatísticas completas incluindo índices e pool de transações.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        # Por simplicidade, criamos uma instância temporária
        blockchain = Blockchain.create()
        
        stats = blockchain.get_performance_statistics()
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao obter estatísticas de performance"
            )
        
        return PerformanceStatisticsResponse(**stats)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas de performance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/optimize", response_model=OptimizationResponse, status_code=status.HTTP_200_OK)
async def optimize_blockchain_performance(
    request: OptimizationRequest,
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Executa otimizações de performance da blockchain.
    
    EVOLUÇÃO: Otimização automática com limpeza de cache e transações.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        # Executar otimizações
        result = blockchain.optimize_performance()
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        # Executar limpezas adicionais se solicitado
        if request.cleanup_cache:
            background_tasks.add_task(blockchain_index.cleanup_expired_cache)
        
        if request.cleanup_transactions:
            background_tasks.add_task(transaction_pool.cleanup_expired_transactions)
        
        return OptimizationResponse(
            success=True,
            optimizations_applied=result["optimizations_applied"],
            cache_cleanup=result["cache_cleanup"],
            transaction_cleanup=result["transaction_cleanup"],
            timestamp=result["timestamp"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na otimização de performance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/cache-statistics", response_model=CacheStatisticsResponse, status_code=status.HTTP_200_OK)
async def get_cache_statistics(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna estatísticas detalhadas do cache da blockchain.
    
    EVOLUÇÃO: Métricas detalhadas de cache e índices.
    """
    try:
        stats = blockchain_index.get_statistics()
        
        return CacheStatisticsResponse(
            index_size=stats["index_size"],
            cache_size=stats["cache_size"],
            validation_cache_size=stats["validation_cache_size"],
            hash_lookups=stats["hash_lookups"],
            height_lookups=stats["height_lookups"],
            cache_hits=stats["cache_hits"],
            cache_misses=stats["cache_misses"],
            cache_hit_rate=stats["cache_hit_rate"],
            validations_cached=stats["validations_cached"],
            validations_computed=stats["validations_computed"],
            validation_cache_hit_rate=stats["validation_cache_hit_rate"]
        )
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas do cache: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/transaction-pool-statistics", response_model=TransactionPoolStatisticsResponse, status_code=status.HTTP_200_OK)
async def get_transaction_pool_statistics(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna estatísticas detalhadas do pool de transações.
    
    EVOLUÇÃO: Métricas detalhadas do pool de transações.
    """
    try:
        stats = transaction_pool.get_statistics()
        
        return TransactionPoolStatisticsResponse(
            pool_size=stats["pool_size"],
            max_pool_size=stats["max_pool_size"],
            unique_addresses=stats["unique_addresses"],
            transactions_added=stats["transactions_added"],
            transactions_removed=stats["transactions_removed"],
            duplicate_rejections=stats["duplicate_rejections"],
            expired_cleanups=stats["expired_cleanups"],
            min_fee_threshold=stats["min_fee_threshold"],
            transaction_ttl=stats["transaction_ttl"]
        )
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas do pool de transações: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/clear-cache", status_code=status.HTTP_200_OK)
async def clear_blockchain_cache(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Limpa todos os caches da blockchain.
    
    EVOLUÇÃO: Limpeza completa de cache para reset de performance.
    """
    try:
        blockchain_index.clear_cache()
        
        return {
            "success": True,
            "message": "Cache da blockchain limpo com sucesso",
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro ao limpar cache da blockchain: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/health-check", status_code=status.HTTP_200_OK)
async def blockchain_performance_health_check(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Verifica a saúde da performance da blockchain.
    
    EVOLUÇÃO: Health check específico para performance.
    """
    try:
        # Obter estatísticas básicas
        index_stats = blockchain_index.get_statistics()
        pool_stats = transaction_pool.get_statistics()
        
        # Verificar indicadores de saúde
        health_indicators = {
            "cache_hit_rate_healthy": index_stats["cache_hit_rate"] > 0.7,
            "validation_cache_hit_rate_healthy": index_stats["validation_cache_hit_rate"] > 0.5,
            "pool_size_healthy": pool_stats["pool_size"] < pool_stats["max_pool_size"] * 0.9,
            "index_size_reasonable": index_stats["index_size"] > 0
        }
        
        # Calcular score geral de saúde
        healthy_count = sum(health_indicators.values())
        total_count = len(health_indicators)
        health_score = healthy_count / total_count if total_count > 0 else 0
        
        # Determinar status geral
        if health_score >= 0.8:
            status = "healthy"
        elif health_score >= 0.6:
            status = "warning"
        else:
            status = "critical"
        
        return {
            "status": status,
            "health_score": health_score,
            "indicators": health_indicators,
            "recommendations": _get_performance_recommendations(health_indicators),
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro no health check de performance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/recommendations", status_code=status.HTTP_200_OK)
async def get_performance_recommendations(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna recomendações de otimização de performance.
    
    EVOLUÇÃO: Recomendações inteligentes baseadas em métricas.
    """
    try:
        index_stats = blockchain_index.get_statistics()
        pool_stats = transaction_pool.get_statistics()
        
        recommendations = []
        
        # Recomendações baseadas em cache hit rate
        if index_stats["cache_hit_rate"] < 0.7:
            recommendations.append({
                "type": "cache_optimization",
                "priority": "high",
                "title": "Cache Hit Rate Baixo",
                "description": f"Cache hit rate atual: {index_stats['cache_hit_rate']:.2%}. Considere aumentar o tamanho do cache.",
                "action": "increase_cache_size"
            })
        
        # Recomendações baseadas em validação cache
        if index_stats["validation_cache_hit_rate"] < 0.5:
            recommendations.append({
                "type": "validation_cache",
                "priority": "medium",
                "title": "Cache de Validação Ineficiente",
                "description": f"Cache de validação hit rate: {index_stats['validation_cache_hit_rate']:.2%}. Considere ajustar TTL.",
                "action": "adjust_validation_cache_ttl"
            })
        
        # Recomendações baseadas no pool de transações
        if pool_stats["pool_size"] > pool_stats["max_pool_size"] * 0.8:
            recommendations.append({
                "type": "transaction_pool",
                "priority": "medium",
                "title": "Pool de Transações Quase Cheio",
                "description": f"Pool atual: {pool_stats['pool_size']}/{pool_stats['max_pool_size']}. Considere aumentar capacidade.",
                "action": "increase_pool_capacity"
            })
        
        # Recomendações baseadas em rejeições de duplicatas
        if pool_stats["duplicate_rejections"] > pool_stats["transactions_added"] * 0.1:
            recommendations.append({
                "type": "duplicate_handling",
                "priority": "low",
                "title": "Muitas Transações Duplicadas",
                "description": f"Taxa de rejeição por duplicatas: {pool_stats['duplicate_rejections']}/{pool_stats['transactions_added']}",
                "action": "improve_duplicate_detection"
            })
        
        return {
            "recommendations": recommendations,
            "total_recommendations": len(recommendations),
            "high_priority": len([r for r in recommendations if r["priority"] == "high"]),
            "medium_priority": len([r for r in recommendations if r["priority"] == "medium"]),
            "low_priority": len([r for r in recommendations if r["priority"] == "low"]),
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter recomendações de performance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# ========== HELPER FUNCTIONS ==========

def _get_performance_recommendations(health_indicators: Dict[str, bool]) -> List[str]:
    """Gera recomendações baseadas nos indicadores de saúde."""
    recommendations = []
    
    if not health_indicators["cache_hit_rate_healthy"]:
        recommendations.append("Considere aumentar o tamanho do cache ou ajustar estratégia de cache")
    
    if not health_indicators["validation_cache_hit_rate_healthy"]:
        recommendations.append("Ajuste o TTL do cache de validações ou implemente cache mais inteligente")
    
    if not health_indicators["pool_size_healthy"]:
        recommendations.append("Aumente a capacidade do pool de transações ou implemente limpeza mais agressiva")
    
    if not health_indicators["index_size_reasonable"]:
        recommendations.append("Verifique se os índices estão sendo populados corretamente")
    
        return recommendations

@router.get("/mining-statistics", status_code=status.HTTP_200_OK)
async def get_mining_statistics(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna estatísticas detalhadas de mineração paralela.
    
    EVOLUÇÃO: Métricas de mineração paralela e otimização.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        stats = blockchain.get_mining_statistics()
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao obter estatísticas de mineração"
            )
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas de mineração: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/optimize-mining", status_code=status.HTTP_200_OK)
async def optimize_mining_performance(
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Executa otimizações de performance de mineração.
    
    EVOLUÇÃO: Otimização automática de mineração paralela.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        # Executar otimizações de mineração
        result = blockchain.optimize_mining_performance()
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        # Executar limpezas adicionais em background
        background_tasks.add_task(blockchain_index.cleanup_expired_cache)
        background_tasks.add_task(transaction_pool.cleanup_expired_transactions)
        
        return {
            "success": True,
            "optimizations_applied": result["optimizations_applied"],
            "mining_config": result["mining_config"],
            "cache_cleanup": result["cache_cleanup"],
            "transaction_cleanup": result["transaction_cleanup"],
            "timestamp": result["timestamp"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na otimização de mineração: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/mining-config", status_code=status.HTTP_200_OK)
async def get_mining_config(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna configuração atual de mineração paralela.
    
    EVOLUÇÃO: Configuração de mineração paralela.
    """
    try:
        stats = parallel_miner.get_mining_statistics()
        
        return {
            "mining_config": {
                "max_threads": parallel_miner.config.max_threads,
                "max_processes": parallel_miner.config.max_processes,
                "batch_size": parallel_miner.config.batch_size,
                "timeout_seconds": parallel_miner.config.timeout_seconds,
                "cache_nonces": parallel_miner.config.cache_nonces,
                "cache_size": parallel_miner.config.cache_size,
                "adaptive_difficulty": parallel_miner.config.adaptive_difficulty
            },
            "mining_stats": stats,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter configuração de mineração: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/reset-mining-cache", status_code=status.HTTP_200_OK)
async def reset_mining_cache(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Reseta cache de nonces de mineração.
    
    EVOLUÇÃO: Reset de cache de mineração para otimização.
    """
    try:
        parallel_miner.nonce_cache.clear_cache()
        
        return {
            "success": True,
            "message": "Cache de mineração resetado com sucesso",
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro ao resetar cache de mineração: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/validation-statistics", status_code=status.HTTP_200_OK)
async def get_validation_statistics(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna estatísticas detalhadas de validação incremental.
    
    EVOLUÇÃO: Métricas de validação incremental e otimização.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        stats = blockchain.get_validation_statistics()
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao obter estatísticas de validação"
            )
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas de validação: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/optimize-validation", status_code=status.HTTP_200_OK)
async def optimize_validation_performance(
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Executa otimizações de performance de validação.
    
    EVOLUÇÃO: Otimização automática de validação incremental.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        # Executar otimizações de validação
        result = blockchain.optimize_validation_performance()
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        # Executar limpezas adicionais em background
        background_tasks.add_task(incremental_validator.cleanup_expired_cache)
        background_tasks.add_task(blockchain_index.cleanup_expired_cache)
        background_tasks.add_task(transaction_pool.cleanup_expired_transactions)
        
        return {
            "success": True,
            "optimizations_applied": result["optimizations_applied"],
            "validation_cache_cleanup": result["validation_cache_cleanup"],
            "mining_config": result["mining_config"],
            "cache_cleanup": result["cache_cleanup"],
            "transaction_cleanup": result["transaction_cleanup"],
            "timestamp": result["timestamp"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na otimização de validação: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/validation-config", status_code=status.HTTP_200_OK)
async def get_validation_config(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna configuração atual de validação incremental.
    
    EVOLUÇÃO: Configuração de validação incremental.
    """
    try:
        stats = incremental_validator.get_validation_statistics()
        
        return {
            "validation_config": {
                "max_workers": incremental_validator.max_workers,
                "cache_ttl": incremental_validator.validation_cache.ttl,
                "cache_sizes": stats["cache_sizes"]
            },
            "validation_stats": stats,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter configuração de validação: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/reset-validation-cache", status_code=status.HTTP_200_OK)
async def reset_validation_cache(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Reseta cache de validações.
    
    EVOLUÇÃO: Reset de cache de validação para otimização.
    """
    try:
        incremental_validator.clear_cache()
        
        return {
            "success": True,
            "message": "Cache de validação resetado com sucesso",
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro ao resetar cache de validação: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/validation-health-check", status_code=status.HTTP_200_OK)
async def validation_performance_health_check(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Verifica a saúde da performance de validação.
    
    EVOLUÇÃO: Health check específico para validação incremental.
    """
    try:
        # Obter estatísticas básicas
        validation_stats = incremental_validator.get_validation_statistics()
        
        # Verificar indicadores de saúde
        health_indicators = {
            "validation_cache_hit_rate_healthy": validation_stats["cache_hit_rate"] > 0.5,
            "average_validation_time_healthy": validation_stats["average_validation_time"] < 1.0,
            "total_validations_reasonable": validation_stats["total_validations"] > 0,
            "cache_sizes_reasonable": sum(validation_stats["cache_sizes"].values()) > 0
        }
        
        # Calcular score geral de saúde
        healthy_count = sum(health_indicators.values())
        total_count = len(health_indicators)
        health_score = healthy_count / total_count if total_count > 0 else 0
        
        # Determinar status geral
        if health_score >= 0.8:
            status = "healthy"
        elif health_score >= 0.6:
            status = "warning"
        else:
            status = "critical"
        
        return {
            "status": status,
            "health_score": health_score,
            "indicators": health_indicators,
            "recommendations": _get_validation_recommendations(health_indicators),
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro no health check de validação: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# ========== HELPER FUNCTIONS ==========

def _get_validation_recommendations(health_indicators: Dict[str, bool]) -> List[str]:
    """Gera recomendações baseadas nos indicadores de saúde de validação."""
    recommendations = []
    
    if not health_indicators["validation_cache_hit_rate_healthy"]:
        recommendations.append("Considere aumentar o TTL do cache de validação ou ajustar estratégia de cache")
    
    if not health_indicators["average_validation_time_healthy"]:
        recommendations.append("Otimize a validação incremental ou aumente o número de workers")
    
    if not health_indicators["total_validations_reasonable"]:
        recommendations.append("Verifique se as validações estão sendo executadas corretamente")
    
    if not health_indicators["cache_sizes_reasonable"]:
        recommendations.append("Verifique se o cache de validação está sendo populado corretamente")
    
    return recommendations

@router.get("/tree-statistics", status_code=status.HTTP_200_OK)
async def get_tree_statistics(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna estatísticas detalhadas da estrutura de árvore.
    
    EVOLUÇÃO: Métricas de estrutura de árvore e otimização.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        stats = blockchain.get_tree_statistics()
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao obter estatísticas da árvore"
            )
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas da árvore: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/optimize-tree", status_code=status.HTTP_200_OK)
async def optimize_tree_structure(
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Executa otimizações de estrutura de árvore.
    
    EVOLUÇÃO: Otimização automática de estrutura de árvore.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        # Executar otimizações de estrutura de árvore
        result = blockchain.optimize_tree_structure()
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        # Executar limpezas adicionais em background
        background_tasks.add_task(blockchain_tree.clear_cache)
        background_tasks.add_task(incremental_validator.cleanup_expired_cache)
        background_tasks.add_task(blockchain_index.cleanup_expired_cache)
        background_tasks.add_task(transaction_pool.cleanup_expired_transactions)
        
        return {
            "success": True,
            "optimizations_applied": result["optimizations_applied"],
            "tree_optimization": result["tree_optimization"],
            "validation_cache_cleanup": result["validation_cache_cleanup"],
            "mining_config": result["mining_config"],
            "cache_cleanup": result["cache_cleanup"],
            "transaction_cleanup": result["transaction_cleanup"],
            "timestamp": result["timestamp"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na otimização da estrutura de árvore: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/tree-config", status_code=status.HTTP_200_OK)
async def get_tree_config(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna configuração atual da estrutura de árvore.
    
    EVOLUÇÃO: Configuração de estrutura de árvore.
    """
    try:
        stats = blockchain_tree.get_tree_statistics()
        
        return {
            "tree_config": {
                "max_cache_size": blockchain_tree.max_cache_size,
                "cache_size": stats["cache_stats"]["cache_size"],
                "max_cache_size": stats["cache_stats"]["max_cache_size"]
            },
            "tree_stats": stats,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter configuração da árvore: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/reset-tree-cache", status_code=status.HTTP_200_OK)
async def reset_tree_cache(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Reseta cache da estrutura de árvore.
    
    EVOLUÇÃO: Reset de cache da árvore para otimização.
    """
    try:
        blockchain_tree.clear_cache()
        
        return {
            "success": True,
            "message": "Cache da estrutura de árvore resetado com sucesso",
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro ao resetar cache da árvore: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/tree-health-check", status_code=status.HTTP_200_OK)
async def tree_structure_health_check(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Verifica a saúde da estrutura de árvore.
    
    EVOLUÇÃO: Health check específico para estrutura de árvore.
    """
    try:
        # Obter estatísticas básicas
        tree_stats = blockchain_tree.get_tree_statistics()
        
        # Verificar indicadores de saúde
        health_indicators = {
            "tree_cache_hit_rate_healthy": tree_stats["cache_stats"]["cache_hit_rate"] > 0.5,
            "tree_structure_balanced": tree_stats["tree_stats"]["max_depth"] - tree_stats["tree_stats"]["average_depth"] < 10,
            "tree_nodes_reasonable": tree_stats["tree_stats"]["total_nodes"] > 0,
            "tree_cache_size_reasonable": tree_stats["cache_stats"]["cache_size"] > 0
        }
        
        # Calcular score geral de saúde
        healthy_count = sum(health_indicators.values())
        total_count = len(health_indicators)
        health_score = healthy_count / total_count if total_count > 0 else 0
        
        # Determinar status geral
        if health_score >= 0.8:
            status = "healthy"
        elif health_score >= 0.6:
            status = "warning"
        else:
            status = "critical"
        
        return {
            "status": status,
            "health_score": health_score,
            "indicators": health_indicators,
            "recommendations": _get_tree_recommendations(health_indicators),
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro no health check da estrutura de árvore: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/blockchain-path/{from_hash}/{to_hash}", status_code=status.HTTP_200_OK)
async def get_blockchain_path(
    from_hash: str,
    to_hash: str,
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna caminho entre dois blocos na blockchain.
    
    EVOLUÇÃO: Caminho otimizado usando estrutura de árvore.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        path = blockchain.get_blockchain_path(from_hash, to_hash)
        
        return {
            "path": [block.hash.value for block in path],
            "path_length": len(path),
            "from_hash": from_hash,
            "to_hash": to_hash,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter caminho da blockchain: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/subtree-blocks/{root_hash}", status_code=status.HTTP_200_OK)
async def get_subtree_blocks(
    root_hash: str,
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna todos os blocos de uma subárvore.
    
    EVOLUÇÃO: Subárvore otimizada com cache.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        blocks = blockchain.get_subtree_blocks(root_hash)
        
        return {
            "blocks": [block.hash.value for block in blocks],
            "block_count": len(blocks),
            "root_hash": root_hash,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter subárvore: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/validate-subtree/{root_hash}", status_code=status.HTTP_200_OK)
async def validate_subtree(
    root_hash: str,
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Valida uma subárvore incrementalmente.
    
    EVOLUÇÃO: Validação incremental de subárvores.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        result = blockchain.validate_subtree(root_hash)
        
        return {
            "valid": result["valid"],
            "validation_time": result.get("validation_time", 0),
            "subtree_size": result.get("subtree_size", 0),
            "nodes_validated": result.get("nodes_validated", 0),
            "root_hash": root_hash,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro na validação de subárvore: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

def _get_tree_recommendations(health_indicators: Dict[str, bool]) -> List[str]:
    """Gera recomendações baseadas nos indicadores de saúde da estrutura de árvore."""
    recommendations = []
    
    if not health_indicators["tree_cache_hit_rate_healthy"]:
        recommendations.append("Considere aumentar o tamanho do cache da árvore ou ajustar estratégia de cache")
    
    if not health_indicators["tree_structure_balanced"]:
        recommendations.append("A árvore pode precisar de rebalanceamento para melhor performance")
    
    if not health_indicators["tree_nodes_reasonable"]:
        recommendations.append("Verifique se os blocos estão sendo inseridos corretamente na árvore")
    
    if not health_indicators["tree_cache_size_reasonable"]:
        recommendations.append("Verifique se o cache da árvore está sendo populado corretamente")
    
    return recommendations

@router.get("/distributed-cache-statistics", status_code=status.HTTP_200_OK)
async def get_distributed_cache_statistics(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna estatísticas detalhadas do cache distribuído.
    
    EVOLUÇÃO: Métricas de cache distribuído e sincronização.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        stats = blockchain.get_distributed_cache_statistics()
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao obter estatísticas do cache distribuído"
            )
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas do cache distribuído: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/network-statistics", status_code=status.HTTP_200_OK)
async def get_network_statistics(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna estatísticas detalhadas da rede.
    
    EVOLUÇÃO: Métricas de rede e otimização.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        stats = blockchain.get_network_statistics()
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao obter estatísticas da rede"
            )
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas da rede: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/optimize-distributed-systems", status_code=status.HTTP_200_OK)
async def optimize_distributed_systems(
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Executa otimizações de sistemas distribuídos.
    
    EVOLUÇÃO: Otimização automática de cache distribuído e rede.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        # Executar otimizações de sistemas distribuídos
        result = blockchain.optimize_distributed_systems()
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        # Executar limpezas adicionais em background
        background_tasks.add_task(distributed_cache.sync_all)
        background_tasks.add_task(network_optimizer.optimize_network)
        background_tasks.add_task(blockchain_tree.clear_cache)
        background_tasks.add_task(incremental_validator.cleanup_expired_cache)
        
        return {
            "success": True,
            "optimizations_applied": result["optimizations_applied"],
            "cache_optimization": result["cache_optimization"],
            "network_optimization": result["network_optimization"],
            "tree_optimization": result["tree_optimization"],
            "validation_cache_cleanup": result["validation_cache_cleanup"],
            "mining_config": result["mining_config"],
            "cache_cleanup": result["cache_cleanup"],
            "transaction_cleanup": result["transaction_cleanup"],
            "timestamp": result["timestamp"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na otimização de sistemas distribuídos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/sync-with-network", status_code=status.HTTP_200_OK)
async def sync_with_network(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Sincroniza blockchain com a rede.
    
    EVOLUÇÃO: Sincronização inteligente com outros nós.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        # Executar sincronização com a rede
        result = blockchain.sync_with_network()
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        return {
            "success": True,
            "cache_sync": result["cache_sync"],
            "network_broadcast": result["network_broadcast"],
            "timestamp": result["timestamp"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na sincronização com a rede: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/add-network-node", status_code=status.HTTP_200_OK)
async def add_network_node(
    node_id: str,
    address: str,
    port: int,
    priority: int = 1,
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Adiciona um nó à rede blockchain.
    
    EVOLUÇÃO: Adição de nós com prioridade e configuração.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        # Adicionar nó à rede
        success = blockchain.add_network_node(node_id, address, port, priority)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao adicionar nó à rede"
            )
        
        return {
            "success": True,
            "node_id": node_id,
            "address": address,
            "port": port,
            "priority": priority,
            "timestamp": time.time()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao adicionar nó à rede: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.delete("/remove-network-node/{node_id}", status_code=status.HTTP_200_OK)
async def remove_network_node(
    node_id: str,
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Remove um nó da rede blockchain.
    
    EVOLUÇÃO: Remoção de nós com limpeza de recursos.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        # Remover nó da rede
        success = blockchain.remove_network_node(node_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao remover nó da rede"
            )
        
        return {
            "success": True,
            "node_id": node_id,
            "timestamp": time.time()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao remover nó da rede: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/distributed-cache-health-check", status_code=status.HTTP_200_OK)
async def distributed_cache_health_check(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Verifica a saúde do cache distribuído.
    
    EVOLUÇÃO: Health check específico para cache distribuído.
    """
    try:
        # Obter estatísticas básicas
        cache_stats = distributed_cache.get_statistics()
        
        # Verificar indicadores de saúde
        health_indicators = {
            "cache_hit_rate_healthy": cache_stats["cache_stats"]["hit_rate"] > 0.5,
            "local_cache_size_reasonable": cache_stats["cache_stats"]["local_cache_size"] > 0,
            "cluster_nodes_active": cache_stats["cluster_stats"]["active_nodes"] > 0,
            "sync_operations_reasonable": cache_stats["sync_stats"]["sync_operations"] > 0
        }
        
        # Calcular score geral de saúde
        healthy_count = sum(health_indicators.values())
        total_count = len(health_indicators)
        health_score = healthy_count / total_count if total_count > 0 else 0
        
        # Determinar status geral
        if health_score >= 0.8:
            status = "healthy"
        elif health_score >= 0.6:
            status = "warning"
        else:
            status = "critical"
        
        return {
            "status": status,
            "health_score": health_score,
            "indicators": health_indicators,
            "recommendations": _get_distributed_cache_recommendations(health_indicators),
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro no health check do cache distribuído: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/network-health-check", status_code=status.HTTP_200_OK)
async def network_health_check(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Verifica a saúde da rede.
    
    EVOLUÇÃO: Health check específico para rede.
    """
    try:
        # Obter estatísticas básicas
        network_stats = network_optimizer.get_network_statistics()
        
        # Verificar indicadores de saúde
        health_indicators = {
            "network_nodes_active": network_stats["network_stats"]["active_nodes"] > 0,
            "connection_pools_healthy": network_stats["network_stats"]["total_connections"] > 0,
            "message_cache_hit_rate_healthy": network_stats["cache_stats"]["cache_hit_rate"] > 0.5,
            "compression_savings_reasonable": network_stats["message_stats"]["compression_savings"] > 0.1
        }
        
        # Calcular score geral de saúde
        healthy_count = sum(health_indicators.values())
        total_count = len(health_indicators)
        health_score = healthy_count / total_count if total_count > 0 else 0
        
        # Determinar status geral
        if health_score >= 0.8:
            status = "healthy"
        elif health_score >= 0.6:
            status = "warning"
        else:
            status = "critical"
        
        return {
            "status": status,
            "health_score": health_score,
            "indicators": health_indicators,
            "recommendations": _get_network_recommendations(health_indicators),
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro no health check da rede: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

def _get_distributed_cache_recommendations(health_indicators: Dict[str, bool]) -> List[str]:
    """Gera recomendações baseadas nos indicadores de saúde do cache distribuído."""
    recommendations = []
    
    if not health_indicators["cache_hit_rate_healthy"]:
        recommendations.append("Considere aumentar o TTL do cache distribuído ou ajustar estratégia de cache")
    
    if not health_indicators["local_cache_size_reasonable"]:
        recommendations.append("Verifique se o cache local está sendo populado corretamente")
    
    if not health_indicators["cluster_nodes_active"]:
        recommendations.append("Verifique se há nós ativos no cluster de cache")
    
    if not health_indicators["sync_operations_reasonable"]:
        recommendations.append("Verifique se as operações de sincronização estão sendo executadas")
    
    return recommendations

def _get_network_recommendations(health_indicators: Dict[str, bool]) -> List[str]:
    """Gera recomendações baseadas nos indicadores de saúde da rede."""
    recommendations = []
    
    if not health_indicators["network_nodes_active"]:
        recommendations.append("Verifique se há nós ativos na rede")
    
    if not health_indicators["connection_pools_healthy"]:
        recommendations.append("Verifique se os pools de conexão estão funcionando corretamente")
    
    if not health_indicators["message_cache_hit_rate_healthy"]:
        recommendations.append("Considere otimizar o cache de mensagens da rede")
    
    if not health_indicators["compression_savings_reasonable"]:
        recommendations.append("Considere ajustar as configurações de compressão da rede")
    
    return recommendations

@router.get("/scaling-statistics", status_code=status.HTTP_200_OK)
async def get_scaling_statistics(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna estatísticas detalhadas de escalabilidade horizontal.
    
    EVOLUÇÃO: Métricas de escalabilidade horizontal e sharding.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        stats = blockchain.get_scaling_statistics()
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao obter estatísticas de escalabilidade"
            )
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas de escalabilidade: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/monitoring-statistics", status_code=status.HTTP_200_OK)
async def get_monitoring_statistics(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Retorna estatísticas detalhadas de monitoramento em tempo real.
    
    EVOLUÇÃO: Métricas de monitoramento em tempo real e alertas.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        stats = blockchain.get_monitoring_statistics()
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao obter estatísticas de monitoramento"
            )
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas de monitoramento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/optimize-enterprise-systems", status_code=status.HTTP_200_OK)
async def optimize_enterprise_systems(
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Executa otimizações de sistemas enterprise.
    
    EVOLUÇÃO: Otimização automática de todos os sistemas enterprise.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        # Executar otimizações de sistemas enterprise
        result = blockchain.optimize_enterprise_systems()
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        # Executar limpezas adicionais em background
        background_tasks.add_task(real_time_monitor.optimize_monitoring)
        background_tasks.add_task(horizontal_scaler.optimize_scaling)
        background_tasks.add_task(distributed_cache.sync_all)
        background_tasks.add_task(network_optimizer.optimize_network)
        background_tasks.add_task(blockchain_tree.clear_cache)
        background_tasks.add_task(incremental_validator.cleanup_expired_cache)
        
        return {
            "success": True,
            "optimizations_applied": result["optimizations_applied"],
            "monitoring_optimization": result["monitoring_optimization"],
            "scaling_optimization": result["scaling_optimization"],
            "cache_optimization": result["cache_optimization"],
            "network_optimization": result["network_optimization"],
            "tree_optimization": result["tree_optimization"],
            "validation_cache_cleanup": result["validation_cache_cleanup"],
            "mining_config": result["mining_config"],
            "cache_cleanup": result["cache_cleanup"],
            "transaction_cleanup": result["transaction_cleanup"],
            "timestamp": result["timestamp"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na otimização de sistemas enterprise: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/create-shard", status_code=status.HTTP_200_OK)
async def create_shard(
    shard_id: str,
    node_count: int = 3,
    replication_factor: int = 2,
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Cria um novo shard para escalabilidade horizontal.
    
    EVOLUÇÃO: Criação de shards com configuração personalizada.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        # Criar shard
        success = blockchain.create_shard(shard_id, node_count, replication_factor)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar shard"
            )
        
        return {
            "success": True,
            "shard_id": shard_id,
            "node_count": node_count,
            "replication_factor": replication_factor,
            "timestamp": time.time()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar shard {shard_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/add-node-to-shard", status_code=status.HTTP_200_OK)
async def add_node_to_shard(
    shard_id: str,
    node_id: str,
    address: str,
    port: int,
    priority: int = 1,
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Adiciona um nó a um shard.
    
    EVOLUÇÃO: Adição de nós com prioridade e configuração.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        # Adicionar nó ao shard
        success = blockchain.add_node_to_shard(shard_id, node_id, address, port, priority)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao adicionar nó ao shard"
            )
        
        return {
            "success": True,
            "shard_id": shard_id,
            "node_id": node_id,
            "address": address,
            "port": port,
            "priority": priority,
            "timestamp": time.time()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao adicionar nó {node_id} ao shard {shard_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/create-alert-rule", status_code=status.HTTP_200_OK)
async def create_alert_rule(
    rule_id: str,
    name: str,
    metric_name: str,
    condition: str,
    threshold: float,
    level: str = "warning",
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Cria uma regra de alerta para monitoramento.
    
    EVOLUÇÃO: Criação de regras de alerta com condições personalizadas.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        # Criar regra de alerta
        success = blockchain.create_alert_rule(rule_id, name, metric_name, condition, threshold, level)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar regra de alerta"
            )
        
        return {
            "success": True,
            "rule_id": rule_id,
            "name": name,
            "metric_name": metric_name,
            "condition": condition,
            "threshold": threshold,
            "level": level,
            "timestamp": time.time()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar regra de alerta {rule_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/active-alerts", status_code=status.HTTP_200_OK)
async def get_active_alerts(
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:read"))
):
    """
    Obtém alertas ativos do monitoramento.
    
    EVOLUÇÃO: Lista de alertas ativos com informações detalhadas.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        alerts = blockchain.get_active_alerts()
        
        return {
            "success": True,
            "alerts": alerts,
            "total_alerts": len(alerts),
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter alertas ativos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/resolve-alert/{alert_id}", status_code=status.HTTP_200_OK)
async def resolve_alert(
    alert_id: str,
    current_user: AuthenticatedUser = Depends(require_scope("blockchain:admin"))
):
    """
    Resolve um alerta.
    
    EVOLUÇÃO: Resolução de alertas com timestamp.
    """
    try:
        # Em uma implementação real, isso viria de uma instância singleton da blockchain
        blockchain = Blockchain.create()
        
        # Resolver alerta
        success = blockchain.resolve_alert(alert_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao resolver alerta"
            )
        
        return {
            "success": True,
            "alert_id": alert_id,
            "timestamp": time.time()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao resolver alerta {alert_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/scaling-health-check", status_code=status.HTTP_200_OK)
async def scaling_health_check(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Verifica a saúde da escalabilidade horizontal.
    
    EVOLUÇÃO: Health check específico para escalabilidade horizontal.
    """
    try:
        # Obter estatísticas básicas
        scaling_stats = horizontal_scaler.get_scaling_statistics()
        
        # Verificar indicadores de saúde
        health_indicators = {
            "shards_active": scaling_stats["scaling_stats"]["total_shards"] > 0,
            "nodes_active": scaling_stats["scaling_stats"]["active_nodes"] > 0,
            "load_distributed": len(scaling_stats["load_distribution"]) > 0,
            "throughput_reasonable": scaling_stats["scaling_stats"]["throughput_per_second"] > 0
        }
        
        # Calcular score geral de saúde
        healthy_count = sum(health_indicators.values())
        total_count = len(health_indicators)
        health_score = healthy_count / total_count if total_count > 0 else 0
        
        # Determinar status geral
        if health_score >= 0.8:
            status = "healthy"
        elif health_score >= 0.6:
            status = "warning"
        else:
            status = "critical"
        
        return {
            "status": status,
            "health_score": health_score,
            "indicators": health_indicators,
            "recommendations": _get_scaling_recommendations(health_indicators),
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro no health check de escalabilidade: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/monitoring-health-check", status_code=status.HTTP_200_OK)
async def monitoring_health_check(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Verifica a saúde do monitoramento em tempo real.
    
    EVOLUÇÃO: Health check específico para monitoramento em tempo real.
    """
    try:
        # Obter estatísticas básicas
        monitoring_stats = real_time_monitor.get_monitoring_statistics()
        
        # Verificar indicadores de saúde
        health_indicators = {
            "metrics_collected": monitoring_stats["monitoring_stats"]["total_metrics_collected"] > 0,
            "alert_rules_active": monitoring_stats["alert_stats"]["active_alert_rules"] > 0,
            "collection_rate_reasonable": monitoring_stats["monitoring_stats"]["metric_collection_rate"] > 0,
            "response_time_reasonable": monitoring_stats["monitoring_stats"]["alert_response_time"] < 300
        }
        
        # Calcular score geral de saúde
        healthy_count = sum(health_indicators.values())
        total_count = len(health_indicators)
        health_score = healthy_count / total_count if total_count > 0 else 0
        
        # Determinar status geral
        if health_score >= 0.8:
            status = "healthy"
        elif health_score >= 0.6:
            status = "warning"
        else:
            status = "critical"
        
        return {
            "status": status,
            "health_score": health_score,
            "indicators": health_indicators,
            "recommendations": _get_monitoring_recommendations(health_indicators),
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Erro no health check de monitoramento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

def _get_scaling_recommendations(health_indicators: Dict[str, bool]) -> List[str]:
    """Gera recomendações baseadas nos indicadores de saúde de escalabilidade."""
    recommendations = []
    
    if not health_indicators["shards_active"]:
        recommendations.append("Considere criar shards para melhor distribuição de carga")
    
    if not health_indicators["nodes_active"]:
        recommendations.append("Verifique se há nós ativos nos shards")
    
    if not health_indicators["load_distributed"]:
        recommendations.append("Verifique se a carga está sendo distribuída entre shards")
    
    if not health_indicators["throughput_reasonable"]:
        recommendations.append("Verifique se o throughput está sendo medido corretamente")
    
    return recommendations

def _get_monitoring_recommendations(health_indicators: Dict[str, bool]) -> List[str]:
    """Gera recomendações baseadas nos indicadores de saúde de monitoramento."""
    recommendations = []
    
    if not health_indicators["metrics_collected"]:
        recommendations.append("Verifique se as métricas estão sendo coletadas corretamente")
    
    if not health_indicators["alert_rules_active"]:
        recommendations.append("Considere criar regras de alerta para monitoramento")
    
    if not health_indicators["collection_rate_reasonable"]:
        recommendations.append("Verifique se a taxa de coleta de métricas está adequada")
    
    if not health_indicators["response_time_reasonable"]:
        recommendations.append("Verifique se o tempo de resposta dos alertas está adequado")
    
    return recommendations
