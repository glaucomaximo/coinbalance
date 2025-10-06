"""
Testes de Segurança e Auditoria
Implementa testes automatizados para validação de segurança
"""

import pytest
import json
import time
from unittest.mock import Mock, patch
import sys
import os

# Adicionar diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crypto_utils import CryptoUtils
from wallet_system import Carteira, GerenciadorCarteiras
from transaction_validator import TransactionValidator
from database_manager import DatabaseManager


class TestCryptoUtils:
    """Testes para utilitários de criptografia"""
    
    def test_gerar_par_chaves(self):
        """Testa geração de par de chaves"""
        private_key, public_key = CryptoUtils.gerar_par_chaves()
        
        assert private_key is not None
        assert public_key is not None
        assert isinstance(private_key, str)
        assert isinstance(public_key, str)
        assert "BEGIN PRIVATE KEY" in private_key
        assert "BEGIN PUBLIC KEY" in public_key
    
    def test_assinatura_valida(self):
        """Testa assinatura e verificação de transação"""
        private_key, public_key = CryptoUtils.gerar_par_chaves()
        
        transacao = {
            'remetente': 'endereco1',
            'destinatario': 'endereco2',
            'valor': 100.0,
            'timestamp': time.time()
        }
        
        # Assinar transação
        assinatura = CryptoUtils.assinar_transacao(transacao, private_key)
        assert assinatura is not None
        
        # Verificar assinatura
        valida = CryptoUtils.verificar_assinatura(transacao, assinatura, public_key)
        assert valida is True
    
    def test_assinatura_invalida(self):
        """Testa verificação de assinatura inválida"""
        private_key1, public_key1 = CryptoUtils.gerar_par_chaves()
        private_key2, public_key2 = CryptoUtils.gerar_par_chaves()
        
        transacao = {
            'remetente': 'endereco1',
            'destinatario': 'endereco2',
            'valor': 100.0,
            'timestamp': time.time()
        }
        
        # Assinar com uma chave
        assinatura = CryptoUtils.assinar_transacao(transacao, private_key1)
        
        # Verificar com chave diferente
        valida = CryptoUtils.verificar_assinatura(transacao, assinatura, public_key2)
        assert valida is False
    
    def test_hash_duplo(self):
        """Testa geração de hash duplo"""
        dados = "teste de hash duplo"
        hash_resultado = CryptoUtils.gerar_hash_duplo(dados)
        
        assert hash_resultado is not None
        assert isinstance(hash_resultado, str)
        assert len(hash_resultado) == 64  # SHA-256 hex length
    
    def test_derivar_chave_maestra(self):
        """Testa derivação de chave mestra"""
        senha = "senha_teste"
        salt = CryptoUtils.gerar_salt()
        
        chave = CryptoUtils.derivar_chave_maestra(senha, salt)
        
        assert chave is not None
        assert isinstance(chave, bytes)
        assert len(chave) == 32  # 256 bits


class TestCarteira:
    """Testes para sistema de carteiras"""
    
    def test_criar_carteira(self):
        """Testa criação de carteira"""
        carteira = Carteira()
        
        assert carteira.private_key is not None
        assert carteira.public_key is not None
        assert carteira.endereco is not None
        assert carteira.saldo == 0.0
    
    def test_criar_transacao(self):
        """Testa criação de transação"""
        carteira = Carteira()
        carteira.atualizar_saldo(100.0)  # Adicionar saldo
        destinatario = "endereco_destinatario"
        valor = 50.0
        
        transacao = carteira.criar_transacao(destinatario, valor)
        
        assert transacao['remetente'] == carteira.endereco
        assert transacao['destinatario'] == destinatario
        assert transacao['valor'] == valor
        assert 'assinatura' in transacao
        assert 'chave_publica' in transacao
    
    def test_verificar_transacao(self):
        """Testa verificação de transação"""
        carteira = Carteira()
        carteira.atualizar_saldo(100.0)  # Adicionar saldo
        destinatario = "endereco_destinatario"
        valor = 50.0
        
        transacao = carteira.criar_transacao(destinatario, valor)
        valida = carteira.verificar_transacao(transacao)
        
        assert valida is True
    
    def test_verificar_transacao_invalida(self):
        """Testa verificação de transação inválida"""
        carteira1 = Carteira()
        carteira1.atualizar_saldo(100.0)  # Adicionar saldo
        carteira2 = Carteira()
        
        transacao = carteira1.criar_transacao("destinatario", 50.0)
        
        # Modificar assinatura
        transacao['assinatura'] = "assinatura_falsa"
        
        valida = carteira2.verificar_transacao(transacao)
        assert valida is False
    
    def test_atualizar_saldo(self):
        """Testa atualização de saldo"""
        carteira = Carteira()
        valor_inicial = carteira.saldo
        
        carteira.atualizar_saldo(100.0)
        assert carteira.saldo == valor_inicial + 100.0
        
        carteira.atualizar_saldo(-50.0)
        assert carteira.saldo == valor_inicial + 50.0


