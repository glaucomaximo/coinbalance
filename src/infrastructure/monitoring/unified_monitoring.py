"""
Sistema de Monitoramento Unificado Consciente
=============================================

Sistema que integra todos os tipos de monitoramento (consciente, segurança, performance)
em uma única interface unificada, criando uma visão holística do sistema.

Este sistema implementa:
- Integração de todos os monitores
- Dashboard unificado
- Análise cruzada de métricas
- Alertas inteligentes
- Tomada de decisão consciente
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from decimal import Decimal
import time
import json
import threading
from collections import defaultdict
import asyncio

from .conscious_monitoring import (
    ConsciousMonitoringSystem, 
    MonitoringLevel, 
    AlertSeverity, 
    MetricType,
    conscious_monitoring
)
from .security_monitor import (
    ConsciousSecurityMonitor,
    ThreatLevel,
    AttackType,
    SecurityEvent,
    security_monitor
)
from .performance_monitor import (
    ConsciousPerformanceMonitor,
    PerformanceMetric,
    OptimizationAction,
    performance_monitor
)


class SystemHealthStatus(Enum):
    """Status de Saúde do Sistema"""
    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class UnifiedAlertPriority(Enum):
    """Prioridade Unificada de Alertas"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class UnifiedAlert:
    """
    Alerta Unificado - Combina alertas de todos os sistemas
    """
    id: str
    alert_type: str  # conscious, security, performance
    priority: UnifiedAlertPriority
    title: str
    description: str
    timestamp: float
    source_system: str
    original_alert_id: str
    affected_components: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    correlation_data: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False
    resolution_time: Optional[float] = None


