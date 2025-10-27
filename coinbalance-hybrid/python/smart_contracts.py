"""
Sistema de Contratos Inteligentes e DeFi
Implementa staking, yield farming, empréstimos e outros protocolos DeFi
"""

import json
import time
from typing import Dict, List, Any, Optional
from database_manager import DatabaseManager


class SmartContract:
    """Contrato inteligente base"""
    
    def __init__(self, endereco: str, criador: str):
        self.endereco = endereco
        self.criador = criador
        self.criado_em = time.time()
        self.estado = {}
        self.funcoes = {}
    
    def executar(self, funcao: str, parametros: Dict, assinante: str) -> Dict:
        """Executa função do contrato"""
        if funcao not in self.funcoes:
            return {'sucesso': False, 'erro': 'Função não encontrada'}
        
        try:
            return self.funcoes[funcao](parametros, assinante)
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}


class StakingContract(SmartContract):
    """Contrato de Staking com recompensas"""
    
    def __init__(self, endereco: str, criador: str, taxa_anual: float = 0.1):
        super().__init__(endereco, criador)
        self.taxa_anual = taxa_anual
        self.stakes = {}  # endereco -> {'valor': float, 'timestamp': float}
        self.total_staked = 0.0
        
        # Definir funções do contrato
        self.funcoes = {
            'stake': self._stake,
            'unstake': self._unstake,
            'claim_rewards': self._claim_rewards,
            'get_stake_info': self._get_stake_info
        }
    
    def _stake(self, parametros: Dict, assinante: str) -> Dict:
        """Faz stake de tokens"""
        valor = float(parametros.get('valor', 0))
        
        if valor <= 0:
            return {'sucesso': False, 'erro': 'Valor inválido'}
        
        # Verificar saldo
        # Implementar verificação de saldo aqui
        
        # Adicionar stake
        if assinante not in self.stakes:
            self.stakes[assinante] = {'valor': 0, 'timestamp': time.time()}
        
        self.stakes[assinante]['valor'] += valor
        self.stakes[assinante]['timestamp'] = time.time()
        self.total_staked += valor
        
        return {
            'sucesso': True,
            'mensagem': f'Stake de {valor} tokens realizado',
            'total_staked': self.stakes[assinante]['valor']
        }
    
    def _unstake(self, parametros: Dict, assinante: str) -> Dict:
        """Remove stake de tokens"""
        valor = float(parametros.get('valor', 0))
        
        if assinante not in self.stakes or self.stakes[assinante]['valor'] < valor:
            return {'sucesso': False, 'erro': 'Saldo de stake insuficiente'}
        
        # Calcular recompensas antes de remover
        recompensas = self._calcular_recompensas(assinante)
        
        # Remover stake
        self.stakes[assinante]['valor'] -= valor
        self.total_staked -= valor
        
        return {
            'sucesso': True,
            'mensagem': f'Unstake de {valor} tokens realizado',
            'recompensas_ganhas': recompensas,
            'total_staked': self.stakes[assinante]['valor']
        }
    
    def _claim_rewards(self, parametros: Dict, assinante: str) -> Dict:
        """Reivindica recompensas de staking"""
        if assinante not in self.stakes:
            return {'sucesso': False, 'erro': 'Nenhum stake encontrado'}
        
        recompensas = self._calcular_recompensas(assinante)
        
        if recompensas <= 0:
            return {'sucesso': False, 'erro': 'Nenhuma recompensa disponível'}
        
        # Resetar timestamp para próximo cálculo
        self.stakes[assinante]['timestamp'] = time.time()
        
        return {
            'sucesso': True,
            'mensagem': f'Recompensas de {recompensas} tokens reivindicadas',
            'recompensas': recompensas
        }
    
    def _get_stake_info(self, parametros: Dict, assinante: str) -> Dict:
        """Obtém informações do stake"""
        if assinante not in self.stakes:
            return {
                'sucesso': True,
                'stake_atual': 0,
                'recompensas_pendentes': 0,
                'apy': self.taxa_anual * 100
            }
        
        recompensas = self._calcular_recompensas(assinante)
        
        return {
            'sucesso': True,
            'stake_atual': self.stakes[assinante]['valor'],
            'recompensas_pendentes': recompensas,
            'apy': self.taxa_anual * 100,
            'total_staked_rede': self.total_staked
        }
    
    def _calcular_recompensas(self, endereco: str) -> float:
        """Calcula recompensas acumuladas"""
        if endereco not in self.stakes:
            return 0.0
        
        stake_info = self.stakes[endereco]
        tempo_decorrido = time.time() - stake_info['timestamp']
        tempo_em_anos = tempo_decorrido / (365 * 24 * 3600)  # Converter para anos
        
        recompensas = stake_info['valor'] * self.taxa_anual * tempo_em_anos
        return recompensas


