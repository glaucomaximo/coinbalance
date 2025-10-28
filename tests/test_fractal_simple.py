#!/usr/bin/env python3
"""
Teste Simplificado dos Sistemas Fractais do CoinBalance
======================================================

Este script testa os sistemas fractais de forma simplificada para verificar
se estão funcionando corretamente.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_fractal_cache():
    """Testa o sistema de cache fractal."""
    print("🧠 Testando Fractal Cache...")
    try:
        from src.infrastructure.fractal.fractal_cache import fractal_cache
        
        # Testar operações básicas
        fractal_cache.set("test_fractal", "test_key", "test_value")
        value = fractal_cache.get("test_fractal", "test_key")
        assert value == "test_value", f"Expected 'test_value', got {value}"
        
        status = fractal_cache.get_stats()
        print(f"   ✅ Cache Status: {status['total_entries']} entradas")
        return True
    except Exception as e:
        print(f"   ❌ Erro no Cache: {e}")
        return False

def test_fractal_load_balancer():
    """Testa o sistema de load balancing fractal."""
    print("⚖️ Testando Fractal Load Balancer...")
    try:
        from src.infrastructure.fractal.fractal_load_balancer import fractal_load_balancer
        
        # Registrar instâncias fractais
        fractal_load_balancer.register_fractal("fractal_1")
        fractal_load_balancer.register_fractal("fractal_2")
        
        # Obter próxima instância
        instance = fractal_load_balancer.select_fractal()
        assert instance is not None, "Nenhuma instância disponível"
        
        status = fractal_load_balancer.get_stats()
        print(f"   ✅ Load Balancer Status: {status['active_fractals']} fractais registrados")
        return True
    except Exception as e:
        print(f"   ❌ Erro no Load Balancer: {e}")
        return False

def test_fractal_compression():
    """Testa o sistema de compressão fractal."""
    print("🗜️ Testando Fractal Compression...")
    try:
        from src.infrastructure.fractal.fractal_compression import fractal_compressor, CompressionAlgorithm
        
        # Testar compressão
        test_data = "Este é um teste de compressão fractal para o CoinBalance"
        compressed_result = fractal_compressor.compress(test_data)
        assert compressed_result is not None, "Compressão falhou"
        
        print(f"   ✅ Compressão: {compressed_result.original_size} -> {compressed_result.compressed_size} bytes (ratio: {compressed_result.compression_ratio:.2f})")
        return True
    except Exception as e:
        print(f"   ❌ Erro na Compressão: {e}")
        return False

def test_distributed_memory():
    """Testa o sistema de memória distribuída."""
    print("💾 Testando Distributed Memory...")
    try:
        from src.infrastructure.fractal.distributed_memory import distributed_memory_manager, MemoryType, MemoryPriority
        
        # Testar alocação de memória
        fractal_id = "test_fractal"
        allocated = distributed_memory_manager.allocate_memory(fractal_id, 1024, MemoryType.CACHE, MemoryPriority.MEDIUM)
        assert allocated, "Falha na alocação de memória"
        
        # Verificar uso de memória
        usage = distributed_memory_manager.get_memory_stats()
        assert usage['total_allocated'] > 0, "Memória não foi alocada"
        
        print(f"   ✅ Memória Distribuída: {usage['total_allocated']} bytes alocados")
        return True
    except Exception as e:
        print(f"   ❌ Erro na Memória Distribuída: {e}")
        return False

def test_ecosystem_integrator():
    """Testa o integrador do ecossistema fractal."""
    print("🌐 Testando Ecosystem Integrator...")
    try:
        from src.infrastructure.fractal.ecosystem_integrator import FractalEcosystemIntegrator
        
        # Criar integrador
        integrator = FractalEcosystemIntegrator()
        
        # Inicializar ecossistema
        init_result = integrator.initialize_ecosystem()
        assert init_result, "Inicialização do ecossistema falhou"
        
        # Obter status do ecossistema
        status = integrator.get_ecosystem_status()
        assert status is not None, "Status do ecossistema falhou"
        
        print(f"   ✅ Ecosystem Integrator: {status['active_systems']}/{status['total_systems']} sistemas ativos")
        return True
    except Exception as e:
        print(f"   ❌ Erro no Ecosystem Integrator: {e}")
        return False

def main():
    """Executa os testes principais dos sistemas fractais."""
    print("🚀 Iniciando Testes Simplificados dos Sistemas Fractais")
    print("=" * 60)
    
    tests = [
        test_fractal_cache,
        test_fractal_load_balancer,
        test_fractal_compression,
        test_distributed_memory,
        test_ecosystem_integrator
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
    
    print("=" * 60)
    print(f"📊 Resultados dos Testes:")
    print(f"   ✅ Sucessos: {passed}")
    print(f"   ❌ Falhas: {failed}")
    print(f"   📈 Taxa de Sucesso: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 Todos os sistemas fractais principais estão funcionando!")
    else:
        print(f"\n⚠️ {failed} sistema(s) precisam de atenção.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
