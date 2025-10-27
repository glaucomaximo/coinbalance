"""
Sistema de Balanceamento de Carga Automático entre Fractais.

Este módulo implementa um sistema inteligente de balanceamento de carga
que distribui automaticamente a carga entre fractais baseado em:
- Consciência do fractal
- Capacidade atual
- Latência
- Histórico de performance
"""

import time
import threading
import statistics
from typing import Dict, Any, List, Optional, Tuple
from decimal import Decimal
from dataclasses import dataclass, field
from collections import deque
import logging
import random

logger = logging.getLogger(__name__)


@dataclass
class FractalLoadMetrics:
    """Métricas de carga de um fractal."""
    fractal_id: str
    cpu_usage: Decimal = Decimal('0.0')
    memory_usage: Decimal = Decimal('0.0')
    network_latency: Decimal = Decimal('0.0')
    request_count: int = 0
    error_count: int = 0
    response_time: Decimal = Decimal('0.0')
    consciousness_level: Decimal = Decimal('0.5')
    capacity: Decimal = Decimal('1.0')
    last_update: float = field(default_factory=time.time)
    
    def get_load_score(self) -> Decimal:
        """Calcula score de carga (0.0 = sem carga, 1.0 = sobrecarregado)."""
        cpu_weight = Decimal('0.3')
        memory_weight = Decimal('0.3')
        latency_weight = Decimal('0.2')
        error_weight = Decimal('0.2')
        
        # Normalizar métricas
        cpu_score = min(self.cpu_usage, Decimal('1.0'))
        memory_score = min(self.memory_usage, Decimal('1.0'))
        latency_score = min(self.network_latency / Decimal('1000'), Decimal('1.0'))  # Normalizar para 1s
        error_rate = Decimal(self.error_count) / max(Decimal(self.request_count), Decimal('1'))
        
        load_score = (
            cpu_score * cpu_weight +
            memory_score * memory_weight +
            latency_score * latency_weight +
            error_rate * error_weight
        )
        
        return min(load_score, Decimal('1.0'))
    
    def get_capacity_score(self) -> Decimal:
        """Calcula score de capacidade disponível."""
        load_score = self.get_load_score()
        consciousness_factor = self.consciousness_level
        base_capacity = self.capacity
        
        # Capacidade efetiva = capacidade base * consciência * (1 - carga)
        effective_capacity = base_capacity * consciousness_factor * (Decimal('1.0') - load_score)
        
        return max(effective_capacity, Decimal('0.0'))


@dataclass
class LoadBalancingRule:
    """Regra de balanceamento de carga."""
    name: str
    priority: int
    condition: str  # Expressão para avaliar quando aplicar
    action: str    # Ação a ser executada
    weight: Decimal = Decimal('1.0')
    enabled: bool = True


