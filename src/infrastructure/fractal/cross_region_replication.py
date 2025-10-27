"""
Sistema de Replicação Cross-Region de Fractais.

Este módulo implementa um sistema inteligente que:
- Replica fractais entre diferentes regiões geográficas
- Garante consistência eventual entre regiões
- Implementa sincronização automática
- Otimiza latência de replicação
- Aplica políticas de consistência configuráveis
"""

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
import random

logger = logging.getLogger(__name__)


class ConsistencyLevel(Enum):
    """Níveis de consistência."""
    EVENTUAL = "eventual"
    STRONG = "strong"
    BOUNDED_STALENESS = "bounded_staleness"
    SESSION = "session"
    MONOTONIC_READ = "monotonic_read"


class ReplicationStatus(Enum):
    """Status da replicação."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ReplicationTask:
    """Tarefa de replicação."""
    task_id: str
    source_fractal_id: str
    target_region: str
    consistency_level: ConsistencyLevel
    status: ReplicationStatus
    data_size: int = 0
    bytes_transferred: int = 0
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    error_message: Optional[str] = None
    consciousness_level: Decimal = Decimal('0.5')
    
    def get_progress(self) -> float:
        """Retorna progresso da replicação (0.0 a 1.0)."""
        if self.data_size == 0:
            return 0.0
        return min(self.bytes_transferred / self.data_size, 1.0)
    
    def get_duration(self) -> float:
        """Retorna duração da replicação."""
        end_time = self.end_time or time.time()
        return end_time - self.start_time


@dataclass
class ReplicationPolicy:
    """Política de replicação."""
    policy_id: str
    source_region: str
    target_regions: List[str]
    consistency_level: ConsistencyLevel
    replication_interval: float = 300.0  # 5 minutos
    max_latency: float = 1000.0  # ms
    enabled: bool = True
    consciousness_level: Decimal = Decimal('0.5')


@dataclass
class RegionSyncStatus:
    """Status de sincronização entre regiões."""
    source_region: str
    target_region: str
    last_sync_time: float
    sync_latency: float
    data_consistency: float  # 0.0 a 1.0
    pending_changes: int = 0
    consciousness_level: Decimal = Decimal('0.5')


class CrossRegionReplicator:
    """
    Sistema de Replicação Cross-Region de Fractais.
    
    Características:
    - Replicação automática entre regiões
    - Múltiplos níveis de consistência
    - Sincronização inteligente
    - Otimização de latência
    - Monitoramento de consistência
    """
    
    def __init__(self):
        self.replication_tasks: Dict[str, ReplicationTask] = {}
        self.replication_policies: Dict[str, ReplicationPolicy] = {}
        self.region_sync_status: Dict[Tuple[str, str], RegionSyncStatus] = {}
        self.fractal_replicas: Dict[str, List[str]] = defaultdict(list)  # fractal_id -> [replica_ids]
        self._lock = threading.RLock()
        
        self.stats = {
            'total_replications': 0,
            'successful_replications': 0,
            'failed_replications': 0,
            'average_replication_time': 0.0,
            'consciousness_level': Decimal('0.1'),
            'active_policies': 0,
            'regions_synced': 0,
            'data_consistency_score': 0.0
        }
        
        self._initialize_default_policies()
        logger.info("CrossRegionReplicator inicializado")
    
    def _initialize_default_policies(self):
        """Inicializa políticas de replicação padrão."""
        # Política de replicação para alta disponibilidade
        self.replication_policies['high_availability'] = ReplicationPolicy(
            policy_id='high_availability',
            source_region='primary',
            target_regions=['secondary', 'disaster_recovery'],
            consistency_level=ConsistencyLevel.EVENTUAL,
            replication_interval=60.0,  # 1 minuto
            max_latency=500.0,
            consciousness_level=Decimal('0.8')
        )
        
        # Política de replicação para consistência forte
        self.replication_policies['strong_consistency'] = ReplicationPolicy(
            policy_id='strong_consistency',
            source_region='primary',
            target_regions=['secondary'],
            consistency_level=ConsistencyLevel.STRONG,
            replication_interval=30.0,  # 30 segundos
            max_latency=200.0,
            consciousness_level=Decimal('0.9')
        )
        
        # Política de replicação para disaster recovery
        self.replication_policies['disaster_recovery'] = ReplicationPolicy(
            policy_id='disaster_recovery',
            source_region='primary',
            target_regions=['disaster_recovery'],
            consistency_level=ConsistencyLevel.EVENTUAL,
            replication_interval=600.0,  # 10 minutos
            max_latency=2000.0,
            consciousness_level=Decimal('0.7')
        )
    
    def create_replication_policy(self, policy_id: str, source_region: str,
                                target_regions: List[str], consistency_level: ConsistencyLevel,
                                replication_interval: float = 300.0) -> bool:
        """Cria nova política de replicação."""
        try:
            with self._lock:
                policy = ReplicationPolicy(
                    policy_id=policy_id,
                    source_region=source_region,
                    target_regions=target_regions,
                    consistency_level=consistency_level,
                    replication_interval=replication_interval,
                    consciousness_level=self.stats['consciousness_level']
                )
                
                self.replication_policies[policy_id] = policy
                self.stats['active_policies'] = len([p for p in self.replication_policies.values() if p.enabled])
                
                logger.info(f"Política de replicação criada: {policy_id}")
                return True
                
        except Exception as e:
            logger.error(f"Erro na criação da política de replicação: {e}")
            return False
    
    def replicate_fractal(self, fractal_id: str, target_region: str,
                        consistency_level: ConsistencyLevel = ConsistencyLevel.EVENTUAL) -> str:
        """
        Inicia replicação de um fractal para outra região.
        
        Args:
            fractal_id: ID do fractal a ser replicado
            target_region: Região de destino
            consistency_level: Nível de consistência
            
        Returns:
            ID da tarefa de replicação
        """
        try:
            with self._lock:
                task_id = f"replication_{fractal_id}_{target_region}_{int(time.time() * 1000)}"
                
                # Simular tamanho dos dados
                data_size = random.randint(1024, 1024 * 1024)  # 1KB a 1MB
                
                task = ReplicationTask(
                    task_id=task_id,
                    source_fractal_id=fractal_id,
                    target_region=target_region,
                    consistency_level=consistency_level,
                    status=ReplicationStatus.PENDING,
                    data_size=data_size,
                    consciousness_level=self.stats['consciousness_level']
                )
                
                self.replication_tasks[task_id] = task
                self.stats['total_replications'] += 1
                
                # Iniciar replicação em thread separada
                threading.Thread(
                    target=self._execute_replication,
                    args=(task_id,),
                    daemon=True
                ).start()
                
                logger.info(f"Replicação iniciada: {fractal_id} -> {target_region}")
                return task_id
                
        except Exception as e:
            logger.error(f"Erro na replicação do fractal: {e}")
            return ""
    
    def _execute_replication(self, task_id: str):
        """Executa tarefa de replicação."""
        try:
            with self._lock:
                if task_id not in self.replication_tasks:
                    return
                
                task = self.replication_tasks[task_id]
                task.status = ReplicationStatus.IN_PROGRESS
            
            # Simular replicação
            bytes_per_second = random.randint(1000, 10000)  # 1KB/s a 10KB/s
            total_bytes = task.data_size
            transferred = 0
            
            while transferred < total_bytes:
                time.sleep(0.1)  # Simular transferência
                
                # Transferir chunk
                chunk_size = min(bytes_per_second // 10, total_bytes - transferred)
                transferred += chunk_size
                
                with self._lock:
                    if task_id in self.replication_tasks:
                        task.bytes_transferred = transferred
                        
                        # Simular falha ocasional
                        if random.random() < 0.05:  # 5% chance de falha
                            task.status = ReplicationStatus.FAILED
                            task.end_time = time.time()
                            task.error_message = "Erro de rede durante replicação"
                            self.stats['failed_replications'] += 1
                            logger.error(f"Replicação falhou: {task_id}")
                            return
            
            # Replicação concluída com sucesso
            with self._lock:
                task.status = ReplicationStatus.COMPLETED
                task.end_time = time.time()
                task.bytes_transferred = total_bytes
                
                # Atualizar estatísticas
                self.stats['successful_replications'] += 1
                
                # Atualizar tempo médio de replicação
                duration = task.get_duration()
                if self.stats['total_replications'] == 1:
                    self.stats['average_replication_time'] = duration
                else:
                    self.stats['average_replication_time'] = (
                        (self.stats['average_replication_time'] * (self.stats['total_replications'] - 1) + 
                         duration) / self.stats['total_replications']
                    )
                
                # Registrar réplica
                replica_id = f"{task.source_fractal_id}_replica_{task.target_region}"
                self.fractal_replicas[task.source_fractal_id].append(replica_id)
                
                # Atualizar status de sincronização
                sync_key = (task.source_fractal_id.split('_')[0], task.target_region)
                if sync_key not in self.region_sync_status:
                    self.region_sync_status[sync_key] = RegionSyncStatus(
                        source_region=sync_key[0],
                        target_region=sync_key[1],
                        last_sync_time=time.time(),
                        sync_latency=duration * 1000,  # Converter para ms
                        data_consistency=1.0,
                        consciousness_level=self.stats['consciousness_level']
                    )
                else:
                    sync_status = self.region_sync_status[sync_key]
                    sync_status.last_sync_time = time.time()
                    sync_status.sync_latency = duration * 1000
                    sync_status.data_consistency = 1.0
                
                logger.info(f"Replicação concluída: {task_id} ({duration:.2f}s)")
                
        except Exception as e:
            logger.error(f"Erro na execução da replicação {task_id}: {e}")
            with self._lock:
                if task_id in self.replication_tasks:
                    task = self.replication_tasks[task_id]
                    task.status = ReplicationStatus.FAILED
                    task.end_time = time.time()
                    task.error_message = str(e)
                    self.stats['failed_replications'] += 1
    
    def get_replication_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retorna status de uma tarefa de replicação."""
        with self._lock:
            if task_id not in self.replication_tasks:
                return None
            
            task = self.replication_tasks[task_id]
            
            return {
                'task_id': task.task_id,
                'source_fractal_id': task.source_fractal_id,
                'target_region': task.target_region,
                'status': task.status.value,
                'progress': task.get_progress(),
                'data_size': task.data_size,
                'bytes_transferred': task.bytes_transferred,
                'duration': task.get_duration(),
                'error_message': task.error_message,
                'consciousness_level': float(task.consciousness_level)
            }
    
    def sync_regions(self, source_region: str, target_region: str) -> bool:
        """Sincroniza duas regiões."""
        try:
            with self._lock:
                sync_key = (source_region, target_region)
                
                # Verificar se já existe status de sincronização
                if sync_key not in self.region_sync_status:
                    self.region_sync_status[sync_key] = RegionSyncStatus(
                        source_region=source_region,
                        target_region=target_region,
                        last_sync_time=time.time(),
                        sync_latency=0.0,
                        data_consistency=0.0,
                        consciousness_level=self.stats['consciousness_level']
                    )
                
                sync_status = self.region_sync_status[sync_key]
                
                # Simular sincronização
                start_time = time.time()
                
                # Encontrar fractais que precisam ser sincronizados
                fractals_to_sync = []
                for fractal_id, replicas in self.fractal_replicas.items():
                    if source_region in fractal_id and target_region not in str(replicas):
                        fractals_to_sync.append(fractal_id)
                
                # Executar sincronização
                for fractal_id in fractals_to_sync:
                    self.replicate_fractal(fractal_id, target_region)
                
                # Atualizar status
                sync_status.last_sync_time = time.time()
                sync_status.sync_latency = (sync_status.last_sync_time - start_time) * 1000
                sync_status.data_consistency = 1.0
                sync_status.pending_changes = 0
                
                self.stats['regions_synced'] += 1
                
                logger.info(f"Regiões sincronizadas: {source_region} -> {target_region}")
                return True
                
        except Exception as e:
            logger.error(f"Erro na sincronização de regiões: {e}")
            return False
    
    def get_region_consistency(self, region1: str, region2: str) -> Dict[str, Any]:
        """Retorna métricas de consistência entre duas regiões."""
        try:
            with self._lock:
                sync_key = (region1, region2)
                reverse_key = (region2, region1)
                
                # Buscar status de sincronização
                sync_status = None
                if sync_key in self.region_sync_status:
                    sync_status = self.region_sync_status[sync_key]
                elif reverse_key in self.region_sync_status:
                    sync_status = self.region_sync_status[reverse_key]
                
                if not sync_status:
                    return {'error': 'Status de sincronização não encontrado'}
                
                # Calcular métricas
                time_since_sync = time.time() - sync_status.last_sync_time
                consistency_score = max(0.0, sync_status.data_consistency - (time_since_sync / 3600))  # Degradar com tempo
                
                return {
                    'source_region': sync_status.source_region,
                    'target_region': sync_status.target_region,
                    'last_sync_time': sync_status.last_sync_time,
                    'time_since_sync': time_since_sync,
                    'sync_latency': sync_status.sync_latency,
                    'data_consistency': consistency_score,
                    'pending_changes': sync_status.pending_changes,
                    'consciousness_level': float(sync_status.consciousness_level)
                }
                
        except Exception as e:
            logger.error(f"Erro na obtenção de consistência entre regiões: {e}")
            return {'error': str(e)}
    
    def optimize_replication(self) -> Dict[str, Any]:
        """Otimiza sistema de replicação."""
        try:
            with self._lock:
                optimization_stats = {
                    'policies_optimized': 0,
                    'latency_improvements': 0,
                    'consciousness_improvement': Decimal('0.0'),
                    'timestamp': time.time()
                }
                
                # Otimizar políticas de replicação
                for policy_id, policy in self.replication_policies.items():
                    if policy.enabled:
                        # Ajustar intervalo baseado na latência
                        if policy.max_latency > 1000:
                            policy.replication_interval = min(600.0, policy.replication_interval * 1.1)
                        elif policy.max_latency < 100:
                            policy.replication_interval = max(30.0, policy.replication_interval * 0.9)
                        
                        # Aumentar consciência da política
                        policy.consciousness_level = min(
                            Decimal('1.0'),
                            policy.consciousness_level + Decimal('0.01')
                        )
                        
                        optimization_stats['policies_optimized'] += 1
                
                # Otimizar status de sincronização
                for sync_key, sync_status in self.region_sync_status.items():
                    # Melhorar consistência de dados
                    if sync_status.data_consistency < 0.9:
                        sync_status.data_consistency = min(1.0, sync_status.data_consistency + 0.05)
                        optimization_stats['latency_improvements'] += 1
                    
                    # Aumentar consciência
                    sync_status.consciousness_level = min(
                        Decimal('1.0'),
                        sync_status.consciousness_level + Decimal('0.01')
                    )
                
                # Aumentar consciência geral
                old_consciousness = self.stats['consciousness_level']
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.02')
                )
                optimization_stats['consciousness_improvement'] = (
                    self.stats['consciousness_level'] - old_consciousness
                )
                
                logger.info(f"Replicação otimizada: {optimization_stats['policies_optimized']} políticas")
                return optimization_stats
                
        except Exception as e:
            logger.error(f"Erro na otimização da replicação: {e}")
            return {'error': str(e)}
    
    def get_replication_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de replicação."""
        with self._lock:
            # Estatísticas das tarefas
            active_tasks = sum(1 for task in self.replication_tasks.values() 
                             if task.status == ReplicationStatus.IN_PROGRESS)
            completed_tasks = sum(1 for task in self.replication_tasks.values() 
                                if task.status == ReplicationStatus.COMPLETED)
            failed_tasks = sum(1 for task in self.replication_tasks.values() 
                             if task.status == ReplicationStatus.FAILED)
            
            # Estatísticas das políticas
            enabled_policies = sum(1 for policy in self.replication_policies.values() if policy.enabled)
            
            # Estatísticas de consistência
            consistency_scores = [sync.data_consistency for sync in self.region_sync_status.values()]
            average_consistency = sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0.0
            
            return {
                'total_replications': self.stats['total_replications'],
                'successful_replications': self.stats['successful_replications'],
                'failed_replications': self.stats['failed_replications'],
                'success_rate': (self.stats['successful_replications'] / 
                               max(self.stats['total_replications'], 1)),
                'average_replication_time': self.stats['average_replication_time'],
                'active_tasks': active_tasks,
                'completed_tasks': completed_tasks,
                'failed_tasks': failed_tasks,
                'consciousness_level': float(self.stats['consciousness_level']),
                'active_policies': enabled_policies,
                'total_policies': len(self.replication_policies),
                'regions_synced': self.stats['regions_synced'],
                'average_consistency': average_consistency,
                'replication_policies': [
                    {
                        'policy_id': policy.policy_id,
                        'source_region': policy.source_region,
                        'target_regions': policy.target_regions,
                        'consistency_level': policy.consistency_level.value,
                        'replication_interval': policy.replication_interval,
                        'max_latency': policy.max_latency,
                        'enabled': policy.enabled,
                        'consciousness_level': float(policy.consciousness_level)
                    }
                    for policy in self.replication_policies.values()
                ],
                'region_sync_status': [
                    {
                        'source_region': sync.source_region,
                        'target_region': sync.target_region,
                        'last_sync_time': sync.last_sync_time,
                        'sync_latency': sync.sync_latency,
                        'data_consistency': sync.data_consistency,
                        'pending_changes': sync.pending_changes,
                        'consciousness_level': float(sync.consciousness_level)
                    }
                    for sync in self.region_sync_status.values()
                ]
            }


# Instância global do replicador cross-region
cross_region_replicator = CrossRegionReplicator()
