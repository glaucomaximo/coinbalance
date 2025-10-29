"""
Testes de Integração para Health Checks
========================================

Testa a integração do sistema de health checks com componentes reais.
"""

import asyncio
import pytest
from src.infrastructure.monitoring.health_checks import (
    HealthCheckManager,
    HealthCheck,
    HealthStatus,
    DatabaseHealthCheck,
    SystemHealthCheck,
    BlockchainHealthCheck,
    health_check_manager
)


@pytest.mark.asyncio
class TestHealthCheckIntegration:
    """Testes de integração dos health checks"""
    
    async def test_database_health_check(self):
        """Testa health check do banco de dados"""
        result = await DatabaseHealthCheck.check_database_connection()
        
        assert result.component == "database"
        assert result.status in [HealthStatus.HEALTHY, HealthStatus.UNHEALTHY]
        assert result.response_time > 0
        assert result.timestamp > 0
    
    async def test_database_performance_check(self):
        """Testa health check de performance do banco"""
        result = await DatabaseHealthCheck.check_database_performance()
        
        assert result.component == "database"
        assert result.response_time > 0
        
        if result.status == HealthStatus.HEALTHY:
            assert "block_count" in result.details
            assert "transaction_count" in result.details
    
    async def test_system_cpu_check(self):
        """Testa health check de CPU"""
        result = await SystemHealthCheck.check_cpu_usage()
        
        assert result.component == "system"
        assert result.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.UNHEALTHY]
        assert "cpu_percent" in result.details
        assert 0 <= result.details["cpu_percent"] <= 100
    
    async def test_system_memory_check(self):
        """Testa health check de memória"""
        result = await SystemHealthCheck.check_memory_usage()
        
        assert result.component == "system"
        assert result.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.UNHEALTHY]
        assert "memory_percent" in result.details
        assert "memory_available" in result.details
        assert "memory_total" in result.details
    
    async def test_system_disk_check(self):
        """Testa health check de disco"""
        result = await SystemHealthCheck.check_disk_usage()
        
        assert result.component == "system"
        assert result.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.UNHEALTHY]
        assert "disk_percent" in result.details
        assert "disk_free" in result.details
        assert "disk_total" in result.details
    
    async def test_blockchain_integrity_check(self):
        """Testa health check de integridade da blockchain"""
        result = await BlockchainHealthCheck.check_blockchain_integrity()
        
        assert result.component == "blockchain"
        assert result.status in [
            HealthStatus.HEALTHY,
            HealthStatus.DEGRADED,
            HealthStatus.UNHEALTHY
        ]


@pytest.mark.asyncio
class TestHealthCheckManager:
    """Testes do gerenciador de health checks"""
    
    async def test_manager_initialization(self):
        """Testa inicialização do manager"""
        manager = HealthCheckManager()
        
        # Verifica que health checks padrão foram registrados
        assert len(manager.health_checks) > 0
        assert "database_connection" in manager.health_checks
        assert "cpu_usage" in manager.health_checks
        assert "memory_usage" in manager.health_checks
    
    async def test_run_specific_health_check(self):
        """Testa execução de health check específico"""
        manager = HealthCheckManager()
        
        result = await manager.run_health_check("cpu_usage")
        
        assert result is not None
        assert result.component == "system"
        assert result.timestamp > 0
    
    async def test_run_all_health_checks(self):
        """Testa execução de todos os health checks"""
        manager = HealthCheckManager()
        
        results = await manager.run_all_health_checks()
        
        assert len(results) > 0
        assert "cpu_usage" in results
        assert "memory_usage" in results
        assert "disk_usage" in results
    
    async def test_overall_health_status(self):
        """Testa status geral de saúde"""
        manager = HealthCheckManager()
        
        # Executa todos os health checks
        await manager.run_all_health_checks()
        
        # Obtém status geral
        overall = manager.get_overall_health()
        
        assert "status" in overall
        assert "message" in overall
        assert "timestamp" in overall
        assert "components" in overall
        
        components = overall["components"]
        assert "total" in components
        assert "healthy" in components
        assert "degraded" in components
        assert "unhealthy" in components
    
    async def test_health_history(self):
        """Testa histórico de health checks"""
        manager = HealthCheckManager()
        
        # Executa múltiplas vezes
        for i in range(5):
            await manager.run_health_check("cpu_usage")
            await asyncio.sleep(0.1)
        
        # Verifica histórico
        history = manager.get_health_history("cpu_usage", limit=10)
        
        assert len(history) == 5
        assert all(h.component == "system" for h in history)
    
    async def test_register_custom_health_check(self):
        """Testa registro de health check customizado"""
        manager = HealthCheckManager()
        
        async def custom_check():
            return {
                "component": "custom",
                "status": HealthStatus.HEALTHY,
                "message": "Custom check OK",
                "timestamp": asyncio.get_event_loop().time(),
                "response_time": 0.1
            }
        
        custom_hc = HealthCheck(
            name="custom_check",
            component="custom",
            check_function=custom_check,
            timeout=5.0,
            critical=True
        )
        
        manager.register_health_check(custom_hc)
        
        assert "custom_check" in manager.health_checks


