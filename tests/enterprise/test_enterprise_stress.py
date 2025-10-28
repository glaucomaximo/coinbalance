"""
Testes de Stress e Carga para Sistemas Enterprise
=================================================

Este módulo implementa testes de stress e carga para todos os sistemas enterprise,
incluindo testes de escalabilidade, performance e estabilidade.

EVOLUÇÃO: Testes de stress e carga para sistemas enterprise com métricas detalhadas.
"""

import pytest
import asyncio
import time
import threading
import multiprocessing
import uuid
import statistics
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import logging
import psutil
import gc

# Imports dos sistemas enterprise
from src.domain.blockchain.entities.blockchain import Blockchain
from src.domain.blockchain.infrastructure.blockchain_index import blockchain_index, transaction_pool
from src.domain.blockchain.infrastructure.parallel_miner import parallel_miner
from src.domain.blockchain.infrastructure.incremental_validator import incremental_validator
from src.domain.blockchain.infrastructure.blockchain_tree import blockchain_tree
from src.domain.blockchain.infrastructure.distributed_cache import distributed_cache
from src.domain.blockchain.infrastructure.network_optimizer import network_optimizer
from src.domain.blockchain.infrastructure.horizontal_scaler import horizontal_scaler
from src.domain.blockchain.infrastructure.real_time_monitor import real_time_monitor

logger = logging.getLogger(__name__)


class StressTestResults:
    """Resultados de testes de stress."""
    
    def __init__(self):
        self.operations_count = 0
        self.total_time = 0.0
        self.operations_per_second = 0.0
        self.memory_usage = []
        self.cpu_usage = []
        self.errors = []
        self.thread_count = 0
        self.process_count = 0
    
    def add_measurement(self, memory_mb: float, cpu_percent: float):
        """Adiciona medição de recursos."""
        self.memory_usage.append(memory_mb)
        self.cpu_usage.append(cpu_percent)
    
    def calculate_stats(self):
        """Calcula estatísticas dos resultados."""
        if self.total_time > 0:
            self.operations_per_second = self.operations_count / self.total_time
        
        self.avg_memory = statistics.mean(self.memory_usage) if self.memory_usage else 0
        self.max_memory = max(self.memory_usage) if self.memory_usage else 0
        self.avg_cpu = statistics.mean(self.cpu_usage) if self.cpu_usage else 0
        self.max_cpu = max(self.cpu_usage) if self.cpu_usage else 0


