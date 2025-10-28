"""
Sistema de Monitoramento Avançado para CoinBalance Enterprise
============================================================

Este módulo implementa um sistema de monitoramento avançado com métricas
customizadas, alertas inteligentes e dashboards em tempo real para
o CoinBalance Enterprise.
"""

import asyncio
import time
import logging
import psutil
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict, deque
import threading

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Tipos de métricas"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


class AlertLevel(Enum):
    """Níveis de alerta"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class Metric:
    """Representa uma métrica"""
    name: str
    value: float
    timestamp: float
    tags: Dict[str, str] = field(default_factory=dict)
    metric_type: MetricType = MetricType.GAUGE


@dataclass
class Alert:
    """Representa um alerta"""
    name: str
    level: AlertLevel
    message: str
    timestamp: float
    metric_name: str
    threshold: float
    current_value: float
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class AlertRule:
    """Regra de alerta"""
    name: str
    metric_name: str
    condition: str  # ">", "<", ">=", "<=", "==", "!="
    threshold: float
    level: AlertLevel
    enabled: bool = True
    cooldown: int = 300  # Cooldown em segundos


class MetricsCollector:
    """Coletor de métricas do sistema"""
    
    def __init__(self):
        self.metrics: deque = deque(maxlen=10000)  # Mantém últimas 10k métricas
        self.counters: Dict[str, float] = defaultdict(float)
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        self.timers: Dict[str, List[float]] = defaultdict(list)
        
        logger.info("MetricsCollector inicializado")
    
    def increment_counter(self, name: str, value: float = 1.0, tags: Dict[str, str] = None):
        """Incrementa um contador"""
        self.counters[name] += value
        self._record_metric(name, self.counters[name], MetricType.COUNTER, tags)
    
    def set_gauge(self, name: str, value: float, tags: Dict[str, str] = None):
        """Define um gauge"""
        self.gauges[name] = value
        self._record_metric(name, value, MetricType.GAUGE, tags)
    
    def record_histogram(self, name: str, value: float, tags: Dict[str, str] = None):
        """Registra um valor em histograma"""
        self.histograms[name].append(value)
        # Mantém apenas os últimos 1000 valores
        if len(self.histograms[name]) > 1000:
            self.histograms[name] = self.histograms[name][-1000:]
        
        self._record_metric(name, value, MetricType.HISTOGRAM, tags)
    
    def record_timer(self, name: str, duration: float, tags: Dict[str, str] = None):
        """Registra um tempo"""
        self.timers[name].append(duration)
        # Mantém apenas os últimos 1000 valores
        if len(self.timers[name]) > 1000:
            self.timers[name] = self.timers[name][-1000:]
        
        self._record_metric(name, duration, MetricType.TIMER, tags)
    
    def _record_metric(self, name: str, value: float, metric_type: MetricType, tags: Dict[str, str] = None):
        """Registra uma métrica"""
        metric = Metric(
            name=name,
            value=value,
            timestamp=time.time(),
            tags=tags or {},
            metric_type=metric_type
        )
        self.metrics.append(metric)
    
    def get_metric_summary(self, name: str, metric_type: MetricType) -> Dict[str, Any]:
        """Retorna resumo de uma métrica"""
        if metric_type == MetricType.COUNTER:
            return {"value": self.counters.get(name, 0)}
        elif metric_type == MetricType.GAUGE:
            return {"value": self.gauges.get(name, 0)}
        elif metric_type == MetricType.HISTOGRAM:
            values = self.histograms.get(name, [])
            if not values:
                return {"count": 0, "min": 0, "max": 0, "avg": 0, "p95": 0, "p99": 0}
            
            sorted_values = sorted(values)
            count = len(values)
            return {
                "count": count,
                "min": min(values),
                "max": max(values),
                "avg": sum(values) / count,
                "p95": sorted_values[int(count * 0.95)] if count > 0 else 0,
                "p99": sorted_values[int(count * 0.99)] if count > 0 else 0
            }
        elif metric_type == MetricType.TIMER:
            values = self.timers.get(name, [])
            if not values:
                return {"count": 0, "min": 0, "max": 0, "avg": 0, "p95": 0, "p99": 0}
            
            sorted_values = sorted(values)
            count = len(values)
            return {
                "count": count,
                "min": min(values),
                "max": max(values),
                "avg": sum(values) / count,
                "p95": sorted_values[int(count * 0.95)] if count > 0 else 0,
                "p99": sorted_values[int(count * 0.99)] if count > 0 else 0
            }
        
        return {}


class SystemMetricsCollector:
    """Coletor de métricas do sistema operacional"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.running = False
        self.collection_task = None
        
        logger.info("SystemMetricsCollector inicializado")
    
    async def start(self):
        """Inicia coleta de métricas do sistema"""
        if self.running:
            return
        
        self.running = True
        self.collection_task = asyncio.create_task(self._collect_system_metrics())
        logger.info("Coleta de métricas do sistema iniciada")
    
    async def stop(self):
        """Para coleta de métricas do sistema"""
        if not self.running:
            return
        
        self.running = False
        if self.collection_task:
            self.collection_task.cancel()
            try:
                await self.collection_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Coleta de métricas do sistema parada")
    
    async def _collect_system_metrics(self):
        """Coleta métricas do sistema em loop"""
        while self.running:
            try:
                # CPU
                cpu_percent = psutil.cpu_percent(interval=1)
                self.metrics_collector.set_gauge("system.cpu.usage", cpu_percent)
                
                # Memória
                memory = psutil.virtual_memory()
                self.metrics_collector.set_gauge("system.memory.usage", memory.percent)
                self.metrics_collector.set_gauge("system.memory.available", memory.available)
                self.metrics_collector.set_gauge("system.memory.used", memory.used)
                
                # Disco
                disk = psutil.disk_usage('/')
                self.metrics_collector.set_gauge("system.disk.usage", disk.percent)
                self.metrics_collector.set_gauge("system.disk.free", disk.free)
                self.metrics_collector.set_gauge("system.disk.used", disk.used)
                
                # Rede
                network = psutil.net_io_counters()
                self.metrics_collector.set_gauge("system.network.bytes_sent", network.bytes_sent)
                self.metrics_collector.set_gauge("system.network.bytes_recv", network.bytes_recv)
                self.metrics_collector.set_gauge("system.network.packets_sent", network.packets_sent)
                self.metrics_collector.set_gauge("system.network.packets_recv", network.packets_recv)
                
                # Processos
                process = psutil.Process()
                self.metrics_collector.set_gauge("system.process.cpu_percent", process.cpu_percent())
                self.metrics_collector.set_gauge("system.process.memory_percent", process.memory_percent())
                self.metrics_collector.set_gauge("system.process.memory_rss", process.memory_info().rss)
                self.metrics_collector.set_gauge("system.process.memory_vms", process.memory_info().vms)
                
                await asyncio.sleep(10)  # Coleta a cada 10 segundos
                
            except Exception as e:
                logger.error(f"Erro ao coletar métricas do sistema: {e}")
                await asyncio.sleep(10)


