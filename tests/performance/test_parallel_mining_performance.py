"""
Testes de Performance de Mineração Paralela
==========================================

Este módulo implementa testes específicos para validar a performance
da mineração paralela implementada na blockchain.

EVOLUÇÃO: Testes abrangentes para mineração paralela com threading e multiprocessing.
"""

import time
import threading
import multiprocessing
from typing import List, Dict, Any, Tuple
import statistics
import logging

from src.domain.blockchain.entities.blockchain import Blockchain
from src.domain.blockchain.entities.block import Block
from src.domain.blockchain.infrastructure.parallel_miner import (
    ParallelMiner, MiningConfig, NonceCache
)
from src.domain.transaction.entities.transaction import Transaction
from src.domain.shared.value_objects.hash_value import HashValue
from src.domain.shared.value_objects.timestamp import Timestamp
from src.domain.shared.value_objects.address import Address
from src.domain.shared.value_objects.money import Money

logger = logging.getLogger(__name__)


class ParallelMiningPerformanceTester:
    """
    Testador de performance de mineração paralela.
    
    EVOLUÇÃO: Testes específicos para mineração paralela.
    """
    
    def __init__(self):
        self.results = {}
        self.test_data = {}
        
    def generate_test_blocks(self, count: int, difficulty: int = 3) -> List[Block]:
        """Gera blocos de teste para mineração."""
        blocks = []
        
        for i in range(count):
            # Criar transações de teste
            transactions = []
            for j in range(5):  # 5 transações por bloco
                tx = Transaction.create_transaction(
                    from_address=Address("mining_test_from_" + str(i) + "_" + str(j)),
                    to_address=Address("mining_test_to_" + str(i) + "_" + str(j)),
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
                    difficulty=difficulty,
                    miner_address="mining_test_miner_" + str(i)
                )
            
            blocks.append(block)
        
        return blocks
    
    def test_parallel_mining_performance(self, blocks: List[Block], config: MiningConfig = None) -> Dict[str, Any]:
        """
        Testa performance de mineração paralela.
        
        EVOLUÇÃO: Validação de mineração paralela vs sequencial.
        """
        logger.info("🧪 Testando performance de mineração paralela...")
        
        if not config:
            config = MiningConfig(max_threads=4, max_processes=2)
        
        miner = ParallelMiner(config)
        
        # Teste de mineração paralela
        parallel_times = []
        successful_mines = 0
        
        for block in blocks[:5]:  # Testar apenas 5 blocos para não demorar muito
            start_time = time.time()
            
            result = miner.mine_block_parallel(
                block=block,
                transactions=block.transactions,
                miner_address="test_miner"
            )
            
            end_time = time.time()
            
            if result and result.success:
                parallel_times.append(end_time - start_time)
                successful_mines += 1
                logger.info(f"Bloco {block.height} minerado: {end_time - start_time:.2f}s")
            else:
                logger.warning(f"Falha na mineração do bloco {block.height}")
        
        # Calcular estatísticas
        if parallel_times:
            parallel_stats = {
                "min_time": min(parallel_times),
                "max_time": max(parallel_times),
                "avg_time": statistics.mean(parallel_times),
                "median_time": statistics.median(parallel_times),
                "successful_mines": successful_mines,
                "total_blocks_tested": len(blocks[:5])
            }
        else:
            parallel_stats = {
                "min_time": 0,
                "max_time": 0,
                "avg_time": 0,
                "median_time": 0,
                "successful_mines": 0,
                "total_blocks_tested": len(blocks[:5])
            }
        
        # Obter estatísticas do minerador
        miner_stats = miner.get_mining_statistics()
        
        result = {
            "parallel_stats": parallel_stats,
            "miner_stats": miner_stats,
            "config_used": {
                "max_threads": config.max_threads,
                "max_processes": config.max_processes,
                "batch_size": config.batch_size,
                "timeout_seconds": config.timeout_seconds
            },
            "performance_target_met": parallel_stats["avg_time"] < 10.0 and successful_mines > 0
        }
        
        logger.info(f"✅ Performance de mineração paralela: Avg={parallel_stats['avg_time']:.2f}s, Sucessos={successful_mines}")
        
        return result
    
    def test_mining_scalability(self, base_block: Block) -> Dict[str, Any]:
        """
        Testa escalabilidade da mineração paralela.
        
        EVOLUÇÃO: Validação de escalabilidade com diferentes números de threads/processos.
        """
        logger.info("🧪 Testando escalabilidade de mineração...")
        
        scalability_results = {}
        
        # Testar diferentes configurações
        configs = [
            MiningConfig(max_threads=1, max_processes=0),  # Sequencial
            MiningConfig(max_threads=2, max_processes=0),  # 2 threads
            MiningConfig(max_threads=4, max_processes=0),  # 4 threads
            MiningConfig(max_threads=8, max_processes=0),  # 8 threads
            MiningConfig(max_threads=4, max_processes=2),  # Híbrido
        ]
        
        for config in configs:
            miner = ParallelMiner(config)
            
            # Testar mineração com esta configuração
            start_time = time.time()
            result = miner.mine_block_parallel(
                block=base_block,
                transactions=base_block.transactions,
                miner_address="scalability_test_miner"
            )
            end_time = time.time()
            
            mining_time = end_time - start_time
            success = result is not None and result.success
            
            config_key = f"{config.max_threads}t_{config.max_processes}p"
            scalability_results[config_key] = {
                "mining_time": mining_time,
                "success": success,
                "config": {
                    "max_threads": config.max_threads,
                    "max_processes": config.max_processes
                }
            }
            
            logger.info(f"Config {config_key}: {mining_time:.2f}s, Success: {success}")
        
        # Calcular melhorias de performance
        sequential_time = scalability_results.get("1t_0p", {}).get("mining_time", 0)
        improvements = {}
        
        for config_key, result in scalability_results.items():
            if config_key != "1t_0p" and sequential_time > 0:
                improvement = (sequential_time - result["mining_time"]) / sequential_time
                improvements[config_key] = improvement
        
        result = {
            "scalability_results": scalability_results,
            "performance_improvements": improvements,
            "best_config": max(improvements.items(), key=lambda x: x[1]) if improvements else ("1t_0p", 0),
            "scalability_target_met": any(imp > 0.1 for imp in improvements.values())
        }
        
        logger.info(f"✅ Escalabilidade: Melhor configuração = {result['best_config'][0]} ({result['best_config'][1]:.2%} melhoria)")
        
        return result
    
    def test_nonce_cache_efficiency(self, blocks: List[Block]) -> Dict[str, Any]:
        """
        Testa eficiência do cache de nonces.
        
        EVOLUÇÃO: Validação de cache de nonces para otimização.
        """
        logger.info("🧪 Testando eficiência do cache de nonces...")
        
        cache = NonceCache(max_size=1000)
        
        # Teste 1: Cache vazio
        cache.clear_cache()
        empty_cache_times = []
        
        for block in blocks[:3]:
            start_time = time.time()
            nonces = cache.get_candidate_nonces("test_data", block.difficulty)
            end_time = time.time()
            
            empty_cache_times.append(end_time - start_time)
        
        # Teste 2: Cache populado
        # Simular sucessos para popular cache
        for difficulty in [1, 2, 3, 4, 5]:
            cache.record_success(difficulty, difficulty * 1000)
        
        populated_cache_times = []
        
        for block in blocks[:3]:
            start_time = time.time()
            nonces = cache.get_candidate_nonces("test_data", block.difficulty)
            end_time = time.time()
            
            populated_cache_times.append(end_time - start_time)
        
        # Calcular estatísticas
        empty_cache_avg = statistics.mean(empty_cache_times) if empty_cache_times else 0
        populated_cache_avg = statistics.mean(populated_cache_times) if populated_cache_times else 0
        
        cache_efficiency = {
            "empty_cache_avg_time": empty_cache_avg,
            "populated_cache_avg_time": populated_cache_avg,
            "cache_size": len(cache.cache),
            "success_patterns": len(cache.success_patterns),
            "performance_improvement": (empty_cache_avg - populated_cache_avg) / empty_cache_avg if empty_cache_avg > 0 else 0
        }
        
        result = {
            "cache_efficiency": cache_efficiency,
            "cache_effective": cache_efficiency["performance_improvement"] > 0.1
        }
        
        logger.info(f"✅ Eficiência do cache: Melhoria={cache_efficiency['performance_improvement']:.2%}")
        
        return result
    
    def test_concurrent_mining(self, base_block: Block) -> Dict[str, Any]:
        """
        Testa mineração concorrente com múltiplas threads.
        
        EVOLUÇÃO: Validação de thread safety e performance concorrente.
        """
        logger.info("🧪 Testando mineração concorrente...")
        
        config = MiningConfig(max_threads=4, max_processes=2)
        miner = ParallelMiner(config)
        
        # Função para thread de mineração
        def mining_thread(thread_id: int, results: List[Dict]):
            start_time = time.time()
            
            result = miner.mine_block_parallel(
                block=base_block,
                transactions=base_block.transactions,
                miner_address=f"concurrent_miner_{thread_id}"
            )
            
            end_time = time.time()
            
            results.append({
                "thread_id": thread_id,
                "mining_time": end_time - start_time,
                "success": result is not None and result.success,
                "nonce": result.nonce if result and result.success else None
            })
        
        # Executar mineração concorrente
        num_threads = 3
        results = []
        threads = []
        
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=mining_thread, args=(i, results))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        
        # Calcular estatísticas
        successful_threads = [r for r in results if r["success"]]
        concurrent_stats = {
            "total_threads": num_threads,
            "successful_threads": len(successful_threads),
            "total_execution_time": total_time,
            "mining_times": [r["mining_time"] for r in results],
            "avg_mining_time": statistics.mean([r["mining_time"] for r in results]) if results else 0,
            "thread_safety_maintained": len(set(r["nonce"] for r in successful_threads if r["nonce"])) == len(successful_threads)
        }
        
        result = {
            "concurrent_stats": concurrent_stats,
            "concurrent_performance_target_met": concurrent_stats["successful_threads"] > 0 and concurrent_stats["thread_safety_maintained"]
        }
        
        logger.info(f"✅ Mineração concorrente: {concurrent_stats['successful_threads']}/{num_threads} sucessos, Thread safety: {concurrent_stats['thread_safety_maintained']}")
        
        return result
    
    def test_mining_config_optimization(self, base_block: Block) -> Dict[str, Any]:
        """
        Testa otimização automática de configuração de mineração.
        
        EVOLUÇÃO: Validação de otimização automática de configuração.
        """
        logger.info("🧪 Testando otimização de configuração de mineração...")
        
        # Configuração inicial subótima
        initial_config = MiningConfig(max_threads=1, max_processes=0, cache_size=100)
        miner = ParallelMiner(initial_config)
        
        # Simular algumas minerações para gerar estatísticas
        for _ in range(3):
            miner.mine_block_parallel(
                block=base_block,
                transactions=base_block.transactions,
                miner_address="optimization_test_miner"
            )
        
        # Obter configuração inicial
        initial_stats = miner.get_mining_statistics()
        
        # Executar otimização
        optimization_result = miner.optimize_mining_config()
        
        # Obter configuração após otimização
        optimized_stats = miner.get_mining_statistics()
        
        result = {
            "initial_config": {
                "max_threads": initial_config.max_threads,
                "max_processes": initial_config.max_processes,
                "cache_size": initial_config.cache_size
            },
            "optimized_config": optimization_result["current_config"],
            "optimizations_applied": optimization_result["optimizations_applied"],
            "initial_stats": initial_stats,
            "optimized_stats": optimized_stats,
            "optimization_effective": len(optimization_result["optimizations_applied"]) > 0
        }
        
        logger.info(f"✅ Otimização de configuração: {len(optimization_result['optimizations_applied'])} otimizações aplicadas")
        
        return result
    
    def run_comprehensive_mining_test(self) -> Dict[str, Any]:
        """
        Executa teste abrangente de mineração paralela.
        
        EVOLUÇÃO: Teste completo de todas as funcionalidades de mineração paralela.
        """
        logger.info("🚀 Iniciando teste abrangente de mineração paralela...")
        
        start_time = time.time()
        
        # Gerar dados de teste
        test_blocks = self.generate_test_blocks(10, difficulty=3)
        base_block = test_blocks[0]
        
        # Executar testes
        test_results = {}
        
        try:
            # Teste de performance de mineração paralela
            test_results["parallel_mining"] = self.test_parallel_mining_performance(test_blocks)
            
            # Teste de escalabilidade
            test_results["scalability"] = self.test_mining_scalability(base_block)
            
            # Teste de eficiência do cache
            test_results["cache_efficiency"] = self.test_nonce_cache_efficiency(test_blocks)
            
            # Teste de mineração concorrente
            test_results["concurrent_mining"] = self.test_concurrent_mining(base_block)
            
            # Teste de otimização de configuração
            test_results["config_optimization"] = self.test_mining_config_optimization(base_block)
            
            # Calcular estatísticas gerais
            total_time = time.time() - start_time
            
            # Verificar se todos os testes passaram
            all_tests_passed = all(
                result.get("performance_target_met", False) or 
                result.get("scalability_target_met", False) or
                result.get("cache_effective", False) or
                result.get("concurrent_performance_target_met", False) or
                result.get("optimization_effective", False)
                for result in test_results.values()
            )
            
            comprehensive_result = {
                "test_results": test_results,
                "total_execution_time": total_time,
                "all_tests_passed": all_tests_passed,
                "performance_summary": {
                    "parallel_mining_optimized": test_results["parallel_mining"]["performance_target_met"],
                    "scalability_improved": test_results["scalability"]["scalability_target_met"],
                    "cache_efficient": test_results["cache_efficiency"]["cache_effective"],
                    "concurrent_safe": test_results["concurrent_mining"]["concurrent_performance_target_met"],
                    "config_optimized": test_results["config_optimization"]["optimization_effective"]
                }
            }
            
            if all_tests_passed:
                logger.info("🎉 Todos os testes de mineração paralela passaram!")
            else:
                logger.warning("⚠️ Alguns testes de mineração paralela falharam")
            
            return comprehensive_result
            
        except Exception as e:
            logger.error(f"Erro no teste de mineração paralela: {e}")
            return {
                "error": str(e),
                "test_results": test_results,
                "total_execution_time": time.time() - start_time,
                "all_tests_passed": False
            }


