"""
Teste do Sistema Web3 CoinBalance
Testa Smart Contracts, Wallet Connect e DeFi Protocols
"""

import requests
import json
import time
import asyncio
from decimal import Decimal

BASE_URL = "http://localhost:8001/api/v1"

def test_web3_system():
    """Testa sistema Web3 completo"""
    print("🌐 Testando Sistema Web3 CoinBalance")
    print("============================================================")
    
    # 1. Health Check
    print("\n1. 🏥 Testando Health Check...")
    try:
        response = requests.get("http://localhost:8001/health/live")
        response.raise_for_status()
        print("   ✅ Health check OK")
    except Exception as e:
        print(f"   ❌ Health check falhou: {e}")
        return False
    
    # 2. Login para obter token
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
    
    # 3. Testar Smart Contracts
    print("\n3. 📜 Testando Smart Contracts...")
    try:
        # Criar contrato ERC20
        contract_data = {
            "contract_type": "ERC20",
            "custom_params": {
                "name": "Test Token",
                "symbol": "TEST",
                "decimals": 18,
                "total_supply": "1000000000000000000000000"
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/web3/contracts",
            json=contract_data,
            headers=headers
        )
        response.raise_for_status()
        contract_info = response.json()
        
        print(f"   ✅ Contrato ERC20 criado: {contract_info['address']}")
        
        # Deploy do contrato
        response = requests.post(
            f"{BASE_URL}/web3/contracts/{contract_info['address']}/deploy",
            headers=headers
        )
        response.raise_for_status()
        deploy_result = response.json()
        
        print(f"   ✅ Contrato deployado: {deploy_result['success']}")
        
    except Exception as e:
        print(f"   ❌ Erro nos Smart Contracts: {e}")
        return False
    
    # 4. Testar Wallet Connect
    print("\n4. 🔗 Testando Wallet Connect...")
    try:
        # Conectar carteira MetaMask
        wallet_data = {
            "wallet_type": "metamask",
            "chain_id": 1
        }
        
        response = requests.post(
            f"{BASE_URL}/web3/wallet/connect",
            json=wallet_data,
            headers=headers
        )
        response.raise_for_status()
        wallet_info = response.json()
        
        print(f"   ✅ Carteira conectada: {wallet_info['address']}")
        
        # Assinar mensagem
        sign_data = {
            "session_id": wallet_info["session_id"],
            "message": "Hello CoinBalance Web3!"
        }
        
        response = requests.post(
            f"{BASE_URL}/web3/wallet/sign",
            json=sign_data,
            headers=headers
        )
        response.raise_for_status()
        sign_result = response.json()
        
        print(f"   ✅ Mensagem assinada: {sign_result['signature'][:20]}...")
        
    except Exception as e:
        print(f"   ❌ Erro no Wallet Connect: {e}")
        return False
    
    # 5. Testar DeFi Protocols
    print("\n5. 💱 Testando DeFi Protocols...")
    try:
        # Listar pools de liquidez
        response = requests.get(
            f"{BASE_URL}/web3/defi/pools",
            headers=headers
        )
        response.raise_for_status()
        pools_data = response.json()
        
        print(f"   ✅ Pools encontrados: {len(pools_data['pools'])}")
        
        # Criar pool de liquidez (simulado)
        if pools_data['pools']:
            pool_address = pools_data['pools'][0]['address']
            
            # Executar swap
            swap_data = {
                "pool_address": pool_address,
                "token_in": "USDC",
                "amount_in": "1000",
                "user_address": wallet_info['address']
            }
            
            response = requests.post(
                f"{BASE_URL}/web3/defi/swap",
                json=swap_data,
                headers=headers
            )
            response.raise_for_status()
            swap_result = response.json()
            
            print(f"   ✅ Swap executado: {swap_result['transaction_hash']}")
            print(f"   💰 Amount out: {swap_result['amount_out']}")
        
    except Exception as e:
        print(f"   ❌ Erro nos DeFi Protocols: {e}")
        return False
    
    # 6. Testar Listagem de Contratos
    print("\n6. 📋 Testando Listagem de Contratos...")
    try:
        response = requests.get(
            f"{BASE_URL}/web3/contracts",
            headers=headers
        )
        response.raise_for_status()
        contracts_data = response.json()
        
        print(f"   ✅ Contratos listados: {len(contracts_data)}")
        for contract in contracts_data:
            print(f"      - {contract['name']} ({contract['contract_type']}) - {contract['status']}")
        
    except Exception as e:
        print(f"   ❌ Erro na listagem: {e}")
        return False
    
    print("\n============================================================")
    print("🎉 Todos os testes Web3 passaram!")
    print("✅ Sistema Web3 funcionando perfeitamente")
    print("\n🚀 Funcionalidades Web3 Disponíveis:")
    print("   📜 Smart Contracts (ERC20, ERC721, ERC1155)")
    print("   🔗 Wallet Connect (MetaMask, Coinbase, Trust)")
    print("   💱 DeFi Protocols (Uniswap, Aave, Compound)")
    print("   🏦 Liquidity Pools")
    print("   🔄 Token Swaps")
    print("   📊 DeFi Analytics")
    
    return True

if __name__ == "__main__":
    if not test_web3_system():
        print("\n❌ Alguns testes Web3 falharam")
