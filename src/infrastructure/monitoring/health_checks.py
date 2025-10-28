"""
Sistema de Health Checks Avançados para CoinBalance Enterprise
==============================================================

Este módulo implementa um sistema completo de health checks para
verificação proativa da saúde de todos os componentes do sistema
CoinBalance Enterprise.
"""

import asyncio
import time
import logging
import psutil
import sqlite3
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Status de saúde dos componentes"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheckResult:
    """Resultado de um health check"""
    component: str
    status: HealthStatus
    message: str
    timestamp: float
    response_time: float
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


@dataclass
class HealthCheck:
    """Definição de um health check"""
    name: str
    component: str
    check_function: Callable
    timeout: float = 30.0
    critical: bool = True
    enabled: bool = True


class DatabaseHealthCheck:
    """Health checks para banco de dados"""
    
    @staticmethod
    async def check_database_connection() -> HealthCheckResult:
        """Verifica conexão com banco de dados"""
        start_time = time.time()
        
        try:
            # Tenta conectar ao banco SQLite
            conn = sqlite3.connect('blockchain.db', timeout=5.0)
            cursor = conn.cursor()
            
            # Executa query simples
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            conn.close()
            
            response_time = time.time() - start_time
            
            if result and result[0] == 1:
                return HealthCheckResult(
                    component="database",
                    status=HealthStatus.HEALTHY,
                    message="Conexão com banco de dados OK",
                    timestamp=time.time(),
                    response_time=response_time,
                    details={"query_result": result[0]}
                )
            else:
                return HealthCheckResult(
                    component="database",
                    status=HealthStatus.UNHEALTHY,
                    message="Query de teste falhou",
                    timestamp=time.time(),
                    response_time=response_time
                )
                
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheckResult(
                component="database",
                status=HealthStatus.UNHEALTHY,
                message=f"Erro de conexão: {str(e)}",
                timestamp=time.time(),
                response_time=response_time,
                error=str(e)
            )
    
    @staticmethod
    async def check_database_performance() -> HealthCheckResult:
        """Verifica performance do banco de dados"""
        start_time = time.time()
        
        try:
            conn = sqlite3.connect('blockchain.db', timeout=5.0)
            cursor = conn.cursor()
            
            # Executa query de performance
            cursor.execute("SELECT COUNT(*) FROM blocks")
            block_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM transactions")
            transaction_count = cursor.fetchone()[0]
            
            conn.close()
            
            response_time = time.time() - start_time
            
            return HealthCheckResult(
                component="database",
                status=HealthStatus.HEALTHY,
                message="Performance do banco OK",
                timestamp=time.time(),
                response_time=response_time,
                details={
                    "block_count": block_count,
                    "transaction_count": transaction_count,
                    "query_time": response_time
                }
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheckResult(
                component="database",
                status=HealthStatus.UNHEALTHY,
                message=f"Erro de performance: {str(e)}",
                timestamp=time.time(),
                response_time=response_time,
                error=str(e)
            )


class SystemHealthCheck:
    """Health checks para sistema operacional"""
    
    @staticmethod
    async def check_cpu_usage() -> HealthCheckResult:
        """Verifica uso de CPU"""
        start_time = time.time()
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            response_time = time.time() - start_time
            
            if cpu_percent < 80:
                status = HealthStatus.HEALTHY
                message = f"CPU usage normal: {cpu_percent:.1f}%"
            elif cpu_percent < 95:
                status = HealthStatus.DEGRADED
                message = f"CPU usage alto: {cpu_percent:.1f}%"
            else:
                status = HealthStatus.UNHEALTHY
                message = f"CPU usage crítico: {cpu_percent:.1f}%"
            
            return HealthCheckResult(
                component="system",
                status=status,
                message=message,
                timestamp=time.time(),
                response_time=response_time,
                details={"cpu_percent": cpu_percent}
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheckResult(
                component="system",
                status=HealthStatus.UNHEALTHY,
                message=f"Erro ao verificar CPU: {str(e)}",
                timestamp=time.time(),
                response_time=response_time,
                error=str(e)
            )
    
    @staticmethod
    async def check_memory_usage() -> HealthCheckResult:
        """Verifica uso de memória"""
        start_time = time.time()
        
        try:
            memory = psutil.virtual_memory()
            response_time = time.time() - start_time
            
            if memory.percent < 80:
                status = HealthStatus.HEALTHY
                message = f"Memória OK: {memory.percent:.1f}%"
            elif memory.percent < 95:
                status = HealthStatus.DEGRADED
                message = f"Memória alta: {memory.percent:.1f}%"
            else:
                status = HealthStatus.UNHEALTHY
                message = f"Memória crítica: {memory.percent:.1f}%"
            
            return HealthCheckResult(
                component="system",
                status=status,
                message=message,
                timestamp=time.time(),
                response_time=response_time,
                details={
                    "memory_percent": memory.percent,
                    "memory_available": memory.available,
                    "memory_total": memory.total
                }
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheckResult(
                component="system",
                status=HealthStatus.UNHEALTHY,
                message=f"Erro ao verificar memória: {str(e)}",
                timestamp=time.time(),
                response_time=response_time,
                error=str(e)
            )
    
    @staticmethod
    async def check_disk_usage() -> HealthCheckResult:
        """Verifica uso de disco"""
        start_time = time.time()
        
        try:
            disk = psutil.disk_usage('/')
            response_time = time.time() - start_time
            
            if disk.percent < 80:
                status = HealthStatus.HEALTHY
                message = f"Disco OK: {disk.percent:.1f}%"
            elif disk.percent < 95:
                status = HealthStatus.DEGRADED
                message = f"Disco alto: {disk.percent:.1f}%"
            else:
                status = HealthStatus.UNHEALTHY
                message = f"Disco crítico: {disk.percent:.1f}%"
            
            return HealthCheckResult(
                component="system",
                status=status,
                message=message,
                timestamp=time.time(),
                response_time=response_time,
                details={
                    "disk_percent": disk.percent,
                    "disk_free": disk.free,
                    "disk_total": disk.total
                }
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheckResult(
                component="system",
                status=HealthStatus.UNHEALTHY,
                message=f"Erro ao verificar disco: {str(e)}",
                timestamp=time.time(),
                response_time=response_time,
                error=str(e)
            )


class BlockchainHealthCheck:
    """Health checks para blockchain"""
    
    @staticmethod
    async def check_blockchain_integrity() -> HealthCheckResult:
        """Verifica integridade da blockchain"""
        start_time = time.time()
        
        try:
            # Importa módulos da blockchain
            from src.domain.blockchain.entities.block import Block
            from src.domain.blockchain.entities.blockchain import Blockchain
            
            # Cria instância da blockchain
            blockchain = Blockchain()
            
            # Verifica se há blocos
            if len(blockchain.blocks) == 0:
                return HealthCheckResult(
                    component="blockchain",
                    status=HealthStatus.DEGRADED,
                    message="Blockchain vazia",
                    timestamp=time.time(),
                    response_time=time.time() - start_time,
                    details={"block_count": 0}
                )
            
            # Verifica integridade dos blocos
            invalid_blocks = 0
            for block in blockchain.blocks:
                if not block.is_valid():
                    invalid_blocks += 1
            
            response_time = time.time() - start_time
            
            if invalid_blocks == 0:
                status = HealthStatus.HEALTHY
                message = f"Blockchain íntegra: {len(blockchain.blocks)} blocos"
            else:
                status = HealthStatus.UNHEALTHY
                message = f"Blockchain com {invalid_blocks} blocos inválidos"
            
            return HealthCheckResult(
                component="blockchain",
                status=status,
                message=message,
                timestamp=time.time(),
                response_time=response_time,
                details={
                    "total_blocks": len(blockchain.blocks),
                    "invalid_blocks": invalid_blocks
                }
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheckResult(
                component="blockchain",
                status=HealthStatus.UNHEALTHY,
                message=f"Erro ao verificar blockchain: {str(e)}",
                timestamp=time.time(),
                response_time=response_time,
                error=str(e)
            )


class APIHealthCheck:
    """Health checks para APIs"""
    
    @staticmethod
    async def check_api_endpoints() -> HealthCheckResult:
        """Verifica endpoints da API"""
        start_time = time.time()
        
        try:
            import httpx
            
            endpoints = [
                "/api/v1/health",
                "/api/v1/health/live",
                "/api/v1/health/ready"
            ]
            
            async with httpx.AsyncClient() as client:
                results = []
                for endpoint in endpoints:
                    try:
                        response = await client.get(f"http://localhost:8000{endpoint}", timeout=5.0)
                        results.append({
                            "endpoint": endpoint,
                            "status": response.status_code,
                            "success": 200 <= response.status_code < 300
                        })
                    except Exception as e:
                        results.append({
                            "endpoint": endpoint,
                            "status": 0,
                            "success": False,
                            "error": str(e)
                        })
                
                response_time = time.time() - start_time
                
                successful_endpoints = sum(1 for r in results if r["success"])
                total_endpoints = len(results)
                
                if successful_endpoints == total_endpoints:
                    status = HealthStatus.HEALTHY
                    message = f"Todos os endpoints OK: {successful_endpoints}/{total_endpoints}"
                elif successful_endpoints > 0:
                    status = HealthStatus.DEGRADED
                    message = f"Alguns endpoints falharam: {successful_endpoints}/{total_endpoints}"
                else:
                    status = HealthStatus.UNHEALTHY
                    message = f"Todos os endpoints falharam: {successful_endpoints}/{total_endpoints}"
                
                return HealthCheckResult(
                    component="api",
                    status=status,
                    message=message,
                    timestamp=time.time(),
                    response_time=response_time,
                    details={"endpoints": results}
                )
                
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheckResult(
                component="api",
                status=HealthStatus.UNHEALTHY,
                message=f"Erro ao verificar APIs: {str(e)}",
                timestamp=time.time(),
                response_time=response_time,
                error=str(e)
            )


class HealthCheckManager:
    """Gerenciador de health checks"""
    
    def __init__(self):
        self.health_checks: Dict[str, HealthCheck] = {}
        self.results_history: Dict[str, List[HealthCheckResult]] = {}
        self.running = False
        
        # Registra health checks padrão
        self._register_default_health_checks()
        
        logger.info("HealthCheckManager inicializado")
    
    def _register_default_health_checks(self):
        """Registra health checks padrão"""
        default_checks = [
            HealthCheck("database_connection", "database", DatabaseHealthCheck.check_database_connection),
            HealthCheck("database_performance", "database", DatabaseHealthCheck.check_database_performance),
            HealthCheck("cpu_usage", "system", SystemHealthCheck.check_cpu_usage),
            HealthCheck("memory_usage", "system", SystemHealthCheck.check_memory_usage),
            HealthCheck("disk_usage", "system", SystemHealthCheck.check_disk_usage),
            HealthCheck("blockchain_integrity", "blockchain", BlockchainHealthCheck.check_blockchain_integrity),
            HealthCheck("api_endpoints", "api", APIHealthCheck.check_api_endpoints),
        ]
        
        for check in default_checks:
            self.register_health_check(check)
    
    def register_health_check(self, health_check: HealthCheck):
        """Registra um health check"""
        self.health_checks[health_check.name] = health_check
        self.results_history[health_check.name] = []
        logger.info(f"Health check '{health_check.name}' registrado")
    
    def unregister_health_check(self, name: str):
        """Remove um health check"""
        if name in self.health_checks:
            del self.health_checks[name]
            if name in self.results_history:
                del self.results_history[name]
            logger.info(f"Health check '{name}' removido")
    
    async def run_health_check(self, name: str) -> Optional[HealthCheckResult]:
        """Executa um health check específico"""
        if name not in self.health_checks:
            return None
        
        health_check = self.health_checks[name]
        if not health_check.enabled:
            return None
        
        try:
            # Executa o health check com timeout
            result = await asyncio.wait_for(
                health_check.check_function(),
                timeout=health_check.timeout
            )
            
            # Armazena resultado no histórico
            self.results_history[name].append(result)
            
            # Mantém apenas os últimos 100 resultados
            if len(self.results_history[name]) > 100:
                self.results_history[name] = self.results_history[name][-100:]
            
            return result
            
        except asyncio.TimeoutError:
            result = HealthCheckResult(
                component=health_check.component,
                status=HealthStatus.UNHEALTHY,
                message=f"Health check '{name}' timeout após {health_check.timeout}s",
                timestamp=time.time(),
                response_time=health_check.timeout,
                error="Timeout"
            )
            self.results_history[name].append(result)
            return result
            
        except Exception as e:
            result = HealthCheckResult(
                component=health_check.component,
                status=HealthStatus.UNHEALTHY,
                message=f"Erro no health check '{name}': {str(e)}",
                timestamp=time.time(),
                response_time=0,
                error=str(e)
            )
            self.results_history[name].append(result)
            return result
    
    async def run_all_health_checks(self) -> Dict[str, HealthCheckResult]:
        """Executa todos os health checks"""
        results = {}
        
        tasks = []
        for name in self.health_checks:
            if self.health_checks[name].enabled:
                task = asyncio.create_task(self.run_health_check(name))
                tasks.append((name, task))
        
        # Executa todos os health checks em paralelo
        for name, task in tasks:
            try:
                result = await task
                if result:
                    results[name] = result
            except Exception as e:
                logger.error(f"Erro ao executar health check '{name}': {e}")
        
        return results
    
    def get_overall_health(self) -> Dict[str, Any]:
        """Retorna saúde geral do sistema"""
        if not self.results_history:
            return {
                "status": HealthStatus.UNKNOWN.value,
                "message": "Nenhum health check executado",
                "timestamp": time.time()
            }
        
        # Obtém último resultado de cada health check
        latest_results = {}
        for name, history in self.results_history.items():
            if history:
                latest_results[name] = history[-1]
        
        if not latest_results:
            return {
                "status": HealthStatus.UNKNOWN.value,
                "message": "Nenhum resultado disponível",
                "timestamp": time.time()
            }
        
        # Determina status geral
        critical_failures = 0
        degraded_components = 0
        healthy_components = 0
        
        for name, result in latest_results.items():
            health_check = self.health_checks.get(name)
            if health_check and health_check.critical:
                if result.status == HealthStatus.UNHEALTHY:
                    critical_failures += 1
                elif result.status == HealthStatus.DEGRADED:
                    degraded_components += 1
                else:
                    healthy_components += 1
        
        if critical_failures > 0:
            status = HealthStatus.UNHEALTHY
            message = f"{critical_failures} componentes críticos com falha"
        elif degraded_components > 0:
            status = HealthStatus.DEGRADED
            message = f"{degraded_components} componentes degradados"
        else:
            status = HealthStatus.HEALTHY
            message = "Todos os componentes saudáveis"
        
        return {
            "status": status.value,
            "message": message,
            "timestamp": time.time(),
            "components": {
                "total": len(latest_results),
                "healthy": healthy_components,
                "degraded": degraded_components,
                "unhealthy": critical_failures
            },
            "details": latest_results
        }
    
    def get_health_history(self, name: str, limit: int = 50) -> List[HealthCheckResult]:
        """Retorna histórico de um health check"""
        if name not in self.results_history:
            return []
        
        return self.results_history[name][-limit:]
    
    async def start_periodic_checks(self, interval: int = 60):
        """Inicia verificações periódicas"""
        if self.running:
            return
        
        self.running = True
        logger.info(f"Iniciando verificações periódicas a cada {interval}s")
        
        while self.running:
            try:
                await self.run_all_health_checks()
                await asyncio.sleep(interval)
            except Exception as e:
                logger.error(f"Erro nas verificações periódicas: {e}")
                await asyncio.sleep(interval)
    
    def stop_periodic_checks(self):
        """Para verificações periódicas"""
        self.running = False
        logger.info("Verificações periódicas paradas")


# Instância global do gerenciador de health checks
health_check_manager = HealthCheckManager()
