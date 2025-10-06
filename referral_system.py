"""
Sistema de Referência Viral - CoinBalance
Implementa programa de indicação com cashback e recompensas
"""

import hashlib
import time
import json
from typing import Dict, List, Any, Optional
from database_manager import DatabaseManager


class ReferralSystem:
    """Sistema de referência viral para CoinBalance"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.cashback_rate_referrer = 0.10  # 10% para quem indica
        self.cashback_rate_referred = 0.05  # 5% para quem é indicado
        self.bonus_new_user = 100.0  # $100 para novos usuários
        self.affiliate_rate = 0.20  # 20% para afiliados
        
    def gerar_codigo_referencia(self, usuario_id: str) -> str:
        """Gera código único de referência para usuário"""
        timestamp = str(int(time.time()))
        dados = f"{usuario_id}_{timestamp}"
        codigo = hashlib.sha256(dados.encode()).hexdigest()[:8].upper()
        return f"CB{codigo}"
    
    def registrar_referencia(self, referrer_id: str, referred_id: str) -> Dict[str, Any]:
        """Registra nova referência"""
        try:
            # Verificar se usuário já foi indicado
            if self._usuario_ja_indicado(referred_id):
                return {
                    'sucesso': False,
                    'erro': 'Usuário já foi indicado anteriormente'
                }
            
            # Verificar se não está se auto-indicando
            if referrer_id == referred_id:
                return {
                    'sucesso': False,
                    'erro': 'Não é possível se auto-indicar'
                }
            
            # Registrar referência
            referencia = {
                'referrer_id': referrer_id,
                'referred_id': referred_id,
                'timestamp': time.time(),
                'status': 'ativa',
                'cashback_pago': False
            }
            
            # Salvar no banco
            self._salvar_referencia(referencia)
            
            # Aplicar bônus para novo usuário
            self._aplicar_bonus_novo_usuario(referred_id)
            
            return {
                'sucesso': True,
                'mensagem': 'Referência registrada com sucesso',
                'bonus_aplicado': self.bonus_new_user
            }
            
        except Exception as e:
            return {
                'sucesso': False,
                'erro': str(e)
            }
    
    def processar_cashback(self, transacao_id: str, valor: float) -> Dict[str, Any]:
        """Processa cashback para referências ativas"""
        try:
            # Buscar referências ativas
            referencias = self._buscar_referencias_ativas()
            
            cashbacks_pagos = []
            
            for referencia in referencias:
                # Calcular cashback
                cashback_referrer = valor * self.cashback_rate_referrer
                cashback_referred = valor * self.cashback_rate_referred
                
                # Pagar cashback para quem indicou
                if cashback_referrer > 0:
                    self._pagar_cashback(
                        referencia['referrer_id'],
                        cashback_referrer,
                        f"Cashback por indicação - Transação {transacao_id}"
                    )
                    cashbacks_pagos.append({
                        'usuario': referencia['referrer_id'],
                        'valor': cashback_referrer,
                        'tipo': 'referrer'
                    })
                
                # Pagar cashback para quem foi indicado
                if cashback_referred > 0:
                    self._pagar_cashback(
                        referencia['referred_id'],
                        cashback_referred,
                        f"Cashback por ser indicado - Transação {transacao_id}"
                    )
                    cashbacks_pagos.append({
                        'usuario': referencia['referred_id'],
                        'valor': cashback_referred,
                        'tipo': 'referred'
                    })
            
            return {
                'sucesso': True,
                'cashbacks_pagos': cashbacks_pagos,
                'total_pago': sum(cb['valor'] for cb in cashbacks_pagos)
            }
            
        except Exception as e:
            return {
                'sucesso': False,
                'erro': str(e)
            }
    
    def obter_estatisticas_referencia(self, usuario_id: str) -> Dict[str, Any]:
        """Obtém estatísticas de referência do usuário"""
        try:
            # Buscar referências do usuário
            referencias = self._buscar_referencias_usuario(usuario_id)
            
            # Calcular estatísticas
            total_indicacoes = len(referencias)
            indicacoes_ativas = len([r for r in referencias if r['status'] == 'ativa'])
            total_cashback = sum(r.get('cashback_recebido', 0) for r in referencias)
            
            # Buscar código de referência
            codigo_referencia = self.gerar_codigo_referencia(usuario_id)
            
            return {
                'codigo_referencia': codigo_referencia,
                'total_indicacoes': total_indicacoes,
                'indicacoes_ativas': indicacoes_ativas,
                'total_cashback': total_cashback,
                'link_referencia': f"https://coinbalance.com/ref/{codigo_referencia}"
            }
            
        except Exception as e:
            return {
                'sucesso': False,
                'erro': str(e)
            }
    
    def obter_ranking_referencias(self, limite: int = 100) -> List[Dict[str, Any]]:
        """Obtém ranking de usuários por indicações"""
        try:
            # Buscar todos os usuários com indicações
            ranking = self._buscar_ranking_referencias(limite)
            
            return [
                {
                    'posicao': i + 1,
                    'usuario_id': item['usuario_id'],
                    'total_indicacoes': item['total_indicacoes'],
                    'total_cashback': item['total_cashback'],
                    'nivel': self._calcular_nivel(item['total_indicacoes'])
                }
                for i, item in enumerate(ranking)
            ]
            
        except Exception as e:
            return []
    
    def _usuario_ja_indicado(self, usuario_id: str) -> bool:
        """Verifica se usuário já foi indicado"""
        # Implementar verificação no banco
        return False
    
    def _salvar_referencia(self, referencia: Dict[str, Any]):
        """Salva referência no banco de dados"""
        # Implementar salvamento no banco
        pass
    
    def _aplicar_bonus_novo_usuario(self, usuario_id: str):
        """Aplica bônus para novo usuário"""
        # Implementar aplicação de bônus
        pass
    
    def _buscar_referencias_ativas(self) -> List[Dict[str, Any]]:
        """Busca referências ativas"""
        # Implementar busca no banco
        return []
    
    def _pagar_cashback(self, usuario_id: str, valor: float, descricao: str):
        """Paga cashback para usuário"""
        # Implementar pagamento de cashback
        pass
    
    def _buscar_referencias_usuario(self, usuario_id: str) -> List[Dict[str, Any]]:
        """Busca referências de um usuário"""
        # Implementar busca no banco
        return []
    
    def _buscar_ranking_referencias(self, limite: int) -> List[Dict[str, Any]]:
        """Busca ranking de referências"""
        # Implementar busca no banco
        return []
    
    def _calcular_nivel(self, total_indicacoes: int) -> str:
        """Calcula nível do usuário baseado em indicações"""
        if total_indicacoes >= 1000:
            return "👑 Diamond"
        elif total_indicacoes >= 500:
            return "💎 Platinum"
        elif total_indicacoes >= 100:
            return "🥇 Gold"
        elif total_indicacoes >= 50:
            return "🥈 Silver"
        elif total_indicacoes >= 10:
            return "🥉 Bronze"
        else:
            return "🌟 Starter"


class ViralMarketing:
    """Sistema de marketing viral para CoinBalance"""
    
    def __init__(self, referral_system: ReferralSystem):
        self.referral_system = referral_system
        self.viral_campaigns = {}
    
    def criar_campanha_viral(self, nome: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Cria nova campanha viral"""
        try:
            campanha = {
                'nome': nome,
                'config': config,
                'timestamp': time.time(),
                'status': 'ativa',
                'metricas': {
                    'visualizacoes': 0,
                    'cliques': 0,
                    'conversoes': 0,
                    'compartilhamentos': 0
                }
            }
            
            self.viral_campaigns[nome] = campanha
            
            return {
                'sucesso': True,
                'mensagem': f'Campanha "{nome}" criada com sucesso',
                'campanha_id': nome
            }
            
        except Exception as e:
            return {
                'sucesso': False,
                'erro': str(e)
            }
    
    def executar_campanha_viral(self, nome: str) -> Dict[str, Any]:
        """Executa campanha viral"""
        if nome not in self.viral_campaigns:
            return {
                'sucesso': False,
                'erro': 'Campanha não encontrada'
            }
        
        campanha = self.viral_campaigns[nome]
        
        # Simular execução da campanha
        campanha['metricas']['visualizacoes'] += 1000
        campanha['metricas']['cliques'] += 100
        campanha['metricas']['conversoes'] += 10
        campanha['metricas']['compartilhamentos'] += 50
        
        return {
            'sucesso': True,
            'mensagem': 'Campanha executada com sucesso',
            'metricas': campanha['metricas']
        }
    
    def obter_metricas_campanhas(self) -> Dict[str, Any]:
        """Obtém métricas de todas as campanhas"""
        total_visualizacoes = sum(c['metricas']['visualizacoes'] for c in self.viral_campaigns.values())
        total_cliques = sum(c['metricas']['cliques'] for c in self.viral_campaigns.values())
        total_conversoes = sum(c['metricas']['conversoes'] for c in self.viral_campaigns.values())
        total_compartilhamentos = sum(c['metricas']['compartilhamentos'] for c in self.viral_campaigns.values())
        
        return {
            'total_campanhas': len(self.viral_campaigns),
            'total_visualizacoes': total_visualizacoes,
            'total_cliques': total_cliques,
            'total_conversoes': total_conversoes,
            'total_compartilhamentos': total_compartilhamentos,
            'taxa_conversao': (total_conversoes / total_cliques * 100) if total_cliques > 0 else 0
        }