class TestEnterpriseStress:
    """
    Testes de stress para sistemas enterprise.
    
    EVOLUÇÃO: Testes de stress completos para todos os sistemas enterprise.
    """
    
    @pytest.fixture
    def blockchain(self):
        """Fixture para blockchain de teste."""
        return Blockchain.create()
    
    def test_distributed_cache_stress(self):
        """
        Teste de stress para cache distribuído.
        
        EVOLUÇÃO: Teste de stress para cache distribuído com métricas detalhadas.
        """
        # Configurar cache para stress
        distributed_cache.max_local_cache_size = 10000
        
        # Adicionar nós
        for i in range(5):
            distributed_cache.add_node(f"stress_node_{i}", "localhost", 8000 + i)
        
        results = StressTestResults()
        operations_count = 10000
        thread_count = 20
        
        def cache_stress_worker(thread_id: int, operations_per_thread: int):
            """Worker para stress de cache."""
            errors = []
            for i in range(operations_per_thread):
                try:
                    key = f"stress_key_{thread_id}_{i}"
                    value = f"stress_value_{thread_id}_{i}"
                    
                    # Operação de escrita
                    distributed_cache.put(key, value)
                    
                    # Operação de leitura
                    retrieved = distributed_cache.get(key)
                    if retrieved != value:
                        errors.append(f"Mismatch for key {key}")
                    
                    # Operação de remoção
                    distributed_cache.delete(key)
                    
                except Exception as e:
                    errors.append(str(e))
            
            return errors
        
        # Executar stress test
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            operations_per_thread = operations_count // thread_count
            
            for thread_id in range(thread_count):
                future = executor.submit(cache_stress_worker, thread_id, operations_per_thread)
                futures.append(future)
            
            # Monitorar recursos
            process = psutil.Process()
            monitoring_thread = threading.Thread(
                target=self._monitor_resources,
                args=(process, results, start_time, 30)  # Monitorar por 30 segundos
            )
            monitoring_thread.start()
            
            # Coletar resultados
            for future in as_completed(futures):
                errors = future.result()
                results.errors.extend(errors)
        
        end_time = time.time()
        results.total_time = end_time - start_time
        results.operations_count = operations_count
        results.thread_count = thread_count
        results.calculate_stats()
        
        # Verificar resultados
        assert results.operations_per_second > 1000, f"Performance insuficiente: {results.operations_per_second} ops/s"
        assert len(results.errors) == 0, f"Erros encontrados: {results.errors}"
        assert results.max_memory < 1000, f"Uso de memória excessivo: {results.max_memory} MB"
        
        logger.info(f"Cache Stress Test: {results.operations_per_second:.2f} ops/s, "
                   f"Memory: {results.max_memory:.2f} MB, CPU: {results.max_cpu:.2f}%")
    
    def test_horizontal_scaling_stress(self):
        """
        Teste de stress para escalabilidade horizontal.
        
        EVOLUÇÃO: Teste de stress para escalabilidade horizontal com métricas detalhadas.
        """
        # Configurar escalabilidade para stress
        horizontal_scaler.max_shards = 50
        horizontal_scaler.shard_size_threshold = 1000
        
        results = StressTestResults()
        operations_count = 5000
        thread_count = 15
        
        # Criar shards iniciais
        for i in range(10):
            horizontal_scaler.create_shard(f"stress_shard_{i}", node_count=3)
        
        def scaling_stress_worker(thread_id: int, operations_per_thread: int):
            """Worker para stress de escalabilidade."""
            errors = []
            for i in range(operations_per_thread):
                try:
                    # Operação de distribuição de bloco
                    from src.domain.blockchain.entities.block import Block
                    from src.domain.shared.value_objects.hash_value import HashValue
                    from src.domain.shared.value_objects.timestamp import Timestamp
                    
                    block = Block(
                        height=i,
                        hash=HashValue(f"stress_hash_{thread_id}_{i}"),
                        previous_hash=HashValue(f"stress_hash_{thread_id}_{i-1}" if i > 0 else "genesis"),
                        timestamp=Timestamp(time.time()),
                        transactions=[],
                        nonce=12345 + i,
                        difficulty=4,
                        mining_time=1.0
                    )
                    
                    result = horizontal_scaler.distribute_block(block)
                    if not result["success"]:
                        errors.append(f"Failed to distribute block {i}")
                    
                    # Operação de seleção de nó
                    shard_id = f"stress_shard_{i % 10}"
                    node = horizontal_scaler.get_node_for_request(shard_id)
                    if node is None:
                        errors.append(f"No node available for shard {shard_id}")
                    
                except Exception as e:
                    errors.append(str(e))
            
            return errors
        
        # Executar stress test
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            operations_per_thread = operations_count // thread_count
            
            for thread_id in range(thread_count):
                future = executor.submit(scaling_stress_worker, thread_id, operations_per_thread)
                futures.append(future)
            
            # Monitorar recursos
            process = psutil.Process()
            monitoring_thread = threading.Thread(
                target=self._monitor_resources,
                args=(process, results, start_time, 30)
            )
            monitoring_thread.start()
            
            # Coletar resultados
            for future in as_completed(futures):
                errors = future.result()
                results.errors.extend(errors)
        
        end_time = time.time()
        results.total_time = end_time - start_time
        results.operations_count = operations_count
        results.thread_count = thread_count
        results.calculate_stats()
        
        # Verificar resultados
        assert results.operations_per_second > 500, f"Performance insuficiente: {results.operations_per_second} ops/s"
        assert len(results.errors) == 0, f"Erros encontrados: {results.errors}"
        
        logger.info(f"Scaling Stress Test: {results.operations_per_second:.2f} ops/s, "
                   f"Memory: {results.max_memory:.2f} MB, CPU: {results.max_cpu:.2f}%")
    
    def test_real_time_monitoring_stress(self):
        """
        Teste de stress para monitoramento em tempo real.
        
        EVOLUÇÃO: Teste de stress para monitoramento em tempo real com métricas detalhadas.
        """
        results = StressTestResults()
        operations_count = 20000
        thread_count = 25
        
        def monitoring_stress_worker(thread_id: int, operations_per_thread: int):
            """Worker para stress de monitoramento."""
            errors = []
            for i in range(operations_per_thread):
                try:
                    # Operação de coleta de métrica
                    metric_name = f"stress.metric.{thread_id}.{i}"
                    metric_value = float(i)
                    tags = {"thread": str(thread_id), "iteration": str(i)}
                    
                    real_time_monitor.collect_metric(metric_name, metric_value, tags=tags)
                    
                    # Operação de criação de regra de alerta (ocasional)
                    if i % 100 == 0:
                        rule_id = f"stress_rule_{thread_id}_{i}"
                        real_time_monitor.create_alert_rule(
                            rule_id, f"Stress Rule {thread_id}_{i}",
                            metric_name, ">", metric_value + 100
                        )
                    
                except Exception as e:
                    errors.append(str(e))
            
            return errors
        
        # Executar stress test
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            operations_per_thread = operations_count // thread_count
            
            for thread_id in range(thread_count):
                future = executor.submit(monitoring_stress_worker, thread_id, operations_per_thread)
                futures.append(future)
            
            # Monitorar recursos
            process = psutil.Process()
            monitoring_thread = threading.Thread(
                target=self._monitor_resources,
                args=(process, results, start_time, 30)
            )
            monitoring_thread.start()
            
            # Coletar resultados
            for future in as_completed(futures):
                errors = future.result()
                results.errors.extend(errors)
        
        end_time = time.time()
        results.total_time = end_time - start_time
        results.operations_count = operations_count
        results.thread_count = thread_count
        results.calculate_stats()
        
        # Verificar resultados
        assert results.operations_per_second > 2000, f"Performance insuficiente: {results.operations_per_second} ops/s"
        assert len(results.errors) == 0, f"Erros encontrados: {results.errors}"
        
        logger.info(f"Monitoring Stress Test: {results.operations_per_second:.2f} ops/s, "
                   f"Memory: {results.max_memory:.2f} MB, CPU: {results.max_cpu:.2f}%")
    
    def test_network_optimization_stress(self):
        """
        Teste de stress para otimização de rede.
        
        EVOLUÇÃO: Teste de stress para otimização de rede com métricas detalhadas.
        """
        # Configurar rede para stress
        network_optimizer.max_cache_size = 5000
        
        # Adicionar nós
        for i in range(10):
            network_optimizer.add_node(f"stress_network_node_{i}", "localhost", 8000 + i)
        
        results = StressTestResults()
        operations_count = 15000
        thread_count = 20
        
        def network_stress_worker(thread_id: int, operations_per_thread: int):
            """Worker para stress de rede."""
            errors = []
            for i in range(operations_per_thread):
                try:
                    # Operação de envio de mensagem
                    target_node = f"stress_network_node_{i % 10}"
                    message_type = f"stress_message_{thread_id}"
                    payload = {"data": f"stress_data_{thread_id}_{i}", "timestamp": time.time()}
                    
                    success = network_optimizer.send_message(target_node, message_type, payload)
                    if not success:
                        errors.append(f"Failed to send message {i}")
                    
                    # Operação de broadcast (ocasional)
                    if i % 50 == 0:
                        broadcast_result = network_optimizer.broadcast_message(
                            f"stress_broadcast_{thread_id}", payload
                        )
                        if len(broadcast_result) == 0:
                            errors.append(f"Failed broadcast {i}")
                    
                except Exception as e:
                    errors.append(str(e))
            
            return errors
        
        # Executar stress test
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            operations_per_thread = operations_count // thread_count
            
            for thread_id in range(thread_count):
                future = executor.submit(network_stress_worker, thread_id, operations_per_thread)
                futures.append(future)
            
            # Monitorar recursos
            process = psutil.Process()
            monitoring_thread = threading.Thread(
                target=self._monitor_resources,
                args=(process, results, start_time, 30)
            )
            monitoring_thread.start()
            
            # Coletar resultados
            for future in as_completed(futures):
                errors = future.result()
                results.errors.extend(errors)
        
        end_time = time.time()
        results.total_time = end_time - start_time
        results.operations_count = operations_count
        results.thread_count = thread_count
        results.calculate_stats()
        
        # Verificar resultados
        assert results.operations_per_second > 1500, f"Performance insuficiente: {results.operations_per_second} ops/s"
        assert len(results.errors) == 0, f"Erros encontrados: {results.errors}"
        
        logger.info(f"Network Stress Test: {results.operations_per_second:.2f} ops/s, "
                   f"Memory: {results.max_memory:.2f} MB, CPU: {results.max_cpu:.2f}%")
    
    def test_parallel_mining_stress(self):
        """
        Teste de stress para mineração paralela.
        
        EVOLUÇÃO: Teste de stress para mineração paralela com métricas detalhadas.
        """
        # Configurar mineração para stress
        parallel_miner.configure_mining(
            max_threads=16,
            max_processes=8,
            nonce_cache_size=5000
        )
        
        results = StressTestResults()
        operations_count = 100
        thread_count = 10
        
        def mining_stress_worker(thread_id: int, operations_per_thread: int):
            """Worker para stress de mineração."""
            errors = []
            for i in range(operations_per_thread):
                try:
                    # Criar bloco para mineração
                    from src.domain.blockchain.entities.block import Block
                    from src.domain.shared.value_objects.hash_value import HashValue
                    from src.domain.shared.value_objects.timestamp import Timestamp
                    
                    block = Block(
                        height=i,
                        hash=HashValue(""),
                        previous_hash=HashValue(f"stress_mining_hash_{thread_id}_{i-1}" if i > 0 else "genesis"),
                        timestamp=Timestamp(time.time()),
                        transactions=[],
                        nonce=0,
                        difficulty=3,  # Dificuldade moderada para teste
                        mining_time=0.0
                    )
                    
                    # Operação de mineração
                    result = parallel_miner.mine_block(block)
                    if not result["success"]:
                        errors.append(f"Failed to mine block {i}")
                    elif result["nonce"] <= 0:
                        errors.append(f"Invalid nonce for block {i}")
                    
                except Exception as e:
                    errors.append(str(e))
            
            return errors
        
        # Executar stress test
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            operations_per_thread = operations_count // thread_count
            
            for thread_id in range(thread_count):
                future = executor.submit(mining_stress_worker, thread_id, operations_per_thread)
                futures.append(future)
            
            # Monitorar recursos
            process = psutil.Process()
            monitoring_thread = threading.Thread(
                target=self._monitor_resources,
                args=(process, results, start_time, 60)  # Mineração pode demorar mais
            )
            monitoring_thread.start()
            
            # Coletar resultados
            for future in as_completed(futures):
                errors = future.result()
                results.errors.extend(errors)
        
        end_time = time.time()
        results.total_time = end_time - start_time
        results.operations_count = operations_count
        results.thread_count = thread_count
        results.calculate_stats()
        
        # Verificar resultados
        assert results.operations_per_second > 1, f"Performance insuficiente: {results.operations_per_second} ops/s"
        assert len(results.errors) == 0, f"Erros encontrados: {results.errors}"
        
        logger.info(f"Mining Stress Test: {results.operations_per_second:.2f} ops/s, "
                   f"Memory: {results.max_memory:.2f} MB, CPU: {results.max_cpu:.2f}%")
    
    def test_enterprise_systems_integrated_stress(self, blockchain):
        """
        Teste de stress integrado para todos os sistemas enterprise.
        
        EVOLUÇÃO: Teste de stress integrado para todos os sistemas enterprise.
        """
        # Configurar todos os sistemas para stress
        distributed_cache.max_local_cache_size = 10000
        network_optimizer.max_cache_size = 5000
        parallel_miner.configure_mining(max_threads=8, max_processes=4)
        
        # Criar shards e nós
        for i in range(5):
            blockchain.create_shard(f"integrated_shard_{i}", 3, 2)
            for j in range(3):
                blockchain.add_node_to_shard(
                    f"integrated_shard_{i}", f"integrated_node_{i}_{j}",
                    "localhost", 8000 + i * 100 + j
                )
        
        # Criar regras de alerta
        for i in range(10):
            blockchain.create_alert_rule(
                f"integrated_alert_{i}", f"Integrated Alert {i}",
                f"integrated.metric.{i}", ">", 100.0 + i
            )
        
        results = StressTestResults()
        operations_count = 5000
        thread_count = 15
        
        def integrated_stress_worker(thread_id: int, operations_per_thread: int):
            """Worker para stress integrado."""
            errors = []
            for i in range(operations_per_thread):
                try:
                    # Operação de cache
                    cache_key = f"integrated_cache_{thread_id}_{i}"
                    cache_value = f"integrated_value_{thread_id}_{i}"
                    distributed_cache.put(cache_key, cache_value)
                    retrieved = distributed_cache.get(cache_key)
                    if retrieved != cache_value:
                        errors.append(f"Cache mismatch for {cache_key}")
                    
                    # Operação de rede
                    target_node = f"integrated_node_{i % 5}_{i % 3}"
                    network_optimizer.send_message(target_node, "integrated_message", {"data": i})
                    
                    # Operação de monitoramento
                    real_time_monitor.collect_metric(
                        f"integrated.metric.{thread_id}.{i}", float(i),
                        tags={"thread": str(thread_id), "operation": str(i)}
                    )
                    
                    # Operação de escalabilidade
                    shard_id = f"integrated_shard_{i % 5}"
                    node = horizontal_scaler.get_node_for_request(shard_id)
                    if node is None:
                        errors.append(f"No node available for shard {shard_id}")
                    
                    # Operação de mineração (ocasional)
                    if i % 20 == 0:
                        from src.domain.blockchain.entities.block import Block
                        from src.domain.shared.value_objects.hash_value import HashValue
                        from src.domain.shared.value_objects.timestamp import Timestamp
                        
                        block = Block(
                            height=i,
                            hash=HashValue(""),
                            previous_hash=HashValue(f"integrated_hash_{thread_id}_{i-1}" if i > 0 else "genesis"),
                            timestamp=Timestamp(time.time()),
                            transactions=[],
                            nonce=0,
                            difficulty=2,
                            mining_time=0.0
                        )
                        
                        result = parallel_miner.mine_block(block)
                        if not result["success"]:
                            errors.append(f"Failed to mine block {i}")
                    
                except Exception as e:
                    errors.append(str(e))
            
            return errors
        
        # Executar stress test
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            operations_per_thread = operations_count // thread_count
            
            for thread_id in range(thread_count):
                future = executor.submit(integrated_stress_worker, thread_id, operations_per_thread)
                futures.append(future)
            
            # Monitorar recursos
            process = psutil.Process()
            monitoring_thread = threading.Thread(
                target=self._monitor_resources,
                args=(process, results, start_time, 60)
            )
            monitoring_thread.start()
            
            # Coletar resultados
            for future in as_completed(futures):
                errors = future.result()
                results.errors.extend(errors)
        
        end_time = time.time()
        results.total_time = end_time - start_time
        results.operations_count = operations_count
        results.thread_count = thread_count
        results.calculate_stats()
        
        # Verificar resultados
        assert results.operations_per_second > 500, f"Performance insuficiente: {results.operations_per_second} ops/s"
        assert len(results.errors) == 0, f"Erros encontrados: {results.errors}"
        assert results.max_memory < 2000, f"Uso de memória excessivo: {results.max_memory} MB"
        
        logger.info(f"Integrated Stress Test: {results.operations_per_second:.2f} ops/s, "
                   f"Memory: {results.max_memory:.2f} MB, CPU: {results.max_cpu:.2f}%")
    
    def _monitor_resources(self, process: psutil.Process, results: StressTestResults, 
                          start_time: float, duration: float):
        """Monitora recursos do sistema durante o teste."""
        end_time = start_time + duration
        
        while time.time() < end_time:
            try:
                memory_info = process.memory_info()
                memory_mb = memory_info.rss / 1024 / 1024
                cpu_percent = process.cpu_percent()
                
                results.add_measurement(memory_mb, cpu_percent)
                time.sleep(0.1)  # Monitorar a cada 100ms
                
            except Exception:
                break


