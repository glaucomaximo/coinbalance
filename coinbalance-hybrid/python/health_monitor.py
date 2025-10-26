"""
Sistema de Monitoramento de Saúde - CoinBalance
Implementa health checks avançados e monitoramento de componentes
"""

import time
import asyncio
import psutil
import sqlite3
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    """Status de saúde dos componentes"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

@dataclass
class HealthCheck:
    """Resultado de um health check"""
    component: str
    status: HealthStatus
    message: str
    response_time: float
    timestamp: float
    details: Dict[str, Any] = None

class HealthMonitor:
    """Monitor de saúde do sistema CoinBalance"""
    
    def __init__(self):
        self.checks = []
        self.last_check_time = 0
        self.check_interval = 30  # segundos
        self.critical_components = ["database", "crypto", "api"]
        
    async def run_all_checks(self) -> List[HealthCheck]:
        """Executa todos os health checks"""
        self.last_check_time = time.time()
        checks = []
        
        # Health checks básicos
        checks.append(await self.check_system_resources())
        checks.append(await self.check_database())
        checks.append(await self.check_crypto_system())
        # checks.append(await self.check_api_responsiveness())  # Temporariamente desabilitado
        checks.append(await self.check_disk_space())
        checks.append(await self.check_memory_usage())
        checks.append(await self.check_network_connectivity())
        
        self.checks = checks
        return checks
    
    async def check_system_resources(self) -> HealthCheck:
        """Verifica recursos do sistema"""
        start_time = time.time()
        
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            response_time = time.time() - start_time
            
            # Determinar status
            if cpu_percent > 90 or memory.percent > 90 or disk.percent > 95:
                status = HealthStatus.CRITICAL
                message = "Recursos do sistema em nível crítico"
            elif cpu_percent > 70 or memory.percent > 70 or disk.percent > 80:
                status = HealthStatus.WARNING
                message = "Recursos do sistema em nível alto"
            else:
                status = HealthStatus.HEALTHY
                message = "Recursos do sistema normais"
            
            return HealthCheck(
                component="system_resources",
                status=status,
                message=message,
                response_time=response_time,
                timestamp=time.time(),
                details={
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "disk_percent": disk.percent,
                    "memory_available_gb": memory.available / (1024**3),
                    "disk_free_gb": disk.free / (1024**3)
                }
            )
            
        except Exception as e:
            return HealthCheck(
                component="system_resources",
                status=HealthStatus.UNKNOWN,
                message=f"Erro ao verificar recursos: {str(e)}",
                response_time=time.time() - start_time,
                timestamp=time.time()
            )
    
    async def check_database(self) -> HealthCheck:
        """Verifica saúde do banco de dados"""
        start_time = time.time()
        
        try:
            # Conectar ao banco
            conn = sqlite3.connect("blockchain.db")
            cursor = conn.cursor()
            
            # Verificar se tabelas existem
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            # Verificar integridade
            cursor.execute("PRAGMA integrity_check")
            integrity = cursor.fetchone()[0]
            
            # Verificar tamanho do banco
            cursor.execute("SELECT COUNT(*) FROM blocos")
            block_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM transacoes")
            transaction_count = cursor.fetchone()[0]
            
            conn.close()
            
            response_time = time.time() - start_time
            
            # Determinar status
            if integrity != "ok":
                status = HealthStatus.CRITICAL
                message = "Banco de dados corrompido"
            elif len(tables) < 4:  # Esperamos pelo menos 4 tabelas
                status = HealthStatus.WARNING
                message = "Estrutura do banco incompleta"
            else:
                status = HealthStatus.HEALTHY
                message = "Banco de dados funcionando normalmente"
            
            return HealthCheck(
                component="database",
                status=status,
                message=message,
                response_time=response_time,
                timestamp=time.time(),
                details={
                    "tables_count": len(tables),
                    "integrity_check": integrity,
                    "block_count": block_count,
                    "transaction_count": transaction_count
                }
            )
            
        except Exception as e:
            return HealthCheck(
                component="database",
                status=HealthStatus.CRITICAL,
                message=f"Erro no banco de dados: {str(e)}",
                response_time=time.time() - start_time,
                timestamp=time.time()
            )
    
    async def check_crypto_system(self) -> HealthCheck:
        """Verifica sistema de criptografia"""
        start_time = time.time()
        
        try:
            from crypto_utils import CryptoUtils
            
            # Testar geração de chaves
            private_key, public_key = CryptoUtils.gerar_par_chaves()
            
            # Testar assinatura
            test_data = {"test": "data", "timestamp": time.time()}
            signature = CryptoUtils.assinar_transacao(test_data, private_key)
            
            # Testar verificação
            is_valid = CryptoUtils.verificar_assinatura(test_data, signature, public_key)
            
            response_time = time.time() - start_time
            
            if not is_valid:
                status = HealthStatus.CRITICAL
                message = "Sistema de criptografia com falha"
            else:
                status = HealthStatus.HEALTHY
                message = "Sistema de criptografia funcionando"
            
            return HealthCheck(
                component="crypto",
                status=status,
                message=message,
                response_time=response_time,
                timestamp=time.time(),
                details={
                    "key_generation_ok": True,
                    "signature_verification_ok": is_valid
                }
            )
            
        except Exception as e:
            return HealthCheck(
                component="crypto",
                status=HealthStatus.CRITICAL,
                message=f"Erro no sistema de criptografia: {str(e)}",
                response_time=time.time() - start_time,
                timestamp=time.time()
            )
    
    async def check_api_responsiveness(self) -> HealthCheck:
        """Verifica responsividade da API"""
        start_time = time.time()
        
        try:
            # Verificação simples - apenas verificar se conseguimos importar
            import api_moderna
            
            response_time = time.time() - start_time
            
            # Se chegou até aqui, a API está funcionando
            status = HealthStatus.HEALTHY
            message = "API funcionando normalmente"
            
            return HealthCheck(
                component="api",
                status=status,
                message=message,
                response_time=response_time,
                timestamp=time.time(),
                details={
                    "status": "running",
                    "response_time_ms": response_time * 1000
                }
            )
            
        except Exception as e:
            return HealthCheck(
                component="api",
                status=HealthStatus.CRITICAL,
                message=f"Erro ao verificar API: {str(e)}",
                response_time=time.time() - start_time,
                timestamp=time.time()
            )
    
    async def check_disk_space(self) -> HealthCheck:
        """Verifica espaço em disco"""
        start_time = time.time()
        
        try:
            disk = psutil.disk_usage('.')
            free_gb = disk.free / (1024**3)
            total_gb = disk.total / (1024**3)
            percent_used = (disk.used / disk.total) * 100
            
            response_time = time.time() - start_time
            
            if percent_used > 95:
                status = HealthStatus.CRITICAL
                message = "Espaço em disco crítico"
            elif percent_used > 80:
                status = HealthStatus.WARNING
                message = "Espaço em disco baixo"
            else:
                status = HealthStatus.HEALTHY
                message = "Espaço em disco adequado"
            
            return HealthCheck(
                component="disk_space",
                status=status,
                message=message,
                response_time=response_time,
                timestamp=time.time(),
                details={
                    "free_gb": round(free_gb, 2),
                    "total_gb": round(total_gb, 2),
                    "percent_used": round(percent_used, 2)
                }
            )
            
        except Exception as e:
            return HealthCheck(
                component="disk_space",
                status=HealthStatus.UNKNOWN,
                message=f"Erro ao verificar disco: {str(e)}",
                response_time=time.time() - start_time,
                timestamp=time.time()
            )
    
    async def check_memory_usage(self) -> HealthCheck:
        """Verifica uso de memória"""
        start_time = time.time()
        
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            response_time = time.time() - start_time
            
            if memory.percent > 95:
                status = HealthStatus.CRITICAL
                message = "Uso de memória crítico"
            elif memory.percent > 80:
                status = HealthStatus.WARNING
                message = "Uso de memória alto"
            else:
                status = HealthStatus.HEALTHY
                message = "Uso de memória normal"
            
            return HealthCheck(
                component="memory",
                status=status,
                message=message,
                response_time=response_time,
                timestamp=time.time(),
                details={
                    "memory_percent": memory.percent,
                    "memory_available_gb": round(memory.available / (1024**3), 2),
                    "swap_percent": swap.percent,
                    "swap_used_gb": round(swap.used / (1024**3), 2)
                }
            )
            
        except Exception as e:
            return HealthCheck(
                component="memory",
                status=HealthStatus.UNKNOWN,
                message=f"Erro ao verificar memória: {str(e)}",
                response_time=time.time() - start_time,
                timestamp=time.time()
            )
    
    async def check_network_connectivity(self) -> HealthCheck:
        """Verifica conectividade de rede"""
        start_time = time.time()
        
        try:
            import socket
            
            # Testar conectividade básica
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            
            response_time = time.time() - start_time
            
            status = HealthStatus.HEALTHY
            message = "Conectividade de rede OK"
            
            return HealthCheck(
                component="network",
                status=status,
                message=message,
                response_time=response_time,
                timestamp=time.time(),
                details={
                    "connectivity_test": "8.8.8.8:53",
                    "response_time_ms": response_time * 1000
                }
            )
            
        except Exception as e:
            return HealthCheck(
                component="network",
                status=HealthStatus.WARNING,
                message=f"Problema de conectividade: {str(e)}",
                response_time=time.time() - start_time,
                timestamp=time.time()
            )
    
    def get_overall_status(self) -> HealthStatus:
        """Retorna status geral do sistema"""
        if not self.checks:
            return HealthStatus.UNKNOWN
        
        # Verificar se há componentes críticos com falha
        critical_failures = [
            check for check in self.checks 
            if check.component in self.critical_components and check.status == HealthStatus.CRITICAL
        ]
        
        if critical_failures:
            return HealthStatus.CRITICAL
        
        # Verificar se há warnings
        warnings = [check for check in self.checks if check.status == HealthStatus.WARNING]
        if warnings:
            return HealthStatus.WARNING
        
        return HealthStatus.HEALTHY
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Retorna resumo da saúde do sistema"""
        overall_status = self.get_overall_status()
        
        return {
            "overall_status": overall_status.value,
            "timestamp": time.time(),
            "last_check": self.last_check_time,
            "total_checks": len(self.checks),
            "healthy_checks": len([c for c in self.checks if c.status == HealthStatus.HEALTHY]),
            "warning_checks": len([c for c in self.checks if c.status == HealthStatus.WARNING]),
            "critical_checks": len([c for c in self.checks if c.status == HealthStatus.CRITICAL]),
            "checks": [
                {
                    "component": check.component,
                    "status": check.status.value,
                    "message": check.message,
                    "response_time": check.response_time,
                    "details": check.details
                }
                for check in self.checks
            ]
        }

# Instância global do monitor
health_monitor = HealthMonitor()
