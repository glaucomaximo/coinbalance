#!/usr/bin/env python3
"""
Script para testar as melhorias implementadas no CoinBalance
"""

import requests
import time
import json

def test_improvements():
    """Testa todas as melhorias implementadas"""
    
    base_url = "http://localhost:8000"
    
    print("🚀 TESTANDO MELHORIAS IMPLEMENTADAS - COINBALANCE")
    print("=" * 60)
    
    # 1. Testar Health Check Avançado
    print("\n1️⃣ TESTANDO HEALTH CHECK AVANÇADO...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status geral: {data['overall_status']}")
            print(f"📊 Total de checks: {data['summary']['total_checks']}")
            print(f"✅ Saudáveis: {data['summary']['healthy']}")
            print(f"⚠️  Avisos: {data['summary']['warnings']}")
            print(f"❌ Críticos: {data['summary']['critical']}")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 2. Testar Health Check Simples
    print("\n2️⃣ TESTANDO HEALTH CHECK SIMPLES...")
    try:
        response = requests.get(f"{base_url}/health/simple")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"📱 Versão: {data['version']}")
            print(f"🔗 Blockchain: {data['blockchain']} blocos")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 3. Testar Métricas do Sistema
    print("\n3️⃣ TESTANDO MÉTRICAS DO SISTEMA...")
    try:
        response = requests.get(f"{base_url}/metrics")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Versão: {data['version']}")
            print(f"🔗 Blocos: {data['blockchain']['total_blocks']}")
            print(f"📈 Uptime: {data['system']['uptime']:.2f}s")
            print(f"💾 Memória: {data['system']['memory_usage']:.1f}%")
            print(f"🚫 Erros totais: {data['errors']['total_errors']}")
            print(f"🔒 IPs bloqueados: {data['rate_limiting']['blocked_ips']}")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 4. Testar Rate Limiting
    print("\n4️⃣ TESTANDO RATE LIMITING...")
    try:
        # Fazer várias requisições rapidamente
        for i in range(15):
            response = requests.get(f"{base_url}/")
            print(f"   Requisição {i+1}: {response.status_code}")
            if response.status_code == 429:
                print(f"   ✅ Rate limiting ativo! Headers: {dict(response.headers)}")
                break
            time.sleep(0.1)
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 5. Testar Tratamento de Erros
    print("\n5️⃣ TESTANDO TRATAMENTO DE ERROS...")
    try:
        # Tentar criar carteira com dados inválidos
        response = requests.post(f"{base_url}/carteiras/criar", json={
            "nome": "",  # Nome vazio
            "senha": "123"  # Senha muito curta
        })
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"   ✅ Erro capturado: {data.get('message', 'N/A')}")
            print(f"   📋 Código: {data.get('error_code', 'N/A')}")
        else:
            print(f"   ⚠️  Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 6. Testar Estatísticas de Erros
    print("\n6️⃣ TESTANDO ESTATÍSTICAS DE ERROS...")
    try:
        response = requests.get(f"{base_url}/admin/errors")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Total de erros: {data['total_errors']}")
            print(f"📈 Taxa de erro: {data['error_rate']:.2f}/min")
            print(f"🔍 Tipos de erro: {list(data['error_counts'].keys())}")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 7. Testar Funcionalidades Originais
    print("\n7️⃣ TESTANDO FUNCIONALIDADES ORIGINAIS...")
    try:
        # Status da API
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API funcionando: {data['status']}")
            print(f"📱 Versão: {data['versao']}")
        
        # Criar carteira
        response = requests.post(f"{base_url}/carteiras/criar", json={
            "nome": "Carteira Melhorada",
            "senha": "senha123"
        })
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Carteira criada: {data['endereco'][:20]}...")
        
        # Listar contratos
        response = requests.get(f"{base_url}/defi/contratos")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Contratos: {data['total']} ativos")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n🎉 TESTE DAS MELHORIAS CONCLUÍDO!")
    print("=" * 60)

if __name__ == "__main__":
    test_improvements()
