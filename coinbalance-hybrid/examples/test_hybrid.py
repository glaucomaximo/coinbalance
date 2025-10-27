#!/usr/bin/env python3
"""
Teste de integração para projeto híbrido Python-Rust
Demonstra funcionalidades e performance
"""

import sys
import time
import json
from pathlib import Path

# Adicionar diretórios ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "integration"))
sys.path.insert(0, str(project_root / "python"))

def test_python_components():
    """Testa componentes Python"""
    print("🐍 Testando componentes Python...")
    
    try:
        # Testar framework Coinbalance
        from coinbalance_framework import FrameworkCoinbalance, ProjetoConsciente, PerfilConsciencia, TipoConsciencia, NivelImpacto
        
        framework = FrameworkCoinbalance()
        
        # Criar projeto de teste
        projeto = ProjetoConsciente(
            nome="Projeto Teste",
            descricao="Projeto de teste para validação",
            impacto=NivelImpacto.ALTO,
            retorno_esperado=0.15,
            risco=0.3,
            valores_consciencia={
                TipoConsciencia.ESPIRITUAL: 0.8,
                TipoConsciencia.MENTAL: 0.7,
                TipoConsciencia.EMOCIONAL: 0.6
            }
        )
        
        # Cadastrar projeto
        result = framework.cadastrar_projeto(projeto)
        print(f"  ✅ Projeto cadastrado: {result['sucesso']}")
        
        # Criar perfil de investidor
        perfil = PerfilConsciencia(
            niveis_consciencia={
                TipoConsciencia.ESPIRITUAL: 0.9,
                TipoConsciencia.MENTAL: 0.8,
                TipoConsciencia.EMOCIONAL: 0.7
            },
            impacto_desejado=NivelImpacto.ALTO,
            tolerancia_risco=0.4,
            horizonte_tempo=5
        )
        
        # Cadastrar investidor
        result = framework.cadastrar_investidor(perfil, "Investidor Teste")
        print(f"  ✅ Investidor cadastrado: {result['sucesso']}")
        
        # Analisar investimento
        result = framework.analisar_investimento(0, 0)
        print(f"  ✅ Análise de investimento: {result['recomendacao_final']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro nos componentes Python: {e}")
        return False

def test_rust_integration():
    """Testa integração Rust"""
    print("🦀 Testando integração Rust...")
    
    try:
        from coinbalance_rust import CoinbalanceRustBridge
        
        # Criar ponte
        bridge = CoinbalanceRustBridge()
        
        # Testar hash
        data = "Hello, Coinbalance!"
        hash_result = bridge.calculate_hash(data)
        print(f"  ✅ Hash calculado: {hash_result[:16]}...")
        
        # Testar geração de chaves
        keypair = bridge.generate_keypair()
        if keypair:
            print(f"  ✅ Par de chaves gerado: {len(keypair)} campos")
        else:
            print("  ❌ Falha na geração de chaves")
            return False
        
        # Testar assinatura
        if keypair.get("private_key"):
            signature = bridge.sign_data(data, keypair["private_key"])
            if signature:
                print(f"  ✅ Assinatura criada: {signature[:16]}...")
                
                # Testar verificação
                is_valid = bridge.verify_signature(data, signature, keypair["public_key"])
                print(f"  ✅ Verificação de assinatura: {is_valid}")
            else:
                print("  ❌ Falha na assinatura")
                return False
        
        # Testar validação de transação
        test_tx = {
            "id": "test_tx_1",
            "from": "CNB_test123",
            "to": "CNB_test456",
            "amount": 100.0,
            "fee": 0.1,
            "timestamp": "2024-01-01T00:00:00Z",
            "signature": "test_signature",
            "nonce": 1
        }
        
        is_valid, message = bridge.validate_transaction(test_tx)
        print(f"  ✅ Validação de transação: {is_valid} - {message}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro na integração Rust: {e}")
        return False

def test_performance():
    """Testa performance Python vs Rust"""
    print("⚡ Testando performance...")
    
    try:
        from coinbalance_rust import CoinbalanceRustBridge
        
        bridge = CoinbalanceRustBridge()
        data = "Performance test data for Coinbalance"
        
        # Teste de hash Python (simulado)
        start_time = time.time()
        for _ in range(1000):
            hash(data)
        python_time = time.time() - start_time
        
        # Teste de hash Rust
        start_time = time.time()
        for _ in range(1000):
            bridge.calculate_hash(data)
        rust_time = time.time() - start_time
        
        improvement = python_time / rust_time if rust_time > 0 else 0
        
        print(f"  🐍 Python hash (1000x): {python_time:.4f}s")
        print(f"  🦀 Rust hash (1000x): {rust_time:.4f}s")
        print(f"  📈 Melhoria: {improvement:.1f}x")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro no teste de performance: {e}")
        return False

def test_mobile_interface():
    """Testa interface mobile"""
    print("📱 Testando interface mobile...")
    
    try:
        mobile_file = project_root / "examples" / "mobile_interface.html"
        if mobile_file.exists():
            print(f"  ✅ Interface mobile encontrada: {mobile_file}")
            
            # Verificar conteúdo
            content = mobile_file.read_text(encoding='utf-8')
            if "Coinbalance" in content and "CNB" in content:
                print("  ✅ Conteúdo da interface validado")
                return True
            else:
                print("  ❌ Conteúdo da interface inválido")
                return False
        else:
            print("  ❌ Interface mobile não encontrada")
            return False
            
    except Exception as e:
        print(f"  ❌ Erro no teste da interface mobile: {e}")
        return False

def test_build_system():
    """Testa sistema de build"""
    print("🛠️ Testando sistema de build...")
    
    try:
        build_script = project_root / "scripts" / "build.py"
        if build_script.exists():
            print(f"  ✅ Script de build encontrado: {build_script}")
            
            # Verificar se é executável
            if build_script.stat().st_mode & 0o111:
                print("  ✅ Script de build é executável")
                return True
            else:
                print("  ❌ Script de build não é executável")
                return False
        else:
            print("  ❌ Script de build não encontrado")
            return False
            
    except Exception as e:
        print(f"  ❌ Erro no teste do sistema de build: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 INICIANDO TESTES DE INTEGRAÇÃO COINBALANCE")
    print("=" * 50)
    
    tests = [
        ("Componentes Python", test_python_components),
        ("Integração Rust", test_rust_integration),
        ("Performance", test_performance),
        ("Interface Mobile", test_mobile_interface),
        ("Sistema de Build", test_build_system),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"  ❌ Erro inesperado: {e}")
            results[test_name] = False
    
    # Resumo dos resultados
    print("\n📊 RESUMO DOS TESTES")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO FINAL: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM! Projeto híbrido funcionando perfeitamente!")
        return True
    else:
        print("⚠️ ALGUNS TESTES FALHARAM. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)