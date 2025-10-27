"""
Sistema de Sharding Inteligente de Fractais.

Este módulo implementa um sistema inteligente que:
- Distribui dados entre fractais usando sharding inteligente
- Aplica algoritmos de hash consistentes
- Implementa rebalancing automático
- Otimiza distribuição baseada em padrões de acesso
- Garante alta disponibilidade e performance
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
import bisect

logger = logging.getLogger(__name__)


class ShardingStrategy(Enum):
    """Estratégias de sharding."""
    CONSISTENT_HASH = "consistent_hash"
    RANGE_BASED = "range_based"
    DIRECTORY_BASED = "directory_based"
    HYBRID = "hybrid"


class ShardStatus(Enum):
    """Status de um shard."""
    ACTIVE = "active"
    MIGRATING = "migrating"
    INACTIVE = "inactive"
    FAILED = "failed"


@dataclass
class Shard:
    """Shard de dados."""
    shard_id: str
    fractal_id: str
    start_key: str
    end_key: str
    data_count: int = 0
    capacity: int = 10000
    status: ShardStatus = ShardStatus.ACTIVE
    last_access: float = field(default_factory=time.time)
    consciousness_level: Decimal = Decimal('0.5')
    
    def get_load_percentage(self) -> float:
        """Retorna porcentagem de carga do shard."""
        return (self.data_count / self.capacity) * 100 if self.capacity > 0 else 0
    
    def is_overloaded(self) -> bool:
        """Verifica se shard está sobrecarregado."""
        return self.get_load_percentage() > 80
    
    def can_accept_data(self, data_size: int = 1) -> bool:
        """Verifica se shard pode aceitar mais dados."""
        return (self.data_count + data_size) <= self.capacity and self.status == ShardStatus.ACTIVE


@dataclass
class ShardingRule:
    """Regra de sharding."""
    rule_id: str
    key_pattern: str
    sharding_strategy: ShardingStrategy
    target_fractals: List[str]
    priority: int = 1
    enabled: bool = True
    consciousness_level: Decimal = Decimal('0.5')


@dataclass
class ConsistentHashRing:
    """Anel de hash consistente."""
    virtual_nodes: int = 100
    hash_ring: List[Tuple[int, str]] = field(default_factory=list)  # (hash, fractal_id)
    fractal_weights: Dict[str, int] = field(default_factory=dict)
    
    def add_fractal(self, fractal_id: str, weight: int = 1):
        """Adiciona fractal ao anel."""
        self.fractal_weights[fractal_id] = weight
        
        for i in range(self.virtual_nodes * weight):
            virtual_key = f"{fractal_id}:{i}"
            hash_value = self._hash(virtual_key)
            bisect.insort(self.hash_ring, (hash_value, fractal_id))
    
    def remove_fractal(self, fractal_id: str):
        """Remove fractal do anel."""
        if fractal_id in self.fractal_weights:
            del self.fractal_weights[fractal_id]
            self.hash_ring = [(h, f) for h, f in self.hash_ring if f != fractal_id]
    
    def get_fractal(self, key: str) -> str:
        """Retorna fractal responsável pela chave."""
        if not self.hash_ring:
            return ""
        
        hash_value = self._hash(key)
        index = bisect.bisect_left(self.hash_ring, (hash_value, ""))
        
        if index >= len(self.hash_ring):
            index = 0
        
        return self.hash_ring[index][1]
    
    def _hash(self, key: str) -> int:
        """Calcula hash da chave."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)


