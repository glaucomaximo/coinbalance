"""
Framework Coinbalance - A Economia da Consciência
Framework proprietário que integra IA simbólica, neuroeconomia e blockchain
para criar investimentos conscientes baseados em consciência e propósito
"""

import json
import time
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class TipoConsciencia(Enum):
    """Tipos de consciência para análise de investimentos"""
    MATERIAL = "material"
    EMOCIONAL = "emocional"
    MENTAL = "mental"
    ESPIRITUAL = "espiritual"
    TRANSCENDENTAL = "transcendental"


class NivelImpacto(Enum):
    """Níveis de impacto social e ambiental"""
    BAIXO = 1
    MEDIO = 2
    ALTO = 3
    TRANSFORMADOR = 4


@dataclass
class PerfilConsciencia:
    """Perfil de consciência de um investidor"""
    material: float  # 0.0 a 1.0
    emocional: float
    mental: float
    espiritual: float
    transcendental: float
    nivel_impacto_desejado: NivelImpacto
    tolerancia_risco: float  # 0.0 a 1.0
    horizonte_temporal: int  # meses


@dataclass
class ProjetoConsciente:
    """Projeto de investimento consciente"""
    nome: str
    descricao: str
    tipo_impacto: List[str]
    nivel_impacto: NivelImpacto
    retorno_esperado: float
    risco: float
    horizonte: int
    valores_consciencia: Dict[TipoConsciencia, float]
    metricas_impacto: Dict[str, float]
    certificacoes: List[str]


