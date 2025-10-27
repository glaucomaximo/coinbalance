"""
Dashboard de Monitoramento para CoinBalance
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List
import time
import psutil
import os
from datetime import datetime, timedelta

from src.infrastructure.persistence.database_manager import DatabaseManager
from src.domain.transaction.services.transaction_history_service import TransactionHistoryService

router = APIRouter(prefix="/dashboard", tags=["Dashboard de Monitoramento"])

class SystemMetrics:
    """Métricas do sistema"""
    
    @staticmethod
    def get_cpu_usage() -> float:
        """Obtém uso de CPU"""
        return psutil.cpu_percent(interval=1)
    
    @staticmethod
    def get_memory_usage() -> Dict[str, Any]:
        """Obtém uso de memória"""
        memory = psutil.virtual_memory()
        return {
            "total_mb": round(memory.total / 1024 / 1024, 2),
            "available_mb": round(memory.available / 1024 / 1024, 2),
            "used_mb": round(memory.used / 1024 / 1024, 2),
            "percentage": memory.percent
        }
    
    @staticmethod
    def get_disk_usage() -> Dict[str, Any]:
        """Obtém uso de disco"""
        disk = psutil.disk_usage('/')
        return {
            "total_gb": round(disk.total / 1024 / 1024 / 1024, 2),
            "used_gb": round(disk.used / 1024 / 1024 / 1024, 2),
            "free_gb": round(disk.free / 1024 / 1024 / 1024, 2),
            "percentage": round((disk.used / disk.total) * 100, 2)
        }
    
    @staticmethod
    def get_process_info() -> Dict[str, Any]:
        """Obtém informações do processo"""
        process = psutil.Process(os.getpid())
        return {
            "pid": process.pid,
            "cpu_percent": process.cpu_percent(),
            "memory_mb": round(process.memory_info().rss / 1024 / 1024, 2),
            "num_threads": process.num_threads(),
            "create_time": datetime.fromtimestamp(process.create_time()).isoformat()
        }

class DatabaseMetrics:
    """Métricas do banco de dados"""
    
    @staticmethod
    def get_database_stats() -> Dict[str, Any]:
        """Obtém estatísticas do banco de dados"""
        try:
            db_manager = DatabaseManager()
            
            # Estatísticas de carteiras
            wallet_stats = db_manager.execute_query("SELECT COUNT(*) as total FROM wallets")
            wallet_count = wallet_stats[0]["total"] if wallet_stats else 0
            
            # Estatísticas de transações
            history_service = TransactionHistoryService(db_manager)
            transaction_stats = history_service.get_transaction_stats(days=30)
            
            # Tamanho do banco
            db_file = "blockchain.db"
            db_size = 0
            if os.path.exists(db_file):
                db_size = os.path.getsize(db_file)
            
            return {
                "wallet_count": wallet_count,
                "transaction_stats": transaction_stats,
                "database_size_mb": round(db_size / 1024 / 1024, 2),
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "error": str(e),
                "last_updated": datetime.now().isoformat()
            }

class ApplicationMetrics:
    """Métricas da aplicação"""
    
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
    
    def get_uptime(self) -> Dict[str, Any]:
        """Obtém tempo de atividade"""
        uptime_seconds = time.time() - self.start_time
        uptime_delta = timedelta(seconds=uptime_seconds)
        
        return {
            "uptime_seconds": uptime_seconds,
            "uptime_human": str(uptime_delta),
            "start_time": datetime.fromtimestamp(self.start_time).isoformat()
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Obtém métricas de performance"""
        return {
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": round((self.error_count / max(self.request_count, 1)) * 100, 2),
            "avg_response_time_ms": 0,  # Implementar se necessário
            "last_updated": datetime.now().isoformat()
        }

# Instância global das métricas
app_metrics = ApplicationMetrics()

@router.get(
    "/overview",
    response_model=dict,
    summary="Visão Geral do Sistema",
    description="Obtém uma visão geral do estado do sistema"
)
async def get_system_overview() -> dict:
    """
    Obtém uma visão geral do estado do sistema.
    
    Inclui métricas de sistema, banco de dados e aplicação.
    """
    try:
        # Métricas do sistema
        system_metrics = {
            "cpu_usage_percent": SystemMetrics.get_cpu_usage(),
            "memory": SystemMetrics.get_memory_usage(),
            "disk": SystemMetrics.get_disk_usage(),
            "process": SystemMetrics.get_process_info()
        }
        
        # Métricas do banco de dados
        database_metrics = DatabaseMetrics.get_database_stats()
        
        # Métricas da aplicação
        app_metrics_data = {
            "uptime": app_metrics.get_uptime(),
            "performance": app_metrics.get_performance_metrics()
        }
        
        # Status geral
        overall_status = "healthy"
        if system_metrics["cpu_usage_percent"] > 80:
            overall_status = "warning"
        if system_metrics["memory"]["percentage"] > 90:
            overall_status = "critical"
        
        return {
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "system": system_metrics,
            "database": database_metrics,
            "application": app_metrics_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"Failed to get system overview: {str(e)}", "code": "METRICS_ERROR"}
        )

