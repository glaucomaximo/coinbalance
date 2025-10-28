"""
Teste do Sistema de Criação de Criptomoedas com IA
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001/api/v1"

def test_ai_crypto_creation():
    print("🤖 Testando Sistema de Criação de Criptomoedas com IA")
    print("============================================================")

    # 1. Health Check
    print("\n1. 🏥 Testando Health Check...")
    try:
        response = requests.get("http://localhost:8001/health/live")
        response.raise_for_status()
        print(f"   ✅ Health check OK")
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

    # 3. Analisar Oportunidade de Mercado
    print("\n3. 📊 Analisando Oportunidade de Mercado...")
    try:
        market_analysis_data = {
            "purpose": "defi",
            "target_market": "global"
        }
        response = requests.post(f"{BASE_URL}/ai-crypto/analyze-market", json=market_analysis_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Análise de mercado concluída")
        print(f"   📈 Demanda: {data['market_demand']:.2f}")
        print(f"   🏆 Competição: {data['competition_level']:.2f}")
        print(f"   💡 Inovação: {data['innovation_potential']:.2f}")
        print(f"   🎯 Adoção: {data['adoption_probability']:.2f}")
        print(f"   💰 Viabilidade: {data['economic_viability']:.2f}")
        print(f"   📋 Recomendação: {data['recommended_action']}")
        print(f"   🎯 Confiança: {data['confidence_score']:.2f}")
    except Exception as e:
        print(f"   ❌ Erro na análise de mercado: {e}")
        return False

    # 4. Criar Nova Criptomoeda
    print("\n4. 🪙 Criando Nova Criptomoeda...")
    try:
        create_crypto_data = {
            "purpose": "defi",
            "target_market": "global",
            "custom_requirements": {
                "features": ["staking", "governance", "burning"],
                "target_users": "defi_protocols"
            }
        }
        response = requests.post(f"{BASE_URL}/ai-crypto/create", json=create_crypto_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Criptomoeda criada com sucesso!")
        print(f"   🪙 Nome: {data['name']}")
        print(f"   🔤 Símbolo: {data['symbol']}")
        print(f"   🎯 Propósito: {data['purpose']}")
        print(f"   🏗️ Consenso: {data['consensus_type']}")
        print(f"   💰 Supply Total: {data['tokenomics']['total_supply']}")
        print(f"   📈 Inflação: {data['tokenomics']['inflation_rate']}")
        print(f"   🎯 Features: {', '.join(data['features'])}")
        print(f"   🤖 Reasoning IA: {data['ai_reasoning']}")
    except Exception as e:
        print(f"   ❌ Erro ao criar criptomoeda: {e}")
        return False

    # 5. Verificar Saúde do Ecossistema
    print("\n5. 🏥 Verificando Saúde do Ecossistema...")
    try:
        response = requests.get(f"{BASE_URL}/ai-crypto/ecosystem-health", headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Saúde do ecossistema verificada")
        print(f"   📊 Score Geral: {data['overall_score']:.2f}")
        print(f"   💧 Liquidez: {data['liquidity_score']:.2f}")
        print(f"   👥 Adoção: {data['adoption_score']:.2f}")
        print(f"   💡 Inovação: {data['innovation_score']:.2f}")
        print(f"   ⚖️ Estabilidade: {data['stability_score']:.2f}")
        print(f"   📈 Potencial: {data['growth_potential']:.2f}")
        print(f"   ⚠️ Risco: {data['risk_level']}")
        print(f"   💡 Recomendações: {len(data['recommendations'])} encontradas")
    except Exception as e:
        print(f"   ❌ Erro ao verificar saúde: {e}")
        return False

    # 6. Tomar Decisão Autônoma
    print("\n6. 🧠 Tomando Decisão Autônoma...")
    try:
        response = requests.post(f"{BASE_URL}/ai-crypto/make-decision", headers=headers)
        if response.status_code == 204:
            print(f"   ℹ️ Nenhuma decisão necessária no momento")
        else:
            response.raise_for_status()
            data = response.json()
            print(f"   ✅ Decisão autônoma tomada!")
            print(f"   🎯 Tipo: {data['decision_type']}")
            print(f"   🧠 Reasoning: {data['reasoning']}")
            print(f"   📈 Confiança: {data['confidence']:.2f}")
            print(f"   📋 Plano: {len(data['execution_plan'])} etapas")
    except Exception as e:
        print(f"   ❌ Erro ao tomar decisão: {e}")
        return False

    # 7. Gerar Token Personalizado
    print("\n7. 🏭 Gerando Token Personalizado...")
    try:
        token_generation_data = {
            "purpose": "Gaming rewards and in-game currency",
            "target_audience": "gaming_community",
            "requirements": {
                "features": ["play_to_earn", "achievements", "leaderboard"],
                "standard": "ERC-1155",
                "max_supply": "1000000000"
            },
            "preferences": {
                "low_fees": True,
                "fast_transactions": True,
                "mobile_support": True
            }
        }
        response = requests.post(f"{BASE_URL}/ai-crypto/generate-token", json=token_generation_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Token personalizado gerado!")
        print(f"   🎮 Nome: {data['name']}")
        print(f"   🔤 Símbolo: {data['symbol']}")
        print(f"   📂 Categoria: {data['category']}")
        print(f"   📋 Padrão: {data['standard']}")
        print(f"   🎯 Features: {', '.join(data['features'])}")
        print(f"   💰 Supply: {data['tokenomics']['total_supply']}")
        print(f"   🎯 Confiança: {data['confidence_score']:.2f}")
        print(f"   📋 Instruções: {len(data['deployment_instructions'])} etapas")
    except Exception as e:
        print(f"   ❌ Erro ao gerar token: {e}")
        return False

    # 8. Listar Criptomoedas Criadas
    print("\n8. 📋 Listando Criptomoedas Criadas...")
    try:
        response = requests.get(f"{BASE_URL}/ai-crypto/created-cryptos", headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Lista obtida com sucesso")
        print(f"   🪙 Total de criptomoedas: {data['total']}")
        for crypto in data['cryptocurrencies']:
            print(f"   - {crypto['name']} ({crypto['symbol']}) - {crypto['purpose']}")
    except Exception as e:
        print(f"   ❌ Erro ao listar criptomoedas: {e}")
        return False

    # 9. Listar Templates de Tokens
    print("\n9. 📋 Listando Templates de Tokens...")
    try:
        response = requests.get(f"{BASE_URL}/ai-crypto/token-templates", headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Templates obtidos com sucesso")
        print(f"   🏭 Total de templates: {data['total']}")
        for template in data['templates']:
            print(f"   - {template['name']} ({template['symbol']}) - {template['category']}")
    except Exception as e:
        print(f"   ❌ Erro ao listar templates: {e}")
        return False

    # 10. Verificar Status do Ecossistema
    print("\n10. 📊 Verificando Status do Ecossistema...")
    try:
        response = requests.get(f"{BASE_URL}/ai-crypto/ecosystem-status", headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"   ✅ Status obtido com sucesso")
        print(f"   🏥 Saúde: {data['health']['overall_score']:.2f}" if data['health'] else "   🏥 Saúde: N/A")
        print(f"   📈 Fase: {data['phase']}")
        print(f"   🪙 Criptomoedas ativas: {data['active_cryptos']}")
        print(f"   🧠 Total de decisões: {data['total_decisions']}")
        print(f"   📋 Decisões recentes: {len(data['recent_decisions'])}")
    except Exception as e:
        print(f"   ❌ Erro ao verificar status: {e}")
        return False

    print("\n============================================================")
    print("✅ Todos os testes de IA Crypto Creation concluídos com sucesso!")
    print("\n🎉 O CoinBalance agora pode criar criptomoedas autonomamente!")
    print("🤖 A IA toma decisões econômicas inteligentes!")
    print("🏭 Tokens personalizados são gerados automaticamente!")
    print("🌍 Uma nova economia descentralizada está nascendo!")
    return True

if __name__ == "__main__":
    if not test_ai_crypto_creation():
        print("\n❌ Alguns testes de IA Crypto Creation falharam")
