"""
Testes unitários para Value Objects do domínio Wallet
"""

import pytest
from decimal import Decimal

from src.domain.wallet.value_objects.wallet_address import WalletAddress
from src.domain.wallet.value_objects.private_key import PrivateKey
from src.domain.wallet.value_objects.public_key import PublicKey
from src.domain.wallet.value_objects.balance import Balance
from src.domain.shared.value_objects.money import Money
from src.domain.shared.exceptions import ValidationError


class TestWalletAddress:
    """Testes para WalletAddress"""
    
    def test_wallet_address_creation_from_public_key(self):
        """Testa criação de endereço a partir de chave pública"""
        # Arrange
        public_key = "test_public_key_123"
        
        # Act
        address = WalletAddress.from_public_key(public_key)
        
        # Assert
        assert address.value is not None
        assert len(address.value) > 0
    
    def test_wallet_address_short_representation(self):
        """Testa representação curta do endereço"""
        # Arrange
        address = WalletAddress.from_public_key("test_key")
        
        # Act
        short = address.short()
        
        # Assert
        assert len(short) < len(address.value)
        assert "..." in short
    
    def test_wallet_address_equality(self):
        """Testa igualdade de endereços"""
        # Arrange
        address1 = WalletAddress.from_public_key("test_key")
        address2 = WalletAddress.from_public_key("test_key")
        address3 = WalletAddress.from_public_key("different_key")
        
        # Act & Assert
        assert address1 == address2
        assert address1 != address3
        assert address1 != "not an address"
    
    def test_wallet_address_hash(self):
        """Testa hash do endereço"""
        # Arrange
        address = WalletAddress.from_public_key("test_key")
        
        # Act
        address_hash = hash(address)
        
        # Assert
        assert isinstance(address_hash, int)


class TestPrivateKey:
    """Testes para PrivateKey"""
    
    def test_private_key_generation(self):
        """Testa geração de chave privada"""
        # Act
        private_key = PrivateKey.generate()
        
        # Assert
        assert private_key.value is not None
        assert len(private_key.value) > 0
    
    def test_private_key_reveal(self):
        """Testa revelação da chave privada"""
        # Arrange
        private_key = PrivateKey.generate()
        
        # Act
        revealed = private_key.reveal()
        
        # Assert
        assert revealed == private_key.value
    
    def test_private_key_equality(self):
        """Testa igualdade de chaves privadas"""
        # Arrange
        key1 = PrivateKey.generate()
        key2 = PrivateKey.generate()
        
        # Act & Assert
        assert key1 == key1
        assert key1 != key2


class TestPublicKey:
    """Testes para PublicKey"""
    
    def test_public_key_from_private_key(self):
        """Testa criação de chave pública a partir de chave privada"""
        # Arrange
        private_key_value = "test_private_key"
        
        # Act
        public_key = PublicKey.from_private_key(private_key_value)
        
        # Assert
        assert public_key.value is not None
        assert public_key.value != private_key_value
    
    def test_public_key_equality(self):
        """Testa igualdade de chaves públicas"""
        # Arrange
        key1 = PublicKey.from_private_key("test_key")
        key2 = PublicKey.from_private_key("test_key")
        key3 = PublicKey.from_private_key("different_key")
        
        # Act & Assert
        assert key1 == key2
        assert key1 != key3


