"""
Sistema de Monitoramento de Segurança Consciente
===============================================

Implementação de um sistema de monitoramento de segurança que não apenas detecta
ameaças, mas compreende padrões, aprende com ataques e evolui continuamente.

Este sistema implementa:
- Detecção inteligente de ameaças
- Análise comportamental
- Aprendizado adaptativo
- Resposta automática a incidentes
- Integração com consciência artificial
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
from decimal import Decimal
import time
import json
import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta
import hashlib
import ipaddress
import re


class ThreatLevel(Enum):
    """Níveis de Ameaça"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    TRANSCENDENT = "transcendent"


class AttackType(Enum):
    """Tipos de Ataque"""
    BRUTE_FORCE = "brute_force"
    DDoS = "ddos"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    CSRF = "csrf"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    DATA_EXFILTRATION = "data_exfiltration"
    MALWARE = "malware"
    PHISHING = "phishing"
    UNKNOWN = "unknown"


class SecurityEvent(Enum):
    """Eventos de Segurança"""
    LOGIN_FAILURE = "login_failure"
    LOGIN_SUCCESS = "login_success"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SUSPICIOUS_REQUEST = "suspicious_request"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    DATA_ACCESS = "data_access"
    CONFIGURATION_CHANGE = "configuration_change"
    SYSTEM_ERROR = "system_error"


