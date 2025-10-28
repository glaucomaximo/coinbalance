"""
Circuit Breaker Pattern Implementation for CoinBalance Enterprise
================================================================

Este módulo implementa o padrão Circuit Breaker para melhorar a resiliência
do sistema CoinBalance Enterprise, protegendo contra falhas em cascata
e melhorando a experiência do usuário.
"""

import asyncio
import time
import logging
from enum import Enum
from typing import Callable, Any, Optional, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Estados do Circuit Breaker"""
    CLOSED = "closed"      # Estado normal, requisições passam
    OPEN = "open"          # Estado de falha, requisições bloqueadas
    HALF_OPEN = "half_open"  # Estado de teste, algumas requisições passam


@dataclass
class CircuitBreakerConfig:
    """Configuração do Circuit Breaker"""
    failure_threshold: int = 5          # Número de falhas para abrir o circuito
    recovery_timeout: int = 60          # Tempo em segundos para tentar recuperação
    success_threshold: int = 3          # Número de sucessos para fechar o circuito
    timeout: float = 30.0               # Timeout para operações
    expected_exception: tuple = (Exception,)  # Exceções que contam como falha


class CircuitBreakerError(Exception):
    """Exceção lançada quando o Circuit Breaker está aberto"""
    pass


class CircuitBreaker:
    """
    Implementação do padrão Circuit Breaker para CoinBalance Enterprise
    
    O Circuit Breaker protege o sistema contra falhas em cascata,
    abrindo o circuito quando há muitas falhas e tentando recuperação
    após um período de tempo.
    """
    
    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.last_success_time = None
        
        # Métricas
        self.total_requests = 0
        self.total_failures = 0
        self.total_successes = 0
        self.circuit_opened_count = 0
        
        logger.info(f"Circuit Breaker '{name}' inicializado com configuração: {self.config}")
    
    def _should_attempt_reset(self) -> bool:
        """Verifica se deve tentar resetar o circuito"""
        if self.state != CircuitState.OPEN:
            return False
        
        if self.last_failure_time is None:
            return True
        
        time_since_failure = time.time() - self.last_failure_time
        return time_since_failure >= self.config.recovery_timeout
    
    def _on_success(self):
        """Chamado quando uma operação é bem-sucedida"""
        self.success_count += 1
        self.total_successes += 1
        self.last_success_time = time.time()
        
        logger.debug(f"Circuit Breaker '{self.name}': Sucesso #{self.success_count}")
        
        if self.state == CircuitState.HALF_OPEN:
            if self.success_count >= self.config.success_threshold:
                self._close_circuit()
        elif self.state == CircuitState.CLOSED:
            # Reset contador de falhas em caso de sucesso
            self.failure_count = 0
    
    def _on_failure(self):
        """Chamado quando uma operação falha"""
        self.failure_count += 1
        self.total_failures += 1
        self.last_failure_time = time.time()
        
        logger.warning(f"Circuit Breaker '{self.name}': Falha #{self.failure_count}")
        
        if self.state == CircuitState.CLOSED:
            if self.failure_count >= self.config.failure_threshold:
                self._open_circuit()
        elif self.state == CircuitState.HALF_OPEN:
            self._open_circuit()
    
    def _open_circuit(self):
        """Abre o circuito"""
        self.state = CircuitState.OPEN
        self.circuit_opened_count += 1
        self.success_count = 0
        
        logger.error(f"Circuit Breaker '{self.name}': Circuito ABERTO após {self.failure_count} falhas")
    
    def _close_circuit(self):
        """Fecha o circuito"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        
        logger.info(f"Circuit Breaker '{self.name}': Circuito FECHADO após {self.success_count} sucessos")
    
    def _half_open_circuit(self):
        """Coloca o circuito em estado half-open"""
        self.state = CircuitState.HALF_OPEN
        self.success_count = 0
        
        logger.info(f"Circuit Breaker '{self.name}': Circuito HALF-OPEN - testando recuperação")
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Executa uma função com proteção do Circuit Breaker
        
        Args:
            func: Função a ser executada
            *args: Argumentos posicionais
            **kwargs: Argumentos nomeados
            
        Returns:
            Resultado da função
            
        Raises:
            CircuitBreakerError: Se o circuito estiver aberto
        """
        self.total_requests += 1
        
        # Verifica se deve tentar resetar o circuito
        if self._should_attempt_reset():
            self._half_open_circuit()
        
        # Verifica se o circuito está aberto
        if self.state == CircuitState.OPEN:
            raise CircuitBreakerError(f"Circuit Breaker '{self.name}' está aberto")
        
        try:
            # Executa a função com timeout
            if asyncio.iscoroutinefunction(func):
                result = await asyncio.wait_for(func(*args, **kwargs), timeout=self.config.timeout)
            else:
                result = await asyncio.wait_for(
                    asyncio.get_event_loop().run_in_executor(None, func, *args, **kwargs),
                    timeout=self.config.timeout
                )
            
            self._on_success()
            return result
            
        except self.config.expected_exception as e:
            self._on_failure()
            raise e
        except asyncio.TimeoutError:
            self._on_failure()
            raise CircuitBreakerError(f"Circuit Breaker '{self.name}': Timeout após {self.config.timeout}s")
        except Exception as e:
            self._on_failure()
            raise CircuitBreakerError(f"Circuit Breaker '{self.name}': Erro inesperado - {str(e)}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas do Circuit Breaker"""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "total_requests": self.total_requests,
            "total_failures": self.total_failures,
            "total_successes": self.total_successes,
            "circuit_opened_count": self.circuit_opened_count,
            "last_failure_time": self.last_failure_time,
            "last_success_time": self.last_success_time,
            "success_rate": (self.total_successes / self.total_requests * 100) if self.total_requests > 0 else 0,
            "failure_rate": (self.total_failures / self.total_requests * 100) if self.total_requests > 0 else 0
        }
    
    def reset(self):
        """Reseta o Circuit Breaker para estado inicial"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.last_success_time = None
        
        logger.info(f"Circuit Breaker '{self.name}': Resetado para estado inicial")


class CircuitBreakerManager:
    """
    Gerenciador de Circuit Breakers para CoinBalance Enterprise
    
    Permite gerenciar múltiplos Circuit Breakers de forma centralizada
    e fornece métricas consolidadas.
    """
    
    def __init__(self):
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        logger.info("Circuit Breaker Manager inicializado")
    
    def get_circuit_breaker(self, name: str, config: CircuitBreakerConfig = None) -> CircuitBreaker:
        """Obtém ou cria um Circuit Breaker"""
        if name not in self.circuit_breakers:
            self.circuit_breakers[name] = CircuitBreaker(name, config)
            logger.info(f"Circuit Breaker '{name}' criado")
        
        return self.circuit_breakers[name]
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Retorna métricas de todos os Circuit Breakers"""
        metrics = {}
        for name, cb in self.circuit_breakers.items():
            metrics[name] = cb.get_metrics()
        
        return metrics
    
    def reset_all(self):
        """Reseta todos os Circuit Breakers"""
        for cb in self.circuit_breakers.values():
            cb.reset()
        
        logger.info("Todos os Circuit Breakers foram resetados")
    
    def get_health_status(self) -> Dict[str, str]:
        """Retorna status de saúde de todos os Circuit Breakers"""
        health = {}
        for name, cb in self.circuit_breakers.items():
            if cb.state == CircuitState.CLOSED:
                health[name] = "healthy"
            elif cb.state == CircuitState.HALF_OPEN:
                health[name] = "degraded"
            else:
                health[name] = "unhealthy"
        
        return health