class TestBalance:
    """Testes para Balance"""
    
    def test_balance_zero_creation(self):
        """Testa criação de saldo zero"""
        # Act
        balance = Balance.zero()
        
        # Assert
        assert balance.to_cnb() == Decimal("0")
        assert balance.to_satoshi() == 0
        assert balance.is_zero() is True
    
    def test_balance_from_cnb(self):
        """Testa criação de saldo a partir de CNB"""
        # Arrange
        cnb_amount = Decimal("100.5")
        
        # Act
        balance = Balance.from_cnb(cnb_amount)
        
        # Assert
        assert balance.to_cnb() == cnb_amount
        assert balance.to_satoshi() == 10050000000  # 100.5 * 10^8
    
    def test_balance_from_satoshi(self):
        """Testa criação de saldo a partir de satoshi"""
        # Arrange
        satoshi_amount = 100000000  # 1 CNB
        
        # Act
        balance = Balance.from_satoshi(satoshi_amount)
        
        # Assert
        assert balance.to_cnb() == Decimal("1")
        assert balance.to_satoshi() == satoshi_amount
    
    def test_balance_add(self):
        """Testa adição de saldos"""
        # Arrange
        balance1 = Balance.from_cnb(Decimal("50.0"))
        money2 = Money.from_cnb(Decimal("25.5"))
        
        # Act
        result = balance1.add(money2)
        
        # Assert
        assert result.to_cnb() == Decimal("75.5")
    
    def test_balance_subtract(self):
        """Testa subtração de saldos"""
        # Arrange
        balance1 = Balance.from_cnb(Decimal("100.0"))
        money2 = Money.from_cnb(Decimal("25.5"))
        
        # Act
        result = balance1.subtract(money2)
        
        # Assert
        assert result.to_cnb() == Decimal("74.5")
    
    def test_balance_subtract_insufficient_funds(self):
        """Testa subtração com saldo insuficiente"""
        # Arrange
        balance1 = Balance.from_cnb(Decimal("50.0"))
        money2 = Money.from_cnb(Decimal("100.0"))
        
        # Act & Assert
        with pytest.raises(ValueError, match="Resulting amount cannot be negative"):
            balance1.subtract(money2)
    
    def test_balance_is_sufficient_for(self):
        """Testa verificação de saldo suficiente"""
        # Arrange
        balance = Balance.from_cnb(Decimal("100.0"))
        amount1 = Money.from_cnb(50.0)
        amount2 = Money.from_cnb(150.0)
        
        # Act & Assert
        assert balance.is_sufficient_for(amount1) is True
        assert balance.is_sufficient_for(amount2) is False
    
    def test_balance_is_positive(self):
        """Testa verificação de saldo positivo"""
        # Arrange
        positive_balance = Balance.from_cnb(Decimal("100.0"))
        zero_balance = Balance.zero()
        
        # Act & Assert
        assert positive_balance.is_positive() is True
        assert zero_balance.is_positive() is False
    
    def test_balance_equality(self):
        """Testa igualdade de saldos"""
        # Arrange
        balance1 = Balance.from_cnb(Decimal("100.0"))
        balance2 = Balance.from_cnb(Decimal("100.0"))
        balance3 = Balance.from_cnb(Decimal("50.0"))
        
        # Act & Assert
        assert balance1 == balance2
        assert balance1 != balance3
        assert balance1 != "not a balance"
    
    def test_balance_string_representation(self):
        """Testa representação string do saldo"""
        # Arrange
        balance = Balance.from_cnb(Decimal("100.5"))
        
        # Act
        str_repr = str(balance)
        
        # Assert
        assert "100.5" in str_repr
        assert "CNB" in str_repr


class TestMoney:
    """Testes para Money"""
    
    def test_money_from_cnb(self):
        """Testa criação de Money a partir de CNB"""
        # Arrange
        cnb_amount = 100.5
        
        # Act
        money = Money.from_cnb(cnb_amount)
        
        # Assert
        assert money.to_cnb() == Decimal("100.5")
        assert money.to_satoshi() == 10050000000
    
    def test_money_from_satoshi(self):
        """Testa criação de Money a partir de satoshi"""
        # Arrange
        satoshi_amount = 100000000  # 1 CNB
        
        # Act
        money = Money.from_satoshi(satoshi_amount)
        
        # Assert
        assert money.to_cnb() == Decimal("1")
        assert money.to_satoshi() == satoshi_amount
    
    def test_money_is_positive(self):
        """Testa verificação de valor positivo"""
        # Arrange
        positive_money = Money.from_cnb(100.0)
        zero_money = Money.from_cnb(0.0)
        
        # Act & Assert
        assert positive_money.is_positive() is True
        assert zero_money.is_positive() is False
        
        # Teste para valor negativo (deve falhar na criação)
        with pytest.raises(ValueError, match="Money amount cannot be negative"):
            Money.from_cnb(-10.0)
    
    def test_money_add(self):
        """Testa adição de valores Money"""
        # Arrange
        money1 = Money.from_cnb(50.0)
        money2 = Money.from_cnb(25.5)
        
        # Act
        result = money1 + money2
        
        # Assert
        assert result.to_cnb() == Decimal("75.5")
    
    def test_money_subtract(self):
        """Testa subtração de valores Money"""
        # Arrange
        money1 = Money.from_cnb(100.0)
        money2 = Money.from_cnb(25.5)
        
        # Act
        result = money1 - money2
        
        # Assert
        assert result.to_cnb() == Decimal("74.5")
    
    def test_money_multiply(self):
        """Testa multiplicação de valores Money"""
        # Arrange
        money = Money.from_cnb(100.0)
        multiplier = 1.5
        
        # Act
        result = money * multiplier
        
        # Assert
        assert result.to_cnb() == Decimal("150.0")
    
    def test_money_divide(self):
        """Testa divisão de valores Money"""
        # Arrange
        money = Money.from_cnb(100.0)
        divisor = 2.0
        
        # Act
        result = money / divisor
        
        # Assert
        assert result.to_cnb() == Decimal("50.0")
    
    def test_money_equality(self):
        """Testa igualdade de valores Money"""
        # Arrange
        money1 = Money.from_cnb(100.0)
        money2 = Money.from_cnb(100.0)
        money3 = Money.from_cnb(50.0)
        
        # Act & Assert
        assert money1 == money2
        assert money1 != money3
        assert money1 != "not money"
    
    def test_money_comparison(self):
        """Testa comparação de valores Money"""
        # Arrange
        money1 = Money.from_cnb(100.0)
        money2 = Money.from_cnb(50.0)
        money3 = Money.from_cnb(100.0)
        
        # Act & Assert
        assert money1 > money2
        assert money2 < money1
        assert money1 >= money3
        assert money2 <= money1
        assert money1 == money3
