"""
Improvement Router - Roteador para Melhorias e Otimizações
Baseado na análise holística do CoinBalance
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List
import logging
from pydantic import BaseModel

from src.infrastructure.optimization.performance_optimizer import (
    performance_optimizer, 
    OptimizationLevel
)
from src.infrastructure.consistency.consistency_checker import (
    consistency_checker,
    ConsistencyLevel
)
from src.infrastructure.fixing.critical_fixer import (
    critical_fixer,
    FixPriority
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/improvements", tags=["Improvements"])


# Schemas Pydantic
class OptimizationRequest(BaseModel):
    level: str = "medium"
    enable_monitoring: bool = True


class ConsistencyCheckRequest(BaseModel):
    run_checks: bool = True
    auto_fix: bool = False


class CriticalFixRequest(BaseModel):
    priority: str = "immediate"
    auto_apply: bool = True


class ImprovementStatus(BaseModel):
    performance: Dict[str, Any]
    consistency: Dict[str, Any]
    critical_fixes: Dict[str, Any]


# Endpoints de Performance
@router.post("/performance/start")
async def start_performance_optimization(request: OptimizationRequest):
    """Inicia otimização de performance"""
    try:
        level = OptimizationLevel(request.level)
        performance_optimizer.set_optimization_level(level)
        
        if request.enable_monitoring:
            # Iniciar monitoramento em background
            import asyncio
            asyncio.create_task(performance_optimizer.start_monitoring())
        
        return {
            "status": "success",
            "message": "Otimização de performance iniciada",
            "level": level.value,
            "monitoring": request.enable_monitoring
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Nível de otimização inválido")
    except Exception as e:
        logger.error(f"Erro ao iniciar otimização de performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/performance/stop")
async def stop_performance_optimization():
    """Para otimização de performance"""
    try:
        await performance_optimizer.stop_monitoring()
        
        return {
            "status": "success",
            "message": "Otimização de performance parada"
        }
        
    except Exception as e:
        logger.error(f"Erro ao parar otimização de performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance/report")
async def get_performance_report():
    """Obtém relatório de performance"""
    try:
        report = performance_optimizer.get_performance_report()
        return report
        
    except Exception as e:
        logger.error(f"Erro ao obter relatório de performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints de Consistência
@router.post("/consistency/start")
async def start_consistency_checking(request: ConsistencyCheckRequest):
    """Inicia verificação de consistência"""
    try:
        if request.run_checks:
            # Iniciar verificação em background
            import asyncio
            asyncio.create_task(consistency_checker.start_consistency_monitoring())
        
        if request.auto_fix:
            # Aplicar correções automáticas
            await consistency_checker.auto_fix_issues()
        
        return {
            "status": "success",
            "message": "Verificação de consistência iniciada",
            "auto_fix": request.auto_fix
        }
        
    except Exception as e:
        logger.error(f"Erro ao iniciar verificação de consistência: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/consistency/stop")
async def stop_consistency_checking():
    """Para verificação de consistência"""
    try:
        await consistency_checker.stop_consistency_monitoring()
        
        return {
            "status": "success",
            "message": "Verificação de consistência parada"
        }
        
    except Exception as e:
        logger.error(f"Erro ao parar verificação de consistência: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/consistency/report")
async def get_consistency_report():
    """Obtém relatório de consistência"""
    try:
        report = consistency_checker.get_consistency_report()
        return report
        
    except Exception as e:
        logger.error(f"Erro ao obter relatório de consistência: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/consistency/fix")
async def fix_consistency_issues():
    """Corrige problemas de consistência automaticamente"""
    try:
        await consistency_checker.auto_fix_issues()
        
        return {
            "status": "success",
            "message": "Correções de consistência aplicadas"
        }
        
    except Exception as e:
        logger.error(f"Erro ao corrigir problemas de consistência: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints de Correções Críticas
@router.post("/critical-fixes/run")
async def run_critical_fixes(request: CriticalFixRequest):
    """Executa correções críticas"""
    try:
        # Executar correções em background
        import asyncio
        asyncio.create_task(critical_fixer.start_auto_fixing())
        
        return {
            "status": "success",
            "message": "Correções críticas iniciadas",
            "auto_apply": request.auto_apply
        }
        
    except Exception as e:
        logger.error(f"Erro ao executar correções críticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/critical-fixes/report")
async def get_critical_fixes_report():
    """Obtém relatório de correções críticas"""
    try:
        report = critical_fixer.get_fixing_report()
        return report
        
    except Exception as e:
        logger.error(f"Erro ao obter relatório de correções críticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint Principal de Status
@router.get("/status")
async def get_improvement_status():
    """Obtém status geral das melhorias"""
    try:
        performance_report = performance_optimizer.get_performance_report()
        consistency_report = consistency_checker.get_consistency_report()
        critical_fixes_report = critical_fixer.get_fixing_report()
        
        return ImprovementStatus(
            performance=performance_report,
            consistency=consistency_report,
            critical_fixes=critical_fixes_report
        )
        
    except Exception as e:
        logger.error(f"Erro ao obter status das melhorias: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint de Análise Holística
@router.get("/holistic-analysis")
async def get_holistic_analysis():
    """Obtém análise holística do sistema"""
    try:
        # Coletar dados de todos os sistemas
        performance_data = performance_optimizer.get_performance_report()
        consistency_data = consistency_checker.get_consistency_report()
        critical_fixes_data = critical_fixer.get_fixing_report()
        
        # Análise holística
        analysis = {
            "timestamp": __import__('time').time(),
            "system_health": "healthy",
            "performance": {
                "status": performance_data.get("status", "unknown"),
                "optimization_level": performance_data.get("optimization_level", "medium"),
                "active_rules": performance_data.get("active_rules", 0)
            },
            "consistency": {
                "status": consistency_data.get("status", "unknown"),
                "total_issues": consistency_data.get("total_issues", 0),
                "critical_issues": consistency_data.get("critical_issues", 0),
                "fixed_issues": consistency_data.get("fixed_issues", 0)
            },
            "critical_fixes": {
                "total_fixes": critical_fixes_data.get("total_fixes", 0),
                "applied_fixes": critical_fixes_data.get("applied_fixes", 0),
                "pending_fixes": critical_fixes_data.get("pending_fixes", 0)
            },
            "recommendations": []
        }
        
        # Gerar recomendações baseadas na análise
        if consistency_data.get("critical_issues", 0) > 0:
            analysis["recommendations"].append({
                "type": "critical",
                "message": "Corrigir problemas críticos de consistência",
                "action": "POST /api/v1/improvements/consistency/fix"
            })
        
        if performance_data.get("status") == "no_data":
            analysis["recommendations"].append({
                "type": "performance",
                "message": "Iniciar monitoramento de performance",
                "action": "POST /api/v1/improvements/performance/start"
            })
        
        if critical_fixes_data.get("pending_fixes", 0) > 0:
            analysis["recommendations"].append({
                "type": "fixes",
                "message": "Aplicar correções críticas pendentes",
                "action": "POST /api/v1/improvements/critical-fixes/run"
            })
        
        # Determinar saúde geral do sistema
        if (consistency_data.get("critical_issues", 0) > 0 or 
            critical_fixes_data.get("pending_fixes", 0) > 0):
            analysis["system_health"] = "needs_attention"
        elif consistency_data.get("high_issues", 0) > 2:
            analysis["system_health"] = "warning"
        
        return analysis
        
    except Exception as e:
        logger.error(f"Erro ao obter análise holística: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint de Execução Completa de Melhorias
@router.post("/execute-all")
async def execute_all_improvements(background_tasks: BackgroundTasks):
    """Executa todas as melhorias automaticamente"""
    try:
        # Executar todas as melhorias em background
        background_tasks.add_task(performance_optimizer.start_monitoring)
        background_tasks.add_task(consistency_checker.start_consistency_monitoring)
        background_tasks.add_task(critical_fixer.start_auto_fixing)
        
        return {
            "status": "success",
            "message": "Todas as melhorias foram iniciadas em background",
            "improvements": [
                "Performance optimization",
                "Consistency checking",
                "Critical fixes"
            ]
        }
        
    except Exception as e:
        logger.error(f"Erro ao executar todas as melhorias: {e}")
        raise HTTPException(status_code=500, detail=str(e))
