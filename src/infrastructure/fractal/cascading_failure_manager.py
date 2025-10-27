"""
Sistema de Tratamento de Falhas em Cascata para Ecossistema Fractal
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import threading
from collections import defaultdict, deque

logger = logging.getLogger(__name__)


class FailureSeverity(Enum):
    """Níveis de severidade de falha"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    CATASTROPHIC = "catastrophic"


class FailureType(Enum):
    """Tipos de falha"""
    SYSTEM_FAILURE = "system_failure"
    NETWORK_FAILURE = "network_failure"
    DATA_CORRUPTION = "data_corruption"
    SECURITY_BREACH = "security_breach"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    CASCADING_FAILURE = "cascading_failure"


@dataclass
class FailureEvent:
    """Evento de falha"""
    system_id: str
    failure_type: FailureType
    severity: FailureSeverity
    message: str
    timestamp: float = field(default_factory=time.time)
    affected_systems: List[str] = field(default_factory=list)
    recovery_actions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RecoveryAction:
    """Ação de recuperação"""
    action_id: str
    description: str
    target_system: str
    priority: int
    timeout_seconds: int = 30
    retry_count: int = 3
    success_callback: Optional[Callable] = None
    failure_callback: Optional[Callable] = None


class CascadingFailureManager:
    """
    Gerenciador de falhas em cascata para o ecossistema fractal.
    
    Este sistema monitora falhas e implementa estratégias de contenção
    para evitar que falhas se propaguem através do ecossistema.
    """
    
    def __init__(self):
        self.failure_history: deque = deque(maxlen=1000)
        self.active_failures: Dict[str, FailureEvent] = {}
        self.system_dependencies: Dict[str, List[str]] = defaultdict(list)
        self.recovery_actions: Dict[str, RecoveryAction] = {}
        self.system_health: Dict[str, float] = {}
        self._lock = threading.RLock()
        
        # Configurações de contenção
        self.cascade_threshold = 0.7  # Limiar para ativar contenção
        self.isolation_enabled = True
        self.auto_recovery_enabled = True
        
        logger.info("CascadingFailureManager inicializado")
    
    def register_system_dependency(self, system_id: str, depends_on: List[str]) -> None:
        """
        Registra dependências entre sistemas.
        
        Args:
            system_id: ID do sistema
            depends_on: Lista de sistemas dos quais depende
        """
        with self._lock:
            self.system_dependencies[system_id] = depends_on
            logger.info(f"Dependências registradas para {system_id}: {depends_on}")
    
    def report_failure(self, failure_event: FailureEvent) -> None:
        """
        Reporta uma falha no sistema.
        
        Args:
            failure_event: Evento de falha
        """
        with self._lock:
            self.failure_history.append(failure_event)
            self.active_failures[failure_event.system_id] = failure_event
            
            logger.warning(f"Falha reportada: {failure_event.system_id} - {failure_event.failure_type.value}")
            
            # Verificar se precisa ativar contenção
            if self._should_activate_containment(failure_event):
                self._activate_containment(failure_event)
            
            # Executar ações de recuperação
            if self.auto_recovery_enabled:
                asyncio.create_task(self._execute_recovery_actions(failure_event))
    
    def _should_activate_containment(self, failure_event: FailureEvent) -> bool:
        """
        Determina se deve ativar contenção baseado na falha.
        
        Args:
            failure_event: Evento de falha
            
        Returns:
            True se deve ativar contenção
        """
        # Ativar contenção para falhas críticas ou catastróficas
        if failure_event.severity in [FailureSeverity.CRITICAL, FailureSeverity.CATASTROPHIC]:
            return True
        
        # Ativar contenção se muitos sistemas estão falhando
        failure_count = len(self.active_failures)
        total_systems = len(self.system_dependencies)
        
        if total_systems > 0 and failure_count / total_systems >= self.cascade_threshold:
            return True
        
        return False
    
    def _activate_containment(self, failure_event: FailureEvent) -> None:
        """
        Ativa estratégias de contenção para evitar propagação.
        
        Args:
            failure_event: Evento de falha que disparou a contenção
        """
        logger.critical(f"ATIVANDO CONTENÇÃO devido a falha em {failure_event.system_id}")
        
        # Isolar sistemas dependentes
        affected_systems = self._get_affected_systems(failure_event.system_id)
        
        for system_id in affected_systems:
            self._isolate_system(system_id)
        
        # Implementar circuit breaker
        self._implement_circuit_breaker(failure_event.system_id)
    
    def _get_affected_systems(self, failed_system: str) -> List[str]:
        """
        Obtém sistemas que podem ser afetados pela falha.
        
        Args:
            failed_system: Sistema que falhou
            
        Returns:
            Lista de sistemas afetados
        """
        affected = []
        
        # Sistemas que dependem do sistema falhado
        for system_id, dependencies in self.system_dependencies.items():
            if failed_system in dependencies:
                affected.append(system_id)
        
        return affected
    
    def _isolate_system(self, system_id: str) -> None:
        """
        Isola um sistema para evitar propagação de falhas.
        
        Args:
            system_id: ID do sistema a ser isolado
        """
        logger.warning(f"Isolando sistema {system_id}")
        
        # Implementar isolamento (desconectar, pausar, etc.)
        self.system_health[system_id] = 0.0
        
        # Aqui seria implementada a lógica específica de isolamento
        # Por exemplo: desconectar do load balancer, pausar processamento, etc.
    
    def _implement_circuit_breaker(self, system_id: str) -> None:
        """
        Implementa circuit breaker para um sistema.
        
        Args:
            system_id: ID do sistema
        """
        logger.warning(f"Implementando circuit breaker para {system_id}")
        
        # Implementar circuit breaker pattern
        # Por enquanto, apenas marcar como isolado
        self.system_health[system_id] = 0.0
    
    async def _execute_recovery_actions(self, failure_event: FailureEvent) -> None:
        """
        Executa ações de recuperação para uma falha.
        
        Args:
            failure_event: Evento de falha
        """
        recovery_actions = self._get_recovery_actions(failure_event)
        
        for action in recovery_actions:
            try:
                await self._execute_recovery_action(action)
            except Exception as e:
                logger.error(f"Erro ao executar ação de recuperação {action.action_id}: {e}")
    
    def _get_recovery_actions(self, failure_event: FailureEvent) -> List[RecoveryAction]:
        """
        Obtém ações de recuperação para uma falha.
        
        Args:
            failure_event: Evento de falha
            
        Returns:
            Lista de ações de recuperação
        """
        actions = []
        
        # Ações baseadas no tipo de falha
        if failure_event.failure_type == FailureType.SYSTEM_FAILURE:
            actions.append(RecoveryAction(
                action_id=f"restart_{failure_event.system_id}",
                description=f"Reiniciar sistema {failure_event.system_id}",
                target_system=failure_event.system_id,
                priority=1
            ))
        
        elif failure_event.failure_type == FailureType.NETWORK_FAILURE:
            actions.append(RecoveryAction(
                action_id=f"reconnect_{failure_event.system_id}",
                description=f"Reconectar sistema {failure_event.system_id}",
                target_system=failure_event.system_id,
                priority=2
            ))
        
        elif failure_event.failure_type == FailureType.RESOURCE_EXHAUSTION:
            actions.append(RecoveryAction(
                action_id=f"scale_{failure_event.system_id}",
                description=f"Escalar recursos para {failure_event.system_id}",
                target_system=failure_event.system_id,
                priority=1
            ))
        
        return actions
    
    async def _execute_recovery_action(self, action: RecoveryAction) -> None:
        """
        Executa uma ação de recuperação.
        
        Args:
            action: Ação de recuperação
        """
        logger.info(f"Executando ação de recuperação: {action.description}")
        
        # Simular execução da ação
        await asyncio.sleep(1)  # Simular tempo de execução
        
        # Marcar como executada
        logger.info(f"Ação de recuperação {action.action_id} executada com sucesso")
        
        # Atualizar saúde do sistema
        if action.target_system in self.system_health:
            self.system_health[action.target_system] = min(1.0, self.system_health[action.target_system] + 0.3)
    
    def get_system_health(self, system_id: str) -> float:
        """
        Obtém a saúde de um sistema.
        
        Args:
            system_id: ID do sistema
            
        Returns:
            Saúde do sistema (0.0 a 1.0)
        """
        return self.system_health.get(system_id, 1.0)
    
    def get_ecosystem_health(self) -> float:
        """
        Obtém a saúde geral do ecossistema.
        
        Returns:
            Saúde do ecossistema (0.0 a 1.0)
        """
        if not self.system_health:
            return 1.0
        
        total_health = sum(self.system_health.values())
        return total_health / len(self.system_health)
    
    def get_failure_summary(self) -> Dict[str, Any]:
        """
        Obtém resumo das falhas.
        
        Returns:
            Resumo das falhas
        """
        with self._lock:
            return {
                "active_failures": len(self.active_failures),
                "total_failures": len(self.failure_history),
                "ecosystem_health": self.get_ecosystem_health(),
                "containment_active": len(self.active_failures) > 0,
                "recent_failures": [
                    {
                        "system": f.system_id,
                        "type": f.failure_type.value,
                        "severity": f.severity.value,
                        "timestamp": f.timestamp
                    }
                    for f in list(self.failure_history)[-10:]  # Últimas 10 falhas
                ]
            }


# Instância global do gerenciador de falhas em cascata
cascading_failure_manager = CascadingFailureManager()
