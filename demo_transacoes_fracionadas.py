#!/usr/bin/env python3
"""
Demonstração do Sistema de Transações Fracionadas CNB
Mostra como usar as novas funcionalidades de negociação de frações
"""

import requests
import json
import time
from typing import Dict, Any

class DemoTranacoesFracionadas:
    """Demonstração das funcionalidades de transações fracionadas"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def aguardar_sistema(self):
        """Aguarda o sistema estar online"""
        print("🔄 Aguardando sistema estar online...")
        max_tentativas = 30
        
        for tentativa in range(max_tentativas):
            try:
                response = self.session.get(f"{self.base_url}/health/simple")
                if response.status_code == 200:
                    print("✅ Sistema online!")
                    return True
            except:
                pass
            
            time.sleep(1)
            print(f"⏳ Tentativa {tentativa + 1}/{max_tentativas}...")
        
        print("❌ Sistema não respondeu")
        return False
    
    def demonstrar_conversao_unidades(self):
        """Demonstra conversão entre diferentes unidades"""
        print("\n🔄 Demonstração de Conversão de Unidades")
        print("=" * 50)
        
        # Informações sobre unidades
        print("\n📊 Informações sobre Unidades:")
        response = self.session.get(f"{self.base_url}/conversao/info")
        if response.status_code == 200:
            info = response.json()
            for unidade, dados in info['unidades_disponiveis'].items():
                print(f"  {dados['simbolo']}: {dados['nome']} - {dados['descricao']}")
        
        # Exemplos de conversão
        exemplos = [
            {"valor": 1.5, "origem": "cnb", "destino": "satoshi"},
            {"valor": 50000000, "origem": "satoshi", "destino": "cnb"},
            {"valor": 0.000001, "origem": "cnb", "destino": "mcnb"},
            {"valor": 1000, "origem": "mcnb", "destino": "cnb"}
        ]
        
        for exemplo in exemplos:
            print(f"\n🔄 Convertendo {exemplo['valor']} {exemplo['origem'].upper()} para {exemplo['destino'].upper()}:")
            
            response = self.session.post(f"{self.base_url}/conversao/unidades", json=exemplo)
            if response.status_code == 200:
                resultado = response.json()
                print(f"  ✅ {resultado['conversao']['valor_origem']} = {resultado['conversao']['valor_destino']}")
                print(f"  📊 Taxa: {resultado['conversao']['taxa_conversao']}")
            else:
                print(f"  ❌ Erro: {response.text}")
    
    def demonstrar_carteiras_fracionadas(self):
        """Demonstra criação e uso de carteiras com frações"""
        print("\n💳 Demonstração de Carteiras Fracionadas")
        print("=" * 50)
        
        # Criar carteiras de teste
        carteiras = []
        for i in range(3):
            nome = f"carteira_teste_{i+1}"
            print(f"\n📝 Criando {nome}...")
            
            response = self.session.post(f"{self.base_url}/carteiras/criar", json={
                "nome": nome,
                "senha": f"senha_{i+1}"
            })
            
            if response.status_code == 200:
                carteira = response.json()
                carteiras.append(carteira)
                print(f"  ✅ Carteira criada: {carteira['endereco']}")
                
                # Mostrar saldo detalhado
                self.mostrar_saldo_detalhado(carteira['endereco'])
            else:
                print(f"  ❌ Erro ao criar carteira: {response.text}")
        
        return carteiras
    
    def mostrar_saldo_detalhado(self, endereco: str):
        """Mostra saldo detalhado em todas as unidades"""
        response = self.session.get(f"{self.base_url}/carteiras/{endereco}/saldo/detalhado")
        if response.status_code == 200:
            saldo = response.json()
            print(f"  💰 Saldo detalhado:")
            print(f"    CNB: {saldo['saldo']['cnb']}")
            print(f"    Satoshi: {saldo['saldo']['satoshi']}")
            print(f"    mCNB: {saldo['saldo']['mcnb']}")
    
    def demonstrar_transacoes_fracionadas(self, carteiras: list):
        """Demonstra transações com valores fracionados"""
        print("\n💸 Demonstração de Transações Fracionadas")
        print("=" * 50)
        
        if len(carteiras) < 2:
            print("❌ Necessário pelo menos 2 carteiras para demonstração")
            return
        
        # Adicionar saldo inicial às carteiras (simulação)
        print("\n💰 Adicionando saldo inicial...")
        for carteira in carteiras:
            # Simular adição de saldo (em um sistema real, isso seria feito via mineração ou transferência)
            print(f"  📈 Adicionando 10.5 CNB para {carteira['endereco']}")
        
        # Exemplos de transações fracionadas
        exemplos_transacoes = [
            {
                "valor": 0.00000001,  # 1 satoshi
                "unidade": "cnb",
                "descricao": "Transação mínima (1 satoshi)"
            },
            {
                "valor": 1000000,  # 1 mCNB
                "unidade": "mcnb",
                "descricao": "Transação em mCNB"
            },
            {
                "valor": 0.12345678,  # Fração decimal
                "unidade": "cnb",
                "descricao": "Transação com 8 casas decimais"
            },
            {
                "valor": 50000000,  # 0.5 CNB em satoshis
                "unidade": "satoshi",
                "descricao": "Transação em satoshis"
            }
        ]
        
        for i, exemplo in enumerate(exemplos_transacoes):
            print(f"\n🔄 Exemplo {i+1}: {exemplo['descricao']}")
            
            # Calcular taxa primeiro
            print(f"  📊 Calculando taxa para {exemplo['valor']} {exemplo['unidade'].upper()}...")
            response = self.session.get(f"{self.base_url}/transacoes/calcular-taxa", 
                                      params={"valor": exemplo['valor'], "unidade": exemplo['unidade']})
            
            if response.status_code == 200:
                taxa_info = response.json()
                print(f"    Taxa necessária: {taxa_info['taxa_cnb']}")
                print(f"    Total necessário: {taxa_info['total_necessario']}")
            
            # Criar transação fracionada
            print(f"  💸 Criando transação...")
            transacao_data = {
                "remetente": carteiras[0]['endereco'],
                "destinatario": carteiras[1]['endereco'],
                "valor": exemplo['valor'],
                "unidade": exemplo['unidade'],
                "dados_extra": {
                    "descricao": exemplo['descricao'],
                    "timestamp": time.time()
                }
            }
            
            response = self.session.post(f"{self.base_url}/transacoes/fracionada", json=transacao_data)
            if response.status_code == 200:
                resultado = response.json()
                print(f"    ✅ Transação criada: {resultado['hash_transacao']}")
                print(f"    📊 Valor original: {resultado['valor_original']}")
                print(f"    💰 Valor CNB: {resultado['valor_cnb']}")
            else:
                print(f"    ❌ Erro na transação: {response.text}")
    
    def demonstrar_precisao_decimal(self):
        """Demonstra a precisão decimal do sistema"""
        print("\n🔢 Demonstração de Precisão Decimal")
        print("=" * 50)
        
        # Testes de precisão
        valores_teste = [
            0.00000001,  # 1 satoshi
            0.0000001,   # 10 satoshis
            0.000001,    # 100 satoshis
            0.00001,     # 1000 satoshis
            0.0001,      # 10000 satoshis
            0.001,       # 100000 satoshis
            0.01,        # 1 milhão de satoshis
            0.1,         # 10 milhões de satoshis
            1.0,         # 100 milhões de satoshis
            1.12345678,  # Valor com 8 casas decimais
            999.99999999 # Valor próximo do máximo
        ]
        
        print("\n📊 Testando precisão com diferentes valores:")
        for valor in valores_teste:
            print(f"\n  Valor: {valor:.8f} CNB")
            
            # Converter para satoshis
            response = self.session.post(f"{self.base_url}/conversao/unidades", json={
                "valor": valor,
                "unidade_origem": "cnb",
                "unidade_destino": "satoshi"
            })
            
            if response.status_code == 200:
                resultado = response.json()
                satoshis = resultado['conversao']['valor_destino'].split()[0]
                print(f"    Satoshis: {satoshis}")
                
                # Converter de volta para CNB
                response2 = self.session.post(f"{self.base_url}/conversao/unidades", json={
                    "valor": float(satoshis),
                    "unidade_origem": "satoshi",
                    "unidade_destino": "cnb"
                })
                
                if response2.status_code == 200:
                    resultado2 = response2.json()
                    valor_convertido = resultado2['conversao']['valor_destino'].split()[0]
                    print(f"    Convertido de volta: {valor_convertido} CNB")
                    
                    # Verificar se há perda de precisão
                    diferenca = abs(valor - float(valor_convertido))
                    if diferenca < 0.00000001:
                        print(f"    ✅ Precisão mantida (diferença: {diferenca:.10f})")
                    else:
                        print(f"    ⚠️ Perda de precisão detectada (diferença: {diferenca:.10f})")
    
    def executar_demonstracao_completa(self):
        """Executa demonstração completa do sistema"""
        print("🚀 Demonstração do Sistema de Transações Fracionadas CNB")
        print("=" * 60)
        
        # Aguardar sistema
        if not self.aguardar_sistema():
            return
        
        # Demonstrações
        self.demonstrar_conversao_unidades()
        carteiras = self.demonstrar_carteiras_fracionadas()
        self.demonstrar_transacoes_fracionadas(carteiras)
        self.demonstrar_precisao_decimal()
        
        print("\n✅ Demonstração concluída!")
        print("\n📋 Resumo das Funcionalidades:")
        print("  • Conversão entre CNB, Satoshi e mCNB")
        print("  • Transações com precisão de 8 casas decimais")
        print("  • Suporte a valores fracionados mínimos (1 satoshi)")
        print("  • Cálculo automático de taxas")
        print("  • Validação rigorosa de transações")
        print("  • Formatação adequada de valores")

if __name__ == "__main__":
    demo = DemoTranacoesFracionadas()
    demo.executar_demonstracao_completa()