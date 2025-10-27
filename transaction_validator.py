"""
Validador de Transações e Prevenção de Gastos Duplos
Implementa validação rigorosa de saldos e integridade com suporte a frações decimais
"""

import hashlib
import json
import time
import decimal
from typing import Dict, List, Set, Optional, Any
from database_manager import DatabaseManager
from crypto_utils import CryptoUtils


class TransactionValidator:
    """Validador de transações com prevenção de gastos duplos e suporte a frações"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.transacoes_pendentes: Set[str] = set()
        self.utxos: Dict[str, List[Dict]] = {}  # Unspent Transaction Outputs
        
        # Configurações para precisão decimal
        self.precision = 8  # 8 casas decimais para CNB
        self.min_transaction_value = decimal.Decimal('0.00000001')  # 1 satoshi equivalente
        self.max_transaction_value = decimal.Decimal('100000000')  # 100M CNB máximo
    
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
        
        # Verificar valor da transação
        if not self._validar_valor_transacao(transacao['valor']):
            resultado['erros'].append("Valor da transação fora dos limites permitidos")
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
        """Valida se o remetente tem saldo suficiente com precisão decimal"""
        try:
            saldo_atual = decimal.Decimal(str(self.db_manager.obter_saldo_carteira(transacao['remetente'])))
            valor_transacao = decimal.Decimal(str(transacao['valor']))
            taxa = self._calcular_taxa_decimal(transacao)
            
            # Arredondar para a precisão configurada
            saldo_atual = saldo_atual.quantize(decimal.Decimal('0.00000001'))
            valor_total = (valor_transacao + taxa).quantize(decimal.Decimal('0.00000001'))
            
            return saldo_atual >= valor_total
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
        """Atualiza saldos das carteiras com precisão decimal"""
        remetente = transacao['remetente']
        destinatario = transacao['destinatario']
        valor = decimal.Decimal(str(transacao['valor']))
        taxa = self._calcular_taxa_decimal(transacao)
        
        # Debitar do remetente
        saldo_remetente = decimal.Decimal(str(self.db_manager.obter_saldo_carteira(remetente)))
        novo_saldo_remetente = saldo_remetente - valor - taxa
        self.db_manager.atualizar_saldo_carteira(remetente, float(novo_saldo_remetente.quantize(decimal.Decimal('0.00000001'))))
        
        # Creditar no destinatário
        saldo_destinatario = decimal.Decimal(str(self.db_manager.obter_saldo_carteira(destinatario)))
        novo_saldo_destinatario = saldo_destinatario + valor
        self.db_manager.atualizar_saldo_carteira(destinatario, float(novo_saldo_destinatario.quantize(decimal.Decimal('0.00000001'))))
    
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
    
    def _calcular_taxa_decimal(self, transacao: Dict) -> decimal.Decimal:
        """Calcula taxa da transação com precisão decimal"""
        valor = decimal.Decimal(str(transacao['valor']))
        taxa_base = decimal.Decimal('0.001')  # 0.1%
        
        # Taxa mínima de 0.00000001 CNB
        taxa_calculada = valor * taxa_base
        taxa_minima = decimal.Decimal('0.00000001')
        
        return max(taxa_calculada, taxa_minima).quantize(decimal.Decimal('0.00000001'))
    
    def _validar_valor_transacao(self, valor: float) -> bool:
        """Valida se o valor da transação está dentro dos limites"""
        try:
            valor_decimal = decimal.Decimal(str(valor))
            return (self.min_transaction_value <= valor_decimal <= self.max_transaction_value)
        except Exception:
            return False
    
    def formatar_valor_cnb(self, valor: float) -> str:
        """Formata valor CNB com precisão adequada"""
        try:
            valor_decimal = decimal.Decimal(str(valor))
            return f"{valor_decimal.quantize(decimal.Decimal('0.00000001')):.8f} CNB"
        except Exception:
            return f"{valor:.8f} CNB"
    
    def converter_para_unidades(self, valor_cnb: float, unidade: str = "satoshi") -> float:
        """Converte CNB para diferentes unidades"""
        try:
            valor_decimal = decimal.Decimal(str(valor_cnb))
            
            if unidade == "satoshi":
                # 1 CNB = 100,000,000 satoshis
                return float(valor_decimal * decimal.Decimal('100000000'))
            elif unidade == "mcnb":
                # 1 CNB = 1,000,000 mCNB (micro CNB)
                return float(valor_decimal * decimal.Decimal('1000000'))
            elif unidade == "cnb":
                return float(valor_decimal)
            else:
                return float(valor_decimal)
        except Exception:
            return valor_cnb
    
    def converter_de_unidades(self, valor: float, unidade: str = "satoshi") -> float:
        """Converte de diferentes unidades para CNB"""
        try:
            valor_decimal = decimal.Decimal(str(valor))
            
            if unidade == "satoshi":
                # 1 satoshi = 0.00000001 CNB
                return float(valor_decimal / decimal.Decimal('100000000'))
            elif unidade == "mcnb":
                # 1 mCNB = 0.000001 CNB
                return float(valor_decimal / decimal.Decimal('1000000'))
            elif unidade == "cnb":
                return float(valor_decimal)
            else:
                return float(valor_decimal)
        except Exception:
            return valor
    
    def limpar_transacoes_pendentes(self):
        """Limpa transações pendentes antigas"""
        # Implementar limpeza de transações antigas
        pass
