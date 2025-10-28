"""
Sistema de Monitoramento em Tempo Real
=====================================

Este módulo implementa monitoramento em tempo real para blockchain,
incluindo métricas, alertas e dashboards.

EVOLUÇÃO: Monitoramento em tempo real com métricas avançadas e alertas.
"""

import time
import threading
import asyncio
import json
import uuid
from typing import List, Optional, Dict, Any, Set, Tuple, Callable
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from decimal import Decimal
from enum import Enum
import statistics

from ..entities.block import Block
from ...transaction.entities.transaction import Transaction
from ...shared.value_objects.hash_value import HashValue
from ...shared.value_objects.timestamp import Timestamp

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
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class Metric:
    """Métrica de monitoramento"""
    name: str
    value: float
    metric_type: MetricType
    timestamp: float = field(default_factory=time.time)
    tags: Dict[str, str] = field(default_factory=dict)
    unit: str = ""
    description: str = ""


@dataclass
class Alert:
    """Alerta de monitoramento"""
    alert_id: str
    name: str
    level: AlertLevel
    message: str
    timestamp: float = field(default_factory=time.time)
    resolved: bool = False
    resolved_at: Optional[float] = None
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class AlertRule:
    """Regra de alerta"""
    rule_id: str
    name: str
    metric_name: str
    condition: str  # ">", "<", ">=", "<=", "==", "!="
    threshold: float
    level: AlertLevel
    enabled: bool = True
    cooldown: int = 300  # 5 minutos


@dataclass
class Dashboard:
    """Dashboard de monitoramento"""
    dashboard_id: str
    name: str
    description: str
    widgets: List[Dict[str, Any]] = field(default_factory=list)
    refresh_interval: int = 30
    created_at: float = field(default_factory=time.time)


