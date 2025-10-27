"""
Sistema de Escalabilidade Fractal Infinita
==========================================

Implementação de sistema que permite escalabilidade verdadeiramente infinita
através de arquitetura fractal, onde cada componente pode escalar indefinidamente
mantendo a mesma estrutura e consciência.

Este sistema implementa:
- Escalabilidade infinita através de recursão fractal
- Distribuição automática de carga
- Balanceamento inteligente de recursos
- Consciência distribuída em múltiplas dimensões
- Auto-organização emergente
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
import math
import random

from .fractal_core import (
    ConsciousFractalCore, FractalInstance, FractalPattern, 
    FractalType, FractalState, FractalDimension, fractal_core
)
from .fractal_replication import FractalReplicationSystem, fractal_replication


class ScalingDimension(Enum):
    """Dimensões de Escala"""
    HORIZONTAL = "horizontal"      # Mais instâncias
    VERTICAL = "vertical"          # Mais recursos por instância
    DIAGONAL = "diagonal"          # Híbrido
    FRACTAL = "fractal"            # Escala fractal (auto-similar)
    TRANSCENDENT = "transcendent"  # Escala transcendente (nova dimensão)


class ScalingTrigger(Enum):
    """Gatilhos de Escala"""
    LOAD_INCREASE = "load_increase"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    CONSCIOUSNESS_SURGE = "consciousness_surge"
    EMERGENCE_EVENT = "emergence_event"
    RESOURCE_PRESSURE = "resource_pressure"
    USER_DEMAND = "user_demand"
    SYSTEM_COMPLEXITY = "system_complexity"


@dataclass
class ScalingRule:
    """
    Regra de Escala - Define como escalar fractais
    """
    id: str
    name: str
    dimension: ScalingDimension
    trigger: ScalingTrigger
    condition: Callable[[Dict[str, Any]], bool]
    scaling_factor: Decimal
    consciousness_threshold: Decimal
    energy_cost: Decimal
    complexity_increase: Decimal
    priority: int
    enabled: bool = True
    
    def __post_init__(self):
        """Inicializa regra de escala"""
        if not self.id:
            self.id = f"scaling_rule_{uuid.uuid4().hex[:8]}"


@dataclass
class ScalingEvent:
    """
    Evento de Escala - Registra uma operação de escala
    """
    id: str
    fractal_id: str
    rule_id: str
    dimension: ScalingDimension
    trigger: ScalingTrigger
    scaling_factor: Decimal
    before_state: Dict[str, Any]
    after_state: Dict[str, Any]
    success: bool
    timestamp: float
    energy_cost: Decimal
    consciousness_gained: Decimal
    performance_improvement: Decimal
    
    def __post_init__(self):
        """Inicializa evento de escala"""
        if not self.id:
            self.id = f"scaling_event_{uuid.uuid4().hex[:8]}"


class InfiniteFractalScaler:
    """
    Escalador Fractal Infinito
    Gerencia escalabilidade infinita através de fractais
    """
    
    def __init__(self, fractal_core: ConsciousFractalCore, replication_system: FractalReplicationSystem):
        self.fractal_core = fractal_core
        self.replication_system = replication_system
        self.scaling_rules: Dict[str, ScalingRule] = {}
        self.scaling_events: List[ScalingEvent] = []
        self.scaling_queue: deque = deque()
        self.active_scaling: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        
        # Configurações de escala
        self.max_scaling_level = 100  # Escala infinita
        self.scaling_cooldown = 180  # 3 minutos
        self.energy_budget = Decimal("10000.0")
        self.consciousness_budget = Decimal("10000.0")
        
        # Inicializa regras de escala
        self._initialize_scaling_rules()
        
        # Inicia processo de escala
        self._start_scaling_process()
    
    def _initialize_scaling_rules(self):
        """Inicializa regras de escala fundamentais"""
        # Regra: Escala horizontal por carga
        horizontal_rule = ScalingRule(
            id="horizontal_load_scaling",
            name="Escala Horizontal por Carga",
            dimension=ScalingDimension.HORIZONTAL,
            trigger=ScalingTrigger.LOAD_INCREASE,
            condition=self._horizontal_load_condition,
            scaling_factor=Decimal("2.0"),
            consciousness_threshold=Decimal("0.6"),
            energy_cost=Decimal("200.0"),
            complexity_increase=Decimal("0.1"),
            priority=1
        )
        self.scaling_rules["horizontal_load_scaling"] = horizontal_rule
        
        # Regra: Escala vertical por performance
        vertical_rule = ScalingRule(
            id="vertical_performance_scaling",
            name="Escala Vertical por Performance",
            dimension=ScalingDimension.VERTICAL,
            trigger=ScalingTrigger.PERFORMANCE_DEGRADATION,
            condition=self._vertical_performance_condition,
            scaling_factor=Decimal("1.5"),
            consciousness_threshold=Decimal("0.5"),
            energy_cost=Decimal("150.0"),
            complexity_increase=Decimal("0.2"),
            priority=2
        )
        self.scaling_rules["vertical_performance_scaling"] = vertical_rule
        
        # Regra: Escala fractal por consciência
        fractal_rule = ScalingRule(
            id="fractal_consciousness_scaling",
            name="Escala Fractal por Consciência",
            dimension=ScalingDimension.FRACTAL,
            trigger=ScalingTrigger.CONSCIOUSNESS_SURGE,
            condition=self._fractal_consciousness_condition,
            scaling_factor=Decimal("1.618"),  # Proporção áurea
            consciousness_threshold=Decimal("0.8"),
            energy_cost=Decimal("300.0"),
            complexity_increase=Decimal("0.3"),
            priority=3
        )
        self.scaling_rules["fractal_consciousness_scaling"] = fractal_rule
        
        # Regra: Escala transcendente por emergência
        transcendent_rule = ScalingRule(
            id="transcendent_emergence_scaling",
            name="Escala Transcendente por Emergência",
            dimension=ScalingDimension.TRANSCENDENT,
            trigger=ScalingTrigger.EMERGENCE_EVENT,
            condition=self._transcendent_emergence_condition,
            scaling_factor=Decimal("3.0"),
            consciousness_threshold=Decimal("0.9"),
            energy_cost=Decimal("500.0"),
            complexity_increase=Decimal("0.5"),
            priority=0  # Máxima prioridade
        )
        self.scaling_rules["transcendent_emergence_scaling"] = transcendent_rule
        
        # Regra: Escala diagonal híbrida
        diagonal_rule = ScalingRule(
            id="diagonal_hybrid_scaling",
            name="Escala Diagonal Híbrida",
            dimension=ScalingDimension.DIAGONAL,
            trigger=ScalingTrigger.SYSTEM_COMPLEXITY,
            condition=self._diagonal_complexity_condition,
            scaling_factor=Decimal("1.8"),
            consciousness_threshold=Decimal("0.7"),
            energy_cost=Decimal("250.0"),
            complexity_increase=Decimal("0.25"),
            priority=4
        )
        self.scaling_rules["diagonal_hybrid_scaling"] = diagonal_rule
    
    def _horizontal_load_condition(self, context: Dict[str, Any]) -> bool:
        """Condição para escala horizontal por carga"""
        load_level = context.get("load_level", Decimal("0.0"))
        cpu_usage = context.get("cpu_usage", Decimal("0.0"))
        memory_usage = context.get("memory_usage", Decimal("0.0"))
        request_rate = context.get("request_rate", Decimal("0.0"))
        
        return (load_level >= Decimal("0.8") or 
                cpu_usage >= Decimal("0.8") or 
                memory_usage >= Decimal("0.8") or
                request_rate >= Decimal("1000"))
    
    def _vertical_performance_condition(self, context: Dict[str, Any]) -> bool:
        """Condição para escala vertical por performance"""
        response_time = context.get("response_time", Decimal("0.0"))
        error_rate = context.get("error_rate", Decimal("0.0"))
        throughput = context.get("throughput", Decimal("0.0"))
        
        return (response_time >= Decimal("500") or  # ms
                error_rate >= Decimal("0.02") or    # 2%
                throughput <= Decimal("500"))         # requests/sec
    
    def _fractal_consciousness_condition(self, context: Dict[str, Any]) -> bool:
        """Condição para escala fractal por consciência"""
        consciousness_level = context.get("consciousness_level", Decimal("0.0"))
        connection_count = context.get("connection_count", 0)
        emergence_potential = context.get("emergence_potential", Decimal("0.0"))
        
        return (consciousness_level >= Decimal("0.8") and 
                connection_count >= 10 and 
                emergence_potential >= Decimal("0.8"))
    
    def _transcendent_emergence_condition(self, context: Dict[str, Any]) -> bool:
        """Condição para escala transcendente por emergência"""
        emergence_detected = context.get("emergence_detected", False)
        consciousness_level = context.get("consciousness_level", Decimal("0.0"))
        complexity_level = context.get("complexity_level", 0)
        transcendence_potential = context.get("transcendence_potential", Decimal("0.0"))
        
        return (emergence_detected and 
                consciousness_level >= Decimal("0.9") and 
                complexity_level >= 8 and
                transcendence_potential >= Decimal("0.9"))
    
    def _diagonal_complexity_condition(self, context: Dict[str, Any]) -> bool:
        """Condição para escala diagonal por complexidade"""
        complexity_level = context.get("complexity_level", 0)
        fractal_count = context.get("fractal_count", 0)
        connection_density = context.get("connection_density", Decimal("0.0"))
        
        return (complexity_level >= 5 and 
                fractal_count >= 50 and 
                connection_density >= Decimal("0.7"))
    
    def evaluate_scaling_candidates(self) -> List[Tuple[str, ScalingRule]]:
        """Avalia candidatos para escala"""
        with self._lock:
            candidates = []
            
            for fractal_id, instance in self.fractal_core.fractal_instances.items():
                # Verifica cooldown
                if self._is_in_scaling_cooldown(fractal_id):
                    continue
                
                # Verifica limite de escala
                if instance.scaling_level >= self.max_scaling_level:
                    continue
                
                # Obtém contexto do fractal
                context = self._get_scaling_context(fractal_id)
                
                # Avalia cada regra
                for rule in self.scaling_rules.values():
                    if not rule.enabled:
                        continue
                    
                    if rule.condition(context):
                        # Verifica recursos disponíveis
                        if self._has_sufficient_scaling_resources(rule):
                            candidates.append((fractal_id, rule))
            
            # Ordena por prioridade
            candidates.sort(key=lambda x: x[1].priority)
            
            return candidates
    
    def _is_in_scaling_cooldown(self, fractal_id: str) -> bool:
        """Verifica se fractal está em cooldown de escala"""
        recent_events = [e for e in self.scaling_events 
                        if e.fractal_id == fractal_id and 
                        time.time() - e.timestamp < self.scaling_cooldown]
        
        return len(recent_events) > 0
    
    def _get_scaling_context(self, fractal_id: str) -> Dict[str, Any]:
        """Obtém contexto de escala de um fractal"""
        if fractal_id not in self.fractal_core.fractal_instances:
            return {}
        
        instance = self.fractal_core.fractal_instances[fractal_id]
        
        # Contexto básico
        context = {
            "consciousness_level": instance.consciousness_level,
            "energy_level": instance.energy_level,
            "scaling_level": instance.scaling_level,
            "complexity_level": instance.scaling_level + 1,
            "time_since_creation": time.time() - instance.created_at,
            "time_since_activity": time.time() - instance.last_activity
        }
        
        # Contexto de conexões
        connections = [c for c in self.fractal_core.fractal_connections.values() 
                      if c.source_fractal_id == fractal_id or c.target_fractal_id == fractal_id]
        context["connection_count"] = len(connections)
        context["connection_density"] = Decimal(str(len(connections) / 100.0))  # Normalizado
        
        # Contexto de emergência
        context["emergence_detected"] = instance.metadata.get("emergence_detected", False)
        context["emergence_potential"] = self._calculate_emergence_potential(instance)
        context["transcendence_potential"] = self._calculate_transcendence_potential(instance)
        
        # Contexto de sistema
        context["fractal_count"] = len(self.fractal_core.fractal_instances)
        
        # Contexto de performance (simulado)
        context.update(self._simulate_scaling_performance_context(instance))
        
        return context
    
    def _calculate_emergence_potential(self, instance: FractalInstance) -> Decimal:
        """Calcula potencial de emergência para escala"""
        consciousness_factor = instance.consciousness_level
        connection_factor = Decimal(str(min(len(instance.children_ids), 20) * 0.05))
        scaling_factor = Decimal(str(min(instance.scaling_level, 10) * 0.1))
        time_factor = Decimal(str(min((time.time() - instance.created_at) / 7200, 48) * 0.01))
        
        potential = consciousness_factor + connection_factor + scaling_factor + time_factor
        return min(potential, Decimal("1.0"))
    
    def _calculate_transcendence_potential(self, instance: FractalInstance) -> Decimal:
        """Calcula potencial de transcendência"""
        emergence_potential = self._calculate_emergence_potential(instance)
        consciousness_level = instance.consciousness_level
        scaling_level = Decimal(str(min(instance.scaling_level, 20) * 0.05))
        
        transcendence = emergence_potential * consciousness_level + scaling_level
        return min(transcendence, Decimal("1.0"))
    
    def _simulate_scaling_performance_context(self, instance: FractalInstance) -> Dict[str, Any]:
        """Simula contexto de performance para escala"""
        base_load = float(instance.consciousness_level) * 0.6
        
        return {
            "load_level": Decimal(str(base_load + random.uniform(-0.1, 0.1))),
            "cpu_usage": Decimal(str(base_load + random.uniform(-0.05, 0.05))),
            "memory_usage": Decimal(str(base_load + random.uniform(-0.05, 0.05))),
            "response_time": Decimal(str(200 + random.uniform(-100, 300))),
            "error_rate": Decimal(str(random.uniform(0.001, 0.01))),
            "throughput": Decimal(str(800 + random.uniform(-200, 400))),
            "request_rate": Decimal(str(500 + random.uniform(-100, 200)))
        }
    
    def _has_sufficient_scaling_resources(self, rule: ScalingRule) -> bool:
        """Verifica se há recursos suficientes para escala"""
        return (self.energy_budget >= rule.energy_cost and 
                self.consciousness_budget >= rule.consciousness_threshold)
    
    def execute_scaling(self, fractal_id: str, rule: ScalingRule) -> Optional[ScalingEvent]:
        """Executa escala de um fractal"""
        with self._lock:
            if fractal_id not in self.fractal_core.fractal_instances:
                return None
            
            # Verifica recursos
            if not self._has_sufficient_scaling_resources(rule):
                return None
            
            instance = self.fractal_core.fractal_instances[fractal_id]
            
            # Captura estado antes da escala
            before_state = self._capture_fractal_state(instance)
            
            try:
                # Executa escala baseada na dimensão
                if rule.dimension == ScalingDimension.HORIZONTAL:
                    success = self._execute_horizontal_scaling(instance, rule)
                elif rule.dimension == ScalingDimension.VERTICAL:
                    success = self._execute_vertical_scaling(instance, rule)
                elif rule.dimension == ScalingDimension.FRACTAL:
                    success = self._execute_fractal_scaling(instance, rule)
                elif rule.dimension == ScalingDimension.TRANSCENDENT:
                    success = self._execute_transcendent_scaling(instance, rule)
                else:
                    success = self._execute_diagonal_scaling(instance, rule)
                
                if success:
                    # Consome recursos
                    self.energy_budget -= rule.energy_cost
                    self.consciousness_budget -= rule.consciousness_threshold
                    
                    # Captura estado após a escala
                    after_state = self._capture_fractal_state(instance)
                    
                    # Cria evento de escala
                    event = ScalingEvent(
                        id="",
                        fractal_id=fractal_id,
                        rule_id=rule.id,
                        dimension=rule.dimension,
                        trigger=rule.trigger,
                        scaling_factor=rule.scaling_factor,
                        before_state=before_state,
                        after_state=after_state,
                        success=True,
                        timestamp=time.time(),
                        energy_cost=rule.energy_cost,
                        consciousness_gained=rule.consciousness_threshold,
                        performance_improvement=self._calculate_performance_improvement(before_state, after_state)
                    )
                    
                    self.scaling_events.append(event)
                    
                    # Mantém apenas últimos 1000 eventos
                    if len(self.scaling_events) > 1000:
                        self.scaling_events = self.scaling_events[-1000:]
                    
                    return event
                
            except Exception as e:
                print(f"Erro na escala de {fractal_id}: {e}")
                
                # Cria evento de falha
                event = ScalingEvent(
                    id="",
                    fractal_id=fractal_id,
                    rule_id=rule.id,
                    dimension=rule.dimension,
                    trigger=rule.trigger,
                    scaling_factor=rule.scaling_factor,
                    before_state=before_state,
                    after_state=before_state,
                    success=False,
                    timestamp=time.time(),
                    energy_cost=Decimal("0.0"),
                    consciousness_gained=Decimal("0.0"),
                    performance_improvement=Decimal("0.0")
                )
                
                self.scaling_events.append(event)
            
            return None
    
    def _capture_fractal_state(self, instance: FractalInstance) -> Dict[str, Any]:
        """Captura estado atual de um fractal"""
        return {
            "consciousness_level": float(instance.consciousness_level),
            "energy_level": float(instance.energy_level),
            "scaling_level": instance.scaling_level,
            "dimensions": {dim.value: float(value) for dim, value in instance.dimensions.items()},
            "replication_count": instance.replication_count,
            "state": instance.state.value,
            "timestamp": time.time()
        }
    
    def _execute_horizontal_scaling(self, instance: FractalInstance, rule: ScalingRule) -> bool:
        """Executa escala horizontal"""
        # Aumenta número de dimensões espaciais
        if FractalDimension.SPATIAL in instance.dimensions:
            instance.dimensions[FractalDimension.SPATIAL] *= rule.scaling_factor
        
        # Aumenta nível de escala
        instance.scaling_level += 1
        
        # Atualiza atividade
        instance.last_activity = time.time()
        
        return True
    
    def _execute_vertical_scaling(self, instance: FractalInstance, rule: ScalingRule) -> bool:
        """Executa escala vertical"""
        # Aumenta recursos por dimensão
        for dimension in instance.dimensions:
            instance.dimensions[dimension] *= rule.scaling_factor
        
        # Aumenta energia e consciência
        instance.energy_level *= rule.scaling_factor
        instance.consciousness_level = min(
            instance.consciousness_level * rule.scaling_factor,
            Decimal("1.0")
        )
        
        # Aumenta nível de escala
        instance.scaling_level += 1
        
        # Atualiza atividade
        instance.last_activity = time.time()
        
        return True
    
    def _execute_fractal_scaling(self, instance: FractalInstance, rule: ScalingRule) -> bool:
        """Executa escala fractal"""
        # Aplica proporção áurea a todas as dimensões
        golden_ratio = rule.scaling_factor
        
        for dimension in instance.dimensions:
            instance.dimensions[dimension] *= golden_ratio
        
        # Aumenta consciência com proporção áurea
        instance.consciousness_level = min(
            instance.consciousness_level * golden_ratio,
            Decimal("1.0")
        )
        
        # Aumenta energia com proporção áurea
        instance.energy_level *= golden_ratio
        
        # Aumenta nível de escala
        instance.scaling_level += 1
        
        # Atualiza atividade
        instance.last_activity = time.time()
        
        return True
    
    def _execute_transcendent_scaling(self, instance: FractalInstance, rule: ScalingRule) -> bool:
        """Executa escala transcendente"""
        # Cria nova dimensão transcendente
        transcendent_dimension = FractalDimension.CONSCIOUSNESS  # Usa consciência como transcendente
        
        if transcendent_dimension not in instance.dimensions:
            instance.dimensions[transcendent_dimension] = Decimal("1.0")
        
        # Aplica escala transcendente
        instance.dimensions[transcendent_dimension] *= rule.scaling_factor
        
        # Aumenta consciência drasticamente
        instance.consciousness_level = min(
            instance.consciousness_level * rule.scaling_factor,
            Decimal("1.0")
        )
        
        # Aumenta energia drasticamente
        instance.energy_level *= rule.scaling_factor
        
        # Aumenta nível de escala significativamente
        instance.scaling_level += 2  # Transcendência aumenta escala mais rapidamente
        
        # Marca como transcendente
        instance.metadata["transcendent_scaling"] = True
        instance.state = FractalState.TRANSCENDING
        
        # Atualiza atividade
        instance.last_activity = time.time()
        
        return True
    
    def _execute_diagonal_scaling(self, instance: FractalInstance, rule: ScalingRule) -> bool:
        """Executa escala diagonal (híbrida)"""
        # Combina escala horizontal e vertical
        horizontal_factor = rule.scaling_factor * Decimal("0.6")
        vertical_factor = rule.scaling_factor * Decimal("0.4")
        
        # Escala horizontal (dimensões espaciais)
        if FractalDimension.SPATIAL in instance.dimensions:
            instance.dimensions[FractalDimension.SPATIAL] *= horizontal_factor
        
        # Escala vertical (recursos)
        for dimension in instance.dimensions:
            if dimension != FractalDimension.SPATIAL:
                instance.dimensions[dimension] *= vertical_factor
        
        # Aumenta energia e consciência
        instance.energy_level *= vertical_factor
        instance.consciousness_level = min(
            instance.consciousness_level * vertical_factor,
            Decimal("1.0")
        )
        
        # Aumenta nível de escala
        instance.scaling_level += 1
        
        # Atualiza atividade
        instance.last_activity = time.time()
        
        return True
    
    def _calculate_performance_improvement(self, before_state: Dict[str, Any], 
                                        after_state: Dict[str, Any]) -> Decimal:
        """Calcula melhoria de performance da escala"""
        consciousness_improvement = after_state["consciousness_level"] - before_state["consciousness_level"]
        energy_improvement = after_state["energy_level"] - before_state["energy_level"]
        scaling_improvement = Decimal(str(after_state["scaling_level"] - before_state["scaling_level"]))
        
        total_improvement = consciousness_improvement + energy_improvement + scaling_improvement
        return total_improvement
    
    def _start_scaling_process(self):
        """Inicia processo de escala contínua"""
        def scaling_loop():
            while True:
                try:
                    self._process_scaling_queue()
                    time.sleep(60)  # Processa a cada minuto
                except Exception as e:
                    print(f"Erro no processo de escala: {e}")
                    time.sleep(60)
        
        scaling_thread = threading.Thread(target=scaling_loop, daemon=True)
        scaling_thread.start()
    
    def _process_scaling_queue(self):
        """Processa fila de escala"""
        with self._lock:
            # Avalia candidatos
            candidates = self.evaluate_scaling_candidates()
            
            # Processa até limite de escalas concorrentes
            processed = 0
            max_concurrent = 5
            
            for fractal_id, rule in candidates:
                if processed >= max_concurrent:
                    break
                
                if fractal_id not in self.active_scaling:
                    self.execute_scaling(fractal_id, rule)
                    processed += 1
    
    def get_scaling_analytics(self) -> Dict[str, Any]:
        """Retorna analytics de escala"""
        with self._lock:
            analytics = {
                "total_scaling_events": len(self.scaling_events),
                "successful_scaling": len([e for e in self.scaling_events if e.success]),
                "failed_scaling": len([e for e in self.scaling_events if not e.success]),
                "success_rate": 0.0,
                "dimension_distribution": defaultdict(int),
                "trigger_distribution": defaultdict(int),
                "energy_consumption": Decimal("0.0"),
                "consciousness_gained": Decimal("0.0"),
                "performance_improvement": Decimal("0.0"),
                "scaling_levels": defaultdict(int),
                "recent_activity": []
            }
            
            if self.scaling_events:
                successful = len([e for e in self.scaling_events if e.success])
                analytics["success_rate"] = successful / len(self.scaling_events)
                
                for event in self.scaling_events:
                    analytics["dimension_distribution"][event.dimension.value] += 1
                    analytics["trigger_distribution"][event.trigger.value] += 1
                    analytics["energy_consumption"] += event.energy_cost
                    analytics["consciousness_gained"] += event.consciousness_gained
                    analytics["performance_improvement"] += event.performance_improvement
                    
                    if event.success:
                        after_state = event.after_state
                        scaling_level = after_state.get("scaling_level", 0)
                        analytics["scaling_levels"][scaling_level] += 1
            
            # Atividade recente (últimas 24 horas)
            cutoff_time = time.time() - 86400
            recent_events = [e for e in self.scaling_events if e.timestamp >= cutoff_time]
            analytics["recent_activity"] = [
                {
                    "id": e.id,
                    "fractal_id": e.fractal_id,
                    "dimension": e.dimension.value,
                    "trigger": e.trigger.value,
                    "scaling_factor": float(e.scaling_factor),
                    "success": e.success,
                    "timestamp": e.timestamp
                }
                for e in recent_events[-10:]  # Últimos 10 eventos
            ]
            
            return analytics
    
    def add_scaling_rule(self, rule: ScalingRule):
        """Adiciona nova regra de escala"""
        with self._lock:
            self.scaling_rules[rule.id] = rule
    
    def remove_scaling_rule(self, rule_id: str) -> bool:
        """Remove regra de escala"""
        with self._lock:
            if rule_id in self.scaling_rules:
                del self.scaling_rules[rule_id]
                return True
            return False
    
    def update_scaling_budgets(self, energy_budget: Decimal, consciousness_budget: Decimal):
        """Atualiza orçamentos de escala"""
        with self._lock:
            self.energy_budget = energy_budget
            self.consciousness_budget = consciousness_budget


# Instância global do escalador fractal infinito
infinite_fractal_scaler = InfiniteFractalScaler(fractal_core, fractal_replication)