class IntelligentShardingSystem:
    """
    Sistema de Sharding Inteligente de Fractais.
    
    Características:
    - Sharding baseado em hash consistente
    - Rebalancing automático
    - Múltiplas estratégias de sharding
    - Otimização baseada em padrões de acesso
    - Monitoramento de performance
    """
    
    def __init__(self):
        self.shards: Dict[str, Shard] = {}
        self.sharding_rules: Dict[str, ShardingRule] = {}
        self.hash_rings: Dict[str, ConsistentHashRing] = {}
        self.key_distribution: Dict[str, str] = {}  # key -> fractal_id
        self.access_patterns: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self._lock = threading.RLock()
        
        self.stats = {
            'total_shards': 0,
            'active_shards': 0,
            'total_keys': 0,
            'average_load': 0.0,
            'consciousness_level': Decimal('0.1'),
            'rebalancing_operations': 0,
            'shard_migrations': 0,
            'performance_score': 0.0
        }
        
        self._initialize_default_rules()
        logger.info("IntelligentShardingSystem inicializado")
    
    def _initialize_default_rules(self):
        """Inicializa regras de sharding padrão."""
        # Regra para dados gerais
        self.sharding_rules['general'] = ShardingRule(
            rule_id='general',
            key_pattern='*',
            sharding_strategy=ShardingStrategy.CONSISTENT_HASH,
            target_fractals=[],
            consciousness_level=Decimal('0.7')
        )
        
        # Regra para dados de usuário
        self.sharding_rules['user_data'] = ShardingRule(
            rule_id='user_data',
            key_pattern='user:*',
            sharding_strategy=ShardingStrategy.CONSISTENT_HASH,
            target_fractals=[],
            consciousness_level=Decimal('0.8')
        )
        
        # Regra para dados de transação
        self.sharding_rules['transaction_data'] = ShardingRule(
            rule_id='transaction_data',
            key_pattern='txn:*',
            sharding_strategy=ShardingStrategy.RANGE_BASED,
            target_fractals=[],
            consciousness_level=Decimal('0.9')
        )
    
    def create_shard(self, shard_id: str, fractal_id: str, start_key: str, 
                    end_key: str, capacity: int = 10000) -> bool:
        """Cria um novo shard."""
        try:
            with self._lock:
                shard = Shard(
                    shard_id=shard_id,
                    fractal_id=fractal_id,
                    start_key=start_key,
                    end_key=end_key,
                    capacity=capacity,
                    consciousness_level=self.stats['consciousness_level']
                )
                
                self.shards[shard_id] = shard
                self.stats['total_shards'] += 1
                self.stats['active_shards'] += 1
                
                logger.info(f"Shard criado: {shard_id} no fractal {fractal_id}")
                return True
                
        except Exception as e:
            logger.error(f"Erro na criação do shard {shard_id}: {e}")
            return False
    
    def add_fractal_to_ring(self, fractal_id: str, ring_name: str = 'default', 
                           weight: int = 1) -> bool:
        """Adiciona fractal ao anel de hash."""
        try:
            with self._lock:
                if ring_name not in self.hash_rings:
                    self.hash_rings[ring_name] = ConsistentHashRing()
                
                self.hash_rings[ring_name].add_fractal(fractal_id, weight)
                
                logger.info(f"Fractal {fractal_id} adicionado ao anel {ring_name}")
                return True
                
        except Exception as e:
            logger.error(f"Erro ao adicionar fractal ao anel: {e}")
            return False
    
    def route_key(self, key: str, rule_id: str = 'general') -> Optional[str]:
        """
        Roteia uma chave para o fractal apropriado.
        
        Args:
            key: Chave a ser roteada
            rule_id: ID da regra de sharding
            
        Returns:
            ID do fractal de destino ou None
        """
        try:
            with self._lock:
                if rule_id not in self.sharding_rules:
                    return None
                
                rule = self.sharding_rules[rule_id]
                if not rule.enabled:
                    return None
                
                # Registrar padrão de acesso
                self.access_patterns[key].append(time.time())
                
                # Determinar fractal baseado na estratégia
                fractal_id = None
                
                if rule.sharding_strategy == ShardingStrategy.CONSISTENT_HASH:
                    fractal_id = self._route_consistent_hash(key, rule)
                elif rule.sharding_strategy == ShardingStrategy.RANGE_BASED:
                    fractal_id = self._route_range_based(key, rule)
                elif rule.sharding_strategy == ShardingStrategy.DIRECTORY_BASED:
                    fractal_id = self._route_directory_based(key, rule)
                elif rule.sharding_strategy == ShardingStrategy.HYBRID:
                    fractal_id = self._route_hybrid(key, rule)
                
                if fractal_id:
                    self.key_distribution[key] = fractal_id
                    self.stats['total_keys'] += 1
                    
                    # Atualizar estatísticas do shard
                    shard = self._find_shard_for_fractal(fractal_id)
                    if shard:
                        shard.data_count += 1
                        shard.last_access = time.time()
                
                logger.debug(f"Chave {key} roteada para fractal {fractal_id}")
                return fractal_id
                
        except Exception as e:
            logger.error(f"Erro no roteamento da chave {key}: {e}")
            return None
    
    def _route_consistent_hash(self, key: str, rule: ShardingRule) -> Optional[str]:
        """Roteia usando hash consistente."""
        try:
            ring_name = f"{rule.rule_id}_ring"
            if ring_name not in self.hash_rings:
                return None
            
            ring = self.hash_rings[ring_name]
            return ring.get_fractal(key)
            
        except Exception as e:
            logger.error(f"Erro no roteamento por hash consistente: {e}")
            return None
    
    def _route_range_based(self, key: str, rule: ShardingRule) -> Optional[str]:
        """Roteia usando ranges."""
        try:
            # Encontrar shard que contém a chave
            for shard in self.shards.values():
                if shard.fractal_id in rule.target_fractals:
                    if shard.start_key <= key <= shard.end_key:
                        return shard.fractal_id
            
            return None
            
        except Exception as e:
            logger.error(f"Erro no roteamento por range: {e}")
            return None
    
    def _route_directory_based(self, key: str, rule: ShardingRule) -> Optional[str]:
        """Roteia usando diretório."""
        try:
            # Verificar se já existe mapeamento
            if key in self.key_distribution:
                return self.key_distribution[key]
            
            # Selecionar fractal com menor carga
            best_fractal = None
            best_load = float('inf')
            
            for fractal_id in rule.target_fractals:
                shard = self._find_shard_for_fractal(fractal_id)
                if shard and shard.can_accept_data():
                    load = shard.get_load_percentage()
                    if load < best_load:
                        best_load = load
                        best_fractal = fractal_id
            
            return best_fractal
            
        except Exception as e:
            logger.error(f"Erro no roteamento por diretório: {e}")
            return None
    
    def _route_hybrid(self, key: str, rule: ShardingRule) -> Optional[str]:
        """Roteia usando estratégia híbrida."""
        try:
            # Combinar hash consistente com balanceamento de carga
            hash_fractal = self._route_consistent_hash(key, rule)
            
            if hash_fractal:
                shard = self._find_shard_for_fractal(hash_fractal)
                if shard and not shard.is_overloaded():
                    return hash_fractal
            
            # Se fractal por hash está sobrecarregado, usar diretório
            return self._route_directory_based(key, rule)
            
        except Exception as e:
            logger.error(f"Erro no roteamento híbrido: {e}")
            return None
    
    def _find_shard_for_fractal(self, fractal_id: str) -> Optional[Shard]:
        """Encontra shard para um fractal."""
        for shard in self.shards.values():
            if shard.fractal_id == fractal_id:
                return shard
        return None
    
    def rebalance_shards(self) -> Dict[str, Any]:
        """Executa rebalancing dos shards."""
        try:
            with self._lock:
                rebalance_stats = {
                    'shards_rebalanced': 0,
                    'keys_migrated': 0,
                    'load_improvement': 0.0,
                    'consciousness_improvement': Decimal('0.0'),
                    'timestamp': time.time()
                }
                
                # Identificar shards sobrecarregados e subutilizados
                overloaded_shards = []
                underloaded_shards = []
                
                for shard in self.shards.values():
                    if shard.status == ShardStatus.ACTIVE:
                        load_percentage = shard.get_load_percentage()
                        
                        if load_percentage > 80:
                            overloaded_shards.append(shard)
                        elif load_percentage < 30:
                            underloaded_shards.append(shard)
                
                # Executar migração de dados
                for overloaded_shard in overloaded_shards:
                    for underloaded_shard in underloaded_shards:
                        if self._migrate_data(overloaded_shard, underloaded_shard):
                            rebalance_stats['shards_rebalanced'] += 1
                            rebalance_stats['keys_migrated'] += 1
                            self.stats['shard_migrations'] += 1
                
                # Recalcular anéis de hash se necessário
                self._recalculate_hash_rings()
                
                # Aumentar consciência
                old_consciousness = self.stats['consciousness_level']
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.02')
                )
                rebalance_stats['consciousness_improvement'] = (
                    self.stats['consciousness_level'] - old_consciousness
                )
                
                self.stats['rebalancing_operations'] += 1
                
                logger.info(f"Rebalancing executado: {rebalance_stats['shards_rebalanced']} shards")
                return rebalance_stats
                
        except Exception as e:
            logger.error(f"Erro no rebalancing: {e}")
            return {'error': str(e)}
    
    def _migrate_data(self, source_shard: Shard, target_shard: Shard) -> bool:
        """Migra dados entre shards."""
        try:
            # Simular migração de dados
            migration_amount = min(
                source_shard.data_count - (source_shard.capacity * 0.7),  # Deixar 70% de carga
                target_shard.capacity - target_shard.data_count  # Não exceder capacidade do destino
            )
            
            if migration_amount > 0:
                source_shard.data_count -= migration_amount
                target_shard.data_count += migration_amount
                
                # Marcar shards como migrando temporariamente
                source_shard.status = ShardStatus.MIGRATING
                target_shard.status = ShardStatus.MIGRATING
                
                # Simular tempo de migração
                time.sleep(0.1)
                
                # Restaurar status
                source_shard.status = ShardStatus.ACTIVE
                target_shard.status = ShardStatus.ACTIVE
                
                logger.debug(f"Dados migrados: {migration_amount} de {source_shard.shard_id} para {target_shard.shard_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erro na migração de dados: {e}")
            return False
    
    def _recalculate_hash_rings(self):
        """Recalcula anéis de hash baseado na carga atual."""
        try:
            for ring_name, ring in self.hash_rings.items():
                # Ajustar pesos baseado na carga
                for fractal_id in ring.fractal_weights.keys():
                    shard = self._find_shard_for_fractal(fractal_id)
                    if shard:
                        load_percentage = shard.get_load_percentage()
                        
                        # Ajustar peso baseado na carga
                        if load_percentage > 80:
                            new_weight = max(1, ring.fractal_weights[fractal_id] - 1)
                        elif load_percentage < 30:
                            new_weight = ring.fractal_weights[fractal_id] + 1
                        else:
                            new_weight = ring.fractal_weights[fractal_id]
                        
                        if new_weight != ring.fractal_weights[fractal_id]:
                            ring.remove_fractal(fractal_id)
                            ring.add_fractal(fractal_id, new_weight)
                
        except Exception as e:
            logger.error(f"Erro no recálculo dos anéis de hash: {e}")
    
    def get_shard_performance(self, shard_id: str) -> Optional[Dict[str, Any]]:
        """Retorna performance de um shard."""
        with self._lock:
            if shard_id not in self.shards:
                return None
            
            shard = self.shards[shard_id]
            
            return {
                'shard_id': shard.shard_id,
                'fractal_id': shard.fractal_id,
                'data_count': shard.data_count,
                'capacity': shard.capacity,
                'load_percentage': shard.get_load_percentage(),
                'status': shard.status.value,
                'last_access': shard.last_access,
                'consciousness_level': float(shard.consciousness_level)
            }
    
    def optimize_sharding(self) -> Dict[str, Any]:
        """Otimiza sistema de sharding."""
        try:
            with self._lock:
                optimization_stats = {
                    'rules_optimized': 0,
                    'rings_optimized': 0,
                    'consciousness_improvement': Decimal('0.0'),
                    'timestamp': time.time()
                }
                
                # Otimizar regras de sharding
                for rule_id, rule in self.sharding_rules.items():
                    if rule.enabled:
                        # Ajustar estratégia baseado nos padrões de acesso
                        access_patterns = self.access_patterns
                        
                        # Se muitos acessos sequenciais, usar range-based
                        sequential_accesses = self._count_sequential_accesses(access_patterns)
                        if sequential_accesses > len(access_patterns) * 0.3:
                            if rule.sharding_strategy != ShardingStrategy.RANGE_BASED:
                                rule.sharding_strategy = ShardingStrategy.RANGE_BASED
                                optimization_stats['rules_optimized'] += 1
                        
                        # Se muitos acessos aleatórios, usar consistent hash
                        elif sequential_accesses < len(access_patterns) * 0.1:
                            if rule.sharding_strategy != ShardingStrategy.CONSISTENT_HASH:
                                rule.sharding_strategy = ShardingStrategy.CONSISTENT_HASH
                                optimization_stats['rules_optimized'] += 1
                        
                        # Aumentar consciência da regra
                        rule.consciousness_level = min(
                            Decimal('1.0'),
                            rule.consciousness_level + Decimal('0.01')
                        )
                
                # Otimizar anéis de hash
                for ring_name, ring in self.hash_rings.items():
                    # Ajustar número de nós virtuais baseado na carga
                    total_fractals = len(ring.fractal_weights)
                    if total_fractals > 0:
                        optimal_virtual_nodes = max(100, total_fractals * 50)
                        if ring.virtual_nodes != optimal_virtual_nodes:
                            ring.virtual_nodes = optimal_virtual_nodes
                            optimization_stats['rings_optimized'] += 1
                
                # Aumentar consciência geral
                old_consciousness = self.stats['consciousness_level']
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.02')
                )
                optimization_stats['consciousness_improvement'] = (
                    self.stats['consciousness_level'] - old_consciousness
                )
                
                logger.info(f"Sharding otimizado: {optimization_stats['rules_optimized']} regras")
                return optimization_stats
                
        except Exception as e:
            logger.error(f"Erro na otimização do sharding: {e}")
            return {'error': str(e)}
    
    def _count_sequential_accesses(self, access_patterns: Dict[str, deque]) -> int:
        """Conta acessos sequenciais nos padrões."""
        sequential_count = 0
        
        for key, accesses in access_patterns.items():
            if len(accesses) > 1:
                # Verificar se acessos são sequenciais (baseado em timestamp)
                timestamps = list(accesses)
                for i in range(1, len(timestamps)):
                    if timestamps[i] - timestamps[i-1] < 1.0:  # Menos de 1 segundo
                        sequential_count += 1
        
        return sequential_count
    
    def get_sharding_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de sharding."""
        with self._lock:
            # Calcular métricas de performance
            total_capacity = sum(shard.capacity for shard in self.shards.values())
            total_data = sum(shard.data_count for shard in self.shards.values())
            average_load = (total_data / total_capacity) * 100 if total_capacity > 0 else 0
            
            # Calcular score de performance
            overloaded_shards = sum(1 for shard in self.shards.values() if shard.is_overloaded())
            performance_score = 1.0 - (overloaded_shards / max(len(self.shards), 1))
            
            return {
                'total_shards': self.stats['total_shards'],
                'active_shards': self.stats['active_shards'],
                'total_keys': self.stats['total_keys'],
                'total_capacity': total_capacity,
                'total_data': total_data,
                'average_load': average_load,
                'overloaded_shards': overloaded_shards,
                'performance_score': performance_score,
                'consciousness_level': float(self.stats['consciousness_level']),
                'rebalancing_operations': self.stats['rebalancing_operations'],
                'shard_migrations': self.stats['shard_migrations'],
                'sharding_rules': [
                    {
                        'rule_id': rule.rule_id,
                        'key_pattern': rule.key_pattern,
                        'sharding_strategy': rule.sharding_strategy.value,
                        'target_fractals': rule.target_fractals,
                        'priority': rule.priority,
                        'enabled': rule.enabled,
                        'consciousness_level': float(rule.consciousness_level)
                    }
                    for rule in self.sharding_rules.values()
                ],
                'hash_rings': {
                    ring_name: {
                        'virtual_nodes': ring.virtual_nodes,
                        'fractal_count': len(ring.fractal_weights),
                        'fractal_weights': dict(ring.fractal_weights)
                    }
                    for ring_name, ring in self.hash_rings.items()
                }
            }


# Instância global do sistema de sharding inteligente
intelligent_sharding_system = IntelligentShardingSystem()
