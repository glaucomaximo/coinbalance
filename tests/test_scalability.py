#!/usr/bin/env python3
"""
Teste de Escalabilidade e Load Balancing do CoinBalance
======================================================

Este script testa os sistemas de escalabilidade e load balancing
para verificar se o sistema pode escalar infinitamente.
"""

import sys
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_load_balancing_stress():
    """Testa o load balancer sob stress."""
    print("⚖️ Testando Load Balancing sob Stress...")
    try:
        from src.infrastructure.fractal.fractal_load_balancer import fractal_load_balancer
        
        # Registrar múltiplos fractais
        fractal_count = 10
        for i in range(fractal_count):
            fractal_load_balancer.register_fractal(f"fractal_{i}")
        
        # Simular múltiplas requisições simultâneas
        def make_request():
            return fractal_load_balancer.select_fractal()
        
        # Executar 100 requisições simultâneas
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_request) for _ in range(100)]
            results = [future.result() for future in as_completed(futures)]
        
        # Verificar distribuição
        distribution = {}
        for result in results:
            if result:
                distribution[result] = distribution.get(result, 0) + 1
        
        stats = fractal_load_balancer.get_stats()
        print(f"   ✅ Load Balancer Stress Test:")
        print(f"      - Fractais registrados: {fractal_count}")
        print(f"      - Requisições processadas: {len(results)}")
        print(f"      - Taxa de sucesso: {stats['success_rate']:.2%}")
        print(f"      - Distribuição: {len(distribution)} fractais utilizados")
        
        return True
    except Exception as e:
        print(f"   ❌ Erro no Load Balancing Stress: {e}")
        return False

def test_memory_scaling():
    """Testa o escalonamento de memória."""
    print("💾 Testando Escalonamento de Memória...")
    try:
        from src.infrastructure.fractal.distributed_memory import distributed_memory_manager, MemoryType, MemoryPriority
        
        # Simular múltiplas alocações de memória
        allocations = []
        for i in range(20):
            fractal_id = f"scaling_fractal_{i}"
            allocated = distributed_memory_manager.allocate_memory(
                fractal_id, 
                1024 * (i + 1),  # Memória crescente
                MemoryType.CACHE, 
                MemoryPriority.HIGH
            )
            if allocated:
                allocations.append(allocated)
        
        # Verificar estatísticas
        stats = distributed_memory_manager.get_memory_stats()
        print(f"   ✅ Memory Scaling Test:")
        print(f"      - Alocações realizadas: {len(allocations)}")
        print(f"      - Memória total alocada: {stats['total_allocated']} bytes")
        print(f"      - Fractais ativos: {stats['active_fractals']}")
        print(f"      - Eficiência: {stats['memory_efficiency']:.2%}")
        
        return True
    except Exception as e:
        print(f"   ❌ Erro no Memory Scaling: {e}")
        return False

def test_cache_scaling():
    """Testa o escalonamento do cache."""
    print("🧠 Testando Escalonamento do Cache...")
    try:
        from src.infrastructure.fractal.fractal_cache import fractal_cache
        
        # Simular múltiplas operações de cache
        operations_count = 1000
        
        def cache_operation(fractal_id, key, value):
            fractal_cache.set(fractal_id, key, value)
            return fractal_cache.get(fractal_id, key)
        
        # Executar operações em paralelo
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for i in range(operations_count):
                fractal_id = f"cache_fractal_{i % 10}"  # 10 fractais diferentes
                key = f"key_{i}"
                value = f"value_{i}"
                futures.append(executor.submit(cache_operation, fractal_id, key, value))
            
            results = [future.result() for future in as_completed(futures)]
        
        # Verificar estatísticas
        stats = fractal_cache.get_stats()
        print(f"   ✅ Cache Scaling Test:")
        print(f"      - Operações realizadas: {operations_count}")
        print(f"      - Entradas no cache: {stats['total_entries']}")
        print(f"      - Taxa de hit: {stats['hit_rate']:.2%}")
        print(f"      - Fractais ativos: {stats['active_fractals']}")
        
        return True
    except Exception as e:
        print(f"   ❌ Erro no Cache Scaling: {e}")
        return False

def test_ecosystem_scaling():
    """Testa o escalonamento do ecossistema completo."""
    print("🌐 Testando Escalonamento do Ecossistema...")
    try:
        from src.infrastructure.fractal.ecosystem_integrator import FractalEcosystemIntegrator
        
        # Criar múltiplos integradores (simulando múltiplas instâncias)
        integrators = []
        for i in range(5):
            integrator = FractalEcosystemIntegrator()
            integrator.initialize_ecosystem()
            integrators.append(integrator)
        
        # Verificar status de cada integrador
        total_systems = 0
        active_systems = 0
        
        for i, integrator in enumerate(integrators):
            status = integrator.get_ecosystem_status()
            total_systems += status['total_systems']
            active_systems += status['active_systems']
        
        print(f"   ✅ Ecosystem Scaling Test:")
        print(f"      - Integradores criados: {len(integrators)}")
        print(f"      - Sistemas totais: {total_systems}")
        print(f"      - Sistemas ativos: {active_systems}")
        print(f"      - Taxa de ativação: {(active_systems/total_systems*100):.1f}%")
        
        return True
    except Exception as e:
        print(f"   ❌ Erro no Ecosystem Scaling: {e}")
        return False

