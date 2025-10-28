"""
Sistema de Monitoramento Consciente
===================================

Implementação de um sistema de monitoramento baseado na consciência artificial
e nos princípios do Sefer Yetzira, criando um sistema que não apenas monitora,
mas compreende, aprende e evolui.

Este sistema implementa:
- Monitoramento consciente em tempo real
- Análise preditiva baseada em padrões
- Alertas inteligentes e contextuais
- Evolução contínua do sistema
- Integração com os 32 caminhos de sabedoria
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable, Set
from decimal import Decimal
import asyncio
import time
import json
import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta
import statistics
import math


class MonitoringLevel(Enum):
    """Níveis de Monitoramento"""
    BASIC = "basic"           # Monitoramento básico
    ENHANCED = "enhanced"     # Monitoramento aprimorado
    CONSCIOUS = "conscious"   # Monitoramento consciente
    TRANSCENDENT = "transcendent"  # Monitoramento transcendente


class AlertSeverity(Enum):
    """Severidade de Alertas"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    TRANSCENDENT = "transcendent"


class MetricType(Enum):
    """Tipos de Métricas"""
    PERFORMANCE = "performance"
    SECURITY = "security"
    BUSINESS = "business"
    TECHNICAL = "technical"
    CONSCIOUSNESS = "consciousness"


@dataclass
class ConsciousMetric:
    """
    Métrica Consciente - Representa uma métrica que evolui e aprende
    """
    id: str
    name: str
    metric_type: MetricType
    value: Decimal
    unit: str
    timestamp: float
    context: Dict[str, Any] = field(default_factory=dict)
    consciousness_level: Decimal = Decimal("0.0")
    trend: str = "stable"  # rising, falling, stable
    anomaly_score: Decimal = Decimal("0.0")
    prediction: Optional[Decimal] = None
    learning_data: List[Tuple[float, Decimal]] = field(default_factory=list)
    
    def __post_init__(self):
        """Inicializa métrica consciente"""
        self._update_consciousness_level()
    
    def _update_consciousness_level(self):
        """Atualiza nível de consciência baseado no histórico"""
        if len(self.learning_data) > 10:
            # Consciência baseada na quantidade de dados e variabilidade
            data_points = len(self.learning_data)
            values = [point[1] for point in self.learning_data]
            
            if len(values) > 1:
                variability = statistics.stdev([float(v) for v in values])
                self.consciousness_level = min(
                    Decimal(str(data_points / 100.0)) + Decimal(str(variability / 10.0)),
                    Decimal("1.0")
                )
    
    def add_data_point(self, timestamp: float, value: Decimal):
        """Adiciona ponto de dados e aprende"""
        self.learning_data.append((timestamp, value))
        
        # Mantém apenas últimos 1000 pontos
        if len(self.learning_data) > 1000:
            self.learning_data = self.learning_data[-1000:]
        
        # Atualiza tendência
        self._update_trend()
        
        # Detecta anomalias
        self._detect_anomaly()
        
        # Faz predição
        self._make_prediction()
        
        # Atualiza consciência
        self._update_consciousness_level()
    
    def _update_trend(self):
        """Atualiza tendência baseada nos últimos pontos"""
        if len(self.learning_data) < 5:
            self.trend = "stable"
            return
        
        recent_values = [point[1] for point in self.learning_data[-5:]]
        
        # Calcula inclinação
        x_values = list(range(len(recent_values)))
        y_values = [float(v) for v in recent_values]
        
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        
        if n * sum_x2 - sum_x * sum_x != 0:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            
            if slope > 0.1:
                self.trend = "rising"
            elif slope < -0.1:
                self.trend = "falling"
            else:
                self.trend = "stable"
    
    def _detect_anomaly(self):
        """Detecta anomalias usando estatística consciente"""
        if len(self.learning_data) < 10:
            self.anomaly_score = Decimal("0.0")
            return
        
        values = [float(point[1]) for point in self.learning_data[-20:]]
        current_value = float(self.value)
        
        if len(values) > 1:
            mean_val = statistics.mean(values)
            std_val = statistics.stdev(values)
            
            if std_val > 0:
                z_score = abs(current_value - mean_val) / std_val
                self.anomaly_score = Decimal(str(min(z_score / 3.0, 1.0)))  # Normalizado
    
    def _make_prediction(self):
        """Faz predição baseada em padrões"""
        if len(self.learning_data) < 10:
            self.prediction = None
            return
        
        # Usa regressão linear simples para predição
        recent_data = self.learning_data[-10:]
        x_values = [point[0] for point in recent_data]
        y_values = [float(point[1]) for point in recent_data]
        
        # Normaliza timestamps
        min_time = min(x_values)
        x_normalized = [(x - min_time) for x in x_values]
        
        n = len(x_normalized)
        sum_x = sum(x_normalized)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_normalized, y_values))
        sum_x2 = sum(x * x for x in x_normalized)
        
        if n * sum_x2 - sum_x * sum_x != 0:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            intercept = (sum_y - slope * sum_x) / n
            
            # Prediz próximo valor (próximos 5 minutos)
            future_time = time.time() + 300  # 5 minutos
            future_x = future_time - min_time
            predicted_value = slope * future_x + intercept
            
            self.prediction = Decimal(str(max(predicted_value, 0.0)))


