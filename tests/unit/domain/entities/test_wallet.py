"""
Testes unitários para a entidade Wallet
"""

import pytest
from decimal import Decimal
from unittest.mock import Mock

from src.domain.wallet.entities.wallet import Wallet
from src.domain.wallet.value_objects.wallet_address import WalletAddress
from src.domain.wallet.value_objects.private_key import PrivateKey
from src.domain.wallet.value_objects.public_key import PublicKey
from src.domain.wallet.value_objects.balance import Balance
from src.domain.shared.value_objects.money import Money
from src.domain.shared.exceptions import InsufficientFundsError, ValidationError
from src.domain.shared.value_objects.timestamp import Timestamp


class TestWallet:
    """Testes para a entidade Wallet"""
    
    def test_wallet_creation(self):
        """Testa criação de carteira"""
        # Arrange
        name = "Test Wallet"
        password = "test123"
        
        # Act
        wallet = Wallet.create(name=name, password=password)
        
        # Assert
        assert wallet.name == name
        assert wallet.address is not None
        assert wallet.public_key is not None
        assert wallet.private_key is not None
        assert wallet.balance.is_zero()
        assert wallet.is_active is True
        assert wallet.created_at is not None
        assert wallet.updated_at is not None
    
    def test_wallet_creation_without_password(self):
        """Testa criação de carteira sem senha"""
        # Arrange
        name = "Test Wallet"
        
        # Act
        wallet = Wallet.create(name=name)
        
        # Assert
        assert wallet.name == name
        assert wallet.is_active is True
    
    def test_wallet_creation_with_metadata(self):
        """Testa criação de carteira com metadados"""
        # Arrange
        name = "Test Wallet"
        metadata = {"type": "test", "version": "1.0"}
        
        # Act
        wallet = Wallet.create(name=name, metadata=metadata)
        
        # Assert
        assert wallet.metadata == metadata
    
    def test_wallet_creation_invalid_name_empty(self):
        """Testa criação com nome vazio"""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError, match="Wallet name cannot be empty"):
            Wallet.create(name="")
    
    def test_wallet_creation_invalid_name_too_long(self):
        """Testa criação com nome muito longo"""
        # Arrange
        long_name = "a" * 101
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Wallet name too long"):
            Wallet.create(name=long_name)
    
    def test_wallet_credit_positive_amount(self):
        """Testa crédito com valor positivo"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        amount = Money.from_cnb(100.0)
        
        # Act
        wallet.credit(amount, "Test credit")
        
        # Assert
        assert wallet.balance.to_cnb() == Decimal("100.0")
        assert len(wallet.get_events()) == 2  # WalletCreated + BalanceUpdated
    
    def test_wallet_credit_zero_amount(self):
        """Testa crédito com valor zero"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        amount = Money.from_cnb(0.0)
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Credit amount must be positive"):
            wallet.credit(amount)
    
    def test_wallet_credit_negative_amount(self):
        """Testa crédito com valor negativo"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        
        # Act & Assert
        with pytest.raises(ValueError, match="Money amount cannot be negative"):
            Money.from_cnb(-10.0)
    
    def test_wallet_debit_sufficient_balance(self):
        """Testa débito com saldo suficiente"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        wallet.credit(Money.from_cnb(100.0), "Initial credit")
        debit_amount = Money.from_cnb(50.0)
        
        # Act
        wallet.debit(debit_amount, "Test debit")
        
        # Assert
        assert wallet.balance.to_cnb() == Decimal("50.0")
    
    def test_wallet_debit_insufficient_balance(self):
        """Testa débito com saldo insuficiente"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        wallet.credit(Money.from_cnb(50.0), "Initial credit")
        debit_amount = Money.from_cnb(100.0)
        
        # Act & Assert
        with pytest.raises(InsufficientFundsError):
            wallet.debit(debit_amount, "Test debit")
    
    def test_wallet_debit_zero_amount(self):
        """Testa débito com valor zero"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        amount = Money.from_cnb(0.0)
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Debit amount must be positive"):
            wallet.debit(amount)
    
    def test_wallet_has_sufficient_balance_true(self):
        """Testa verificação de saldo suficiente - verdadeiro"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        wallet.credit(Money.from_cnb(100.0), "Initial credit")
        amount = Money.from_cnb(50.0)
        
        # Act
        result = wallet.has_sufficient_balance(amount)
        
        # Assert
        assert result is True
    
    def test_wallet_has_sufficient_balance_false(self):
        """Testa verificação de saldo suficiente - falso"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        wallet.credit(Money.from_cnb(50.0), "Initial credit")
        amount = Money.from_cnb(100.0)
        
        # Act
        result = wallet.has_sufficient_balance(amount)
        
        # Assert
        assert result is False
    
    def test_wallet_activate(self):
        """Testa ativação de carteira"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        wallet.is_active = False
        
        # Act
        wallet.activate()
        
        # Assert
        assert wallet.is_active is True
    
    def test_wallet_deactivate_with_zero_balance(self):
        """Testa desativação de carteira com saldo zero"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        
        # Act
        wallet.deactivate()
        
        # Assert
        assert wallet.is_active is False
    
    def test_wallet_deactivate_with_non_zero_balance(self):
        """Testa desativação de carteira com saldo não zero"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        wallet.credit(Money.from_cnb(100.0), "Initial credit")
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Cannot deactivate wallet with non-zero balance"):
            wallet.deactivate()
    
    def test_wallet_update_metadata(self):
        """Testa atualização de metadados"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        key = "test_key"
        value = "test_value"
        
        # Act
        wallet.update_metadata(key, value)
        
        # Assert
        assert wallet.metadata[key] == value
    
    def test_wallet_domain_events(self):
        """Testa eventos de domínio"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        
        # Act
        events = wallet.get_events()
        
        # Assert
        assert len(events) == 1
        assert events[0].__class__.__name__ == "WalletCreated"
        
        # Testar limpeza de eventos
        wallet.clear_events()
        assert len(wallet.get_events()) == 0
    
    def test_wallet_equality(self):
        """Testa igualdade de carteiras"""
        # Arrange
        wallet1 = Wallet.create("Test Wallet 1")
        wallet2 = Wallet.create("Test Wallet 2")
        
        # Act & Assert
        assert wallet1 == wallet1
        assert wallet1 != wallet2
        assert wallet1 != "not a wallet"
    
    def test_wallet_hash(self):
        """Testa hash de carteira"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        
        # Act
        wallet_hash = hash(wallet)
        
        # Assert
        assert isinstance(wallet_hash, int)
        assert wallet_hash == hash(wallet.address)
    
    def test_wallet_string_representation(self):
        """Testa representação string da carteira"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        
        # Act
        str_repr = str(wallet)
        
        # Assert
        assert "Test Wallet" in str_repr
        assert "Wallet(" in str_repr
    
    def test_wallet_to_dict_without_private_key(self):
        """Testa serialização sem chave privada"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        
        # Act
        data = wallet.to_dict(include_private_key=False)
        
        # Assert
        assert "address" in data
        assert "name" in data
        assert "public_key" in data
        assert "balance" in data
        assert "private_key" not in data
    
    def test_wallet_to_dict_with_private_key(self):
        """Testa serialização com chave privada"""
        # Arrange
        wallet = Wallet.create("Test Wallet")
        
        # Act
        data = wallet.to_dict(include_private_key=True)
        
        # Assert
        assert "private_key" in data
        assert data["private_key"] is not None
