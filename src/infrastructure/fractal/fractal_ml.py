"""
Sistema de Aprendizado de Máquina entre Fractais.

Este módulo implementa um sistema inteligente de ML distribuído que:
- Permite fractais aprenderem uns com os outros
- Implementa transfer learning entre fractais
- Aplica ensemble learning distribuído
- Usa federated learning consciente
- Otimiza modelos baseado em consciência coletiva
"""

import numpy as np
import threading
import time
import json
import hashlib
from typing import Dict, Any, Optional, List, Tuple, Union
from decimal import Decimal
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import logging
import pickle
import random

logger = logging.getLogger(__name__)


class ModelType(Enum):
    """Tipos de modelos de ML."""
    PREDICTION = "prediction"
    CLASSIFICATION = "classification"
    OPTIMIZATION = "optimization"
    PATTERN_RECOGNITION = "pattern_recognition"
    ANOMALY_DETECTION = "anomaly_detection"
    CONSCIOUSNESS_MODEL = "consciousness_model"


class LearningMethod(Enum):
    """Métodos de aprendizado."""
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised"
    REINFORCEMENT = "reinforcement"
    TRANSFER = "transfer"
    FEDERATED = "federated"
    ENSEMBLE = "ensemble"


@dataclass
class ModelMetrics:
    """Métricas de um modelo de ML."""
    model_id: str
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    loss: float = 0.0
    consciousness_level: Decimal = Decimal('0.5')
    training_samples: int = 0
    last_update: float = field(default_factory=time.time)
    fractal_source: str = ""
    
    def get_performance_score(self) -> float:
        """Calcula score de performance do modelo."""
        return (self.accuracy + self.precision + self.recall + self.f1_score) / 4


@dataclass
class FractalModel:
    """Modelo de ML de um fractal."""
    model_id: str
    fractal_id: str
    model_type: ModelType
    learning_method: LearningMethod
    model_data: bytes
    metrics: ModelMetrics
    features: List[str] = field(default_factory=list)
    target_variable: Optional[str] = None
    training_data_size: int = 0
    is_trained: bool = False
    can_share: bool = True
    
    def get_model_hash(self) -> str:
        """Calcula hash do modelo para identificação."""
        return hashlib.md5(self.model_data).hexdigest()[:16]


@dataclass
class LearningSession:
    """Sessão de aprendizado entre fractais."""
    session_id: str
    participating_fractals: List[str]
    learning_method: LearningMethod
    target_model_type: ModelType
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    shared_data_size: int = 0
    models_exchanged: int = 0
    consciousness_gained: Decimal = Decimal('0.0')
    
    def is_active(self) -> bool:
        """Verifica se a sessão está ativa."""
        return self.end_time is None


