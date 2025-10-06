"""
Sistema de Tokenomics Avançado
Implementa supply limitado, queima de tokens, governance e mecanismos econômicos
"""

import json
import time
from typing import Dict, List, Any, Optional
from database_manager import DatabaseManager


class Tokenomics:
    """Sistema de tokenomics para blockchain"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.supply_maximo = 21_000_000  # 21 milhões de tokens (como Bitcoin)
        self.supply_atual = 0
        self.supply_queimado = 0
        self.taxa_inflacao_inicial = 0.05  # 5% ao ano
        self.halving_intervalo = 4 * 365 * 24 * 3600  # 4 anos em segundos
        self.recompensa_bloco_inicial = 50.0
        self.recompensa_atual = self.recompensa_bloco_inicial
        self.ultimo_halving = time.time()
        
        # Governance
        self.propostas_governance = {}
        self.votos_governance = {}
        self.participantes_governance = set()
        
        # Mecanismos econômicos
        self.taxa_transacao_base = 0.001
        self.taxa_queima = 0.1  # 10% das taxas são queimadas
        self.fundo_governance = 0.0
        
    def obter_supply_info(self) -> Dict[str, Any]:
        """Obtém informações sobre o supply de tokens"""
        return {
            "supply_maximo": self.supply_maximo,
            "supply_atual": self.supply_atual,
            "supply_queimado": self.supply_queimado,
            "supply_circulante": self.supply_atual - self.supply_queimado,
            "percentual_queimado": (self.supply_queimado / self.supply_atual * 100) if self.supply_atual > 0 else 0,
            "recompensa_bloco_atual": self.recompensa_atual,
            "proximo_halving": self.ultimo_halving + self.halving_intervalo
        }
    
    def calcular_recompensa_bloco(self) -> float:
        """Calcula recompensa atual por bloco baseada no halving"""
        tempo_atual = time.time()
        halvings_ocorridos = int((tempo_atual - self.ultimo_halving) // self.halving_intervalo)
        
        if halvings_ocorridos > 0:
            self.recompensa_atual = self.recompensa_bloco_inicial / (2 ** halvings_ocorridos)
            self.ultimo_halving = tempo_atual
        
        # Recompensa mínima de 0.1 tokens
        return max(self.recompensa_atual, 0.1)
    
    def queimar_tokens(self, quantidade: float, motivo: str = "Queima automática") -> Dict[str, Any]:
        """Queima tokens do supply circulante"""
        if quantidade <= 0:
            return {"sucesso": False, "erro": "Quantidade inválida"}
        
        if quantidade > self.supply_atual:
            return {"sucesso": False, "erro": "Quantidade excede supply atual"}
        
        # Queimar tokens
        self.supply_atual -= quantidade
        self.supply_queimado += quantidade
        
        # Registrar queima
        self._registrar_queima(quantidade, motivo)
        
        return {
            "sucesso": True,
            "mensagem": f"{quantidade} tokens queimados",
            "supply_atual": self.supply_atual,
            "supply_queimado": self.supply_queimado
        }
    
    def _registrar_queima(self, quantidade: float, motivo: str):
        """Registra evento de queima de tokens"""
        evento = {
            "timestamp": time.time(),
            "quantidade": quantidade,
            "motivo": motivo,
            "supply_apos_queima": self.supply_atual
        }
        
        # Salvar no banco de dados
        # Implementar salvamento no banco
    
    def emitir_tokens(self, quantidade: float, destinatario: str, motivo: str = "Emissão") -> Dict[str, Any]:
        """Emite novos tokens (apenas se dentro do limite)"""
        if quantidade <= 0:
            return {"sucesso": False, "erro": "Quantidade inválida"}
        
        if self.supply_atual + quantidade > self.supply_maximo:
            return {"sucesso": False, "erro": "Emissão excederia supply máximo"}
        
        # Emitir tokens
        self.supply_atual += quantidade
        
        # Atualizar saldo do destinatário
        saldo_atual = self.db_manager.obter_saldo_carteira(destinatario)
        novo_saldo = saldo_atual + quantidade
        self.db_manager.atualizar_saldo_carteira(destinatario, novo_saldo)
        
        return {
            "sucesso": True,
            "mensagem": f"{quantidade} tokens emitidos para {destinatario}",
            "supply_atual": self.supply_atual,
            "novo_saldo": novo_saldo
        }
    
    def calcular_taxa_transacao(self, valor_transacao: float, prioridade: str = "normal") -> float:
        """Calcula taxa de transação baseada no valor e prioridade"""
        taxa_base = self.taxa_transacao_base
        
        # Ajustar por prioridade
        multiplicadores = {
            "baixa": 0.5,
            "normal": 1.0,
            "alta": 2.0,
            "urgente": 5.0
        }
        
        multiplicador = multiplicadores.get(prioridade, 1.0)
        taxa_calculada = taxa_base * multiplicador
        
        # Taxa mínima
        return max(taxa_calculada, 0.0001)
    
    def processar_taxa_transacao(self, taxa: float) -> Dict[str, Any]:
        """Processa taxa de transação (queima + fundo governance)"""
        # Calcular queima
        quantidade_queimar = taxa * self.taxa_queima
        quantidade_governance = taxa - quantidade_queimar
        
        # Queimar tokens
        if quantidade_queimar > 0:
            self.queimar_tokens(quantidade_queimar, "Taxa de transação")
        
        # Adicionar ao fundo de governance
        self.fundo_governance += quantidade_governance
        
        return {
            "taxa_total": taxa,
            "queimado": quantidade_queimar,
            "governance": quantidade_governance,
            "fundo_governance": self.fundo_governance
        }


class Governance:
    """Sistema de governance descentralizado"""
    
    def __init__(self, tokenomics: Tokenomics):
        self.tokenomics = tokenomics
        self.propostas = {}
        self.votos = {}
        self.quorum_minimo = 0.1  # 10% do supply
        self.maioria_necessaria = 0.51  # 51%
    
    def criar_proposta(self, titulo: str, descricao: str, tipo: str, 
                      parametros: Dict, criador: str) -> Dict[str, Any]:
        """Cria nova proposta de governance"""
        proposta_id = f"PROP_{int(time.time())}"
        
        proposta = {
            "id": proposta_id,
            "titulo": titulo,
            "descricao": descricao,
            "tipo": tipo,  # "mudanca_taxa", "novo_contrato", "queima_tokens", etc.
            "parametros": parametros,
            "criador": criador,
            "timestamp": time.time(),
            "status": "ativa",
            "votos_favor": 0,
            "votos_contra": 0,
            "total_votos": 0,
            "participantes": set()
        }
        
        self.propostas[proposta_id] = proposta
        return {"sucesso": True, "proposta_id": proposta_id}
    
    def votar_proposta(self, proposta_id: str, voto: bool, votante: str, 
                      peso_voto: float) -> Dict[str, Any]:
        """Vota em uma proposta de governance"""
        if proposta_id not in self.propostas:
            return {"sucesso": False, "erro": "Proposta não encontrada"}
        
        proposta = self.propostas[proposta_id]
        
        if proposta["status"] != "ativa":
            return {"sucesso": False, "erro": "Proposta não está ativa"}
        
        # Verificar se já votou
        if votante in proposta["participantes"]:
            return {"sucesso": False, "erro": "Já votou nesta proposta"}
        
        # Registrar voto
        if voto:
            proposta["votos_favor"] += peso_voto
        else:
            proposta["votos_contra"] += peso_voto
        
        proposta["total_votos"] += peso_voto
        proposta["participantes"].add(votante)
        
        # Verificar se atingiu quorum
        if self._verificar_quorum(proposta):
            resultado = self._processar_proposta(proposta)
            return {"sucesso": True, "voto_registrado": True, "resultado": resultado}
        
        return {"sucesso": True, "voto_registrado": True}
    
    def _verificar_quorum(self, proposta: Dict) -> bool:
        """Verifica se proposta atingiu quorum necessário"""
        total_supply = self.tokenomics.supply_atual
        quorum_necessario = total_supply * self.quorum_minimo
        
        return proposta["total_votos"] >= quorum_necessario
    
    def _processar_proposta(self, proposta: Dict) -> Dict[str, Any]:
        """Processa proposta que atingiu quorum"""
        total_votos = proposta["votos_favor"] + proposta["votos_contra"]
        percentual_favor = proposta["votos_favor"] / total_votos if total_votos > 0 else 0
        
        if percentual_favor >= self.maioria_necessaria:
            # Proposta aprovada
            resultado = self._executar_proposta(proposta)
            proposta["status"] = "aprovada"
            return {"aprovada": True, "resultado": resultado}
        else:
            # Proposta rejeitada
            proposta["status"] = "rejeitada"
            return {"aprovada": False, "motivo": "Não atingiu maioria necessária"}
    
    def _executar_proposta(self, proposta: Dict) -> Dict[str, Any]:
        """Executa proposta aprovada"""
        tipo = proposta["tipo"]
        parametros = proposta["parametros"]
        
        if tipo == "mudanca_taxa":
            return self._mudar_taxa(parametros)
        elif tipo == "queima_tokens":
            return self._queimar_tokens_governance(parametros)
        elif tipo == "novo_contrato":
            return self._criar_contrato_governance(parametros)
        else:
            return {"sucesso": False, "erro": "Tipo de proposta não suportado"}
    
    def _mudar_taxa(self, parametros: Dict) -> Dict[str, Any]:
        """Muda taxa de transação via governance"""
        nova_taxa = parametros.get("nova_taxa")
        if nova_taxa and nova_taxa > 0:
            self.tokenomics.taxa_transacao_base = nova_taxa
            return {"sucesso": True, "nova_taxa": nova_taxa}
        return {"sucesso": False, "erro": "Parâmetros inválidos"}
    
    def _queimar_tokens_governance(self, parametros: Dict) -> Dict[str, Any]:
        """Queima tokens via governance"""
        quantidade = parametros.get("quantidade")
        motivo = parametros.get("motivo", "Queima via governance")
        
        if quantidade and quantidade > 0:
            return self.tokenomics.queimar_tokens(quantidade, motivo)
        return {"sucesso": False, "erro": "Parâmetros inválidos"}
    
    def _criar_contrato_governance(self, parametros: Dict) -> Dict[str, Any]:
        """Cria novo contrato via governance"""
        # Implementar criação de contrato
        return {"sucesso": True, "mensagem": "Contrato criado via governance"}
    
    def obter_propostas_ativas(self) -> List[Dict]:
        """Obtém todas as propostas ativas"""
        return [
            {k: v for k, v in proposta.items() if k != "participantes"}
            for proposta in self.propostas.values()
            if proposta["status"] == "ativa"
        ]
    
    def obter_estatisticas_governance(self) -> Dict[str, Any]:
        """Obtém estatísticas do sistema de governance"""
        total_propostas = len(self.propostas)
        propostas_ativas = len([p for p in self.propostas.values() if p["status"] == "ativa"])
        propostas_aprovadas = len([p for p in self.propostas.values() if p["status"] == "aprovada"])
        
        return {
            "total_propostas": total_propostas,
            "propostas_ativas": propostas_ativas,
            "propostas_aprovadas": propostas_aprovadas,
            "fundo_governance": self.tokenomics.fundo_governance,
            "quorum_minimo": self.quorum_minimo,
            "maioria_necessaria": self.maioria_necessaria
        }
