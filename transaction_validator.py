"""
Validador de Transações e Prevenção de Gastos Duplos
Implementa validação rigorosa de saldos e integridade
"""

import hashlib
import json
import time
from typing import Dict, List, Set, Optional, Any
from database_manager import DatabaseManager
from crypto_utils import CryptoUtils


class TransactionValidator:
    """Validador de transações com prevenção de gastos duplos"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.transacoes_pendentes: Set[str] = set()
        self.utxos: Dict[str, List[Dict]] = {}  # Unspent Transaction Outputs
    
    def validar_transacao(self, transacao: Dict[str, Any]) -> Dict[str, Any]:
        """Valida uma transação completa"""
        resultado = {
            'valida': False,
            'erros': [],
            'avisos': []
        }
        
        # Verificar estrutura básica
        if not self._validar_estrutura(transacao):
            resultado['erros'].append("Estrutura da transação inválida")
            return resultado
        
        # Verificar assinatura digital
        if not self._validar_assinatura(transacao):
            resultado['erros'].append("Assinatura digital inválida")
            return resultado
        
        # Verificar saldo do remetente
        if not self._validar_saldo(transacao):
            resultado['erros'].append("Saldo insuficiente")
            return resultado
        
        # Verificar gastos duplos
        if not self._verificar_gastos_duplos(transacao):
            resultado['erros'].append("Tentativa de gasto duplo detectada")
            return resultado
        
        # Verificar valor mínimo
        if not self._validar_valor_minimo(transacao):
            resultado['avisos'].append("Valor muito baixo para transação")
        
        # Verificar taxa de transação
        if not self._validar_taxa(transacao):
            resultado['erros'].append("Taxa de transação insuficiente")
            return resultado
        
        resultado['valida'] = True
        return resultado
    
    def _validar_estrutura(self, transacao: Dict) -> bool:
        """Valida estrutura básica da transação"""
        campos_obrigatorios = [
            'remetente', 'destinatario', 'valor', 'timestamp', 
            'assinatura', 'chave_publica'
        ]
        
        return all(campo in transacao for campo in campos_obrigatorios)
    
    def _validar_assinatura(self, transacao: Dict) -> bool:
        """Valida assinatura digital da transação"""
        try:
            dados_verificacao = {k: v for k, v in transacao.items() 
                               if k not in ['assinatura', 'chave_publica']}
            
            return CryptoUtils.verificar_assinatura(
                dados_verificacao,
                transacao['assinatura'],
                transacao['chave_publica']
            )
        except Exception:
            return False
    
    def _validar_saldo(self, transacao: Dict) -> bool:
        """Valida se o remetente tem saldo suficiente"""
        try:
            saldo_atual = self.db_manager.obter_saldo_carteira(transacao['remetente'])
            valor_transacao = float(transacao['valor'])
            taxa = self._calcular_taxa(transacao)
            
            return saldo_atual >= (valor_transacao + taxa)
        except Exception:
            return False
    
    def _verificar_gastos_duplos(self, transacao: Dict) -> bool:
        """Verifica se não há tentativa de gasto duplo"""
        hash_transacao = self._gerar_hash_transacao(transacao)
        
        # Verificar se transação já foi processada
        if hash_transacao in self.transacoes_pendentes:
            return False
        
        # Verificar se remetente não tem transações pendentes
        if self._tem_transacoes_pendentes(transacao['remetente']):
            return False
        
        return True
    
    def _validar_valor_minimo(self, transacao: Dict) -> bool:
        """Valida valor mínimo da transação"""
        valor_minimo = 0.001  # 0.001 moedas
        return float(transacao['valor']) >= valor_minimo
    
    def _validar_taxa(self, transacao: Dict) -> bool:
        """Valida taxa de transação"""
        taxa_necessaria = self._calcular_taxa(transacao)
        taxa_fornecida = transacao.get('taxa', 0)
        
        return float(taxa_fornecida) >= taxa_necessaria
    
    def _calcular_taxa(self, transacao: Dict) -> float:
        """Calcula taxa necessária para a transação"""
        # Taxa base + taxa por tamanho da transação
        taxa_base = 0.001
        tamanho_transacao = len(json.dumps(transacao))
        taxa_tamanho = tamanho_transacao * 0.000001
        
        return taxa_base + taxa_tamanho
    
    def _gerar_hash_transacao(self, transacao: Dict) -> str:
        """Gera hash único da transação"""
        dados_hash = {
            'remetente': transacao['remetente'],
            'destinatario': transacao['destinatario'],
            'valor': transacao['valor'],
            'timestamp': transacao['timestamp']
        }
        
        transacao_str = json.dumps(dados_hash, sort_keys=True)
        return hashlib.sha256(transacao_str.encode()).hexdigest()
    
    def _tem_transacoes_pendentes(self, endereco: str) -> bool:
        """Verifica se endereço tem transações pendentes"""
        # Implementar verificação de transações pendentes
        return False
    
    def processar_transacao(self, transacao: Dict) -> bool:
        """Processa transação validada"""
        try:
            # Adicionar à lista de pendentes
            hash_transacao = self._gerar_hash_transacao(transacao)
            self.transacoes_pendentes.add(hash_transacao)
            
            # Atualizar saldos
            self._atualizar_saldos(transacao)
            
            return True
        except Exception as e:
            print(f"Erro ao processar transação: {e}")
            return False
    
    def _atualizar_saldos(self, transacao: Dict):
        """Atualiza saldos das carteiras"""
        remetente = transacao['remetente']
        destinatario = transacao['destinatario']
        valor = float(transacao['valor'])
        taxa = self._calcular_taxa(transacao)
        
        # Debitar do remetente
        saldo_remetente = self.db_manager.obter_saldo_carteira(remetente)
        novo_saldo_remetente = saldo_remetente - valor - taxa
        self.db_manager.atualizar_saldo_carteira(remetente, novo_saldo_remetente)
        
        # Creditar no destinatário
        saldo_destinatario = self.db_manager.obter_saldo_carteira(destinatario)
        novo_saldo_destinatario = saldo_destinatario + valor
        self.db_manager.atualizar_saldo_carteira(destinatario, novo_saldo_destinatario)
    
    def obter_historico_transacoes(self, endereco: str) -> List[Dict]:
        """Obtém histórico de transações de uma carteira"""
        try:
            # Implementar busca no banco de dados
            return []
        except Exception:
            return []
    
    def obter_saldo_total(self, endereco: str) -> float:
        """Obtém saldo total de uma carteira"""
        return self.db_manager.obter_saldo_carteira(endereco)
    
    def limpar_transacoes_pendentes(self):
        """Limpa transações pendentes antigas"""
        # Implementar limpeza de transações antigas
        pass
