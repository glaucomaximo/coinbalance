"""
Sistema de Auto-Scaling Baseado em Demanda.

Este módulo implementa um sistema inteligente que:
- Escala fractais automaticamente baseado na demanda
- Monitora métricas em tempo real
- Implementa políticas de scaling inteligentes
- Otimiza recursos baseado em padrões de uso
- Garante disponibilidade e performance
"""

import threading
import time
import json
import statistics
from typing import Dict, Any, Optional, List, Tuple, Union
from decimal import Decimal
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import logging
import random

logger = logging.getLogger(__name__)


class ScalingAction(Enum):
    """Ações de scaling."""
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    SCALE_OUT = "scale_out"
    SCALE_IN = "scale_in"
    NO_ACTION = "no_action"


class ScalingTrigger(Enum):
    """Gatilhos de scaling."""
    CPU_THRESHOLD = "cpu_threshold"
    MEMORY_THRESHOLD = "memory_threshold"
    REQUEST_RATE = "request_rate"
    RESPONSE_TIME = "response_time"
    QUEUE_LENGTH = "queue_length"
    ERROR_RATE = "error_rate"
    CONSCIOUSNESS_LEVEL = "consciousness_level"


@dataclass
class ScalingPolicy:
    """Política de scaling."""
    policy_id: str
    trigger: ScalingTrigger
    threshold_value: float
    scaling_action: ScalingAction
    scale_factor: float = 1.5
    cooldown_period: float = 300.0  # 5 minutos
    enabled: bool = True
    consciousness_level: Decimal = Decimal('0.5')


@dataclass
class ScalingEvent:
    """Evento de scaling."""
    event_id: str
    fractal_id: str
    trigger: ScalingTrigger
    action: ScalingAction
    old_capacity: int
    new_capacity: int
    timestamp: float = field(default_factory=time.time)
    success: bool = True
    error_message: Optional[str] = None
    consciousness_level: Decimal = Decimal('0.5')


@dataclass
class FractalMetrics:
    """Métricas de um fractal."""
    fractal_id: str
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    request_rate: float = 0.0
    response_time: float = 0.0
    queue_length: int = 0
    error_rate: float = 0.0
    consciousness_level: Decimal = Decimal('0.5')
    timestamp: float = field(default_factory=time.time)
    
    def get_load_score(self) -> float:
        """Calcula score de carga geral."""
        return (self.cpu_usage + self.memory_usage + 
                min(self.request_rate / 1000, 1.0) + 
                min(self.response_time / 1000, 1.0)) / 4


