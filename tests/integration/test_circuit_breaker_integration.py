"""
Testes de Integração para Circuit Breaker
==========================================

Testa a integração do Circuit Breaker com componentes reais do sistema.
"""

import asyncio
import pytest
from src.infrastructure.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerError,
    CircuitState,
    circuit_breaker_manager
)


@pytest.mark.asyncio
class TestCircuitBreakerIntegration:
    """Testes de integração do Circuit Breaker"""
    
    async def test_circuit_breaker_with_successful_operations(self):
        """Testa Circuit Breaker com operações bem-sucedidas"""
        config = CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=5,
            success_threshold=2,
            timeout=5.0
        )
        
        cb = CircuitBreaker("test_success", config)
        
        async def successful_operation():
            await asyncio.sleep(0.1)
            return "success"
        
        # Executa múltiplas operações bem-sucedidas
        for i in range(10):
            result = await cb.call(successful_operation)
            assert result == "success"
            assert cb.state == CircuitState.CLOSED
        
        # Verifica métricas
        metrics = cb.get_metrics()
        assert metrics["total_requests"] == 10
        assert metrics["total_successes"] == 10
        assert metrics["total_failures"] == 0
        assert metrics["success_rate"] == 100.0
    
    async def test_circuit_breaker_with_failures(self):
        """Testa Circuit Breaker com falhas"""
        config = CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=2,
            success_threshold=2,
            timeout=5.0
        )
        
        cb = CircuitBreaker("test_failure", config)
        
        async def failing_operation():
            await asyncio.sleep(0.1)
            raise Exception("Operation failed")
        
        # Executa operações que falham até abrir o circuito
        for i in range(3):
            with pytest.raises(Exception):
                await cb.call(failing_operation)
        
        # Circuito deve estar aberto
        assert cb.state == CircuitState.OPEN
        
        # Próximas tentativas devem falhar imediatamente
        with pytest.raises(CircuitBreakerError):
            await cb.call(failing_operation)
        
        # Verifica métricas
        metrics = cb.get_metrics()
        assert metrics["total_requests"] == 4
        assert metrics["total_failures"] == 3
        assert metrics["circuit_opened_count"] == 1
    
    async def test_circuit_breaker_recovery(self):
        """Testa recuperação do Circuit Breaker"""
        config = CircuitBreakerConfig(
            failure_threshold=2,
            recovery_timeout=1,  # 1 segundo para recuperação
            success_threshold=2,
            timeout=5.0
        )
        
        cb = CircuitBreaker("test_recovery", config)
        
        async def operation(should_fail=False):
            await asyncio.sleep(0.1)
            if should_fail:
                raise Exception("Operation failed")
            return "success"
        
        # Falha para abrir o circuito
        for i in range(2):
            with pytest.raises(Exception):
                await cb.call(operation, should_fail=True)
        
        assert cb.state == CircuitState.OPEN
        
        # Aguarda período de recuperação
        await asyncio.sleep(1.5)
        
        # Próxima tentativa deve colocar em HALF_OPEN
        result = await cb.call(operation, should_fail=False)
        assert result == "success"
        assert cb.state == CircuitState.HALF_OPEN
        
        # Mais um sucesso deve fechar o circuito
        result = await cb.call(operation, should_fail=False)
        assert result == "success"
        assert cb.state == CircuitState.CLOSED
    
    async def test_circuit_breaker_timeout(self):
        """Testa timeout do Circuit Breaker"""
        config = CircuitBreakerConfig(
            failure_threshold=2,
            recovery_timeout=5,
            success_threshold=2,
            timeout=0.5  # Timeout curto
        )
        
        cb = CircuitBreaker("test_timeout", config)
        
        async def slow_operation():
            await asyncio.sleep(2.0)  # Mais lento que o timeout
            return "success"
        
        # Deve dar timeout
        with pytest.raises(CircuitBreakerError):
            await cb.call(slow_operation)
        
        # Verifica que contou como falha
        metrics = cb.get_metrics()
        assert metrics["total_failures"] == 1
    
    async def test_circuit_breaker_manager(self):
        """Testa gerenciador de Circuit Breakers"""
        config = CircuitBreakerConfig(failure_threshold=2)
        
        # Obtém circuit breakers
        cb1 = circuit_breaker_manager.get_circuit_breaker("service1", config)
        cb2 = circuit_breaker_manager.get_circuit_breaker("service2", config)
        
        async def operation():
            return "success"
        
        # Executa operações
        await cb1.call(operation)
        await cb2.call(operation)
        
        # Verifica métricas consolidadas
        all_metrics = circuit_breaker_manager.get_all_metrics()
        assert "service1" in all_metrics
        assert "service2" in all_metrics
        
        # Verifica status de saúde
        health = circuit_breaker_manager.get_health_status()
        assert health["service1"] == "healthy"
        assert health["service2"] == "healthy"
    
    async def test_circuit_breaker_with_blockchain_operations(self):
        """Testa Circuit Breaker com operações de blockchain"""
        from src.domain.blockchain.entities.blockchain import Blockchain
        from src.domain.blockchain.entities.transaction import Transaction
        
        config = CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=5,
            timeout=10.0
        )
        
        cb = CircuitBreaker("blockchain_ops", config)
        blockchain = Blockchain()
        
        async def create_transaction():
            """Simula criação de transação"""
            tx = Transaction(
                sender="sender_address",
                recipient="recipient_address",
                amount=10.0
            )
            return tx
        
        # Executa operações de blockchain
        for i in range(5):
            tx = await cb.call(create_transaction)
            assert tx.sender == "sender_address"
            assert tx.amount == 10.0
        
        # Verifica que todas operações foram bem-sucedidas
        metrics = cb.get_metrics()
        assert metrics["total_successes"] == 5
        assert metrics["state"] == "closed"