class TestEnterpriseLoad:
    """
    Testes de carga para sistemas enterprise.
    
    EVOLUÇÃO: Testes de carga completos para todos os sistemas enterprise.
    """
    
    def test_sustained_load_performance(self):
        """
        Teste de performance sob carga sustentada.
        
        EVOLUÇÃO: Teste de performance sob carga sustentada para sistemas enterprise.
        """
        # Configurar sistemas para carga sustentada
        distributed_cache.max_local_cache_size = 50000
        network_optimizer.max_cache_size = 10000
        
        # Adicionar nós
        for i in range(20):
            distributed_cache.add_node(f"load_node_{i}", "localhost", 8000 + i)
            network_optimizer.add_node(f"load_network_node_{i}", "localhost", 8000 + i)
        
        # Criar shards
        for i in range(10):
            horizontal_scaler.create_shard(f"load_shard_{i}", node_count=5)
        
        # Executar carga sustentada
        duration_minutes = 5
        operations_per_second = 1000
        total_operations = duration_minutes * 60 * operations_per_second
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        operations_completed = 0
        errors = []
        
        while time.time() < end_time:
            batch_start = time.time()
            batch_operations = 0
            
            # Executar lote de operações
            for i in range(100):  # Lotes de 100 operações
                try:
                    # Operação de cache
                    key = f"load_key_{operations_completed + i}"
                    value = f"load_value_{operations_completed + i}"
                    distributed_cache.put(key, value)
                    distributed_cache.get(key)
                    
                    # Operação de rede
                    target_node = f"load_network_node_{i % 20}"
                    network_optimizer.send_message(target_node, "load_message", {"data": i})
                    
                    # Operação de monitoramento
                    real_time_monitor.collect_metric(
                        f"load.metric.{operations_completed + i}", float(i)
                    )
                    
                    # Operação de escalabilidade
                    shard_id = f"load_shard_{i % 10}"
                    horizontal_scaler.get_node_for_request(shard_id)
                    
                    batch_operations += 1
                    
                except Exception as e:
                    errors.append(str(e))
                
                operations_completed += 1
            
            # Controlar taxa de operações
            batch_time = time.time() - batch_start
            target_batch_time = 100 / operations_per_second
            
            if batch_time < target_batch_time:
                time.sleep(target_batch_time - batch_time)
        
        total_time = time.time() - start_time
        actual_ops_per_second = operations_completed / total_time
        
        # Verificar resultados
        assert actual_ops_per_second >= operations_per_second * 0.9, f"Performance insuficiente: {actual_ops_per_second} ops/s"
        assert len(errors) == 0, f"Erros encontrados: {errors}"
        
        logger.info(f"Sustained Load Test: {actual_ops_per_second:.2f} ops/s over {duration_minutes} minutes")
    
    def test_memory_leak_detection(self):
        """
        Teste de detecção de vazamentos de memória.
        
        EVOLUÇÃO: Teste de detecção de vazamentos de memória para sistemas enterprise.
        """
        import gc
        
        # Medir memória inicial
        gc.collect()
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Executar operações que podem causar vazamentos
        iterations = 1000
        for i in range(iterations):
            # Operações de cache
            for j in range(10):
                key = f"leak_test_key_{i}_{j}"
                value = f"leak_test_value_{i}_{j}"
                distributed_cache.put(key, value)
                distributed_cache.get(key)
                distributed_cache.delete(key)
            
            # Operações de monitoramento
            for j in range(10):
                real_time_monitor.collect_metric(
                    f"leak_test.metric.{i}.{j}", float(j)
                )
            
            # Operações de rede
            for j in range(10):
                network_optimizer.send_message(
                    f"load_network_node_{j % 20}", "leak_test_message", {"data": j}
                )
            
            # Limpeza periódica
            if i % 100 == 0:
                gc.collect()
        
        # Medir memória final
        gc.collect()
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        memory_increase = final_memory - initial_memory
        
        # Verificar vazamento de memória
        assert memory_increase < 100, f"Possível vazamento de memória: {memory_increase} MB"
        
        logger.info(f"Memory Leak Test: {memory_increase:.2f} MB increase over {iterations} iterations")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
