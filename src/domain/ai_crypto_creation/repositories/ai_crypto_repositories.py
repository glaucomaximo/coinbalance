"""
Repositórios para AI Crypto Creation
===================================

Interfaces de repositório padronizadas para o módulo de criação
de criptomoedas com IA, seguindo os padrões DDD estabelecidos.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from decimal import Decimal
import time

from src.domain.ai_crypto_creation.entities.crypto_intelligence import CryptoSpecification
from src.domain.ai_crypto_creation.services.token_factory import TokenTemplate
from src.domain.ai_crypto_creation.services.autonomous_economy import EconomicDecision, EcosystemHealth

@dataclass
class CryptoSpecificationEntity:
    """Entidade de especificação de criptomoeda"""
    crypto_id: str
    name: str
    symbol: str
    purpose: str
    target_market: str
    specification: Dict[str, Any]
    ai_reasoning: str
    confidence_score: float
    fractal_scaling: Decimal
    evolution_potential: bool
    created_at: float
    updated_at: float

@dataclass
class TokenTemplateEntity:
    """Entidade de template de token"""
    template_id: str
    name: str
    symbol: str
    category: str
    standard: str
    description: str
    features: List[str]
    use_cases: List[str]
    tokenomics: Dict[str, Any]
    smart_contract_code: str
    deployment_instructions: List[str]
    confidence_score: float
    fractal_optimization: Dict[str, Any]
    created_at: float

@dataclass
class EconomicDecisionEntity:
    """Entidade de decisão econômica"""
    decision_id: str
    decision_type: str
    reasoning: str
    expected_outcome: str
    confidence: float
    impact_assessment: Dict[str, Any]
    execution_plan: List[str]
    fractal_context: Dict[str, Any]
    executed: bool
    execution_result: Optional[Dict[str, Any]]
    created_at: float
    executed_at: Optional[float]

class AICryptoRepository(ABC):
    """Interface de repositório para especificações de criptomoedas"""
    
    @abstractmethod
    async def save_crypto_specification(self, specification: CryptoSpecificationEntity) -> bool:
        """Salva especificação de criptomoeda"""
        pass
    
    @abstractmethod
    async def get_crypto_specification(self, crypto_id: str) -> Optional[CryptoSpecificationEntity]:
        """Obtém especificação de criptomoeda por ID"""
        pass
    
    @abstractmethod
    async def get_cryptos_by_purpose(self, purpose: str) -> List[CryptoSpecificationEntity]:
        """Obtém criptomoedas por propósito"""
        pass
    
    @abstractmethod
    async def get_cryptos_by_market(self, target_market: str) -> List[CryptoSpecificationEntity]:
        """Obtém criptomoedas por mercado alvo"""
        pass
    
    @abstractmethod
    async def get_cryptos_by_confidence(self, min_confidence: float) -> List[CryptoSpecificationEntity]:
        """Obtém criptomoedas por nível de confiança"""
        pass
    
    @abstractmethod
    async def update_crypto_specification(self, crypto_id: str, updates: Dict[str, Any]) -> bool:
        """Atualiza especificação de criptomoeda"""
        pass
    
    @abstractmethod
    async def delete_crypto_specification(self, crypto_id: str) -> bool:
        """Remove especificação de criptomoeda"""
        pass
    
    @abstractmethod
    async def get_all_crypto_specifications(self, limit: Optional[int] = None) -> List[CryptoSpecificationEntity]:
        """Obtém todas as especificações de criptomoedas"""
        pass

class TokenTemplateRepository(ABC):
    """Interface de repositório para templates de tokens"""
    
    @abstractmethod
    async def save_token_template(self, template: TokenTemplateEntity) -> bool:
        """Salva template de token"""
        pass
    
    @abstractmethod
    async def get_token_template(self, template_id: str) -> Optional[TokenTemplateEntity]:
        """Obtém template de token por ID"""
        pass
    
    @abstractmethod
    async def get_templates_by_category(self, category: str) -> List[TokenTemplateEntity]:
        """Obtém templates por categoria"""
        pass
    
    @abstractmethod
    async def get_templates_by_standard(self, standard: str) -> List[TokenTemplateEntity]:
        """Obtém templates por padrão"""
        pass
    
    @abstractmethod
    async def get_templates_by_confidence(self, min_confidence: float) -> List[TokenTemplateEntity]:
        """Obtém templates por nível de confiança"""
        pass
    
    @abstractmethod
    async def search_templates(self, query: str) -> List[TokenTemplateEntity]:
        """Busca templates por query"""
        pass
    
    @abstractmethod
    async def get_all_token_templates(self, limit: Optional[int] = None) -> List[TokenTemplateEntity]:
        """Obtém todos os templates de tokens"""
        pass

class EconomicDecisionRepository(ABC):
    """Interface de repositório para decisões econômicas"""
    
    @abstractmethod
    async def save_economic_decision(self, decision: EconomicDecisionEntity) -> bool:
        """Salva decisão econômica"""
        pass
    
    @abstractmethod
    async def get_economic_decision(self, decision_id: str) -> Optional[EconomicDecisionEntity]:
        """Obtém decisão econômica por ID"""
        pass
    
    @abstractmethod
    async def get_decisions_by_type(self, decision_type: str) -> List[EconomicDecisionEntity]:
        """Obtém decisões por tipo"""
        pass
    
    @abstractmethod
    async def get_pending_decisions(self) -> List[EconomicDecisionEntity]:
        """Obtém decisões pendentes"""
        pass
    
    @abstractmethod
    async def get_executed_decisions(self) -> List[EconomicDecisionEntity]:
        """Obtém decisões executadas"""
        pass
    
    @abstractmethod
    async def update_decision_execution(self, decision_id: str, execution_result: Dict[str, Any]) -> bool:
        """Atualiza resultado de execução de decisão"""
        pass
    
    @abstractmethod
    async def get_decisions_by_confidence(self, min_confidence: float) -> List[EconomicDecisionEntity]:
        """Obtém decisões por nível de confiança"""
        pass
    
    @abstractmethod
    async def get_all_economic_decisions(self, limit: Optional[int] = None) -> List[EconomicDecisionEntity]:
        """Obtém todas as decisões econômicas"""
        pass

class Web3ConsciousnessRepository(ABC):
    """Interface de repositório para consciência Web3"""
    
    @abstractmethod
    async def save_consciousness_state(self, state: Dict[str, Any]) -> bool:
        """Salva estado de consciência"""
        pass
    
    @abstractmethod
    async def get_consciousness_state(self, state_id: str) -> Optional[Dict[str, Any]]:
        """Obtém estado de consciência por ID"""
        pass
    
    @abstractmethod
    async def save_learning_pattern(self, pattern: Dict[str, Any]) -> bool:
        """Salva padrão de aprendizado"""
        pass
    
    @abstractmethod
    async def get_learning_patterns(self, web3_type: str) -> List[Dict[str, Any]]:
        """Obtém padrões de aprendizado por tipo Web3"""
        pass
    
    @abstractmethod
    async def get_consciousness_metrics(self) -> Dict[str, Any]:
        """Obtém métricas de consciência"""
        pass
    
    @abstractmethod
    async def update_consciousness_level(self, level: float) -> bool:
        """Atualiza nível de consciência"""
        pass

class FractalWeb3IntegrationRepository(ABC):
    """Interface de repositório para integração fractal-Web3"""
    
    @abstractmethod
    async def save_integration_context(self, context: Dict[str, Any]) -> bool:
        """Salva contexto de integração"""
        pass
    
    @abstractmethod
    async def get_integration_context(self, context_id: str) -> Optional[Dict[str, Any]]:
        """Obtém contexto de integração por ID"""
        pass
    
    @abstractmethod
    async def save_conscious_deployment(self, deployment: Dict[str, Any]) -> bool:
        """Salva deploy consciente"""
        pass
    
    @abstractmethod
    async def get_conscious_deployments(self) -> List[Dict[str, Any]]:
        """Obtém deploys conscientes"""
        pass
    
    @abstractmethod
    async def save_optimization_result(self, optimization: Dict[str, Any]) -> bool:
        """Salva resultado de otimização"""
        pass
    
    @abstractmethod
    async def get_optimization_history(self) -> List[Dict[str, Any]]:
        """Obtém histórico de otimizações"""
        pass
    
    @abstractmethod
    async def get_integration_health(self) -> Dict[str, Any]:
        """Obtém saúde da integração"""
        pass

class HolisticMonitoringRepository(ABC):
    """Interface de repositório para monitoramento holístico"""
    
    @abstractmethod
    async def save_component_health(self, component: str, health_data: Dict[str, Any]) -> bool:
        """Salva saúde de componente"""
        pass
    
    @abstractmethod
    async def get_component_health_history(self, component: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtém histórico de saúde de componente"""
        pass
    
    @abstractmethod
    async def save_ecosystem_insight(self, insight: Dict[str, Any]) -> bool:
        """Salva insight do ecossistema"""
        pass
    
    @abstractmethod
    async def get_ecosystem_insights(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtém insights do ecossistema"""
        pass
    
    @abstractmethod
    async def save_holistic_alert(self, alert: Dict[str, Any]) -> bool:
        """Salva alerta holístico"""
        pass
    
    @abstractmethod
    async def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Obtém alertas ativos"""
        pass
    
    @abstractmethod
    async def get_alert_correlations(self) -> List[Dict[str, Any]]:
        """Obtém correlações de alertas"""
        pass
    
    @abstractmethod
    async def save_optimization_recommendation(self, recommendation: Dict[str, Any]) -> bool:
        """Salva recomendação de otimização"""
        pass
    
    @abstractmethod
    async def get_optimization_recommendations(self, priority: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtém recomendações de otimização"""
        pass