@router.get(
    "/system",
    response_model=dict,
    summary="Métricas do Sistema",
    description="Obtém métricas detalhadas do sistema"
)
async def get_system_metrics() -> dict:
    """
    Obtém métricas detalhadas do sistema.
    
    Inclui CPU, memória, disco e informações do processo.
    """
    try:
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "usage_percent": SystemMetrics.get_cpu_usage(),
                "count": psutil.cpu_count(),
                "frequency": psutil.cpu_freq().current if psutil.cpu_freq() else None
            },
            "memory": SystemMetrics.get_memory_usage(),
            "disk": SystemMetrics.get_disk_usage(),
            "process": SystemMetrics.get_process_info(),
            "network": {
                "connections": len(psutil.net_connections()),
                "io": psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {}
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"Failed to get system metrics: {str(e)}", "code": "SYSTEM_METRICS_ERROR"}
        )

@router.get(
    "/database",
    response_model=dict,
    summary="Métricas do Banco de Dados",
    description="Obtém métricas detalhadas do banco de dados"
)
async def get_database_metrics() -> dict:
    """
    Obtém métricas detalhadas do banco de dados.
    
    Inclui estatísticas de carteiras, transações e tamanho do banco.
    """
    try:
        db_manager = DatabaseManager()
        history_service = TransactionHistoryService(db_manager)
        
        # Estatísticas detalhadas
        wallet_stats = db_manager.execute_query("SELECT COUNT(*) as total FROM wallets")
        wallet_count = wallet_stats[0]["total"] if wallet_stats else 0
        
        # Estatísticas de transações por período
        stats_1d = history_service.get_transaction_stats(days=1)
        stats_7d = history_service.get_transaction_stats(days=7)
        stats_30d = history_service.get_transaction_stats(days=30)
        
        # Transações recentes
        recent_transactions = history_service.get_recent_transactions(limit=10)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "wallets": {
                "total_count": wallet_count
            },
            "transactions": {
                "last_1_day": stats_1d,
                "last_7_days": stats_7d,
                "last_30_days": stats_30d
            },
            "recent_activity": [
                {
                    "id": tx.id,
                    "type": tx.type.value,
                    "amount": float(tx.amount),
                    "created_at": tx.created_at
                }
                for tx in recent_transactions
            ],
            "database": {
                "size_mb": DatabaseMetrics.get_database_stats().get("database_size_mb", 0),
                "file_exists": os.path.exists("blockchain.db")
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"Failed to get database metrics: {str(e)}", "code": "DATABASE_METRICS_ERROR"}
        )

@router.get(
    "/performance",
    response_model=dict,
    summary="Métricas de Performance",
    description="Obtém métricas de performance da aplicação"
)
async def get_performance_metrics() -> dict:
    """
    Obtém métricas de performance da aplicação.
    
    Inclui tempo de atividade, contadores de requisições e taxas de erro.
    """
    try:
        return {
            "timestamp": datetime.now().isoformat(),
            "uptime": app_metrics.get_uptime(),
            "performance": app_metrics.get_performance_metrics(),
            "system_load": {
                "load_avg": os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0],
                "cpu_count": psutil.cpu_count()
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"Failed to get performance metrics: {str(e)}", "code": "PERFORMANCE_METRICS_ERROR"}
        )

@router.get(
    "/health",
    response_model=dict,
    summary="Health Check do Dashboard",
    description="Verifica se o dashboard está funcionando"
)
async def dashboard_health_check() -> dict:
    """Verifica se o dashboard está funcionando"""
    try:
        # Verificações básicas
        cpu_usage = SystemMetrics.get_cpu_usage()
        memory = SystemMetrics.get_memory_usage()
        
        # Status baseado nas métricas
        status = "healthy"
        if cpu_usage > 90 or memory["percentage"] > 95:
            status = "critical"
        elif cpu_usage > 80 or memory["percentage"] > 85:
            status = "warning"
        
        return {
            "service": "monitoring_dashboard",
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "checks": {
                "cpu_ok": cpu_usage < 90,
                "memory_ok": memory["percentage"] < 95,
                "database_ok": os.path.exists("blockchain.db")
            }
        }
        
    except Exception as e:
        return {
            "service": "monitoring_dashboard",
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# Função para incrementar contadores (usar nos middlewares)
def increment_request_count():
    """Incrementa contador de requisições"""
    app_metrics.request_count += 1

def increment_error_count():
    """Incrementa contador de erros"""
    app_metrics.error_count += 1
