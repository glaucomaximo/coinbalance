"""
Testes de Performance para CoinBalance
"""

import pytest
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
from fastapi.testclient import TestClient

from src.presentation.api.app import app


class TestWalletPerformance:
    """Testes de performance para operações de carteira"""
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_wallet_creation_performance(self):
        """Testa performance de criação de carteiras"""
        # Arrange - Limpar banco antes do teste
        from src.infrastructure.persistence.database_manager import DatabaseManager
        db_manager = DatabaseManager()
        db_manager.execute_update('DELETE FROM wallets')
        
        client = TestClient(app)
        wallet_data = {
            "name": "Performance Test Wallet",
            "password": "test12345"
        }
        
        # Act - Medir tempo de criação
        start_time = time.time()
        response = client.post("/api/v1/carteiras/", json=wallet_data)
        end_time = time.time()
        
        # Assert
        assert response.status_code == 201
        creation_time = end_time - start_time
        
        # Performance assertion - criação deve ser rápida
        assert creation_time < 1.0, f"Wallet creation took {creation_time:.3f}s, expected < 1.0s"
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_wallet_creation_concurrent_performance(self):
        """Testa performance de criação concorrente de carteiras"""
        # Arrange
        client = TestClient(app)
        num_wallets = 10  # Reduzido para teste mais rápido
        wallet_data_template = {
            "name": "Concurrent Test Wallet",
            "password": "test12345"
        }
        
        def create_wallet(index: int):
            """Cria uma carteira com índice único"""
            wallet_data = wallet_data_template.copy()
            wallet_data["name"] = f"{wallet_data_template['name']} {index}"
            
            start_time = time.time()
            response = client.post("/api/v1/carteiras/", json=wallet_data)
            end_time = time.time()
            
            return {
                "status_code": response.status_code,
                "creation_time": end_time - start_time,
                "index": index
            }
        
        # Act - Criar carteiras concorrentemente
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(create_wallet, i) for i in range(num_wallets)]
            results = [future.result() for future in as_completed(futures)]
        end_time = time.time()
        
        # Assert
        total_time = end_time - start_time
        successful_creations = [r for r in results if r["status_code"] == 201]
        creation_times = [r["creation_time"] for r in successful_creations]
        
        # Verificar que todas as criações foram bem-sucedidas
        assert len(successful_creations) == num_wallets
        
        # Verificar performance
        if creation_times:
            avg_creation_time = statistics.mean(creation_times)
            max_creation_time = max(creation_times)
            
            # Performance assertions
            assert avg_creation_time < 0.5, f"Average creation time {avg_creation_time:.3f}s too slow"
            assert max_creation_time < 2.0, f"Max creation time {max_creation_time:.3f}s too slow"
            assert total_time < 10.0, f"Total concurrent time {total_time:.3f}s too slow"
            
            # Calcular throughput
            throughput = num_wallets / total_time
            assert throughput > 1.0, f"Throughput {throughput:.2f} wallets/sec too low"
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_wallet_operations_performance(self):
        """Testa performance de operações de carteira"""
        # Arrange - Criar carteira
        client = TestClient(app)
        wallet_data = {
            "name": "Operations Test Wallet",
            "password": "test12345"
        }
        
        create_response = client.post("/api/v1/carteiras/", json=wallet_data)
        assert create_response.status_code == 201
        
        created_wallet = create_response.json()
        wallet_address = created_wallet["address"]
        
        # Creditar valor primeiro
        credit_data = {"amount": 1000.0, "reason": "Initial credit"}
        client.post(f"/api/v1/carteiras/{wallet_address}/credit", json=credit_data)
        
        # Act - Medir operações
        operations = [
            {"type": "credit", "amount": 100.0, "reason": "Test credit"},
            {"type": "debit", "amount": 50.0, "reason": "Test debit"},
            {"type": "credit", "amount": 25.0, "reason": "Test credit 2"},
            {"type": "debit", "amount": 10.0, "reason": "Test debit 2"},
        ]
        
        operation_times = []
        
        for op in operations:
            start_time = time.time()
            if op["type"] == "credit":
                response = client.post(
                    f"/api/v1/carteiras/{wallet_address}/credit",
                    json={"amount": op["amount"], "reason": op["reason"]}
                )
            else:
                response = client.post(
                    f"/api/v1/carteiras/{wallet_address}/debit",
                    json={"amount": op["amount"], "reason": op["reason"]}
                )
            end_time = time.time()
            
            assert response.status_code == 200
            operation_times.append(end_time - start_time)
        
        # Assert
        avg_operation_time = statistics.mean(operation_times)
        max_operation_time = max(operation_times)
        
        assert avg_operation_time < 0.1, f"Average operation time {avg_operation_time:.3f}s too slow"
        assert max_operation_time < 0.5, f"Max operation time {max_operation_time:.3f}s too slow"
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_wallet_list_performance(self):
        """Testa performance de listagem de carteiras"""
        # Arrange - Criar várias carteiras
        client = TestClient(app)
        num_wallets = 20
        
        for i in range(num_wallets):
            wallet_data = {
                "name": f"List Test Wallet {i}",
                "password": "test12345"
            }
            response = client.post("/api/v1/carteiras/", json=wallet_data)
            assert response.status_code == 201
        
        # Act - Medir tempo de listagem
        start_time = time.time()
        response = client.get("/api/v1/carteiras/")
        end_time = time.time()
        
        # Assert
        assert response.status_code == 200
        list_time = end_time - start_time
        
        data = response.json()
        assert len(data["wallets"]) >= num_wallets
        
        # Performance assertion
        assert list_time < 0.5, f"Wallet list took {list_time:.3f}s, expected < 0.5s"
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_memory_usage_performance(self):
        """Testa uso de memória durante operações"""
        import psutil
        import gc
        
        # Arrange
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        client = TestClient(app)
        
        # Act - Criar muitas carteiras
        num_wallets = 100
        for i in range(num_wallets):
            wallet_data = {
                "name": f"Memory Test Wallet {i}",
                "password": "test12345"
            }
            response = client.post("/api/v1/carteiras/", json=wallet_data)
            assert response.status_code == 201
            
            # Forçar garbage collection a cada 10 carteiras
            if i % 10 == 0:
                gc.collect()
        
        # Medir memória final
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Assert
        # Memória não deve aumentar mais que 50MB para 100 carteiras
        assert memory_increase < 50, f"Memory increased by {memory_increase:.2f}MB, expected < 50MB"