class IASimbolica:
    """Inteligência Artificial Simbólica baseada em lógica mônadica"""
    
    def __init__(self):
        self.regras_consciencia = self._carregar_regras_consciencia()
        self.padroes_investimento = self._carregar_padroes_investimento()
    
    def _carregar_regras_consciencia(self) -> Dict[str, Any]:
        """Carrega regras de consciência baseadas em lógica mônadica"""
        return {
            "material": {
                "peso": 0.2,
                "indicadores": ["lucratividade", "sustentabilidade_financeira", "crescimento"],
                "limiar_minimo": 0.3
            },
            "emocional": {
                "peso": 0.2,
                "indicadores": ["satisfacao_cliente", "bem_estar_funcionarios", "relacionamentos"],
                "limiar_minimo": 0.4
            },
            "mental": {
                "peso": 0.2,
                "indicadores": ["inovacao", "aprendizado", "conhecimento"],
                "limiar_minimo": 0.5
            },
            "espiritual": {
                "peso": 0.2,
                "indicadores": ["proposito", "valores", "significado"],
                "limiar_minimo": 0.6
            },
            "transcendental": {
                "peso": 0.2,
                "indicadores": ["transformacao", "evolucao", "consciencia_coletiva"],
                "limiar_minimo": 0.7
            }
        }
    
    def _carregar_padroes_investimento(self) -> Dict[str, Any]:
        """Carrega padrões de investimento consciente"""
        return {
            "padroes_otimos": {
                "consciencia_equilibrada": [0.8, 0.8, 0.8, 0.8, 0.8],
                "impacto_alto": NivelImpacto.ALTO,
                "risco_moderado": 0.5,
                "retorno_sustentavel": 0.12
            },
            "padroes_evitados": {
                "apenas_material": [1.0, 0.0, 0.0, 0.0, 0.0],
                "impacto_baixo": NivelImpacto.BAIXO,
                "risco_extremo": 0.9,
                "retorno_insustentavel": 0.5
            }
        }
    
    def analisar_projeto(self, projeto: ProjetoConsciente, perfil: PerfilConsciencia) -> Dict[str, Any]:
        """Analisa um projeto usando IA simbólica"""
        score_consciencia = self._calcular_score_consciencia(projeto, perfil)
        compatibilidade = self._calcular_compatibilidade(projeto, perfil)
        recomendacao = self._gerar_recomendacao(score_consciencia, compatibilidade)
        
        return {
            "projeto": projeto.nome,
            "score_consciencia": score_consciencia,
            "compatibilidade": compatibilidade,
            "recomendacao": recomendacao,
            "pontos_fortes": self._identificar_pontos_fortes(projeto),
            "pontos_fracos": self._identificar_pontos_fracos(projeto),
            "sugestoes_melhoria": self._gerar_sugestoes_melhoria(projeto, perfil)
        }
    
    def _calcular_score_consciencia(self, projeto: ProjetoConsciente, perfil: PerfilConsciencia) -> float:
        """Calcula score de consciência do projeto"""
        score_total = 0.0
        
        for tipo_consciencia, regra in self.regras_consciencia.items():
            valor_projeto = projeto.valores_consciencia.get(TipoConsciencia(tipo_consciencia), 0.0)
            peso = regra["peso"]
            limiar = regra["limiar_minimo"]
            
            # Aplicar função de ativação baseada em consciência
            if valor_projeto >= limiar:
                score_tipo = valor_projeto * peso
            else:
                score_tipo = valor_projeto * peso * 0.5  # Penalizar abaixo do limiar
            
            score_total += score_tipo
        
        return min(score_total, 1.0)
    
    def _calcular_compatibilidade(self, projeto: ProjetoConsciente, perfil: PerfilConsciencia) -> float:
        """Calcula compatibilidade entre projeto e perfil do investidor"""
        # Comparar níveis de impacto
        compatibilidade_impacto = self._comparar_impacto(projeto.nivel_impacto, perfil.nivel_impacto_desejado)
        
        # Comparar tolerância ao risco
        compatibilidade_risco = self._comparar_risco(projeto.risco, perfil.tolerancia_risco)
        
        # Comparar horizonte temporal
        compatibilidade_horizonte = self._comparar_horizonte(projeto.horizonte, perfil.horizonte_temporal)
        
        # Média ponderada
        return (compatibilidade_impacto * 0.4 + compatibilidade_risco * 0.3 + compatibilidade_horizonte * 0.3)
    
    def _comparar_impacto(self, impacto_projeto: NivelImpacto, impacto_desejado: NivelImpacto) -> float:
        """Compara níveis de impacto"""
        if impacto_projeto.value >= impacto_desejado.value:
            return 1.0
        else:
            return impacto_projeto.value / impacto_desejado.value
    
    def _comparar_risco(self, risco_projeto: float, tolerancia_risco: float) -> float:
        """Compara risco do projeto com tolerância do investidor"""
        if risco_projeto <= tolerancia_risco:
            return 1.0
        else:
            return max(0.0, 1.0 - (risco_projeto - tolerancia_risco))
    
    def _comparar_horizonte(self, horizonte_projeto: int, horizonte_desejado: int) -> float:
        """Compara horizontes temporais"""
        diferenca = abs(horizonte_projeto - horizonte_desejado)
        return max(0.0, 1.0 - (diferenca / max(horizonte_projeto, horizonte_desejado)))
    
    def _gerar_recomendacao(self, score_consciencia: float, compatibilidade: float) -> str:
        """Gera recomendação baseada nos scores"""
        if score_consciencia >= 0.8 and compatibilidade >= 0.8:
            return "ALTAMENTE_RECOMENDADO"
        elif score_consciencia >= 0.6 and compatibilidade >= 0.6:
            return "RECOMENDADO"
        elif score_consciencia >= 0.4 and compatibilidade >= 0.4:
            return "NEUTRO"
        else:
            return "NÃO_RECOMENDADO"
    
    def _identificar_pontos_fortes(self, projeto: ProjetoConsciente) -> List[str]:
        """Identifica pontos fortes do projeto"""
        pontos = []
        
        if projeto.nivel_impacto.value >= 3:
            pontos.append("Alto impacto social/ambiental")
        
        if projeto.retorno_esperado >= 0.12:
            pontos.append("Retorno atrativo")
        
        if projeto.risco <= 0.5:
            pontos.append("Risco controlado")
        
        if len(projeto.certificacoes) >= 3:
            pontos.append("Bem certificado")
        
        return pontos
    
    def _identificar_pontos_fracos(self, projeto: ProjetoConsciente) -> List[str]:
        """Identifica pontos fracos do projeto"""
        pontos = []
        
        if projeto.nivel_impacto.value < 2:
            pontos.append("Baixo impacto social/ambiental")
        
        if projeto.retorno_esperado < 0.08:
            pontos.append("Retorno baixo")
        
        if projeto.risco > 0.7:
            pontos.append("Alto risco")
        
        if len(projeto.certificacoes) < 2:
            pontos.append("Poucas certificações")
        
        return pontos
    
    def _gerar_sugestoes_melhoria(self, projeto: ProjetoConsciente, perfil: PerfilConsciencia) -> List[str]:
        """Gera sugestões de melhoria para o projeto"""
        sugestoes = []
        
        # Analisar valores de consciência
        for tipo, valor in projeto.valores_consciencia.items():
            if valor < 0.6:
                sugestoes.append(f"Melhorar aspectos de {tipo.value} no projeto")
        
        # Analisar métricas de impacto
        if projeto.nivel_impacto.value < perfil.nivel_impacto_desejado.value:
            sugestoes.append("Aumentar impacto social/ambiental do projeto")
        
        # Analisar risco
        if projeto.risco > perfil.tolerancia_risco:
            sugestoes.append("Reduzir risco do projeto")
        
        return sugestoes