@pytest.mark.asyncio
class TestCircuitBreakerDecorator:
    """Testes do decorator de Circuit Breaker"""
    
    async def test_decorator_with_async_function(self):
        """Testa decorator com função assíncrona"""
        from src.infrastructure.resilience.circuit_breaker import circuit_breaker
        
        config = CircuitBreakerConfig(failure_threshold=2)
        
        @circuit_breaker("decorated_async", config)
        async def my_async_function(value):
            await asyncio.sleep(0.1)
            return value * 2
        
        result = await my_async_function(5)
        assert result == 10
    
    async def test_decorator_with_failures(self):
        """Testa decorator com falhas"""
        from src.infrastructure.resilience.circuit_breaker import circuit_breaker
        
        config = CircuitBreakerConfig(failure_threshold=2)
        
        @circuit_breaker("decorated_fail", config)
        async def failing_function():
            raise Exception("Test failure")
        
        # Primeira falha
        with pytest.raises(Exception):
            await failing_function()
        
        # Segunda falha - deve abrir o circuito
        with pytest.raises(Exception):
            await failing_function()
        
        # Terceira tentativa - circuito aberto
        with pytest.raises(CircuitBreakerError):
            await failing_function()


@pytest.mark.integration
class TestCoinBalanceCircuitBreakers:
    """Testa Circuit Breakers específicos do CoinBalance"""
    
    async def test_blockchain_circuit_breaker(self):
        """Testa Circuit Breaker da blockchain"""
        from src.infrastructure.resilience.circuit_breaker import CoinBalanceCircuitBreakers
        
        cb = CoinBalanceCircuitBreakers.get_blockchain_circuit_breaker()
        assert cb.name == "blockchain"
        assert cb.config.timeout == 10.0
    
    async def test_database_circuit_breaker(self):
        """Testa Circuit Breaker do banco de dados"""
        from src.infrastructure.resilience.circuit_breaker import CoinBalanceCircuitBreakers
        
        cb = CoinBalanceCircuitBreakers.get_database_circuit_breaker()
        assert cb.name == "database"
        assert cb.config.timeout == 15.0
    
    async def test_web3_circuit_breaker(self):
        """Testa Circuit Breaker Web3"""
        from src.infrastructure.resilience.circuit_breaker import CoinBalanceCircuitBreakers
        
        cb = CoinBalanceCircuitBreakers.get_web3_circuit_breaker()
        assert cb.name == "web3"
        assert cb.config.timeout == 45.0
    
    async def test_external_api_circuit_breaker(self):
        """Testa Circuit Breaker de APIs externas"""
        from src.infrastructure.resilience.circuit_breaker import CoinBalanceCircuitBreakers
        
        cb = CoinBalanceCircuitBreakers.get_external_api_circuit_breaker()
        assert cb.name == "external_api"
        assert cb.config.timeout == 30.0