@pytest.mark.integration
class TestHealthCheckWithCircuitBreaker:
    """Testa integração entre Health Checks e Circuit Breaker"""
    
    async def test_health_check_with_circuit_breaker(self):
        """Testa health check protegido por Circuit Breaker"""
        from src.infrastructure.resilience.circuit_breaker import (
            CircuitBreaker,
            CircuitBreakerConfig
        )
        
        config = CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=5,
            timeout=10.0
        )
        
        cb = CircuitBreaker("health_check", config)
        
        async def protected_health_check():
            """Health check protegido"""
            result = await SystemHealthCheck.check_cpu_usage()
            return result
        
        # Executa health check protegido
        result = await cb.call(protected_health_check)
        
        assert result.component == "system"
        assert cb.state.value == "closed"
    
    async def test_health_check_manager_with_circuit_breakers(self):
        """Testa manager com circuit breakers"""
        from src.infrastructure.resilience.circuit_breaker import circuit_breaker_manager
        
        manager = HealthCheckManager()
        
        # Executa health checks
        await manager.run_all_health_checks()
        
        # Verifica status dos circuit breakers
        cb_health = circuit_breaker_manager.get_health_status()
        
        # Todos devem estar healthy inicialmente
        for name, status in cb_health.items():
            assert status in ["healthy", "degraded", "unhealthy"]


@pytest.mark.integration
@pytest.mark.slow
class TestPeriodicHealthChecks:
    """Testa verificações periódicas de saúde"""
    
    async def test_periodic_checks(self):
        """Testa execução periódica de health checks"""
        manager = HealthCheckManager()
        
        # Inicia verificações periódicas (intervalo curto para teste)
        task = asyncio.create_task(manager.start_periodic_checks(interval=2))
        
        # Aguarda algumas execuções
        await asyncio.sleep(5)
        
        # Para verificações
        manager.stop_periodic_checks()
        task.cancel()
        
        try:
            await task
        except asyncio.CancelledError:
            pass
        
        # Verifica que foram executados múltiplos checks
        history = manager.get_health_history("cpu_usage", limit=10)
        assert len(history) >= 2  # Pelo menos 2 execuções


@pytest.mark.integration
class TestHealthCheckEndpoints:
    """Testa endpoints de health check da API"""
    
    async def test_api_health_endpoints(self):
        """Testa endpoints de saúde da API"""
        from src.infrastructure.monitoring.health_checks import APIHealthCheck
        
        # Nota: Este teste pode falhar se a API não estiver rodando
        result = await APIHealthCheck.check_api_endpoints()
        
        assert result.component == "api"
        
        if result.status == HealthStatus.HEALTHY:
            assert "endpoints" in result.details
            endpoints = result.details["endpoints"]
            assert len(endpoints) > 0


@pytest.mark.integration
class TestHealthCheckMetrics:
    """Testa métricas dos health checks"""
    
    async def test_health_check_response_times(self):
        """Testa tempos de resposta dos health checks"""
        manager = HealthCheckManager()
        
        results = await manager.run_all_health_checks()
        
        # Todos devem ter tempo de resposta medido
        for name, result in results.items():
            assert result.response_time >= 0
            # Health checks devem ser rápidos (< 5 segundos)
            assert result.response_time < 5.0
    
    async def test_health_check_timestamps(self):
        """Testa timestamps dos health checks"""
        manager = HealthCheckManager()
        
        before = asyncio.get_event_loop().time()
        results = await manager.run_all_health_checks()
        after = asyncio.get_event_loop().time()
        
        # Todos os timestamps devem estar no intervalo
        for name, result in results.items():
            assert before <= result.timestamp <= after