class TestAPIPerformance:
    """Testes de performance da API"""
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_api_response_time_consistency(self):
        """Testa consistência dos tempos de resposta da API"""
        # Arrange
        client = TestClient(app)
        wallet_data = {
            "name": "Consistency Test Wallet",
            "password": "test12345"
        }
        
        # Act - Múltiplas requisições
        response_times = []
        num_requests = 10
        
        for i in range(num_requests):
            wallet_data["name"] = f"Consistency Test Wallet {i}"
            
            start_time = time.time()
            response = client.post("/api/v1/carteiras/", json=wallet_data)
            end_time = time.time()
            
            assert response.status_code == 201
            response_times.append(end_time - start_time)
        
        # Assert
        avg_response_time = statistics.mean(response_times)
        std_deviation = statistics.stdev(response_times) if len(response_times) > 1 else 0
        
        # Tempo médio deve ser consistente
        assert avg_response_time < 0.5, f"Average response time {avg_response_time:.3f}s too slow"
        
        # Desvio padrão deve ser baixo (consistência)
        assert std_deviation < 0.1, f"Response time inconsistency {std_deviation:.3f}s too high"
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_api_concurrent_load_performance(self):
        """Testa performance da API sob carga concorrente"""
        # Arrange
        client = TestClient(app)
        num_concurrent_requests = 20
        
        def make_request(index: int):
            """Faz uma requisição de criação de carteira"""
            wallet_data = {
                "name": f"Load Test Wallet {index}",
                "password": "test12345"
            }
            
            start_time = time.time()
            response = client.post("/api/v1/carteiras/", json=wallet_data)
            end_time = time.time()
            
            return {
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "index": index
            }
        
        # Act - Requisições concorrentes
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request, i) for i in range(num_concurrent_requests)]
            results = [future.result() for future in as_completed(futures)]
        end_time = time.time()
        
        # Assert
        total_time = end_time - start_time
        successful_requests = [r for r in results if r["status_code"] == 201]
        response_times = [r["response_time"] for r in successful_requests]
        
        # Verificar sucesso
        assert len(successful_requests) == num_concurrent_requests
        
        # Verificar performance
        if response_times:
            avg_response_time = statistics.mean(response_times)
            max_response_time = max(response_times)
            
            assert avg_response_time < 0.5, f"Average response time {avg_response_time:.3f}s too slow"
            assert max_response_time < 2.0, f"Max response time {max_response_time:.3f}s too slow"
            assert total_time < 15.0, f"Total load test time {total_time:.3f}s too slow"
            
            # Throughput
            throughput = num_concurrent_requests / total_time
            assert throughput > 1.0, f"Throughput {throughput:.2f} requests/sec too low"
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_api_error_handling_performance(self):
        """Testa performance do tratamento de erros"""
        # Arrange
        client = TestClient(app)
        
        # Act - Requisições com erro
        error_requests = [
            {"name": "", "password": "test12345"},  # Nome vazio
            {"name": "Test", "password": "123"},  # Senha muito curta
            {"name": "A" * 200, "password": "test12345"},  # Nome muito longo
        ]
        
        error_response_times = []
        
        for request_data in error_requests:
            start_time = time.time()
            response = client.post("/api/v1/carteiras/", json=request_data)
            end_time = time.time()
            
            # Deve retornar erro
            assert response.status_code in [400, 422]
            error_response_times.append(end_time - start_time)
        
        # Assert
        avg_error_time = statistics.mean(error_response_times)
        max_error_time = max(error_response_times)
        
        # Tratamento de erro deve ser rápido
        assert avg_error_time < 0.1, f"Average error handling time {avg_error_time:.3f}s too slow"
        assert max_error_time < 0.5, f"Max error handling time {max_error_time:.3f}s too slow"