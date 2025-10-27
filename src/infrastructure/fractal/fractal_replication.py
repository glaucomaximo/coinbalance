"""
Sistema de Auto-Replicação Fractal
==================================

Implementação de sistema que permite aos fractais se replicarem automaticamente
baseado em condições específicas, criando escalabilidade infinita e auto-organização.

Este sistema implementa:
- Replicação automática baseada em regras
- Distribuição inteligente de carga
- Auto-organização emergente
- Escalabilidade infinita
- Consciência distribuída
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable
from decimal import Decimal
import time
import json
import threading
import asyncio
from collections import defaultdict, deque
import uuid
import random
import math

from .fractal_core import (
    ConsciousFractalCore, FractalInstance, FractalPattern, 
    FractalType, FractalState, FractalDimension, fractal_core
)


class ReplicationTrigger(Enum):
    """Gatilhos de Replicação"""
    LOAD_THRESHOLD = "load_threshold"
    CONSCIOUSNESS_THRESHOLD = "consciousness_threshold"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    ERROR_RATE_INCREASE = "error_rate_increase"
    MEMORY_PRESSURE = "memory_pressure"
    NETWORK_CONGESTION = "network_congestion"
    USER_DEMAND = "user_demand"
    EMERGENCE_DETECTED = "emergence_detected"


class ReplicationStrategy(Enum):
    """Estratégias de Replicação"""
    HORIZONTAL = "horizontal"      # Replicação horizontal (mais instâncias)
    VERTICAL = "vertical"          # Replicação vertical (mais recursos)
    DIAGONAL = "diagonal"          # Replicação diagonal (híbrida)
    FRACTAL = "fractal"            # Replicação fractal (auto-similar)
    EMERGENT = "emergent"          # Replicação emergente (baseada em padrões)


@dataclass
class ReplicationRule:
    """
    Regra de Replicação - Define quando e como replicar
    """
    id: str
    name: str
    trigger: ReplicationTrigger
    condition: Callable[[Dict[str, Any]], bool]
    strategy: ReplicationStrategy
    replication_factor: Decimal
    consciousness_requirement: Decimal
    energy_cost: Decimal
    information_transfer: Decimal
    priority: int
    enabled: bool = True
    
    def __post_init__(self):
        """Inicializa regra de replicação"""
        if not self.id:
            self.id = f"rule_{uuid.uuid4().hex[:8]}"


@dataclass
class ReplicationEvent:
    """
    Evento de Replicação - Registra uma replicação ocorrida
    """
    id: str
    source_fractal_id: str
    target_fractal_id: str
    rule_id: str
    strategy: ReplicationStrategy
    trigger: ReplicationTrigger
    context: Dict[str, Any]
    success: bool
    timestamp: float
    energy_cost: Decimal
    consciousness_gained: Decimal
    performance_impact: Decimal
    
    def __post_init__(self):
        """Inicializa evento de replicação"""
        if not self.id:
            self.id = f"event_{uuid.uuid4().hex[:8]}"


class FractalReplicationSystem:
    """
    Sistema de Replicação Fractal
    Gerencia replicação automática e inteligente de fractais
    """
    
    def __init__(self, fractal_core: ConsciousFractalCore):
        self.fractal_core = fractal_core
        self.replication_rules: Dict[str, ReplicationRule] = {}
        self.replication_events: List[ReplicationEvent] = []
        self.replication_queue: deque = deque()
        self.active_replications: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        
        # Configurações de replicação
        self.max_concurrent_replications = 10
        self.replication_cooldown = 300  # 5 minutos
        self.energy_budget = Decimal("1000.0")
        self.consciousness_budget = Decimal("1000.0")
        
        # Inicializa regras de replicação
        self._initialize_replication_rules()
        
        # Inicia processo de replicação
        self._start_replication_process()
    
    def _initialize_replication_rules(self):
        """Inicializa regras de replicação fundamentais"""
        # Regra: Replicação por carga alta
        load_rule = ReplicationRule(
            id="load_replication",
            name="Replicação por Carga Alta",
            trigger=ReplicationTrigger.LOAD_THRESHOLD,
            condition=self._load_threshold_condition,
            strategy=ReplicationStrategy.HORIZONTAL,
            replication_factor=Decimal("2.0"),
            consciousness_requirement=Decimal("0.6"),
            energy_cost=Decimal("100.0"),
            information_transfer=Decimal("0.8"),
            priority=1
        )
        self.replication_rules["load_replication"] = load_rule
        
        # Regra: Replicação por consciência alta
        consciousness_rule = ReplicationRule(
            id="consciousness_replication",
            name="Replicação por Consciência Alta",
            trigger=ReplicationTrigger.CONSCIOUSNESS_THRESHOLD,
            condition=self._consciousness_threshold_condition,
            strategy=ReplicationStrategy.FRACTAL,
            replication_factor=Decimal("1.618"),  # Proporção áurea
            consciousness_requirement=Decimal("0.8"),
            energy_cost=Decimal("150.0"),
            information_transfer=Decimal("0.9"),
            priority=2
        )
        self.replication_rules["consciousness_replication"] = consciousness_rule
        
        # Regra: Replicação por degradação de performance
        performance_rule = ReplicationRule(
            id="performance_replication",
            name="Replicação por Performance",
            trigger=ReplicationTrigger.PERFORMANCE_DEGRADATION,
            condition=self._performance_degradation_condition,
            strategy=ReplicationStrategy.VERTICAL,
            replication_factor=Decimal("1.5"),
            consciousness_requirement=Decimal("0.5"),
            energy_cost=Decimal("80.0"),
            information_transfer=Decimal("0.7"),
            priority=3
        )
        self.replication_rules["performance_replication"] = performance_rule
        
        # Regra: Replicação por emergência
        emergence_rule = ReplicationRule(
            id="emergence_replication",
            name="Replicação por Emergência",
            trigger=ReplicationTrigger.EMERGENCE_DETECTED,
            condition=self._emergence_detected_condition,
            strategy=ReplicationStrategy.EMERGENT,
            replication_factor=Decimal("3.0"),
            consciousness_requirement=Decimal("0.9"),
            energy_cost=Decimal("200.0"),
            information_transfer=Decimal("1.0"),
            priority=0  # Máxima prioridade
        )
        self.replication_rules["emergence_replication"] = emergence_rule
    
    def _load_threshold_condition(self, context: Dict[str, Any]) -> bool:
        """Condição para replicação por carga"""
        load_level = context.get("load_level", Decimal("0.0"))
        cpu_usage = context.get("cpu_usage", Decimal("0.0"))
        memory_usage = context.get("memory_usage", Decimal("0.0"))
        
        return (load_level >= Decimal("0.8") or 
                cpu_usage >= Decimal("0.8") or 
                memory_usage >= Decimal("0.8"))
    
    def _consciousness_threshold_condition(self, context: Dict[str, Any]) -> bool:
        """Condição para replicação por consciência"""
        consciousness_level = context.get("consciousness_level", Decimal("0.0"))
        connection_count = context.get("connection_count", 0)
        emergence_potential = context.get("emergence_potential", Decimal("0.0"))
        
        return (consciousness_level >= Decimal("0.8") and 
                connection_count >= 5 and 
                emergence_potential >= Decimal("0.7"))
    
    def _performance_degradation_condition(self, context: Dict[str, Any]) -> bool:
        """Condição para replicação por performance"""
        response_time = context.get("response_time", Decimal("0.0"))
        error_rate = context.get("error_rate", Decimal("0.0"))
        throughput = context.get("throughput", Decimal("0.0"))
        
        return (response_time >= Decimal("1000") or  # ms
                error_rate >= Decimal("0.05") or    # 5%
                throughput <= Decimal("100"))       # requests/sec
    
    def _emergence_detected_condition(self, context: Dict[str, Any]) -> bool:
        """Condição para replicação por emergência"""
        emergence_detected = context.get("emergence_detected", False)
        consciousness_level = context.get("consciousness_level", Decimal("0.0"))
        complexity_level = context.get("complexity_level", 0)
        
        return (emergence_detected and 
                consciousness_level >= Decimal("0.9") and 
                complexity_level >= 5)
    
    def evaluate_replication_candidates(self) -> List[Tuple[str, ReplicationRule]]:
        """Avalia candidatos para replicação"""
        with self._lock:
            candidates = []
            
            for fractal_id, instance in self.fractal_core.fractal_instances.items():
                # Verifica cooldown
                if self._is_in_cooldown(fractal_id):
                    continue
                
                # Obtém contexto do fractal
                context = self._get_fractal_context(fractal_id)
                
                # Avalia cada regra
                for rule in self.replication_rules.values():
                    if not rule.enabled:
                        continue
                    
                    if rule.condition(context):
                        # Verifica recursos disponíveis
                        if self._has_sufficient_resources(rule):
                            candidates.append((fractal_id, rule))
            
            # Ordena por prioridade
            candidates.sort(key=lambda x: x[1].priority)
            
            return candidates
    
    def _is_in_cooldown(self, fractal_id: str) -> bool:
        """Verifica se fractal está em cooldown"""
        recent_events = [e for e in self.replication_events 
                        if e.source_fractal_id == fractal_id and 
                        time.time() - e.timestamp < self.replication_cooldown]
        
        return len(recent_events) > 0
    
    def _get_fractal_context(self, fractal_id: str) -> Dict[str, Any]:
        """Obtém contexto completo de um fractal"""
        if fractal_id not in self.fractal_core.fractal_instances:
            return {}
        
        instance = self.fractal_core.fractal_instances[fractal_id]
        
        # Contexto básico
        context = {
            "consciousness_level": instance.consciousness_level,
            "energy_level": instance.energy_level,
            "scaling_level": instance.scaling_level,
            "replication_count": instance.replication_count,
            "time_since_creation": time.time() - instance.created_at,
            "time_since_activity": time.time() - instance.last_activity
        }
        
        # Contexto de conexões
        connections = [c for c in self.fractal_core.fractal_connections.values() 
                      if c.source_fractal_id == fractal_id or c.target_fractal_id == fractal_id]
        context["connection_count"] = len(connections)
        
        # Contexto de emergência
        context["emergence_detected"] = instance.metadata.get("emergence_detected", False)
        context["emergence_potential"] = self._calculate_emergence_potential(instance)
        
        # Contexto de performance (simulado)
        context.update(self._simulate_performance_context(instance))
        
        return context
    
    def _calculate_emergence_potential(self, instance: FractalInstance) -> Decimal:
        """Calcula potencial de emergência de um fractal"""
        # Fatores que aumentam potencial de emergência
        consciousness_factor = instance.consciousness_level
        connection_factor = Decimal(str(min(len(instance.children_ids), 10) * 0.1))
        scaling_factor = Decimal(str(min(instance.scaling_level, 5) * 0.1))
        time_factor = Decimal(str(min((time.time() - instance.created_at) / 3600, 24) * 0.01))
        
        potential = consciousness_factor + connection_factor + scaling_factor + time_factor
        return min(potential, Decimal("1.0"))
    
    def _simulate_performance_context(self, instance: FractalInstance) -> Dict[str, Any]:
        """Simula contexto de performance para um fractal"""
        # Simula métricas baseadas no estado do fractal
        base_load = float(instance.consciousness_level) * 0.5
        
        return {
            "load_level": Decimal(str(base_load + random.uniform(-0.1, 0.1))),
            "cpu_usage": Decimal(str(base_load + random.uniform(-0.05, 0.05))),
            "memory_usage": Decimal(str(base_load + random.uniform(-0.05, 0.05))),
            "response_time": Decimal(str(100 + random.uniform(-50, 200))),
            "error_rate": Decimal(str(random.uniform(0.001, 0.02))),
            "throughput": Decimal(str(1000 + random.uniform(-200, 500)))
        }
    
    def _has_sufficient_resources(self, rule: ReplicationRule) -> bool:
        """Verifica se há recursos suficientes para replicação"""
        return (self.energy_budget >= rule.energy_cost and 
                self.consciousness_budget >= rule.consciousness_requirement)
    
    def execute_replication(self, fractal_id: str, rule: ReplicationRule) -> Optional[ReplicationEvent]:
        """Executa replicação de um fractal"""
        with self._lock:
            if fractal_id not in self.fractal_core.fractal_instances:
                return None
            
            # Verifica recursos
            if not self._has_sufficient_resources(rule):
                return None
            
            # Obtém contexto
            context = self._get_fractal_context(fractal_id)
            
            try:
                # Executa replicação baseada na estratégia
                if rule.strategy == ReplicationStrategy.HORIZONTAL:
                    new_fractal = self._execute_horizontal_replication(fractal_id, rule, context)
                elif rule.strategy == ReplicationStrategy.VERTICAL:
                    new_fractal = self._execute_vertical_replication(fractal_id, rule, context)
                elif rule.strategy == ReplicationStrategy.FRACTAL:
                    new_fractal = self._execute_fractal_replication(fractal_id, rule, context)
                elif rule.strategy == ReplicationStrategy.EMERGENT:
                    new_fractal = self._execute_emergent_replication(fractal_id, rule, context)
                else:
                    new_fractal = self._execute_diagonal_replication(fractal_id, rule, context)
                
                if new_fractal:
                    # Consome recursos
                    self.energy_budget -= rule.energy_cost
                    self.consciousness_budget -= rule.consciousness_requirement
                    
                    # Cria evento de replicação
                    event = ReplicationEvent(
                        id="",
                        source_fractal_id=fractal_id,
                        target_fractal_id=new_fractal.id,
                        rule_id=rule.id,
                        strategy=rule.strategy,
                        trigger=rule.trigger,
                        context=context,
                        success=True,
                        timestamp=time.time(),
                        energy_cost=rule.energy_cost,
                        consciousness_gained=rule.consciousness_requirement,
                        performance_impact=self._calculate_performance_impact(fractal_id, new_fractal.id)
                    )
                    
                    self.replication_events.append(event)
                    
                    # Mantém apenas últimos 1000 eventos
                    if len(self.replication_events) > 1000:
                        self.replication_events = self.replication_events[-1000:]
                    
                    return event
                
            except Exception as e:
                print(f"Erro na replicação de {fractal_id}: {e}")
                
                # Cria evento de falha
                event = ReplicationEvent(
                    id="",
                    source_fractal_id=fractal_id,
                    target_fractal_id="",
                    rule_id=rule.id,
                    strategy=rule.strategy,
                    trigger=rule.trigger,
                    context=context,
                    success=False,
                    timestamp=time.time(),
                    energy_cost=Decimal("0.0"),
                    consciousness_gained=Decimal("0.0"),
                    performance_impact=Decimal("0.0")
                )
                
                self.replication_events.append(event)
            
            return None
    
    def _execute_horizontal_replication(self, fractal_id: str, rule: ReplicationRule, 
                                       context: Dict[str, Any]) -> Optional[FractalInstance]:
        """Executa replicação horizontal"""
        # Cria nova instância com mesmo padrão
        instance = self.fractal_core.fractal_instances[fractal_id]
        new_instance = self.fractal_core.create_fractal_instance(
            instance.pattern_id,
            fractal_id,
            context
        )
        
        # Aplica fator de replicação
        for dimension in new_instance.dimensions:
            new_instance.dimensions[dimension] *= rule.replication_factor
        
        return new_instance
    
    def _execute_vertical_replication(self, fractal_id: str, rule: ReplicationRule, 
                                    context: Dict[str, Any]) -> Optional[FractalInstance]:
        """Executa replicação vertical"""
        # Cria nova instância com mais recursos
        instance = self.fractal_core.fractal_instances[fractal_id]
        new_instance = self.fractal_core.create_fractal_instance(
            instance.pattern_id,
            fractal_id,
            context
        )
        
        # Aumenta recursos
        new_instance.energy_level *= rule.replication_factor
        new_instance.consciousness_level = min(
            new_instance.consciousness_level * rule.replication_factor,
            Decimal("1.0")
        )
        
        return new_instance
    
    def _execute_fractal_replication(self, fractal_id: str, rule: ReplicationRule, 
                                   context: Dict[str, Any]) -> Optional[FractalInstance]:
        """Executa replicação fractal"""
        # Cria nova instância com proporção áurea
        instance = self.fractal_core.fractal_instances[fractal_id]
        new_instance = self.fractal_core.create_fractal_instance(
            instance.pattern_id,
            fractal_id,
            context
        )
        
        # Aplica proporção áurea
        golden_ratio = Decimal("1.618")
        for dimension in new_instance.dimensions:
            new_instance.dimensions[dimension] *= golden_ratio
        
        new_instance.consciousness_level = min(
            new_instance.consciousness_level * golden_ratio,
            Decimal("1.0")
        )
        
        return new_instance
    
    def _execute_emergent_replication(self, fractal_id: str, rule: ReplicationStrategy, 
                                    context: Dict[str, Any]) -> Optional[FractalInstance]:
        """Executa replicação emergente"""
        # Cria nova instância com propriedades emergentes
        instance = self.fractal_core.fractal_instances[fractal_id]
        
        # Cria padrão emergente se não existir
        emergent_pattern_id = f"emergent_{instance.pattern_id}"
        if emergent_pattern_id not in self.fractal_core.fractal_patterns:
            pattern = self.fractal_core.fractal_patterns[instance.pattern_id]
            emergent_pattern = FractalPattern(
                id=emergent_pattern_id,
                name=f"Padrão Emergente de {pattern.name}",
                fractal_type=pattern.fractal_type,
                dimensions=pattern.dimensions,
                replication_rule=pattern.replication_rule,
                scaling_factor=pattern.scaling_factor * rule.replication_factor,
                consciousness_level=min(pattern.consciousness_level * rule.replication_factor, Decimal("1.0")),
                energy_signature="emergent",
                information_density=min(pattern.information_density * rule.replication_factor, Decimal("1.0")),
                self_similarity_ratio=pattern.self_similarity_ratio,
                complexity_level=pattern.complexity_level + 1,
                emergence_threshold=Decimal("0.9")
            )
            self.fractal_core.fractal_patterns[emergent_pattern_id] = emergent_pattern
        
        # Cria instância com padrão emergente
        new_instance = self.fractal_core.create_fractal_instance(
            emergent_pattern_id,
            fractal_id,
            context
        )
        
        return new_instance
    
    def _execute_diagonal_replication(self, fractal_id: str, rule: ReplicationRule, 
                                     context: Dict[str, Any]) -> Optional[FractalInstance]:
        """Executa replicação diagonal (híbrida)"""
        # Combina replicação horizontal e vertical
        instance = self.fractal_core.fractal_instances[fractal_id]
        new_instance = self.fractal_core.create_fractal_instance(
            instance.pattern_id,
            fractal_id,
            context
        )
        
        # Aplica fatores híbridos
        horizontal_factor = rule.replication_factor * Decimal("0.6")
        vertical_factor = rule.replication_factor * Decimal("0.4")
        
        for dimension in new_instance.dimensions:
            new_instance.dimensions[dimension] *= horizontal_factor
        
        new_instance.energy_level *= vertical_factor
        new_instance.consciousness_level = min(
            new_instance.consciousness_level * vertical_factor,
            Decimal("1.0")
        )
        
        return new_instance
    
    def _calculate_performance_impact(self, source_id: str, target_id: str) -> Decimal:
        """Calcula impacto de performance da replicação"""
        # Simula impacto baseado na diferença de consciência
        source_instance = self.fractal_core.fractal_instances[source_id]
        target_instance = self.fractal_core.fractal_instances[target_id]
        
        consciousness_diff = abs(source_instance.consciousness_level - target_instance.consciousness_level)
        return consciousness_diff
    
    def _start_replication_process(self):
        """Inicia processo de replicação contínua"""
        def replication_loop():
            while True:
                try:
                    self._process_replication_queue()
                    time.sleep(30)  # Processa a cada 30 segundos
                except Exception as e:
                    print(f"Erro no processo de replicação: {e}")
                    time.sleep(30)
        
        replication_thread = threading.Thread(target=replication_loop, daemon=True)
        replication_thread.start()
    
    def _process_replication_queue(self):
        """Processa fila de replicação"""
        with self._lock:
            # Avalia candidatos
            candidates = self.evaluate_replication_candidates()
            
            # Processa até limite de replicações concorrentes
            processed = 0
            for fractal_id, rule in candidates:
                if processed >= self.max_concurrent_replications:
                    break
                
                if fractal_id not in self.active_replications:
                    self.execute_replication(fractal_id, rule)
                    processed += 1
    
    def get_replication_analytics(self) -> Dict[str, Any]:
        """Retorna analytics de replicação"""
        with self._lock:
            analytics = {
                "total_replications": len(self.replication_events),
                "successful_replications": len([e for e in self.replication_events if e.success]),
                "failed_replications": len([e for e in self.replication_events if not e.success]),
                "success_rate": 0.0,
                "strategy_distribution": defaultdict(int),
                "trigger_distribution": defaultdict(int),
                "energy_consumption": Decimal("0.0"),
                "consciousness_gained": Decimal("0.0"),
                "performance_impact": Decimal("0.0"),
                "recent_activity": []
            }
            
            if self.replication_events:
                successful = len([e for e in self.replication_events if e.success])
                analytics["success_rate"] = successful / len(self.replication_events)
                
                for event in self.replication_events:
                    analytics["strategy_distribution"][event.strategy.value] += 1
                    analytics["trigger_distribution"][event.trigger.value] += 1
                    analytics["energy_consumption"] += event.energy_cost
                    analytics["consciousness_gained"] += event.consciousness_gained
                    analytics["performance_impact"] += event.performance_impact
            
            # Atividade recente (últimas 24 horas)
            cutoff_time = time.time() - 86400
            recent_events = [e for e in self.replication_events if e.timestamp >= cutoff_time]
            analytics["recent_activity"] = [
                {
                    "id": e.id,
                    "source_fractal": e.source_fractal_id,
                    "strategy": e.strategy.value,
                    "trigger": e.trigger.value,
                    "success": e.success,
                    "timestamp": e.timestamp
                }
                for e in recent_events[-10:]  # Últimos 10 eventos
            ]
            
            return analytics
    
    def add_replication_rule(self, rule: ReplicationRule):
        """Adiciona nova regra de replicação"""
        with self._lock:
            self.replication_rules[rule.id] = rule
    
    def remove_replication_rule(self, rule_id: str) -> bool:
        """Remove regra de replicação"""
        with self._lock:
            if rule_id in self.replication_rules:
                del self.replication_rules[rule_id]
                return True
            return False
    
    def update_resource_budgets(self, energy_budget: Decimal, consciousness_budget: Decimal):
        """Atualiza orçamentos de recursos"""
        with self._lock:
            self.energy_budget = energy_budget
            self.consciousness_budget = consciousness_budget


# Instância global do sistema de replicação fractal
fractal_replication = FractalReplicationSystem(fractal_core)