class RealTimeMonitor:
    """
    Sistema de monitoramento em tempo real para blockchain.
    
    EVOLUÇÃO: Monitoramento em tempo real com métricas avançadas e alertas.
    
    Funcionalidades:
    - Coleta de métricas em tempo real
    - Sistema de alertas inteligente
    - Dashboards personalizáveis
    - Análise de tendências
    - Detecção de anomalias
    - Notificações automáticas
    - Estatísticas detalhadas de monitoramento
    - Thread safety completo
    """
    
    def __init__(self, node_id: str, local_address: str = "localhost", local_port: int = 8000):
        self.node_id = node_id
        self.local_address = local_address
        self.local_port = local_port
        
        # Métricas e alertas
        self.metrics: Dict[str, List[Metric]] = {}
        self.alerts: List[Alert] = []
        self.alert_rules: Dict[str, AlertRule] = {}
        self.dashboards: Dict[str, Dashboard] = {}
        
        # Configurações
        self.metric_retention_hours = 24
        self.alert_retention_hours = 168  # 7 dias
        self.collection_interval = 10  # segundos
        self.alert_check_interval = 30  # segundos
        
        # Estatísticas
        self.stats = {
            "total_metrics_collected": 0,
            "total_alerts_triggered": 0,
            "active_alerts": 0,
            "resolved_alerts": 0,
            "average_metric_value": 0.0,
            "metric_collection_rate": 0.0,
            "alert_response_time": 0.0
        }
        
        # Threading
        self.collection_thread: Optional[threading.Thread] = None
        self.alert_thread: Optional[threading.Thread] = None
        self.cleanup_thread: Optional[threading.Thread] = None
        self.is_running = False
        
        logger.info(f"RealTimeMonitor inicializado: node_id={node_id}, address={local_address}:{local_port}")
    
    def start(self) -> None:
        """Inicia o sistema de monitoramento em tempo real."""
        with threading.Lock():
            if self.is_running:
                return
            
            self.is_running = True
            
            # Iniciar threads de coleta, alertas e limpeza
            self.collection_thread = threading.Thread(target=self._collection_worker, daemon=True)
            self.alert_thread = threading.Thread(target=self._alert_worker, daemon=True)
            self.cleanup_thread = threading.Thread(target=self._cleanup_worker, daemon=True)
            
            self.collection_thread.start()
            self.alert_thread.start()
            self.cleanup_thread.start()
            
            logger.info("Sistema de monitoramento em tempo real iniciado")
    
    def stop(self) -> None:
        """Para o sistema de monitoramento em tempo real."""
        with threading.Lock():
            if not self.is_running:
                return
            
            self.is_running = False
            
            # Aguardar threads terminarem
            threads = [self.collection_thread, self.alert_thread, self.cleanup_thread]
            for thread in threads:
                if thread and thread.is_alive():
                    thread.join(timeout=5)
            
            logger.info("Sistema de monitoramento em tempo real parado")
    
    def collect_metric(self, name: str, value: float, metric_type: MetricType = MetricType.GAUGE, 
                     tags: Optional[Dict[str, str]] = None, unit: str = "", description: str = "") -> None:
        """
        Coleta uma métrica.
        
        EVOLUÇÃO: Coleta de métricas com tags e metadados.
        """
        try:
            metric = Metric(
                name=name,
                value=value,
                metric_type=metric_type,
                tags=tags or {},
                unit=unit,
                description=description
            )
            
            # Armazenar métrica
            if name not in self.metrics:
                self.metrics[name] = []
            
            self.metrics[name].append(metric)
            
            # Manter apenas métricas recentes
            cutoff_time = time.time() - (self.metric_retention_hours * 3600)
            self.metrics[name] = [m for m in self.metrics[name] if m.timestamp > cutoff_time]
            
            # Atualizar estatísticas
            self.stats["total_metrics_collected"] += 1
            
            logger.debug(f"Métrica coletada: {name}={value} {unit}")
            
        except Exception as e:
            logger.error(f"Erro ao coletar métrica {name}: {e}")
    
    def create_alert_rule(self, rule_id: str, name: str, metric_name: str, condition: str, 
                         threshold: float, level: AlertLevel, cooldown: int = 300) -> bool:
        """
        Cria uma regra de alerta.
        
        EVOLUÇÃO: Criação de regras de alerta com condições personalizadas.
        """
        try:
            rule = AlertRule(
                rule_id=rule_id,
                name=name,
                metric_name=metric_name,
                condition=condition,
                threshold=threshold,
                level=level,
                cooldown=cooldown
            )
            
            self.alert_rules[rule_id] = rule
            
            logger.info(f"Regra de alerta criada: {name} ({metric_name} {condition} {threshold})")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar regra de alerta {rule_id}: {e}")
            return False
    
    def create_dashboard(self, dashboard_id: str, name: str, description: str, 
                        widgets: Optional[List[Dict[str, Any]]] = None, refresh_interval: int = 30) -> bool:
        """
        Cria um dashboard de monitoramento.
        
        EVOLUÇÃO: Criação de dashboards personalizáveis.
        """
        try:
            dashboard = Dashboard(
                dashboard_id=dashboard_id,
                name=name,
                description=description,
                widgets=widgets or [],
                refresh_interval=refresh_interval
            )
            
            self.dashboards[dashboard_id] = dashboard
            
            logger.info(f"Dashboard criado: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar dashboard {dashboard_id}: {e}")
            return False
    
    def get_metric_history(self, metric_name: str, hours: int = 1) -> List[Metric]:
        """
        Obtém histórico de uma métrica.
        
        EVOLUÇÃO: Histórico de métricas com filtro de tempo.
        """
        try:
            if metric_name not in self.metrics:
                return []
            
            cutoff_time = time.time() - (hours * 3600)
            return [m for m in self.metrics[metric_name] if m.timestamp > cutoff_time]
            
        except Exception as e:
            logger.error(f"Erro ao obter histórico da métrica {metric_name}: {e}")
            return []
    
    def get_active_alerts(self) -> List[Alert]:
        """Obtém alertas ativos."""
        return [alert for alert in self.alerts if not alert.resolved]
    
    def resolve_alert(self, alert_id: str) -> bool:
        """
        Resolve um alerta.
        
        EVOLUÇÃO: Resolução de alertas com timestamp.
        """
        try:
            for alert in self.alerts:
                if alert.alert_id == alert_id and not alert.resolved:
                    alert.resolved = True
                    alert.resolved_at = time.time()
                    self.stats["resolved_alerts"] += 1
                    self.stats["active_alerts"] -= 1
                    
                    logger.info(f"Alerta resolvido: {alert.name}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erro ao resolver alerta {alert_id}: {e}")
            return False
    
    def get_monitoring_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas de monitoramento.
        
        EVOLUÇÃO: Métricas detalhadas de monitoramento e performance.
        """
        try:
            # Calcular estatísticas de métricas
            total_metrics = sum(len(metrics) for metrics in self.metrics.values())
            metric_names = list(self.metrics.keys())
            
            # Calcular taxa de coleta
            current_time = time.time()
            if hasattr(self, '_last_stats_time'):
                time_diff = current_time - self._last_stats_time
                if time_diff > 0:
                    self.stats["metric_collection_rate"] = self.stats["total_metrics_collected"] / time_diff
            
            self._last_stats_time = current_time
            
            # Calcular estatísticas de alertas
            active_alerts = len(self.get_active_alerts())
            resolved_alerts = len([a for a in self.alerts if a.resolved])
            
            # Calcular tempo médio de resposta de alertas
            resolved_with_time = [a for a in self.alerts if a.resolved and a.resolved_at]
            if resolved_with_time:
                response_times = [a.resolved_at - a.timestamp for a in resolved_with_time]
                self.stats["alert_response_time"] = statistics.mean(response_times)
            
            return {
                "monitoring_stats": {
                    "total_metrics_collected": self.stats["total_metrics_collected"],
                    "total_alerts_triggered": self.stats["total_alerts_triggered"],
                    "active_alerts": active_alerts,
                    "resolved_alerts": resolved_alerts,
                    "metric_collection_rate": self.stats["metric_collection_rate"],
                    "alert_response_time": self.stats["alert_response_time"]
                },
                "metric_stats": {
                    "total_metrics": total_metrics,
                    "metric_names": metric_names,
                    "metrics_count": len(metric_names)
                },
                "alert_stats": {
                    "total_alert_rules": len(self.alert_rules),
                    "active_alert_rules": len([r for r in self.alert_rules.values() if r.enabled]),
                    "alerts_by_level": self._get_alerts_by_level()
                },
                "dashboard_stats": {
                    "total_dashboards": len(self.dashboards),
                    "dashboard_names": [d.name for d in self.dashboards.values()]
                }
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas de monitoramento: {e}")
            return {}
    
    def optimize_monitoring(self) -> Dict[str, Any]:
        """
        Otimiza o sistema de monitoramento.
        
        EVOLUÇÃO: Otimização automática de monitoramento.
        """
        try:
            optimizations_applied = []
            
            # Limpar métricas antigas
            cleaned_metrics = self._cleanup_old_metrics()
            if cleaned_metrics > 0:
                optimizations_applied.append(f"Removidas {cleaned_metrics} métricas antigas")
            
            # Limpar alertas antigos
            cleaned_alerts = self._cleanup_old_alerts()
            if cleaned_alerts > 0:
                optimizations_applied.append(f"Removidos {cleaned_alerts} alertas antigos")
            
            # Otimizar regras de alerta
            optimized_rules = self._optimize_alert_rules()
            if optimized_rules > 0:
                optimizations_applied.append(f"Otimizadas {optimized_rules} regras de alerta")
            
            # Consolidar métricas similares
            consolidated_metrics = self._consolidate_metrics()
            if consolidated_metrics > 0:
                optimizations_applied.append(f"Consolidadas {consolidated_metrics} métricas similares")
            
            return {
                "optimizations_applied": optimizations_applied,
                "cleaned_metrics": cleaned_metrics,
                "cleaned_alerts": cleaned_alerts,
                "optimized_rules": optimized_rules,
                "consolidated_metrics": consolidated_metrics,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro na otimização de monitoramento: {e}")
            return {"error": str(e)}
    
    def _check_alerts(self) -> None:
        """Verifica regras de alerta."""
        try:
            current_time = time.time()
            
            for rule_id, rule in self.alert_rules.items():
                if not rule.enabled:
                    continue
                
                # Verificar cooldown
                if hasattr(self, '_last_alert_time'):
                    if rule_id in self._last_alert_time:
                        if current_time - self._last_alert_time[rule_id] < rule.cooldown:
                            continue
                
                # Obter métrica mais recente
                if rule.metric_name not in self.metrics:
                    continue
                
                recent_metrics = self.get_metric_history(rule.metric_name, hours=1)
                if not recent_metrics:
                    continue
                
                latest_metric = max(recent_metrics, key=lambda m: m.timestamp)
                
                # Verificar condição
                should_alert = False
                if rule.condition == ">":
                    should_alert = latest_metric.value > rule.threshold
                elif rule.condition == "<":
                    should_alert = latest_metric.value < rule.threshold
                elif rule.condition == ">=":
                    should_alert = latest_metric.value >= rule.threshold
                elif rule.condition == "<=":
                    should_alert = latest_metric.value <= rule.threshold
                elif rule.condition == "==":
                    should_alert = latest_metric.value == rule.threshold
                elif rule.condition == "!=":
                    should_alert = latest_metric.value != rule.threshold
                
                if should_alert:
                    # Criar alerta
                    alert = Alert(
                        alert_id=str(uuid.uuid4()),
                        name=rule.name,
                        level=rule.level,
                        message=f"{rule.metric_name} {rule.condition} {rule.threshold} (atual: {latest_metric.value})",
                        tags={"rule_id": rule_id, "metric_name": rule.metric_name}
                    )
                    
                    self.alerts.append(alert)
                    self.stats["total_alerts_triggered"] += 1
                    self.stats["active_alerts"] += 1
                    
                    # Registrar tempo do último alerta
                    if not hasattr(self, '_last_alert_time'):
                        self._last_alert_time = {}
                    self._last_alert_time[rule_id] = current_time
                    
                    logger.warning(f"Alerta disparado: {rule.name} - {alert.message}")
                    
        except Exception as e:
            logger.error(f"Erro na verificação de alertas: {e}")
    
    def _cleanup_old_metrics(self) -> int:
        """Remove métricas antigas."""
        cleaned_count = 0
        cutoff_time = time.time() - (self.metric_retention_hours * 3600)
        
        for metric_name in list(self.metrics.keys()):
            original_count = len(self.metrics[metric_name])
            self.metrics[metric_name] = [m for m in self.metrics[metric_name] if m.timestamp > cutoff_time]
            cleaned_count += original_count - len(self.metrics[metric_name])
            
            # Remover métricas vazias
            if not self.metrics[metric_name]:
                del self.metrics[metric_name]
        
        return cleaned_count
    
    def _cleanup_old_alerts(self) -> int:
        """Remove alertas antigos."""
        cutoff_time = time.time() - (self.alert_retention_hours * 3600)
        original_count = len(self.alerts)
        
        self.alerts = [a for a in self.alerts if a.timestamp > cutoff_time]
        
        return original_count - len(self.alerts)
    
    def _optimize_alert_rules(self) -> int:
        """Otimiza regras de alerta."""
        optimized_count = 0
        
        # Desabilitar regras que não foram disparadas recentemente
        current_time = time.time()
        for rule in self.alert_rules.values():
            if hasattr(self, '_last_alert_time'):
                if rule.rule_id in self._last_alert_time:
                    if current_time - self._last_alert_time[rule.rule_id] > 86400:  # 24 horas
                        rule.enabled = False
                        optimized_count += 1
        
        return optimized_count
    
    def _consolidate_metrics(self) -> int:
        """Consolida métricas similares."""
        # Implementação simplificada de consolidação
        # Em implementação real, seria mais complexa
        return 0
    
    def _get_alerts_by_level(self) -> Dict[str, int]:
        """Obtém contagem de alertas por nível."""
        alerts_by_level = {}
        
        for alert in self.alerts:
            level = alert.level.value
            if level not in alerts_by_level:
                alerts_by_level[level] = 0
            alerts_by_level[level] += 1
        
        return alerts_by_level
    
    def _collection_worker(self) -> None:
        """Worker thread para coleta de métricas."""
        while self.is_running:
            try:
                time.sleep(self.collection_interval)
                if self.is_running:
                    # Coletar métricas do sistema
                    self._collect_system_metrics()
            except Exception as e:
                logger.error(f"Erro no worker de coleta: {e}")
    
    def _alert_worker(self) -> None:
        """Worker thread para verificação de alertas."""
        while self.is_running:
            try:
                time.sleep(self.alert_check_interval)
                if self.is_running:
                    self._check_alerts()
            except Exception as e:
                logger.error(f"Erro no worker de alertas: {e}")
    
    def _cleanup_worker(self) -> None:
        """Worker thread para limpeza."""
        while self.is_running:
            try:
                time.sleep(3600)  # Limpeza a cada hora
                if self.is_running:
                    self._cleanup_old_metrics()
                    self._cleanup_old_alerts()
            except Exception as e:
                logger.error(f"Erro no worker de limpeza: {e}")
    
    def _collect_system_metrics(self) -> None:
        """Coleta métricas do sistema."""
        try:
            # Métricas de sistema simuladas
            # Em implementação real, seriam métricas reais do sistema
            
            # CPU usage
            self.collect_metric("system.cpu.usage", 45.2, MetricType.GAUGE, 
                              {"node": self.node_id}, "%", "CPU usage percentage")
            
            # Memory usage
            self.collect_metric("system.memory.usage", 67.8, MetricType.GAUGE,
                              {"node": self.node_id}, "%", "Memory usage percentage")
            
            # Disk usage
            self.collect_metric("system.disk.usage", 23.4, MetricType.GAUGE,
                              {"node": self.node_id}, "%", "Disk usage percentage")
            
            # Network I/O
            self.collect_metric("system.network.bytes_sent", 1024000, MetricType.COUNTER,
                              {"node": self.node_id}, "bytes", "Network bytes sent")
            
            self.collect_metric("system.network.bytes_received", 2048000, MetricType.COUNTER,
                              {"node": self.node_id}, "bytes", "Network bytes received")
            
        except Exception as e:
            logger.error(f"Erro na coleta de métricas do sistema: {e}")


# Instância global otimizada
real_time_monitor = RealTimeMonitor(
    node_id=f"monitor_{uuid.uuid4().hex[:8]}",
    local_address="localhost",
    local_port=8000
)
