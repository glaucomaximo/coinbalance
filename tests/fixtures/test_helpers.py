"""
Fixtures e Helpers para Testes
"""

import pytest
import asyncio
from typing import Dict, Any, List
from unittest.mock import Mock, AsyncMock
from dataclasses import dataclass

from src.domain.wallet.entities.wallet import Wallet
from src.domain.wallet.value_objects.balance import Balance
from src.domain.shared.value_objects.money import Money


@dataclass
class WalletTestData:
    """Dados de teste para carteira"""
    name: str
    password: str = "test123"
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {"test": True}


class WalletTestBuilder:
    """Builder para criar carteiras de teste"""
    
    def __init__(self):
        self._name = "Test Wallet"
        self._password = "test123"
        self._metadata = {"test": True}
    
    def with_name(self, name: str) -> 'WalletTestBuilder':
        """Define nome da carteira"""
        self._name = name
        return self
    
    def with_password(self, password: str) -> 'WalletTestBuilder':
        """Define senha da carteira"""
        self._password = password
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> 'WalletTestBuilder':
        """Define metadados da carteira"""
        self._metadata = metadata
        return self
    
    def with_balance(self, amount: float) -> 'WalletTestBuilder':
        """Define saldo inicial da carteira"""
        self._initial_balance = amount
        return self
    
    def build(self) -> Wallet:
        """Constrói a carteira"""
        wallet = Wallet.create(
            name=self._name,
            password=self._password,
            metadata=self._metadata
        )
        
        # Aplicar saldo inicial se especificado
        if hasattr(self, '_initial_balance'):
            wallet.credit(Money.from_cnb(self._initial_balance), "Initial balance")
        
        return wallet
    
    def build_data(self) -> Dict[str, Any]:
        """Constrói dados para API"""
        return {
            "name": self._name,
            "password": self._password,
            "metadata": self._metadata
        }


class TestDataFactory:
    """Factory para criar dados de teste"""
    
    @staticmethod
    def create_wallet_data(name: str = None, **kwargs) -> Dict[str, Any]:
        """Cria dados de carteira para API"""
        if name is None:
            name = f"Test Wallet {pytest.current_test_id()}"
        
        return {
            "name": name,
            "password": kwargs.get("password", "test123"),
            "metadata": kwargs.get("metadata", {"test": True})
        }
    
    @staticmethod
    def create_credit_data(amount: float, reason: str = "Test credit") -> Dict[str, Any]:
        """Cria dados de crédito"""
        return {
            "amount": amount,
            "reason": reason
        }
    
    @staticmethod
    def create_debit_data(amount: float, reason: str = "Test debit") -> Dict[str, Any]:
        """Cria dados de débito"""
        return {
            "amount": amount,
            "reason": reason
        }
    
    @staticmethod
    def create_multiple_wallets(count: int) -> List[Dict[str, Any]]:
        """Cria múltiplas carteiras"""
        return [
            TestDataFactory.create_wallet_data(f"Wallet {i}")
            for i in range(count)
        ]


class MockRepositoryFactory:
    """Factory para criar mocks de repositórios"""
    
    @staticmethod
    def create_wallet_repository_mock():
        """Cria mock do repositório de carteiras"""
        mock = Mock()
        mock.find_by_address = AsyncMock(return_value=None)
        mock.find_by_name = AsyncMock(return_value=None)
        mock.save = AsyncMock(return_value=None)
        mock.delete = AsyncMock(return_value=None)
        mock.find_all = AsyncMock(return_value=[])
        return mock
    
    @staticmethod
    def create_event_dispatcher_mock():
        """Cria mock do dispatcher de eventos"""
        mock = Mock()
        mock.dispatch = AsyncMock(return_value=None)
        return mock


