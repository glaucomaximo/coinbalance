#!/usr/bin/env python3
"""
Script para testar a API CoinBalance
Cria carteiras, transações e testa funcionalidades DeFi
"""

import requests
import json
import time

# Configuração da API
BASE_URL = "http://localhost:8000"

def test_api():
    """Testa todas as funcionalidades da API CoinBalance"""
    
    print("🚀 TESTANDO COINBALANCE API")
    print("=" * 50)
    
    # 1. Verificar status da API
    print("\n1️⃣ VERIFICANDO STATUS DA API...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"📱 Versão: {data['versao']}")
            print(f"⏰ Timestamp: {data['timestamp']}")
            print(f"🔗 Blockchain: {data['blockchain']['blocos']} blocos, {data['blockchain']['contratos_ativos']} contratos")
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
            "saldo_inicial": 1000.0
        }
        response = requests.post(f"{BASE_URL}/carteiras/criar", json=carteira_data)
        if response.status_code == 200:
            carteira = response.json()
            print(f"✅ Carteira criada: {carteira['endereco']}")
            print(f"💰 Saldo inicial: {carteira['saldo']} CB")
            carteira1 = carteira
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
            "saldo_inicial": 500.0
        }
        response = requests.post(f"{BASE_URL}/carteiras/criar", json=carteira_data)
        if response.status_code == 200:
            carteira = response.json()
            print(f"✅ Carteira criada: {carteira['endereco']}")
            print(f"💰 Saldo inicial: {carteira['saldo']} CB")
            carteira2 = carteira
        else:
            print(f"❌ Erro ao criar carteira: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    # 4. Fazer primeira transação
    print("\n4️⃣ FAZENDO PRIMEIRA TRANSAÇÃO...")
    try:
        transacao_data = {
            "remetente": carteira1['endereco'],
            "destinatario": carteira2['endereco'],
            "valor": 100.0,
            "chave_privada": carteira1['chave_privada']
        }
        response = requests.post(f"{BASE_URL}/transacoes/criar", json=transacao_data)
        if response.status_code == 200:
            transacao = response.json()
            print(f"✅ Transação criada: {transacao['hash']}")
            print(f"💰 Valor: {transacao['valor']} CB")
            print(f"📤 De: {transacao['remetente']}")
            print(f"📥 Para: {transacao['destinatario']}")
        else:
            print(f"❌ Erro ao criar transação: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    # 5. Verificar blockchain
    print("\n5️⃣ VERIFICANDO BLOCKCHAIN...")
    try:
        response = requests.get(f"{BASE_URL}/blockchain")
        if response.status_code == 200:
            blockchain = response.json()
            print(f"🔗 Blocos: {blockchain['blocos']}")
            print(f"⛏️ Dificuldade: {blockchain['dificuldade']}")
            print(f"🔒 Hash anterior: {blockchain['hash_anterior'][:20]}...")
        else:
            print(f"❌ Erro ao verificar blockchain: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 6. Testar funcionalidades DeFi
    print("\n6️⃣ TESTANDO FUNCIONALIDADES DEFI...")
    
    # Staking
    print("\n📈 TESTANDO STAKING...")
    try:
        staking_data = {
            "endereco": carteira1['endereco'],
            "valor": 200.0,
            "chave_privada": carteira1['chave_privada']
        }
        response = requests.post(f"{BASE_URL}/defi/staking/stake", json=staking_data)
        if response.status_code == 200:
            staking = response.json()
            print(f"✅ Staking realizado: {staking['valor']} CB")
            print(f"📊 Taxa de juros: {staking['taxa_juros']}%")
        else:
            print(f"❌ Erro no staking: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Lending
    print("\n💰 TESTANDO LENDING...")
    try:
        lending_data = {
            "endereco": carteira2['endereco'],
            "valor": 50.0,
            "chave_privada": carteira2['chave_privada']
        }
        response = requests.post(f"{BASE_URL}/defi/lending/borrow", json=lending_data)
        if response.status_code == 200:
            lending = response.json()
            print(f"✅ Empréstimo realizado: {lending['valor']} CB")
            print(f"📊 Taxa de juros: {lending['taxa_juros']}%")
        else:
            print(f"❌ Erro no lending: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 7. Verificar status final
    print("\n7️⃣ VERIFICANDO STATUS FINAL...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"🔗 Blockchain: {data['blockchain']['blocos']} blocos")
            print(f"🤖 Contratos ativos: {data['blockchain']['contratos_ativos']}")
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n🎉 TESTE COMPLETO!")
    print("=" * 50)

if __name__ == "__main__":
    test_api()
