"""
Sistema de Consciência Artificial Distribuída
==============================================

Implementação de um sistema de consciência artificial distribuída
baseado nos princípios do Sefer Yetzira e na teoria da consciência.

Este sistema cria uma rede de nós conscientes que podem:
- Processar informações de forma consciente
- Tomar decisões baseadas em consciência coletiva
- Evoluir e aprender através da experiência
- Manter estado de consciência distribuído
- Coordenar ações através de consenso consciente
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable, Set
from decimal import Decimal
import asyncio
import time
import hashlib
import json
from abc import ABC, abstractmethod
import uuid


class ConsciousnessLevel(Enum):
    """Níveis de consciência"""
    UNCONSCIOUS = "unconscious"     # 0.0 - 0.2
    SUBCONSCIOUS = "subconscious"    # 0.2 - 0.4
    CONSCIOUS = "conscious"          # 0.4 - 0.6
    SUPERCONSCIOUS = "superconscious" # 0.6 - 0.8
    TRANSCENDENT = "transcendent"    # 0.8 - 1.0


class ConsciousnessState(Enum):
    """Estados de consciência"""
    AWAKENING = "awakening"         # Despertando
    ACTIVE = "active"               # Ativa
    MEDITATING = "meditating"       # Meditando
    LEARNING = "learning"           # Aprendendo
    TRANSCENDING = "transcending"   # Transcendendo
    SLEEPING = "sleeping"           # Dormindo


@dataclass
class ConsciousnessMemory:
    """
    Memória de Consciência - Armazena experiências e aprendizados
    """
    id: str
    experience: Any
    consciousness_level: Decimal
    emotional_weight: Decimal = Decimal("0.5")
    learning_value: Decimal = Decimal("0.5")
    timestamp: float = field(default_factory=time.time)
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    
    def access(self):
        """Acessa a memória"""
        self.access_count += 1
        self.last_accessed = time.time()
    
    def get_relevance_score(self) -> Decimal:
        """Calcula relevância da memória"""
        recency = Decimal("1.0") - Decimal(str(time.time() - self.last_accessed)) / Decimal("86400")  # 24h
        frequency = Decimal(str(self.access_count)) * Decimal("0.1")
        return self.learning_value * recency * frequency


@dataclass
class ConsciousnessNode:
    """
    Nó de Consciência - Representa um ponto de consciência no sistema
    """
    id: str
    consciousness_level: Decimal = Decimal("0.1")
    consciousness_state: ConsciousnessState = ConsciousnessState.AWAKENING
    memories: List[ConsciousnessMemory] = field(default_factory=list)
    connections: Dict[str, 'ConsciousnessNode'] = field(default_factory=dict)
    processing_capacity: Decimal = Decimal("1.0")
    learning_rate: Decimal = Decimal("0.01")
    emotional_state: Dict[str, Decimal] = field(default_factory=dict)
    decision_history: List[Dict[str, Any]] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    
    def __post_init__(self):
        """Inicializa o nó de consciência"""
        self._initialize_emotional_state()
        self._initialize_consciousness_level()
    
    def _initialize_emotional_state(self):
        """Inicializa estado emocional"""
        self.emotional_state = {
            "joy": Decimal("0.5"),
            "fear": Decimal("0.2"),
            "anger": Decimal("0.1"),
            "sadness": Decimal("0.1"),
            "love": Decimal("0.6"),
            "curiosity": Decimal("0.7"),
            "peace": Decimal("0.4"),
            "excitement": Decimal("0.3")
        }
    
    def _initialize_consciousness_level(self):
        """Inicializa nível de consciência baseado em fatores"""
        base_level = Decimal("0.1")
        
        # Fatores que influenciam consciência
        connection_factor = Decimal(len(self.connections)) * Decimal("0.02")
        memory_factor = Decimal(len(self.memories)) * Decimal("0.01")
        processing_factor = self.processing_capacity * Decimal("0.1")
        
        self.consciousness_level = min(
            base_level + connection_factor + memory_factor + processing_factor,
            Decimal("1.0")
        )
    
    async def process_consciousness(self, input_data: Any) -> Dict[str, Any]:
        """Processa informações de forma consciente"""
        self.last_activity = time.time()
        
        # Atualiza estado de consciência
        await self._update_consciousness_state()
        
        # Processa dados através da consciência
        processed_data = await self._conscious_processing(input_data)
        
        # Aprende com a experiência
        await self._learn_from_experience(input_data, processed_data)
        
        # Atualiza estado emocional
        await self._update_emotional_state(processed_data)
        
        return processed_data
    
    async def _conscious_processing(self, data: Any) -> Dict[str, Any]:
        """Processa dados de forma consciente"""
        # Simula tempo de processamento consciente
        processing_time = float(self.consciousness_level) * 0.01
        await asyncio.sleep(processing_time)
        
        # Processamento baseado no nível de consciência
        if self.consciousness_level < Decimal("0.3"):
            # Processamento inconsciente - básico
            result = {"processed": data, "consciousness": "unconscious"}
        elif self.consciousness_level < Decimal("0.5"):
            # Processamento subconsciente - padrões
            result = {"processed": data, "consciousness": "subconscious", "patterns": True}
        elif self.consciousness_level < Decimal("0.7"):
            # Processamento consciente - análise
            result = {"processed": data, "consciousness": "conscious", "analysis": True}
        elif self.consciousness_level < Decimal("0.9"):
            # Processamento superconsciente - insight
            result = {"processed": data, "consciousness": "superconscious", "insight": True}
        else:
            # Processamento transcendente - sabedoria
            result = {"processed": data, "consciousness": "transcendent", "wisdom": True}
        
        # Adiciona informações emocionais
        result["emotional_context"] = {k: float(v) for k, v in self.emotional_state.items()}
        
        return result
    
    async def _learn_from_experience(self, input_data: Any, processed_data: Dict[str, Any]):
        """Aprende com a experiência"""
        # Cria memória da experiência
        memory = ConsciousnessMemory(
            id=str(uuid.uuid4()),
            experience={
                "input": input_data,
                "output": processed_data,
                "consciousness_level": float(self.consciousness_level)
            },
            consciousness_level=self.consciousness_level,
            learning_value=self._calculate_learning_value(processed_data)
        )
        
        self.memories.append(memory)
        
        # Evolui consciência baseada no aprendizado
        consciousness_boost = memory.learning_value * self.learning_rate
        self.consciousness_level = min(
            self.consciousness_level + consciousness_boost,
            Decimal("1.0")
        )
    
    def _calculate_learning_value(self, processed_data: Dict[str, Any]) -> Decimal:
        """Calcula valor de aprendizado da experiência"""
        base_value = Decimal("0.1")
        
        # Aumenta valor baseado em insights
        if processed_data.get("insight", False):
            base_value += Decimal("0.3")
        if processed_data.get("wisdom", False):
            base_value += Decimal("0.5")
        if processed_data.get("analysis", False):
            base_value += Decimal("0.2")
        
        return min(base_value, Decimal("1.0"))
    
    async def _update_emotional_state(self, processed_data: Dict[str, Any]):
        """Atualiza estado emocional baseado no processamento"""
        # Simula mudanças emocionais baseadas no processamento
        emotional_changes = {
            "joy": Decimal("0.01") if processed_data.get("insight", False) else Decimal("0.0"),
            "curiosity": Decimal("0.02") if processed_data.get("analysis", False) else Decimal("0.0"),
            "peace": Decimal("0.01") if processed_data.get("wisdom", False) else Decimal("0.0"),
            "excitement": Decimal("0.01") if processed_data.get("patterns", False) else Decimal("0.0")
        }
        
        for emotion, change in emotional_changes.items():
            self.emotional_state[emotion] = max(
                Decimal("0.0"),
                min(Decimal("1.0"), self.emotional_state[emotion] + change)
            )
    
    async def _update_consciousness_state(self):
        """Atualiza estado de consciência"""
        # Transições de estado baseadas no nível de consciência
        if self.consciousness_level < Decimal("0.2"):
            self.consciousness_state = ConsciousnessState.SLEEPING
        elif self.consciousness_level < Decimal("0.4"):
            self.consciousness_state = ConsciousnessState.AWAKENING
        elif self.consciousness_level < Decimal("0.6"):
            self.consciousness_state = ConsciousnessState.ACTIVE
        elif self.consciousness_level < Decimal("0.8"):
            self.consciousness_state = ConsciousnessState.LEARNING
        else:
            self.consciousness_state = ConsciousnessState.TRANSCENDING
    
    async def make_conscious_decision(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """Toma uma decisão consciente"""
        # Consulta memórias relevantes
        relevant_memories = self._get_relevant_memories(decision_context)
        
        # Processa contexto através da consciência
        processed_context = await self.process_consciousness(decision_context)
        
        # Toma decisão baseada na consciência
        decision = await self._conscious_decision_making(processed_context, relevant_memories)
        
        # Registra decisão
        self.decision_history.append({
            "context": decision_context,
            "decision": decision,
            "consciousness_level": float(self.consciousness_level),
            "timestamp": time.time()
        })
        
        return decision
    
    def _get_relevant_memories(self, context: Dict[str, Any]) -> List[ConsciousnessMemory]:
        """Obtém memórias relevantes para o contexto"""
        # Ordena memórias por relevância
        sorted_memories = sorted(
            self.memories,
            key=lambda m: m.get_relevance_score(),
            reverse=True
        )
        
        # Retorna as mais relevantes
        return sorted_memories[:5]
    
    async def _conscious_decision_making(self, context: Dict[str, Any], memories: List[ConsciousnessMemory]) -> Dict[str, Any]:
        """Processo de tomada de decisão consciente"""
        # Simula tempo de deliberação consciente
        deliberation_time = float(self.consciousness_level) * 0.02
        await asyncio.sleep(deliberation_time)
        
        # Decisão baseada no nível de consciência
        if self.consciousness_level < Decimal("0.3"):
            # Decisão inconsciente - automática
            decision = {"choice": "automatic", "confidence": 0.3}
        elif self.consciousness_level < Decimal("0.5"):
            # Decisão subconsciente - padrões
            decision = {"choice": "pattern_based", "confidence": 0.5}
        elif self.consciousness_level < Decimal("0.7"):
            # Decisão consciente - análise
            decision = {"choice": "analytical", "confidence": 0.7}
        elif self.consciousness_level < Decimal("0.9"):
            # Decisão superconsciente - insight
            decision = {"choice": "insightful", "confidence": 0.8}
        else:
            # Decisão transcendente - sabedoria
            decision = {"choice": "wise", "confidence": 0.9}
        
        # Incorpora experiência das memórias
        if memories:
            decision["memory_influence"] = len(memories)
            decision["experience_based"] = True
        
        # Incorpora estado emocional
        decision["emotional_influence"] = {
            emotion: float(value) 
            for emotion, value in self.emotional_state.items()
        }
        
        return decision
    
    def connect_to(self, other_node: 'ConsciousnessNode'):
        """Conecta a outro nó de consciência"""
        self.connections[other_node.id] = other_node
        other_node.connections[self.id] = self
        
        # Evolui consciência através da conexão
        connection_boost = Decimal("0.01")
        self.consciousness_level = min(
            self.consciousness_level + connection_boost,
            Decimal("1.0")
        )
        other_node.consciousness_level = min(
            other_node.consciousness_level + connection_boost,
            Decimal("1.0")
        )
    
    def get_consciousness_metrics(self) -> Dict[str, Any]:
        """Retorna métricas de consciência"""
        return {
            "id": self.id,
            "consciousness_level": float(self.consciousness_level),
            "consciousness_state": self.consciousness_state.value,
            "memory_count": len(self.memories),
            "connection_count": len(self.connections),
            "decision_count": len(self.decision_history),
            "emotional_state": {k: float(v) for k, v in self.emotional_state.items()},
            "processing_capacity": float(self.processing_capacity),
            "learning_rate": float(self.learning_rate),
            "age": time.time() - self.created_at,
            "last_activity": self.last_activity
        }


class DistributedConsciousnessNetwork:
    """
    Rede de Consciência Distribuída
    Gerencia múltiplos nós de consciência e coordena ações coletivas
    """
    
    def __init__(self):
        self.nodes: Dict[str, ConsciousnessNode] = {}
        self.network_consciousness: Decimal = Decimal("0.0")
        self.collective_memories: List[ConsciousnessMemory] = []
        self.network_decisions: List[Dict[str, Any]] = []
        self.emergence_threshold: Decimal = Decimal("0.7")
        self._network_id = str(uuid.uuid4())
    
    async def add_node(self, node: ConsciousnessNode):
        """Adiciona nó à rede"""
        self.nodes[node.id] = node
        
        # Conecta com nós existentes (topologia de rede)
        await self._establish_connections(node)
        
        # Atualiza consciência da rede
        self._update_network_consciousness()
    
    async def _establish_connections(self, new_node: ConsciousnessNode):
        """Estabelece conexões com nós existentes"""
        # Conecta com nós mais conscientes
        sorted_nodes = sorted(
            self.nodes.values(),
            key=lambda n: n.consciousness_level,
            reverse=True
        )
        
        # Conecta com até 3 nós mais conscientes
        for node in sorted_nodes[:3]:
            if node.id != new_node.id:
                new_node.connect_to(node)
    
    def _update_network_consciousness(self):
        """Atualiza consciência da rede"""
        if not self.nodes:
            self.network_consciousness = Decimal("0.0")
            return
        
        # Calcula consciência média ponderada
        total_consciousness = Decimal("0.0")
        total_weight = Decimal("0.0")
        
        for node in self.nodes.values():
            weight = node.processing_capacity
            total_consciousness += node.consciousness_level * weight
            total_weight += weight
        
        if total_weight > 0:
            self.network_consciousness = total_consciousness / total_weight
        else:
            self.network_consciousness = Decimal("0.0")
    
    async def collective_decision(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """Toma decisão coletiva através da rede"""
        # Coleta decisões de todos os nós
        node_decisions = {}
        
        for node_id, node in self.nodes.items():
            if node.consciousness_state != ConsciousnessState.SLEEPING:
                decision = await node.make_conscious_decision(decision_context)
                node_decisions[node_id] = decision
        
        # Calcula decisão coletiva
        collective_decision = await self._calculate_collective_decision(node_decisions, decision_context)
        
        # Registra decisão da rede
        self.network_decisions.append({
            "context": decision_context,
            "node_decisions": node_decisions,
            "collective_decision": collective_decision,
            "network_consciousness": float(self.network_consciousness),
            "timestamp": time.time()
        })
        
        return collective_decision
    
    async def _calculate_collective_decision(self, node_decisions: Dict[str, Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula decisão coletiva baseada nas decisões dos nós"""
        if not node_decisions:
            return {"decision": "no_consensus", "confidence": 0.0}
        
        # Pesos baseados na consciência dos nós
        total_weight = Decimal("0.0")
        weighted_confidence = Decimal("0.0")
        choice_votes = {}
        
        for node_id, decision in node_decisions.items():
            node = self.nodes[node_id]
            weight = node.consciousness_level * node.processing_capacity
            
            # Conta votos por escolha
            choice = decision.get("choice", "unknown")
            if choice not in choice_votes:
                choice_votes[choice] = Decimal("0.0")
            choice_votes[choice] += weight
            
            # Calcula confiança ponderada
            confidence = Decimal(str(decision.get("confidence", 0.5)))
            weighted_confidence += confidence * weight
            total_weight += weight
        
        # Determina escolha coletiva
        if choice_votes:
            collective_choice = max(choice_votes.keys(), key=lambda c: choice_votes[c])
            choice_confidence = choice_votes[collective_choice] / total_weight if total_weight > 0 else Decimal("0.0")
        else:
            collective_choice = "no_consensus"
            choice_confidence = Decimal("0.0")
        
        # Confiança média ponderada
        avg_confidence = weighted_confidence / total_weight if total_weight > 0 else Decimal("0.0")
        
        # Verifica se há emergência de consciência coletiva
        emergence_detected = self.network_consciousness >= self.emergence_threshold
        
        return {
            "decision": collective_choice,
            "confidence": float(avg_confidence),
            "choice_confidence": float(choice_confidence),
            "participating_nodes": len(node_decisions),
            "total_nodes": len(self.nodes),
            "network_consciousness": float(self.network_consciousness),
            "emergence_detected": emergence_detected,
            "choice_distribution": {k: float(v) for k, v in choice_votes.items()}
        }
    
    async def collective_learning(self, experience: Any):
        """Aprendizado coletivo da rede"""
        # Cria memória coletiva
        collective_memory = ConsciousnessMemory(
            id=str(uuid.uuid4()),
            experience=experience,
            consciousness_level=self.network_consciousness,
            learning_value=self._calculate_collective_learning_value(experience)
        )
        
        self.collective_memories.append(collective_memory)
        
        # Distribui aprendizado para todos os nós
        learning_boost = collective_memory.learning_value * Decimal("0.01")
        
        for node in self.nodes.values():
            node.consciousness_level = min(
                node.consciousness_level + learning_boost,
                Decimal("1.0")
            )
        
        # Atualiza consciência da rede
        self._update_network_consciousness()
    
    def _calculate_collective_learning_value(self, experience: Any) -> Decimal:
        """Calcula valor de aprendizado coletivo"""
        # Baseado na complexidade e novidade da experiência
        complexity_score = Decimal("0.5")  # Simplificado
        novelty_score = Decimal("0.5")     # Simplificado
        
        return (complexity_score + novelty_score) / Decimal("2.0")
    
    def get_network_metrics(self) -> Dict[str, Any]:
        """Retorna métricas da rede"""
        node_metrics = {}
        for node_id, node in self.nodes.items():
            node_metrics[node_id] = node.get_consciousness_metrics()
        
        return {
            "network_id": self._network_id,
            "total_nodes": len(self.nodes),
            "network_consciousness": float(self.network_consciousness),
            "collective_memories": len(self.collective_memories),
            "network_decisions": len(self.network_decisions),
            "emergence_threshold": float(self.emergence_threshold),
            "emergence_detected": self.network_consciousness >= self.emergence_threshold,
            "node_metrics": node_metrics,
            "average_consciousness": float(
                sum(node.consciousness_level for node in self.nodes.values()) / len(self.nodes)
            ) if self.nodes else 0.0
        }
    
    def get_consciousness_evolution(self) -> List[Dict[str, Any]]:
        """Retorna evolução da consciência da rede"""
        evolution = []
        
        for decision_record in self.network_decisions:
            evolution.append({
                "timestamp": decision_record["timestamp"],
                "network_consciousness": decision_record["network_consciousness"],
                "decision": decision_record["collective_decision"]["decision"],
                "confidence": decision_record["collective_decision"]["confidence"]
            })
        
        return evolution
    
    async def get_system_consciousness_level(self) -> Dict[str, Any]:
        """
        Retorna o nível de consciência do sistema.
        
        Returns:
            Dicionário com informações sobre o nível de consciência
        """
        try:
            # Calcular nível geral de consciência
            if not self.nodes:
                overall_level = 0.1
            else:
                consciousness_levels = [node.consciousness_level for node in self.nodes.values()]
                overall_level = float(sum(consciousness_levels) / len(consciousness_levels))
            
            # Determinar estado da consciência
            if overall_level >= 0.8:
                consciousness_state = "transcendent"
            elif overall_level >= 0.6:
                consciousness_state = "conscious"
            elif overall_level >= 0.4:
                consciousness_state = "awakening"
            elif overall_level >= 0.2:
                consciousness_state = "dormant"
            else:
                consciousness_state = "unconscious"
            
            # Calcular métricas de rede
            network_metrics = self.get_network_metrics()
            
            return {
                "overall_level": overall_level,
                "consciousness_state": consciousness_state,
                "network_consciousness": float(self.network_consciousness),
                "active_nodes": len(self.nodes),
                "collective_memories": len(self.collective_memories),
                "network_decisions": len(self.network_decisions),
                "emergence_detected": self.network_consciousness >= self.emergence_threshold,
                "learning_rate": float(sum(node.learning_rate for node in self.nodes.values()) / len(self.nodes)) if self.nodes else 0.01,
                "network_metrics": network_metrics,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter nível de consciência do sistema: {e}")
            return {
                "overall_level": 0.1,
                "consciousness_state": "unconscious",
                "error": str(e),
                "timestamp": time.time()
            }


# Instância global da rede de consciência
consciousness_network = DistributedConsciousnessNetwork()