# Instância global do gerenciador
circuit_breaker_manager = CircuitBreakerManager()


def circuit_breaker(name: str, config: CircuitBreakerConfig = None):
    """
    Decorator para aplicar Circuit Breaker a funções
    
    Args:
        name: Nome do Circuit Breaker
        config: Configuração do Circuit Breaker
    """
    def decorator(func):
        cb = circuit_breaker_manager.get_circuit_breaker(name, config)
        
        async def async_wrapper(*args, **kwargs):
            return await cb.call(func, *args, **kwargs)
        
        def sync_wrapper(*args, **kwargs):
            return cb.call(func, *args, **kwargs)
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


# Exemplos de uso para CoinBalance Enterprise
class CoinBalanceCircuitBreakers:
    """Circuit Breakers específicos para CoinBalance Enterprise"""
    
    @staticmethod
    def get_blockchain_circuit_breaker():
        """Circuit Breaker para operações de blockchain"""
        config = CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=30,
            success_threshold=2,
            timeout=10.0
        )
        return circuit_breaker_manager.get_circuit_breaker("blockchain", config)
    
    @staticmethod
    def get_database_circuit_breaker():
        """Circuit Breaker para operações de banco de dados"""
        config = CircuitBreakerConfig(
            failure_threshold=5,
            recovery_timeout=60,
            success_threshold=3,
            timeout=15.0
        )
        return circuit_breaker_manager.get_circuit_breaker("database", config)
    
    @staticmethod
    def get_external_api_circuit_breaker():
        """Circuit Breaker para APIs externas"""
        config = CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=120,
            success_threshold=2,
            timeout=30.0
        )
        return circuit_breaker_manager.get_circuit_breaker("external_api", config)
    
    @staticmethod
    def get_web3_circuit_breaker():
        """Circuit Breaker para operações Web3"""
        config = CircuitBreakerConfig(
            failure_threshold=4,
            recovery_timeout=90,
            success_threshold=2,
            timeout=45.0
        )
        return circuit_breaker_manager.get_circuit_breaker("web3", config)
