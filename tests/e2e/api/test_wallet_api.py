"""
Testes End-to-End para API de Carteiras
"""

import pytest
from httpx import AsyncClient
from fastapi import status
from unittest.mock import patch, AsyncMock


class TestWalletAPI:
    """Testes E2E para endpoints de carteiras"""
    
    def test_create_wallet_success(self, async_client):
        """Testa criação de carteira via API"""
        # Arrange
        wallet_data = {
            "name": "Test Wallet",
            "password": "test12345",
            "metadata": {"test": True}
        }
        
        # Act
        response = async_client.post("/api/v1/carteiras/", json=wallet_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert "address" in data
        assert "name" in data
        assert "public_key" in data
        assert "balance" in data
        assert "created_at" in data
        
        assert data["name"] == "Test Wallet"
        assert data["balance"] == 0.0
        assert data["address"] is not None
        assert data["public_key"] is not None
    
    def test_create_wallet_duplicate_name(self, async_client):
        """Testa criação de carteira com nome duplicado"""
        # Arrange
        wallet_data = {
            "name": "Duplicate Wallet",
            "password": "test12345"
        }
        
        # Criar primeira carteira
        async_client.post("/api/v1/carteiras/", json=wallet_data)
        
        # Act - Tentar criar segunda carteira com mesmo nome
        response = async_client.post("/api/v1/carteiras/", json=wallet_data)
        
        # Assert
        assert response.status_code == status.HTTP_409_CONFLICT
        
        data = response.json()
        assert "detail" in data
        assert "already exists" in data["detail"]["error"]
    
    def test_create_wallet_invalid_data(self, async_client):
        """Testa criação de carteira com dados inválidos"""
        # Arrange
        invalid_data = {
            "name": "",  # Nome vazio
            "password": "test12345"
        }
        
        # Act
        response = async_client.post("/api/v1/carteiras/", json=invalid_data)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        data = response.json()
        assert "error" in data
        assert data["error"] == "Validation error"
    
    def test_create_wallet_missing_required_fields(self, async_client):
        """Testa criação de carteira sem campos obrigatórios"""
        # Arrange
        incomplete_data = {
            "password": "test12345"
            # Nome ausente
        }
        
        # Act
        response = async_client.post("/api/v1/carteiras/", json=incomplete_data)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        data = response.json()
        assert "error" in data
        assert "details" in data
    
    def test_create_wallet_without_password(self, async_client):
        """Testa criação de carteira sem senha"""
        # Arrange
        wallet_data = {
            "name": "No Password Wallet"
        }
        
        # Act
        response = async_client.post("/api/v1/carteiras/", json=wallet_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert data["name"] == "No Password Wallet"
        assert data["address"] is not None
    
    def test_create_wallet_with_metadata(self, async_client):
        """Testa criação de carteira com metadados"""
        # Arrange
        wallet_data = {
            "name": "Metadata Wallet",
            "password": "test12345",
            "metadata": {
                "type": "test",
                "version": "1.0",
                "tags": ["test", "wallet"]
            }
        }
        
        # Act
        response = async_client.post("/api/v1/carteiras/", json=wallet_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert data["name"] == "Metadata Wallet"
        assert data["address"] is not None
    
    def test_get_wallet_by_address(self, async_client):
        """Testa busca de carteira por endereço"""
        # Arrange - Criar carteira primeiro
        wallet_data = {
            "name": "Search Test Wallet",
            "password": "test12345"
        }
        
        create_response = async_client.post("/api/v1/carteiras/", json=wallet_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        
        created_wallet = create_response.json()
        wallet_address = created_wallet["address"]
        
        # Act
        response = async_client.get(f"/api/v1/carteiras/{wallet_address}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["address"] == wallet_address
        assert data["name"] == "Search Test Wallet"
        assert data["balance_cnb"] == 0.0
    
    def test_get_wallet_not_found(self, async_client):
        """Testa busca de carteira inexistente"""
        # Arrange
        non_existent_address = "non_existent_address_123"
        
        # Act
        response = async_client.get(f"/api/v1/carteiras/{non_existent_address}")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
    
    def test_list_wallets(self, async_client):
        """Testa listagem de carteiras"""
        # Arrange - Criar algumas carteiras
        wallets_data = [
            {"name": "Wallet 1", "password": "test12345"},
            {"name": "Wallet 2", "password": "test12345"},
            {"name": "Wallet 3", "password": "test12345"}
        ]
        
        for wallet_data in wallets_data:
            response = async_client.post("/api/v1/carteiras/", json=wallet_data)
            assert response.status_code == status.HTTP_201_CREATED
        
        # Act
        response = async_client.get("/api/v1/carteiras")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "wallets" in data
        assert "total" in data
        assert data["total"] >= 3
        
        # Verificar se as carteiras criadas estão na lista
        wallet_names = [wallet["name"] for wallet in data["wallets"]]
        assert "Wallet 1" in wallet_names
        assert "Wallet 2" in wallet_names
        assert "Wallet 3" in wallet_names
    
    def test_wallet_credit_operation(self, async_client):
        """Testa operação de crédito na carteira"""
        # Arrange - Criar carteira
        wallet_data = {
            "name": "Credit Test Wallet",
            "password": "test12345"
        }
        
        create_response = async_client.post("/api/v1/carteiras/", json=wallet_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        
        created_wallet = create_response.json()
        wallet_address = created_wallet["address"]
        
        # Act - Creditar valor
        credit_data = {
            "amount": 100.0,
            "reason": "Test credit"
        }
        
        response = async_client.post(
            f"/api/v1/carteiras/{wallet_address}/credit",
            json=credit_data
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["balance_cnb"] == 100.0
        assert data["address"] == wallet_address
    
    def test_wallet_debit_operation(self, async_client):
        """Testa operação de débito na carteira"""
        # Arrange - Criar carteira e creditar valor
        wallet_data = {
            "name": "Debit Test Wallet",
            "password": "test12345"
        }
        
        create_response = async_client.post("/api/v1/carteiras/", json=wallet_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        
        created_wallet = create_response.json()
        wallet_address = created_wallet["address"]
        
        # Creditar valor primeiro
        credit_data = {"amount": 100.0, "reason": "Initial credit"}
        async_client.post(f"/api/v1/carteiras/{wallet_address}/credit", json=credit_data)
        
        # Act - Debitar valor
        debit_data = {
            "amount": 50.0,
            "reason": "Test debit"
        }
        
        response = async_client.post(
            f"/api/v1/carteiras/{wallet_address}/debit",
            json=debit_data
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["balance_cnb"] == 50.0
        assert data["address"] == wallet_address
    
    def test_wallet_debit_insufficient_funds(self, async_client):
        """Testa débito com saldo insuficiente"""
        # Arrange - Criar carteira sem crédito
        wallet_data = {
            "name": "Insufficient Funds Wallet",
            "password": "test12345"
        }
        
        create_response = async_client.post("/api/v1/carteiras/", json=wallet_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        
        created_wallet = create_response.json()
        wallet_address = created_wallet["address"]
        
        # Act - Tentar debitar valor maior que o saldo
        debit_data = {
            "amount": 100.0,
            "reason": "Test debit"
        }
        
        response = async_client.post(
            f"/api/v1/carteiras/{wallet_address}/debit",
            json=debit_data
        )
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert "detail" in data
        assert "Insufficient" in data["detail"]["error"]
    
    def test_wallet_invalid_operations(self, async_client):
        """Testa operações inválidas na carteira"""
        # Arrange - Criar carteira
        wallet_data = {
            "name": "Invalid Operations Wallet",
            "password": "test12345"
        }
        
        create_response = async_client.post("/api/v1/carteiras/", json=wallet_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        
        created_wallet = create_response.json()
        wallet_address = created_wallet["address"]
        
        # Act & Assert - Tentar creditar valor negativo
        credit_data = {"amount": -10.0, "reason": "Invalid credit"}
        response = async_client.post(
            f"/api/v1/carteiras/{wallet_address}/credit",
            json=credit_data
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        
        # Act & Assert - Tentar debitar valor negativo
        debit_data = {"amount": -10.0, "reason": "Invalid debit"}
        response = async_client.post(
            f"/api/v1/carteiras/{wallet_address}/debit",
            json=debit_data
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    
    def test_api_error_handling(self, async_client):
        """Testa tratamento de erros da API"""
        # Arrange
        invalid_endpoint = "/api/v1/carteiras/invalid_endpoint"
        
        # Act
        response = async_client.get(invalid_endpoint)
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_api_response_format(self, async_client):
        """Testa formato das respostas da API"""
        # Arrange
        wallet_data = {
            "name": "Format Test Wallet",
            "password": "test12345"
        }
        
        # Act
        response = async_client.post("/api/v1/carteiras/", json=wallet_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        
        # Verificar estrutura da resposta
        required_fields = ["address", "name", "public_key", "balance", "created_at"]
        for field in required_fields:
            assert field in data
        
        # Verificar tipos dos campos
        assert isinstance(data["address"], str)
        assert isinstance(data["name"], str)
        assert isinstance(data["public_key"], str)
        assert isinstance(data["balance"], (int, float))
        assert isinstance(data["created_at"], (int, float))
