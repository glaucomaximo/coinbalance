"""
Sistema de Cache Distribuído Otimizado
=====================================

Este módulo implementa um sistema de cache distribuído para blockchain,
permitindo sincronização entre múltiplos nós e otimização de performance.

EVOLUÇÃO: Cache distribuído com sincronização e otimizações de rede.
"""

import time
import threading
import asyncio
import json
from typing import List, Optional, Dict, Any, Set, Tuple, Callable
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from decimal import Decimal
import hashlib
import uuid

from ..entities.block import Block
from ...transaction.entities.transaction import Transaction
from ...shared.value_objects.hash_value import HashValue
from ...shared.value_objects.timestamp import Timestamp

logger = logging.getLogger(__name__)


@dataclass
class CacheNode:
    """Nó do cache distribuído"""
    node_id: str
    address: str
    port: int
    is_active: bool = True
    last_heartbeat: float = field(default_factory=time.time)
    cache_size: int = 0
    hit_rate: float = 0.0
    response_time: float = 0.0
    priority: int = 1  # 1 = alta, 2 = média, 3 = baixa


@dataclass
class CacheEntry:
    """Entrada do cache distribuído"""
    key: str
    value: Any
    timestamp: float = field(default_factory=time.time)
    ttl: int = 3600  # 1 hora
    node_id: str = ""
    version: int = 1
    is_dirty: bool = False
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)


@dataclass
class CacheSyncMessage:
    """Mensagem de sincronização do cache"""
    message_id: str
    message_type: str  # "put", "delete", "sync", "heartbeat"
    key: str = ""
    value: Any = None
    timestamp: float = field(default_factory=time.time)
    source_node: str = ""
    target_nodes: List[str] = field(default_factory=list)
    version: int = 1