class Neuroeconomia:
    """Neuroeconomia aplicada a investimentos conscientes"""
    
    def __init__(self):
        self.vieses_cognitivos = self._carregar_vieses_cognitivos()
        self.emocoes_investimento = self._carregar_emocoes_investimento()
    
    def _carregar_vieses_cognitivos(self) -> Dict[str, Any]:
        """Carrega vieses cognitivos comuns em investimentos"""
        return {
            "viés_confirmação": {
                "descricao": "Tendência a buscar informações que confirmem crenças existentes",
                "peso": 0.3,
                "mitigação": "Buscar evidências contrárias"
            },
            "viés_ancoragem": {
                "descricao": "Dependência excessiva da primeira informação recebida",
                "peso": 0.2,
                "mitigação": "Considerar múltiplas fontes"
            },
            "viés_disponibilidade": {
                "descricao": "Superestimação de eventos facilmente lembrados",
                "peso": 0.25,
                "mitigação": "Análise estatística rigorosa"
            },
            "viés_representatividade": {
                "descricao": "Julgamento baseado em estereótipos",
                "peso": 0.25,
                "mitigação": "Análise individual detalhada"
            }
        }
    
    def _carregar_emocoes_investimento(self) -> Dict[str, Any]:
        """Carrega emoções que afetam decisões de investimento"""
        return {
            "medo": {
                "impacto": -0.3,
                "sintomas": ["evitação_risco", "vendas_panico"],
                "controle": "educacao_risco"
            },
            "ganancia": {
                "impacto": 0.4,
                "sintomas": ["tomada_risco_excessivo", "fomo"],
                "controle": "limites_rigidos"
            },
            "confianca": {
                "impacto": 0.2,
                "sintomas": ["decisoes_rapidas", "menos_analise"],
                "controle": "processo_estruturado"
            },
            "ansiedade": {
                "impacto": -0.2,
                "sintomas": ["paralisia_decisao", "microgerenciamento"],
                "controle": "meditacao_consciencia"
            }
        }
    
    def analisar_decisao(self, perfil: PerfilConsciencia, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa decisão de investimento considerando neuroeconomia"""
        vieses_detectados = self._detectar_vieses(perfil, contexto)
        emocoes_ativas = self._detectar_emocoes(perfil, contexto)
        recomendacoes = self._gerar_recomendacoes_neuroeconomicas(vieses_detectados, emocoes_ativas)
        
        return {
            "vieses_detectados": vieses_detectados,
            "emocoes_ativas": emocoes_ativas,
            "recomendacoes": recomendacoes,
            "score_racionalidade": self._calcular_score_racionalidade(vieses_detectados, emocoes_ativas),
            "nivel_consciencia": self._calcular_nivel_consciencia(perfil)
        }
    
    def _detectar_vieses(self, perfil: PerfilConsciencia, contexto: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detecta vieses cognitivos na decisão"""
        vieses = []
        
        # Verificar viés de confirmação
        if contexto.get("busca_confirmacao", False):
            vieses.append({
                "tipo": "viés_confirmação",
                "intensidade": 0.7,
                "descricao": "Tendência a buscar informações que confirmem crenças"
            })
        
        # Verificar viés de ancoragem
        if contexto.get("ancoragem", False):
            vieses.append({
                "tipo": "viés_ancoragem",
                "intensidade": 0.6,
                "descricao": "Dependência excessiva de primeira informação"
            })
        
        return vieses
    
    def _detectar_emocoes(self, perfil: PerfilConsciencia, contexto: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detecta emoções ativas na decisão"""
        emocoes = []
        
        # Verificar medo
        if contexto.get("nivel_medo", 0) > 0.5:
            emocoes.append({
                "tipo": "medo",
                "intensidade": contexto["nivel_medo"],
                "impacto": -0.3
            })
        
        # Verificar ganância
        if contexto.get("nivel_ganancia", 0) > 0.5:
            emocoes.append({
                "tipo": "ganancia",
                "intensidade": contexto["nivel_ganancia"],
                "impacto": 0.4
            })
        
        return emocoes
    
    def _gerar_recomendacoes_neuroeconomicas(self, vieses: List[Dict], emocoes: List[Dict]) -> List[str]:
        """Gera recomendações baseadas em neuroeconomia"""
        recomendacoes = []
        
        for vies in vieses:
            if vies["tipo"] == "viés_confirmação":
                recomendacoes.append("Busque evidências contrárias à sua posição")
            elif vies["tipo"] == "viés_ancoragem":
                recomendacoes.append("Considere múltiplas fontes de informação")
        
        for emocao in emocoes:
            if emocao["tipo"] == "medo":
                recomendacoes.append("Pratique meditação para reduzir ansiedade")
            elif emocao["tipo"] == "ganancia":
                recomendacoes.append("Estabeleça limites rígidos de investimento")
        
        return recomendacoes
    
    def _calcular_score_racionalidade(self, vieses: List[Dict], emocoes: List[Dict]) -> float:
        """Calcula score de racionalidade da decisão"""
        score = 1.0
        
        # Penalizar vieses
        for vies in vieses:
            score -= vies["intensidade"] * 0.2
        
        # Penalizar emoções negativas
        for emocao in emocoes:
            if emocao["impacto"] < 0:
                score -= emocao["intensidade"] * abs(emocao["impacto"])
        
        return max(0.0, min(1.0, score))
    
    def _calcular_nivel_consciencia(self, perfil: PerfilConsciencia) -> float:
        """Calcula nível de consciência do investidor"""
        valores = [
            perfil.material,
            perfil.emocional,
            perfil.mental,
            perfil.espiritual,
            perfil.transcendental
        ]
        
        # Média ponderada com foco em consciência superior
        pesos = [0.1, 0.2, 0.3, 0.4, 0.5]
        return sum(v * p for v, p in zip(valores, pesos)) / sum(pesos)


class FrameworkCoinbalance:
    """Framework principal Coinbalance - A Economia da Consciência"""
    
    def __init__(self):
        self.ia_simbolica = IASimbolica()
        self.neuroeconomia = Neuroeconomia()
        self.projetos_cadastrados = []
        self.investidores_cadastrados = []
    
    def cadastrar_projeto(self, projeto: ProjetoConsciente) -> Dict[str, Any]:
        """Cadastra um novo projeto consciente"""
        self.projetos_cadastrados.append(projeto)
        
        return {
            "sucesso": True,
            "mensagem": f"Projeto {projeto.nome} cadastrado com sucesso",
            "projeto_id": len(self.projetos_cadastrados) - 1,
            "framework": "Coinbalance"
        }
    
    def cadastrar_investidor(self, perfil: PerfilConsciencia, nome: str) -> Dict[str, Any]:
        """Cadastra um novo investidor"""
        self.investidores_cadastrados.append({
            "nome": nome,
            "perfil": perfil,
            "data_cadastro": time.time()
        })
        
        return {
            "sucesso": True,
            "mensagem": f"Investidor {nome} cadastrado com sucesso",
            "investidor_id": len(self.investidores_cadastrados) - 1,
            "framework": "Coinbalance"
        }
    
    def analisar_investimento(self, projeto_id: int, investidor_id: int) -> Dict[str, Any]:
        """Analisa compatibilidade entre projeto e investidor"""
        if projeto_id >= len(self.projetos_cadastrados):
            return {"erro": "Projeto não encontrado"}
        
        if investidor_id >= len(self.investidores_cadastrados):
            return {"erro": "Investidor não encontrado"}
        
        projeto = self.projetos_cadastrados[projeto_id]
        perfil = self.investidores_cadastrados[investidor_id]["perfil"]
        
        # Análise com IA simbólica
        analise_ia = self.ia_simbolica.analisar_projeto(projeto, perfil)
        
        # Análise neuroeconômica
        contexto = {
            "busca_confirmacao": True,
            "nivel_medo": 0.3,
            "nivel_ganancia": 0.2
        }
        analise_neuro = self.neuroeconomia.analisar_decisao(perfil, contexto)
        
        # Resultado final
        return {
            "projeto": projeto.nome,
            "investidor": self.investidores_cadastrados[investidor_id]["nome"],
            "analise_ia": analise_ia,
            "analise_neuroeconomia": analise_neuro,
            "recomendacao_final": self._gerar_recomendacao_final(analise_ia, analise_neuro),
            "framework": "Coinbalance",
            "timestamp": time.time()
        }
    
    def _gerar_recomendacao_final(self, analise_ia: Dict, analise_neuro: Dict) -> str:
        """Gera recomendação final baseada em ambas as análises"""
        score_ia = analise_ia["score_consciencia"]
        compatibilidade = analise_ia["compatibilidade"]
        racionalidade = analise_neuro["score_racionalidade"]
        
        score_final = (score_ia * 0.4 + compatibilidade * 0.3 + racionalidade * 0.3)
        
        if score_final >= 0.8:
            return "INVESTIR_AGORA"
        elif score_final >= 0.6:
            return "INVESTIR_COM_CUIDADO"
        elif score_final >= 0.4:
            return "AGUARDAR_MELHORIAS"
        else:
            return "NÃO_INVESTIR"
    
    def obter_estatisticas_framework(self) -> Dict[str, Any]:
        """Obtém estatísticas do framework"""
        return {
            "framework": "Coinbalance",
            "versao": "1.0",
            "projetos_cadastrados": len(self.projetos_cadastrados),
            "investidores_cadastrados": len(self.investidores_cadastrados),
            "descricao": "A Economia da Consciência",
            "moeda": "CNB",
            "timestamp": time.time()
        }


# Exemplo de uso do framework
if __name__ == "__main__":
    # Inicializar framework
    framework = FrameworkCoinbalance()
    
    # Criar projeto de exemplo
    projeto = ProjetoConsciente(
        nome="Energia Solar Comunitária",
        descricao="Projeto de energia solar para comunidades carentes",
        tipo_impacto=["ambiental", "social", "econômico"],
        nivel_impacto=NivelImpacto.ALTO,
        retorno_esperado=0.15,
        risco=0.4,
        horizonte=24,
        valores_consciencia={
            TipoConsciencia.MATERIAL: 0.8,
            TipoConsciencia.EMOCIONAL: 0.9,
            TipoConsciencia.MENTAL: 0.7,
            TipoConsciencia.ESPIRITUAL: 0.9,
            TipoConsciencia.TRANSCENDENTAL: 0.8
        },
        metricas_impacto={
            "co2_evitado": 1000.0,
            "familias_beneficiadas": 500,
            "empregos_criados": 50
        },
        certificacoes=["B-Corp", "ISO 14001", "Selo Verde"]
    )
    
    # Criar perfil de investidor
    perfil = PerfilConsciencia(
        material=0.7,
        emocional=0.8,
        mental=0.9,
        espiritual=0.8,
        transcendental=0.7,
        nivel_impacto_desejado=NivelImpacto.ALTO,
        tolerancia_risco=0.5,
        horizonte_temporal=36
    )
    
    # Cadastrar no framework
    resultado_projeto = framework.cadastrar_projeto(projeto)
    resultado_investidor = framework.cadastrar_investidor(perfil, "João Silva")
    
    # Analisar investimento
    analise = framework.analisar_investimento(0, 0)
    
    print("🪙 Framework Coinbalance - A Economia da Consciência")
    print("=" * 50)
    print(f"Projeto: {resultado_projeto['mensagem']}")
    print(f"Investidor: {resultado_investidor['mensagem']}")
    print(f"Recomendação: {analise['recomendacao_final']}")
    print(f"Score Consciência: {analise['analise_ia']['score_consciencia']:.2f}")
    print(f"Compatibilidade: {analise['analise_ia']['compatibilidade']:.2f}")
    print(f"Racionalidade: {analise['analise_neuroeconomia']['score_racionalidade']:.2f}")