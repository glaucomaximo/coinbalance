#!/usr/bin/env python3
"""
Script para testar a API CoinBalance completa
"""

import requests
import json
import time

def test_coinbalance_api():
    """Testa todas as funcionalidades da API CoinBalance"""
    
    base_url = "http://localhost:8000"
    
    print("🚀 TESTANDO API COINBALANCE")
    print("=" * 50)
    
    # 1. Testar status da API
    print("\n1️⃣ TESTANDO STATUS DA API...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"📱 Versão: {data['versao']}")
            print(f"🔗 Blockchain: {data['blockchain']['blocos']} blocos")
            print(f"🤖 Contratos: {data['blockchain']['contratos_ativos']} ativos")
        else:
            print(f"❌ Erro: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return
    
    # 2. Criar primeira carteira
    print("\n2️⃣ CRIANDO PRIMEIRA CARTEIRA...")
    try:
        carteira_data = {
            "nome": "Carteira Principal",
            "senha": "senha123"
        }
        response = requests.post(f"{base_url}/carteiras/criar", json=carteira_data)
        if response.status_code == 200:
            carteira1 = response.json()
            print(f"✅ Carteira criada: {carteira1['endereco']}")
            print(f"💰 Saldo: {carteira1['saldo']} CB")
            print(f"🔑 Chave pública: {carteira1['chave_publica'][:50]}...")
        else:
            print(f"❌ Erro ao criar carteira: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    # 3. Criar segunda carteira
    print("\n3️⃣ CRIANDO SEGUNDA CARTEIRA...")
    try:
        carteira_data = {
            "nome": "Carteira Secundária",
            "senha": "senha456"
        }
        response = requests.post(f"{base_url}/carteiras/criar", json=carteira_data)
        if response.status_code == 200:
            carteira2 = response.json()
            print(f"✅ Carteira criada: {carteira2['endereco']}")
            print(f"💰 Saldo: {carteira2['saldo']} CB")
        else:
            print(f"❌ Erro ao criar carteira: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    # 4. Testar blockchain
    print("\n4️⃣ TESTANDO BLOCKCHAIN...")
    try:
        response = requests.get(f"{base_url}/blockchain")
        if response.status_code == 200:
            blockchain = response.json()
            print(f"🔗 Blocos: {blockchain['comprimento']}")
            print(f"📊 Hash último bloco: {blockchain.get('hash_ultimo_bloco', 'N/A')}")
        else:
            print(f"❌ Erro ao verificar blockchain: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 5. Testar contratos DeFi
    print("\n5️⃣ TESTANDO CONTRATOS DEFI...")
    try:
        response = requests.get(f"{base_url}/defi/contratos")
        if response.status_code == 200:
            contratos = response.json()
            print(f"🤖 Total de contratos: {contratos['total']}")
            for contrato in contratos['contratos']:
                print(f"   📋 {contrato['endereco']}: {contrato['tipo']}")
        else:
            print(f"❌ Erro ao listar contratos: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 6. Testar staking
    print("\n6️⃣ TESTANDO STAKING...")
    try:
        staking_data = {
            "valor": 100.0,
            "contrato": "STAKING_CONTRACT_001"
        }
        response = requests.post(f"{base_url}/defi/stake", json=staking_data)
        if response.status_code == 200:
            staking = response.json()
            print(f"✅ Stake realizado: {staking.get('mensagem', 'Sucesso')}")
        else:
            print(f"❌ Erro no staking: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 7. Testar empréstimo
    print("\n7️⃣ TESTANDO EMPRÉSTIMO...")
    try:
        lending_data = {
            "valor": 50.0,
            "colateral": 100.0
        }
        response = requests.post(f"{base_url}/defi/borrow", json=lending_data)
        if response.status_code == 200:
            lending = response.json()
            print(f"✅ Empréstimo: {lending.get('mensagem', 'Sucesso')}")
        else:
            print(f"❌ Erro no empréstimo: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 8. Testar estatísticas
    print("\n8️⃣ TESTANDO ESTATÍSTICAS...")
    try:
        response = requests.get(f"{base_url}/estatisticas")
        if response.status_code == 200:
            stats = response.json()
            print(f"📊 Blockchain: {stats['blockchain']['total_blocos']} blocos")
            print(f"🤖 Contratos: {stats['contratos']['total_contratos']} ativos")
            print(f"🌐 Rede: {stats['rede']['status']}")
        else:
            print(f"❌ Erro ao obter estatísticas: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n🎉 TESTE COMPLETO DA API COINBALANCE!")
    print("=" * 50)

if __name__ == "__main__":
    test_coinbalance_api()