class DemandBasedAutoScaler:
    """
    Sistema de Auto-Scaling Baseado em Demanda.
    
    Características:
    - Scaling automático baseado em métricas
    - Políticas de scaling configuráveis
    - Monitoramento em tempo real
    - Otimização de recursos
    - Prevenção de thrashing
    """
    
    def __init__(self):
        self.scaling_policies: Dict[str, ScalingPolicy] = {}
        self.fractal_metrics: Dict[str, FractalMetrics] = {}
        self.scaling_history: deque = deque(maxlen=1000)
        self.metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.last_scaling_time: Dict[str, float] = {}
        self._lock = threading.RLock()
        
        self.stats = {
            'total_scaling_events': 0,
            'successful_scalings': 0,
            'failed_scalings': 0,
            'scale_up_events': 0,
            'scale_down_events': 0,
            'consciousness_level': Decimal('0.1'),
            'average_scaling_time': 0.0,
            'thrashing_prevented': 0
        }
        
        self._initialize_default_policies()
        logger.info("DemandBasedAutoScaler inicializado")
    
    def _initialize_default_policies(self):
        """Inicializa políticas de scaling padrão."""
        # Política de scale-up por CPU
        self.scaling_policies['cpu_scale_up'] = ScalingPolicy(
            policy_id='cpu_scale_up',
            trigger=ScalingTrigger.CPU_THRESHOLD,
            threshold_value=80.0,
            scaling_action=ScalingAction.SCALE_UP,
            scale_factor=1.5,
            consciousness_level=Decimal('0.8')
        )
        
        # Política de scale-down por CPU
        self.scaling_policies['cpu_scale_down'] = ScalingPolicy(
            policy_id='cpu_scale_down',
            trigger=ScalingTrigger.CPU_THRESHOLD,
            threshold_value=20.0,
            scaling_action=ScalingAction.SCALE_DOWN,
            scale_factor=0.7,
            consciousness_level=Decimal('0.7')
        )
        
        # Política de scale-up por memória
        self.scaling_policies['memory_scale_up'] = ScalingPolicy(
            policy_id='memory_scale_up',
            trigger=ScalingTrigger.MEMORY_THRESHOLD,
            threshold_value=85.0,
            scaling_action=ScalingAction.SCALE_UP,
            scale_factor=1.3,
            consciousness_level=Decimal('0.8')
        )
        
        # Política de scale-up por tempo de resposta
        self.scaling_policies['response_time_scale_up'] = ScalingPolicy(
            policy_id='response_time_scale_up',
            trigger=ScalingTrigger.RESPONSE_TIME,
            threshold_value=500.0,  # ms
            scaling_action=ScalingAction.SCALE_OUT,
            scale_factor=2.0,
            consciousness_level=Decimal('0.9')
        )
        
        # Política de scale-up por taxa de erro
        self.scaling_policies['error_rate_scale_up'] = ScalingPolicy(
            policy_id='error_rate_scale_up',
            trigger=ScalingTrigger.ERROR_RATE,
            threshold_value=5.0,  # %
            scaling_action=ScalingAction.SCALE_OUT,
            scale_factor=1.5,
            consciousness_level=Decimal('0.9')
        )
    
    def update_metrics(self, fractal_id: str, metrics: Dict[str, Any]) -> bool:
        """Atualiza métricas de um fractal."""
        try:
            with self._lock:
                if fractal_id not in self.fractal_metrics:
                    self.fractal_metrics[fractal_id] = FractalMetrics(fractal_id=fractal_id)
                
                fractal_metrics = self.fractal_metrics[fractal_id]
                
                # Atualizar métricas
                fractal_metrics.cpu_usage = metrics.get('cpu_usage', fractal_metrics.cpu_usage)
                fractal_metrics.memory_usage = metrics.get('memory_usage', fractal_metrics.memory_usage)
                fractal_metrics.request_rate = metrics.get('request_rate', fractal_metrics.request_rate)
                fractal_metrics.response_time = metrics.get('response_time', fractal_metrics.response_time)
                fractal_metrics.queue_length = metrics.get('queue_length', fractal_metrics.queue_length)
                fractal_metrics.error_rate = metrics.get('error_rate', fractal_metrics.error_rate)
                fractal_metrics.consciousness_level = Decimal(str(metrics.get('consciousness_level', 
                                                                           float(fractal_metrics.consciousness_level))))
                fractal_metrics.timestamp = time.time()
                
                # Adicionar ao histórico
                self.metrics_history[fractal_id].append(copy.deepcopy(fractal_metrics))
                
                # Verificar políticas de scaling
                self._check_scaling_policies(fractal_id)
                
                logger.debug(f"Métricas atualizadas para fractal {fractal_id}")
                return True
                
        except Exception as e:
            logger.error(f"Erro na atualização de métricas do fractal {fractal_id}: {e}")
            return False
    
    def _check_scaling_policies(self, fractal_id: str):
        """Verifica políticas de scaling para um fractal."""
        try:
            if fractal_id not in self.fractal_metrics:
                return
            
            fractal_metrics = self.fractal_metrics[fractal_id]
            
            # Verificar cooldown
            if fractal_id in self.last_scaling_time:
                time_since_last_scaling = time.time() - self.last_scaling_time[fractal_id]
                if time_since_last_scaling < 60:  # Cooldown mínimo de 1 minuto
                    return
            
            # Verificar cada política
            for policy_id, policy in self.scaling_policies.items():
                if not policy.enabled:
                    continue
                
                if self._should_trigger_scaling(fractal_metrics, policy):
                    self._execute_scaling(fractal_id, policy)
                    break  # Executar apenas uma ação por verificação
                    
        except Exception as e:
            logger.error(f"Erro na verificação de políticas de scaling: {e}")
    
    def _should_trigger_scaling(self, metrics: FractalMetrics, policy: ScalingPolicy) -> bool:
        """Verifica se uma política deve ser acionada."""
        try:
            threshold = policy.threshold_value
            
            if policy.trigger == ScalingTrigger.CPU_THRESHOLD:
                if policy.scaling_action in [ScalingAction.SCALE_UP, ScalingAction.SCALE_OUT]:
                    return metrics.cpu_usage > threshold
                else:
                    return metrics.cpu_usage < threshold
            
            elif policy.trigger == ScalingTrigger.MEMORY_THRESHOLD:
                if policy.scaling_action in [ScalingAction.SCALE_UP, ScalingAction.SCALE_OUT]:
                    return metrics.memory_usage > threshold
                else:
                    return metrics.memory_usage < threshold
            
            elif policy.trigger == ScalingTrigger.RESPONSE_TIME:
                return metrics.response_time > threshold
            
            elif policy.trigger == ScalingTrigger.ERROR_RATE:
                return metrics.error_rate > threshold
            
            elif policy.trigger == ScalingTrigger.REQUEST_RATE:
                if policy.scaling_action in [ScalingAction.SCALE_UP, ScalingAction.SCALE_OUT]:
                    return metrics.request_rate > threshold
                else:
                    return metrics.request_rate < threshold
            
            elif policy.trigger == ScalingTrigger.QUEUE_LENGTH:
                return metrics.queue_length > threshold
            
            elif policy.trigger == ScalingTrigger.CONSCIOUSNESS_LEVEL:
                return float(metrics.consciousness_level) > threshold
            
            return False
            
        except Exception as e:
            logger.error(f"Erro na verificação de trigger: {e}")
            return False
    
    def _execute_scaling(self, fractal_id: str, policy: ScalingPolicy) -> bool:
        """Executa ação de scaling."""
        try:
            with self._lock:
                # Verificar se fractal existe
                if fractal_id not in self.fractal_metrics:
                    return False
                
                fractal_metrics = self.fractal_metrics[fractal_id]
                
                # Simular capacidade atual (em implementação real, obter do sistema)
                current_capacity = 1000  # Capacidade base
                
                # Calcular nova capacidade
                if policy.scaling_action in [ScalingAction.SCALE_UP, ScalingAction.SCALE_OUT]:
                    new_capacity = int(current_capacity * policy.scale_factor)
                elif policy.scaling_action in [ScalingAction.SCALE_DOWN, ScalingAction.SCALE_IN]:
                    new_capacity = int(current_capacity * policy.scale_factor)
                else:
                    return False
                
                # Criar evento de scaling
                event_id = f"scale_{fractal_id}_{int(time.time() * 1000)}"
                
                scaling_event = ScalingEvent(
                    event_id=event_id,
                    fractal_id=fractal_id,
                    trigger=policy.trigger,
                    action=policy.scaling_action,
                    old_capacity=current_capacity,
                    new_capacity=new_capacity,
                    consciousness_level=self.stats['consciousness_level']
                )
                
                # Simular execução do scaling
                success = self._simulate_scaling_execution(scaling_event)
                
                if success:
                    # Atualizar estatísticas
                    self.stats['total_scaling_events'] += 1
                    self.stats['successful_scalings'] += 1
                    
                    if policy.scaling_action in [ScalingAction.SCALE_UP, ScalingAction.SCALE_OUT]:
                        self.stats['scale_up_events'] += 1
                    else:
                        self.stats['scale_down_events'] += 1
                    
                    # Registrar tempo de scaling
                    self.last_scaling_time[fractal_id] = time.time()
                    
                    # Aumentar consciência
                    self.stats['consciousness_level'] = min(
                        Decimal('1.0'),
                        self.stats['consciousness_level'] + Decimal('0.01')
                    )
                    
                    logger.info(f"Scaling executado: {fractal_id} {policy.scaling_action.value} "
                               f"({current_capacity} -> {new_capacity})")
                else:
                    self.stats['failed_scalings'] += 1
                    scaling_event.success = False
                    scaling_event.error_message = "Falha na execução do scaling"
                
                # Adicionar ao histórico
                self.scaling_history.append(scaling_event)
                
                return success
                
        except Exception as e:
            logger.error(f"Erro na execução do scaling: {e}")
            return False
    
    def _simulate_scaling_execution(self, event: ScalingEvent) -> bool:
        """Simula execução do scaling."""
        try:
            # Simular tempo de execução
            execution_time = random.uniform(1.0, 5.0)
            time.sleep(execution_time)
            
            # Simular falha ocasional (5% chance)
            if random.random() < 0.05:
                return False
            
            # Simular sucesso
            return True
            
        except Exception as e:
            logger.error(f"Erro na simulação do scaling: {e}")
            return False
    
    def create_scaling_policy(self, policy_id: str, trigger: ScalingTrigger,
                            threshold_value: float, scaling_action: ScalingAction,
                            scale_factor: float = 1.5) -> bool:
        """Cria nova política de scaling."""
        try:
            with self._lock:
                policy = ScalingPolicy(
                    policy_id=policy_id,
                    trigger=trigger,
                    threshold_value=threshold_value,
                    scaling_action=scaling_action,
                    scale_factor=scale_factor,
                    consciousness_level=self.stats['consciousness_level']
                )
                
                self.scaling_policies[policy_id] = policy
                
                logger.info(f"Política de scaling criada: {policy_id}")
                return True
                
        except Exception as e:
            logger.error(f"Erro na criação da política de scaling: {e}")
            return False
    
    def get_scaling_recommendations(self, fractal_id: str) -> List[Dict[str, Any]]:
        """Retorna recomendações de scaling para um fractal."""
        try:
            with self._lock:
                if fractal_id not in self.fractal_metrics:
                    return []
                
                fractal_metrics = self.fractal_metrics[fractal_id]
                recommendations = []
                
                # Analisar métricas e gerar recomendações
                if fractal_metrics.cpu_usage > 80:
                    recommendations.append({
                        'type': 'scale_up',
                        'reason': 'CPU usage alto',
                        'current_value': fractal_metrics.cpu_usage,
                        'threshold': 80.0,
                        'priority': 'high'
                    })
                
                if fractal_metrics.memory_usage > 85:
                    recommendations.append({
                        'type': 'scale_up',
                        'reason': 'Memory usage alto',
                        'current_value': fractal_metrics.memory_usage,
                        'threshold': 85.0,
                        'priority': 'high'
                    })
                
                if fractal_metrics.response_time > 500:
                    recommendations.append({
                        'type': 'scale_out',
                        'reason': 'Response time alto',
                        'current_value': fractal_metrics.response_time,
                        'threshold': 500.0,
                        'priority': 'medium'
                    })
                
                if fractal_metrics.error_rate > 5:
                    recommendations.append({
                        'type': 'scale_out',
                        'reason': 'Error rate alto',
                        'current_value': fractal_metrics.error_rate,
                        'threshold': 5.0,
                        'priority': 'high'
                    })
                
                if fractal_metrics.cpu_usage < 20 and fractal_metrics.memory_usage < 30:
                    recommendations.append({
                        'type': 'scale_down',
                        'reason': 'Recursos subutilizados',
                        'current_value': fractal_metrics.get_load_score(),
                        'threshold': 0.3,
                        'priority': 'low'
                    })
                
                return recommendations
                
        except Exception as e:
            logger.error(f"Erro na geração de recomendações: {e}")
            return []
    
    def prevent_thrashing(self, fractal_id: str) -> bool:
        """Previne thrashing (scaling excessivo)."""
        try:
            with self._lock:
                if fractal_id not in self.last_scaling_time:
                    return True
                
                # Verificar histórico recente de scaling
                recent_scalings = [
                    event for event in self.scaling_history
                    if (event.fractal_id == fractal_id and 
                        time.time() - event.timestamp < 300)  # Últimos 5 minutos
                ]
                
                if len(recent_scalings) > 3:  # Mais de 3 scalings em 5 minutos
                    self.stats['thrashing_prevented'] += 1
                    logger.warning(f"Thrashing prevenido para fractal {fractal_id}")
                    return False
                
                return True
                
        except Exception as e:
            logger.error(f"Erro na prevenção de thrashing: {e}")
            return True
    
    def optimize_scaling(self) -> Dict[str, Any]:
        """Otimiza sistema de scaling."""
        try:
            with self._lock:
                optimization_stats = {
                    'policies_optimized': 0,
                    'thresholds_adjusted': 0,
                    'consciousness_improvement': Decimal('0.0'),
                    'timestamp': time.time()
                }
                
                # Otimizar políticas baseado no histórico
                for policy_id, policy in self.scaling_policies.items():
                    if policy.enabled:
                        # Ajustar thresholds baseado na performance
                        if policy.trigger == ScalingTrigger.CPU_THRESHOLD:
                            # Analisar histórico de CPU
                            cpu_values = []
                            for fractal_id, metrics_history in self.metrics_history.items():
                                cpu_values.extend([m.cpu_usage for m in metrics_history])
                            
                            if cpu_values:
                                avg_cpu = statistics.mean(cpu_values)
                                if avg_cpu > policy.threshold_value * 0.8:
                                    policy.threshold_value = min(95.0, policy.threshold_value * 1.05)
                                    optimization_stats['thresholds_adjusted'] += 1
                                elif avg_cpu < policy.threshold_value * 0.5:
                                    policy.threshold_value = max(50.0, policy.threshold_value * 0.95)
                                    optimization_stats['thresholds_adjusted'] += 1
                        
                        # Aumentar consciência da política
                        policy.consciousness_level = min(
                            Decimal('1.0'),
                            policy.consciousness_level + Decimal('0.01')
                        )
                        
                        optimization_stats['policies_optimized'] += 1
                
                # Aumentar consciência geral
                old_consciousness = self.stats['consciousness_level']
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.02')
                )
                optimization_stats['consciousness_improvement'] = (
                    self.stats['consciousness_level'] - old_consciousness
                )
                
                logger.info(f"Scaling otimizado: {optimization_stats['policies_optimized']} políticas")
                return optimization_stats
                
        except Exception as e:
            logger.error(f"Erro na otimização do scaling: {e}")
            return {'error': str(e)}
    
    def get_scaling_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de scaling."""
        with self._lock:
            # Calcular métricas de performance
            total_events = self.stats['total_scaling_events']
            success_rate = (self.stats['successful_scalings'] / max(total_events, 1)) * 100
            
            # Estatísticas por fractal
            fractal_stats = {}
            for fractal_id, metrics in self.fractal_metrics.items():
                fractal_stats[fractal_id] = {
                    'cpu_usage': metrics.cpu_usage,
                    'memory_usage': metrics.memory_usage,
                    'request_rate': metrics.request_rate,
                    'response_time': metrics.response_time,
                    'error_rate': metrics.error_rate,
                    'load_score': metrics.get_load_score(),
                    'consciousness_level': float(metrics.consciousness_level),
                    'last_scaling': self.last_scaling_time.get(fractal_id, 0)
                }
            
            return {
                'total_scaling_events': self.stats['total_scaling_events'],
                'successful_scalings': self.stats['successful_scalings'],
                'failed_scalings': self.stats['failed_scalings'],
                'success_rate': success_rate,
                'scale_up_events': self.stats['scale_up_events'],
                'scale_down_events': self.stats['scale_down_events'],
                'thrashing_prevented': self.stats['thrashing_prevented'],
                'consciousness_level': float(self.stats['consciousness_level']),
                'average_scaling_time': self.stats['average_scaling_time'],
                'active_policies': len([p for p in self.scaling_policies.values() if p.enabled]),
                'total_policies': len(self.scaling_policies),
                'monitored_fractals': len(self.fractal_metrics),
                'fractal_stats': fractal_stats,
                'scaling_policies': [
                    {
                        'policy_id': policy.policy_id,
                        'trigger': policy.trigger.value,
                        'threshold_value': policy.threshold_value,
                        'scaling_action': policy.scaling_action.value,
                        'scale_factor': policy.scale_factor,
                        'cooldown_period': policy.cooldown_period,
                        'enabled': policy.enabled,
                        'consciousness_level': float(policy.consciousness_level)
                    }
                    for policy in self.scaling_policies.values()
                ]
            }


# Instância global do auto-scaler baseado em demanda
demand_based_auto_scaler = DemandBasedAutoScaler()