@dataclass
class SystemInsight:
    """
    Insight do Sistema - Análise inteligente baseada em múltiplas métricas
    """
    id: str
    insight_type: str
    title: str
    description: str
    confidence: Decimal
    impact_level: str  # low, medium, high, critical
    affected_systems: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class UnifiedConsciousMonitoringSystem:
    """
    Sistema de Monitoramento Unificado Consciente
    Integra todos os sistemas de monitoramento
    """
    
    def __init__(self):
        self.conscious_monitor = conscious_monitoring
        self.security_monitor = security_monitor
        self.performance_monitor = performance_monitor
        
        self.unified_alerts: List[UnifiedAlert] = []
        self.system_insights: List[SystemInsight] = []
        self.correlation_rules: List[Dict[str, Any]] = []
        self._lock = threading.RLock()
        
        # Configurações
        self.alert_correlation_window = 300  # 5 minutos
        self.insight_generation_interval = 60  # 1 minuto
        
        # Inicializa regras de correlação
        self._initialize_correlation_rules()
        
        # Inicia análise contínua
        self._start_continuous_analysis()
    
    def _initialize_correlation_rules(self):
        """Inicializa regras de correlação entre sistemas"""
        # Regra: CPU alto + múltiplas falhas de login = possível ataque
        self.correlation_rules.append({
            "id": "cpu_high_login_failures",
            "name": "High CPU with Login Failures",
            "conditions": [
                {"system": "performance", "metric": "cpu_usage", "operator": ">", "value": 0.8},
                {"system": "security", "event": "login_failure", "count": ">", "value": 5}
            ],
            "correlation": "possible_attack",
            "priority": UnifiedAlertPriority.HIGH,
            "description": "Alto uso de CPU combinado com múltiplas falhas de login pode indicar ataque de força bruta"
        })
        
        # Regra: Tempo de resposta alto + taxa de erro alta = possível DDoS
        self.correlation_rules.append({
            "id": "response_time_error_rate",
            "name": "High Response Time with Error Rate",
            "conditions": [
                {"system": "performance", "metric": "response_time", "operator": ">", "value": 2000},
                {"system": "performance", "metric": "error_rate", "operator": ">", "value": 0.05}
            ],
            "correlation": "possible_ddos",
            "priority": UnifiedAlertPriority.CRITICAL,
            "description": "Alto tempo de resposta com alta taxa de erro pode indicar ataque DDoS"
        })
        
        # Regra: Baixa consciência + problemas de segurança = sistema comprometido
        self.correlation_rules.append({
            "id": "low_consciousness_security",
            "name": "Low Consciousness with Security Issues",
            "conditions": [
                {"system": "conscious", "metric": "consciousness_level", "operator": "<", "value": 0.3},
                {"system": "security", "incidents": "active", "count": ">", "value": 3}
            ],
            "correlation": "system_compromised",
            "priority": UnifiedAlertPriority.EMERGENCY,
            "description": "Baixo nível de consciência combinado com incidentes de segurança pode indicar sistema comprometido"
        })
    
    def _start_continuous_analysis(self):
        """Inicia análise contínua do sistema"""
        def analyze_system():
            while True:
                try:
                    self._correlate_alerts()
                    self._generate_insights()
                    self._update_system_health()
                    time.sleep(self.insight_generation_interval)
                except Exception as e:
                    print(f"Erro na análise contínua: {e}")
                    time.sleep(self.insight_generation_interval)
        
        analysis_thread = threading.Thread(target=analyze_system, daemon=True)
        analysis_thread.start()
    
    def _correlate_alerts(self):
        """Correlaciona alertas de diferentes sistemas"""
        with self._lock:
            current_time = time.time()
            
            # Obtém alertas recentes de todos os sistemas
            recent_conscious_alerts = self._get_recent_conscious_alerts()
            recent_security_alerts = self._get_recent_security_alerts()
            recent_performance_alerts = self._get_recent_performance_alerts()
            
            # Aplica regras de correlação
            for rule in self.correlation_rules:
                if self._check_correlation_rule(rule, recent_conscious_alerts, 
                                               recent_security_alerts, recent_performance_alerts):
                    self._create_correlated_alert(rule, current_time)
    
    def _get_recent_conscious_alerts(self) -> List[Dict[str, Any]]:
        """Obtém alertas recentes do sistema consciente"""
        current_time = time.time()
        recent_alerts = []
        
        for alert in self.conscious_monitor.alerts:
            if current_time - alert.timestamp < self.alert_correlation_window:
                recent_alerts.append({
                    "id": alert.id,
                    "metric_id": alert.metric_id,
                    "severity": alert.severity.value,
                    "timestamp": alert.timestamp,
                    "message": alert.message
                })
        
        return recent_alerts
    
    def _get_recent_security_alerts(self) -> List[Dict[str, Any]]:
        """Obtém alertas recentes do sistema de segurança"""
        current_time = time.time()
        recent_alerts = []
        
        for incident in self.security_monitor.incidents:
            if current_time - incident.timestamp < self.alert_correlation_window:
                recent_alerts.append({
                    "id": incident.id,
                    "incident_type": incident.incident_type.value,
                    "threat_level": incident.threat_level.value,
                    "timestamp": incident.timestamp,
                    "description": incident.description
                })
        
        return recent_alerts
    
    def _get_recent_performance_alerts(self) -> List[Dict[str, Any]]:
        """Obtém alertas recentes do sistema de performance"""
        current_time = time.time()
        recent_alerts = []
        
        for alert in self.performance_monitor.alerts:
            if current_time - alert.timestamp < self.alert_correlation_window:
                recent_alerts.append({
                    "id": alert.id,
                    "metric": alert.metric.value,
                    "severity": alert.severity,
                    "timestamp": alert.timestamp,
                    "message": alert.message
                })
        
        return recent_alerts
    
    def _check_correlation_rule(self, rule: Dict[str, Any], 
                               conscious_alerts: List[Dict[str, Any]],
                               security_alerts: List[Dict[str, Any]],
                               performance_alerts: List[Dict[str, Any]]) -> bool:
        """Verifica se regra de correlação é satisfeita"""
        conditions = rule.get("conditions", [])
        
        for condition in conditions:
            system = condition.get("system")
            
            if system == "conscious":
                if not self._check_conscious_condition(condition, conscious_alerts):
                    return False
            elif system == "security":
                if not self._check_security_condition(condition, security_alerts):
                    return False
            elif system == "performance":
                if not self._check_performance_condition(condition, performance_alerts):
                    return False
        
        return True
    
    def _check_conscious_condition(self, condition: Dict[str, Any], alerts: List[Dict[str, Any]]) -> bool:
        """Verifica condição do sistema consciente"""
        metric = condition.get("metric")
        operator = condition.get("operator")
        value = condition.get("value")
        
        # Obtém valor atual da métrica
        if metric == "consciousness_level":
            system_health = self.conscious_monitor.get_system_health()
            consciousness_analysis = system_health.get("consciousness_analysis", {})
            current_value = consciousness_analysis.get("average_consciousness", 0.0)
        else:
            return False
        
        # Aplica operador
        if operator == ">":
            return current_value > value
        elif operator == "<":
            return current_value < value
        elif operator == ">=":
            return current_value >= value
        elif operator == "<=":
            return current_value <= value
        elif operator == "==":
            return current_value == value
        
        return False
    
    def _check_security_condition(self, condition: Dict[str, Any], alerts: List[Dict[str, Any]]) -> bool:
        """Verifica condição do sistema de segurança"""
        event = condition.get("event")
        count_operator = condition.get("count")
        value = condition.get("value")
        
        if event == "login_failure":
            # Conta falhas de login recentes
            login_failures = sum(1 for alert in alerts 
                               if "login" in alert.get("description", "").lower())
            current_count = login_failures
        elif event == "incidents":
            # Conta incidentes ativos
            active_incidents = len([i for i in self.security_monitor.incidents 
                                  if i.status == "active"])
            current_count = active_incidents
        else:
            return False
        
        # Aplica operador de contagem
        if count_operator == ">":
            return current_count > value
        elif count_operator == "<":
            return current_count < value
        elif count_operator == ">=":
            return current_count >= value
        elif count_operator == "<=":
            return current_count <= value
        elif count_operator == "==":
            return current_count == value
        
        return False
    
    def _check_performance_condition(self, condition: Dict[str, Any], alerts: List[Dict[str, Any]]) -> bool:
        """Verifica condição do sistema de performance"""
        metric = condition.get("metric")
        operator = condition.get("operator")
        value = condition.get("value")
        
        # Obtém valor atual da métrica
        dashboard_data = self.performance_monitor.get_performance_dashboard()
        current_metrics = dashboard_data.get("current_metrics", {})
        
        if metric == "cpu_usage":
            current_value = current_metrics.get("cpu_usage", 0.0)
        elif metric == "memory_usage":
            current_value = current_metrics.get("memory_usage", 0.0)
        elif metric == "response_time":
            current_value = current_metrics.get("response_time", 0.0)
        elif metric == "error_rate":
            current_value = current_metrics.get("error_rate", 0.0)
        else:
            return False
        
        # Aplica operador
        if operator == ">":
            return current_value > value
        elif operator == "<":
            return current_value < value
        elif operator == ">=":
            return current_value >= value
        elif operator == "<=":
            return current_value <= value
        elif operator == "==":
            return current_value == value
        
        return False
    
    def _create_correlated_alert(self, rule: Dict[str, Any], timestamp: float):
        """Cria alerta correlacionado"""
        # Verifica se já existe alerta similar recente
        recent_correlated = []
        for a in self.unified_alerts:
            if a.correlation_data.get("rule_id") == rule["id"]:
                # Garantir que timestamp é float
                alert_timestamp = a.timestamp
                if isinstance(alert_timestamp, str):
                    alert_timestamp = float(alert_timestamp)
                if timestamp - alert_timestamp < self.alert_correlation_window:
                    recent_correlated.append(a)
        
        if recent_correlated:
            return  # Já existe alerta similar
        
        alert = UnifiedAlert(
            id=f"unified_{rule['id']}_{int(timestamp * 1000)}",
            alert_type="correlated",
            priority=rule["priority"],
            title=f"Alerta Correlacionado: {rule['name']}",
            description=rule["description"],
            timestamp=timestamp,
            source_system="unified",
            original_alert_id="",
            correlation_data={
                "rule_id": rule["id"],
                "rule_name": rule["name"],
                "correlation_type": rule["correlation"]
            }
        )
        
        self.unified_alerts.append(alert)
        
        # Mantém apenas últimos 1000 alertas
        if len(self.unified_alerts) > 1000:
            self.unified_alerts = self.unified_alerts[-1000:]
    
    def _generate_insights(self):
        """Gera insights inteligentes do sistema"""
        with self._lock:
            current_time = time.time()
            
            # Insight: Análise de saúde geral
            health_insight = self._analyze_system_health()
            if health_insight:
                self.system_insights.append(health_insight)
            
            # Insight: Análise de tendências
            trend_insight = self._analyze_system_trends()
            if trend_insight:
                self.system_insights.append(trend_insight)
            
            # Insight: Análise de segurança
            security_insight = self._analyze_security_posture()
            if security_insight:
                self.system_insights.append(security_insight)
            
            # Mantém apenas últimos 100 insights
            if len(self.system_insights) > 100:
                self.system_insights = self.system_insights[-100:]
    
    def _analyze_system_health(self) -> Optional[SystemInsight]:
        """Analisa saúde geral do sistema"""
        conscious_health = self.conscious_monitor.get_system_health()
        security_dashboard = self.security_monitor.get_security_dashboard()
        performance_dashboard = self.performance_monitor.get_performance_dashboard()
        
        # Calcula score geral de saúde
        conscious_score = conscious_health.get("health_score", 100.0)
        security_score = security_dashboard.get("security_score", 100.0)
        performance_score = performance_dashboard.get("performance_score", 100.0)
        
        overall_score = (conscious_score + security_score + performance_score) / 3
        
        # Determina nível de impacto
        if overall_score >= 90:
            impact_level = "low"
            title = "Sistema Operando Excelentemente"
            description = f"Sistema funcionando com score de saúde de {overall_score:.1f}%"
        elif overall_score >= 75:
            impact_level = "medium"
            title = "Sistema Operando Bem"
            description = f"Sistema funcionando adequadamente com score de {overall_score:.1f}%"
        elif overall_score >= 50:
            impact_level = "high"
            title = "Sistema com Problemas Moderados"
            description = f"Sistema apresentando problemas com score de {overall_score:.1f}%"
        else:
            impact_level = "critical"
            title = "Sistema com Problemas Críticos"
            description = f"Sistema com problemas críticos - score de {overall_score:.1f}%"
        
        # Gera recomendações
        recommendations = []
        if conscious_score < 80:
            recommendations.append("Melhore monitoramento consciente do sistema")
        if security_score < 80:
            recommendations.append("Implemente medidas de segurança adicionais")
        if performance_score < 80:
            recommendations.append("Otimize performance do sistema")
        
        return SystemInsight(
            id=f"health_analysis_{int(time.time())}",
            insight_type="system_health",
            title=title,
            description=description,
            confidence=Decimal("0.9"),
            impact_level=impact_level,
            affected_systems=["conscious", "security", "performance"],
            recommendations=recommendations,
            evidence={
                "conscious_score": conscious_score,
                "security_score": security_score,
                "performance_score": performance_score,
                "overall_score": overall_score
            }
        )
    
    def _analyze_system_trends(self) -> Optional[SystemInsight]:
        """Analisa tendências do sistema"""
        # Analisa tendências de performance
        cpu_trend = self.performance_monitor.get_metric_trends(PerformanceMetric.CPU_USAGE, 1)
        memory_trend = self.performance_monitor.get_metric_trends(PerformanceMetric.MEMORY_USAGE, 1)
        
        # Identifica tendências preocupantes
        concerning_trends = []
        recommendations = []
        
        if cpu_trend["trend"] == "rising" and cpu_trend["current_value"] > 0.7:
            concerning_trends.append("CPU em tendência crescente")
            recommendations.append("Considere escalar recursos de CPU")
        
        if memory_trend["trend"] == "rising" and memory_trend["current_value"] > 0.8:
            concerning_trends.append("Memória em tendência crescente")
            recommendations.append("Considere aumentar memória ou otimizar uso")
        
        if concerning_trends:
            return SystemInsight(
                id=f"trend_analysis_{int(time.time())}",
                insight_type="trend_analysis",
                title="Tendências Preocupantes Detectadas",
                description=f"Sistema apresentando: {', '.join(concerning_trends)}",
                confidence=Decimal("0.8"),
                impact_level="medium",
                affected_systems=["performance"],
                recommendations=recommendations,
                evidence={
                    "cpu_trend": cpu_trend,
                    "memory_trend": memory_trend,
                    "concerning_trends": concerning_trends
                }
            )
        
        return None
    
    def _analyze_security_posture(self) -> Optional[SystemInsight]:
        """Analisa postura de segurança"""
        security_dashboard = self.security_monitor.get_security_dashboard()
        
        active_incidents = security_dashboard.get("active_incidents", 0)
        suspicious_ips = len(security_dashboard.get("suspicious_ips", []))
        
        if active_incidents > 5 or suspicious_ips > 10:
            return SystemInsight(
                id=f"security_analysis_{int(time.time())}",
                insight_type="security_posture",
                title="Postura de Segurança Comprometida",
                description=f"Sistema com {active_incidents} incidentes ativos e {suspicious_ips} IPs suspeitos",
                confidence=Decimal("0.9"),
                impact_level="critical",
                affected_systems=["security"],
                recommendations=[
                    "Investigue incidentes de segurança ativos",
                    "Bloqueie IPs suspeitos",
                    "Implemente medidas de segurança adicionais"
                ],
                evidence={
                    "active_incidents": active_incidents,
                    "suspicious_ips": suspicious_ips
                }
            )
        
        return None
    
    def _update_system_health(self):
        """Atualiza saúde geral do sistema"""
        try:
            # Calcular métricas globais
            total_alerts = len(self.active_alerts)
            critical_alerts = len([a for a in self.active_alerts if a.get('severity') == 'critical'])
            
            # Calcular score de saúde (0-100)
            health_score = 100
            if critical_alerts > 0:
                health_score -= (critical_alerts * 20)  # -20 por alerta crítico
            if total_alerts > 5:
                health_score -= ((total_alerts - 5) * 5)  # -5 por alerta adicional
            
            health_score = max(0, health_score)
            
            # Atualizar métricas globais
            self.global_metrics.update({
                "health_score": health_score,
                "total_alerts": total_alerts,
                "critical_alerts": critical_alerts,
                "last_health_update": time.time()
            })
            
            # Log se saúde baixa
            if health_score < 70:
                logger.warning(f"⚠️ Saúde do sistema baixa: {health_score}%")
                
        except Exception as e:
            logger.error(f"Erro ao atualizar saúde do sistema: {e}")
    
    def get_unified_dashboard(self) -> Dict[str, Any]:
        """Retorna dashboard unificado com todos os dados"""
        with self._lock:
            # Obtém dados de todos os sistemas
            conscious_data = self.conscious_monitor.get_monitoring_dashboard()
            security_data = self.security_monitor.get_security_dashboard()
            performance_data = self.performance_monitor.get_performance_dashboard()
            
            # Alertas unificados ativos
            active_unified_alerts = [a for a in self.unified_alerts if not a.resolved]
            
            # Insights recentes
            recent_insights = sorted(
                self.system_insights,
                key=lambda x: x.timestamp,
                reverse=True
            )[:10]
            
            # Calcula saúde geral
            overall_health = self._calculate_overall_health(
                conscious_data, security_data, performance_data
            )
            
            return {
                "overall_health": overall_health,
                "conscious_monitoring": conscious_data,
                "security_monitoring": security_data,
                "performance_monitoring": performance_data,
                "unified_alerts": [
                    {
                        "id": alert.id,
                        "type": alert.alert_type,
                        "priority": alert.priority.value,
                        "title": alert.title,
                        "description": alert.description,
                        "timestamp": alert.timestamp,
                        "source_system": alert.source_system,
                        "recommendations": alert.recommendations
                    }
                    for alert in active_unified_alerts
                ],
                "system_insights": [
                    {
                        "id": insight.id,
                        "type": insight.insight_type,
                        "title": insight.title,
                        "description": insight.description,
                        "confidence": float(insight.confidence),
                        "impact_level": insight.impact_level,
                        "affected_systems": insight.affected_systems,
                        "recommendations": insight.recommendations,
                        "timestamp": insight.timestamp
                    }
                    for insight in recent_insights
                ],
                "correlation_rules": len(self.correlation_rules),
                "last_updated": time.time()
            }
    
    def _calculate_overall_health(self, conscious_data: Dict[str, Any], 
                                 security_data: Dict[str, Any], 
                                 performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula saúde geral do sistema"""
        conscious_score = conscious_data.get("system_health", {}).get("health_score", 100.0)
        security_score = security_data.get("security_score", 100.0)
        performance_score = performance_data.get("performance_score", 100.0)
        
        overall_score = (conscious_score + security_score + performance_score) / 3
        
        # Determina status geral
        if overall_score >= 90:
            status = SystemHealthStatus.EXCELLENT
        elif overall_score >= 75:
            status = SystemHealthStatus.GOOD
        elif overall_score >= 50:
            status = SystemHealthStatus.WARNING
        elif overall_score >= 25:
            status = SystemHealthStatus.CRITICAL
        else:
            status = SystemHealthStatus.EMERGENCY
        
        return {
            "overall_score": overall_score,
            "status": status.value,
            "conscious_score": conscious_score,
            "security_score": security_score,
            "performance_score": performance_score,
            "timestamp": time.time()
        }
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """
        Retorna todos os alertas ativos do sistema unificado.
        
        Returns:
            Lista de alertas ativos com informações detalhadas
        """
        try:
            active_alerts = []
            
            # Obter alertas do monitor consciente
            conscious_alerts = self.conscious_monitor.get_active_alerts()
            for alert in conscious_alerts:
                active_alerts.append({
                    "id": alert.get("id", f"conscious_{int(time.time())}"),
                    "type": "conscious",
                    "severity": alert.get("severity", "info"),
                    "title": alert.get("title", "Conscious Alert"),
                    "description": alert.get("description", ""),
                    "affected_components": alert.get("affected_components", []),
                    "timestamp": alert.get("timestamp", time.time()),
                    "source": "conscious_monitor"
                })
            
            # Obter alertas do monitor de segurança
            security_alerts = self.security_monitor.get_active_alerts()
            for alert in security_alerts:
                active_alerts.append({
                    "id": alert.get("id", f"security_{int(time.time())}"),
                    "type": "security",
                    "severity": alert.get("severity", "warning"),
                    "title": alert.get("title", "Security Alert"),
                    "description": alert.get("description", ""),
                    "affected_components": alert.get("affected_components", []),
                    "timestamp": alert.get("timestamp", time.time()),
                    "source": "security_monitor"
                })
            
            # Obter alertas do monitor de performance
            performance_alerts = self.performance_monitor.get_active_alerts()
            for alert in performance_alerts:
                active_alerts.append({
                    "id": alert.get("id", f"performance_{int(time.time())}"),
                    "type": "performance",
                    "severity": alert.get("severity", "info"),
                    "title": alert.get("title", "Performance Alert"),
                    "description": alert.get("description", ""),
                    "affected_components": alert.get("affected_components", []),
                    "timestamp": alert.get("timestamp", time.time()),
                    "source": "performance_monitor"
                })
            
            # Adicionar alertas unificados
            for alert in self.unified_alerts:
                active_alerts.append({
                    "id": alert.alert_id,
                    "type": "unified",
                    "severity": alert.severity.value,
                    "title": alert.title,
                    "description": alert.description,
                    "affected_components": alert.affected_components,
                    "timestamp": alert.timestamp,
                    "source": "unified_monitor",
                    "correlation_data": alert.correlation_data
                })
            
            # Ordenar por severidade e timestamp
            severity_order = {"critical": 4, "error": 3, "warning": 2, "info": 1}
            active_alerts.sort(key=lambda x: (severity_order.get(x["severity"], 0), -x["timestamp"]), reverse=True)
            
            return active_alerts
            
        except Exception as e:
            logger.error(f"Erro ao obter alertas ativos: {e}")
            return []
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve um alerta unificado"""
        with self._lock:
            for alert in self.unified_alerts:
                if alert.id == alert_id:
                    alert.resolved = True
                    alert.resolution_time = time.time()
                    return True
        return False
    
    def get_system_recommendations(self) -> List[str]:
        """Retorna recomendações gerais do sistema"""
        recommendations = []
        
        # Obtém dados atuais
        dashboard = self.get_unified_dashboard()
        overall_health = dashboard.get("overall_health", {})
        
        overall_score = overall_health.get("overall_score", 100.0)
        
        if overall_score < 80:
            recommendations.append("Sistema apresentando problemas - investigue métricas detalhadas")
        
        if overall_score < 60:
            recommendations.append("CRÍTICO: Sistema com problemas sérios - ação imediata necessária")
        
        # Recomendações baseadas em insights
        recent_insights = dashboard.get("system_insights", [])
        for insight in recent_insights[:3]:  # Top 3 insights
            recommendations.extend(insight.get("recommendations", []))
        
        return list(set(recommendations))  # Remove duplicatas


# Instância global do sistema de monitoramento unificado
unified_monitoring = UnifiedConsciousMonitoringSystem()