@dataclass
class SecurityIncident:
    """
    Incidente de Segurança - Representa uma ameaça detectada
    """
    id: str
    incident_type: AttackType
    threat_level: ThreatLevel
    source_ip: str
    user_agent: str
    timestamp: float
    description: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    status: str = "active"  # active, investigating, resolved, false_positive
    confidence: Decimal = Decimal("0.0")
    false_positive_probability: Decimal = Decimal("0.0")
    mitigation_applied: List[str] = field(default_factory=list)
    learning_data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Inicializa incidente"""
        if not self.id:
            self.id = f"incident_{int(time.time() * 1000)}"
    
    def calculate_confidence(self, historical_data: Dict[str, Any]) -> Decimal:
        """Calcula confiança baseada em dados históricos"""
        # Fatores que aumentam confiança
        confidence_factors = []
        
        # IP conhecido como malicioso
        if self.source_ip in historical_data.get("malicious_ips", []):
            confidence_factors.append(Decimal("0.3"))
        
        # Padrão de ataque conhecido
        if self.incident_type in historical_data.get("known_patterns", []):
            confidence_factors.append(Decimal("0.2"))
        
        # User agent suspeito
        if self._is_suspicious_user_agent(self.user_agent):
            confidence_factors.append(Decimal("0.1"))
        
        # Múltiplas tentativas
        recent_attempts = historical_data.get("recent_attempts", {}).get(self.source_ip, 0)
        if recent_attempts > 5:
            confidence_factors.append(Decimal("0.2"))
        
        # Calcula confiança total
        total_confidence = sum(confidence_factors)
        self.confidence = min(total_confidence, Decimal("1.0"))
        
        return self.confidence
    
    def _is_suspicious_user_agent(self, user_agent: str) -> bool:
        """Verifica se user agent é suspeito"""
        suspicious_patterns = [
            r"bot", r"crawler", r"spider", r"scraper",
            r"python", r"curl", r"wget", r"postman",
            r"sqlmap", r"nikto", r"nmap"
        ]
        
        user_agent_lower = user_agent.lower()
        return any(re.search(pattern, user_agent_lower) for pattern in suspicious_patterns)
    
    def apply_mitigation(self, mitigation: str):
        """Aplica medida de mitigação"""
        if mitigation not in self.mitigation_applied:
            self.mitigation_applied.append(mitigation)
    
    def resolve(self, resolution: str = "resolved"):
        """Resolve incidente"""
        self.status = resolution


@dataclass
class SecurityPattern:
    """
    Padrão de Segurança - Representa um padrão aprendido
    """
    pattern_id: str
    pattern_type: str
    description: str
    indicators: List[str]
    confidence: Decimal
    false_positive_rate: Decimal
    detection_count: int = 0
    last_seen: float = 0.0
    learning_data: Dict[str, Any] = field(default_factory=dict)
    
    def update_confidence(self, is_true_positive: bool):
        """Atualiza confiança do padrão"""
        self.detection_count += 1
        
        if is_true_positive:
            # Aumenta confiança
            self.confidence = min(self.confidence + Decimal("0.01"), Decimal("1.0"))
        else:
            # Diminui confiança e aumenta taxa de falso positivo
            self.confidence = max(self.confidence - Decimal("0.02"), Decimal("0.0"))
            self.false_positive_rate = min(
                self.false_positive_rate + Decimal("0.01"), 
                Decimal("1.0")
            )


class ConsciousSecurityMonitor:
    """
    Monitor de Segurança Consciente
    Detecta, aprende e evolui continuamente
    """
    
    def __init__(self):
        self.incidents: List[SecurityIncident] = []
        self.patterns: Dict[str, SecurityPattern] = {}
        self.threat_intelligence: Dict[str, Any] = defaultdict(dict)
        self.behavioral_profiles: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self._lock = threading.RLock()
        
        # Configurações
        self.incident_retention_days = 30
        self.pattern_learning_window_hours = 24
        self.behavioral_analysis_window_hours = 168  # 1 semana
        
        # Thresholds de detecção
        self.detection_thresholds = {
            ThreatLevel.LOW: Decimal("0.3"),
            ThreatLevel.MEDIUM: Decimal("0.5"),
            ThreatLevel.HIGH: Decimal("0.7"),
            ThreatLevel.CRITICAL: Decimal("0.9")
        }
        
        # Inicializa padrões conhecidos
        self._initialize_known_patterns()
    
    def _initialize_known_patterns(self):
        """Inicializa padrões de segurança conhecidos"""
        # Padrão de força bruta
        brute_force_pattern = SecurityPattern(
            pattern_id="brute_force_login",
            pattern_type="authentication",
            description="Múltiplas tentativas de login falhadas",
            indicators=[
                "multiple_login_failures",
                "same_ip_multiple_attempts",
                "rapid_successive_attempts"
            ],
            confidence=Decimal("0.8"),
            false_positive_rate=Decimal("0.1")
        )
        self.patterns["brute_force_login"] = brute_force_pattern
        
        # Padrão de DDoS
        ddos_pattern = SecurityPattern(
            pattern_id="ddos_attack",
            pattern_type="availability",
            description="Ataque de negação de serviço",
            indicators=[
                "high_request_rate",
                "multiple_source_ips",
                "unusual_traffic_patterns"
            ],
            confidence=Decimal("0.7"),
            false_positive_rate=Decimal("0.2")
        )
        self.patterns["ddos_attack"] = ddos_pattern
        
        # Padrão de SQL Injection
        sql_injection_pattern = SecurityPattern(
            pattern_id="sql_injection",
            pattern_type="injection",
            description="Tentativa de injeção SQL",
            indicators=[
                "sql_keywords_in_params",
                "union_select_patterns",
                "database_error_responses"
            ],
            confidence=Decimal("0.9"),
            false_positive_rate=Decimal("0.05")
        )
        self.patterns["sql_injection"] = sql_injection_pattern
    
    def log_security_event(self, event_type: SecurityEvent, source_ip: str, 
                          user_agent: str, details: Dict[str, Any] = None):
        """Registra evento de segurança"""
        with self._lock:
            timestamp = time.time()
            details = details or {}
            
            # Atualiza perfil comportamental
            self._update_behavioral_profile(source_ip, event_type, timestamp, details)
            
            # Verifica padrões de ameaça
            threat_patterns = self._detect_threat_patterns(
                event_type, source_ip, user_agent, details, timestamp
            )
            
            # Cria incidentes se necessário
            for pattern in threat_patterns:
                incident = self._create_incident(pattern, source_ip, user_agent, details, timestamp)
                if incident:
                    self.incidents.append(incident)
            
            # Aprende com o evento
            self._learn_from_event(event_type, source_ip, user_agent, details, timestamp)
    
    def log_suspicious_activity(self, activity_type: str, description: str,
                               source_ip: str, severity: str = "MEDIUM") -> None:
        """
        Registra atividade suspeita.
        
        Args:
            activity_type: Tipo da atividade
            description: Descrição da atividade
            source_ip: IP de origem
            severity: Severidade (LOW, MEDIUM, HIGH, CRITICAL)
        """
        try:
            threat_level = ThreatLevel(severity.lower())
        except ValueError:
            threat_level = ThreatLevel.MEDIUM
        
        incident = SecurityIncident(
            id="",
            incident_type=AttackType.UNKNOWN,
            threat_level=threat_level,
            source_ip=source_ip,
            user_agent="",
            timestamp=time.time(),
            description=f"{activity_type}: {description}",
            evidence={"activity_type": activity_type, "description": description}
        )
        
        with self._lock:
            self.incidents.append(incident)
            
            # Manter apenas últimos 500 incidentes
            if len(self.incidents) > 500:
                self.incidents = self.incidents[-500:]
            
            logger.warning(f"Suspicious activity detected: {activity_type} from {source_ip} - {description}")
    
    def log_auth_failure(self, wallet_address: str, source_ip: str, user_agent: str = "") -> None:
        """
        Registra falha de autenticação.
        
        Args:
            wallet_address: Endereço da carteira
            source_ip: IP de origem
            user_agent: User agent
        """
        self.log_security_event(
            SecurityEvent.LOGIN_FAILURE,
            source_ip,
            user_agent,
            {"wallet_address": wallet_address}
        )
    
    def log_rate_limit_exceeded(self, endpoint: str, source_ip: str, user_agent: str = "") -> None:
        """
        Registra excedência de rate limit.
        
        Args:
            endpoint: Endpoint acessado
            source_ip: IP de origem
            user_agent: User agent
        """
        self.log_security_event(
            SecurityEvent.RATE_LIMIT_EXCEEDED,
            source_ip,
            user_agent,
            {"endpoint": endpoint}
        )
    
    def _update_behavioral_profile(self, source_ip: str, event_type: SecurityEvent, 
                                  timestamp: float, details: Dict[str, Any]):
        """Atualiza perfil comportamental de um IP"""
        profile = self.behavioral_profiles[source_ip]
        
        # Atualiza contadores de eventos
        if "event_counts" not in profile:
            profile["event_counts"] = defaultdict(int)
        
        profile["event_counts"][event_type.value] += 1
        
        # Atualiza timestamps
        if "first_seen" not in profile:
            profile["first_seen"] = timestamp
        profile["last_seen"] = timestamp
        
        # Atualiza padrões de atividade
        if "activity_patterns" not in profile:
            profile["activity_patterns"] = []
        
        profile["activity_patterns"].append({
            "timestamp": timestamp,
            "event_type": event_type.value,
            "details": details
        })
        
        # Mantém apenas últimos 1000 eventos
        if len(profile["activity_patterns"]) > 1000:
            profile["activity_patterns"] = profile["activity_patterns"][-1000:]
        
        # Calcula anomalias comportamentais
        profile["anomaly_score"] = self._calculate_behavioral_anomaly(profile)
    
    def _calculate_behavioral_anomaly(self, profile: Dict[str, Any]) -> float:
        """Calcula score de anomalia comportamental"""
        if "activity_patterns" not in profile or len(profile["activity_patterns"]) < 10:
            return 0.0
        
        patterns = profile["activity_patterns"]
        
        # Análise de frequência
        recent_patterns = patterns[-50:] if len(patterns) >= 50 else patterns
        
        # Calcula intervalo médio entre eventos
        intervals = []
        for i in range(1, len(recent_patterns)):
            interval = recent_patterns[i]["timestamp"] - recent_patterns[i-1]["timestamp"]
            intervals.append(interval)
        
        if intervals:
            avg_interval = sum(intervals) / len(intervals)
            current_interval = time.time() - recent_patterns[-1]["timestamp"]
            
            # Anomalia se intervalo atual é muito diferente da média
            if avg_interval > 0:
                interval_anomaly = abs(current_interval - avg_interval) / avg_interval
            else:
                interval_anomaly = 0.0
        else:
            interval_anomaly = 0.0
        
        # Análise de tipos de evento
        event_types = [p["event_type"] for p in recent_patterns]
        event_type_counts = defaultdict(int)
        for event_type in event_types:
            event_type_counts[event_type] += 1
        
        # Anomalia se há muitos eventos de falha
        failure_events = sum(count for event_type, count in event_type_counts.items() 
                           if "failure" in event_type or "error" in event_type)
        failure_anomaly = failure_events / len(recent_patterns) if recent_patterns else 0.0
        
        # Score total de anomalia
        total_anomaly = min(interval_anomaly + failure_anomaly, 1.0)
        
        return total_anomaly
    
    def _detect_threat_patterns(self, event_type: SecurityEvent, source_ip: str,
                               user_agent: str, details: Dict[str, Any], 
                               timestamp: float) -> List[Dict[str, Any]]:
        """Detecta padrões de ameaça"""
        threat_patterns = []
        
        # Verifica padrão de força bruta
        if event_type == SecurityEvent.LOGIN_FAILURE:
            brute_force_pattern = self._check_brute_force_pattern(source_ip, timestamp)
            if brute_force_pattern:
                threat_patterns.append(brute_force_pattern)
        
        # Verifica padrão de DDoS
        if event_type == SecurityEvent.RATE_LIMIT_EXCEEDED:
            ddos_pattern = self._check_ddos_pattern(source_ip, timestamp)
            if ddos_pattern:
                threat_patterns.append(ddos_pattern)
        
        # Verifica padrão de SQL Injection
        if event_type == SecurityEvent.SUSPICIOUS_REQUEST:
            sql_injection_pattern = self._check_sql_injection_pattern(details)
            if sql_injection_pattern:
                threat_patterns.append(sql_injection_pattern)
        
        # Verifica padrões comportamentais
        behavioral_pattern = self._check_behavioral_pattern(source_ip, timestamp)
        if behavioral_pattern:
            threat_patterns.append(behavioral_pattern)
        
        return threat_patterns
    
    def _check_brute_force_pattern(self, source_ip: str, timestamp: float) -> Optional[Dict[str, Any]]:
        """Verifica padrão de força bruta"""
        profile = self.behavioral_profiles.get(source_ip, {})
        event_counts = profile.get("event_counts", {})
        
        # Conta falhas de login nos últimos 10 minutos
        recent_failures = 0
        activity_patterns = profile.get("activity_patterns", [])
        
        for pattern in activity_patterns:
            if (pattern["event_type"] == SecurityEvent.LOGIN_FAILURE.value and
                timestamp - pattern["timestamp"] < 600):  # 10 minutos
                recent_failures += 1
        
        # Detecta força bruta se há muitas falhas
        if recent_failures >= 5:
            return {
                "attack_type": AttackType.BRUTE_FORCE,
                "threat_level": ThreatLevel.HIGH if recent_failures >= 10 else ThreatLevel.MEDIUM,
                "confidence": min(Decimal(str(recent_failures / 20.0)), Decimal("1.0")),
                "evidence": {
                    "recent_failures": recent_failures,
                    "time_window": "10_minutes"
                }
            }
        
        return None
    
    def _check_ddos_pattern(self, source_ip: str, timestamp: float) -> Optional[Dict[str, Any]]:
        """Verifica padrão de DDoS"""
        # Analisa múltiplos IPs com alta frequência
        recent_ips = []
        cutoff_time = timestamp - 300  # 5 minutos
        
        for ip, profile in self.behavioral_profiles.items():
            if profile.get("last_seen", 0) > cutoff_time:
                event_counts = profile.get("event_counts", {})
                rate_limit_exceeded = event_counts.get(SecurityEvent.RATE_LIMIT_EXCEEDED.value, 0)
                
                if rate_limit_exceeded > 3:
                    recent_ips.append(ip)
        
        # Detecta DDoS se há muitos IPs com alta frequência
        if len(recent_ips) >= 10:
            return {
                "attack_type": AttackType.DDoS,
                "threat_level": ThreatLevel.CRITICAL,
                "confidence": Decimal("0.8"),
                "evidence": {
                    "affected_ips": len(recent_ips),
                    "time_window": "5_minutes"
                }
            }
        
        return None
    
    def _check_sql_injection_pattern(self, details: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Verifica padrão de SQL Injection"""
        # Padrões SQL Injection comuns
        sql_patterns = [
            r"union\s+select", r"drop\s+table", r"delete\s+from",
            r"insert\s+into", r"update\s+set", r"exec\s*\(",
            r"script\s*>", r"<script", r"javascript:",
            r"or\s+1\s*=\s*1", r"and\s+1\s*=\s*1"
        ]
        
        # Verifica em parâmetros da requisição
        request_params = details.get("request_params", {})
        for param_name, param_value in request_params.items():
            if isinstance(param_value, str):
                for pattern in sql_patterns:
                    if re.search(pattern, param_value, re.IGNORECASE):
                        return {
                            "attack_type": AttackType.SQL_INJECTION,
                            "threat_level": ThreatLevel.HIGH,
                            "confidence": Decimal("0.9"),
                            "evidence": {
                                "parameter": param_name,
                                "pattern": pattern,
                                "value": param_value[:100]  # Primeiros 100 caracteres
                            }
                        }
        
        return None
    
    def _check_behavioral_pattern(self, source_ip: str, timestamp: float) -> Optional[Dict[str, Any]]:
        """Verifica padrões comportamentais anômalos"""
        profile = self.behavioral_profiles.get(source_ip, {})
        anomaly_score = profile.get("anomaly_score", 0.0)
        
        if anomaly_score > 0.7:
            return {
                "attack_type": AttackType.UNKNOWN,
                "threat_level": ThreatLevel.MEDIUM,
                "confidence": Decimal(str(anomaly_score)),
                "evidence": {
                    "anomaly_score": anomaly_score,
                    "behavioral_analysis": "suspicious_activity_pattern"
                }
            }
        
        return None
    
    def _create_incident(self, pattern: Dict[str, Any], source_ip: str,
                        user_agent: str, details: Dict[str, Any], 
                        timestamp: float) -> Optional[SecurityIncident]:
        """Cria incidente de segurança"""
        # Verifica se já existe incidente similar recente
        recent_incidents = [i for i in self.incidents 
                           if i.source_ip == source_ip and 
                           timestamp - i.timestamp < 3600]  # 1 hora
        
        if recent_incidents:
            # Atualiza incidente existente
            incident = recent_incidents[0]
            incident.evidence.update(pattern.get("evidence", {}))
            incident.confidence = max(incident.confidence, pattern.get("confidence", Decimal("0.0")))
            return None
        
        # Cria novo incidente
        incident = SecurityIncident(
            id="",
            incident_type=pattern["attack_type"],
            threat_level=pattern["threat_level"],
            source_ip=source_ip,
            user_agent=user_agent,
            timestamp=timestamp,
            description=self._generate_incident_description(pattern),
            evidence=pattern.get("evidence", {}),
            confidence=pattern.get("confidence", Decimal("0.0"))
        )
        
        # Calcula confiança baseada em dados históricos
        historical_data = self._get_historical_data(source_ip)
        incident.calculate_confidence(historical_data)
        
        return incident
    
    def _generate_incident_description(self, pattern: Dict[str, Any]) -> str:
        """Gera descrição do incidente"""
        attack_type = pattern["attack_type"]
        threat_level = pattern["threat_level"]
        evidence = pattern.get("evidence", {})
        
        descriptions = {
            AttackType.BRUTE_FORCE: f"Tentativa de força bruta detectada - {evidence.get('recent_failures', 0)} falhas em {evidence.get('time_window', 'unknown')}",
            AttackType.DDoS: f"Ataque DDoS detectado - {evidence.get('affected_ips', 0)} IPs afetados",
            AttackType.SQL_INJECTION: f"Tentativa de SQL Injection detectada no parâmetro '{evidence.get('parameter', 'unknown')}'",
            AttackType.UNKNOWN: f"Atividade suspeita detectada - Score de anomalia: {evidence.get('anomaly_score', 0.0)}"
        }
        
        return descriptions.get(attack_type, "Ameaça de segurança detectada")
    
    def _get_historical_data(self, source_ip: str) -> Dict[str, Any]:
        """Obtém dados históricos para um IP"""
        return {
            "malicious_ips": [ip for ip, profile in self.behavioral_profiles.items() 
                             if profile.get("anomaly_score", 0.0) > 0.8],
            "known_patterns": [pattern.pattern_id for pattern in self.patterns.values()],
            "recent_attempts": {ip: profile.get("event_counts", {}).get(SecurityEvent.LOGIN_FAILURE.value, 0)
                              for ip, profile in self.behavioral_profiles.items()}
        }
    
    def _learn_from_event(self, event_type: SecurityEvent, source_ip: str,
                          user_agent: str, details: Dict[str, Any], timestamp: float):
        """Aprende com evento de segurança"""
        # Atualiza padrões conhecidos
        for pattern in self.patterns.values():
            if self._matches_pattern(pattern, event_type, source_ip, user_agent, details):
                pattern.last_seen = timestamp
                pattern.detection_count += 1
    
    def _matches_pattern(self, pattern: SecurityPattern, event_type: SecurityEvent,
                        source_ip: str, user_agent: str, details: Dict[str, Any]) -> bool:
        """Verifica se evento corresponde a um padrão"""
        # Implementação simplificada - em produção seria mais sofisticada
        if pattern.pattern_id == "brute_force_login" and event_type == SecurityEvent.LOGIN_FAILURE:
            return True
        elif pattern.pattern_id == "ddos_attack" and event_type == SecurityEvent.RATE_LIMIT_EXCEEDED:
            return True
        elif pattern.pattern_id == "sql_injection" and event_type == SecurityEvent.SUSPICIOUS_REQUEST:
            return True
        
        return False
    
    def get_security_dashboard(self) -> Dict[str, Any]:
        """Retorna dados para dashboard de segurança"""
        with self._lock:
            current_time = time.time()
            
            # Incidentes ativos
            active_incidents = [i for i in self.incidents if i.status == "active"]
            
            # Incidentes por nível de ameaça
            threat_level_counts = defaultdict(int)
            for incident in active_incidents:
                threat_level_counts[incident.threat_level.value] += 1
            
            # Top IPs suspeitos
            suspicious_ips = sorted(
                self.behavioral_profiles.items(),
                key=lambda x: x[1].get("anomaly_score", 0.0),
                reverse=True
            )[:10]
            
            # Padrões mais detectados
            top_patterns = sorted(
                self.patterns.values(),
                key=lambda p: p.detection_count,
                reverse=True
            )[:5]
            
            return {
                "active_incidents": len(active_incidents),
                "total_incidents": len(self.incidents),
                "threat_level_distribution": dict(threat_level_counts),
                "suspicious_ips": [
                    {
                        "ip": ip,
                        "anomaly_score": profile.get("anomaly_score", 0.0),
                        "last_seen": profile.get("last_seen", 0),
                        "event_counts": dict(profile.get("event_counts", {}))
                    }
                    for ip, profile in suspicious_ips
                ],
                "top_patterns": [
                    {
                        "pattern_id": pattern.pattern_id,
                        "description": pattern.description,
                        "detection_count": pattern.detection_count,
                        "confidence": float(pattern.confidence),
                        "false_positive_rate": float(pattern.false_positive_rate)
                    }
                    for pattern in top_patterns
                ],
                "security_score": self._calculate_security_score(),
                "last_updated": current_time
            }
    
    def _calculate_security_score(self) -> float:
        """Calcula score de segurança geral"""
        if not self.incidents:
            return 100.0
        
        # Penaliza por incidentes ativos
        active_incidents = [i for i in self.incidents if i.status == "active"]
        
        penalty = 0.0
        for incident in active_incidents:
            if incident.threat_level == ThreatLevel.CRITICAL:
                penalty += 20.0
            elif incident.threat_level == ThreatLevel.HIGH:
                penalty += 10.0
            elif incident.threat_level == ThreatLevel.MEDIUM:
                penalty += 5.0
            else:
                penalty += 2.0
        
        # Penaliza por IPs suspeitos
        high_anomaly_ips = sum(1 for profile in self.behavioral_profiles.values() 
                              if profile.get("anomaly_score", 0.0) > 0.8)
        penalty += high_anomaly_ips * 2.0
        
        return max(100.0 - penalty, 0.0)
    
    def apply_automatic_mitigation(self, incident: SecurityIncident) -> List[str]:
        """Aplica mitigação automática"""
        mitigations = []
        
        if incident.incident_type == AttackType.BRUTE_FORCE:
            mitigations.append("block_ip_temporarily")
            mitigations.append("increase_login_delay")
        
        elif incident.incident_type == AttackType.DDoS:
            mitigations.append("enable_ddos_protection")
            mitigations.append("rate_limit_aggressive")
        
        elif incident.incident_type == AttackType.SQL_INJECTION:
            mitigations.append("block_sql_patterns")
            mitigations.append("enable_waf")
        
        # Aplica mitigações
        for mitigation in mitigations:
            incident.apply_mitigation(mitigation)
        
        return mitigations


# Instância global do monitor de segurança consciente
security_monitor = ConsciousSecurityMonitor()