class PerformanceTestHelper:
    """Helper para testes de performance"""
    
    @staticmethod
    async def measure_time(async_func, *args, **kwargs):
        """Mede tempo de execução de função assíncrona"""
        start_time = asyncio.get_event_loop().time()
        result = await async_func(*args, **kwargs)
        end_time = asyncio.get_event_loop().time()
        
        return {
            "result": result,
            "execution_time": end_time - start_time
        }
    
    @staticmethod
    async def run_concurrent_tasks(tasks: List[callable], max_concurrent: int = 10):
        """Executa tarefas concorrentemente"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def run_with_semaphore(task):
            async with semaphore:
                return await task
        
        return await asyncio.gather(*[run_with_semaphore(task) for task in tasks])
    
    @staticmethod
    def calculate_performance_metrics(times: List[float]) -> Dict[str, float]:
        """Calcula métricas de performance"""
        import statistics
        
        return {
            "min": min(times),
            "max": max(times),
            "mean": statistics.mean(times),
            "median": statistics.median(times),
            "stdev": statistics.stdev(times) if len(times) > 1 else 0,
            "count": len(times)
        }


class AssertionHelper:
    """Helper para asserções de teste"""
    
    @staticmethod
    def assert_wallet_response(response_data: Dict[str, Any], expected_name: str = None):
        """Verifica estrutura de resposta de carteira"""
        required_fields = ["address", "name", "public_key", "balance", "created_at"]
        
        for field in required_fields:
            assert field in response_data, f"Missing field: {field}"
        
        if expected_name:
            assert response_data["name"] == expected_name
        
        assert isinstance(response_data["address"], str)
        assert isinstance(response_data["name"], str)
        assert isinstance(response_data["public_key"], str)
        assert isinstance(response_data["balance"], (int, float))
        assert isinstance(response_data["created_at"], (int, float))
    
    @staticmethod
    def assert_error_response(response_data: Dict[str, Any], expected_status: int = None):
        """Verifica estrutura de resposta de erro"""
        assert "error" in response_data, "Missing error field"
        assert isinstance(response_data["error"], str)
        
        if expected_status:
            assert response_data.get("status_code") == expected_status
    
    @staticmethod
    def assert_performance_acceptable(metrics: Dict[str, float], max_mean: float, max_max: float):
        """Verifica se performance está aceitável"""
        assert metrics["mean"] < max_mean, f"Mean time {metrics['mean']:.3f}s exceeds {max_mean}s"
        assert metrics["max"] < max_max, f"Max time {metrics['max']:.3f}s exceeds {max_max}s"


# Fixtures do pytest
@pytest.fixture
def wallet_builder():
    """Fixture para builder de carteiras"""
    return WalletTestBuilder()


@pytest.fixture
def test_data_factory():
    """Fixture para factory de dados de teste"""
    return TestDataFactory()


@pytest.fixture
def mock_repository_factory():
    """Fixture para factory de mocks de repositório"""
    return MockRepositoryFactory()


@pytest.fixture
def performance_helper():
    """Fixture para helper de performance"""
    return PerformanceTestHelper()


@pytest.fixture
def assertion_helper():
    """Fixture para helper de asserções"""
    return AssertionHelper()


@pytest.fixture
def sample_wallet_data():
    """Fixture para dados de carteira de exemplo"""
    return TestDataFactory.create_wallet_data("Sample Wallet")


@pytest.fixture
def sample_wallet_entity():
    """Fixture para entidade de carteira de exemplo"""
    return WalletTestBuilder().with_name("Sample Wallet").build()


@pytest.fixture
def wallet_with_balance():
    """Fixture para carteira com saldo"""
    return WalletTestBuilder().with_name("Wallet with Balance").with_balance(1000.0).build()


@pytest.fixture
def multiple_wallet_data():
    """Fixture para múltiplas carteiras"""
    return TestDataFactory.create_multiple_wallets(5)


@pytest.fixture
def mock_wallet_repository():
    """Fixture para mock do repositório de carteiras"""
    return MockRepositoryFactory.create_wallet_repository_mock()


@pytest.fixture
def mock_event_dispatcher():
    """Fixture para mock do dispatcher de eventos"""
    return MockRepositoryFactory.create_event_dispatcher_mock()


# Fixtures para testes de performance
@pytest.fixture
def performance_test_data():
    """Fixture para dados de teste de performance"""
    return {
        "num_wallets": 100,
        "num_operations": 1000,
        "max_response_time": 1.0,
        "max_concurrent": 50
    }


@pytest.fixture
def load_test_scenarios():
    """Fixture para cenários de teste de carga"""
    return [
        {"users": 10, "requests_per_user": 10},
        {"users": 50, "requests_per_user": 20},
        {"users": 100, "requests_per_user": 50}
    ]