class TestTransactionValidator:
    """Testes para validador de transações"""
    
    def setup_method(self):
        """Configuração para cada teste"""
        self.db_manager = Mock(spec=DatabaseManager)
        self.validator = TransactionValidator(self.db_manager)
    
    def test_validar_estrutura_valida(self):
        """Testa validação de estrutura válida"""
        transacao = {
            'remetente': 'endereco1',
            'destinatario': 'endereco2',
            'valor': 100.0,
            'timestamp': time.time(),
            'assinatura': 'assinatura_teste',
            'chave_publica': 'chave_publica_teste'
        }
        
        valida = self.validator._validar_estrutura(transacao)
        assert valida is True
    
    def test_validar_estrutura_invalida(self):
        """Testa validação de estrutura inválida"""
        transacao = {
            'remetente': 'endereco1',
            'destinatario': 'endereco2',
            'valor': 100.0
            # Faltam campos obrigatórios
        }
        
        valida = self.validator._validar_estrutura(transacao)
        assert valida is False
    
    def test_validar_saldo_suficiente(self):
        """Testa validação de saldo suficiente"""
        transacao = {
            'remetente': 'endereco1',
            'destinatario': 'endereco2',
            'valor': 50.0,
            'timestamp': time.time(),
            'assinatura': 'assinatura_teste',
            'chave_publica': 'chave_publica_teste'
        }
        
        # Mock saldo suficiente
        self.db_manager.obter_saldo_carteira.return_value = 100.0
        
        valida = self.validator._validar_saldo(transacao)
        assert valida is True
    
    def test_validar_saldo_insuficiente(self):
        """Testa validação de saldo insuficiente"""
        transacao = {
            'remetente': 'endereco1',
            'destinatario': 'endereco2',
            'valor': 150.0,
            'timestamp': time.time(),
            'assinatura': 'assinatura_teste',
            'chave_publica': 'chave_publica_teste'
        }
        
        # Mock saldo insuficiente
        self.db_manager.obter_saldo_carteira.return_value = 100.0
        
        valida = self.validator._validar_saldo(transacao)
        assert valida is False
    
    def test_verificar_gastos_duplos(self):
        """Testa verificação de gastos duplos"""
        transacao = {
            'remetente': 'endereco1',
            'destinatario': 'endereco2',
            'valor': 50.0,
            'timestamp': time.time()
        }
        
        # Primeira verificação deve passar
        valida1 = self.validator._verificar_gastos_duplos(transacao)
        assert valida1 is True
        
        # Adicionar à lista de pendentes
        hash_transacao = self.validator._gerar_hash_transacao(transacao)
        self.validator.transacoes_pendentes.add(hash_transacao)
        
        # Segunda verificação deve falhar
        valida2 = self.validator._verificar_gastos_duplos(transacao)
        assert valida2 is False
    
    def test_calcular_taxa(self):
        """Testa cálculo de taxa de transação"""
        transacao = {
            'remetente': 'endereco1',
            'destinatario': 'endereco2',
            'valor': 100.0,
            'timestamp': time.time()
        }
        
        taxa = self.validator._calcular_taxa(transacao)
        assert taxa > 0
        assert isinstance(taxa, float)


