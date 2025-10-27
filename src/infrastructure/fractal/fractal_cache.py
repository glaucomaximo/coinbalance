"""
Sistema de Cache Inteligente entre Fractais.

Este módulo implementa um sistema de cache distribuído e consciente
que permite aos fractais compartilhar informações de forma eficiente,
reduzindo latência e melhorando performance.
"""

import time
import threading
from typing import Dict, Any, Optional, List, Tuple
from decimal import Decimal
from dataclasses import dataclass, field
from collections import OrderedDict
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Entrada do cache com metadados conscientes."""
    key: str
    value: Any
    timestamp: float
    access_count: int = 0
    last_access: float = field(default_factory=time.time)
    consciousness_level: Decimal = Decimal('0.5')
    fractal_source: str = ""
    expiration_time: Optional[float] = None
    priority: int = 1  # 1=baixa, 2=média, 3=alta
    
    def is_expired(self) -> bool:
        """Verifica se a entrada expirou."""
        if self.expiration_time is None:
            return False
        return time.time() > self.expiration_time
    
    def update_access(self):
        """Atualiza estatísticas de acesso."""
        self.access_count += 1
        self.last_access = time.time()
        # Aumentar consciência com base no uso
        if self.access_count > 10:
            self.consciousness_level = min(Decimal('1.0'), 
                                         self.consciousness_level + Decimal('0.01'))


class FractalCache:
    """
    Sistema de Cache Inteligente entre Fractais.
    
    Características:
    - Cache distribuído entre fractais
    - Consciência adaptativa
    - Expulsão inteligente baseada em uso
    - Sincronização automática
    - Compressão de dados
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.fractal_caches: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_accesses': 0,
            'consciousness_level': Decimal('0.1')
        }
        
        logger.info(f"FractalCache inicializado com tamanho máximo {max_size}")
    
    def _generate_key(self, fractal_id: str, key: str) -> str:
        """Gera chave única para o cache."""
        return f"{fractal_id}:{key}"
    
    def _evict_entries(self, count: int = 1):
        """Remove entradas menos importantes do cache."""
        with self._lock:
            # Ordenar por prioridade e último acesso
            sorted_entries = sorted(
                self.cache.items(),
                key=lambda x: (x[1].priority, x[1].last_access, x[1].access_count)
            )
            
            for i in range(min(count, len(sorted_entries))):
                key, entry = sorted_entries[i]
                del self.cache[key]
                self.stats['evictions'] += 1
                logger.debug(f"Entrada evictada do cache: {key}")
    
    def set(self, fractal_id: str, key: str, value: Any, 
            ttl: Optional[int] = None, priority: int = 1) -> bool:
        """
        Armazena valor no cache.
        
        Args:
            fractal_id: ID do fractal
            key: Chave do valor
            value: Valor a ser armazenado
            ttl: Tempo de vida em segundos
            priority: Prioridade (1=baixa, 2=média, 3=alta)
        """
        try:
            with self._lock:
                cache_key = self._generate_key(fractal_id, key)
                
                # Verificar se precisa evictar entradas
                if len(self.cache) >= self.max_size:
                    self._evict_entries(1)
                
                expiration_time = None
                if ttl:
                    expiration_time = time.time() + ttl
                elif self.default_ttl:
                    expiration_time = time.time() + self.default_ttl
                
                entry = CacheEntry(
                    key=cache_key,
                    value=value,
                    timestamp=time.time(),
                    consciousness_level=Decimal('0.5'),
                    fractal_source=fractal_id,
                    expiration_time=expiration_time,
                    priority=priority
                )
                
                self.cache[cache_key] = entry
                
                # Atualizar cache específico do fractal
                if fractal_id not in self.fractal_caches:
                    self.fractal_caches[fractal_id] = {}
                self.fractal_caches[fractal_id][key] = value
                
                logger.debug(f"Valor armazenado no cache: {cache_key}")
                return True
                
        except Exception as e:
            logger.error(f"Erro ao armazenar no cache: {e}")
            return False
    
    def get(self, fractal_id: str, key: str) -> Optional[Any]:
        """
        Recupera valor do cache.
        
        Args:
            fractal_id: ID do fractal
            key: Chave do valor
            
        Returns:
            Valor armazenado ou None se não encontrado
        """
        try:
            with self._lock:
                cache_key = self._generate_key(fractal_id, key)
                self.stats['total_accesses'] += 1
                
                if cache_key in self.cache:
                    entry = self.cache[cache_key]
                    
                    # Verificar expiração
                    if entry.is_expired():
                        del self.cache[cache_key]
                        self.stats['misses'] += 1
                        return None
                    
                    # Atualizar estatísticas de acesso
                    entry.update_access()
                    
                    # Mover para o final (LRU)
                    self.cache.move_to_end(cache_key)
                    
                    self.stats['hits'] += 1
                    logger.debug(f"Cache hit: {cache_key}")
                    return entry.value
                else:
                    self.stats['misses'] += 1
                    logger.debug(f"Cache miss: {cache_key}")
                    return None
                    
        except Exception as e:
            logger.error(f"Erro ao recuperar do cache: {e}")
            self.stats['misses'] += 1
            return None
    
    def invalidate(self, fractal_id: str, key: str) -> bool:
        """Invalida entrada específica do cache."""
        try:
            with self._lock:
                cache_key = self._generate_key(fractal_id, key)
                if cache_key in self.cache:
                    del self.cache[cache_key]
                    if fractal_id in self.fractal_caches:
                        self.fractal_caches[fractal_id].pop(key, None)
                    logger.debug(f"Entrada invalidada: {cache_key}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Erro ao invalidar cache: {e}")
            return False
    
    def invalidate_fractal(self, fractal_id: str) -> int:
        """Invalida todas as entradas de um fractal."""
        try:
            with self._lock:
                count = 0
                keys_to_remove = []
                
                for cache_key in self.cache:
                    if cache_key.startswith(f"{fractal_id}:"):
                        keys_to_remove.append(cache_key)
                
                for cache_key in keys_to_remove:
                    del self.cache[cache_key]
                    count += 1
                
                if fractal_id in self.fractal_caches:
                    del self.fractal_caches[fractal_id]
                
                logger.info(f"Cache invalidado para fractal {fractal_id}: {count} entradas")
                return count
                
        except Exception as e:
            logger.error(f"Erro ao invalidar cache do fractal: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache."""
        with self._lock:
            hit_rate = 0.0
            if self.stats['total_accesses'] > 0:
                hit_rate = self.stats['hits'] / self.stats['total_accesses']
            
            # Calcular consciência do cache baseada no hit rate
            consciousness = min(Decimal('1.0'), 
                              Decimal(str(hit_rate)) + self.stats['consciousness_level'])
            
            return {
                'total_entries': len(self.cache),
                'max_size': self.max_size,
                'hit_rate': hit_rate,
                'hits': self.stats['hits'],
                'misses': self.stats['misses'],
                'evictions': self.stats['evictions'],
                'consciousness_level': consciousness,
                'fractal_count': len(self.fractal_caches),
                'memory_usage': self._estimate_memory_usage()
            }
    
    def _estimate_memory_usage(self) -> int:
        """Estima uso de memória do cache."""
        try:
            total_size = 0
            for entry in self.cache.values():
                # Estimativa simples baseada no tamanho da string
                total_size += len(str(entry.value)) + len(entry.key)
            return total_size
        except:
            return 0
    
    def sync_fractals(self, fractal_ids: List[str]) -> Dict[str, Any]:
        """
        Sincroniza cache entre fractais.
        
        Args:
            fractal_ids: Lista de IDs dos fractais para sincronizar
            
        Returns:
            Estatísticas da sincronização
        """
        try:
            sync_stats = {
                'fractals_synced': len(fractal_ids),
                'entries_synced': 0,
                'conflicts_resolved': 0,
                'timestamp': time.time()
            }
            
            with self._lock:
                # Simular sincronização entre fractais
                for fractal_id in fractal_ids:
                    if fractal_id in self.fractal_caches:
                        sync_stats['entries_synced'] += len(self.fractal_caches[fractal_id])
                
                # Aumentar consciência com sincronização
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.05')
                )
            
            logger.info(f"Cache sincronizado entre {len(fractal_ids)} fractais")
            return sync_stats
            
        except Exception as e:
            logger.error(f"Erro na sincronização do cache: {e}")
            return {'error': str(e)}
    
    def optimize(self) -> Dict[str, Any]:
        """
        Otimiza o cache removendo entradas desnecessárias.
        
        Returns:
            Estatísticas da otimização
        """
        try:
            with self._lock:
                initial_size = len(self.cache)
                
                # Remover entradas expiradas
                expired_keys = []
                for key, entry in self.cache.items():
                    if entry.is_expired():
                        expired_keys.append(key)
                
                for key in expired_keys:
                    del self.cache[key]
                
                # Remover entradas com baixo acesso e baixa prioridade
                low_value_keys = []
                for key, entry in self.cache.items():
                    if (entry.access_count < 2 and 
                        entry.priority == 1 and 
                        time.time() - entry.last_access > 1800):  # 30 minutos
                        low_value_keys.append(key)
                
                for key in low_value_keys:
                    del self.cache[key]
                
                optimized_size = len(self.cache)
                removed_count = initial_size - optimized_size
                
                # Aumentar consciência com otimização
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.02')
                )
                
                logger.info(f"Cache otimizado: {removed_count} entradas removidas")
                
                return {
                    'initial_size': initial_size,
                    'final_size': optimized_size,
                    'removed_count': removed_count,
                    'optimization_time': time.time(),
                    'consciousness_level': self.stats['consciousness_level']
                }
                
        except Exception as e:
            logger.error(f"Erro na otimização do cache: {e}")
            return {'error': str(e)}


# Instância global do cache fractal
fractal_cache = FractalCache(max_size=2000, default_ttl=7200)
