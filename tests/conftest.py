"""
Configuração global do pytest para CoinBalance
"""

import pytest
import pytest_asyncio
import asyncio
import os
import sys
from pathlib import Path
from typing import Generator, AsyncGenerator
from unittest.mock import Mock

# Adicionar src ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Configurações de ambiente para testes
os.environ["TESTING"] = "true"
os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DEBUG"] = "true"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Cria event loop para toda a sessão de testes"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def async_client():
    """Cliente HTTP para testes de API"""
    from fastapi.testclient import TestClient
    from src.presentation.api.app import app
    
    # Limpar banco de dados antes do teste
    from src.infrastructure.persistence.database_manager import DatabaseManager
    db_manager = DatabaseManager()
    
    # Limpar tabelas
    db_manager.execute_update("DELETE FROM wallets")
    db_manager.execute_update("DELETE FROM transactions")
    db_manager.execute_update("DELETE FROM blocks")
    
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_wallet_repository():
    """Mock do repositório de carteiras"""
    mock = Mock()
    mock.find_by_address.return_value = None
    mock.find_by_name.return_value = None
    mock.save.return_value = None
    mock.delete.return_value = None
    return mock


@pytest.fixture
def mock_event_dispatcher():
    """Mock do dispatcher de eventos"""
    mock = Mock()
    mock.dispatch.return_value = None
    return mock


@pytest.fixture
def sample_wallet_data():
    """Dados de exemplo para carteira"""
    return {
        "name": "Test Wallet",
        "password": "test123",
        "metadata": {"test": True}
    }


@pytest.fixture
def sample_wallet_entity():
    """Entidade de carteira de exemplo"""
    from src.domain.wallet.entities.wallet import Wallet
    
    return Wallet.create(
        name="Test Wallet",
        password="test123",
        metadata={"test": True}
    )


# Configurações do pytest
def pytest_configure(config):
    """Configurações do pytest"""
    config.addinivalue_line(
        "markers", "unit: marca testes unitários"
    )
    config.addinivalue_line(
        "markers", "integration: marca testes de integração"
    )
    config.addinivalue_line(
        "markers", "e2e: marca testes end-to-end"
    )
    config.addinivalue_line(
        "markers", "performance: marca testes de performance"
    )
    config.addinivalue_line(
        "markers", "slow: marca testes lentos"
    )


def pytest_collection_modifyitems(config, items):
    """Modifica itens de teste durante coleta"""
    for item in items:
        # Marcar testes por localização
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
        
        # Marcar testes lentos
        if "slow" in item.name or "stress" in item.name:
            item.add_marker(pytest.mark.slow)