class LendingContract(SmartContract):
    """Contrato de Empréstimos DeFi"""
    
    def __init__(self, endereco: str, criador: str):
        super().__init__(endereco, criador)
        self.emprestimos = {}  # endereco -> {'valor': float, 'juros': float, 'timestamp': float}
        self.reservas = 0.0
        self.taxa_juros_base = 0.05  # 5% ao ano
        
        self.funcoes = {
            'deposit': self._deposit,
            'withdraw': self._deposit,  # Usar deposit como withdraw por enquanto
            'borrow': self._borrow,
            'repay': self._repay,
            'get_borrow_info': self._get_borrow_info
        }
    
    def _deposit(self, parametros: Dict, assinante: str) -> Dict:
        """Deposita tokens no protocolo de empréstimo"""
        valor = float(parametros.get('valor', 0))
        
        if valor <= 0:
            return {'sucesso': False, 'erro': 'Valor inválido'}
        
        # Implementar lógica de depósito
        self.reservas += valor
        
        return {
            'sucesso': True,
            'mensagem': f'Depósito de {valor} tokens realizado',
            'reservas_totais': self.reservas
        }
    
    def _borrow(self, parametros: Dict, assinante: str) -> Dict:
        """Solicita empréstimo"""
        valor = float(parametros.get('valor', 0))
        colateral = float(parametros.get('colateral', 0))
        
        if valor <= 0 or colateral <= 0:
            return {'sucesso': False, 'erro': 'Valores inválidos'}
        
        # Verificar se há reservas suficientes
        if valor > self.reservas:
            return {'sucesso': False, 'erro': 'Reservas insuficientes'}
        
        # Verificar ratio de colateral (exemplo: 150%)
        ratio_minimo = 1.5
        if colateral < valor * ratio_minimo:
            return {'sucesso': False, 'erro': 'Colateral insuficiente'}
        
        # Criar empréstimo
        self.emprestimos[assinante] = {
            'valor': valor,
            'colateral': colateral,
            'juros': self.taxa_juros_base,
            'timestamp': time.time()
        }
        
        self.reservas -= valor
        
        return {
            'sucesso': True,
            'mensagem': f'Empréstimo de {valor} tokens aprovado',
            'colateral_necessario': colateral
        }
    
    def _repay(self, parametros: Dict, assinante: str) -> Dict:
        """Quita empréstimo"""
        if assinante not in self.emprestimos:
            return {'sucesso': False, 'erro': 'Nenhum empréstimo encontrado'}
        
        emprestimo = self.emprestimos[assinante]
        tempo_decorrido = time.time() - emprestimo['timestamp']
        tempo_em_anos = tempo_decorrido / (365 * 24 * 3600)
        
        # Calcular juros
        juros = emprestimo['valor'] * emprestimo['juros'] * tempo_em_anos
        valor_total = emprestimo['valor'] + juros
        
        # Verificar se tem saldo suficiente
        # Implementar verificação de saldo
        
        # Quitar empréstimo
        self.reservas += valor_total
        del self.emprestimos[assinante]
        
        return {
            'sucesso': True,
            'mensagem': f'Empréstimo quitado. Valor: {emprestimo["valor"]}, Juros: {juros}',
            'valor_pago': valor_total
        }
    
    def _get_borrow_info(self, parametros: Dict, assinante: str) -> Dict:
        """Obtém informações do empréstimo"""
        if assinante not in self.emprestimos:
            return {
                'sucesso': True,
                'tem_emprestimo': False,
                'reservas_disponiveis': self.reservas
            }
        
        emprestimo = self.emprestimos[assinante]
        tempo_decorrido = time.time() - emprestimo['timestamp']
        tempo_em_anos = tempo_decorrido / (365 * 24 * 3600)
        juros_acumulados = emprestimo['valor'] * emprestimo['juros'] * tempo_em_anos
        
        return {
            'sucesso': True,
            'tem_emprestimo': True,
            'valor_emprestado': emprestimo['valor'],
            'juros_acumulados': juros_acumulados,
            'valor_total_devido': emprestimo['valor'] + juros_acumulados,
            'reservas_disponiveis': self.reservas
        }


class ContractManager:
    """Gerenciador de contratos inteligentes"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.contratos: Dict[str, SmartContract] = {}
        self._inicializar_contratos_padrao()
    
    def _inicializar_contratos_padrao(self):
        """Inicializa contratos padrão do sistema"""
        # Contrato de Staking
        staking_contract = StakingContract(
            endereco="STAKING_CONTRACT_001",
            criador="SYSTEM",
            taxa_anual=0.12  # 12% APY
        )
        self.contratos["STAKING_CONTRACT_001"] = staking_contract
        
        # Contrato de Empréstimos
        lending_contract = LendingContract(
            endereco="LENDING_CONTRACT_001",
            criador="SYSTEM"
        )
        self.contratos["LENDING_CONTRACT_001"] = lending_contract
    
    def executar_contrato(self, endereco_contrato: str, funcao: str, 
                         parametros: Dict, assinante: str) -> Dict:
        """Executa função de um contrato"""
        if endereco_contrato not in self.contratos:
            return {'sucesso': False, 'erro': 'Contrato não encontrado'}
        
        contrato = self.contratos[endereco_contrato]
        return contrato.executar(funcao, parametros, assinante)
    
    def criar_contrato(self, tipo: str, endereco: str, criador: str, 
                      parametros: Dict = None) -> Dict:
        """Cria novo contrato inteligente"""
        try:
            if tipo == "staking":
                contrato = StakingContract(endereco, criador)
            elif tipo == "lending":
                contrato = LendingContract(endereco, criador)
            else:
                return {'sucesso': False, 'erro': 'Tipo de contrato não suportado'}
            
            self.contratos[endereco] = contrato
            return {'sucesso': True, 'mensagem': 'Contrato criado com sucesso'}
            
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}
    
    def listar_contratos(self) -> List[Dict]:
        """Lista todos os contratos disponíveis"""
        return [
            {
                'endereco': endereco,
                'tipo': type(contrato).__name__,
                'criador': contrato.criador,
                'criado_em': contrato.criado_em
            }
            for endereco, contrato in self.contratos.items()
        ]
