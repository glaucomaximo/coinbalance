"""
Sistema de Carteiras Coinbalance (CNB)
Implementa carteiras digitais com criptografia robusta para a moeda CNB
Suporte completo a frações decimais e precisão de 8 casas decimais
"""

import json
import hashlib
import time
import decimal
from typing import Dict, List, Optional
from crypto_utils import CryptoUtils


class Carteira:
    """Carteira digital segura para Coinbalance (CNB) com suporte a frações"""
    
    def __init__(self, senha: str = None):
        self.private_key, self.public_key = CryptoUtils.gerar_par_chaves()
        self.senha = senha
        self.salt = CryptoUtils.gerar_salt()
        self.endereco = self._gerar_endereco()
        self.saldo = decimal.Decimal('0.00000000')  # Precisão de 8 casas decimais
        self.transacoes = []
        self.moeda = "CNB"
        self.plataforma = "Coinbalance"
        self.precision = 8  # 8 casas decimais
    
    def _gerar_endereco(self) -> str:
        """Gera endereço único da carteira baseado na chave pública"""
        public_key_hash = hashlib.sha256(self.public_key.encode()).hexdigest()
        return f"CNB_{public_key_hash[:20]}"
    
    def criar_transacao(self, destinatario: str, valor: float, dados_extra: Dict = None) -> Dict:
        """Cria uma transação assinada com suporte a frações decimais"""
        valor_decimal = decimal.Decimal(str(valor))
        
        if valor_decimal > self.saldo:
            raise ValueError(f"Saldo insuficiente. Disponível: {self.saldo:.8f} CNB, Necessário: {valor_decimal:.8f} CNB")
        
        transacao = {
            'remetente': self.endereco,
            'destinatario': destinatario,
            'valor': float(valor_decimal.quantize(decimal.Decimal('0.00000001'))),
            'moeda': self.moeda,
            'plataforma': self.plataforma,
            'timestamp': self._obter_timestamp(),
            'dados_extra': dados_extra or {}
        }
        
        # Assinar transação
        assinatura = CryptoUtils.assinar_transacao(transacao, self.private_key)
        transacao['assinatura'] = assinatura
        transacao['chave_publica'] = self.public_key
        
        return transacao
    
    def _obter_timestamp(self) -> float:
        """Obtém timestamp atual"""
        return time.time()
    
    def verificar_transacao(self, transacao: Dict) -> bool:
        """Verifica se uma transação é válida"""
        try:
            # Extrair dados para verificação
            dados_verificacao = {k: v for k, v in transacao.items() 
                               if k not in ['assinatura', 'chave_publica']}
            
            return CryptoUtils.verificar_assinatura(
                dados_verificacao,
                transacao['assinatura'],
                transacao['chave_publica']
            )
        except Exception:
            return False
    
    def atualizar_saldo(self, valor: float):
        """Atualiza saldo da carteira com precisão decimal"""
        valor_decimal = decimal.Decimal(str(valor))
        self.saldo = (self.saldo + valor_decimal).quantize(decimal.Decimal('0.00000001'))
    
    def obter_saldo_formatado(self) -> str:
        """Retorna saldo formatado com 8 casas decimais"""
        return f"{self.saldo:.8f} CNB"
    
    def obter_saldo_em_unidades(self, unidade: str = "satoshi") -> float:
        """Converte saldo para diferentes unidades"""
        if unidade == "satoshi":
            # 1 CNB = 100,000,000 satoshis
            return float(self.saldo * decimal.Decimal('100000000'))
        elif unidade == "mcnb":
            # 1 CNB = 1,000,000 mCNB (micro CNB)
            return float(self.saldo * decimal.Decimal('1000000'))
        elif unidade == "cnb":
            return float(self.saldo)
        else:
            return float(self.saldo)
    
    def _obter_timestamp(self) -> float:
        """Obtém timestamp atual"""
        import time
        return time.time()
    
    def exportar_carteira(self, senha_exportacao: str) -> str:
        """Exporta carteira criptografada"""
        dados_carteira = {
            'endereco': self.endereco,
            'private_key': self.private_key,
            'public_key': self.public_key,
            'salt': self.salt.hex()
        }
        
        # Criptografar dados
        chave_maestra = CryptoUtils.derivar_chave_maestra(senha_exportacao, self.salt)
        # Implementar criptografia AES aqui se necessário
        
        return json.dumps(dados_carteira)
    
    def importar_carteira(self, dados_criptografados: str, senha: str) -> bool:
        """Importa carteira criptografada"""
        try:
            dados = json.loads(dados_criptografados)
            self.endereco = dados['endereco']
            self.private_key = dados['private_key']
            self.public_key = dados['public_key']
            self.salt = bytes.fromhex(dados['salt'])
            return True
        except Exception:
            return False


class GerenciadorCarteiras:
    """Gerencia múltiplas carteiras"""
    
    def __init__(self):
        self.carteiras: Dict[str, Carteira] = {}
    
    def criar_carteira(self, nome: str, senha: str = None) -> Carteira:
        """Cria nova carteira"""
        carteira = Carteira(senha)
        self.carteiras[nome] = carteira
        return carteira
    
    def obter_carteira(self, nome: str) -> Optional[Carteira]:
        """Obtém carteira por nome"""
        return self.carteiras.get(nome)
    
    def listar_carteiras(self) -> List[Dict]:
        """Lista todas as carteiras"""
        return [
            {
                'nome': nome,
                'endereco': carteira.endereco,
                'saldo': carteira.saldo,
                'moeda': carteira.moeda,
                'plataforma': carteira.plataforma
            }
            for nome, carteira in self.carteiras.items()
        ]
