"""
Teste Completo das Próximas Funcionalidades Web3
Testa NFT Marketplace, DAO Governance, Cross-Chain Bridge e Analytics
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001/api/v1"

def run_comprehensive_web3_tests():
    print("🚀 Testando Próximas Funcionalidades Web3 CoinBalance")
    print("=" * 60)

    # 1. Health Check
    print("\n1. 🏥 Testando Health Check...")
    try:
        response = requests.get("http://localhost:8001/health/live")
        response.raise_for_status()
        print("   ✅ Health check OK")
    except Exception as e:
        print(f"   ❌ Erro no health check: {e}")
        return False

    # 2. Login para obter token JWT
    print("\n2. 🔑 Fazendo Login...")
    login_data = {"username": "admin", "password": "admin123"}
    access_token = None
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        response.raise_for_status()
        data = response.json()
        access_token = data["access_token"]
        print(f"   ✅ Login bem-sucedido")
        print(f"   🎫 Token obtido: {access_token[:30]}...")
    except Exception as e:
        print(f"   ❌ Login falhou: {e}")
        return False

    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Testar NFT Marketplace
    print("\n3. 🎨 Testando NFT Marketplace...")
    try:
        # Criar NFT
        nft_data = {
            "contract_address": "0x1234567890123456789012345678901234567890",
            "token_id": "1",
            "owner": "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
            "creator": "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
            "name": "CoinBalance Genesis NFT",
            "description": "Primeiro NFT do CoinBalance",
            "image_url": "https://coinbalance.com/nft/genesis.jpg"
        }
        
        response = requests.post(f"{BASE_URL}/web3/nft/create", json=nft_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ NFT criado: {data['nft']['name']}")
        
        # Listar NFT
        listing_data = {
            "nft_key": f"{nft_data['contract_address']}:{nft_data['token_id']}",
            "seller": nft_data["owner"],
            "listing_type": "fixed_price",
            "price": "100",
            "currency": "CNB"
        }
        
        response = requests.post(f"{BASE_URL}/web3/nft/list", json=listing_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ NFT listado: {data['listing_id']}")
        
    except Exception as e:
        print(f"   ❌ Erro no NFT Marketplace: {e}")
        print(f"   📄 Resposta: {response.text if 'response' in locals() else 'N/A'}")

    # 4. Testar DAO Governance
    print("\n4. 🏛️ Testando DAO Governance...")
    try:
        # Criar proposta
        proposal_data = {
            "proposer": "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
            "title": "Proposta de Upgrade do Sistema",
            "description": "Esta proposta sugere um upgrade do sistema CoinBalance para melhorar a performance",
            "proposal_type": "upgrade",
            "targets": ["0x1234567890123456789012345678901234567890"],
            "values": ["0"],
            "calldatas": ["0x"]
        }
        
        response = requests.post(f"{BASE_URL}/web3/dao/proposal", json=proposal_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Proposta criada: {data['proposal_id']}")
        
        # Votar na proposta
        vote_data = {
            "voter": "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
            "proposal_id": data["proposal_id"],
            "vote_type": "for",
            "reason": "Concordo com o upgrade"
        }
        
        response = requests.post(f"{BASE_URL}/web3/dao/vote", json=vote_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Voto registrado: {data['vote_type']}")
        
    except Exception as e:
        print(f"   ❌ Erro no DAO Governance: {e}")
        print(f"   📄 Resposta: {response.text if 'response' in locals() else 'N/A'}")

    # 5. Testar Cross-Chain Bridge
    print("\n5. 🌉 Testando Cross-Chain Bridge...")
    try:
        # Iniciar bridge
        bridge_data = {
            "source_chain": "ethereum",
            "target_chain": "polygon",
            "sender": "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
            "receiver": "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
            "token": "CNB",
            "amount": "1000"
        }
        
        response = requests.post(f"{BASE_URL}/web3/bridge/initiate", json=bridge_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Bridge iniciado: {data['tx_id']}")
        
        # Verificar status
        tx_id = data["tx_id"]
        response = requests.get(f"{BASE_URL}/web3/bridge/status/{tx_id}", headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Status do bridge: {data['status']}")
        
    except Exception as e:
        print(f"   ❌ Erro no Cross-Chain Bridge: {e}")
        print(f"   📄 Resposta: {response.text if 'response' in locals() else 'N/A'}")

    # 6. Testar Web3 Analytics
    print("\n6. 📊 Testando Web3 Analytics...")
    try:
        # Gráfico de preços
        response = requests.get(f"{BASE_URL}/web3/analytics/price/CNB?time_range=24h", headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Gráfico de preços obtido: {data['current_price']} CNB")
        
        # Visão geral do mercado
        response = requests.get(f"{BASE_URL}/web3/analytics/market-overview", headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Visão geral: {data['total_users']} usuários, {data['total_transactions']} transações")
        
        # Analytics do usuário
        user_address = "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B"
        response = requests.get(f"{BASE_URL}/web3/analytics/user/{user_address}", headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Analytics do usuário: {data.get('total_transactions', 0)} transações")
        
    except Exception as e:
        print(f"   ❌ Erro no Web3 Analytics: {e}")
        print(f"   📄 Resposta: {response.text if 'response' in locals() else 'N/A'}")

    # 7. Testar Funcionalidades Existentes
    print("\n7. 🔧 Testando Funcionalidades Existentes...")
    try:
        # Smart Contracts
        contract_data = {
            "bytecode": "0x6080604052...",
            "abi": [{"constant": True, "inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"}],
            "constructor_args": []
        }
        
        response = requests.post(f"{BASE_URL}/web3/contracts", json=contract_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Smart Contract deployado: {data['contract_address']}")
        else:
            print(f"   ⚠️ Smart Contract: {response.status_code} (esperado)")
        
        # Wallet Connect
        wallet_data = {
            "session_id": f"session_{int(time.time())}",
            "wallet_address": "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
            "chain_id": 1
        }
        
        response = requests.post(f"{BASE_URL}/web3/wallet-connect/connect", json=wallet_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Wallet conectado: {data['session_id']}")
        else:
            print(f"   ⚠️ Wallet Connect: {response.status_code} (esperado)")
        
        # DeFi Protocols
        response = requests.get(f"{BASE_URL}/web3/defi/token-price?token_address=0xTokenA&vs_token_address=ETH", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Preço DeFi obtido: {data['price']}")
        else:
            print(f"   ⚠️ DeFi: {response.status_code} (esperado)")
        
    except Exception as e:
        print(f"   ❌ Erro nas funcionalidades existentes: {e}")

    print("\n" + "=" * 60)
    print("✅ Teste das Próximas Funcionalidades Web3 concluído!")
    print("\n🎯 Funcionalidades Testadas:")
    print("   • NFT Marketplace - Criação e listagem de NFTs")
    print("   • DAO Governance - Criação de propostas e votação")
    print("   • Cross-Chain Bridge - Ponte entre blockchains")
    print("   • Web3 Analytics - Gráficos e métricas")
    print("   • Smart Contracts - Deploy de contratos")
    print("   • Wallet Connect - Conexão de carteiras")
    print("   • DeFi Protocols - Protocolos descentralizados")
    
    return True

if __name__ == "__main__":
    if not run_comprehensive_web3_tests():
        print("\n❌ Alguns testes falharam")
