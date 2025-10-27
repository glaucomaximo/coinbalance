"""
Sistema de Predição de Falhas Proativa.

Este módulo implementa um sistema inteligente que:
- Prediz falhas antes que ocorram
- Usa análise de padrões e tendências
- Aplica machine learning para detecção
- Implementa alertas preventivos
- Otimiza recursos baseado em predições
"""

import numpy as np
import threading
import time
import json
from typing import Dict, Any, Optional, List, Tuple, Union
from decimal import Decimal
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import logging
import statistics
import math

logger = logging.getLogger(__name__)


class FailureType(Enum):
    """Tipos de falhas que podem ser preditas."""
    SYSTEM_OVERLOAD = "system_overload"
    MEMORY_EXHAUSTION = "memory_exhaustion"
    NETWORK_FAILURE = "network_failure"
    FRACTAL_DEGRADATION = "fractal_degradation"
    DATA_CORRUPTION = "data_corruption"
    SECURITY_BREACH = "security_breach"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    RESOURCE_EXHAUSTION = "resource_exhaustion"


class PredictionConfidence(Enum):
    """Níveis de confiança da predição."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class FailurePrediction:
    """Predição de falha."""
    prediction_id: str
    failure_type: FailureType
    predicted_time: float
    confidence: PredictionConfidence
    probability: float
    affected_fractals: List[str]
    severity: int  # 1-10
    description: str
    recommended_actions: List[str]
    consciousness_level: Decimal = Decimal('0.5')
    timestamp: float = field(default_factory=time.time)
    
    def is_critical(self) -> bool:
        """Verifica se a predição é crítica."""
        return self.severity >= 8 or self.confidence == PredictionConfidence.CRITICAL


@dataclass
class SystemMetric:
    """Métrica do sistema para análise."""
    metric_name: str
    value: float
    timestamp: float
    fractal_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FailurePattern:
    """Padrão de falha identificado."""
    pattern_id: str
    failure_type: FailureType
    metric_patterns: Dict[str, List[float]]
    time_window: float  # Janela de tempo em segundos
    threshold_values: Dict[str, float]
    consciousness_level: Decimal = Decimal('0.5')
    accuracy: float = 0.0
    occurrences: int = 0


class ProactiveFailurePredictor:
    """
    Sistema de Predição de Falhas Proativa.
    
    Características:
    - Análise de padrões em tempo real
    - Machine learning para predição
    - Alertas preventivos inteligentes
    - Otimização baseada em predições
    - Consciência adaptativa
    """
    
    def __init__(self):
        self.metric_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.failure_patterns: Dict[str, FailurePattern] = {}
        self.active_predictions: Dict[str, FailurePrediction] = {}
        self.prediction_history: deque = deque(maxlen=500)
        self.fractal_metrics: Dict[str, Dict[str, deque]] = defaultdict(lambda: defaultdict(lambda: deque(maxlen=100)))
        self._lock = threading.RLock()
        
        self.stats = {
            'total_predictions': 0,
            'accurate_predictions': 0,
            'false_positives': 0,
            'false_negatives': 0,
            'consciousness_level': Decimal('0.1'),
            'prediction_accuracy': 0.0,
            'patterns_learned': 0,
            'failures_prevented': 0
        }
        
        self._initialize_default_patterns()
        logger.info("ProactiveFailurePredictor inicializado")
    
    def _initialize_default_patterns(self):
        """Inicializa padrões de falha padrão."""
        # Padrão de sobrecarga do sistema
        self.failure_patterns['system_overload'] = FailurePattern(
            pattern_id='system_overload',
            failure_type=FailureType.SYSTEM_OVERLOAD,
            metric_patterns={
                'cpu_usage': [0.7, 0.8, 0.9],
                'memory_usage': [0.6, 0.7, 0.8],
                'response_time': [100, 200, 500]
            },
            time_window=300,  # 5 minutos
            threshold_values={
                'cpu_usage': 0.85,
                'memory_usage': 0.80,
                'response_time': 300
            },
            consciousness_level=Decimal('0.6'),
            accuracy=0.85
        )
        
        # Padrão de esgotamento de memória
        self.failure_patterns['memory_exhaustion'] = FailurePattern(
            pattern_id='memory_exhaustion',
            failure_type=FailureType.MEMORY_EXHAUSTION,
            metric_patterns={
                'memory_usage': [0.5, 0.6, 0.7, 0.8],
                'memory_growth_rate': [0.01, 0.02, 0.05],
                'garbage_collection_frequency': [10, 20, 50]
            },
            time_window=600,  # 10 minutos
            threshold_values={
                'memory_usage': 0.90,
                'memory_growth_rate': 0.03,
                'garbage_collection_frequency': 30
            },
            consciousness_level=Decimal('0.7'),
            accuracy=0.90
        )
        
        # Padrão de degradação de performance
        self.failure_patterns['performance_degradation'] = FailurePattern(
            pattern_id='performance_degradation',
            failure_type=FailureType.PERFORMANCE_DEGRADATION,
            metric_patterns={
                'response_time': [50, 100, 200, 400],
                'throughput': [1000, 800, 600, 400],
                'error_rate': [0.01, 0.02, 0.05]
            },
            time_window=180,  # 3 minutos
            threshold_values={
                'response_time': 500,
                'throughput': 300,
                'error_rate': 0.10
            },
            consciousness_level=Decimal('0.8'),
            accuracy=0.75
        )
    
    def add_metric(self, metric: SystemMetric):
        """Adiciona métrica para análise."""
        try:
            with self._lock:
                # Adicionar ao histórico geral
                self.metric_history[metric.metric_name].append(metric)
                
                # Adicionar ao histórico do fractal se especificado
                if metric.fractal_id:
                    self.fractal_metrics[metric.fractal_id][metric.metric_name].append(metric)
                
                # Verificar padrões de falha
                self._check_failure_patterns(metric)
                
                logger.debug(f"Métrica adicionada: {metric.metric_name} = {metric.value}")
                
        except Exception as e:
            logger.error(f"Erro ao adicionar métrica: {e}")
    
    def _check_failure_patterns(self, metric: SystemMetric):
        """Verifica padrões de falha baseado na métrica."""
        try:
            for pattern_id, pattern in self.failure_patterns.items():
                if metric.metric_name in pattern.metric_patterns:
                    # Verificar se métrica está seguindo padrão de falha
                    if self._is_following_failure_pattern(metric, pattern):
                        # Gerar predição de falha
                        prediction = self._generate_failure_prediction(metric, pattern)
                        if prediction:
                            self._register_prediction(prediction)
                
        except Exception as e:
            logger.error(f"Erro na verificação de padrões: {e}")
    
    def _is_following_failure_pattern(self, metric: SystemMetric, pattern: FailurePattern) -> bool:
        """Verifica se métrica está seguindo padrão de falha."""
        try:
            metric_history = self.metric_history[metric.metric_name]
            
            if len(metric_history) < 3:
                return False
            
            # Obter valores recentes dentro da janela de tempo
            current_time = time.time()
            recent_values = [
                m.value for m in metric_history
                if current_time - m.timestamp <= pattern.time_window
            ]
            
            if len(recent_values) < 3:
                return False
            
            # Verificar tendência crescente (para métricas de carga)
            if metric.metric_name in ['cpu_usage', 'memory_usage', 'response_time', 'error_rate']:
                # Calcular tendência
                if len(recent_values) >= 3:
                    trend = self._calculate_trend(recent_values)
                    threshold = pattern.threshold_values.get(metric.metric_name, 0.8)
                    
                    # Verificar se está se aproximando do threshold
                    if trend > 0 and recent_values[-1] > threshold * 0.7:
                        return True
            
            # Verificar padrão específico de crescimento exponencial
            if self._detect_exponential_growth(recent_values):
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erro na verificação de padrão: {e}")
            return False
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calcula tendência dos valores."""
        try:
            if len(values) < 2:
                return 0.0
            
            # Usar regressão linear simples
            x = np.arange(len(values))
            y = np.array(values)
            
            # Calcular coeficiente angular
            n = len(values)
            sum_x = np.sum(x)
            sum_y = np.sum(y)
            sum_xy = np.sum(x * y)
            sum_x2 = np.sum(x * x)
            
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            return slope
            
        except:
            return 0.0
    
    def _detect_exponential_growth(self, values: List[float]) -> bool:
        """Detecta crescimento exponencial."""
        try:
            if len(values) < 4:
                return False
            
            # Verificar se valores estão crescendo exponencialmente
            growth_rates = []
            for i in range(1, len(values)):
                if values[i-1] > 0:
                    growth_rate = (values[i] - values[i-1]) / values[i-1]
                    growth_rates.append(growth_rate)
            
            if len(growth_rates) < 2:
                return False
            
            # Verificar se taxa de crescimento está aumentando
            avg_growth_rate = statistics.mean(growth_rates)
            if avg_growth_rate > 0.1:  # Crescimento de pelo menos 10%
                return True
            
            return False
            
        except:
            return False
    
    def _generate_failure_prediction(self, metric: SystemMetric, pattern: FailurePattern) -> Optional[FailurePrediction]:
        """Gera predição de falha baseada no padrão."""
        try:
            # Calcular probabilidade baseada na métrica e padrão
            probability = self._calculate_failure_probability(metric, pattern)
            
            if probability < 0.3:  # Muito baixa probabilidade
                return None
            
            # Determinar confiança
            confidence = self._determine_confidence(probability, pattern)
            
            # Calcular tempo previsto para falha
            predicted_time = self._predict_failure_time(metric, pattern)
            
            # Determinar severidade
            severity = self._calculate_severity(probability, pattern)
            
            # Identificar fractais afetados
            affected_fractals = self._identify_affected_fractals(metric, pattern)
            
            # Gerar ações recomendadas
            recommended_actions = self._generate_recommended_actions(pattern, severity)
            
            prediction_id = f"pred_{int(time.time() * 1000)}"
            
            prediction = FailurePrediction(
                prediction_id=prediction_id,
                failure_type=pattern.failure_type,
                predicted_time=predicted_time,
                confidence=confidence,
                probability=probability,
                affected_fractals=affected_fractals,
                severity=severity,
                description=f"Predição de {pattern.failure_type.value} baseada em {metric.metric_name}",
                recommended_actions=recommended_actions,
                consciousness_level=self.stats['consciousness_level']
            )
            
            return prediction
            
        except Exception as e:
            logger.error(f"Erro na geração de predição: {e}")
            return None
    
    def _calculate_failure_probability(self, metric: SystemMetric, pattern: FailurePattern) -> float:
        """Calcula probabilidade de falha."""
        try:
            threshold = pattern.threshold_values.get(metric.metric_name, 0.8)
            current_value = metric.value
            
            # Probabilidade baseada na proximidade do threshold
            if current_value >= threshold:
                base_probability = 0.9
            else:
                base_probability = current_value / threshold
            
            # Ajustar pela consciência do padrão
            consciousness_factor = float(pattern.consciousness_level)
            accuracy_factor = pattern.accuracy
            
            # Calcular tendência
            metric_history = self.metric_history[metric.metric_name]
            if len(metric_history) >= 3:
                recent_values = [m.value for m in list(metric_history)[-3:]]
                trend = self._calculate_trend(recent_values)
                
                # Ajustar probabilidade pela tendência
                if trend > 0:
                    trend_factor = min(trend * 10, 1.0)  # Normalizar tendência
                    base_probability += trend_factor * 0.2
            
            # Aplicar fatores de ajuste
            final_probability = base_probability * consciousness_factor * accuracy_factor
            
            return min(final_probability, 1.0)
            
        except:
            return 0.0
    
    def _determine_confidence(self, probability: float, pattern: FailurePattern) -> PredictionConfidence:
        """Determina nível de confiança da predição."""
        if probability >= 0.9:
            return PredictionConfidence.CRITICAL
        elif probability >= 0.7:
            return PredictionConfidence.HIGH
        elif probability >= 0.5:
            return PredictionConfidence.MEDIUM
        else:
            return PredictionConfidence.LOW
    
    def _predict_failure_time(self, metric: SystemMetric, pattern: FailurePattern) -> float:
        """Prediz tempo até a falha."""
        try:
            threshold = pattern.threshold_values.get(metric.metric_name, 0.8)
            current_value = metric.value
            
            if current_value >= threshold:
                return time.time() + 60  # Falha iminente (1 minuto)
            
            # Calcular tendência
            metric_history = self.metric_history[metric.metric_name]
            if len(metric_history) >= 3:
                recent_values = [m.value for m in list(metric_history)[-3:]]
                trend = self._calculate_trend(recent_values)
                
                if trend > 0:
                    # Calcular tempo baseado na tendência
                    time_to_threshold = (threshold - current_value) / trend
                    return time.time() + max(time_to_threshold, 60)  # Mínimo 1 minuto
            
            # Fallback: tempo baseado no padrão
            return time.time() + pattern.time_window
            
        except:
            return time.time() + 300  # 5 minutos como fallback
    
    def _calculate_severity(self, probability: float, pattern: FailurePattern) -> int:
        """Calcula severidade da falha predita."""
        # Severidade baseada na probabilidade e tipo de falha
        base_severity = int(probability * 10)
        
        # Ajustar pelo tipo de falha
        severity_adjustments = {
            FailureType.SYSTEM_OVERLOAD: 2,
            FailureType.MEMORY_EXHAUSTION: 3,
            FailureType.NETWORK_FAILURE: 2,
            FailureType.FRACTAL_DEGRADATION: 1,
            FailureType.DATA_CORRUPTION: 4,
            FailureType.SECURITY_BREACH: 5,
            FailureType.PERFORMANCE_DEGRADATION: 1,
            FailureType.RESOURCE_EXHAUSTION: 3
        }
        
        adjustment = severity_adjustments.get(pattern.failure_type, 0)
        final_severity = min(base_severity + adjustment, 10)
        
        return max(final_severity, 1)
    
    def _identify_affected_fractals(self, metric: SystemMetric, pattern: FailurePattern) -> List[str]:
        """Identifica fractais que podem ser afetados."""
        try:
            affected_fractals = []
            
            if metric.fractal_id:
                affected_fractals.append(metric.fractal_id)
            
            # Se é uma métrica global, identificar fractais com métricas similares
            if metric.metric_name in ['cpu_usage', 'memory_usage', 'response_time']:
                for fractal_id, fractal_metrics in self.fractal_metrics.items():
                    if metric.metric_name in fractal_metrics:
                        fractal_values = list(fractal_metrics[metric.metric_name])
                        if fractal_values:
                            last_value = fractal_values[-1].value
                            threshold = pattern.threshold_values.get(metric.metric_name, 0.8)
                            
                            if last_value > threshold * 0.6:  # Próximo do threshold
                                affected_fractals.append(fractal_id)
            
            return list(set(affected_fractals))  # Remover duplicatas
            
        except Exception as e:
            logger.error(f"Erro na identificação de fractais afetados: {e}")
            return []
    
    def _generate_recommended_actions(self, pattern: FailurePattern, severity: int) -> List[str]:
        """Gera ações recomendadas baseadas no padrão e severidade."""
        actions = []
        
        if pattern.failure_type == FailureType.SYSTEM_OVERLOAD:
            actions.extend([
                "Escalar fractais automaticamente",
                "Redistribuir carga entre fractais",
                "Ativar cache inteligente",
                "Otimizar algoritmos de processamento"
            ])
        
        elif pattern.failure_type == FailureType.MEMORY_EXHAUSTION:
            actions.extend([
                "Executar garbage collection",
                "Comprimir dados em memória",
                "Liberar cache não utilizado",
                "Redistribuir memória entre fractais"
            ])
        
        elif pattern.failure_type == FailureType.PERFORMANCE_DEGRADATION:
            actions.extend([
                "Otimizar queries de banco de dados",
                "Ativar compressão de dados",
                "Balancear carga automaticamente",
                "Monitorar métricas de performance"
            ])
        
        elif pattern.failure_type == FailureType.NETWORK_FAILURE:
            actions.extend([
                "Ativar replicação de dados",
                "Usar cache local",
                "Implementar fallback de conectividade",
                "Monitorar latência de rede"
            ])
        
        # Ajustar ações pela severidade
        if severity >= 8:
            actions.insert(0, "AÇÃO CRÍTICA: Implementar medidas de emergência")
        elif severity >= 6:
            actions.insert(0, "AÇÃO URGENTE: Implementar medidas preventivas")
        
        return actions
    
    def _register_prediction(self, prediction: FailurePrediction):
        """Registra predição de falha."""
        try:
            with self._lock:
                self.active_predictions[prediction.prediction_id] = prediction
                self.prediction_history.append(prediction)
                self.stats['total_predictions'] += 1
                
                # Log da predição
                logger.warning(f"PREDIÇÃO DE FALHA: {prediction.failure_type.value} "
                             f"(Probabilidade: {prediction.probability:.2%}, "
                             f"Severidade: {prediction.severity}/10)")
                
                # Se for crítica, log de alerta
                if prediction.is_critical():
                    logger.critical(f"ALERTA CRÍTICO: Falha iminente detectada! "
                                 f"Ações recomendadas: {prediction.recommended_actions}")
                
        except Exception as e:
            logger.error(f"Erro no registro de predição: {e}")
    
    def validate_prediction(self, prediction_id: str, actual_failure: bool, 
                           actual_time: Optional[float] = None) -> bool:
        """Valida predição de falha."""
        try:
            with self._lock:
                if prediction_id not in self.active_predictions:
                    return False
                
                prediction = self.active_predictions[prediction_id]
                
                # Calcular precisão temporal se disponível
                time_accuracy = 1.0
                if actual_time:
                    time_diff = abs(actual_time - prediction.predicted_time)
                    time_accuracy = max(0.0, 1.0 - (time_diff / 3600))  # Normalizar para 1 hora
                
                # Atualizar estatísticas
                if actual_failure:
                    self.stats['accurate_predictions'] += 1
                    self.stats['failures_prevented'] += 1
                    
                    # Aumentar consciência do padrão
                    pattern_id = f"{prediction.failure_type.value}"
                    if pattern_id in self.failure_patterns:
                        pattern = self.failure_patterns[pattern_id]
                        pattern.consciousness_level = min(
                            Decimal('1.0'),
                            pattern.consciousness_level + Decimal('0.05')
                        )
                        pattern.accuracy = min(1.0, pattern.accuracy + 0.01)
                        pattern.occurrences += 1
                    
                    logger.info(f"Predição validada: {prediction_id} (Precisão temporal: {time_accuracy:.2%})")
                else:
                    self.stats['false_positives'] += 1
                    logger.warning(f"Falso positivo: {prediction_id}")
                
                # Remover predição ativa
                del self.active_predictions[prediction_id]
                
                # Atualizar precisão geral
                self._update_prediction_accuracy()
                
                return True
                
        except Exception as e:
            logger.error(f"Erro na validação de predição: {e}")
            return False
    
    def _update_prediction_accuracy(self):
        """Atualiza precisão geral das predições."""
        try:
            total_predictions = self.stats['total_predictions']
            if total_predictions > 0:
                accurate_predictions = self.stats['accurate_predictions']
                self.stats['prediction_accuracy'] = accurate_predictions / total_predictions
                
                # Aumentar consciência geral baseada na precisão
                if self.stats['prediction_accuracy'] > 0.8:
                    self.stats['consciousness_level'] = min(
                        Decimal('1.0'),
                        self.stats['consciousness_level'] + Decimal('0.01')
                    )
                
        except Exception as e:
            logger.error(f"Erro na atualização de precisão: {e}")
    
    def get_active_predictions(self) -> List[FailurePrediction]:
        """Retorna predições ativas."""
        with self._lock:
            return list(self.active_predictions.values())
    
    def get_prediction_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de predição."""
        with self._lock:
            # Estatísticas por tipo de falha
            failure_type_stats = {}
            for failure_type in FailureType:
                predictions_of_type = [
                    p for p in self.prediction_history
                    if p.failure_type == failure_type
                ]
                
                if predictions_of_type:
                    avg_probability = sum(p.probability for p in predictions_of_type) / len(predictions_of_type)
                    avg_severity = sum(p.severity for p in predictions_of_type) / len(predictions_of_type)
                    
                    failure_type_stats[failure_type.value] = {
                        'count': len(predictions_of_type),
                        'average_probability': avg_probability,
                        'average_severity': avg_severity,
                        'critical_predictions': sum(1 for p in predictions_of_type if p.is_critical())
                    }
            
            return {
                'total_predictions': self.stats['total_predictions'],
                'active_predictions': len(self.active_predictions),
                'accurate_predictions': self.stats['accurate_predictions'],
                'false_positives': self.stats['false_positives'],
                'prediction_accuracy': self.stats['prediction_accuracy'],
                'consciousness_level': float(self.stats['consciousness_level']),
                'patterns_learned': self.stats['patterns_learned'],
                'failures_prevented': self.stats['failures_prevented'],
                'failure_types': failure_type_stats,
                'patterns': {
                    pattern_id: {
                        'accuracy': pattern.accuracy,
                        'consciousness_level': float(pattern.consciousness_level),
                        'occurrences': pattern.occurrences,
                        'time_window': pattern.time_window
                    }
                    for pattern_id, pattern in self.failure_patterns.items()
                }
            }
    
    def learn_new_pattern(self, failure_type: FailureType, metric_patterns: Dict[str, List[float]],
                         threshold_values: Dict[str, float], time_window: float) -> str:
        """Aprende novo padrão de falha."""
        try:
            with self._lock:
                pattern_id = f"{failure_type.value}_{int(time.time() * 1000)}"
                
                pattern = FailurePattern(
                    pattern_id=pattern_id,
                    failure_type=failure_type,
                    metric_patterns=metric_patterns,
                    time_window=time_window,
                    threshold_values=threshold_values,
                    consciousness_level=self.stats['consciousness_level'],
                    accuracy=0.5  # Iniciar com precisão moderada
                )
                
                self.failure_patterns[pattern_id] = pattern
                self.stats['patterns_learned'] += 1
                
                logger.info(f"Novo padrão de falha aprendido: {pattern_id}")
                return pattern_id
                
        except Exception as e:
            logger.error(f"Erro no aprendizado de padrão: {e}")
            return ""
    
    def optimize_predictions(self) -> Dict[str, Any]:
        """Otimiza sistema de predições."""
        try:
            with self._lock:
                optimization_stats = {
                    'patterns_optimized': 0,
                    'predictions_cleaned': 0,
                    'consciousness_improvement': Decimal('0.0'),
                    'timestamp': time.time()
                }
                
                # Otimizar padrões com baixa precisão
                patterns_to_remove = []
                for pattern_id, pattern in self.failure_patterns.items():
                    if pattern.accuracy < 0.3 and pattern.occurrences < 3:
                        patterns_to_remove.append(pattern_id)
                    else:
                        # Aumentar consciência de padrões bons
                        if pattern.accuracy > 0.7:
                            pattern.consciousness_level = min(
                                Decimal('1.0'),
                                pattern.consciousness_level + Decimal('0.01')
                            )
                            optimization_stats['patterns_optimized'] += 1
                
                # Remover padrões ruins
                for pattern_id in patterns_to_remove:
                    del self.failure_patterns[pattern_id]
                
                # Limpar predições antigas
                current_time = time.time()
                old_predictions = [
                    pred_id for pred_id, pred in self.active_predictions.items()
                    if current_time - pred.timestamp > 3600  # 1 hora
                ]
                
                for pred_id in old_predictions:
                    del self.active_predictions[pred_id]
                    optimization_stats['predictions_cleaned'] += 1
                
                # Aumentar consciência geral
                old_consciousness = self.stats['consciousness_level']
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.02')
                )
                optimization_stats['consciousness_improvement'] = (
                    self.stats['consciousness_level'] - old_consciousness
                )
                
                logger.info(f"Sistema de predições otimizado: {optimization_stats['patterns_optimized']} padrões")
                return optimization_stats
                
        except Exception as e:
            logger.error(f"Erro na otimização de predições: {e}")
            return {'error': str(e)}


# Instância global do preditor de falhas proativo
proactive_failure_predictor = ProactiveFailurePredictor()