class AlertManager:
    """Gerenciador de alertas"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.alert_rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: deque = deque(maxlen=1000)
        self.last_alert_time: Dict[str, float] = {}
        
        logger.info("AlertManager inicializado")
    
    def add_alert_rule(self, rule: AlertRule):
        """Adiciona uma regra de alerta"""
        self.alert_rules[rule.name] = rule
        logger.info(f"Regra de alerta '{rule.name}' adicionada")
    
    def remove_alert_rule(self, rule_name: str):
        """Remove uma regra de alerta"""
        if rule_name in self.alert_rules:
            del self.alert_rules[rule_name]
            logger.info(f"Regra de alerta '{rule_name}' removida")
    
    def check_alerts(self):
        """Verifica todas as regras de alerta"""
        for rule_name, rule in self.alert_rules.items():
            if not rule.enabled:
                continue
            
            # Verifica cooldown
            if rule_name in self.last_alert_time:
                time_since_last = time.time() - self.last_alert_time[rule_name]
                if time_since_last < rule.cooldown:
                    continue
            
            # Obtém valor atual da métrica
            current_value = self._get_metric_value(rule.metric_name)
            if current_value is None:
                continue
            
            # Verifica condição
            if self._evaluate_condition(current_value, rule.condition, rule.threshold):
                self._trigger_alert(rule, current_value)
    
    def _get_metric_value(self, metric_name: str) -> Optional[float]:
        """Obtém valor atual de uma métrica"""
        # Tenta obter do gauge primeiro
        if metric_name in self.metrics_collector.gauges:
            return self.metrics_collector.gauges[metric_name]
        
        # Tenta obter do counter
        if metric_name in self.metrics_collector.counters:
            return self.metrics_collector.counters[metric_name]
        
        return None
    
    def _evaluate_condition(self, value: float, condition: str, threshold: float) -> bool:
        """Avalia condição de alerta"""
        if condition == ">":
            return value > threshold
        elif condition == "<":
            return value < threshold
        elif condition == ">=":
            return value >= threshold
        elif condition == "<=":
            return value <= threshold
        elif condition == "==":
            return value == threshold
        elif condition == "!=":
            return value != threshold
        
        return False
    
    def _trigger_alert(self, rule: AlertRule, current_value: float):
        """Dispara um alerta"""
        alert = Alert(
            name=rule.name,
            level=rule.level,
            message=f"Métrica '{rule.metric_name}' {rule.condition} {rule.threshold} (atual: {current_value})",
            timestamp=time.time(),
            metric_name=rule.metric_name,
            threshold=rule.threshold,
            current_value=current_value
        )
        
        self.active_alerts[rule.name] = alert
        self.alert_history.append(alert)
        self.last_alert_time[rule.name] = time.time()
        
        logger.warning(f"ALERTA {rule.level.value.upper()}: {alert.message}")
    
    def get_active_alerts(self) -> List[Alert]:
        """Retorna alertas ativos"""
        return list(self.active_alerts.values())
    
    def get_alert_history(self, limit: int = 100) -> List[Alert]:
        """Retorna histórico de alertas"""
        return list(self.alert_history)[-limit:]


class CoinBalanceMonitoringSystem:
    """Sistema de monitoramento principal do CoinBalance Enterprise"""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.system_collector = SystemMetricsCollector(self.metrics_collector)
        self.alert_manager = AlertManager(self.metrics_collector)
        self.running = False
        
        # Configura alertas padrão
        self._setup_default_alerts()
        
        logger.info("CoinBalance Monitoring System inicializado")
    
    def _setup_default_alerts(self):
        """Configura alertas padrão do sistema"""
        default_alerts = [
            AlertRule("high_cpu", "system.cpu.usage", ">", 80.0, AlertLevel.WARNING),
            AlertRule("critical_cpu", "system.cpu.usage", ">", 95.0, AlertLevel.CRITICAL),
            AlertRule("high_memory", "system.memory.usage", ">", 85.0, AlertLevel.WARNING),
            AlertRule("critical_memory", "system.memory.usage", ">", 95.0, AlertLevel.CRITICAL),
            AlertRule("high_disk", "system.disk.usage", ">", 90.0, AlertLevel.WARNING),
            AlertRule("critical_disk", "system.disk.usage", ">", 95.0, AlertLevel.CRITICAL),
        ]
        
        for alert in default_alerts:
            self.alert_manager.add_alert_rule(alert)
    
    async def start(self):
        """Inicia o sistema de monitoramento"""
        if self.running:
            return
        
        self.running = True
        await self.system_collector.start()
        
        # Inicia verificação de alertas
        asyncio.create_task(self._alert_check_loop())
        
        logger.info("Sistema de monitoramento CoinBalance iniciado")
    
    async def stop(self):
        """Para o sistema de monitoramento"""
        if not self.running:
            return
        
        self.running = False
        await self.system_collector.stop()
        
        logger.info("Sistema de monitoramento CoinBalance parado")
    
    async def _alert_check_loop(self):
        """Loop de verificação de alertas"""
        while self.running:
            try:
                self.alert_manager.check_alerts()
                await asyncio.sleep(30)  # Verifica alertas a cada 30 segundos
            except Exception as e:
                logger.error(f"Erro na verificação de alertas: {e}")
                await asyncio.sleep(30)
    
    def record_blockchain_metric(self, name: str, value: float, tags: Dict[str, str] = None):
        """Registra métrica específica da blockchain"""
        self.metrics_collector.set_gauge(f"blockchain.{name}", value, tags)
    
    def record_api_metric(self, endpoint: str, response_time: float, status_code: int):
        """Registra métrica de API"""
        tags = {"endpoint": endpoint, "status_code": str(status_code)}
        self.metrics_collector.record_timer(f"api.response_time", response_time, tags)
        self.metrics_collector.increment_counter(f"api.requests", tags=tags)
    
    def record_transaction_metric(self, transaction_type: str, amount: float):
        """Registra métrica de transação"""
        tags = {"type": transaction_type}
        self.metrics_collector.record_histogram("transaction.amount", amount, tags)
        self.metrics_collector.increment_counter("transaction.count", tags=tags)
    
    def get_system_health(self) -> Dict[str, Any]:
        """Retorna saúde geral do sistema"""
        active_alerts = self.alert_manager.get_active_alerts()
        critical_alerts = [a for a in active_alerts if a.level == AlertLevel.CRITICAL]
        warning_alerts = [a for a in active_alerts if a.level == AlertLevel.WARNING]
        
        health_status = "healthy"
        if critical_alerts:
            health_status = "critical"
        elif warning_alerts:
            health_status = "warning"
        
        return {
            "status": health_status,
            "active_alerts": len(active_alerts),
            "critical_alerts": len(critical_alerts),
            "warning_alerts": len(warning_alerts),
            "timestamp": time.time()
        }
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Retorna resumo de todas as métricas"""
        summary = {
            "system": {},
            "blockchain": {},
            "api": {},
            "transaction": {}
        }
        
        # Métricas do sistema
        for metric_name in ["cpu.usage", "memory.usage", "disk.usage"]:
            summary["system"][metric_name] = self.metrics_collector.get_metric_summary(
                f"system.{metric_name}", MetricType.GAUGE
            )
        
        # Métricas da API
        summary["api"]["response_time"] = self.metrics_collector.get_metric_summary(
            "api.response_time", MetricType.TIMER
        )
        
        return summary


# Instância global do sistema de monitoramento
monitoring_system = CoinBalanceMonitoringSystem()


# Decorators para facilitar o uso
def monitor_performance(metric_name: str):
    """Decorator para monitorar performance de funções"""
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                monitoring_system.metrics_collector.record_timer(metric_name, duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                monitoring_system.metrics_collector.record_timer(f"{metric_name}.error", duration)
                raise
        
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                monitoring_system.metrics_collector.record_timer(metric_name, duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                monitoring_system.metrics_collector.record_timer(f"{metric_name}.error", duration)
                raise
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def monitor_counter(metric_name: str):
    """Decorator para monitorar contadores"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            monitoring_system.metrics_collector.increment_counter(metric_name)
            return result
        return wrapper
    return decorator