class FractalMLSystem:
    """
    Sistema de Aprendizado de Máquina entre Fractais.
    
    Características:
    - Aprendizado distribuído consciente
    - Transfer learning entre fractais
    - Federated learning seguro
    - Ensemble learning coletivo
    - Otimização baseada em consciência
    """
    
    def __init__(self):
        self.fractal_models: Dict[str, FractalModel] = {}
        self.learning_sessions: Dict[str, LearningSession] = {}
        self.shared_knowledge: Dict[str, Any] = {}
        self.model_performance_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self._lock = threading.RLock()
        
        self.stats = {
            'total_models': 0,
            'active_sessions': 0,
            'models_shared': 0,
            'knowledge_transfers': 0,
            'consciousness_level': Decimal('0.1'),
            'average_accuracy': 0.0,
            'collaborative_learning_events': 0
        }
        
        logger.info("FractalMLSystem inicializado")
    
    def register_model(self, fractal_id: str, model_type: ModelType, 
                      learning_method: LearningMethod, model_data: bytes,
                      features: List[str], target_variable: Optional[str] = None) -> str:
        """
        Registra um modelo de ML de um fractal.
        
        Args:
            fractal_id: ID do fractal
            model_type: Tipo do modelo
            learning_method: Método de aprendizado
            model_data: Dados do modelo (serializados)
            features: Lista de features
            target_variable: Variável alvo (se supervisionado)
            
        Returns:
            ID do modelo registrado
        """
        try:
            with self._lock:
                model_id = f"{fractal_id}_{model_type.value}_{int(time.time() * 1000)}"
                
                # Criar métricas iniciais
                metrics = ModelMetrics(
                    model_id=model_id,
                    fractal_source=fractal_id,
                    consciousness_level=Decimal('0.5')
                )
                
                # Criar modelo fractal
                fractal_model = FractalModel(
                    model_id=model_id,
                    fractal_id=fractal_id,
                    model_type=model_type,
                    learning_method=learning_method,
                    model_data=model_data,
                    metrics=metrics,
                    features=features,
                    target_variable=target_variable,
                    training_data_size=0,
                    is_trained=False
                )
                
                # Registrar modelo
                self.fractal_models[model_id] = fractal_model
                self.stats['total_models'] += 1
                
                logger.info(f"Modelo {model_id} registrado para fractal {fractal_id}")
                return model_id
                
        except Exception as e:
            logger.error(f"Erro no registro do modelo: {e}")
            return ""
    
    def train_model(self, model_id: str, training_data: List[Dict[str, Any]], 
                   labels: Optional[List[Any]] = None) -> bool:
        """
        Treina um modelo com dados.
        
        Args:
            model_id: ID do modelo
            training_data: Dados de treinamento
            labels: Labels (se supervisionado)
            
        Returns:
            True se treinamento bem-sucedido
        """
        try:
            with self._lock:
                if model_id not in self.fractal_models:
                    return False
                
                model = self.fractal_models[model_id]
                
                # Simular treinamento (em implementação real, usar bibliotecas ML)
                training_samples = len(training_data)
                
                # Calcular métricas simuladas baseadas no tipo de modelo
                if model.model_type == ModelType.CLASSIFICATION:
                    # Simular métricas de classificação
                    accuracy = random.uniform(0.7, 0.95)
                    precision = random.uniform(0.6, 0.9)
                    recall = random.uniform(0.6, 0.9)
                    f1_score = 2 * (precision * recall) / (precision + recall)
                    loss = random.uniform(0.1, 0.5)
                    
                elif model.model_type == ModelType.PREDICTION:
                    # Simular métricas de predição
                    accuracy = random.uniform(0.6, 0.9)
                    precision = random.uniform(0.5, 0.8)
                    recall = random.uniform(0.5, 0.8)
                    f1_score = 2 * (precision * recall) / (precision + recall)
                    loss = random.uniform(0.2, 0.8)
                    
                elif model.model_type == ModelType.ANOMALY_DETECTION:
                    # Simular métricas de detecção de anomalias
                    accuracy = random.uniform(0.8, 0.98)
                    precision = random.uniform(0.7, 0.95)
                    recall = random.uniform(0.7, 0.95)
                    f1_score = 2 * (precision * recall) / (precision + recall)
                    loss = random.uniform(0.05, 0.3)
                    
                else:
                    # Métricas padrão
                    accuracy = random.uniform(0.5, 0.8)
                    precision = random.uniform(0.4, 0.7)
                    recall = random.uniform(0.4, 0.7)
                    f1_score = 2 * (precision * recall) / (precision + recall)
                    loss = random.uniform(0.3, 0.7)
                
                # Atualizar métricas
                model.metrics.accuracy = accuracy
                model.metrics.precision = precision
                model.metrics.recall = recall
                model.metrics.f1_score = f1_score
                model.metrics.loss = loss
                model.metrics.training_samples = training_samples
                model.metrics.last_update = time.time()
                
                # Aumentar consciência com treinamento
                model.metrics.consciousness_level = min(
                    Decimal('1.0'),
                    model.metrics.consciousness_level + Decimal('0.1')
                )
                
                # Marcar como treinado
                model.is_trained = True
                model.training_data_size = training_samples
                
                # Adicionar ao histórico de performance
                self.model_performance_history[model_id].append({
                    'timestamp': time.time(),
                    'accuracy': accuracy,
                    'loss': loss,
                    'training_samples': training_samples
                })
                
                # Atualizar estatísticas globais
                self._update_global_stats()
                
                logger.info(f"Modelo {model_id} treinado com {training_samples} amostras")
                return True
                
        except Exception as e:
            logger.error(f"Erro no treinamento do modelo {model_id}: {e}")
            return False
    
    def start_collaborative_learning(self, participating_fractals: List[str],
                                   learning_method: LearningMethod,
                                   target_model_type: ModelType) -> str:
        """
        Inicia sessão de aprendizado colaborativo.
        
        Args:
            participating_fractals: Lista de fractais participantes
            learning_method: Método de aprendizado
            target_model_type: Tipo de modelo alvo
            
        Returns:
            ID da sessão de aprendizado
        """
        try:
            with self._lock:
                session_id = f"session_{int(time.time() * 1000)}"
                
                session = LearningSession(
                    session_id=session_id,
                    participating_fractals=participating_fractals,
                    learning_method=learning_method,
                    target_model_type=target_model_type
                )
                
                self.learning_sessions[session_id] = session
                self.stats['active_sessions'] += 1
                
                logger.info(f"Sessão de aprendizado colaborativo iniciada: {session_id}")
                return session_id
                
        except Exception as e:
            logger.error(f"Erro ao iniciar aprendizado colaborativo: {e}")
            return ""
    
    def share_model_knowledge(self, source_model_id: str, target_fractal_id: str) -> bool:
        """
        Compartilha conhecimento de um modelo com outro fractal.
        
        Args:
            source_model_id: ID do modelo fonte
            target_fractal_id: ID do fractal alvo
            
        Returns:
            True se compartilhamento bem-sucedido
        """
        try:
            with self._lock:
                if source_model_id not in self.fractal_models:
                    return False
                
                source_model = self.fractal_models[source_model_id]
                
                # Verificar se modelo pode ser compartilhado
                if not source_model.can_share:
                    return False
                
                # Criar novo modelo para o fractal alvo
                new_model_id = f"{target_fractal_id}_{source_model.model_type.value}_{int(time.time() * 1000)}"
                
                # Criar métricas baseadas no modelo fonte
                new_metrics = ModelMetrics(
                    model_id=new_model_id,
                    accuracy=source_model.metrics.accuracy * 0.9,  # Pequena degradação
                    precision=source_model.metrics.precision * 0.9,
                    recall=source_model.metrics.recall * 0.9,
                    f1_score=source_model.metrics.f1_score * 0.9,
                    loss=source_model.metrics.loss * 1.1,  # Pequeno aumento
                    consciousness_level=source_model.metrics.consciousness_level * Decimal('0.8'),
                    fractal_source=target_fractal_id
                )
                
                # Criar novo modelo fractal
                new_model = FractalModel(
                    model_id=new_model_id,
                    fractal_id=target_fractal_id,
                    model_type=source_model.model_type,
                    learning_method=source_model.learning_method,
                    model_data=source_model.model_data,  # Copiar dados do modelo
                    metrics=new_metrics,
                    features=source_model.features.copy(),
                    target_variable=source_model.target_variable,
                    training_data_size=source_model.training_data_size,
                    is_trained=True,  # Já vem treinado
                    can_share=True
                )
                
                # Registrar novo modelo
                self.fractal_models[new_model_id] = new_model
                
                # Atualizar estatísticas
                self.stats['models_shared'] += 1
                self.stats['knowledge_transfers'] += 1
                
                # Aumentar consciência do sistema
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.01')
                )
                
                logger.info(f"Conhecimento compartilhado: {source_model_id} -> {target_fractal_id}")
                return True
                
        except Exception as e:
            logger.error(f"Erro no compartilhamento de conhecimento: {e}")
            return False
    
    def federated_learning_update(self, session_id: str, fractal_id: str,
                                 model_updates: Dict[str, Any]) -> bool:
        """
        Atualiza modelo usando federated learning.
        
        Args:
            session_id: ID da sessão
            fractal_id: ID do fractal
            model_updates: Atualizações do modelo
            
        Returns:
            True se atualização bem-sucedida
        """
        try:
            with self._lock:
                if session_id not in self.learning_sessions:
                    return False
                
                session = self.learning_sessions[session_id]
                if not session.is_active():
                    return False
                
                # Simular agregação de atualizações federadas
                if 'federated_updates' not in self.shared_knowledge:
                    self.shared_knowledge['federated_updates'] = {}
                
                if session_id not in self.shared_knowledge['federated_updates']:
                    self.shared_knowledge['federated_updates'][session_id] = []
                
                # Adicionar atualização
                update_entry = {
                    'fractal_id': fractal_id,
                    'updates': model_updates,
                    'timestamp': time.time(),
                    'consciousness_level': float(self.stats['consciousness_level'])
                }
                
                self.shared_knowledge['federated_updates'][session_id].append(update_entry)
                
                # Simular agregação quando temos atualizações suficientes
                updates = self.shared_knowledge['federated_updates'][session_id]
                if len(updates) >= len(session.participating_fractals):
                    self._aggregate_federated_updates(session_id)
                
                logger.debug(f"Atualização federada recebida de {fractal_id} para sessão {session_id}")
                return True
                
        except Exception as e:
            logger.error(f"Erro na atualização federada: {e}")
            return False
    
    def _aggregate_federated_updates(self, session_id: str):
        """Agrega atualizações federadas."""
        try:
            session = self.learning_sessions[session_id]
            updates = self.shared_knowledge['federated_updates'][session_id]
            
            # Simular agregação (média ponderada por consciência)
            total_consciousness = sum(update['consciousness_level'] for update in updates)
            
            if total_consciousness > 0:
                # Calcular ganho de consciência
                consciousness_gain = Decimal(str(total_consciousness / len(updates))) * Decimal('0.1')
                session.consciousness_gained += consciousness_gain
                
                # Atualizar consciência do sistema
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + consciousness_gain
                )
                
                # Marcar sessão como concluída
                session.end_time = time.time()
                session.models_exchanged = len(updates)
                session.shared_data_size = sum(
                    len(str(update['updates'])) for update in updates
                )
                
                self.stats['active_sessions'] -= 1
                self.stats['collaborative_learning_events'] += 1
                
                logger.info(f"Sessão federada {session_id} concluída com ganho de consciência "
                           f"{consciousness_gain:.3f}")
                
        except Exception as e:
            logger.error(f"Erro na agregação federada: {e}")
    
    def ensemble_prediction(self, fractal_ids: List[str], model_type: ModelType,
                          input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faz predição usando ensemble de modelos de múltiplos fractais.
        
        Args:
            fractal_ids: Lista de fractais participantes
            model_type: Tipo de modelo
            input_data: Dados de entrada
            
        Returns:
            Resultado da predição ensemble
        """
        try:
            with self._lock:
                # Encontrar modelos relevantes
                relevant_models = []
                for model_id, model in self.fractal_models.items():
                    if (model.fractal_id in fractal_ids and 
                        model.model_type == model_type and 
                        model.is_trained):
                        relevant_models.append(model)
                
                if not relevant_models:
                    return {'error': 'Nenhum modelo relevante encontrado'}
                
                # Simular predições individuais
                predictions = []
                weights = []
                
                for model in relevant_models:
                    # Simular predição baseada na performance do modelo
                    base_prediction = random.uniform(0.0, 1.0)
                    
                    # Ajustar pela consciência do modelo
                    consciousness_factor = float(model.metrics.consciousness_level)
                    adjusted_prediction = base_prediction * consciousness_factor
                    
                    predictions.append(adjusted_prediction)
                    
                    # Peso baseado na performance e consciência
                    weight = model.metrics.get_performance_score() * consciousness_factor
                    weights.append(weight)
                
                # Calcular predição ensemble (média ponderada)
                total_weight = sum(weights)
                if total_weight > 0:
                    ensemble_prediction = sum(
                        pred * weight for pred, weight in zip(predictions, weights)
                    ) / total_weight
                else:
                    ensemble_prediction = sum(predictions) / len(predictions)
                
                # Calcular confiança baseada na concordância
                prediction_variance = np.var(predictions) if len(predictions) > 1 else 0.0
                confidence = 1.0 - min(prediction_variance, 1.0)
                
                result = {
                    'ensemble_prediction': ensemble_prediction,
                    'confidence': confidence,
                    'individual_predictions': predictions,
                    'model_weights': weights,
                    'models_used': len(relevant_models),
                    'consciousness_level': float(self.stats['consciousness_level'])
                }
                
                logger.info(f"Predição ensemble realizada com {len(relevant_models)} modelos")
                return result
                
        except Exception as e:
            logger.error(f"Erro na predição ensemble: {e}")
            return {'error': str(e)}
    
    def transfer_learning(self, source_model_id: str, target_fractal_id: str,
                         target_task_data: List[Dict[str, Any]]) -> str:
        """
        Aplica transfer learning de um modelo para outro fractal.
        
        Args:
            source_model_id: ID do modelo fonte
            target_fractal_id: ID do fractal alvo
            target_task_data: Dados da nova tarefa
            
        Returns:
            ID do novo modelo criado
        """
        try:
            with self._lock:
                if source_model_id not in self.fractal_models:
                    return ""
                
                source_model = self.fractal_models[source_model_id]
                
                # Criar novo modelo baseado no modelo fonte
                new_model_id = f"{target_fractal_id}_transfer_{int(time.time() * 1000)}"
                
                # Métricas iniciais baseadas no modelo fonte
                transfer_metrics = ModelMetrics(
                    model_id=new_model_id,
                    accuracy=source_model.metrics.accuracy * 0.7,  # Degradação inicial
                    precision=source_model.metrics.precision * 0.7,
                    recall=source_model.metrics.recall * 0.7,
                    f1_score=source_model.metrics.f1_score * 0.7,
                    loss=source_model.metrics.loss * 1.5,  # Aumento inicial
                    consciousness_level=source_model.metrics.consciousness_level * Decimal('0.6'),
                    fractal_source=target_fractal_id
                )
                
                # Criar modelo de transfer learning
                transfer_model = FractalModel(
                    model_id=new_model_id,
                    fractal_id=target_fractal_id,
                    model_type=source_model.model_type,
                    learning_method=LearningMethod.TRANSFER,
                    model_data=source_model.model_data,  # Usar dados do modelo fonte
                    metrics=transfer_metrics,
                    features=source_model.features.copy(),
                    target_variable=source_model.target_variable,
                    training_data_size=len(target_task_data),
                    is_trained=False,  # Precisa ser retreinado
                    can_share=True
                )
                
                # Registrar modelo
                self.fractal_models[new_model_id] = transfer_model
                
                # Simular retreinamento com dados da nova tarefa
                if self.train_model(new_model_id, target_task_data):
                    logger.info(f"Transfer learning aplicado: {source_model_id} -> {new_model_id}")
                    return new_model_id
                
                return ""
                
        except Exception as e:
            logger.error(f"Erro no transfer learning: {e}")
            return ""
    
    def _update_global_stats(self):
        """Atualiza estatísticas globais do sistema."""
        try:
            if self.fractal_models:
                # Calcular acurácia média
                accuracies = [model.metrics.accuracy for model in self.fractal_models.values()]
                self.stats['average_accuracy'] = sum(accuracies) / len(accuracies)
                
                # Atualizar consciência baseada na qualidade dos modelos
                high_performance_models = sum(
                    1 for model in self.fractal_models.values()
                    if model.metrics.get_performance_score() > 0.8
                )
                
                if high_performance_models > 0:
                    consciousness_boost = Decimal(str(high_performance_models / len(self.fractal_models))) * Decimal('0.01')
                    self.stats['consciousness_level'] = min(
                        Decimal('1.0'),
                        self.stats['consciousness_level'] + consciousness_boost
                    )
                
        except Exception as e:
            logger.error(f"Erro na atualização de estatísticas globais: {e}")
    
    def get_ml_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do sistema de ML."""
        with self._lock:
            # Estatísticas por tipo de modelo
            model_type_stats = {}
            for model_type in ModelType:
                models_of_type = [
                    model for model in self.fractal_models.values()
                    if model.model_type == model_type
                ]
                
                if models_of_type:
                    avg_accuracy = sum(model.metrics.accuracy for model in models_of_type) / len(models_of_type)
                    avg_consciousness = sum(float(model.metrics.consciousness_level) for model in models_of_type) / len(models_of_type)
                    
                    model_type_stats[model_type.value] = {
                        'count': len(models_of_type),
                        'average_accuracy': avg_accuracy,
                        'average_consciousness': avg_consciousness,
                        'trained_models': sum(1 for model in models_of_type if model.is_trained)
                    }
            
            # Estatísticas por fractal
            fractal_stats = {}
            fractal_models = defaultdict(list)
            for model in self.fractal_models.values():
                fractal_models[model.fractal_id].append(model)
            
            for fractal_id, models in fractal_models.items():
                if models:
                    avg_accuracy = sum(model.metrics.accuracy for model in models) / len(models)
                    avg_consciousness = sum(float(model.metrics.consciousness_level) for model in models) / len(models)
                    
                    fractal_stats[fractal_id] = {
                        'model_count': len(models),
                        'average_accuracy': avg_accuracy,
                        'average_consciousness': avg_consciousness,
                        'trained_models': sum(1 for model in models if model.is_trained),
                        'shareable_models': sum(1 for model in models if model.can_share)
                    }
            
            return {
                'total_models': self.stats['total_models'],
                'active_sessions': self.stats['active_sessions'],
                'models_shared': self.stats['models_shared'],
                'knowledge_transfers': self.stats['knowledge_transfers'],
                'consciousness_level': float(self.stats['consciousness_level']),
                'average_accuracy': self.stats['average_accuracy'],
                'collaborative_learning_events': self.stats['collaborative_learning_events'],
                'model_types': model_type_stats,
                'fractal_stats': fractal_stats,
                'learning_sessions': {
                    'active': sum(1 for session in self.learning_sessions.values() if session.is_active()),
                    'completed': sum(1 for session in self.learning_sessions.values() if not session.is_active()),
                    'total': len(self.learning_sessions)
                }
            }
    
    def optimize_ml_system(self) -> Dict[str, Any]:
        """Otimiza sistema de ML."""
        try:
            with self._lock:
                optimization_stats = {
                    'models_optimized': 0,
                    'knowledge_consolidated': 0,
                    'consciousness_improvement': Decimal('0.0'),
                    'timestamp': time.time()
                }
                
                # Otimizar modelos com baixa performance
                models_to_remove = []
                for model_id, model in self.fractal_models.items():
                    if (model.metrics.get_performance_score() < 0.3 and 
                        model.metrics.consciousness_level < Decimal('0.2')):
                        models_to_remove.append(model_id)
                    else:
                        # Aumentar consciência de modelos bons
                        if model.metrics.get_performance_score() > 0.8:
                            model.metrics.consciousness_level = min(
                                Decimal('1.0'),
                                model.metrics.consciousness_level + Decimal('0.01')
                            )
                            optimization_stats['models_optimized'] += 1
                
                # Remover modelos ruins
                for model_id in models_to_remove:
                    del self.fractal_models[model_id]
                
                # Consolidar conhecimento compartilhado
                if len(self.shared_knowledge) > 100:
                    # Manter apenas conhecimento recente
                    recent_knowledge = {}
                    current_time = time.time()
                    
                    for key, value in self.shared_knowledge.items():
                        if isinstance(value, list) and len(value) > 0:
                            # Manter apenas entradas recentes
                            recent_entries = [
                                entry for entry in value
                                if isinstance(entry, dict) and 
                                current_time - entry.get('timestamp', 0) < 3600  # 1 hora
                            ]
                            if recent_entries:
                                recent_knowledge[key] = recent_entries
                        else:
                            recent_knowledge[key] = value
                    
                    self.shared_knowledge = recent_knowledge
                    optimization_stats['knowledge_consolidated'] = 1
                
                # Aumentar consciência geral
                old_consciousness = self.stats['consciousness_level']
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.02')
                )
                optimization_stats['consciousness_improvement'] = (
                    self.stats['consciousness_level'] - old_consciousness
                )
                
                logger.info(f"Sistema ML otimizado: {optimization_stats['models_optimized']} modelos")
                return optimization_stats
                
        except Exception as e:
            logger.error(f"Erro na otimização do sistema ML: {e}")
            return {'error': str(e)}


# Instância global do sistema de ML fractal
fractal_ml_system = FractalMLSystem()