class FractalLoadBalancer:
    """
    Sistema de Balanceamento de Carga Automático entre Fractais.
    
    Características:
    - Balanceamento baseado em consciência
    - Adaptação automática às condições
    - Múltiplas estratégias de balanceamento
    - Monitoramento em tempo real
    - Auto-otimização contínua
    """
    
    def __init__(self):
        self.fractal_metrics: Dict[str, FractalLoadMetrics] = {}
        self.load_history: Dict[str, deque] = {}
        self.balancing_rules: List[LoadBalancingRule] = []
        self._lock = threading.RLock()
        self.stats = {
            'total_requests': 0,
            'successful_balances': 0,
            'failed_balances': 0,
            'consciousness_level': Decimal('0.1'),
            'average_response_time': Decimal('0.0'),
            'load_distribution_variance': Decimal('0.0')
        }
        
        self._initialize_default_rules()
        logger.info("FractalLoadBalancer inicializado")
    
    def _initialize_default_rules(self):
        """Inicializa regras padrão de balanceamento."""
        self.balancing_rules = [
            LoadBalancingRule(
                name="Consciousness Priority",
                priority=1,
                condition="consciousness_level > 0.8",
                action="increase_weight",
                weight=Decimal('1.5')
            ),
            LoadBalancingRule(
                name="Load Threshold",
                priority=2,
                condition="load_score > 0.8",
                action="decrease_weight",
                weight=Decimal('0.5')
            ),
            LoadBalancingRule(
                name="Error Rate",
                priority=3,
                condition="error_rate > 0.1",
                action="temporary_exclude",
                weight=Decimal('0.0')
            ),
            LoadBalancingRule(
                name="Latency Optimization",
                priority=4,
                condition="latency < 100",
                action="increase_weight",
                weight=Decimal('1.2')
            ),
            LoadBalancingRule(
                name="Capacity Utilization",
                priority=5,
                condition="capacity_score > 0.7",
                action="increase_weight",
                weight=Decimal('1.3')
            )
        ]
    
    def register_fractal(self, fractal_id: str, initial_capacity: Decimal = Decimal('1.0')):
        """Registra um fractal no sistema de balanceamento."""
        with self._lock:
            self.fractal_metrics[fractal_id] = FractalLoadMetrics(
                fractal_id=fractal_id,
                capacity=initial_capacity
            )
            self.load_history[fractal_id] = deque(maxlen=100)
            logger.info(f"Fractal {fractal_id} registrado no load balancer")
    
    def update_metrics(self, fractal_id: str, metrics: Dict[str, Any]):
        """Atualiza métricas de um fractal."""
        try:
            with self._lock:
                if fractal_id not in self.fractal_metrics:
                    self.register_fractal(fractal_id)
                
                fractal_metrics = self.fractal_metrics[fractal_id]
                
                # Atualizar métricas
                if 'cpu_usage' in metrics:
                    fractal_metrics.cpu_usage = Decimal(str(metrics['cpu_usage']))
                if 'memory_usage' in metrics:
                    fractal_metrics.memory_usage = Decimal(str(metrics['memory_usage']))
                if 'network_latency' in metrics:
                    fractal_metrics.network_latency = Decimal(str(metrics['network_latency']))
                if 'request_count' in metrics:
                    fractal_metrics.request_count = metrics['request_count']
                if 'error_count' in metrics:
                    fractal_metrics.error_count = metrics['error_count']
                if 'response_time' in metrics:
                    fractal_metrics.response_time = Decimal(str(metrics['response_time']))
                if 'consciousness_level' in metrics:
                    fractal_metrics.consciousness_level = Decimal(str(metrics['consciousness_level']))
                
                fractal_metrics.last_update = time.time()
                
                # Adicionar ao histórico
                load_score = fractal_metrics.get_load_score()
                self.load_history[fractal_id].append({
                    'timestamp': time.time(),
                    'load_score': float(load_score),
                    'capacity_score': float(fractal_metrics.get_capacity_score())
                })
                
                logger.debug(f"Métricas atualizadas para fractal {fractal_id}: carga={load_score:.3f}")
                
        except Exception as e:
            logger.error(f"Erro ao atualizar métricas do fractal {fractal_id}: {e}")
    
    def select_fractal(self, request_type: str = "default") -> Optional[str]:
        """
        Seleciona o melhor fractal para processar uma requisição.
        
        Args:
            request_type: Tipo da requisição (default, cpu_intensive, memory_intensive, etc.)
            
        Returns:
            ID do fractal selecionado ou None se nenhum disponível
        """
        try:
            with self._lock:
                if not self.fractal_metrics:
                    return None
                
                # Filtrar fractais disponíveis
                available_fractals = self._get_available_fractals()
                if not available_fractals:
                    return None
                
                # Aplicar estratégia de seleção baseada no tipo de requisição
                if request_type == "cpu_intensive":
                    selected = self._select_cpu_optimized(available_fractals)
                elif request_type == "memory_intensive":
                    selected = self._select_memory_optimized(available_fractals)
                elif request_type == "latency_critical":
                    selected = self._select_latency_optimized(available_fractals)
                else:
                    selected = self._select_balanced(available_fractals)
                
                if selected:
                    self.stats['total_requests'] += 1
                    self.stats['successful_balances'] += 1
                    
                    # Atualizar consciência do sistema
                    self._update_system_consciousness()
                    
                    logger.debug(f"Fractal selecionado: {selected} para requisição {request_type}")
                
                return selected
                
        except Exception as e:
            logger.error(f"Erro na seleção de fractal: {e}")
            self.stats['failed_balances'] += 1
            return None
    
    def _get_available_fractals(self) -> List[str]:
        """Retorna lista de fractais disponíveis."""
        available = []
        current_time = time.time()
        
        for fractal_id, metrics in self.fractal_metrics.items():
            # Verificar se fractal está ativo (atualizado nos últimos 30 segundos)
            if current_time - metrics.last_update < 30:
                # Verificar se não está sobrecarregado
                if metrics.get_load_score() < Decimal('0.9'):
                    # Verificar taxa de erro
                    error_rate = Decimal(metrics.error_count) / max(Decimal(metrics.request_count), Decimal('1'))
                    if error_rate < Decimal('0.2'):  # Menos de 20% de erro
                        available.append(fractal_id)
        
        return available
    
    def _select_balanced(self, available_fractals: List[str]) -> Optional[str]:
        """Seleção balanceada considerando múltiplos fatores."""
        if not available_fractals:
            return None
        
        scores = {}
        for fractal_id in available_fractals:
            metrics = self.fractal_metrics[fractal_id]
            
            # Calcular score composto
            capacity_score = metrics.get_capacity_score()
            consciousness_score = metrics.consciousness_level
            load_score = Decimal('1.0') - metrics.get_load_score()  # Inverter carga
            
            # Aplicar regras de balanceamento
            weight = self._apply_balancing_rules(fractal_id, metrics)
            
            # Score final = (capacidade * consciência * (1-carga)) * peso
            final_score = (capacity_score * consciousness_score * load_score) * weight
            scores[fractal_id] = final_score
        
        # Selecionar fractal com maior score
        if scores:
            best_fractal = max(scores.keys(), key=lambda x: scores[x])
            return best_fractal
        
        return None
    
    def _select_cpu_optimized(self, available_fractals: List[str]) -> Optional[str]:
        """Seleção otimizada para tarefas intensivas em CPU."""
        scores = {}
        for fractal_id in available_fractals:
            metrics = self.fractal_metrics[fractal_id]
            
            # Priorizar fractais com baixo uso de CPU e alta consciência
            cpu_score = Decimal('1.0') - metrics.cpu_usage
            consciousness_score = metrics.consciousness_level
            
            final_score = cpu_score * consciousness_score
            scores[fractal_id] = final_score
        
        if scores:
            return max(scores.keys(), key=lambda x: scores[x])
        return None
    
    def _select_memory_optimized(self, available_fractals: List[str]) -> Optional[str]:
        """Seleção otimizada para tarefas intensivas em memória."""
        scores = {}
        for fractal_id in available_fractals:
            metrics = self.fractal_metrics[fractal_id]
            
            # Priorizar fractais com baixo uso de memória
            memory_score = Decimal('1.0') - metrics.memory_usage
            consciousness_score = metrics.consciousness_level
            
            final_score = memory_score * consciousness_score
            scores[fractal_id] = final_score
        
        if scores:
            return max(scores.keys(), key=lambda x: scores[x])
        return None
    
    def _select_latency_optimized(self, available_fractals: List[str]) -> Optional[str]:
        """Seleção otimizada para baixa latência."""
        scores = {}
        for fractal_id in available_fractals:
            metrics = self.fractal_metrics[fractal_id]
            
            # Priorizar fractais com baixa latência
            latency_score = Decimal('1.0') - min(metrics.network_latency / Decimal('1000'), Decimal('1.0'))
            consciousness_score = metrics.consciousness_level
            
            final_score = latency_score * consciousness_score
            scores[fractal_id] = final_score
        
        if scores:
            return max(scores.keys(), key=lambda x: scores[x])
        return None
    
    def _apply_balancing_rules(self, fractal_id: str, metrics: FractalLoadMetrics) -> Decimal:
        """Aplica regras de balanceamento a um fractal."""
        weight = Decimal('1.0')
        
        for rule in sorted(self.balancing_rules, key=lambda x: x.priority):
            if not rule.enabled:
                continue
            
            try:
                # Avaliar condição da regra
                if self._evaluate_condition(rule.condition, metrics):
                    if rule.action == "increase_weight":
                        weight *= rule.weight
                    elif rule.action == "decrease_weight":
                        weight *= rule.weight
                    elif rule.action == "temporary_exclude":
                        weight = Decimal('0.0')
                        break
                    
                    logger.debug(f"Regra '{rule.name}' aplicada ao fractal {fractal_id}")
                    
            except Exception as e:
                logger.error(f"Erro ao aplicar regra {rule.name}: {e}")
        
        return weight
    
    def _evaluate_condition(self, condition: str, metrics: FractalLoadMetrics) -> bool:
        """Avalia condição de uma regra."""
        try:
            # Substituir variáveis na condição
            condition = condition.replace('consciousness_level', str(metrics.consciousness_level))
            condition = condition.replace('load_score', str(metrics.get_load_score()))
            condition = condition.replace('capacity_score', str(metrics.get_capacity_score()))
            condition = condition.replace('error_rate', 
                                       str(Decimal(metrics.error_count) / max(Decimal(metrics.request_count), Decimal('1'))))
            condition = condition.replace('latency', str(metrics.network_latency))
            
            # Avaliar condição
            return eval(condition)
        except:
            return False
    
    def _update_system_consciousness(self):
        """Atualiza consciência do sistema de balanceamento."""
        try:
            # Calcular consciência baseada na eficiência do balanceamento
            if self.stats['total_requests'] > 0:
                success_rate = self.stats['successful_balances'] / self.stats['total_requests']
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + (success_rate * Decimal('0.01'))
                )
        except:
            pass
    
    def get_load_distribution(self) -> Dict[str, Any]:
        """Retorna distribuição de carga entre fractais."""
        with self._lock:
            distribution = {}
            total_load = Decimal('0.0')
            
            for fractal_id, metrics in self.fractal_metrics.items():
                load_score = metrics.get_load_score()
                capacity_score = metrics.get_capacity_score()
                
                distribution[fractal_id] = {
                    'load_score': float(load_score),
                    'capacity_score': float(capacity_score),
                    'consciousness_level': float(metrics.consciousness_level),
                    'request_count': metrics.request_count,
                    'error_count': metrics.error_count,
                    'last_update': metrics.last_update
                }
                
                total_load += load_score
            
            # Calcular variância da distribuição
            if len(self.fractal_metrics) > 1:
                load_scores = [float(metrics.get_load_score()) for metrics in self.fractal_metrics.values()]
                self.stats['load_distribution_variance'] = Decimal(str(statistics.variance(load_scores)))
            
            return {
                'fractal_distribution': distribution,
                'total_load': float(total_load),
                'average_load': float(total_load / len(self.fractal_metrics)) if self.fractal_metrics else 0.0,
                'load_variance': float(self.stats['load_distribution_variance']),
                'consciousness_level': float(self.stats['consciousness_level'])
            }
    
    def optimize_balancing(self) -> Dict[str, Any]:
        """
        Otimiza o sistema de balanceamento.
        
        Returns:
            Estatísticas da otimização
        """
        try:
            with self._lock:
                optimization_stats = {
                    'rules_evaluated': len(self.balancing_rules),
                    'rules_optimized': 0,
                    'consciousness_improvement': Decimal('0.0'),
                    'timestamp': time.time()
                }
                
                # Otimizar regras baseado no histórico
                for rule in self.balancing_rules:
                    if self._should_optimize_rule(rule):
                        self._optimize_rule(rule)
                        optimization_stats['rules_optimized'] += 1
                
                # Aumentar consciência com otimização
                old_consciousness = self.stats['consciousness_level']
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.05')
                )
                optimization_stats['consciousness_improvement'] = (
                    self.stats['consciousness_level'] - old_consciousness
                )
                
                logger.info(f"Balanceamento otimizado: {optimization_stats['rules_optimized']} regras")
                return optimization_stats
                
        except Exception as e:
            logger.error(f"Erro na otimização do balanceamento: {e}")
            return {'error': str(e)}
    
    def _should_optimize_rule(self, rule: LoadBalancingRule) -> bool:
        """Determina se uma regra deve ser otimizada."""
        # Lógica simples: otimizar regras com baixa prioridade
        return rule.priority > 3
    
    def _optimize_rule(self, rule: LoadBalancingRule):
        """Otimiza uma regra específica."""
        # Ajustar peso baseado na eficiência
        if rule.weight < Decimal('1.0'):
            rule.weight = min(Decimal('2.0'), rule.weight * Decimal('1.1'))
        else:
            rule.weight = max(Decimal('0.5'), rule.weight * Decimal('0.9'))
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do sistema de balanceamento."""
        with self._lock:
            return {
                'total_requests': self.stats['total_requests'],
                'successful_balances': self.stats['successful_balances'],
                'failed_balances': self.stats['failed_balances'],
                'success_rate': (
                    self.stats['successful_balances'] / max(self.stats['total_requests'], 1)
                ),
                'consciousness_level': float(self.stats['consciousness_level']),
                'average_response_time': float(self.stats['average_response_time']),
                'load_distribution_variance': float(self.stats['load_distribution_variance']),
                'active_fractals': len(self.fractal_metrics),
                'balancing_rules': len(self.balancing_rules)
            }


# Instância global do load balancer
fractal_load_balancer = FractalLoadBalancer()
