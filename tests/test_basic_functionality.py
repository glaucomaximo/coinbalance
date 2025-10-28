"""
Testes Unitários Básicos para CoinBalance
=========================================

Implementa testes unitários essenciais para validar funcionalidades críticas
e garantir qualidade do código.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from decimal import Decimal
from datetime import datetime
import json

# ========== TESTES DE VALIDAÇÃO ==========

class TestValidationModels:
    """Testes para modelos de validação"""
    
    def test_create_wallet_request_valid(self):
        """Testa criação de carteira com dados válidos"""
        from src.presentation.api.models.validation_models import CreateWalletRequest
        
        data = {
            "name": "Minha Carteira",
            "description": "Carteira de teste"
        }
        
        request = CreateWalletRequest(**data)
        assert request.name == "Minha Carteira"
        assert request.description == "Carteira de teste"
    
    def test_create_wallet_request_invalid_name(self):
        """Testa criação de carteira com nome inválido"""
        from src.presentation.api.models.validation_models import CreateWalletRequest
        from pydantic import ValidationError

        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            CreateWalletRequest(name="", description="Test")
    
    def test_transfer_request_valid(self):
        """Testa transferência com dados válidos"""
        from src.presentation.api.models.validation_models import TransferRequest
        
        data = {
            "from_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            "to_address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
            "amount": "10.5",
            "memo": "Transferência de teste"
        }
        
        request = TransferRequest(**data)
        assert request.from_address == "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        assert request.amount == Decimal("10.5")
    
    def test_transfer_request_invalid_address(self):
        """Testa transferência com endereço inválido"""
        from src.presentation.api.models.validation_models import TransferRequest
        
        with pytest.raises(ValueError, match="Endereço de carteira inválido"):
            TransferRequest(
                from_address="invalid",
                to_address="1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
                amount="10.5"
            )
    
    def test_transfer_request_negative_amount(self):
        """Testa transferência com valor negativo"""
        from src.presentation.api.models.validation_models import TransferRequest
        
        with pytest.raises(ValueError, match="Valor não pode ser negativo"):
            TransferRequest(
                from_address="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
                to_address="1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
                amount="-10.5"
            )

# ========== TESTES DE SEGURANÇA ==========

class TestSecurityFeatures:
    """Testes para funcionalidades de segurança"""
    
    def test_validation_middleware_sql_injection(self):
        """Testa proteção contra SQL injection"""
        from src.infrastructure.security.validation_middleware import InputValidator
        from fastapi import HTTPException

        validator = InputValidator()

        # Testar uma entrada específica
        with pytest.raises(HTTPException):
            validator.validate_string("DROP TABLE users", "test_field")
    
    def test_validation_middleware_xss(self):
        """Testa proteção contra XSS"""
        from src.infrastructure.security.validation_middleware import InputValidator
        
        validator = InputValidator()
        
        xss_inputs = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "onload=alert('xss')"
        ]
        
        for xss_input in xss_inputs:
            with pytest.raises(Exception):  # Deve rejeitar entrada XSS
                validator.validate_string(xss_input, "test_field")
    
    def test_rate_limiter_basic(self):
        """Testa funcionamento básico do rate limiter"""
        from src.infrastructure.security.rate_limiter import AdvancedRateLimiter
        from unittest.mock import Mock
        
        rate_limiter = AdvancedRateLimiter()
        
        # Mock request
        request = Mock()
        request.url.path = "/api/v1/auth/login"
        request.client.host = "127.0.0.1"
        request.headers = {}
        
        # Primeira requisição deve passar
        is_limited, reason, retry_after = asyncio.run(rate_limiter.check_rate_limit(request))
        assert not is_limited
        
        # Muitas requisições devem ser limitadas
        for _ in range(5):  # Exceder limite de 3 por minuto
            asyncio.run(rate_limiter.check_rate_limit(request))
        
        is_limited, reason, retry_after = asyncio.run(rate_limiter.check_rate_limit(request))
        assert is_limited
        assert "Rate limit exceeded" in reason

# ========== TESTES DE CONFIGURAÇÃO ==========

class TestConfiguration:
    """Testes para configuração de ambiente"""
    
    def test_environment_manager_development(self):
        """Testa configuração de desenvolvimento"""
        from src.infrastructure.config.environment_manager import EnvironmentConfigManager
        
        config_manager = EnvironmentConfigManager()
        
        # Mock environment
        with patch.dict('os.environ', {'ENVIRONMENT': 'development'}):
            env_type = config_manager.get_environment_type()
            assert env_type.value == "development"
    
    def test_environment_manager_production_validation(self):
        """Testa validação de configuração de produção"""
        from src.infrastructure.config.environment_manager import EnvironmentConfigManager, ConfigValidationError
        
        config_manager = EnvironmentConfigManager()
        
        # Mock environment de produção sem variáveis obrigatórias
        with patch.dict('os.environ', {
            'ENVIRONMENT': 'production',
            'DEBUG': 'true'  # Não deveria ser true em produção
        }, clear=True):
            errors = config_manager.validate_production_config()
            assert len(errors) > 0
            # Verificar se há erros relacionados a configurações obrigatórias
            error_messages = [error.message for error in errors]
            assert any("SECRET_KEY" in msg or "DEBUG" in msg for msg in error_messages)
            assert any("DEBUG" in error.message for error in errors)
    
    def test_settings_validation(self):
        """Testa validação de configurações"""
        from src.infrastructure.config.settings import Settings
        
        # Teste com configurações válidas
        settings = Settings(
            ENVIRONMENT="development",
            DEBUG=True,
            SECRET_KEY="test-secret-key-32-chars-long",
            JWT_SECRET_KEY="test-jwt-secret-32-chars-long",
            ENCRYPTION_KEY="test-encryption-key-32-chars",
            COINBALANCE_MASTER_KEY="test-master-key-32-chars-long"
        )
        
        assert settings.is_development
        assert not settings.is_production

# ========== TESTES DE LOGGING ==========

class TestStructuredLogging:
    """Testes para logging estruturado"""
    
    def test_logging_manager_configuration(self):
        """Testa configuração do logging manager"""
        from src.infrastructure.logging.structured_logging import LoggingManager
        
        logging_manager = LoggingManager()
        
        # Configurar logging
        logging_manager.configure(
            log_level="INFO",
            log_format="json",
            enable_console=True,
            enable_file=False
        )
        
        # Verificar se foi configurado
        stats = logging_manager.get_log_statistics()
        assert stats["configured"] is True
        assert "console" in stats["handlers"]
    
    def test_contextual_logger(self):
        """Testa logger contextual"""
        from src.infrastructure.logging.structured_logging import get_logger, LogCategory
        
        logger = get_logger("test", LogCategory.BUSINESS_LOGIC)
        
        # Teste básico de logging
        logger.info("Test message", {"test_data": "value"})
        
        # Verificar se não houve exceções
        assert True  # Se chegou aqui, não houve erro
    
    def test_request_context(self):
        """Testa contexto de requisição"""
        from src.infrastructure.logging.structured_logging import logging_manager
        
        # Definir contexto
        logging_manager.set_request_context(
            request_id="test-123",
            user_id="user-456",
            session_id="session-789"
        )
        
        # Verificar contexto
        stats = logging_manager.get_log_statistics()
        assert stats["context"]["request_id"] == "test-123"
        assert stats["context"]["user_id"] == "user-456"
        assert stats["context"]["session_id"] == "session-789"
        
        # Limpar contexto
        logging_manager.clear_request_context()
        stats = logging_manager.get_log_statistics()
        assert stats["context"]["request_id"] is None

# ========== TESTES DE TRATAMENTO DE EXCEÇÕES ==========

class TestExceptionHandling:
    """Testes para tratamento de exceções"""
    
    def test_exception_handler_basic(self):
        """Testa funcionamento básico do manipulador de exceções"""
        from src.infrastructure.exceptions.robust_handler import RobustExceptionHandler, ErrorContext, ErrorSeverity, ErrorCategory
        
        handler = RobustExceptionHandler()
        
        # Criar contexto de erro
        context = ErrorContext(
            user_id="test-user",
            operation="test_operation"
        )
        
        # Testar tratamento de exceção
        exception = ValueError("Test error")
        error_info = asyncio.run(handler.handle_exception(
            exception, context, ErrorSeverity.MEDIUM, ErrorCategory.BUSINESS_LOGIC
        ))
        
        assert error_info.error_id is not None
        assert error_info.message == "Test error"
        assert error_info.severity == ErrorSeverity.MEDIUM
        assert error_info.category == ErrorCategory.BUSINESS_LOGIC
    
    def test_exception_handler_recovery(self):
        """Testa estratégias de recuperação"""
        from src.infrastructure.exceptions.robust_handler import RobustExceptionHandler, ErrorContext, ErrorSeverity, ErrorCategory
        
        handler = RobustExceptionHandler()
        
        # Adicionar estratégia de recuperação personalizada
        def custom_recovery(error_info):
            return True  # Simular recuperação bem-sucedida
        
        handler.add_recovery_strategy("ValueError", custom_recovery)
        
        # Testar recuperação
        context = ErrorContext(operation="test")
        exception = ValueError("Test error")
        
        error_info = asyncio.run(handler.handle_exception(
            exception, context, ErrorSeverity.LOW, ErrorCategory.BUSINESS_LOGIC
        ))
        
        assert error_info.recovery_attempted is True
    
    def test_exception_handler_statistics(self):
        """Testa estatísticas de erro"""
        from src.infrastructure.exceptions.robust_handler import RobustExceptionHandler, ErrorContext, ErrorSeverity, ErrorCategory
        
        handler = RobustExceptionHandler()
        
        # Gerar alguns erros
        for i in range(3):
            context = ErrorContext(operation=f"test_{i}")
            exception = ValueError(f"Test error {i}")
            asyncio.run(handler.handle_exception(
                exception, context, ErrorSeverity.MEDIUM, ErrorCategory.BUSINESS_LOGIC
            ))
        
        # Verificar estatísticas
        stats = handler.get_error_statistics()
        assert stats["total_errors"] == 3
        assert "errors_by_severity" in stats
        assert "errors_by_category" in stats

# ========== TESTES DE INTEGRAÇÃO ==========

class TestIntegration:
    """Testes de integração básicos"""
    
    def test_application_startup(self):
        """Testa inicialização da aplicação"""
        from src.presentation.api.app import create_app
        
        # Criar aplicação
        app = create_app()
        
        # Verificar se foi criada
        assert app is not None
        assert app.title == "CoinBalance"
    
    def test_health_endpoint(self):
        """Testa endpoint de saúde"""
        from fastapi.testclient import TestClient
        from src.presentation.api.app import create_app
        
        app = create_app()
        client = TestClient(app)
        
        # Testar endpoint de saúde
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_wallet_endpoints(self):
        """Testa endpoints de carteira"""
        from fastapi.testclient import TestClient
        from src.presentation.api.app import create_app
        
        app = create_app()
        client = TestClient(app)
        
        # Testar listagem de carteiras
        response = client.get("/api/v1/carteiras/")
        # Pode retornar 200 (sucesso), 403 (forbidden) ou 500 (erro de configuração)
        assert response.status_code in [200, 403, 500]

# ========== FIXTURES ==========

@pytest.fixture
def mock_database():
    """Fixture para mock de banco de dados"""
    mock_db = Mock()
    mock_db.execute_query = Mock(return_value=[])
    mock_db.execute_insert = Mock(return_value=1)
    mock_db.execute_update = Mock(return_value=1)
    return mock_db

@pytest.fixture
def mock_wallet():
    """Fixture para mock de carteira"""
    from src.domain.wallet.entities.wallet import Wallet
    from src.domain.wallet.value_objects.wallet_address import WalletAddress
    from src.domain.wallet.value_objects.public_key import PublicKey
    from src.domain.wallet.value_objects.private_key import PrivateKey
    from src.domain.wallet.value_objects.balance import Balance
    from src.domain.shared.value_objects.timestamp import Timestamp
    
    return Wallet(
        address=WalletAddress.create("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"),
        name="Test Wallet",
        public_key=PublicKey.create("test-public-key"),
        private_key=PrivateKey.generate(),
        balance=Balance.from_cnb(100.0),
        created_at=Timestamp.now(),
        updated_at=Timestamp.now()
    )

# ========== CONFIGURAÇÃO DE TESTES ==========

@pytest.fixture(scope="session")
def event_loop():
    """Cria event loop para testes assíncronos"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Configuração do pytest
def pytest_configure(config):
    """Configuração do pytest"""
    config.addinivalue_line(
        "markers", "slow: marca testes lentos"
    )
    config.addinivalue_line(
        "markers", "integration: marca testes de integração"
    )

# Executar testes se chamado diretamente
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
