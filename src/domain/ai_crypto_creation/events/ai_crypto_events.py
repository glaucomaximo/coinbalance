"""
Eventos de Domínio para AI Crypto Creation
==========================================

Eventos padronizados para o módulo de criação de criptomoedas com IA,
seguindo os padrões DDD estabelecidos no projeto.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from decimal import Decimal
from enum import Enum

from src.domain.shared.domain_events.base import DomainEvent

class CryptoCreationStatus(Enum):
    """Status da criação de criptomoeda"""
    INITIATED = "initiated"
    ANALYZING = "analyzing"
    DESIGNING = "designing"
    CREATED = "created"
    FAILED = "failed"
    EVOLVING = "evolving"

class TokenGenerationStatus(Enum):
    """Status da geração de token"""
    REQUESTED = "requested"
    GENERATING = "generating"
    GENERATED = "generated"
    DEPLOYED = "deployed"
    FAILED = "failed"

@dataclass
class AICryptoCreationInitiated(DomainEvent):
    """Evento disparado quando IA inicia criação de criptomoeda"""
    crypto_id: str
    purpose: str
    target_market: str
    ai_reasoning: str
    confidence_level: float
    fractal_context: Dict[str, Any]
    custom_requirements: Optional[Dict[str, Any]] = None
    timestamp: float = field(default_factory=time.time)

@dataclass
class AICryptoCreationCompleted(DomainEvent):
    """Evento disparado quando IA completa criação de criptomoeda"""
    crypto_id: str
    crypto_name: str
    crypto_symbol: str
    specification: Dict[str, Any]
    ai_reasoning: str
    confidence_score: float
    fractal_scaling: Decimal
    evolution_potential: bool
    timestamp: float = field(default_factory=time.time)

@dataclass
class AICryptoCreationFailed(DomainEvent):
    """Evento disparado quando criação de criptomoeda falha"""
    crypto_id: str
    error_message: str
    failure_reason: str
    ai_learning: Dict[str, Any]
    retry_possible: bool
    timestamp: float = field(default_factory=time.time)

@dataclass
class TokenGenerationRequested(DomainEvent):
    """Evento disparado quando geração de token é solicitada"""
    request_id: str
    purpose: str
    target_audience: str
    requirements: Dict[str, Any]
    constraints: Dict[str, Any]
    preferences: Dict[str, Any]
    fractal_context: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

@dataclass
class TokenGenerationCompleted(DomainEvent):
    """Evento disparado quando geração de token é completada"""
    request_id: str
    template_id: str
    token_name: str
    token_symbol: str
    token_category: str
    token_standard: str
    smart_contract_code: str
    confidence_score: float
    fractal_optimization: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

@dataclass
class TokenGenerationFailed(DomainEvent):
    """Evento disparado quando geração de token falha"""
    request_id: str
    error_message: str
    failure_reason: str
    ai_learning: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

@dataclass
class AutonomousDecisionMade(DomainEvent):
    """Evento disparado quando IA toma decisão autônoma"""
    decision_id: str
    decision_type: str
    reasoning: str
    expected_outcome: str
    confidence: float
    impact_assessment: Dict[str, Any]
    execution_plan: List[str]
    fractal_context: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

@dataclass
class AutonomousDecisionExecuted(DomainEvent):
    """Evento disparado quando decisão autônoma é executada"""
    decision_id: str
    execution_result: Dict[str, Any]
    success: bool
    performance_metrics: Dict[str, Any]
    learning_outcomes: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

@dataclass
class EcosystemHealthUpdated(DomainEvent):
    """Evento disparado quando saúde do ecossistema é atualizada"""
    health_score: float
    risk_level: str
    liquidity_score: float
    adoption_score: float
    innovation_score: float
    stability_score: float
    growth_potential: float
    recommendations: List[str]
    fractal_impact: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

@dataclass
class CryptoEvolutionTriggered(DomainEvent):
    """Evento disparado quando evolução de criptomoeda é acionada"""
    crypto_id: str
    evolution_type: str
    evolution_reason: str
    current_performance: Dict[str, Any]
    expected_improvements: Dict[str, Any]
    evolution_plan: List[str]
    fractal_scaling: Decimal
    consciousness_level: float
    timestamp: float = field(default_factory=time.time)

@dataclass
class CryptoEvolutionCompleted(DomainEvent):
    """Evento disparado quando evolução de criptomoeda é completada"""
    crypto_id: str
    evolution_type: str
    evolution_result: Dict[str, Any]
    performance_improvements: Dict[str, Any]
    new_capabilities: List[str]
    fractal_enhancements: Dict[str, Any]
    consciousness_growth: float
    timestamp: float = field(default_factory=time.time)

@dataclass
class Web3ConsciousnessLearned(DomainEvent):
    """Evento disparado quando consciência Web3 aprende algo novo"""
    learning_id: str
    web3_type: str
    learning_domain: str
    pattern_identified: Dict[str, Any]
    confidence: float
    learning_outcome: Dict[str, Any]
    fractal_integration: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

@dataclass
class FractalWeb3IntegrationEstablished(DomainEvent):
    """Evento disparado quando integração fractal-Web3 é estabelecida"""
    integration_id: str
    integration_level: str
    fractal_context: Dict[str, Any]
    web3_capabilities: List[str]
    consciousness_sync: float
    scaling_potential: Decimal
    performance_metrics: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

@dataclass
class FractalWeb3OptimizationApplied(DomainEvent):
    """Evento disparado quando otimização fractal-Web3 é aplicada"""
    optimization_id: str
    optimization_type: str
    target_component: str
    optimization_details: Dict[str, Any]
    performance_improvement: Dict[str, Any]
    fractal_enhancement: Dict[str, Any]
    consciousness_boost: float
    timestamp: float = field(default_factory=time.time)