def run_parallel_mining_performance_tests():
    """Função principal para executar testes de mineração paralela."""
    tester = ParallelMiningPerformanceTester()
    return tester.run_comprehensive_mining_test()


if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Executar testes
    results = run_parallel_mining_performance_tests()
    
    # Imprimir resultados
    print("\n" + "="*80)
    print("📊 RESULTADOS DOS TESTES DE MINERAÇÃO PARALELA")
    print("="*80)
    
    if "error" in results:
        print(f"❌ Erro: {results['error']}")
    else:
        print(f"⏱️ Tempo total de execução: {results['total_execution_time']:.2f}s")
        print(f"✅ Todos os testes passaram: {results['all_tests_passed']}")
        
        print("\n📈 RESUMO DE PERFORMANCE:")
        for test_name, result in results["test_results"].items():
            status = "✅" if any(result.get(key, False) for key in ["performance_target_met", "scalability_target_met", "cache_effective", "concurrent_performance_target_met", "optimization_effective"]) else "❌"
            print(f"   {status} {test_name}: {'PASSOU' if any(result.get(key, False) for key in ['performance_target_met', 'scalability_target_met', 'cache_effective', 'concurrent_performance_target_met', 'optimization_effective']) else 'FALHOU'}")
        
        print("\n📊 RESUMO DE OTIMIZAÇÕES:")
        summary = results["performance_summary"]
        for key, value in summary.items():
            status = "✅" if value else "❌"
            print(f"   {status} {key}: {'SIM' if value else 'NÃO'}")
    
    print("="*80)
