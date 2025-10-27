"""
Testes de integração para Application Layer - Command Handlers
"""

import pytest
from unittest.mock import Mock, AsyncMock
from dataclasses import dataclass

from src.application.wallet.commands.create_wallet import (
    CreateWalletCommand,
    CreateWalletCommandHandler,
    CreateWalletResult
)
from src.domain.wallet.entities.wallet import Wallet
from src.domain.wallet.repositories.wallet_repository import WalletRepository
from src.domain.shared.exceptions import DuplicateEntityError


class TestCreateWalletCommandHandler:
    """Testes para o handler de criação de carteira"""
    
    @pytest.fixture
    def mock_wallet_repository(self):
        """Mock do repositório de carteiras"""
        mock = Mock(spec=WalletRepository)
        mock.find_by_name = AsyncMock(return_value=None)
        mock.save = AsyncMock(return_value=None)
        return mock
    
    @pytest.fixture
    def mock_event_dispatcher(self):
        """Mock do dispatcher de eventos"""
        mock = Mock()
        mock.dispatch = AsyncMock(return_value=None)
        return mock
    
    @pytest.fixture
    def command_handler(self, mock_wallet_repository, mock_event_dispatcher):
        """Handler de comando com mocks"""
        handler = CreateWalletCommandHandler(mock_wallet_repository)
        handler.event_dispatcher = mock_event_dispatcher
        return handler
    
    @pytest.mark.asyncio
    async def test_create_wallet_success(self, command_handler, mock_wallet_repository, mock_event_dispatcher):
        """Testa criação de carteira com sucesso"""
        # Arrange
        command = CreateWalletCommand(
            name="Test Wallet",
            password="test123",
            metadata={"test": True}
        )
        
        # Act
        result = await command_handler.execute(command)
        
        # Assert
        assert isinstance(result, CreateWalletResult)
        assert result.name == "Test Wallet"
        assert result.address is not None
        assert result.public_key is not None
        assert result.balance == 0.0
        assert result.created_at is not None
        
        # Verificar chamadas
        mock_wallet_repository.find_by_name.assert_called_once_with("Test Wallet")
        mock_wallet_repository.save.assert_called_once()
        mock_event_dispatcher.dispatch.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_wallet_duplicate_name(self, command_handler, mock_wallet_repository):
        """Testa criação de carteira com nome duplicado"""
        # Arrange
        existing_wallet = Wallet.create("Test Wallet")
        mock_wallet_repository.find_by_name.return_value = existing_wallet
        
        command = CreateWalletCommand(name="Test Wallet")
        
        # Act & Assert
        with pytest.raises(DuplicateEntityError, match="Wallet with name 'Test Wallet' already exists"):
            await command_handler.execute(command)
        
        # Verificar que save não foi chamado
        mock_wallet_repository.save.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_create_wallet_without_password(self, command_handler, mock_wallet_repository, mock_event_dispatcher):
        """Testa criação de carteira sem senha"""
        # Arrange
        command = CreateWalletCommand(name="Test Wallet")
        
        # Act
        result = await command_handler.execute(command)
        
        # Assert
        assert result.name == "Test Wallet"
        assert result.address is not None
        assert result.public_key is not None
        assert result.balance == 0.0
        
        # Verificar chamadas
        mock_wallet_repository.find_by_name.assert_called_once_with("Test Wallet")
        mock_wallet_repository.save.assert_called_once()
        mock_event_dispatcher.dispatch.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_wallet_with_metadata(self, command_handler, mock_wallet_repository, mock_event_dispatcher):
        """Testa criação de carteira com metadados"""
        # Arrange
        metadata = {"type": "test", "version": "1.0"}
        command = CreateWalletCommand(
            name="Test Wallet",
            metadata=metadata
        )
        
        # Act
        result = await command_handler.execute(command)
        
        # Assert
        assert result.name == "Test Wallet"
        assert result.address is not None
        
        # Verificar que a carteira foi salva com metadados
        saved_wallet = mock_wallet_repository.save.call_args[0][0]
        assert saved_wallet.metadata == metadata
    
    @pytest.mark.asyncio
    async def test_create_wallet_repository_error(self, command_handler, mock_wallet_repository):
        """Testa erro no repositório durante criação"""
        # Arrange
        mock_wallet_repository.save.side_effect = Exception("Database error")
        command = CreateWalletCommand(name="Test Wallet")
        
        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await command_handler.execute(command)
    
    @pytest.mark.asyncio
    async def test_create_wallet_event_dispatcher_error(self, command_handler, mock_wallet_repository, mock_event_dispatcher):
        """Testa erro no dispatcher de eventos"""
        # Arrange
        mock_event_dispatcher.dispatch.side_effect = Exception("Event dispatch error")
        command = CreateWalletCommand(name="Test Wallet")
        
        # Act & Assert
        with pytest.raises(Exception, match="Event dispatch error"):
            await command_handler.execute(command)
    
    @pytest.mark.asyncio
    async def test_create_wallet_events_cleared_after_dispatch(self, command_handler, mock_wallet_repository, mock_event_dispatcher):
        """Testa se eventos são limpos após dispatch"""
        # Arrange
        command = CreateWalletCommand(name="Test Wallet")
        
        # Act
        await command_handler.execute(command)
        
        # Assert
        # Verificar que save foi chamado com uma carteira que tem eventos limpos
        saved_wallet = mock_wallet_repository.save.call_args[0][0]
        assert len(saved_wallet.get_events()) == 0  # Eventos devem estar limpos após dispatch
    
    @pytest.mark.asyncio
    async def test_create_wallet_multiple_events_dispatched(self, command_handler, mock_wallet_repository, mock_event_dispatcher):
        """Testa se múltiplos eventos são despachados"""
        # Arrange
        command = CreateWalletCommand(name="Test Wallet")
        
        # Act
        await command_handler.execute(command)
        
        # Assert
        # Deve ter despachado pelo menos o evento WalletCreated
        assert mock_event_dispatcher.dispatch.call_count >= 1
        
        # Verificar se o evento despachado é do tipo correto
        dispatched_event = mock_event_dispatcher.dispatch.call_args[0][0]
        assert dispatched_event.__class__.__name__ == "WalletCreated"
