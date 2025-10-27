"""
Sistema de Otimização de Memória Distribuída entre Fractais.

Este módulo implementa um sistema inteligente de gerenciamento de memória que:
- Distribui memória entre fractais de forma consciente
- Otimiza uso de memória baseado em padrões de acesso
- Implementa garbage collection inteligente
- Gerencia pools de memória compartilhados
- Aplica compressão de memória em tempo real
"""

import gc
import psutil
import threading
import time
from typing import Dict, Any, Optional, List, Tuple, Set
from decimal import Decimal
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import logging
import weakref
import sys

logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """Tipos de memória para otimização."""
    CACHE = "cache"
    FRACTAL_DATA = "fractal_data"
    BLOCKCHAIN_DATA = "blockchain_data"
    TRANSACTION_DATA = "transaction_data"
    USER_DATA = "user_data"
    SYSTEM_DATA = "system_data"
    TEMPORARY = "temporary"


class MemoryPriority(Enum):
    """Prioridades de memória."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    TEMPORARY = 5


@dataclass
class MemoryBlock:
    """Bloco de memória com metadados."""
    block_id: str
    memory_type: MemoryType
    priority: MemoryPriority
    size_bytes: int
    fractal_id: str
    access_count: int = 0
    last_access: float = field(default_factory=time.time)
    creation_time: float = field(default_factory=time.time)
    consciousness_level: Decimal = Decimal('0.5')
    compression_ratio: float = 1.0
    is_compressed: bool = False
    
    def get_age_score(self) -> float:
        """Calcula score de idade do bloco."""
        age_seconds = time.time() - self.creation_time
        return min(age_seconds / 3600, 1.0)  # Normalizar para 1 hora
    
    def get_access_score(self) -> float:
        """Calcula score de acesso do bloco."""
        if self.access_count == 0:
            return 0.0
        
        # Score baseado em frequência de acesso e recência
        frequency_score = min(self.access_count / 100, 1.0)
        recency_score = 1.0 - min((time.time() - self.last_access) / 3600, 1.0)
        
        return (frequency_score + recency_score) / 2
    
    def get_importance_score(self) -> float:
        """Calcula score de importância do bloco."""
        priority_scores = {
            MemoryPriority.CRITICAL: 1.0,
            MemoryPriority.HIGH: 0.8,
            MemoryPriority.MEDIUM: 0.6,
            MemoryPriority.LOW: 0.4,
            MemoryPriority.TEMPORARY: 0.2
        }
        
        priority_score = priority_scores.get(self.priority, 0.5)
        consciousness_score = float(self.consciousness_level)
        access_score = self.get_access_score()
        
        return (priority_score + consciousness_score + access_score) / 3


@dataclass
class FractalMemoryStats:
    """Estatísticas de memória de um fractal."""
    fractal_id: str
    total_memory: int = 0
    used_memory: int = 0
    available_memory: int = 0
    memory_blocks: int = 0
    consciousness_level: Decimal = Decimal('0.5')
    compression_efficiency: float = 1.0
    last_optimization: float = field(default_factory=time.time)


class DistributedMemoryManager:
    """
    Sistema de Otimização de Memória Distribuída entre Fractais.
    
    Características:
    - Gerenciamento consciente de memória
    - Distribuição inteligente entre fractais
    - Compressão automática de dados
    - Garbage collection adaptativo
    - Pool de memória compartilhado
    """
    
    def __init__(self, max_total_memory: int = 1024 * 1024 * 1024):  # 1GB padrão
        self.max_total_memory = max_total_memory
        self.memory_blocks: Dict[str, MemoryBlock] = {}
        self.fractal_memory: Dict[str, FractalMemoryStats] = {}
        self.memory_pools: Dict[MemoryType, List[str]] = defaultdict(list)
        self._lock = threading.RLock()
        
        self.stats = {
            'total_allocated': 0,
            'total_compressed': 0,
            'compression_savings': 0,
            'garbage_collections': 0,
            'consciousness_level': Decimal('0.1'),
            'optimization_cycles': 0
        }
        
        self._initialize_memory_monitoring()
        logger.info(f"DistributedMemoryManager inicializado com {max_total_memory // (1024*1024)}MB")
    
    def _initialize_memory_monitoring(self):
        """Inicializa monitoramento de memória do sistema."""
        try:
            # Obter informações de memória do sistema
            memory_info = psutil.virtual_memory()
            self.system_memory_info = {
                'total': memory_info.total,
                'available': memory_info.available,
                'used': memory_info.used,
                'free': memory_info.free,
                'percent': memory_info.percent
            }
            
            logger.info(f"Memória do sistema: {memory_info.total // (1024*1024)}MB total, "
                       f"{memory_info.available // (1024*1024)}MB disponível")
            
        except Exception as e:
            logger.error(f"Erro na inicialização do monitoramento: {e}")
            self.system_memory_info = {
                'total': self.max_total_memory,
                'available': self.max_total_memory,
                'used': 0,
                'free': self.max_total_memory,
                'percent': 0.0
            }
    
    def register_fractal(self, fractal_id: str, initial_memory_limit: int = 0):
        """Registra um fractal no sistema de memória."""
        try:
            with self._lock:
                if fractal_id not in self.fractal_memory:
                    # Calcular limite de memória se não especificado
                    if initial_memory_limit == 0:
                        available_fractals = len(self.fractal_memory) + 1
                        initial_memory_limit = self.max_total_memory // max(available_fractals, 1)
                    
                    self.fractal_memory[fractal_id] = FractalMemoryStats(
                        fractal_id=fractal_id,
                        available_memory=initial_memory_limit
                    )
                    
                    logger.info(f"Fractal {fractal_id} registrado com {initial_memory_limit // (1024*1024)}MB")
                
        except Exception as e:
            logger.error(f"Erro no registro do fractal {fractal_id}: {e}")
    
    def allocate_memory(self, fractal_id: str, size_bytes: int, 
                       memory_type: MemoryType, priority: MemoryPriority = MemoryPriority.MEDIUM) -> Optional[str]:
        """
        Aloca memória para um fractal.
        
        Args:
            fractal_id: ID do fractal
            size_bytes: Tamanho em bytes
            memory_type: Tipo de memória
            priority: Prioridade da memória
            
        Returns:
            ID do bloco de memória ou None se falhar
        """
        try:
            with self._lock:
                # Verificar se fractal está registrado
                if fractal_id not in self.fractal_memory:
                    self.register_fractal(fractal_id)
                
                fractal_stats = self.fractal_memory[fractal_id]
                
                # Verificar limite de memória do fractal
                if fractal_stats.used_memory + size_bytes > fractal_stats.available_memory:
                    # Tentar liberar memória
                    if not self._free_memory_for_fractal(fractal_id, size_bytes):
                        logger.warning(f"Falha ao alocar {size_bytes} bytes para fractal {fractal_id}")
                        return None
                
                # Verificar limite total do sistema
                if self.stats['total_allocated'] + size_bytes > self.max_total_memory:
                    # Tentar liberar memória global
                    if not self._free_global_memory(size_bytes):
                        logger.warning(f"Falha ao alocar {size_bytes} bytes - limite do sistema atingido")
                        return None
                
                # Criar bloco de memória
                block_id = f"{fractal_id}_{memory_type.value}_{int(time.time() * 1000)}"
                
                memory_block = MemoryBlock(
                    block_id=block_id,
                    memory_type=memory_type,
                    priority=priority,
                    size_bytes=size_bytes,
                    fractal_id=fractal_id,
                    consciousness_level=fractal_stats.consciousness_level
                )
                
                # Registrar bloco
                self.memory_blocks[block_id] = memory_block
                self.memory_pools[memory_type].append(block_id)
                
                # Atualizar estatísticas
                fractal_stats.used_memory += size_bytes
                fractal_stats.memory_blocks += 1
                self.stats['total_allocated'] += size_bytes
                
                logger.debug(f"Memória alocada: {block_id} ({size_bytes} bytes)")
                return block_id
                
        except Exception as e:
            logger.error(f"Erro na alocação de memória: {e}")
            return None
    
    def deallocate_memory(self, block_id: str) -> bool:
        """Desaloca bloco de memória."""
        try:
            with self._lock:
                if block_id not in self.memory_blocks:
                    return False
                
                memory_block = self.memory_blocks[block_id]
                fractal_id = memory_block.fractal_id
                
                # Atualizar estatísticas do fractal
                if fractal_id in self.fractal_memory:
                    fractal_stats = self.fractal_memory[fractal_id]
                    fractal_stats.used_memory -= memory_block.size_bytes
                    fractal_stats.memory_blocks -= 1
                
                # Atualizar estatísticas globais
                self.stats['total_allocated'] -= memory_block.size_bytes
                
                # Remover dos pools
                memory_type = memory_block.memory_type
                if block_id in self.memory_pools[memory_type]:
                    self.memory_pools[memory_type].remove(block_id)
                
                # Remover bloco
                del self.memory_blocks[block_id]
                
                logger.debug(f"Memória desalocada: {block_id}")
                return True
                
        except Exception as e:
            logger.error(f"Erro na desalocação de memória {block_id}: {e}")
            return False
    
    def access_memory(self, block_id: str) -> bool:
        """Registra acesso a um bloco de memória."""
        try:
            with self._lock:
                if block_id in self.memory_blocks:
                    memory_block = self.memory_blocks[block_id]
                    memory_block.access_count += 1
                    memory_block.last_access = time.time()
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Erro no acesso à memória {block_id}: {e}")
            return False
    
    def _free_memory_for_fractal(self, fractal_id: str, required_bytes: int) -> bool:
        """Libera memória para um fractal específico."""
        try:
            # Encontrar blocos do fractal ordenados por importância
            fractal_blocks = []
            for block_id, block in self.memory_blocks.items():
                if block.fractal_id == fractal_id:
                    fractal_blocks.append((block_id, block))
            
            # Ordenar por score de importância (menor = menos importante)
            fractal_blocks.sort(key=lambda x: x[1].get_importance_score())
            
            freed_bytes = 0
            blocks_to_free = []
            
            for block_id, block in fractal_blocks:
                if freed_bytes >= required_bytes:
                    break
                
                # Não liberar blocos críticos
                if block.priority == MemoryPriority.CRITICAL:
                    continue
                
                blocks_to_free.append(block_id)
                freed_bytes += block.size_bytes
            
            # Desalocar blocos
            for block_id in blocks_to_free:
                self.deallocate_memory(block_id)
            
            logger.info(f"Liberados {freed_bytes} bytes para fractal {fractal_id}")
            return freed_bytes >= required_bytes
            
        except Exception as e:
            logger.error(f"Erro ao liberar memória para fractal {fractal_id}: {e}")
            return False
    
    def _free_global_memory(self, required_bytes: int) -> bool:
        """Libera memória global do sistema."""
        try:
            # Encontrar todos os blocos ordenados por importância
            all_blocks = [(block_id, block) for block_id, block in self.memory_blocks.items()]
            all_blocks.sort(key=lambda x: x[1].get_importance_score())
            
            freed_bytes = 0
            blocks_to_free = []
            
            for block_id, block in all_blocks:
                if freed_bytes >= required_bytes:
                    break
                
                # Não liberar blocos críticos
                if block.priority == MemoryPriority.CRITICAL:
                    continue
                
                blocks_to_free.append(block_id)
                freed_bytes += block.size_bytes
            
            # Desalocar blocos
            for block_id in blocks_to_free:
                self.deallocate_memory(block_id)
            
            logger.info(f"Liberados {freed_bytes} bytes globalmente")
            return freed_bytes >= required_bytes
            
        except Exception as e:
            logger.error(f"Erro ao liberar memória global: {e}")
            return False
    
    def compress_memory(self, block_id: str, compression_ratio: float = 0.5) -> bool:
        """Comprime um bloco de memória."""
        try:
            with self._lock:
                if block_id not in self.memory_blocks:
                    return False
                
                memory_block = self.memory_blocks[block_id]
                
                # Não comprimir se já estiver comprimido
                if memory_block.is_compressed:
                    return True
                
                # Calcular novo tamanho
                new_size = int(memory_block.size_bytes * compression_ratio)
                size_savings = memory_block.size_bytes - new_size
                
                # Atualizar bloco
                memory_block.size_bytes = new_size
                memory_block.compression_ratio = compression_ratio
                memory_block.is_compressed = True
                
                # Atualizar estatísticas
                fractal_id = memory_block.fractal_id
                if fractal_id in self.fractal_memory:
                    fractal_stats = self.fractal_memory[fractal_id]
                    fractal_stats.used_memory -= size_savings
                
                self.stats['total_allocated'] -= size_savings
                self.stats['total_compressed'] += 1
                self.stats['compression_savings'] += size_savings
                
                logger.debug(f"Bloco {block_id} comprimido: {size_savings} bytes economizados")
                return True
                
        except Exception as e:
            logger.error(f"Erro na compressão de memória {block_id}: {e}")
            return False
    
    def optimize_memory(self) -> Dict[str, Any]:
        """
        Otimiza uso de memória do sistema.
        
        Returns:
            Estatísticas da otimização
        """
        try:
            with self._lock:
                optimization_stats = {
                    'blocks_optimized': 0,
                    'memory_freed': 0,
                    'compressions_applied': 0,
                    'garbage_collections': 0,
                    'consciousness_improvement': Decimal('0.0'),
                    'timestamp': time.time()
                }
                
                # 1. Executar garbage collection
                initial_objects = len(gc.get_objects())
                collected = gc.collect()
                optimization_stats['garbage_collections'] = collected
                self.stats['garbage_collections'] += collected
                
                # 2. Comprimir blocos pouco acessados
                blocks_to_compress = []
                for block_id, block in self.memory_blocks.items():
                    if (not block.is_compressed and 
                        block.priority != MemoryPriority.CRITICAL and
                        block.get_access_score() < 0.3):  # Baixo acesso
                        blocks_to_compress.append(block_id)
                
                for block_id in blocks_to_compress[:10]:  # Limitar a 10 por vez
                    if self.compress_memory(block_id, 0.7):
                        optimization_stats['compressions_applied'] += 1
                
                # 3. Liberar blocos temporários antigos
                blocks_to_free = []
                current_time = time.time()
                
                for block_id, block in self.memory_blocks.items():
                    if (block.priority == MemoryPriority.TEMPORARY and
                        current_time - block.last_access > 1800):  # 30 minutos
                        blocks_to_free.append(block_id)
                
                for block_id in blocks_to_free:
                    if self.deallocate_memory(block_id):
                        optimization_stats['memory_freed'] += 1
                
                # 4. Redistribuir memória entre fractais
                self._redistribute_memory()
                
                # 5. Atualizar consciência
                old_consciousness = self.stats['consciousness_level']
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.02')
                )
                optimization_stats['consciousness_improvement'] = (
                    self.stats['consciousness_level'] - old_consciousness
                )
                
                optimization_stats['blocks_optimized'] = (
                    optimization_stats['compressions_applied'] + 
                    optimization_stats['memory_freed']
                )
                
                self.stats['optimization_cycles'] += 1
                
                logger.info(f"Memória otimizada: {optimization_stats['blocks_optimized']} blocos, "
                           f"{optimization_stats['memory_freed']} bytes liberados")
                
                return optimization_stats
                
        except Exception as e:
            logger.error(f"Erro na otimização de memória: {e}")
            return {'error': str(e)}
    
    def _redistribute_memory(self):
        """Redistribui memória entre fractais baseado na consciência."""
        try:
            if len(self.fractal_memory) < 2:
                return
            
            # Calcular consciência total
            total_consciousness = sum(
                stats.consciousness_level for stats in self.fractal_memory.values()
            )
            
            if total_consciousness == 0:
                return
            
            # Redistribuir baseado na consciência
            for fractal_id, stats in self.fractal_memory.items():
                consciousness_ratio = stats.consciousness_level / total_consciousness
                new_limit = int(self.max_total_memory * consciousness_ratio)
                
                if new_limit != stats.available_memory:
                    stats.available_memory = new_limit
                    logger.debug(f"Limite de memória redistribuído para {fractal_id}: "
                               f"{new_limit // (1024*1024)}MB")
                
        except Exception as e:
            logger.error(f"Erro na redistribuição de memória: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de memória."""
        with self._lock:
            # Estatísticas por tipo de memória
            memory_type_stats = {}
            for memory_type, block_ids in self.memory_pools.items():
                total_size = sum(
                    self.memory_blocks[block_id].size_bytes 
                    for block_id in block_ids 
                    if block_id in self.memory_blocks
                )
                memory_type_stats[memory_type.value] = {
                    'blocks': len(block_ids),
                    'total_size': total_size,
                    'average_size': total_size // max(len(block_ids), 1)
                }
            
            # Estatísticas por fractal
            fractal_stats = {}
            for fractal_id, stats in self.fractal_memory.items():
                fractal_stats[fractal_id] = {
                    'used_memory': stats.used_memory,
                    'available_memory': stats.available_memory,
                    'memory_blocks': stats.memory_blocks,
                    'consciousness_level': float(stats.consciousness_level),
                    'compression_efficiency': stats.compression_efficiency
                }
            
            return {
                'system_memory': self.system_memory_info,
                'total_allocated': self.stats['total_allocated'],
                'max_total_memory': self.max_total_memory,
                'utilization_percent': (self.stats['total_allocated'] / self.max_total_memory) * 100,
                'consciousness_level': float(self.stats['consciousness_level']),
                'memory_types': memory_type_stats,
                'fractal_stats': fractal_stats,
                'compression_stats': {
                    'total_compressed': self.stats['total_compressed'],
                    'compression_savings': self.stats['compression_savings'],
                    'garbage_collections': self.stats['garbage_collections'],
                    'optimization_cycles': self.stats['optimization_cycles']
                }
            }
    
    def get_memory_recommendations(self) -> List[Dict[str, Any]]:
        """Retorna recomendações de otimização de memória."""
        recommendations = []
        
        try:
            with self._lock:
                # Verificar utilização geral
                utilization = (self.stats['total_allocated'] / self.max_total_memory) * 100
                
                if utilization > 90:
                    recommendations.append({
                        'type': 'critical',
                        'message': 'Utilização de memória crítica (>90%)',
                        'action': 'Liberar memória imediatamente',
                        'priority': 1
                    })
                elif utilization > 75:
                    recommendations.append({
                        'type': 'warning',
                        'message': 'Utilização de memória alta (>75%)',
                        'action': 'Considerar liberação de memória',
                        'priority': 2
                    })
                
                # Verificar fractais com baixa consciência
                for fractal_id, stats in self.fractal_memory.items():
                    if stats.consciousness_level < Decimal('0.3'):
                        recommendations.append({
                            'type': 'info',
                            'message': f'Fractal {fractal_id} com baixa consciência',
                            'action': 'Otimizar uso de memória do fractal',
                            'priority': 3
                        })
                
                # Verificar blocos não comprimidos
                uncompressed_blocks = sum(
                    1 for block in self.memory_blocks.values() 
                    if not block.is_compressed and block.priority != MemoryPriority.CRITICAL
                )
                
                if uncompressed_blocks > 50:
                    recommendations.append({
                        'type': 'info',
                        'message': f'{uncompressed_blocks} blocos não comprimidos',
                        'action': 'Aplicar compressão automática',
                        'priority': 4
                    })
                
        except Exception as e:
            logger.error(f"Erro ao gerar recomendações: {e}")
        
        return recommendations


# Instância global do gerenciador de memória distribuída
distributed_memory_manager = DistributedMemoryManager()
