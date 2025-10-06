#!/usr/bin/env python3
"""
CryptoChain - Exemplo de Uso Rápido
Demonstra as principais funcionalidades da blockchain
"""

import requests
import time
import json
from typing import Dict, Any

# Configuração da API
API_BASE = "http://localhost:8000"

class CryptoChainClient:
    """Cliente para interagir com a CryptoChain API"""
    
    def __init__(self, base_url: str = API_BASE):
        self.base_url = base_url
        self.session = requests.Session()
    
    def criar_carteira(self, nome: str, senha: str = None) -> Dict[str, Any]:
        """Cria uma nova carteira"""
        response = self.session.post(f"{self.base_url}/carteiras/criar", json={
            "nome": nome,
            "senha": senha
        })
        response.raise_for_status()
        return response.json()
    
    def obter_carteira(self, nome: str) -> Dict[str, Any]:
        """Obtém informações de uma carteira"""
        response = self.session.get(f"{self.base_url}/carteiras/{nome}")
        response.raise_for_status()
        return response.json()
    
    def criar_transacao(self, remetente: str, destinatario: str, valor: float) -> Dict[str, Any]:
        """Cria uma nova transação"""
        response = self.session.post(f"{self.base_url}/transacoes/criar", json={
            "remetente": remetente,
            "destinatario": destinatario,
            "valor": valor,
            "taxa": 0.001
        })
        response.raise_for_status()
        return response.json()
    
    def fazer_stake(self, valor: float, contrato: str = "STAKING_CONTRACT_001") -> Dict[str, Any]:
        """Faz stake de tokens"""
        response = self.session.post(f"{self.base_url}/defi/stake", json={
            "valor": valor,
            "contrato": contrato
        })
        response.raise_for_status()
        return response.json()
    
    def obter_blockchain(self) -> Dict[str, Any]:
        """Obtém a blockchain completa"""
        response = self.session.get(f"{self.base_url}/blockchain")
        response.raise_for_status()
        return response.json()
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas da rede"""
        response = self.session.get(f"{self.base_url}/estatisticas")
        response.raise_for_status()
        return response.json()

def exemplo_basico():
    """Exemplo básico de uso da CryptoChain"""
    print("🚀 Exemplo Básico da CryptoChain")
    print("=" * 50)
    
    # Inicializar cliente
    client = CryptoChainClient()
    
    try:
        # 1. Criar carteiras
        print("1. 📝 Criando carteiras...")
        
        carteira_alice = client.criar_carteira("alice", "senha123")
        carteira_bob = client.criar_carteira("bob", "senha456")
        
        print(f"   ✅ Carteira Alice: {carteira_alice['endereco']}")
        print(f"   ✅ Carteira Bob: {carteira_bob['endereco']}")
        
        # 2. Verificar saldos iniciais
        print("\n2. 💰 Verificando saldos iniciais...")
        
        saldo_alice = client.obter_carteira("alice")['saldo']
        saldo_bob = client.obter_carteira("bob")['saldo']
        
        print(f"   💳 Saldo Alice: {saldo_alice} tokens")
        print(f"   💳 Saldo Bob: {saldo_bob} tokens")
        
        # 3. Simular mineração para obter tokens
        print("\n3. ⛏️  Simulando mineração...")
        print("   (Em um sistema real, você precisaria minerar blocos)")
        
        # 4. Verificar blockchain
        print("\n4. ⛓️  Verificando blockchain...")
        
        blockchain = client.obter_blockchain()
        print(f"   📊 Total de blocos: {blockchain['comprimento']}")
        print(f"   🔗 Hash último bloco: {blockchain['hash_ultimo_bloco']}")
        
        # 5. Obter estatísticas
        print("\n5. 📊 Estatísticas da rede...")
        
        stats = client.obter_estatisticas()
        print(f"   🌐 Status da rede: {stats['rede']['status']}")
        print(f"   📈 Total de blocos: {stats['blockchain']['total_blocos']}")
        print(f"   🤖 Contratos ativos: {stats['contratos']['total_contratos']}")
        
        print("\n🎉 Exemplo básico concluído com sucesso!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API")
        print("   Certifique-se de que a CryptoChain está rodando:")
        print("   python main.py")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def exemplo_defi():
    """Exemplo de funcionalidades DeFi"""
    print("\n🏦 Exemplo DeFi da CryptoChain")
    print("=" * 50)
    
    client = CryptoChainClient()
    
    try:
        # 1. Criar carteira para DeFi
        print("1. 📝 Criando carteira para DeFi...")
        
        carteira_defi = client.criar_carteira("defi_user", "senha_defi")
        print(f"   ✅ Carteira DeFi: {carteira_defi['endereco']}")
        
        # 2. Fazer stake (simulado)
        print("\n2. 🏦 Fazendo stake...")
        
        try:
            stake_result = client.fazer_stake(1000.0)
            print(f"   ✅ Stake realizado: {stake_result['total_staked']} tokens")
            print(f"   📈 APY: {stake_result.get('apy', 'N/A')}%")
        except requests.exceptions.HTTPError as e:
            print(f"   ⚠️  Stake não disponível: {e}")
        
        # 3. Verificar contratos DeFi
        print("\n3. 🤖 Verificando contratos DeFi...")
        
        try:
            response = client.session.get(f"{client.base_url}/defi/contratos")
            contratos = response.json()
            print(f"   📋 Total de contratos: {contratos['total']}")
            
            for contrato in contratos['contratos']:
                print(f"   🔧 {contrato['tipo']}: {contrato['endereco']}")
        except Exception as e:
            print(f"   ⚠️  Erro ao obter contratos: {e}")
        
        print("\n🎉 Exemplo DeFi concluído!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def exemplo_governance():
    """Exemplo de sistema de governança"""
    print("\n🏛️ Exemplo de Governança")
    print("=" * 50)
    
    client = CryptoChainClient()
    
    try:
        # 1. Verificar propostas ativas
        print("1. 📋 Verificando propostas ativas...")
        
        try:
            response = client.session.get(f"{client.base_url}/governance/propostas")
            propostas = response.json()
            print(f"   📊 Total de propostas: {propostas.get('total', 0)}")
            
            for proposta in propostas.get('propostas', []):
                print(f"   📝 {proposta['titulo']} - Status: {proposta['status']}")
        except Exception as e:
            print(f"   ⚠️  Erro ao obter propostas: {e}")
        
        # 2. Criar proposta (simulado)
        print("\n2. ✍️  Criando proposta...")
        
        try:
            proposta = {
                "titulo": "Aumentar taxa de staking",
                "descricao": "Proposta para aumentar APY de 12% para 15%",
                "tipo": "mudanca_taxa",
                "parametros": {"nova_taxa": 0.15}
            }
            
            response = client.session.post(f"{client.base_url}/governance/proposta", json=proposta)
            resultado = response.json()
            print(f"   ✅ Proposta criada: {resultado.get('proposta_id', 'N/A')}")
        except Exception as e:
            print(f"   ⚠️  Erro ao criar proposta: {e}")
        
        print("\n🎉 Exemplo de governança concluído!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def main():
    """Função principal dos exemplos"""
    print("🚀 CryptoChain - Exemplos de Uso")
    print("=" * 60)
    
    # Verificar se a API está rodando
    try:
        client = CryptoChainClient()
        client.session.get(f"{client.base_url}/", timeout=5)
        print("✅ API CryptoChain detectada e funcionando!")
    except requests.exceptions.ConnectionError:
        print("❌ API CryptoChain não está rodando!")
        print("   Para iniciar a API, execute:")
        print("   python main.py")
        return
    except Exception as e:
        print(f"❌ Erro ao conectar com a API: {e}")
        return
    
    # Executar exemplos
    exemplo_basico()
    exemplo_defi()
    exemplo_governance()
    
    print("\n" + "=" * 60)
    print("🎉 Todos os exemplos foram executados!")
    print("📚 Para mais informações, consulte a documentação:")
    print("   http://localhost:8000/docs")

if __name__ == "__main__":
    main()
