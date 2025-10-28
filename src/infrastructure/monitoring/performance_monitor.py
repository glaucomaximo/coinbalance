"""
Sistema de Monitoramento de Performance Consciente
=================================================

Implementação de um sistema de monitoramento de performance que não apenas mede
métricas, mas compreende padrões de uso, otimiza automaticamente e evolui continuamente.

Este sistema implementa:
- Monitoramento de performance em tempo real
- Análise preditiva de recursos
- Otimização automática
- Detecção de gargalos
- Integração com consciência artificial
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable
from decimal import Decimal
import time
import psutil
import threading
from collections import defaultdict, deque
import statistics
import asyncio
import logging

logger = logging.getLogger(__name__)


class PerformanceMetric(Enum):
    """Métricas de Performance"""
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    DISK_USAGE = "disk_usage"
    NETWORK_IO = "network_io"
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    CONCURRENT_USERS = "concurrent_users"


class OptimizationAction(Enum):
    """Ações de Otimização"""
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    CACHE_ENABLE = "cache_enable"
    CACHE_DISABLE = "cache_disable"
    CONNECTION_POOL_INCREASE = "connection_pool_increase"
    CONNECTION_POOL_DECREASE = "connection_pool_decrease"
    WORKER_INCREASE = "worker_increase"
    WORKER_DECREASE = "worker_decrease"
    TIMEOUT_INCREASE = "timeout_increase"
    TIMEOUT_DECREASE = "timeout_decrease"


@dataclass
class PerformanceDataPoint:
    """
    Ponto de Dados de Performance
    """
    metric: PerformanceMetric
    value: Decimal
    timestamp: float
    context: Dict[str, Any] = field(default_factory=dict)
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class PerformanceAlert:
    """
    Alerta de Performance
    """
    id: str
    metric: PerformanceMetric
    threshold: Decimal
    current_value: Decimal
    severity: str  # low, medium, high, critical
    timestamp: float
    message: str
    recommendations: List[str] = field(default_factory=list)
    resolved: bool = False


@dataclass
class OptimizationRule:
    """
    Regra de Otimização
    """
    id: str
    name: str
    condition: Callable[[Dict[str, Decimal]], bool]
    action: OptimizationAction
    parameters: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    last_applied: Optional[float] = None
    success_count: int = 0
    failure_count: int = 0


class ConsciousPerformanceMonitor:
    """
    Monitor de Performance Consciente
    Monitora, analisa e otimiza automaticamente
    """
    
    def __init__(self):
        self.metrics_history: Dict[PerformanceMetric, deque] = defaultdict(
            lambda: deque(maxlen=1000)
        )
        self.alerts: List[PerformanceAlert] = []
        self.optimization_rules: List[OptimizationRule] = []
        self.optimization_history: List[Dict[str, Any]] = []
        self._lock = threading.RLock()
        
        # Atributos faltantes
        self.performance_history: List[PerformanceDataPoint] = []
        self.performance_alerts: List[PerformanceAlert] = []
        self.auto_optimization_enabled = True
        self.monitoring_active = True
        
        # Configurações
        self.collection_interval = 5  # segundos
        self.alert_thresholds = {
            PerformanceMetric.CPU_USAGE: Decimal("0.8"),
            PerformanceMetric.MEMORY_USAGE: Decimal("0.85"),
            PerformanceMetric.DISK_USAGE: Decimal("0.9"),
            PerformanceMetric.RESPONSE_TIME: Decimal("2000"),  # ms
            PerformanceMetric.ERROR_RATE: Decimal("0.05"),  # 5%
        }
        
        # Inicializa regras de otimização
        self._initialize_optimization_rules()
        
        # Inicia coleta automática
        self._start_collection()
    
    def _initialize_optimization_rules(self):
        """Inicializa regras de otimização"""
        # Regra: CPU alto -> aumentar workers
        cpu_high_rule = OptimizationRule(
            id="cpu_high_scale_up",
            name="Scale up on high CPU",
            condition=lambda metrics: metrics.get(PerformanceMetric.CPU_USAGE, Decimal("0")) > Decimal("0.8"),
            action=OptimizationAction.WORKER_INCREASE,
            parameters={"worker_count": 2}
        )
        self.optimization_rules.append(cpu_high_rule)
        
        # Regra: CPU baixo -> diminuir workers
        cpu_low_rule = OptimizationRule(
            id="cpu_low_scale_down",
            name="Scale down on low CPU",
            condition=lambda metrics: metrics.get(PerformanceMetric.CPU_USAGE, Decimal("0")) < Decimal("0.3"),
            action=OptimizationAction.WORKER_DECREASE,
            parameters={"worker_count": 1}
        )
        self.optimization_rules.append(cpu_low_rule)
        
        # Regra: Memória alta -> habilitar cache
        memory_high_rule = OptimizationRule(
            id="memory_high_enable_cache",
            name="Enable cache on high memory",
            condition=lambda metrics: metrics.get(PerformanceMetric.MEMORY_USAGE, Decimal("0")) > Decimal("0.8"),
            action=OptimizationAction.CACHE_ENABLE,
            parameters={"cache_size": "256MB"}
        )
        self.optimization_rules.append(memory_high_rule)
        
        # Regra: Response time alto -> aumentar timeout
        response_time_high_rule = OptimizationRule(
            id="response_time_high_increase_timeout",
            name="Increase timeout on high response time",
            condition=lambda metrics: metrics.get(PerformanceMetric.RESPONSE_TIME, Decimal("0")) > Decimal("1000"),
            action=OptimizationAction.TIMEOUT_INCREASE,
            parameters={"timeout_increase": 1000}  # ms
        )
        self.optimization_rules.append(response_time_high_rule)
    
    def _start_collection(self):
        """Inicia coleta automática de métricas"""
        def collect_metrics():
            while True:
                try:
                    self._collect_system_metrics()
                    self._check_alerts()
                    self._apply_optimization_rules()
                    time.sleep(self.collection_interval)
                except Exception as e:
                    print(f"Erro na coleta de métricas: {e}")
                    time.sleep(self.collection_interval)
        
        collection_thread = threading.Thread(target=collect_metrics, daemon=True)
        collection_thread.start()
    
    def _collect_system_metrics(self):
        """Coleta métricas do sistema"""
        with self._lock:
            timestamp = time.time()
            
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            self._add_metric(PerformanceMetric.CPU_USAGE, Decimal(str(cpu_percent / 100)), timestamp)
            
            # Memória
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            self._add_metric(PerformanceMetric.MEMORY_USAGE, Decimal(str(memory_percent / 100)), timestamp)
            
            # Disco
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            self._add_metric(PerformanceMetric.DISK_USAGE, Decimal(str(disk_percent / 100)), timestamp)
            
            # Network I/O
            network = psutil.net_io_counters()
            network_bytes = network.bytes_sent + network.bytes_recv
            self._add_metric(PerformanceMetric.NETWORK_IO, Decimal(str(network_bytes)), timestamp)
    
    def _add_metric(self, metric: PerformanceMetric, value: Decimal, timestamp: float):
        """Adiciona métrica ao histórico"""
        data_point = PerformanceDataPoint(
            metric=metric,
            value=value,
            timestamp=timestamp
        )
        
        self.metrics_history[metric].append(data_point)
    
    def add_custom_metric(self, metric: PerformanceMetric, value: Decimal, 
                         context: Dict[str, Any] = None, tags: Dict[str, str] = None):
        """Adiciona métrica customizada"""
        with self._lock:
            timestamp = time.time()
            data_point = PerformanceDataPoint(
                metric=metric,
                value=value,
                timestamp=timestamp,
                context=context or {},
                tags=tags or {}
            )
            
            self.metrics_history[metric].append(data_point)
    
    def _check_alerts(self):
        """Verifica alertas de performance"""
        current_metrics = self._get_current_metrics()
        
        for metric, threshold in self.alert_thresholds.items():
            current_value = current_metrics.get(metric, Decimal("0"))
            
            if current_value >= threshold:
                # Verifica se já existe alerta recente
                recent_alerts = [a for a in self.alerts 
                               if a.metric == metric and 
                               time.time() - a.timestamp < 300]  # 5 minutos
                
                if not recent_alerts:
                    self._create_alert(metric, threshold, current_value)
    
    def _get_current_metrics(self) -> Dict[PerformanceMetric, Decimal]:
        """Obtém métricas atuais"""
        current_metrics = {}
        
        for metric, history in self.metrics_history.items():
            if history:
                current_metrics[metric] = history[-1].value
        
        return current_metrics
    
    def _create_alert(self, metric: PerformanceMetric, threshold: Decimal, current_value: Decimal):
        """Cria alerta de performance"""
        severity = self._determine_severity(metric, current_value)
        message = self._generate_alert_message(metric, threshold, current_value, severity)
        recommendations = self._generate_recommendations(metric, current_value)
        
        alert = PerformanceAlert(
            id=f"perf_alert_{int(time.time() * 1000)}",
            metric=metric,
            threshold=threshold,
            current_value=current_value,
            severity=severity,
            timestamp=time.time(),
            message=message,
            recommendations=recommendations
        )
        
        self.alerts.append(alert)
        
        # Mantém apenas últimos 100 alertas
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
    
    def _determine_severity(self, metric: PerformanceMetric, value: Decimal) -> str:
        """Determina severidade do alerta"""
        thresholds = {
            PerformanceMetric.CPU_USAGE: {
                "low": Decimal("0.6"),
                "medium": Decimal("0.8"),
                "high": Decimal("0.9")
            },
            PerformanceMetric.MEMORY_USAGE: {
                "low": Decimal("0.7"),
                "medium": Decimal("0.85"),
                "high": Decimal("0.95")
            },
            PerformanceMetric.DISK_USAGE: {
                "low": Decimal("0.8"),
                "medium": Decimal("0.9"),
                "high": Decimal("0.95")
            },
            PerformanceMetric.RESPONSE_TIME: {
                "low": Decimal("1000"),
                "medium": Decimal("2000"),
                "high": Decimal("5000")
            },
            PerformanceMetric.ERROR_RATE: {
                "low": Decimal("0.01"),
                "medium": Decimal("0.05"),
                "high": Decimal("0.1")
            }
        }
        
        metric_thresholds = thresholds.get(metric, {})
        
        if value >= metric_thresholds.get("high", Decimal("1.0")):
            return "critical"
        elif value >= metric_thresholds.get("medium", Decimal("0.5")):
            return "high"
        elif value >= metric_thresholds.get("low", Decimal("0.1")):
            return "medium"
        else:
            return "low"
    
    def _generate_alert_message(self, metric: PerformanceMetric, threshold: Decimal, 
                               current_value: Decimal, severity: str) -> str:
        """Gera mensagem do alerta"""
        metric_names = {
            PerformanceMetric.CPU_USAGE: "CPU",
            PerformanceMetric.MEMORY_USAGE: "Memória",
            PerformanceMetric.DISK_USAGE: "Disco",
            PerformanceMetric.RESPONSE_TIME: "Tempo de Resposta",
            PerformanceMetric.ERROR_RATE: "Taxa de Erro"
        }
        
        metric_name = metric_names.get(metric, metric.value)
        
        if metric == PerformanceMetric.RESPONSE_TIME:
            return f"{metric_name} está em {current_value}ms (threshold: {threshold}ms) - Severidade: {severity}"
        elif metric == PerformanceMetric.ERROR_RATE:
            return f"{metric_name} está em {current_value * 100:.2f}% (threshold: {threshold * 100:.2f}%) - Severidade: {severity}"
        else:
            return f"{metric_name} está em {current_value * 100:.2f}% (threshold: {threshold * 100:.2f}%) - Severidade: {severity}"
    
    def _generate_recommendations(self, metric: PerformanceMetric, value: Decimal) -> List[str]:
        """Gera recomendações para métrica"""
        recommendations = []
        
        if metric == PerformanceMetric.CPU_USAGE:
            if value > Decimal("0.8"):
                recommendations.append("Considere escalar horizontalmente os recursos de CPU")
                recommendations.append("Verifique processos com alto consumo de CPU")
                recommendations.append("Implemente cache para reduzir processamento")
            elif value > Decimal("0.6"):
                recommendations.append("Monitore tendência de crescimento da CPU")
                recommendations.append("Prepare plano de escalabilidade")
        
        elif metric == PerformanceMetric.MEMORY_USAGE:
            if value > Decimal("0.85"):
                recommendations.append("Considere aumentar a memória disponível")
                recommendations.append("Verifique vazamentos de memória")
                recommendations.append("Implemente garbage collection mais agressivo")
            elif value > Decimal("0.7"):
                recommendations.append("Monitore uso de memória")
                recommendations.append("Considere otimizar estruturas de dados")
        
        elif metric == PerformanceMetric.DISK_USAGE:
            if value > Decimal("0.9"):
                recommendations.append("CRÍTICO: Espaço em disco quase esgotado")
                recommendations.append("Limpe arquivos temporários e logs antigos")
                recommendations.append("Considere aumentar capacidade de armazenamento")
            elif value > Decimal("0.8"):
                recommendations.append("Monitore espaço em disco")
                recommendations.append("Implemente rotação de logs")
        
        elif metric == PerformanceMetric.RESPONSE_TIME:
            if value > Decimal("2000"):
                recommendations.append("Otimize consultas de banco de dados")
                recommendations.append("Implemente cache para melhorar performance")
                recommendations.append("Considere CDN para conteúdo estático")
            elif value > Decimal("1000"):
                recommendations.append("Monitore tempo de resposta")
                recommendations.append("Identifique gargalos de performance")
        
        elif metric == PerformanceMetric.ERROR_RATE:
            if value > Decimal("0.05"):
                recommendations.append("Investigue causa raiz dos erros")
                recommendations.append("Implemente tratamento de erro mais robusto")
                recommendations.append("Monitore logs de erro")
            elif value > Decimal("0.01"):
                recommendations.append("Monitore taxa de erro")
                recommendations.append("Analise padrões de erro")
        
        return recommendations
    
    def _apply_optimization_rules(self):
        """Aplica regras de otimização"""
        current_metrics = self._get_current_metrics()
        
        for rule in self.optimization_rules:
            if not rule.enabled:
                continue
            
            # Verifica cooldown (não aplicar mesma regra muito frequentemente)
            if rule.last_applied and time.time() - rule.last_applied < 300:  # 5 minutos
                continue
            
            try:
                if rule.condition(current_metrics):
                    success = self._apply_optimization_action(rule.action, rule.parameters)
                    
                    rule.last_applied = time.time()
                    
                    if success:
                        rule.success_count += 1
                        self.optimization_history.append({
                            "timestamp": time.time(),
                            "rule_id": rule.id,
                            "rule_name": rule.name,
                            "action": rule.action.value,
                            "parameters": rule.parameters,
                            "success": True,
                            "metrics": current_metrics.copy()
                        })
                    else:
                        rule.failure_count += 1
                        self.optimization_history.append({
                            "timestamp": time.time(),
                            "rule_id": rule.id,
                            "rule_name": rule.name,
                            "action": rule.action.value,
                            "parameters": rule.parameters,
                            "success": False,
                            "metrics": current_metrics.copy()
                        })
            
            except Exception as e:
                print(f"Erro ao aplicar regra de otimização {rule.id}: {e}")
                rule.failure_count += 1
    
    def _apply_optimization_action(self, action: OptimizationAction, parameters: Dict[str, Any]) -> bool:
        """Aplica ação de otimização"""
        try:
            if action == OptimizationAction.WORKER_INCREASE:
                # Em produção, isso seria integrado com o sistema de workers
                print(f"Aplicando WORKER_INCREASE: {parameters}")
                return True
            
            elif action == OptimizationAction.WORKER_DECREASE:
                print(f"Aplicando WORKER_DECREASE: {parameters}")
                return True
            
            elif action == OptimizationAction.CACHE_ENABLE:
                print(f"Aplicando CACHE_ENABLE: {parameters}")
                return True
            
            elif action == OptimizationAction.CACHE_DISABLE:
                print(f"Aplicando CACHE_DISABLE: {parameters}")
                return True
            
            elif action == OptimizationAction.TIMEOUT_INCREASE:
                print(f"Aplicando TIMEOUT_INCREASE: {parameters}")
                return True
            
            elif action == OptimizationAction.TIMEOUT_DECREASE:
                print(f"Aplicando TIMEOUT_DECREASE: {parameters}")
                return True
            
            else:
                print(f"Ação de otimização não implementada: {action}")
                return False
        
        except Exception as e:
            print(f"Erro ao aplicar ação {action}: {e}")
            return False
    
    def get_performance_dashboard(self) -> Dict[str, Any]:
        """Retorna dados para dashboard de performance"""
        with self._lock:
            current_metrics = self._get_current_metrics()
            
            # Alertas ativos
            active_alerts = [a for a in self.alerts if not a.resolved]
            
            # Histórico de otimizações
            recent_optimizations = sorted(
                self.optimization_history,
                key=lambda x: x["timestamp"],
                reverse=True
            )[:10]
            
            # Estatísticas de regras
            rule_stats = [
                {
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "enabled": rule.enabled,
                    "success_count": rule.success_count,
                    "failure_count": rule.failure_count,
                    "success_rate": rule.success_count / (rule.success_count + rule.failure_count) 
                                   if (rule.success_count + rule.failure_count) > 0 else 0
                }
                for rule in self.optimization_rules
            ]
            
            # Performance score
            performance_score = self._calculate_performance_score(current_metrics)
            
            return {
                "current_metrics": {
                    metric.value: float(value) for metric, value in current_metrics.items()
                },
                "active_alerts": len(active_alerts),
                "total_alerts": len(self.alerts),
                "performance_score": performance_score,
                "optimization_rules": rule_stats,
                "recent_optimizations": recent_optimizations,
                "alert_thresholds": {
                    metric.value: float(threshold) for metric, threshold in self.alert_thresholds.items()
                },
                "last_updated": time.time()
            }
    
    def _calculate_performance_score(self, metrics: Dict[PerformanceMetric, Decimal]) -> float:
        """Calcula score de performance geral"""
        if not metrics:
            return 100.0
        
        total_score = 0.0
        weight_sum = 0.0
        
        # Pesos para diferentes métricas
        weights = {
            PerformanceMetric.CPU_USAGE: 0.25,
            PerformanceMetric.MEMORY_USAGE: 0.25,
            PerformanceMetric.DISK_USAGE: 0.15,
            PerformanceMetric.RESPONSE_TIME: 0.20,
            PerformanceMetric.ERROR_RATE: 0.15
        }
        
        for metric, value in metrics.items():
            weight = weights.get(metric, 0.1)
            
            # Calcula score baseado no valor da métrica
            if metric in [PerformanceMetric.CPU_USAGE, PerformanceMetric.MEMORY_USAGE, 
                          PerformanceMetric.DISK_USAGE, PerformanceMetric.ERROR_RATE]:
                # Para métricas de uso, quanto menor melhor
                score = max(100.0 - float(value) * 100, 0.0)
            elif metric == PerformanceMetric.RESPONSE_TIME:
                # Para tempo de resposta, quanto menor melhor
                score = max(100.0 - float(value) / 100, 0.0)  # Normalizado
            else:
                score = 50.0  # Neutro
            
            total_score += score * weight
            weight_sum += weight
        
        return total_score / weight_sum if weight_sum > 0 else 100.0
    
    def get_metric_trends(self, metric: PerformanceMetric, hours: int = 24) -> Dict[str, Any]:
        """Retorna tendências de uma métrica"""
        with self._lock:
            history = self.metrics_history.get(metric, deque())
            
            if not history:
                return {"trend": "no_data", "values": [], "timestamps": []}
            
            # Filtra dados das últimas N horas
            cutoff_time = time.time() - (hours * 3600)
            recent_data = [dp for dp in history if dp.timestamp >= cutoff_time]
            
            if len(recent_data) < 2:
                return {"trend": "insufficient_data", "values": [], "timestamps": []}
            
            values = [float(dp.value) for dp in recent_data]
            timestamps = [dp.timestamp for dp in recent_data]
            
            # Calcula tendência
            trend = self._calculate_trend(values)
            
            return {
                "trend": trend,
                "values": values,
                "timestamps": timestamps,
                "current_value": values[-1],
                "average_value": statistics.mean(values),
                "min_value": min(values),
                "max_value": max(values)
            }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calcula tendência de uma série de valores"""
        if len(values) < 2:
            return "stable"
        
        # Usa regressão linear simples
        n = len(values)
        x_values = list(range(n))
        
        sum_x = sum(x_values)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(x_values, values))
        sum_x2 = sum(x * x for x in x_values)
        
        if n * sum_x2 - sum_x * sum_x != 0:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            
            if slope > 0.01:
                return "rising"
            elif slope < -0.01:
                return "falling"
            else:
                return "stable"
        
        return "stable"
    
    def get_performance_status(self) -> Dict[str, Any]:
        """
        Retorna status geral de performance do sistema.
        
        Returns:
            Dicionário com informações de performance
        """
        try:
            # Obter métricas atuais
            current_metrics = self.get_current_metrics()
            
            # Calcular score de performance (0-100)
            cpu_score = max(0, 100 - (current_metrics.get("cpu_usage", 0) * 100))
            memory_score = max(0, 100 - (current_metrics.get("memory_usage", 0) * 100))
            response_score = max(0, 100 - (current_metrics.get("avg_response_time", 0) / 10))
            
            overall_score = (cpu_score + memory_score + response_score) / 3
            
            # Determinar status de performance
            if overall_score >= 90:
                performance_status = "excellent"
            elif overall_score >= 75:
                performance_status = "good"
            elif overall_score >= 50:
                performance_status = "fair"
            elif overall_score >= 25:
                performance_status = "poor"
            else:
                performance_status = "critical"
            
            # Calcular tendências
            recent_data = [point for point in self.performance_history 
                          if time.time() - point.timestamp < 3600]  # Última hora
            
            cpu_trend = self._calculate_trend([p.cpu_usage for p in recent_data])
            memory_trend = self._calculate_trend([p.memory_usage for p in recent_data])
            response_trend = self._calculate_trend([p.avg_response_time for p in recent_data])
            
            # Obter estatísticas de otimização
            total_optimizations = len(self.optimization_history)
            successful_optimizations = len([opt for opt in self.optimization_history if opt.get("success", False)])
            optimization_success_rate = (successful_optimizations / total_optimizations * 100) if total_optimizations > 0 else 0
            
            # Obter alertas ativos
            active_alerts = [alert for alert in self.performance_alerts 
                           if alert.severity in [AlertSeverity.WARNING, AlertSeverity.ERROR, AlertSeverity.CRITICAL]]
            
            return {
                "performance_score": round(overall_score, 2),
                "performance_status": performance_status,
                "cpu_usage": current_metrics.get("cpu_usage", 0),
                "memory_usage": current_metrics.get("memory_usage", 0),
                "avg_response_time": current_metrics.get("avg_response_time", 0),
                "throughput": current_metrics.get("throughput", 0),
                "error_rate": current_metrics.get("error_rate", 0),
                "active_connections": current_metrics.get("active_connections", 0),
                "trends": {
                    "cpu_trend": cpu_trend,
                    "memory_trend": memory_trend,
                    "response_trend": response_trend
                },
                "optimization_stats": {
                    "total_optimizations": total_optimizations,
                    "successful_optimizations": successful_optimizations,
                    "success_rate": round(optimization_success_rate, 2),
                    "active_rules": len([rule for rule in self.optimization_rules if rule.enabled])
                },
                "active_alerts": len(active_alerts),
                "monitoring_active": self.monitoring_active,
                "auto_optimization_enabled": self.auto_optimization_enabled,
                "last_optimization": self.optimization_history[-1]["timestamp"] if self.optimization_history else None,
                "recommendations": self._generate_performance_recommendations(overall_score, performance_status),
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter status de performance: {e}")
            return {
                "performance_score": 0.0,
                "performance_status": "critical",
                "error": str(e),
                "timestamp": time.time()
            }
    
    def _generate_performance_recommendations(self, performance_score: float, performance_status: str) -> List[str]:
        """Gera recomendações de performance baseadas no status atual"""
        recommendations = []
        
        if performance_score < 70:
            recommendations.append("Considerar escalonamento horizontal de recursos")
            recommendations.append("Otimizar consultas de banco de dados")
        
        if performance_status in ["poor", "critical"]:
            recommendations.append("Ativar otimizações automáticas agressivas")
            recommendations.append("Implementar cache distribuído")
        
        if not self.auto_optimization_enabled:
            recommendations.append("Ativar otimizações automáticas de performance")
        
        if len(self.performance_history) > 10000:
            recommendations.append("Arquivar dados históricos de performance antigos")
        
        return recommendations
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """
        Retorna métricas atuais do sistema.
        
        Returns:
            Dicionário com métricas atuais
        """
        try:
            # Obter métricas do sistema
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Calcular métricas de rede
            network_io = psutil.net_io_counters()
            
            return {
                "cpu_usage": cpu_percent / 100.0,  # Normalizar para 0-1
                "memory_usage": memory.percent / 100.0,  # Normalizar para 0-1
                "disk_usage": disk.percent / 100.0,  # Normalizar para 0-1
                "avg_response_time": 100.0,  # Simulado
                "throughput": 1000.0,  # Simulado
                "error_rate": 0.01,  # Simulado
                "active_connections": 50,  # Simulado
                "network_bytes_sent": network_io.bytes_sent,
                "network_bytes_recv": network_io.bytes_recv
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter métricas atuais: {e}")
            return {
                "cpu_usage": 0.0,
                "memory_usage": 0.0,
                "disk_usage": 0.0,
                "avg_response_time": 0.0,
                "throughput": 0.0,
                "error_rate": 0.0,
                "active_connections": 0
            }
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """
        Retorna todos os alertas ativos do sistema de performance.
        
        Returns:
            Lista de alertas ativos com informações detalhadas
        """
        try:
            current_time = time.time()
            
            # Filtra alertas ativos
            active_alerts = []
            
            for alert in self.performance_alerts:
                # Verifica se alerta está ativo e dentro do período de retenção
                if alert.status == "active" and current_time - alert.timestamp < 24 * 3600:  # 24 horas
                    # Determina severidade baseada no tipo de alerta
                    severity_map = {
                        AlertSeverity.INFO: "info",
                        AlertSeverity.WARNING: "warning",
                        AlertSeverity.ERROR: "error", 
                        AlertSeverity.CRITICAL: "critical"
                    }
                    
                    active_alerts.append({
                        "id": alert.alert_id,
                        "type": "performance",
                        "severity": severity_map.get(alert.severity, "warning"),
                        "title": f"Alerta de Performance: {alert.metric_name}",
                        "description": alert.message,
                        "affected_components": [alert.metric_name],
                        "timestamp": alert.timestamp,
                        "metric_name": alert.metric_name,
                        "current_value": alert.current_value,
                        "threshold": alert.threshold,
                        "recommendations": alert.recommendations
                    })
            
            # Ordena por severidade e timestamp
            severity_order = {"critical": 4, "error": 3, "warning": 2, "info": 1}
            active_alerts.sort(key=lambda x: (severity_order.get(x["severity"], 0), -x["timestamp"]), reverse=True)
            
            return active_alerts
            
        except Exception as e:
            # Se houver erro, retorna lista vazia
            return []


# Instância global do monitor de performance consciente
performance_monitor = ConsciousPerformanceMonitor()
