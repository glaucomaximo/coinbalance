"""
Testes de Performance da Blockchain Otimizada
============================================

Este módulo implementa testes de performance para validar as otimizações
implementadas na blockchain, incluindo testes de carga, latência e escalabilidade.

EVOLUÇÃO: Testes abrangentes para validar otimizações de performance.
"""

import time
import asyncio
import threading
from typing import List, Dict, Any, Tuple
from decimal import Decimal
import statistics
import logging

from src.domain.blockchain.entities.blockchain import Blockchain
from src.domain.blockchain.entities.block import Block
from src.domain.blockchain.infrastructure.blockchain_index import (
    blockchain_index, transaction_pool
)
from src.domain.transaction.entities.transaction import Transaction
from src.domain.shared.value_objects.hash_value import HashValue
from src.domain.shared.value_objects.timestamp import Timestamp
from src.domain.shared.value_objects.address import Address
from src.domain.shared.value_objects.money import Money

logger = logging.getLogger(__name__)


class BlockchainPerformanceTester:
    """
    Testador de performance da blockchain otimizada.
    
    EVOLUÇÃO: Testes abrangentes para validar otimizações.
    """
    
    def __init__(self):
        self.results = {}
        self.test_data = {}
        
    def generate_test_blocks(self, count: int) -> List[Block]:
        """Gera blocos de teste para performance."""
        blocks = []
        
        for i in range(count):
            # Criar transações de teste
            transactions = []
            for j in range(10):  # 10 transações por bloco
                tx = Transaction.create_transaction(
                    from_address=Address("test_from_" + str(i) + "_" + str(j)),
                    to_address=Address("test_to_" + str(i) + "_" + str(j)),
                    amount=Money.from_cnb(Decimal("1.0")),
                    fee=Money.from_cnb(Decimal("0.001"))
                )
                transactions.append(tx)
            
            # Criar bloco
            if i == 0:
                block = Block.create_genesis_block()
            else:
                previous_hash = blocks[-1].hash if blocks else HashValue("0")
                block = Block.create_block(
                    height=i,
                    previous_hash=previous_hash,
                    transactions=transactions,
                    difficulty=1,
                    miner_address="test_miner_" + str(i)
                )
            
            blocks.append(block)
        
        return blocks
    
    def generate_test_transactions(self, count: int) -> List[Transaction]:
        """Gera transações de teste para performance."""
        transactions = []
        
        for i in range(count):
            tx = Transaction.create_transaction(
                from_address=Address("perf_test_from_" + str(i)),
                to_address=Address("perf_test_to_" + str(i)),
                amount=Money.from_cnb(Decimal("1.0")),
                fee=Money.from_cnb(Decimal("0.001"))
            )
            transactions.append(tx)
        
        return transactions
    
    def test_block_lookup_performance(self, blocks: List[Block]) -> Dict[str, Any]:
        """
        Testa performance de busca de blocos por hash.
        
        EVOLUÇÃO: Validação de busca O(1) vs O(n).
        """
        logger.info("🧪 Testando performance de busca de blocos por hash...")
        
        # Adicionar blocos ao índice
        for block in blocks:
            blockchain_index.add_block(block)
        
        # Teste de busca por hash
        hash_lookup_times = []
        for _ in range(100):  # 100 buscas
            for block in blocks:
                start_time = time.time()
                found_block = blockchain_index.get_block_by_hash(block.hash.value)
                end_time = time.time()
                
                hash_lookup_times.append(end_time - start_time)
                
                # Verificar se encontrou o bloco correto
                assert found_block is not None, "Bloco não encontrado"
                assert found_block.hash.value == block.hash.value, "Bloco incorreto encontrado"
        
        # Teste de busca por altura
        height_lookup_times = []
        for _ in range(100):  # 100 buscas
            for i, block in enumerate(blocks):
                start_time = time.time()
                found_block = blockchain_index.get_block_by_height(i)
                end_time = time.time()
                
                height_lookup_times.append(end_time - start_time)
                
                # Verificar se encontrou o bloco correto
                assert found_block is not None, "Bloco não encontrado por altura"
                assert found_block.height == i, "Altura incorreta"
        
        # Calcular estatísticas
        hash_stats = {
            "min_time": min(hash_lookup_times),
            "max_time": max(hash_lookup_times),
            "avg_time": statistics.mean(hash_lookup_times),
            "median_time": statistics.median(hash_lookup_times),
            "total_lookups": len(hash_lookup_times)
        }
        
        height_stats = {
            "min_time": min(height_lookup_times),
            "max_time": max(height_lookup_times),
            "avg_time": statistics.mean(height_lookup_times),
            "median_time": statistics.median(height_lookup_times),
            "total_lookups": len(height_lookup_times)
        }
        
        # Verificar se performance está dentro dos limites esperados
        assert hash_stats["avg_time"] < 0.001, f"Busca por hash muito lenta: {hash_stats['avg_time']:.6f}s"
        assert height_stats["avg_time"] < 0.001, f"Busca por altura muito lenta: {height_stats['avg_time']:.6f}s"
        
        result = {
            "hash_lookup_stats": hash_stats,
            "height_lookup_stats": height_stats,
            "performance_target_met": hash_stats["avg_time"] < 0.001 and height_stats["avg_time"] < 0.001
        }
        
        logger.info(f"✅ Performance de busca: Hash avg={hash_stats['avg_time']:.6f}s, Height avg={height_stats['avg_time']:.6f}s")
        
        return result
    
    def test_transaction_pool_performance(self, transactions: List[Transaction]) -> Dict[str, Any]:
        """
        Testa performance do pool de transações.
        
        EVOLUÇÃO: Validação de pool otimizado com priorização.
        """
        logger.info("🧪 Testando performance do pool de transações...")
        
        # Teste de adição de transações
        add_times = []
        for tx in transactions:
            start_time = time.time()
            success = transaction_pool.add_transaction(tx)
            end_time = time.time()
            
            add_times.append(end_time - start_time)
            assert success, "Falha ao adicionar transação ao pool"
        
        # Teste de busca de transações para bloco
        retrieval_times = []
        for _ in range(10):  # 10 buscas
            start_time = time.time()
            block_transactions = transaction_pool.get_transactions_for_block(100)
            end_time = time.time()
            
            retrieval_times.append(end_time - start_time)
        
        # Teste de busca por endereço
        address_lookup_times = []
        test_addresses = ["perf_test_from_0", "perf_test_from_1", "perf_test_from_2"]
        for address in test_addresses:
            start_time = time.time()
            address_transactions = transaction_pool.get_transactions_by_address(address)
            end_time = time.time()
            
            address_lookup_times.append(end_time - start_time)
        
        # Calcular estatísticas
        add_stats = {
            "min_time": min(add_times),
            "max_time": max(add_times),
            "avg_time": statistics.mean(add_times),
            "median_time": statistics.median(add_times),
            "total_additions": len(add_times)
        }
        
        retrieval_stats = {
            "min_time": min(retrieval_times),
            "max_time": max(retrieval_times),
            "avg_time": statistics.mean(retrieval_times),
            "median_time": statistics.median(retrieval_times),
            "total_retrievals": len(retrieval_times)
        }
        
        address_stats = {
            "min_time": min(address_lookup_times),
            "max_time": max(address_lookup_times),
            "avg_time": statistics.mean(address_lookup_times),
            "median_time": statistics.median(address_lookup_times),
            "total_lookups": len(address_lookup_times)
        }
        
        # Verificar se performance está dentro dos limites esperados
        assert add_stats["avg_time"] < 0.001, f"Adição de transação muito lenta: {add_stats['avg_time']:.6f}s"
        assert retrieval_stats["avg_time"] < 0.01, f"Busca de transações muito lenta: {retrieval_stats['avg_time']:.6f}s"
        assert address_stats["avg_time"] < 0.01, f"Busca por endereço muito lenta: {address_stats['avg_time']:.6f}s"
        
        result = {
            "add_stats": add_stats,
            "retrieval_stats": retrieval_stats,
            "address_stats": address_stats,
            "performance_target_met": (
                add_stats["avg_time"] < 0.001 and 
                retrieval_stats["avg_time"] < 0.01 and 
                address_stats["avg_time"] < 0.01
            )
        }
        
        logger.info(f"✅ Performance do pool: Add avg={add_stats['avg_time']:.6f}s, Retrieval avg={retrieval_stats['avg_time']:.6f}s")
        
        return result
    
    def test_concurrent_access(self, blocks: List[Block], transactions: List[Transaction]) -> Dict[str, Any]:
        """
        Testa acesso concorrente aos índices e pool.
        
        EVOLUÇÃO: Validação de thread safety e performance concorrente.
        """
        logger.info("🧪 Testando acesso concorrente...")
        
        # Adicionar dados de teste
        for block in blocks:
            blockchain_index.add_block(block)
        
        for tx in transactions[:100]:  # Adicionar apenas 100 transações
            transaction_pool.add_transaction(tx)
        
        # Função para thread de busca de blocos
        def block_lookup_thread(thread_id: int, results: List[Dict]):
            thread_times = []
            for _ in range(50):  # 50 buscas por thread
                for block in blocks:
                    start_time = time.time()
                    found_block = blockchain_index.get_block_by_hash(block.hash.value)
                    end_time = time.time()
                    
                    thread_times.append(end_time - start_time)
                    
                    assert found_block is not None, f"Thread {thread_id}: Bloco não encontrado"
            
            results.append({
                "thread_id": thread_id,
                "times": thread_times,
                "avg_time": statistics.mean(thread_times)
            })
        
        # Função para thread de operações no pool
        def pool_operations_thread(thread_id: int, results: List[Dict]):
            thread_times = []
            for i in range(20):  # 20 operações por thread
                # Adicionar transação
                tx = Transaction.create_transaction(
                    from_address=Address(f"concurrent_from_{thread_id}_{i}"),
                    to_address=Address(f"concurrent_to_{thread_id}_{i}"),
                    amount=Money.from_cnb(Decimal("1.0")),
                    fee=Money.from_cnb(Decimal("0.001"))
                )
                
                start_time = time.time()
                success = transaction_pool.add_transaction(tx)
                end_time = time.time()
                
                thread_times.append(end_time - start_time)
                assert success, f"Thread {thread_id}: Falha ao adicionar transação"
            
            results.append({
                "thread_id": thread_id,
                "times": thread_times,
                "avg_time": statistics.mean(thread_times)
            })
        
        # Executar testes concorrentes
        num_threads = 5
        block_results = []
        pool_results = []
        
        # Criar threads
        block_threads = []
        pool_threads = []
        
        for i in range(num_threads):
            block_thread = threading.Thread(target=block_lookup_thread, args=(i, block_results))
            pool_thread = threading.Thread(target=pool_operations_thread, args=(i, pool_results))
            
            block_threads.append(block_thread)
            pool_threads.append(pool_thread)
        
        # Executar threads
        start_time = time.time()
        
        for thread in block_threads + pool_threads:
            thread.start()
        
        for thread in block_threads + pool_threads:
            thread.join()
        
        end_time = time.time()
        
        # Calcular estatísticas
        all_block_times = []
        for result in block_results:
            all_block_times.extend(result["times"])
        
        all_pool_times = []
        for result in pool_results:
            all_pool_times.extend(result["times"])
        
        block_concurrent_stats = {
            "total_threads": num_threads,
            "total_operations": len(all_block_times),
            "min_time": min(all_block_times),
            "max_time": max(all_block_times),
            "avg_time": statistics.mean(all_block_times),
            "median_time": statistics.median(all_block_times),
            "total_execution_time": end_time - start_time
        }
        
        pool_concurrent_stats = {
            "total_threads": num_threads,
            "total_operations": len(all_pool_times),
            "min_time": min(all_pool_times),
            "max_time": max(all_pool_times),
            "avg_time": statistics.mean(all_pool_times),
            "median_time": statistics.median(all_pool_times),
            "total_execution_time": end_time - start_time
        }
        
        # Verificar se performance concorrente está dentro dos limites
        assert block_concurrent_stats["avg_time"] < 0.01, f"Performance concorrente de blocos muito lenta: {block_concurrent_stats['avg_time']:.6f}s"
        assert pool_concurrent_stats["avg_time"] < 0.01, f"Performance concorrente do pool muito lenta: {pool_concurrent_stats['avg_time']:.6f}s"
        
        result = {
            "block_concurrent_stats": block_concurrent_stats,
            "pool_concurrent_stats": pool_concurrent_stats,
            "performance_target_met": (
                block_concurrent_stats["avg_time"] < 0.01 and 
                pool_concurrent_stats["avg_time"] < 0.01
            )
        }
        
        logger.info(f"✅ Performance concorrente: Blocos avg={block_concurrent_stats['avg_time']:.6f}s, Pool avg={pool_concurrent_stats['avg_time']:.6f}s")
        
        return result
    
    def test_cache_efficiency(self, blocks: List[Block]) -> Dict[str, Any]:
        """
        Testa eficiência do cache.
        
        EVOLUÇÃO: Validação de cache hit rate e performance.
        """
        logger.info("🧪 Testando eficiência do cache...")
        
        # Adicionar blocos ao índice
        for block in blocks:
            blockchain_index.add_block(block)
        
        # Limpar cache para teste limpo
        blockchain_index.clear_cache()
        
        # Primeira passada - cache miss
        first_pass_times = []
        for block in blocks:
            start_time = time.time()
            found_block = blockchain_index.get_block_by_hash(block.hash.value)
            end_time = time.time()
            
            first_pass_times.append(end_time - start_time)
            assert found_block is not None, "Bloco não encontrado na primeira passada"
        
        # Segunda passada - cache hit
        second_pass_times = []
        for block in blocks:
            start_time = time.time()
            found_block = blockchain_index.get_block_by_hash(block.hash.value)
            end_time = time.time()
            
            second_pass_times.append(end_time - start_time)
            assert found_block is not None, "Bloco não encontrado na segunda passada"
        
        # Obter estatísticas do cache
        cache_stats = blockchain_index.get_statistics()
        
        # Calcular melhorias de performance
        first_pass_avg = statistics.mean(first_pass_times)
        second_pass_avg = statistics.mean(second_pass_times)
        
        performance_improvement = (first_pass_avg - second_pass_avg) / first_pass_avg if first_pass_avg > 0 else 0
        
        result = {
            "first_pass_avg_time": first_pass_avg,
            "second_pass_avg_time": second_pass_avg,
            "performance_improvement": performance_improvement,
            "cache_hit_rate": cache_stats["cache_hit_rate"],
            "cache_size": cache_stats["cache_size"],
            "cache_efficient": cache_stats["cache_hit_rate"] > 0.5 and performance_improvement > 0.1
        }
        
        # Verificar se cache está funcionando eficientemente
        assert cache_stats["cache_hit_rate"] > 0.5, f"Cache hit rate muito baixo: {cache_stats['cache_hit_rate']:.2%}"
        assert performance_improvement > 0.1, f"Melhoria de performance muito baixa: {performance_improvement:.2%}"
        
        logger.info(f"✅ Eficiência do cache: Hit rate={cache_stats['cache_hit_rate']:.2%}, Melhoria={performance_improvement:.2%}")
        
        return result
    
    def run_comprehensive_performance_test(self) -> Dict[str, Any]:
        """
        Executa teste abrangente de performance.
        
        EVOLUÇÃO: Teste completo de todas as otimizações.
        """
        logger.info("🚀 Iniciando teste abrangente de performance da blockchain...")
        
        start_time = time.time()
        
        # Gerar dados de teste
        test_blocks = self.generate_test_blocks(100)
        test_transactions = self.generate_test_transactions(1000)
        
        # Executar testes
        test_results = {}
        
        try:
            # Teste de busca de blocos
            test_results["block_lookup"] = self.test_block_lookup_performance(test_blocks)
            
            # Teste do pool de transações
            test_results["transaction_pool"] = self.test_transaction_pool_performance(test_transactions)
            
            # Teste de acesso concorrente
            test_results["concurrent_access"] = self.test_concurrent_access(test_blocks, test_transactions)
            
            # Teste de eficiência do cache
            test_results["cache_efficiency"] = self.test_cache_efficiency(test_blocks)
            
            # Calcular estatísticas gerais
            total_time = time.time() - start_time
            
            # Verificar se todos os testes passaram
            all_tests_passed = all(
                result.get("performance_target_met", False) 
                for result in test_results.values()
            )
            
            # Estatísticas finais
            final_stats = blockchain_index.get_statistics()
            pool_stats = transaction_pool.get_statistics()
            
            comprehensive_result = {
                "test_results": test_results,
                "total_execution_time": total_time,
                "all_tests_passed": all_tests_passed,
                "final_index_stats": final_stats,
                "final_pool_stats": pool_stats,
                "performance_summary": {
                    "block_lookup_optimized": test_results["block_lookup"]["performance_target_met"],
                    "transaction_pool_optimized": test_results["transaction_pool"]["performance_target_met"],
                    "concurrent_access_optimized": test_results["concurrent_access"]["performance_target_met"],
                    "cache_efficient": test_results["cache_efficiency"]["cache_efficient"]
                }
            }
            
            if all_tests_passed:
                logger.info("🎉 Todos os testes de performance passaram!")
            else:
                logger.warning("⚠️ Alguns testes de performance falharam")
            
            return comprehensive_result
            
        except Exception as e:
            logger.error(f"Erro no teste de performance: {e}")
            return {
                "error": str(e),
                "test_results": test_results,
                "total_execution_time": time.time() - start_time,
                "all_tests_passed": False
            }
        finally:
            # Limpar dados de teste
            blockchain_index.clear_cache()
            # Note: transaction_pool não tem método clear, mas as transações expirarão


