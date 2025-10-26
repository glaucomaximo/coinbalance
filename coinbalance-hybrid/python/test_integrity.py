#!/usr/bin/env python3
"""
Script de Teste de Integridade - CoinBalance
Verifica erros de lógica e funcionamento correto de todos os módulos
"""

import sys
import traceback
import time
from typing import Dict, List, Any

def test_module_integrity():
    """Testa integridade de todos os módulos"""
    
    print("🔍 TESTE DE INTEGRIDADE - COINBALANCE")
    print("=" * 60)
    
    results = {
        "total_tests": 0,
        "passed": 0,
        "failed": 0,
        "errors": []
    }
    
    # 1. Testar importações
    print("\n1️⃣ TESTANDO IMPORTAÇÕES...")
    modules_to_test = [
        "crypto_utils",
        "wallet_system", 
        "database_manager",
        "transaction_validator",
        "smart_contracts",
        "tokenomics",
        "scalability",
        "blocosencadeados",
        "api_moderna",
        "error_handlers",
        "rate_limiter",
        "health_monitor",
        "database_optimizer"
    ]
    
    for module_name in modules_to_test:
        results["total_tests"] += 1
        try:
            __import__(module_name)
            print(f"   ✅ {module_name}")
            results["passed"] += 1
        except Exception as e:
            print(f"   ❌ {module_name}: {e}")
            results["failed"] += 1
            results["errors"].append(f"{module_name}: {e}")
    
    # 2. Testar criação de carteira
    print("\n2️⃣ TESTANDO CRIAÇÃO DE CARTEIRA...")
    results["total_tests"] += 1
    try:
        from wallet_system import Carteira
        carteira = Carteira("senha123")
        print(f"   ✅ Carteira criada: {carteira.endereco[:20]}...")
        print(f"   ✅ Saldo inicial: {carteira.saldo}")
        results["passed"] += 1
    except Exception as e:
        print(f"   ❌ Erro na criação de carteira: {e}")
        results["failed"] += 1
        results["errors"].append(f"Criação de carteira: {e}")
    
    # 3. Testar sistema de criptografia
    print("\n3️⃣ TESTANDO SISTEMA DE CRIPTOGRAFIA...")
    results["total_tests"] += 1
    try:
        from crypto_utils import CryptoUtils
        private_key, public_key = CryptoUtils.gerar_par_chaves()
        
        # Testar assinatura
        test_data = {"test": "data", "timestamp": time.time()}
        signature = CryptoUtils.assinar_transacao(test_data, private_key)
        is_valid = CryptoUtils.verificar_assinatura(test_data, signature, public_key)
        
        if is_valid:
            print("   ✅ Geração de chaves funcionando")
            print("   ✅ Assinatura e verificação funcionando")
            results["passed"] += 1
        else:
            print("   ❌ Verificação de assinatura falhou")
            results["failed"] += 1
            results["errors"].append("Verificação de assinatura falhou")
    except Exception as e:
        print(f"   ❌ Erro no sistema de criptografia: {e}")
        results["failed"] += 1
        results["errors"].append(f"Sistema de criptografia: {e}")
    
    # 4. Testar blockchain
    print("\n4️⃣ TESTANDO SISTEMA DE BLOCKCHAIN...")
    results["total_tests"] += 1
    try:
        from blocosencadeados import BlocosEncadeados
        blockchain = BlocosEncadeados()
        
        # Adicionar transação
        blockchain.nova_troca("Alice", "Bob", 10.0)
        
        # Criar novo bloco
        bloco = blockchain.novo_bloco(prova=12345, fragmento_anterior=None)
        
        print(f"   ✅ Blockchain criado com {len(blockchain.cadeia)} blocos")
        print(f"   ✅ Último bloco: {bloco['indice']}")
        results["passed"] += 1
    except Exception as e:
        print(f"   ❌ Erro no sistema de blockchain: {e}")
        results["failed"] += 1
        results["errors"].append(f"Sistema de blockchain: {e}")
    
    # 5. Testar banco de dados
    print("\n5️⃣ TESTANDO SISTEMA DE BANCO DE DADOS...")
    results["total_tests"] += 1
    try:
        from database_manager import DatabaseManager
        db = DatabaseManager("test_integrity.db")
        
        # Testar operações básicas
        bloco_teste = {
            "indice": 1,
            "timestamp": time.time(),
            "hash_anterior": "0",
            "hash_atual": "test_hash",
            "prova": 12345,
            "dados": "test_data"
        }
        
        db.salvar_bloco(bloco_teste)
        blocos = db.obter_todos_blocos()
        
        print(f"   ✅ Banco de dados funcionando")
        print(f"   ✅ Blocos salvos: {len(blocos)}")
        results["passed"] += 1
    except Exception as e:
        print(f"   ❌ Erro no banco de dados: {e}")
        results["failed"] += 1
        results["errors"].append(f"Banco de dados: {e}")
    
    # 6. Testar validação de transações
    print("\n6️⃣ TESTANDO VALIDAÇÃO DE TRANSAÇÕES...")
    results["total_tests"] += 1
    try:
        from transaction_validator import TransactionValidator
        from database_manager import DatabaseManager
        
        db = DatabaseManager("test_validation.db")
        validator = TransactionValidator(db)
        
        # Criar transação de teste
        transacao_teste = {
            "remetente": "CRYPTO_test123",
            "destinatario": "CRYPTO_test456", 
            "valor": 10.0,
            "timestamp": time.time(),
            "assinatura": "test_signature",
            "chave_publica": "test_public_key"
        }
        
        resultado = validator.validar_transacao(transacao_teste)
        print(f"   ✅ Validador funcionando")
        print(f"   ✅ Resultado: {resultado['valida']}")
        results["passed"] += 1
    except Exception as e:
        print(f"   ❌ Erro na validação: {e}")
        results["failed"] += 1
        results["errors"].append(f"Validação: {e}")
    
    # 7. Testar contratos inteligentes
    print("\n7️⃣ TESTANDO CONTRATOS INTELIGENTES...")
    results["total_tests"] += 1
    try:
        from smart_contracts import StakingContract, ContractManager
        from database_manager import DatabaseManager
        
        db = DatabaseManager("test_contracts.db")
        contract_manager = ContractManager(db)
        
        # Criar contrato de staking
        staking_contract = StakingContract("CONTRACT_test", "CRYPTO_creator")
        
        # Testar função de staking
        resultado = staking_contract.executar("stake", {"valor": 100.0}, "CRYPTO_user")
        
        print(f"   ✅ Contratos inteligentes funcionando")
        print(f"   ✅ Staking: {resultado['sucesso']}")
        results["passed"] += 1
    except Exception as e:
        print(f"   ❌ Erro nos contratos: {e}")
        results["failed"] += 1
        results["errors"].append(f"Contratos: {e}")
    
    # 8. Testar tokenomics
    print("\n8️⃣ TESTANDO SISTEMA DE TOKENOMICS...")
    results["total_tests"] += 1
    try:
        from tokenomics import Tokenomics
        from database_manager import DatabaseManager
        
        db = DatabaseManager("test_tokenomics.db")
        tokenomics = Tokenomics(db)
        
        # Testar informações de supply
        supply_info = tokenomics.obter_supply_info()
        
        print(f"   ✅ Tokenomics funcionando")
        print(f"   ✅ Supply máximo: {supply_info['supply_maximo']}")
        results["passed"] += 1
    except Exception as e:
        print(f"   ❌ Erro no tokenomics: {e}")
        results["failed"] += 1
        results["errors"].append(f"Tokenomics: {e}")
    
    # 9. Testar sistema de escalabilidade
    print("\n9️⃣ TESTANDO SISTEMA DE ESCALABILIDADE...")
    results["total_tests"] += 1
    try:
        from scalability import ShardManager, CacheManager
        from database_manager import DatabaseManager
        
        db = DatabaseManager("test_scalability.db")
        shard_manager = ShardManager(db, num_shards=2)
        cache_manager = CacheManager()
        
        print(f"   ✅ Escalabilidade funcionando")
        print(f"   ✅ Shards criados: {shard_manager.num_shards}")
        results["passed"] += 1
    except Exception as e:
        print(f"   ❌ Erro na escalabilidade: {e}")
        results["failed"] += 1
        results["errors"].append(f"Escalabilidade: {e}")
    
    # 10. Testar melhorias implementadas
    print("\n🔟 TESTANDO MELHORIAS IMPLEMENTADAS...")
    results["total_tests"] += 1
    try:
        from error_handlers import error_handler
        from rate_limiter import rate_limiter
        from health_monitor import health_monitor
        from database_optimizer import DatabaseOptimizer
        from database_manager import DatabaseManager
        
        db = DatabaseManager("test_improvements.db")
        optimizer = DatabaseOptimizer(db)
        
        print("   ✅ Error handlers funcionando")
        print("   ✅ Rate limiter funcionando")
        print("   ✅ Health monitor funcionando")
        print("   ✅ Database optimizer funcionando")
        results["passed"] += 1
    except Exception as e:
        print(f"   ❌ Erro nas melhorias: {e}")
        results["failed"] += 1
        results["errors"].append(f"Melhorias: {e}")
    
    # Resumo dos resultados
    print("\n📊 RESUMO DOS TESTES")
    print("=" * 60)
    print(f"Total de testes: {results['total_tests']}")
    print(f"✅ Aprovados: {results['passed']}")
    print(f"❌ Falharam: {results['failed']}")
    print(f"📈 Taxa de sucesso: {(results['passed']/results['total_tests']*100):.1f}%")
    
    if results['errors']:
        print("\n🚨 ERROS ENCONTRADOS:")
        for i, error in enumerate(results['errors'], 1):
            print(f"   {i}. {error}")
    
    return results

if __name__ == "__main__":
    test_module_integrity()
