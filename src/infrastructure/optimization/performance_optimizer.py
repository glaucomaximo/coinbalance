"""
Performance Optimizer - Sistema de Otimização de Performance
Baseado na análise holística do CoinBalance
"""

import asyncio
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import psutil
import gc

logger = logging.getLogger(__name__)


class OptimizationLevel(Enum):
    """Níveis de otimização"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class PerformanceMetrics:
    """Métricas de performance"""
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_io: float = 0.0
    network_io: float = 0.0
    response_time: float = 0.0
    throughput: float = 0.0
    error_rate: float = 0.0
    timestamp: float = field(default_factory=time.time)


@dataclass
class OptimizationRule:
    """Regra de otimização"""
    name: str
    condition: str
    action: str
    priority: int
    enabled: bool = True
    last_applied: Optional[float] = None


class PerformanceOptimizer:
    """Otimizador de Performance Holístico"""
    
    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
        self.optimization_rules: List[OptimizationRule] = []
        self.is_monitoring = False
        self.optimization_level = OptimizationLevel.MEDIUM
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Configura regras padrão de otimização"""
        self.optimization_rules = [
            OptimizationRule(
                name="memory_cleanup",
                condition="memory_usage > 80",
                action="gc.collect()",
                priority=1
            ),
            OptimizationRule(
                name="cpu_throttling",
                condition="cpu_usage > 90",
                action="throttle_requests",
                priority=2
            ),
            OptimizationRule(
                name="cache_optimization",
                condition="response_time > 500",
                action="optimize_cache",
                priority=3
            ),
            OptimizationRule(
                name="connection_pooling",
                condition="throughput < 100",
                action="optimize_connections",
                priority=4
            )
        ]
    
    async def start_monitoring(self):
        """Inicia monitoramento contínuo"""
        self.is_monitoring = True
        logger.info("🔍 Iniciando monitoramento de performance")
        
        while self.is_monitoring:
            try:
                metrics = await self._collect_metrics()
                self.metrics_history.append(metrics)
                
                # Manter apenas últimas 100 métricas
                if len(self.metrics_history) > 100:
                    self.metrics_history = self.metrics_history[-100:]
                
                await self._apply_optimizations(metrics)
                await asyncio.sleep(5)  # Monitorar a cada 5 segundos
                
            except Exception as e:
                logger.error(f"Erro no monitoramento: {e}")
                await asyncio.sleep(10)
    
    async def stop_monitoring(self):
        """Para o monitoramento"""
        self.is_monitoring = False
        logger.info("🛑 Monitoramento de performance parado")
    
    async def _collect_metrics(self) -> PerformanceMetrics:
        """Coleta métricas do sistema"""
        try:
            # Métricas do sistema
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_io_counters()
            network = psutil.net_io_counters()
            
            # Métricas da aplicação (simuladas)
            response_time = self._calculate_avg_response_time()
            throughput = self._calculate_throughput()
            error_rate = self._calculate_error_rate()
            
            return PerformanceMetrics(
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                disk_io=disk.read_bytes + disk.write_bytes if disk else 0,
                network_io=network.bytes_sent + network.bytes_recv if network else 0,
                response_time=response_time,
                throughput=throughput,
                error_rate=error_rate
            )
            
        except Exception as e:
            logger.error(f"Erro ao coletar métricas: {e}")
            return PerformanceMetrics()
    
    def _calculate_avg_response_time(self) -> float:
        """Calcula tempo médio de resposta"""
        # Simulação - em produção seria baseado em logs reais
        return 150.0  # ms
    
    def _calculate_throughput(self) -> float:
        """Calcula throughput atual"""
        # Simulação - em produção seria baseado em métricas reais
        return 500.0  # RPS
    
    def _calculate_error_rate(self) -> float:
        """Calcula taxa de erro"""
        # Simulação - em produção seria baseado em logs de erro
        return 0.01  # 1%
    
    async def _apply_optimizations(self, metrics: PerformanceMetrics):
        """Aplica otimizações baseadas nas métricas"""
        for rule in self.optimization_rules:
            if not rule.enabled:
                continue
            
            if self._evaluate_condition(rule.condition, metrics):
                await self._execute_action(rule.action, rule)
                rule.last_applied = time.time()
                logger.info(f"✅ Otimização aplicada: {rule.name}")
    
    def _evaluate_condition(self, condition: str, metrics: PerformanceMetrics) -> bool:
        """Avalia condição de otimização"""
        try:
            # Substitui variáveis pelas métricas
            eval_context = {
                'cpu_usage': metrics.cpu_usage,
                'memory_usage': metrics.memory_usage,
                'response_time': metrics.response_time,
                'throughput': metrics.throughput,
                'error_rate': metrics.error_rate
            }
            
            return eval(condition, {"__builtins__": {}}, eval_context)
        except Exception as e:
            logger.error(f"Erro ao avaliar condição '{condition}': {e}")
            return False
    
    async def _execute_action(self, action: str, rule: OptimizationRule):
        """Executa ação de otimização"""
        try:
            if action == "gc.collect()":
                gc.collect()
                logger.info("🧹 Garbage collection executado")
            
            elif action == "throttle_requests":
                await self._throttle_requests()
            
            elif action == "optimize_cache":
                await self._optimize_cache()
            
            elif action == "optimize_connections":
                await self._optimize_connections()
            
            else:
                logger.warning(f"Ação desconhecida: {action}")
                
        except Exception as e:
            logger.error(f"Erro ao executar ação '{action}': {e}")
    
    async def _throttle_requests(self):
        """Aplica throttling de requisições"""
        logger.info("⏳ Aplicando throttling de requisições")
        # Implementação do throttling
    
    async def _optimize_cache(self):
        """Otimiza cache"""
        logger.info("💾 Otimizando cache")
        # Implementação da otimização de cache
    
    async def _optimize_connections(self):
        """Otimiza conexões"""
        logger.info("🔗 Otimizando conexões")
        # Implementação da otimização de conexões
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Gera relatório de performance"""
        if not self.metrics_history:
            return {"status": "no_data"}
        
        latest = self.metrics_history[-1]
        avg_cpu = sum(m.cpu_usage for m in self.metrics_history) / len(self.metrics_history)
        avg_memory = sum(m.memory_usage for m in self.metrics_history) / len(self.metrics_history)
        avg_response = sum(m.response_time for m in self.metrics_history) / len(self.metrics_history)
        
        return {
            "status": "active",
            "current_metrics": {
                "cpu_usage": latest.cpu_usage,
                "memory_usage": latest.memory_usage,
                "response_time": latest.response_time,
                "throughput": latest.throughput,
                "error_rate": latest.error_rate
            },
            "average_metrics": {
                "cpu_usage": avg_cpu,
                "memory_usage": avg_memory,
                "response_time": avg_response
            },
            "optimization_level": self.optimization_level.value,
            "active_rules": len([r for r in self.optimization_rules if r.enabled]),
            "total_optimizations": len([r for r in self.optimization_rules if r.last_applied])
        }
    
    def add_optimization_rule(self, rule: OptimizationRule):
        """Adiciona nova regra de otimização"""
        self.optimization_rules.append(rule)
        logger.info(f"➕ Nova regra adicionada: {rule.name}")
    
    def remove_optimization_rule(self, rule_name: str):
        """Remove regra de otimização"""
        self.optimization_rules = [r for r in self.optimization_rules if r.name != rule_name]
        logger.info(f"➖ Regra removida: {rule_name}")
    
    def set_optimization_level(self, level: OptimizationLevel):
        """Define nível de otimização"""
        self.optimization_level = level
        logger.info(f"🎚️ Nível de otimização alterado para: {level.value}")


# Instância global do otimizador
performance_optimizer = PerformanceOptimizer()
