#!/usr/bin/env python3
"""
Teste dos Sistemas Fractais do CoinBalance
==========================================

Este script testa todos os sistemas fractais implementados para verificar
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
        
        status = fractal_cache.get_cache_status()
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
        
        status = fractal_load_balancer.get_load_balancer_status()
        print(f"   ✅ Load Balancer Status: {status['registered_fractals']} fractais registrados")
        return True
    except Exception as e:
        print(f"   ❌ Erro no Load Balancer: {e}")
        return False

def test_fractal_compression():
    """Testa o sistema de compressão fractal."""
    print("🗜️ Testando Fractal Compression...")
    try:
        from src.infrastructure.fractal.fractal_compression import fractal_compressor
        
        # Testar compressão
        test_data = "Este é um teste de compressão fractal para o CoinBalance"
        compressed = fractal_compressor.compress_data(test_data)
        assert compressed is not None, "Compressão falhou"
        
        # Testar descompressão
        decompressed = fractal_compressor.decompress_data(compressed)
        assert decompressed == test_data, f"Descompressão falhou: {decompressed}"
        
        print(f"   ✅ Compressão: {len(test_data)} -> {len(compressed)} bytes")
        return True
    except Exception as e:
        print(f"   ❌ Erro na Compressão: {e}")
        return False

def test_distributed_memory():
    """Testa o sistema de memória distribuída."""
    print("💾 Testando Distributed Memory...")
    try:
        from src.infrastructure.fractal.distributed_memory import distributed_memory_manager
        
        # Testar alocação de memória
        fractal_id = "test_fractal"
        allocated = distributed_memory_manager.allocate_memory(fractal_id, 1024)
        assert allocated, "Falha na alocação de memória"
        
        # Verificar uso de memória
        usage = distributed_memory_manager.get_memory_usage()
        assert usage['total_allocated'] > 0, "Memória não foi alocada"
        
        print(f"   ✅ Memória Distribuída: {usage['total_allocated']} bytes alocados")
        return True
    except Exception as e:
        print(f"   ❌ Erro na Memória Distribuída: {e}")
        return False

def test_fractal_ml():
    """Testa o sistema de machine learning fractal."""
    print("🤖 Testando Fractal ML...")
    try:
        from src.infrastructure.fractal.fractal_ml import fractal_ml_system
        
        # Registrar modelo
        model_id = "test_model"
        fractal_ml_system.register_model(model_id, "classification", "Modelo de teste")
        
        # Adicionar fonte de dados
        fractal_ml_system.add_data_source("test_data", [1, 2, 3, 4, 5])
        
        # Treinar modelo
        fractal_ml_system.train_model(model_id)
        
        # Fazer predição
        prediction = fractal_ml_system.predict(model_id, [6, 7, 8])
        assert prediction is not None, "Predição falhou"
        
        status = fractal_ml_system.get_model_status()
        print(f"   ✅ ML Status: {status['registered_models']} modelos registrados")
        return True
    except Exception as e:
        print(f"   ❌ Erro no ML: {e}")
        return False

def test_failure_prediction():
    """Testa o sistema de predição de falhas."""
    print("🔮 Testando Failure Prediction...")
    try:
        from src.infrastructure.fractal.failure_prediction import proactive_failure_predictor
        
        # Adicionar métricas
        proactive_failure_predictor.add_metric("cpu_usage", 75.0, 80.0)
        proactive_failure_predictor.add_metric("memory_usage", 60.0, 85.0)
        
        # Analisar métricas
        analysis = proactive_failure_predictor.analyze_metrics()
        assert analysis is not None, "Análise de métricas falhou"
        
        # Predizer falha
        prediction = proactive_failure_predictor.predict_failure()
        assert prediction is not None, "Predição de falha falhou"
        
        status = proactive_failure_predictor.get_prediction_status()
        print(f"   ✅ Failure Prediction: {status['monitored_metrics']} métricas monitoradas")
        return True
    except Exception as e:
        print(f"   ❌ Erro na Predição de Falhas: {e}")
        return False

def test_genetic_optimization():
    """Testa o sistema de otimização genética."""
    print("🧬 Testando Genetic Optimization...")
    try:
        from src.infrastructure.fractal.genetic_optimization import fractal_genetic_optimizer
        
        # Inicializar população
        population = fractal_genetic_optimizer.initialize_population(10)
        assert len(population) == 10, "População não foi inicializada corretamente"
        
        # Avaliar população
        evaluated = fractal_genetic_optimizer.evaluate_population(population)
        assert len(evaluated) == 10, "Avaliação da população falhou"
        
        # Evoluir
        evolved = fractal_genetic_optimizer.evolve(population, generations=1)
        assert len(evolved) == 10, "Evolução falhou"
        
        print(f"   ✅ Genetic Optimization: População de {len(population)} indivíduos")
        return True
    except Exception as e:
        print(f"   ❌ Erro na Otimização Genética: {e}")
        return False

def test_sentiment_analysis():
    """Testa o sistema de análise de sentimento."""
    print("😊 Testando Sentiment Analysis...")
    try:
        from src.infrastructure.fractal.sentiment_analysis import fractal_sentiment_analyzer
        
        # Analisar sentimento
        sentiment = fractal_sentiment_analyzer.analyze_sentiment("Este sistema é incrível!")
        assert sentiment is not None, "Análise de sentimento falhou"
        
        # Obter sentimento geral
        overall = fractal_sentiment_analyzer.get_overall_sentiment()
        assert overall is not None, "Sentimento geral falhou"
        
        # Obter tendências
        trends = fractal_sentiment_analyzer.get_sentiment_trends()
        assert trends is not None, "Tendências de sentimento falharam"
        
        print(f"   ✅ Sentiment Analysis: Sentimento geral {overall['overall_sentiment']}")
        return True
    except Exception as e:
        print(f"   ❌ Erro na Análise de Sentimento: {e}")
        return False

def test_geographic_distribution():
    """Testa o sistema de distribuição geográfica."""
    print("🌍 Testando Geographic Distribution...")
    try:
        from src.infrastructure.fractal.geographic_distribution import geographic_fractal_distributor
        
        # Registrar fractais
        geographic_fractal_distributor.register_fractal("fractal_br", "São Paulo", -23.5505, -46.6333)
        geographic_fractal_distributor.register_fractal("fractal_us", "New York", 40.7128, -74.0060)
        
        # Obter fractal mais próximo
        closest = geographic_fractal_distributor.get_closest_fractal(-23.5505, -46.6333)
        assert closest is not None, "Fractal mais próximo não encontrado"
        
        # Obter mapa de distribuição
        distribution_map = geographic_fractal_distributor.get_distribution_map()
        assert distribution_map is not None, "Mapa de distribuição falhou"
        
        print(f"   ✅ Geographic Distribution: {len(distribution_map['fractals'])} fractais registrados")
        return True
    except Exception as e:
        print(f"   ❌ Erro na Distribuição Geográfica: {e}")
        return False

def test_cross_region_replication():
    """Testa o sistema de replicação cross-region."""
    print("🔄 Testando Cross-Region Replication...")
    try:
        from src.infrastructure.fractal.cross_region_replication import cross_region_replicator
        
        # Replicar fractal
        replication_result = cross_region_replicator.replicate_fractal("fractal_br", "us-east-1")
        assert replication_result is not None, "Replicação falhou"
        
        # Sincronizar dados
        sync_result = cross_region_replicator.sync_data("fractal_br", "fractal_us")
        assert sync_result is not None, "Sincronização falhou"
        
        # Obter status de replicação
        status = cross_region_replicator.get_replication_status()
        assert status is not None, "Status de replicação falhou"
        
        print(f"   ✅ Cross-Region Replication: {status['active_replications']} replicações ativas")
        return True
    except Exception as e:
        print(f"   ❌ Erro na Replicação Cross-Region: {e}")
        return False

def test_intelligent_sharding():
    """Testa o sistema de sharding inteligente."""
    print("🔀 Testando Intelligent Sharding...")
    try:
        from src.infrastructure.fractal.intelligent_sharding import intelligent_sharding_system
        
        # Criar shard
        shard = intelligent_sharding_system.create_shard("shard_1", "hash_based")
        assert shard is not None, "Criação de shard falhou"
        
        # Obter shard para dados
        shard_for_data = intelligent_sharding_system.get_shard_for_data("test_data_123")
        assert shard_for_data is not None, "Shard para dados não encontrado"
        
        # Rebalancear shards
        rebalance_result = intelligent_sharding_system.rebalance_shards()
        assert rebalance_result is not None, "Rebalanceamento falhou"
        
        # Obter status de sharding
        status = intelligent_sharding_system.get_sharding_status()
        assert status is not None, "Status de sharding falhou"
        
        print(f"   ✅ Intelligent Sharding: {status['total_shards']} shards ativos")
        return True
    except Exception as e:
        print(f"   ❌ Erro no Sharding Inteligente: {e}")
        return False

def test_demand_scaling():
    """Testa o sistema de auto-scaling baseado em demanda."""
    print("📈 Testando Demand-Based Auto-Scaling...")
    try:
        from src.infrastructure.fractal.demand_scaling import demand_based_auto_scaler
        
        # Atualizar métricas
        demand_based_auto_scaler.update_metrics("cpu_usage", 85.0)
        demand_based_auto_scaler.update_metrics("memory_usage", 75.0)
        demand_based_auto_scaler.update_metrics("request_rate", 1000)
        
        # Avaliar necessidades de escala
        scaling_needs = demand_based_auto_scaler.evaluate_scaling_needs()
        assert scaling_needs is not None, "Avaliação de escala falhou"
        
        # Escalar para cima
        scale_up_result = demand_based_auto_scaler.scale_up()
        assert scale_up_result is not None, "Escala para cima falhou"
        
        # Obter status do scaler
        status = demand_based_auto_scaler.get_scaler_status()
        assert status is not None, "Status do scaler falhou"
        
        print(f"   ✅ Auto-Scaling: {status['active_instances']} instâncias ativas")
        return True
    except Exception as e:
        print(f"   ❌ Erro no Auto-Scaling: {e}")
        return False

def test_cascading_failure_manager():
    """Testa o sistema de gerenciamento de falhas em cascata."""
    print("🛡️ Testando Cascading Failure Manager...")
    try:
        from src.infrastructure.fractal.cascading_failure_manager import cascading_failure_manager
        
        # Registrar dependência entre sistemas
        cascading_failure_manager.register_system_dependency("cache", ["load_balancer"])
        
        # Reportar falha
        failure_result = cascading_failure_manager.report_failure("load_balancer", "HIGH")
        assert failure_result is not None, "Reporte de falha falhou"
        
        # Ativar contenção
        containment_result = cascading_failure_manager.activate_containment("cache")
        assert containment_result is not None, "Ativação de contenção falhou"
        
        print(f"   ✅ Cascading Failure Manager: Sistema de proteção ativo")
        return True
    except Exception as e:
        print(f"   ❌ Erro no Cascading Failure Manager: {e}")
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
        
        # Obter consciência do ecossistema
        consciousness = integrator.get_ecosystem_consciousness()
        assert consciousness is not None, "Consciência do ecossistema falhou"
        
        print(f"   ✅ Ecosystem Integrator: {status['active_systems']}/{status['total_systems']} sistemas ativos")
        print(f"   🧠 Consciência do Ecossistema: {consciousness['overall_consciousness']:.2f}")
        return True
    except Exception as e:
        print(f"   ❌ Erro no Ecosystem Integrator: {e}")
        return False

def main():
    """Executa todos os testes dos sistemas fractais."""
    print("🚀 Iniciando Testes dos Sistemas Fractais do CoinBalance")
    print("=" * 60)
    
    tests = [
        test_fractal_cache,
        test_fractal_load_balancer,
        test_fractal_compression,
        test_distributed_memory,
        test_fractal_ml,
        test_failure_prediction,
        test_genetic_optimization,
        test_sentiment_analysis,
        test_geographic_distribution,
        test_cross_region_replication,
        test_intelligent_sharding,
        test_demand_scaling,
        test_cascading_failure_manager,
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
        print("\n🎉 Todos os sistemas fractais estão funcionando perfeitamente!")
        print("   O CoinBalance está pronto para escalar infinitamente!")
    else:
        print(f"\n⚠️ {failed} sistema(s) precisam de atenção.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