class TestDatabaseManager:
    """Testes para gerenciador de banco de dados"""
    
    def setup_method(self):
        """Configuração para cada teste"""
        self.db_manager = DatabaseManager("test_blockchain.db")
    
    def teardown_method(self):
        """Limpeza após cada teste"""
        import os
        if os.path.exists("test_blockchain.db"):
            os.remove("test_blockchain.db")
    
    def test_inicializar_banco(self):
        """Testa inicialização do banco de dados"""
        # Verificar se tabelas foram criadas
        import sqlite3
        conn = sqlite3.connect("test_blockchain.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = [row[0] for row in cursor.fetchall()]
        
        assert 'blocos' in tabelas
        assert 'transacoes' in tabelas
        assert 'carteiras' in tabelas
        assert 'nos_rede' in tabelas
        
        conn.close()
    
    def test_salvar_bloco(self):
        """Testa salvamento de bloco"""
        bloco = {
            'indice': 1,
            'carimbo_temporal': time.time(),
            'fragmento_anterior': 'hash_anterior',
            'hash_atual': 'hash_atual',
            'prova': 12345,
            'transacoes': []
        }
        
        sucesso = self.db_manager.salvar_bloco(bloco)
        assert sucesso is True
        
        # Verificar se bloco foi salvo
        bloco_salvo = self.db_manager.obter_bloco(1)
        assert bloco_salvo is not None
        assert bloco_salvo['indice'] == 1
    
    def test_atualizar_saldo_carteira(self):
        """Testa atualização de saldo de carteira"""
        endereco = "endereco_teste"
        saldo = 100.0
        
        sucesso = self.db_manager.atualizar_saldo_carteira(endereco, saldo)
        assert sucesso is True
        
        saldo_obtido = self.db_manager.obter_saldo_carteira(endereco)
        assert saldo_obtido == saldo
    
    def test_obter_ultimo_bloco(self):
        """Testa obtenção do último bloco"""
        # Inserir alguns blocos
        for i in range(3):
            bloco = {
                'indice': i + 1,
                'carimbo_temporal': time.time(),
                'fragmento_anterior': f'hash_{i}',
                'hash_atual': f'hash_{i+1}',
                'prova': 12345 + i,
                'transacoes': []
            }
            self.db_manager.salvar_bloco(bloco)
        
        ultimo_bloco = self.db_manager.obter_ultimo_bloco()
        assert ultimo_bloco is not None
        assert ultimo_bloco['indice'] == 3


class TestSecurityAudit:
    """Testes de auditoria de segurança"""
    
    def test_auditoria_chaves_privadas(self):
        """Testa se chaves privadas são geradas com segurança"""
        chaves_geradas = []
        
        # Gerar várias chaves
        for _ in range(10):
            private_key, public_key = CryptoUtils.gerar_par_chaves()
            chaves_geradas.append((private_key, public_key))
        
        # Verificar se todas são únicas
        private_keys = [pk for pk, _ in chaves_geradas]
        public_keys = [pk for _, pk in chaves_geradas]
        
        assert len(set(private_keys)) == 10  # Todas únicas
        assert len(set(public_keys)) == 10  # Todas únicas
    
    def test_auditoria_assinaturas(self):
        """Testa integridade das assinaturas"""
        private_key, public_key = CryptoUtils.gerar_par_chaves()
        
        # Testar com diferentes transações
        transacoes = [
            {'remetente': 'A', 'destinatario': 'B', 'valor': 100},
            {'remetente': 'B', 'destinatario': 'C', 'valor': 50},
            {'remetente': 'C', 'destinatario': 'A', 'valor': 25}
        ]
        
        for transacao in transacoes:
            assinatura = CryptoUtils.assinar_transacao(transacao, private_key)
            valida = CryptoUtils.verificar_assinatura(transacao, assinatura, public_key)
            assert valida is True
    
    def test_auditoria_gastos_duplos(self):
        """Testa prevenção de gastos duplos"""
        db_manager = Mock(spec=DatabaseManager)
        validator = TransactionValidator(db_manager)
        
        transacao = {
            'remetente': 'endereco1',
            'destinatario': 'endereco2',
            'valor': 50.0,
            'timestamp': time.time()
        }
        
        # Primeira tentativa deve passar
        valida1 = validator._verificar_gastos_duplos(transacao)
        assert valida1 is True
        
        # Adicionar à lista de pendentes
        hash_transacao = validator._gerar_hash_transacao(transacao)
        validator.transacoes_pendentes.add(hash_transacao)
        
        # Segunda tentativa deve falhar
        valida2 = validator._verificar_gastos_duplos(transacao)
        assert valida2 is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
