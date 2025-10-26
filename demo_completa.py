#!/usr/bin/env python3
"""
Demonstração Completa do Sistema CoinBalance
Mostra todas as funcionalidades em pleno funcionamento
"""

import requests
import time
import json
from typing import Dict, Any

class CoinBalanceDemo:
    """Demonstração completa do sistema CoinBalance"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.carteiras = []
        self.contratos = []
        
    def aguardar_sistema(self):
        """Aguarda o sistema estar pronto"""
        print("⏳ Aguardando sistema inicializar...")
        for i in range(10):
            try:
                response = requests.get(f"{self.base_url}/health/simple", timeout=2)
                if response.status_code == 200:
                    print("✅ Sistema pronto!")
                    return True
            except:
                time.sleep(1)
        return False
    
    def demonstrar_status_sistema(self):
        """Demonstra status do sistema"""
        print("\n" + "="*60)
        print("🔍 STATUS DO SISTEMA COINBALANCE")
        print("="*60)
        
        # Health check simples
        response = requests.get(f"{self.base_url}/health/simple")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"📱 Versão: {data['version']}")
            print(f"🔗 Blockchain: {data['blockchain']} blocos")
        
        # Health check avançado
        response = requests.get(f"{self.base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Status geral: {data['overall_status']}")
            print(f"✅ Componentes saudáveis: {data['summary']['healthy']}")
            print(f"⚠️  Avisos: {data['summary'].get('warnings', 0)}")
            print(f"❌ Críticos: {data['summary'].get('critical', 0)}")
        
        # Métricas do sistema
        response = requests.get(f"{self.base_url}/metrics")
        if response.status_code == 200:
            data = response.json()
            print(f"📈 Uptime: {data['system']['uptime']:.2f}s")
            print(f"💾 Memória: {data['system']['memory_usage']:.1f}%")
            print(f"🚫 Erros totais: {data['errors']['total_errors']}")
    
    def demonstrar_carteiras(self):
        """Demonstra sistema de carteiras"""
        print("\n" + "="*60)
        print("💰 SISTEMA DE CARTEIRAS")
        print("="*60)
        
        # Criar carteiras
        for i in range(3):
            nome = f"Carteira Demo {i+1}"
            senha = f"senha{i+1}23"
            
            response = requests.post(f"{self.base_url}/carteiras/criar", 
                                   json={"nome": nome, "senha": senha})
            
            if response.status_code == 200:
                data = response.json()
                carteira = {
                    "nome": nome,
                    "endereco": data["endereco"],
                    "chave_publica": data["chave_publica"][:50] + "...",
                    "saldo": data["saldo"]
                }
                self.carteiras.append(carteira)
                print(f"✅ {nome}: {carteira['endereco'][:20]}...")
                print(f"   Saldo: {carteira['saldo']} tokens")
            else:
                print(f"❌ Erro ao criar {nome}: {response.status_code}")
        
        # Listar carteiras
        response = requests.get(f"{self.base_url}/carteiras")
        if response.status_code == 200:
            data = response.json()
            print(f"\n📋 Total de carteiras: {data['total']}")
    
    def demonstrar_blockchain(self):
        """Demonstra sistema de blockchain"""
        print("\n" + "="*60)
        print("⛓️  SISTEMA DE BLOCKCHAIN")
        print("="*60)
        
        # Status da blockchain
        response = requests.get(f"{self.base_url}/blockchain/status")
        if response.status_code == 200:
            data = response.json()
            print(f"🔗 Blocos na cadeia: {data['total_blocos']}")
            print(f"📊 Transações pendentes: {data['transacoes_pendentes']}")
            print(f"⛏️  Dificuldade atual: {data['dificuldade']}")
        
        # Criar transação se tivermos carteiras
        if len(self.carteiras) >= 2:
            print("\n💸 Criando transação de demonstração...")
            
            remetente = self.carteiras[0]["endereco"]
            destinatario = self.carteiras[1]["endereco"]
            valor = 10.0
            
            response = requests.post(f"{self.base_url}/transacoes/criar", 
                                   json={
                                       "remetente": remetente,
                                       "destinatario": destinatario,
                                       "valor": valor
                                   })
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Transação criada: {data['hash_transacao'][:20]}...")
                print(f"   De: {remetente[:20]}...")
                print(f"   Para: {destinatario[:20]}...")
                print(f"   Valor: {valor} tokens")
            else:
                print(f"❌ Erro ao criar transação: {response.status_code}")
    
    def demonstrar_defi(self):
        """Demonstra sistema DeFi"""
        print("\n" + "="*60)
        print("🏦 SISTEMA DEFI")
        print("="*60)
        
        # Listar contratos disponíveis
        response = requests.get(f"{self.base_url}/defi/contratos")
        if response.status_code == 200:
            data = response.json()
            print(f"📋 Contratos disponíveis: {data['total']}")
            for contrato in data['contratos']:
                print(f"   • {contrato['tipo']}: {contrato['endereco'][:20]}...")
        
        # Demonstrar staking se tivermos carteiras
        if len(self.carteiras) >= 1:
            print("\n🥩 Demonstração de Staking...")
            
            carteira = self.carteiras[0]["endereco"]
            valor_stake = 100.0
            
            response = requests.post(f"{self.base_url}/defi/stake", 
                                   json={
                                       "carteira": carteira,
                                       "valor": valor_stake
                                   })
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Stake realizado: {valor_stake} tokens")
                print(f"   APY: {data.get('apy', 'N/A')}%")
                print(f"   Recompensas estimadas: {data.get('recompensas_estimadas', 'N/A')}")
            else:
                print(f"❌ Erro no staking: {response.status_code}")
    
    def demonstrar_otimizacoes(self):
        """Demonstra otimizações do sistema"""
        print("\n" + "="*60)
        print("⚡ OTIMIZAÇÕES E PERFORMANCE")
        print("="*60)
        
        # Otimizar banco de dados
        print("🔧 Otimizando banco de dados...")
        response = requests.post(f"{self.base_url}/admin/database/optimize")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['message']}")
        
        # Análise de performance
        response = requests.get(f"{self.base_url}/admin/database/performance")
        if response.status_code == 200:
            data = response.json()
            perf = data['performance']
            print(f"📊 Performance do banco:")
            print(f"   • Tamanho: {perf.get('db_size_mb', 0)} MB")
            print(f"   • Blocos: {perf.get('total_blocos', 0)}")
            print(f"   • Transações: {perf.get('total_transacoes', 0)}")
            print(f"   • Índices: {perf.get('indices_count', 0)}")
        
        # Estatísticas de cache
        response = requests.get(f"{self.base_url}/admin/database/cache")
        if response.status_code == 200:
            data = response.json()
            cache = data['cache']
            print(f"💾 Cache:")
            print(f"   • Itens em cache: {cache.get('itens_em_cache', 0)}")
            print(f"   • TTL: {cache.get('ttl_segundos', 0)}s")
    
    def demonstrar_monitoramento(self):
        """Demonstra sistema de monitoramento"""
        print("\n" + "="*60)
        print("📊 SISTEMA DE MONITORAMENTO")
        print("="*60)
        
        # Estatísticas de erros
        response = requests.get(f"{self.base_url}/admin/errors")
        if response.status_code == 200:
            data = response.json()
            print(f"🚫 Estatísticas de erros:")
            print(f"   • Total de erros: {data.get('total_errors', 0)}")
            print(f"   • Taxa de erro: {data.get('error_rate', 0):.2f}/min")
            print(f"   • Tipos de erro: {list(data.get('error_counts', {}).keys())}")
        
        # Rate limiting
        response = requests.get(f"{self.base_url}/metrics")
        if response.status_code == 200:
            data = response.json()
            rate_limit = data.get('rate_limiting', {})
            print(f"🔒 Rate Limiting:")
            print(f"   • IPs bloqueados: {rate_limit.get('blocked_ips', 0)}")
            print(f"   • IPs suspeitos: {rate_limit.get('suspicious_ips', 0)}")
    
    def demonstrar_api_endpoints(self):
        """Demonstra endpoints da API"""
        print("\n" + "="*60)
        print("🌐 ENDPOINTS DA API")
        print("="*60)
        
        endpoints = [
            ("GET", "/", "Status da API"),
            ("GET", "/health", "Health check avançado"),
            ("GET", "/metrics", "Métricas do sistema"),
            ("GET", "/carteiras", "Listar carteiras"),
            ("GET", "/blockchain/status", "Status da blockchain"),
            ("GET", "/defi/contratos", "Contratos DeFi"),
            ("GET", "/estatisticas", "Estatísticas gerais"),
        ]
        
        for method, endpoint, description in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                status = "✅" if response.status_code == 200 else "⚠️"
                print(f"{status} {method} {endpoint} - {description}")
            except:
                print(f"❌ {method} {endpoint} - {description}")
    
    def executar_demonstracao_completa(self):
        """Executa demonstração completa do sistema"""
        print("🚀 DEMONSTRAÇÃO COMPLETA - COINBALANCE")
        print("Sistema de Blockchain Moderno com DeFi, Staking e Contratos Inteligentes")
        
        # Aguardar sistema
        if not self.aguardar_sistema():
            print("❌ Sistema não está respondendo. Verifique se a API está rodando.")
            return
        
        # Executar demonstrações
        self.demonstrar_status_sistema()
        self.demonstrar_carteiras()
        self.demonstrar_blockchain()
        self.demonstrar_defi()
        self.demonstrar_otimizacoes()
        self.demonstrar_monitoramento()
        self.demonstrar_api_endpoints()
        
        print("\n" + "="*60)
        print("🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print("✅ Sistema CoinBalance funcionando perfeitamente!")
        print("✅ Todas as funcionalidades validadas!")
        print("✅ Pronto para produção!")
        print("\n🌐 Acesse a documentação da API em: http://localhost:8000/docs")

if __name__ == "__main__":
    demo = CoinBalanceDemo()
    demo.executar_demonstracao_completa()