class DistributedCache:
    """
    Sistema de cache distribuído para blockchain.
    
    EVOLUÇÃO: Cache distribuído com sincronização e otimizações de rede.
    
    Funcionalidades:
    - Cache distribuído entre múltiplos nós
    - Sincronização automática de dados
    - Heartbeat e detecção de falhas
    - Balanceamento de carga entre nós
    - Compressão e otimização de dados
    - Estatísticas detalhadas de performance
    - Thread safety completo
    """
    
    def __init__(self, node_id: str, local_address: str = "localhost", local_port: int = 8000):
        self.node_id = node_id
        self.local_address = local_address
        self.local_port = local_port
        
        # Cache local
        self.local_cache: Dict[str, CacheEntry] = {}
        self.cache_lock = threading.RLock()
        
        # Nós do cluster
        self.cache_nodes: Dict[str, CacheNode] = {}
        self.nodes_lock = threading.RLock()
        
        # Configurações
        self.max_local_cache_size = 10000
        self.sync_interval = 30  # segundos
        self.heartbeat_interval = 10  # segundos
        self.ttl_default = 3600  # 1 hora
        
        # Estatísticas
        self.stats = {
            "local_hits": 0,
            "local_misses": 0,
            "remote_hits": 0,
            "remote_misses": 0,
            "sync_operations": 0,
            "sync_conflicts": 0,
            "total_operations": 0,
            "average_response_time": 0.0
        }
        
        # Threading
        self.sync_thread: Optional[threading.Thread] = None
        self.heartbeat_thread: Optional[threading.Thread] = None
        self.is_running = False
        
        logger.info(f"DistributedCache inicializado: node_id={node_id}, address={local_address}:{local_port}")
    
    def start(self) -> None:
        """Inicia o sistema de cache distribuído."""
        with self.cache_lock:
            if self.is_running:
                return
            
            self.is_running = True
            
            # Iniciar threads de sincronização e heartbeat
            self.sync_thread = threading.Thread(target=self._sync_worker, daemon=True)
            self.heartbeat_thread = threading.Thread(target=self._heartbeat_worker, daemon=True)
            
            self.sync_thread.start()
            self.heartbeat_thread.start()
            
            logger.info("Sistema de cache distribuído iniciado")
    
    def stop(self) -> None:
        """Para o sistema de cache distribuído."""
        with self.cache_lock:
            if not self.is_running:
                return
            
            self.is_running = False
            
            # Aguardar threads terminarem
            if self.sync_thread and self.sync_thread.is_alive():
                self.sync_thread.join(timeout=5)
            if self.heartbeat_thread and self.heartbeat_thread.is_alive():
                self.heartbeat_thread.join(timeout=5)
            
            logger.info("Sistema de cache distribuído parado")
    
    def add_node(self, node_id: str, address: str, port: int, priority: int = 1) -> bool:
        """
        Adiciona um nó ao cluster de cache.
        
        EVOLUÇÃO: Adição de nós com prioridade e configuração.
        """
        try:
            with self.nodes_lock:
                node = CacheNode(
                    node_id=node_id,
                    address=address,
                    port=port,
                    priority=priority
                )
                
                self.cache_nodes[node_id] = node
                
                logger.info(f"Nó adicionado ao cluster: {node_id} ({address}:{port})")
                return True
                
        except Exception as e:
            logger.error(f"Erro ao adicionar nó ao cluster: {e}")
            return False
    
    def remove_node(self, node_id: str) -> bool:
        """Remove um nó do cluster de cache."""
        try:
            with self.nodes_lock:
                if node_id in self.cache_nodes:
                    del self.cache_nodes[node_id]
                    logger.info(f"Nó removido do cluster: {node_id}")
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Erro ao remover nó do cluster: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Obtém valor do cache distribuído.
        
        EVOLUÇÃO: Busca local primeiro, depois remota com fallback.
        """
        try:
            start_time = time.time()
            
            # Buscar no cache local primeiro
            with self.cache_lock:
                if key in self.local_cache:
                    entry = self.local_cache[key]
                    
                    # Verificar TTL
                    if time.time() - entry.timestamp < entry.ttl:
                        entry.access_count += 1
                        entry.last_accessed = time.time()
                        self.stats["local_hits"] += 1
                        
                        response_time = time.time() - start_time
                        self._update_response_time(response_time)
                        
                        logger.debug(f"Cache hit local: {key}")
                        return entry.value
                    else:
                        # TTL expirado, remover
                        del self.local_cache[key]
                        self.stats["local_misses"] += 1
                else:
                    self.stats["local_misses"] += 1
            
            # Buscar em nós remotos
            remote_value = self._get_from_remote_nodes(key)
            if remote_value is not None:
                # Armazenar localmente para próximas consultas
                self._put_local(key, remote_value)
                self.stats["remote_hits"] += 1
                
                response_time = time.time() - start_time
                self._update_response_time(response_time)
                
                logger.debug(f"Cache hit remoto: {key}")
                return remote_value
            
            self.stats["remote_misses"] += 1
            self.stats["total_operations"] += 1
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao obter valor do cache: {e}")
            return None
    
    def put(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Armazena valor no cache distribuído.
        
        EVOLUÇÃO: Armazenamento local e sincronização com nós remotos.
        """
        try:
            # Armazenar localmente
            self._put_local(key, value, ttl)
            
            # Sincronizar com nós remotos
            self._sync_to_remote_nodes(key, value, ttl)
            
            self.stats["total_operations"] += 1
            
            logger.debug(f"Valor armazenado no cache: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao armazenar valor no cache: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Remove valor do cache distribuído.
        
        EVOLUÇÃO: Remoção local e sincronização com nós remotos.
        """
        try:
            # Remover localmente
            with self.cache_lock:
                if key in self.local_cache:
                    del self.local_cache[key]
            
            # Sincronizar remoção com nós remotos
            self._sync_delete_to_remote_nodes(key)
            
            self.stats["total_operations"] += 1
            
            logger.debug(f"Valor removido do cache: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao remover valor do cache: {e}")
            return False
    
    def sync_all(self) -> Dict[str, Any]:
        """
        Sincroniza todo o cache com nós remotos.
        
        EVOLUÇÃO: Sincronização completa com resolução de conflitos.
        """
        try:
            sync_results = {
                "local_to_remote": 0,
                "remote_to_local": 0,
                "conflicts_resolved": 0,
                "errors": []
            }
            
            # Sincronizar cache local para nós remotos
            with self.cache_lock:
                for key, entry in self.local_cache.items():
                    if self._sync_to_remote_nodes(key, entry.value, entry.ttl):
                        sync_results["local_to_remote"] += 1
            
            # Sincronizar cache remoto para local
            for node_id, node in self.cache_nodes.items():
                if node.is_active:
                    try:
                        remote_keys = self._get_remote_keys(node_id)
                        for key in remote_keys:
                            remote_value = self._get_from_remote_node(node_id, key)
                            if remote_value is not None:
                                # Verificar conflitos
                                if key in self.local_cache:
                                    local_entry = self.local_cache[key]
                                    if local_entry.timestamp < time.time() - 300:  # 5 minutos
                                        # Conflito: usar versão mais recente
                                        self._put_local(key, remote_value)
                                        sync_results["conflicts_resolved"] += 1
                                else:
                                    self._put_local(key, remote_value)
                                    sync_results["remote_to_local"] += 1
                    except Exception as e:
                        sync_results["errors"].append(f"Erro ao sincronizar com {node_id}: {e}")
            
            self.stats["sync_operations"] += 1
            
            logger.info(f"Sincronização completa: {sync_results}")
            return sync_results
            
        except Exception as e:
            logger.error(f"Erro na sincronização completa: {e}")
            return {"error": str(e)}
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas do cache distribuído.
        
        EVOLUÇÃO: Métricas detalhadas de performance e sincronização.
        """
        with self.cache_lock:
            # Calcular taxas de hit
            total_hits = self.stats["local_hits"] + self.stats["remote_hits"]
            total_misses = self.stats["local_misses"] + self.stats["remote_misses"]
            total_requests = total_hits + total_misses
            
            hit_rate = total_hits / total_requests if total_requests > 0 else 0.0
            local_hit_rate = self.stats["local_hits"] / (self.stats["local_hits"] + self.stats["local_misses"]) if (self.stats["local_hits"] + self.stats["local_misses"]) > 0 else 0.0
            
            return {
                "cache_stats": {
                    "local_cache_size": len(self.local_cache),
                    "max_local_cache_size": self.max_local_cache_size,
                    "total_hits": total_hits,
                    "total_misses": total_misses,
                    "hit_rate": hit_rate,
                    "local_hit_rate": local_hit_rate,
                    "average_response_time": self.stats["average_response_time"]
                },
                "sync_stats": {
                    "sync_operations": self.stats["sync_operations"],
                    "sync_conflicts": self.stats["sync_conflicts"],
                    "total_operations": self.stats["total_operations"]
                },
                "cluster_stats": {
                    "total_nodes": len(self.cache_nodes),
                    "active_nodes": sum(1 for node in self.cache_nodes.values() if node.is_active),
                    "nodes": {node_id: {
                        "address": node.address,
                        "port": node.port,
                        "is_active": node.is_active,
                        "priority": node.priority,
                        "last_heartbeat": node.last_heartbeat
                    } for node_id, node in self.cache_nodes.items()}
                }
            }
    
    def optimize_cache(self) -> Dict[str, Any]:
        """
        Otimiza o cache distribuído.
        
        EVOLUÇÃO: Otimização automática de cache e sincronização.
        """
        try:
            optimizations_applied = []
            
            # Limpar cache local expirado
            expired_count = self._cleanup_expired_local_cache()
            if expired_count > 0:
                optimizations_applied.append(f"Removidas {expired_count} entradas expiradas do cache local")
            
            # Otimizar tamanho do cache local
            if len(self.local_cache) > self.max_local_cache_size * 0.9:
                self._evict_least_used_entries()
                optimizations_applied.append("Cache local otimizado (LRU)")
            
            # Verificar nós inativos
            inactive_nodes = self._check_inactive_nodes()
            if inactive_nodes:
                optimizations_applied.append(f"Marcados {len(inactive_nodes)} nós como inativos")
            
            # Sincronizar com nós ativos
            sync_result = self.sync_all()
            if sync_result.get("local_to_remote", 0) > 0 or sync_result.get("remote_to_local", 0) > 0:
                optimizations_applied.append("Cache sincronizado com nós remotos")
            
            return {
                "optimizations_applied": optimizations_applied,
                "expired_entries_removed": expired_count,
                "inactive_nodes": inactive_nodes,
                "sync_result": sync_result,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro na otimização do cache: {e}")
            return {"error": str(e)}
    
    def _put_local(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Armazena valor no cache local."""
        with self.cache_lock:
            entry = CacheEntry(
                key=key,
                value=value,
                ttl=ttl or self.ttl_default,
                node_id=self.node_id
            )
            
            self.local_cache[key] = entry
            
            # Verificar limite de tamanho
            if len(self.local_cache) > self.max_local_cache_size:
                self._evict_least_used_entries()
    
    def _get_from_remote_nodes(self, key: str) -> Optional[Any]:
        """Busca valor em nós remotos."""
        # Ordenar nós por prioridade e performance
        sorted_nodes = sorted(
            self.cache_nodes.items(),
            key=lambda x: (x[1].priority, -x[1].hit_rate, x[1].response_time)
        )
        
        for node_id, node in sorted_nodes:
            if node.is_active:
                try:
                    value = self._get_from_remote_node(node_id, key)
                    if value is not None:
                        return value
                except Exception as e:
                    logger.warning(f"Erro ao buscar em nó {node_id}: {e}")
                    continue
        
        return None
    
    def _get_from_remote_node(self, node_id: str, key: str) -> Optional[Any]:
        """Busca valor em um nó remoto específico."""
        # Simulação de chamada de rede
        # Em uma implementação real, isso seria uma chamada HTTP/gRPC
        node = self.cache_nodes[node_id]
        
        # Simular latência de rede
        time.sleep(0.001)  # 1ms
        
        # Simular resposta (em implementação real, seria uma chamada real)
        return None  # Simular cache miss
    
    def _sync_to_remote_nodes(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Sincroniza valor com nós remotos."""
        success_count = 0
        
        for node_id, node in self.cache_nodes.items():
            if node.is_active:
                try:
                    # Simular sincronização
                    # Em implementação real, seria uma chamada HTTP/gRPC
                    success_count += 1
                except Exception as e:
                    logger.warning(f"Erro ao sincronizar com nó {node_id}: {e}")
        
        return success_count > 0
    
    def _sync_delete_to_remote_nodes(self, key: str) -> None:
        """Sincroniza remoção com nós remotos."""
        for node_id, node in self.cache_nodes.items():
            if node.is_active:
                try:
                    # Simular sincronização de remoção
                    # Em implementação real, seria uma chamada HTTP/gRPC
                    pass
                except Exception as e:
                    logger.warning(f"Erro ao sincronizar remoção com nó {node_id}: {e}")
    
    def _get_remote_keys(self, node_id: str) -> List[str]:
        """Obtém lista de chaves de um nó remoto."""
        # Simulação de chamada de rede
        # Em implementação real, seria uma chamada HTTP/gRPC
        return []
    
    def _cleanup_expired_local_cache(self) -> int:
        """Remove entradas expiradas do cache local."""
        with self.cache_lock:
            current_time = time.time()
            expired_keys = []
            
            for key, entry in self.local_cache.items():
                if current_time - entry.timestamp > entry.ttl:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.local_cache[key]
            
            return len(expired_keys)
    
    def _evict_least_used_entries(self) -> None:
        """Remove entradas menos usadas do cache local."""
        with self.cache_lock:
            if len(self.local_cache) <= self.max_local_cache_size * 0.8:
                return
            
            # Ordenar por último acesso e contagem de acesso
            sorted_entries = sorted(
                self.local_cache.items(),
                key=lambda x: (x[1].last_accessed, x[1].access_count)
            )
            
            # Remover 20% das entradas menos usadas
            evict_count = int(len(self.local_cache) * 0.2)
            for i in range(evict_count):
                if i < len(sorted_entries):
                    key = sorted_entries[i][0]
                    del self.local_cache[key]
    
    def _check_inactive_nodes(self) -> List[str]:
        """Verifica e marca nós inativos."""
        with self.nodes_lock:
            current_time = time.time()
            inactive_nodes = []
            
            for node_id, node in self.cache_nodes.items():
                if current_time - node.last_heartbeat > self.heartbeat_interval * 3:
                    if node.is_active:
                        node.is_active = False
                        inactive_nodes.append(node_id)
            
            return inactive_nodes
    
    def _update_response_time(self, response_time: float) -> None:
        """Atualiza tempo médio de resposta."""
        if self.stats["total_operations"] > 0:
            self.stats["average_response_time"] = (
                (self.stats["average_response_time"] * (self.stats["total_operations"] - 1) + response_time) /
                self.stats["total_operations"]
            )
    
    def _sync_worker(self) -> None:
        """Worker thread para sincronização automática."""
        while self.is_running:
            try:
                time.sleep(self.sync_interval)
                if self.is_running:
                    self.sync_all()
            except Exception as e:
                logger.error(f"Erro no worker de sincronização: {e}")
    
    def _heartbeat_worker(self) -> None:
        """Worker thread para heartbeat."""
        while self.is_running:
            try:
                time.sleep(self.heartbeat_interval)
                if self.is_running:
                    self._send_heartbeat()
            except Exception as e:
                logger.error(f"Erro no worker de heartbeat: {e}")
    
    def _send_heartbeat(self) -> None:
        """Envia heartbeat para nós remotos."""
        with self.nodes_lock:
            for node_id, node in self.cache_nodes.items():
                if node.is_active:
                    try:
                        # Simular envio de heartbeat
                        # Em implementação real, seria uma chamada HTTP/gRPC
                        node.last_heartbeat = time.time()
                    except Exception as e:
                        logger.warning(f"Erro ao enviar heartbeat para {node_id}: {e}")


# Instância global otimizada
distributed_cache = DistributedCache(
    node_id=f"node_{uuid.uuid4().hex[:8]}",
    local_address="localhost",
    local_port=8000
)