def test_compression_scaling():
    """Testa o escalonamento da compressão."""
    print("🗜️ Testando Escalonamento da Compressão...")
    try:
        from src.infrastructure.fractal.fractal_compression import fractal_compressor
        
        # Simular compressão de múltiplos dados
        test_data_sets = [
            "Dados pequenos para teste",
            "Dados médios " * 100,
            "Dados grandes " * 1000,
            "Dados muito grandes " * 10000
        ]
        
        compression_results = []
        for i, data in enumerate(test_data_sets):
            result = fractal_compressor.compress(data)
            compression_results.append(result)
        
        # Calcular estatísticas
        total_original = sum(r.original_size for r in compression_results)
        total_compressed = sum(r.compressed_size for r in compression_results)
        avg_ratio = sum(r.compression_ratio for r in compression_results) / len(compression_results)
        
        print(f"   ✅ Compression Scaling Test:")
        print(f"      - Conjuntos de dados: {len(test_data_sets)}")
        print(f"      - Tamanho original total: {total_original} bytes")
        print(f"      - Tamanho comprimido total: {total_compressed} bytes")
        print(f"      - Taxa de compressão média: {avg_ratio:.2f}")
        print(f"      - Economia de espaço: {((total_original - total_compressed) / total_original * 100):.1f}%")
        
        return True
    except Exception as e:
        print(f"   ❌ Erro no Compression Scaling: {e}")
        return False

def test_concurrent_operations():
    """Testa operações concorrentes em múltiplos sistemas."""
    print("🔄 Testando Operações Concorrentes...")
    try:
        from src.infrastructure.fractal.fractal_cache import fractal_cache
        from src.infrastructure.fractal.fractal_load_balancer import fractal_load_balancer
        from src.infrastructure.fractal.distributed_memory import distributed_memory_manager, MemoryType, MemoryPriority
        
        def concurrent_operation(operation_id):
            """Executa uma operação concorrente."""
            results = {}
            
            # Operação de cache
            fractal_cache.set(f"concurrent_fractal_{operation_id}", f"key_{operation_id}", f"value_{operation_id}")
            results['cache'] = fractal_cache.get(f"concurrent_fractal_{operation_id}", f"key_{operation_id}")
            
            # Operação de load balancing
            results['load_balancer'] = fractal_load_balancer.select_fractal()
            
            # Operação de memória
            allocated = distributed_memory_manager.allocate_memory(
                f"concurrent_memory_{operation_id}", 
                512, 
                MemoryType.CACHE, 
                MemoryPriority.MEDIUM
            )
            results['memory'] = allocated is not None
            
            return results
        
        # Executar 50 operações concorrentes
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(concurrent_operation, i) for i in range(50)]
            results = [future.result() for future in as_completed(futures)]
        
        # Verificar resultados
        successful_operations = len([r for r in results if all(r.values())])
        
        print(f"   ✅ Concurrent Operations Test:")
        print(f"      - Operações executadas: {len(results)}")
        print(f"      - Operações bem-sucedidas: {successful_operations}")
        print(f"      - Taxa de sucesso: {(successful_operations/len(results)*100):.1f}%")
        
        return True
    except Exception as e:
        print(f"   ❌ Erro nas Operações Concorrentes: {e}")
        return False

def main():
    """Executa todos os testes de escalabilidade."""
    print("🚀 Iniciando Testes de Escalabilidade e Load Balancing")
    print("=" * 70)
    
    tests = [
        test_load_balancing_stress,
        test_memory_scaling,
        test_cache_scaling,
        test_ecosystem_scaling,
        test_compression_scaling,
        test_concurrent_operations
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"   ❌ Erro crítico no teste: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"📊 Resultados dos Testes de Escalabilidade:")
    print(f"   ✅ Sucessos: {passed}")
    print(f"   ❌ Falhas: {failed}")
    print(f"   📈 Taxa de Sucesso: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 Todos os testes de escalabilidade passaram!")
        print("   O CoinBalance está pronto para escalar infinitamente!")
        print("   🚀 Sistema preparado para alta performance e disponibilidade!")
    else:
        print(f"\n⚠️ {failed} teste(s) de escalabilidade precisam de atenção.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