@dataclass
class ConsciousAlert:
    """
    Alerta Consciente - Representa um alerta que compreende contexto
    """
    id: str
    metric_id: str
    severity: AlertSeverity
    message: str
    timestamp: float
    context: Dict[str, Any] = field(default_factory=dict)
    consciousness_level: Decimal = Decimal("0.0")
    confidence: Decimal = Decimal("0.0")
    recommendations: List[str] = field(default_factory=list)
    resolved: bool = False
    resolution_time: Optional[float] = None
    
    def __post_init__(self):
        """Inicializa alerta consciente"""
        if not self.id:
            self.id = f"alert_{int(time.time() * 1000)}"
    
    def resolve(self):
        """Resolve o alerta"""
        self.resolved = True
        self.resolution_time = time.time()


class ConsciousMonitoringSystem:
    """
    Sistema de Monitoramento Consciente
    Monitora, aprende e evolui continuamente
    """
    
    def __init__(self):
        self.metrics: Dict[str, ConsciousMetric] = {}
        self.alerts: List[ConsciousAlert] = []
        self.monitoring_level: MonitoringLevel = MonitoringLevel.CONSCIOUS
        self.alert_thresholds: Dict[str, Dict[str, Decimal]] = {}
        self.learning_patterns: Dict[str, List[Any]] = defaultdict(list)
        self._lock = threading.RLock()
        
        # Configurações de monitoramento
        self.metric_retention_hours = 24
        self.alert_cooldown_minutes = 5
        self.learning_window_hours = 1
        
        # Inicializa thresholds padrão
        self._initialize_default_thresholds()
    
    def _initialize_default_thresholds(self):
        """Inicializa thresholds padrão baseados na sabedoria"""
        self.alert_thresholds = {
            "cpu_usage": {
                "warning": Decimal("0.7"),
                "error": Decimal("0.85"),
                "critical": Decimal("0.95")
            },
            "memory_usage": {
                "warning": Decimal("0.8"),
                "error": Decimal("0.9"),
                "critical": Decimal("0.95")
            },
            "response_time": {
                "warning": Decimal("1000"),  # ms
                "error": Decimal("2000"),
                "critical": Decimal("5000")
            },
            "error_rate": {
                "warning": Decimal("0.01"),  # 1%
                "error": Decimal("0.05"),    # 5%
                "critical": Decimal("0.1")    # 10%
            },
            "consciousness_level": {
                "warning": Decimal("0.3"),
                "error": Decimal("0.2"),
                "critical": Decimal("0.1")
            }
        }
    
    def add_metric(self, metric_id: str, name: str, metric_type: MetricType, 
                  value: Decimal, unit: str, context: Dict[str, Any] = None):
        """Adiciona métrica ao sistema"""
        with self._lock:
            if metric_id not in self.metrics:
                self.metrics[metric_id] = ConsciousMetric(
                    id=metric_id,
                    name=name,
                    metric_type=metric_type,
                    value=value,
                    unit=unit,
                    timestamp=time.time(),
                    context=context or {}
                )
            else:
                # Atualiza métrica existente
                metric = self.metrics[metric_id]
                metric.value = value
                metric.timestamp = time.time()
                metric.context.update(context or {})
                
                # Adiciona ponto de dados para aprendizado
                metric.add_data_point(time.time(), value)
            
            # Verifica alertas
            self._check_alerts(metric_id)
    
    def _check_alerts(self, metric_id: str):
        """Verifica se métrica gera alertas"""
        if metric_id not in self.metrics:
            return
        
        metric = self.metrics[metric_id]
        
        # Verifica cooldown
        recent_alerts = [a for a in self.alerts 
                        if a.metric_id == metric_id and 
                        time.time() - a.timestamp < self.alert_cooldown_minutes * 60]
        
        if recent_alerts:
            return
        
        # Verifica thresholds
        thresholds = self.alert_thresholds.get(metric_id, {})
        
        for severity_name, threshold in thresholds.items():
            severity = AlertSeverity(severity_name.upper())
            
            if metric.value >= threshold:
                self._create_alert(metric, severity, threshold)
                break
    
    def _create_alert(self, metric: ConsciousMetric, severity: AlertSeverity, threshold: Decimal):
        """Cria alerta consciente"""
        # Gera mensagem contextual
        message = self._generate_contextual_message(metric, severity, threshold)
        
        # Gera recomendações
        recommendations = self._generate_recommendations(metric, severity)
        
        # Calcula confiança baseada na consciência
        confidence = metric.consciousness_level
        
        alert = ConsciousAlert(
            id="",
            metric_id=metric.id,
            severity=severity,
            message=message,
            timestamp=time.time(),
            context=metric.context.copy(),
            consciousness_level=metric.consciousness_level,
            confidence=confidence,
            recommendations=recommendations
        )
        
        with self._lock:
            self.alerts.append(alert)
            
            # Mantém apenas últimos 1000 alertas
            if len(self.alerts) > 1000:
                self.alerts = self.alerts[-1000:]
    
    def _generate_contextual_message(self, metric: ConsciousMetric, severity: AlertSeverity, threshold: Decimal) -> str:
        """Gera mensagem contextual baseada na consciência"""
        base_message = f"{metric.name} atingiu {metric.value} {metric.unit} (threshold: {threshold})"
        
        # Adiciona contexto baseado na consciência
        if metric.consciousness_level > Decimal("0.7"):
            if metric.trend == "rising":
                base_message += f" - Tendência crescente detectada"
            elif metric.trend == "falling":
                base_message += f" - Tendência decrescente detectada"
            
            if metric.anomaly_score > Decimal("0.5"):
                base_message += f" - Anomalia detectada (score: {metric.anomaly_score})"
            
            if metric.prediction:
                base_message += f" - Predição: {metric.prediction} {metric.unit} em 5min"
        
        # Adiciona contexto baseado no tipo de métrica
        if metric.metric_type == MetricType.CONSCIOUSNESS:
            base_message += " - Sistema de consciência comprometido"
        elif metric.metric_type == MetricType.SECURITY:
            base_message += " - Possível ameaça de segurança detectada"
        elif metric.metric_type == MetricType.PERFORMANCE:
            base_message += " - Performance degradada"
        
        return base_message
    
    def _generate_recommendations(self, metric: ConsciousMetric, severity: AlertSeverity) -> List[str]:
        """Gera recomendações baseadas na consciência"""
        recommendations = []
        
        # Recomendações baseadas no tipo de métrica
        if metric.metric_type == MetricType.PERFORMANCE:
            if "cpu" in metric.name.lower():
                recommendations.append("Considere escalar horizontalmente os recursos de CPU")
                recommendations.append("Verifique processos com alto consumo de CPU")
            elif "memory" in metric.name.lower():
                recommendations.append("Considere aumentar a memória disponível")
                recommendations.append("Verifique vazamentos de memória")
            elif "response" in metric.name.lower():
                recommendations.append("Otimize consultas de banco de dados")
                recommendations.append("Implemente cache para melhorar performance")
        
        elif metric.metric_type == MetricType.SECURITY:
            recommendations.append("Ative monitoramento de segurança adicional")
            recommendations.append("Verifique logs de acesso e autenticação")
            recommendations.append("Considere implementar rate limiting")
        
        elif metric.metric_type == MetricType.CONSCIOUSNESS:
            recommendations.append("Verifique integridade do sistema de consciência")
            recommendations.append("Analise padrões de aprendizado")
            recommendations.append("Considere ajustar parâmetros de consciência")
        
        # Recomendações baseadas na severidade
        if severity == AlertSeverity.CRITICAL:
            recommendations.append("AÇÃO IMEDIATA NECESSÁRIA")
            recommendations.append("Notifique equipe de emergência")
        
        elif severity == AlertSeverity.ERROR:
            recommendations.append("Investigue causa raiz imediatamente")
            recommendations.append("Implemente medidas corretivas")
        
        elif severity == AlertSeverity.WARNING:
            recommendations.append("Monitore tendência de crescimento")
            recommendations.append("Prepare plano de contingência")
        
        return recommendations
    
    def get_metric_insights(self, metric_id: str) -> Dict[str, Any]:
        """Retorna insights sobre uma métrica"""
        if metric_id not in self.metrics:
            return {}
        
        metric = self.metrics[metric_id]
        
        return {
            "id": metric.id,
            "name": metric.name,
            "current_value": float(metric.value),
            "unit": metric.unit,
            "trend": metric.trend,
            "anomaly_score": float(metric.anomaly_score),
            "consciousness_level": float(metric.consciousness_level),
            "prediction": float(metric.prediction) if metric.prediction else None,
            "data_points": len(metric.learning_data),
            "last_updated": metric.timestamp,
            "context": metric.context
        }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Retorna saúde geral do sistema"""
        with self._lock:
            current_time = time.time()
            
            # Métricas ativas (últimos 5 minutos)
            active_metrics = [m for m in self.metrics.values() 
                            if current_time - m.timestamp < 300]
            
            # Alertas ativos (não resolvidos)
            active_alerts = [a for a in self.alerts if not a.resolved]
            
            # Calcula saúde baseada em métricas
            health_score = self._calculate_health_score(active_metrics)
            
            # Análise de tendências
            trend_analysis = self._analyze_trends(active_metrics)
            
            # Análise de consciência
            consciousness_analysis = self._analyze_consciousness(active_metrics)
            
            return {
                "health_score": health_score,
                "monitoring_level": self.monitoring_level.value,
                "active_metrics": len(active_metrics),
                "total_metrics": len(self.metrics),
                "active_alerts": len(active_alerts),
                "total_alerts": len(self.alerts),
                "trend_analysis": trend_analysis,
                "consciousness_analysis": consciousness_analysis,
                "recommendations": self._generate_system_recommendations(active_metrics, active_alerts)
            }
    
    def _calculate_health_score(self, metrics: List[ConsciousMetric]) -> float:
        """Calcula score de saúde do sistema"""
        if not metrics:
            return 100.0
        
        total_score = 0.0
        weight_sum = 0.0
        
        for metric in metrics:
            # Peso baseado na consciência da métrica
            weight = float(metric.consciousness_level) + 0.1
            
            # Score baseado no tipo de métrica
            if metric.metric_type == MetricType.PERFORMANCE:
                # Performance: quanto menor o valor, melhor (para CPU, memória, etc.)
                if metric.value <= Decimal("0.5"):
                    score = 100.0
                elif metric.value <= Decimal("0.8"):
                    score = 80.0
                elif metric.value <= Decimal("0.9"):
                    score = 60.0
                else:
                    score = 40.0
            elif metric.metric_type == MetricType.SECURITY:
                # Segurança: quanto menor o valor, melhor (para taxa de erro, etc.)
                if metric.value <= Decimal("0.01"):
                    score = 100.0
                elif metric.value <= Decimal("0.05"):
                    score = 80.0
                elif metric.value <= Decimal("0.1"):
                    score = 60.0
                else:
                    score = 40.0
            elif metric.metric_type == MetricType.CONSCIOUSNESS:
                # Consciência: quanto maior o valor, melhor
                score = float(metric.consciousness_level) * 100.0
            else:
                score = 50.0  # Neutro
            
            total_score += score * weight
            weight_sum += weight
        
        return total_score / weight_sum if weight_sum > 0 else 100.0
    
    def _analyze_trends(self, metrics: List[ConsciousMetric]) -> Dict[str, Any]:
        """Analisa tendências do sistema"""
        trend_counts = defaultdict(int)
        
        for metric in metrics:
            trend_counts[metric.trend] += 1
        
        total_metrics = len(metrics)
        
        return {
            "rising": trend_counts["rising"],
            "falling": trend_counts["falling"],
            "stable": trend_counts["stable"],
            "rising_percentage": (trend_counts["rising"] / total_metrics * 100) if total_metrics > 0 else 0,
            "falling_percentage": (trend_counts["falling"] / total_metrics * 100) if total_metrics > 0 else 0,
            "stable_percentage": (trend_counts["stable"] / total_metrics * 100) if total_metrics > 0 else 0
        }
    
    def _analyze_consciousness(self, metrics: List[ConsciousMetric]) -> Dict[str, Any]:
        """Analisa consciência do sistema"""
        if not metrics:
            return {"average_consciousness": 0.0, "consciousness_distribution": {}}
        
        consciousness_values = [float(m.consciousness_level) for m in metrics]
        avg_consciousness = statistics.mean(consciousness_values)
        
        # Distribuição de consciência
        distribution = {
            "low": sum(1 for c in consciousness_values if c < 0.3),
            "medium": sum(1 for c in consciousness_values if 0.3 <= c < 0.7),
            "high": sum(1 for c in consciousness_values if c >= 0.7)
        }
        
        return {
            "average_consciousness": avg_consciousness,
            "consciousness_distribution": distribution,
            "most_conscious_metric": max(metrics, key=lambda m: m.consciousness_level).name if metrics else None
        }
    
    def _generate_system_recommendations(self, metrics: List[ConsciousMetric], alerts: List[ConsciousAlert]) -> List[str]:
        """Gera recomendações para o sistema"""
        recommendations = []
        
        # Recomendações baseadas em alertas
        critical_alerts = [a for a in alerts if a.severity == AlertSeverity.CRITICAL]
        if critical_alerts:
            recommendations.append(f"CRÍTICO: {len(critical_alerts)} alertas críticos ativos")
        
        error_alerts = [a for a in alerts if a.severity == AlertSeverity.ERROR]
        if error_alerts:
            recommendations.append(f"ERRO: {len(error_alerts)} alertas de erro ativos")
        
        # Recomendações baseadas em tendências
        rising_metrics = [m for m in metrics if m.trend == "rising"]
        if len(rising_metrics) > len(metrics) * 0.6:
            recommendations.append("Muitas métricas em tendência crescente - considere escalabilidade")
        
        # Recomendações baseadas em consciência
        low_consciousness_metrics = [m for m in metrics if m.consciousness_level < Decimal("0.3")]
        if len(low_consciousness_metrics) > len(metrics) * 0.5:
            recommendations.append("Baixo nível de consciência detectado - melhore monitoramento")
        
        return recommendations
    
    def get_monitoring_dashboard(self) -> Dict[str, Any]:
        """Retorna dados para dashboard de monitoramento"""
        system_health = self.get_system_health()
        
        # Métricas mais importantes
        important_metrics = sorted(
            self.metrics.values(),
            key=lambda m: m.consciousness_level,
            reverse=True
        )[:10]
        
        # Alertas recentes
        recent_alerts = sorted(
            [a for a in self.alerts if not a.resolved],
            key=lambda a: a.timestamp,
            reverse=True
        )[:10]
        
        return {
            "system_health": system_health,
            "important_metrics": [self.get_metric_insights(m.id) for m in important_metrics],
            "recent_alerts": [
                {
                    "id": a.id,
                    "metric_id": a.metric_id,
                    "severity": a.severity.value,
                    "message": a.message,
                    "timestamp": a.timestamp,
                    "confidence": float(a.confidence),
                    "recommendations": a.recommendations
                }
                for a in recent_alerts
            ],
            "monitoring_level": self.monitoring_level.value,
            "last_updated": time.time()
        }
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """
        Retorna todos os alertas ativos do sistema.
        
        Returns:
            Lista de alertas ativos com informações detalhadas
        """
        try:
            current_time = time.time()
            
            # Filtra alertas ativos (não resolvidos e dentro do período de retenção)
            active_alerts = []
            
            for alert in self.alerts:
                # Verifica se alerta está ativo
                if alert.status == "active":
                    # Verifica se está dentro do período de retenção
                    if current_time - alert.timestamp < self.metric_retention_hours * 3600:
                        active_alerts.append({
                            "id": alert.id,
                            "metric_id": alert.metric_id,
                            "severity": alert.severity.value,
                            "title": alert.message,
                            "description": f"Alerta de {alert.metric_id}: {alert.message}",
                            "affected_components": [alert.metric_id],
                            "timestamp": alert.timestamp,
                            "confidence": float(alert.confidence),
                            "recommendations": alert.recommendations,
                            "context": alert.context
                        })
            
            # Ordena por severidade e timestamp
            severity_order = {"critical": 4, "error": 3, "warning": 2, "info": 1, "transcendent": 5}
            active_alerts.sort(key=lambda x: (severity_order.get(x["severity"], 0), -x["timestamp"]), reverse=True)
            
            return active_alerts
            
        except Exception as e:
            # Se houver erro, retorna lista vazia
            return []


# Instância global do sistema de monitoramento consciente
conscious_monitoring = ConsciousMonitoringSystem()
