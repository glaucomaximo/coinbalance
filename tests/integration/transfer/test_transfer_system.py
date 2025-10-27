"""
Testes para Sistema de Transferências entre Carteiras
"""
import pytest
from decimal import Decimal
from fastapi.testclient import TestClient
from src.presentation.api.app import app
from src.infrastructure.persistence.database_manager import DatabaseManager

class TestTransferSystem:
    """Testes para o sistema de transferências"""
    
    @pytest.fixture(autouse=True)
    def setup_and_cleanup(self):
        """Setup e cleanup para cada teste"""
        # Limpar banco antes de cada teste
        db_manager = DatabaseManager()
        db_manager.execute_update('DELETE FROM wallets')
        yield
        # Cleanup após cada teste
        db_manager.execute_update('DELETE FROM wallets')
    
    def test_successful_transfer(self):
        """Testa transferência bem-sucedida entre carteiras"""
        client = TestClient(app)
        
        # Criar duas carteiras
        wallet1_data = {'name': 'Sender Wallet', 'password': 'test12345'}
        response1 = client.post('/api/v1/carteiras/', json=wallet1_data)
        assert response1.status_code == 201
        wallet1 = response1.json()
        
        wallet2_data = {'name': 'Receiver Wallet', 'password': 'test12345'}
        response2 = client.post('/api/v1/carteiras/', json=wallet2_data)
        assert response2.status_code == 201
        wallet2 = response2.json()
        
        # Creditar carteira de origem
        credit_data = {'amount': 100.0, 'reason': 'Initial credit'}
        response = client.post(f'/api/v1/carteiras/{wallet1["address"]}/credit', json=credit_data)
        assert response.status_code == 200
        
        # Fazer transferência
        transfer_data = {
            'from_address': wallet1['address'],
            'to_address': wallet2['address'],
            'amount': 50.0,
            'reason': 'Test transfer'
        }
        response = client.post('/api/v1/transferencias/', json=transfer_data)
        
        # Verificar resposta
        assert response.status_code == 201
        transfer = response.json()
        
        assert transfer['success'] is True
        assert transfer['from_address'] == wallet1['address']
        assert transfer['to_address'] == wallet2['address']
        assert transfer['amount'] == 50.0
        assert transfer['fee'] == 0.05  # Taxa mínima
        assert transfer['total_amount'] == 50.05
        assert transfer['reason'] == 'Test transfer'
        assert transfer['status'] == 'completed'
        assert 'transaction_id' in transfer
        assert 'created_at' in transfer
        
        # Verificar saldos das carteiras
        response1 = client.get(f'/api/v1/carteiras/{wallet1["address"]}')
        assert response1.status_code == 200
        wallet1_updated = response1.json()
        assert wallet1_updated['balance_cnb'] == 49.95  # 100 - 50.05
        
        response2 = client.get(f'/api/v1/carteiras/{wallet2["address"]}')
        assert response2.status_code == 200
        wallet2_updated = response2.json()
        assert wallet2_updated['balance_cnb'] == 50.0
    
    def test_transfer_insufficient_funds(self):
        """Testa transferência com saldo insuficiente"""
        client = TestClient(app)
        
        # Criar duas carteiras
        wallet1_data = {'name': 'Poor Wallet', 'password': 'test12345'}
        response1 = client.post('/api/v1/carteiras/', json=wallet1_data)
        assert response1.status_code == 201
        wallet1 = response1.json()
        
        wallet2_data = {'name': 'Rich Wallet', 'password': 'test12345'}
        response2 = client.post('/api/v1/carteiras/', json=wallet2_data)
        assert response2.status_code == 201
        wallet2 = response2.json()
        
        # Tentar transferência sem crédito
        transfer_data = {
            'from_address': wallet1['address'],
            'to_address': wallet2['address'],
            'amount': 50.0,
            'reason': 'Test transfer'
        }
        response = client.post('/api/v1/transferencias/', json=transfer_data)
        
        # Verificar erro
        assert response.status_code == 400
        error = response.json()
        assert 'INSUFFICIENT_BALANCE' in error['code']
    
    def test_transfer_same_wallet(self):
        """Testa transferência para a mesma carteira"""
        client = TestClient(app)
        
        # Criar carteira
        wallet_data = {'name': 'Test Wallet', 'password': 'test12345'}
        response = client.post('/api/v1/carteiras/', json=wallet_data)
        assert response.status_code == 201
        wallet = response.json()
        
        # Creditar carteira
        credit_data = {'amount': 100.0, 'reason': 'Initial credit'}
        response = client.post(f'/api/v1/carteiras/{wallet["address"]}/credit', json=credit_data)
        assert response.status_code == 200
        
        # Tentar transferência para a mesma carteira
        transfer_data = {
            'from_address': wallet['address'],
            'to_address': wallet['address'],
            'amount': 50.0,
            'reason': 'Test transfer'
        }
        response = client.post('/api/v1/transferencias/', json=transfer_data)
        
        # Verificar erro
        assert response.status_code == 400
        error = response.json()
        assert 'SAME_WALLET_TRANSFER' in error['code']
    
    def test_transfer_invalid_addresses(self):
        """Testa transferência com endereços inválidos"""
        client = TestClient(app)
        
        # Criar carteira
        wallet_data = {'name': 'Test Wallet', 'password': 'test12345'}
        response = client.post('/api/v1/carteiras/', json=wallet_data)
        assert response.status_code == 201
        wallet = response.json()
        
        # Tentar transferência com endereço inexistente
        transfer_data = {
            'from_address': wallet['address'],
            'to_address': 'invalid_address',
            'amount': 50.0,
            'reason': 'Test transfer'
        }
        response = client.post('/api/v1/transferencias/', json=transfer_data)
        
        # Verificar erro
        assert response.status_code == 400
        error = response.json()
        assert 'DESTINATION_WALLET_NOT_FOUND' in error['code']
    
    def test_transfer_invalid_amount(self):
        """Testa transferência com valores inválidos"""
        client = TestClient(app)
        
        # Criar duas carteiras
        wallet1_data = {'name': 'Sender Wallet', 'password': 'test12345'}
        response1 = client.post('/api/v1/carteiras/', json=wallet1_data)
        assert response1.status_code == 201
        wallet1 = response1.json()
        
        wallet2_data = {'name': 'Receiver Wallet', 'password': 'test12345'}
        response2 = client.post('/api/v1/carteiras/', json=wallet2_data)
        assert response2.status_code == 201
        wallet2 = response2.json()
        
        # Testar valores inválidos
        invalid_amounts = [0, -10, -0.01]
        
        for amount in invalid_amounts:
            transfer_data = {
                'from_address': wallet1['address'],
                'to_address': wallet2['address'],
                'amount': amount,
                'reason': 'Test transfer'
            }
            response = client.post('/api/v1/transferencias/', json=transfer_data)
            
            # Verificar erro
            assert response.status_code == 422  # Validation error
    
    def test_transfer_custom_fee(self):
        """Testa transferência com taxa personalizada"""
        client = TestClient(app)
        
        # Criar duas carteiras
        wallet1_data = {'name': 'Sender Wallet', 'password': 'test12345'}
        response1 = client.post('/api/v1/carteiras/', json=wallet1_data)
        assert response1.status_code == 201
        wallet1 = response1.json()
        
        wallet2_data = {'name': 'Receiver Wallet', 'password': 'test12345'}
        response2 = client.post('/api/v1/carteiras/', json=wallet2_data)
        assert response2.status_code == 201
        wallet2 = response2.json()
        
        # Creditar carteira de origem
        credit_data = {'amount': 100.0, 'reason': 'Initial credit'}
        response = client.post(f'/api/v1/carteiras/{wallet1["address"]}/credit', json=credit_data)
        assert response.status_code == 200
        
        # Fazer transferência com taxa personalizada
        transfer_data = {
            'from_address': wallet1['address'],
            'to_address': wallet2['address'],
            'amount': 50.0,
            'fee': 0.1,  # Taxa personalizada
            'reason': 'Test transfer with custom fee'
        }
        response = client.post('/api/v1/transferencias/', json=transfer_data)
        
        # Verificar resposta
        assert response.status_code == 201
        transfer = response.json()
        
        assert transfer['fee'] == 0.1
        assert transfer['total_amount'] == 50.1
    
    def test_transfer_fee_calculation(self):
        """Testa cálculo automático de taxas"""
        client = TestClient(app)
        
        # Criar duas carteiras
        wallet1_data = {'name': 'Sender Wallet', 'password': 'test12345'}
        response1 = client.post('/api/v1/carteiras/', json=wallet1_data)
        assert response1.status_code == 201
        wallet1 = response1.json()
        
        wallet2_data = {'name': 'Receiver Wallet', 'password': 'test12345'}
        response2 = client.post('/api/v1/carteiras/', json=wallet2_data)
        assert response2.status_code == 201
        wallet2 = response2.json()
        
        # Creditar carteira de origem
        credit_data = {'amount': 1000.0, 'reason': 'Initial credit'}
        response = client.post(f'/api/v1/carteiras/{wallet1["address"]}/credit', json=credit_data)
        assert response.status_code == 200
        
        # Fazer transferência grande (deve usar taxa percentual)
        transfer_data = {
            'from_address': wallet1['address'],
            'to_address': wallet2['address'],
            'amount': 500.0,  # Transferência grande
            'reason': 'Large transfer test'
        }
        response = client.post('/api/v1/transferencias/', json=transfer_data)
        
        # Verificar resposta
        assert response.status_code == 201
        transfer = response.json()
        
        # Taxa deve ser 0.5 (0.1% de 500)
        assert transfer['fee'] == 0.5
        assert transfer['total_amount'] == 500.5
    
    def test_transfer_missing_fields(self):
        """Testa transferência com campos obrigatórios ausentes"""
        client = TestClient(app)
        
        # Testar campos ausentes
        invalid_transfers = [
            {},  # Todos os campos ausentes
            {'from_address': 'test'},  # Campos obrigatórios ausentes
            {'to_address': 'test'},  # Campos obrigatórios ausentes
            {'amount': 50.0},  # Campos obrigatórios ausentes
        ]
        
        for transfer_data in invalid_transfers:
            response = client.post('/api/v1/transferencias/', json=transfer_data)
            assert response.status_code == 422  # Validation error
    
    def test_transfer_reason_validation(self):
        """Testa validação do campo reason"""
        client = TestClient(app)
        
        # Criar duas carteiras
        wallet1_data = {'name': 'Sender Wallet', 'password': 'test12345'}
        response1 = client.post('/api/v1/carteiras/', json=wallet1_data)
        assert response1.status_code == 201
        wallet1 = response1.json()
        
        wallet2_data = {'name': 'Receiver Wallet', 'password': 'test12345'}
        response2 = client.post('/api/v1/carteiras/', json=wallet2_data)
        assert response2.status_code == 201
        wallet2 = response2.json()
        
        # Creditar carteira de origem
        credit_data = {'amount': 100.0, 'reason': 'Initial credit'}
        response = client.post(f'/api/v1/carteiras/{wallet1["address"]}/credit', json=credit_data)
        assert response.status_code == 200
        
        # Testar reasons inválidos
        invalid_reasons = [
            '',  # Vazio
            'a' * 201,  # Muito longo
        ]
        
        for reason in invalid_reasons:
            transfer_data = {
                'from_address': wallet1['address'],
                'to_address': wallet2['address'],
                'amount': 10.0,
                'reason': reason
            }
            response = client.post('/api/v1/transferencias/', json=transfer_data)
            assert response.status_code == 422  # Validation error
    
    def test_transfer_concurrent_operations(self):
        """Testa operações concorrentes de transferência"""
        import threading
        import time
        
        client = TestClient(app)
        
        # Criar duas carteiras
        wallet1_data = {'name': 'Sender Wallet', 'password': 'test12345'}
        response1 = client.post('/api/v1/carteiras/', json=wallet1_data)
        assert response1.status_code == 201
        wallet1 = response1.json()
        
        wallet2_data = {'name': 'Receiver Wallet', 'password': 'test12345'}
        response2 = client.post('/api/v1/carteiras/', json=wallet2_data)
        assert response2.status_code == 201
        wallet2 = response2.json()
        
        # Creditar carteira de origem
        credit_data = {'amount': 100.0, 'reason': 'Initial credit'}
        response = client.post(f'/api/v1/carteiras/{wallet1["address"]}/credit', json=credit_data)
        assert response.status_code == 200
        
        # Resultados das transferências concorrentes
        results = []
        
        def make_transfer(amount):
            transfer_data = {
                'from_address': wallet1['address'],
                'to_address': wallet2['address'],
                'amount': amount,
                'reason': f'Concurrent transfer {amount}'
            }
            response = client.post('/api/v1/transferencias/', json=transfer_data)
            results.append((amount, response.status_code))
        
        # Criar threads para transferências concorrentes
        threads = []
        amounts = [10.0, 15.0, 20.0, 25.0]  # Total: 70.0 (saldo: 100.0)
        
        for amount in amounts:
            thread = threading.Thread(target=make_transfer, args=(amount,))
            threads.append(thread)
            thread.start()
        
        # Aguardar todas as threads
        for thread in threads:
            thread.join()
        
        # Verificar resultados
        successful_transfers = [result for result in results if result[1] == 201]
        failed_transfers = [result for result in results if result[1] != 201]
        
        # Pelo menos uma transferência deve ter sucesso
        assert len(successful_transfers) >= 1
        
        # Verificar que não excedeu o saldo total
        total_successful = sum(result[0] for result in successful_transfers)
        assert total_successful <= 100.0  # Saldo inicial
    
    def test_transfer_health_check(self):
        """Testa endpoint de health check das transferências"""
        client = TestClient(app)
        
        response = client.get('/api/v1/transferencias/health')
        assert response.status_code == 200
        
        health = response.json()
        assert health['service'] == 'transferencias'
        assert health['status'] == 'healthy'
        assert 'version' in health