def run_blockchain_performance_tests():
    """Função principal para executar testes de performance."""
    tester = BlockchainPerformanceTester()
    return tester.run_comprehensive_performance_test()


if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Executar testes
    results = run_blockchain_performance_tests()
    
    # Imprimir resultados
    print("\n" + "="*80)
    print("📊 RESULTADOS DOS TESTES DE PERFORMANCE DA BLOCKCHAIN")
    print("="*80)
    
    if "error" in results:
        print(f"❌ Erro: {results['error']}")
    else:
        print(f"⏱️ Tempo total de execução: {results['total_execution_time']:.2f}s")
        print(f"✅ Todos os testes passaram: {results['all_tests_passed']}")
        
        print("\n📈 RESUMO DE PERFORMANCE:")
        for test_name, result in results["test_results"].items():
            status = "✅" if result.get("performance_target_met", False) else "❌"
            print(f"   {status} {test_name}: {'PASSOU' if result.get('performance_target_met', False) else 'FALHOU'}")
        
        print("\n📊 ESTATÍSTICAS FINAIS:")
        print(f"   Índice: {results['final_index_stats']['index_size']} blocos, Cache hit rate: {results['final_index_stats']['cache_hit_rate']:.2%}")
        print(f"   Pool: {results['final_pool_stats']['pool_size']} transações, {results['final_pool_stats']['unique_addresses']} endereços únicos")
    
    print("="*80)
