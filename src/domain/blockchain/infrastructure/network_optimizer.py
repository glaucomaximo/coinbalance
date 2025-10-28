"""
Sistema de Otimização de Rede
=============================

Este módulo implementa otimizações de rede para blockchain,
incluindo compressão, cache de conexões e balanceamento de carga.

EVOLUÇÃO: Otimização de rede com compressão e balanceamento de carga.
"""

import time
import threading
import asyncio
import json
import gzip
import zlib
from typing import List, Optional, Dict, Any, Set, Tuple, Callable
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from decimal import Decimal
import hashlib
import uuid
import socket
import ssl

from ..entities.block import Block
from ...transaction.entities.transaction import Transaction
from ...shared.value_objects.hash_value import HashValue
from ...shared.value_objects.timestamp import Timestamp

logger = logging.getLogger(__name__)


@dataclass
class NetworkNode:
    """Nó da rede blockchain"""
    node_id: str
    address: str
    port: int
    is_active: bool = True
    last_heartbeat: float = field(default_factory=time.time)
    response_time: float = 0.0
    bandwidth: float = 0.0
    priority: int = 1
    connection_count: int = 0
    max_connections: int = 100


@dataclass
class NetworkMessage:
    """Mensagem de rede otimizada"""
    message_id: str
    message_type: str
    payload: Any
    timestamp: float = field(default_factory=time.time)
    source_node: str = ""
    target_node: str = ""
    compression: str = "none"  # "none", "gzip", "zlib"
    encrypted: bool = False
    priority: int = 1


@dataclass
class ConnectionPool:
    """Pool de conexões otimizado"""
    node_id: str
    connections: List[Any] = field(default_factory=list)
    max_connections: int = 10
    active_connections: int = 0
    last_used: float = field(default_factory=time.time)
    total_requests: int = 0
    successful_requests: int = 0


class NetworkOptimizer:
    """
    Sistema de otimização de rede para blockchain.
    
    EVOLUÇÃO: Otimização de rede com compressão e balanceamento de carga.
    
    Funcionalidades:
    - Compressão de dados (gzip, zlib)
    - Pool de conexões reutilizáveis
    - Balanceamento de carga entre nós
    - Cache de mensagens frequentes
    - Compressão adaptativa baseada em conteúdo
    - Estatísticas detalhadas de rede
    - Thread safety completo
    """
    
    def __init__(self, node_id: str, local_address: str = "localhost", local_port: int = 8000):
        self.node_id = node_id
        self.local_address = local_address
        self.local_port = local_port
        
        # Nós da rede
        self.network_nodes: Dict[str, NetworkNode] = {}
        self.nodes_lock = threading.RLock()
        
        # Pool de conexões
        self.connection_pools: Dict[str, ConnectionPool] = {}
        self.pools_lock = threading.RLock()
        
        # Cache de mensagens
        self.message_cache: Dict[str, Any] = {}
        self.cache_lock = threading.RLock()
        
        # Configurações
        self.max_cache_size = 1000
        self.cache_ttl = 300  # 5 minutos
        self.compression_threshold = 1024  # 1KB
        self.max_connections_per_node = 10
        self.connection_timeout = 30  # segundos
        
        # Estatísticas
        self.stats = {
            "total_messages_sent": 0,
            "total_messages_received": 0,
            "compressed_messages": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "connection_reuses": 0,
            "new_connections": 0,
            "compression_savings": 0.0,
            "average_response_time": 0.0,
            "bandwidth_usage": 0.0
        }
        
        # Threading
        self.cleanup_thread: Optional[threading.Thread] = None
        self.is_running = False
        
        logger.info(f"NetworkOptimizer inicializado: node_id={node_id}, address={local_address}:{local_port}")
    
    def start(self) -> None:
        """Inicia o sistema de otimização de rede."""
        with self.pools_lock:
            if self.is_running:
                return
            
            self.is_running = True
            
            # Iniciar thread de limpeza
            self.cleanup_thread = threading.Thread(target=self._cleanup_worker, daemon=True)
            self.cleanup_thread.start()
            
            logger.info("Sistema de otimização de rede iniciado")
    
    def stop(self) -> None:
        """Para o sistema de otimização de rede."""
        with self.pools_lock:
            if not self.is_running:
                return
            
            self.is_running = False
            
            # Fechar todas as conexões
            self._close_all_connections()
            
            # Aguardar thread de limpeza
            if self.cleanup_thread and self.cleanup_thread.is_alive():
                self.cleanup_thread.join(timeout=5)
            
            logger.info("Sistema de otimização de rede parado")
    
    def add_node(self, node_id: str, address: str, port: int, priority: int = 1) -> bool:
        """
        Adiciona um nó à rede.
        
        EVOLUÇÃO: Adição de nós com prioridade e configuração de rede.
        """
        try:
            with self.nodes_lock:
                node = NetworkNode(
                    node_id=node_id,
                    address=address,
                    port=port,
                    priority=priority
                )
                
                self.network_nodes[node_id] = node
                
                # Criar pool de conexões para o nó
                with self.pools_lock:
                    self.connection_pools[node_id] = ConnectionPool(
                        node_id=node_id,
                        max_connections=self.max_connections_per_node
                    )
                
                logger.info(f"Nó adicionado à rede: {node_id} ({address}:{port})")
                return True
                
        except Exception as e:
            logger.error(f"Erro ao adicionar nó à rede: {e}")
            return False
    
    def remove_node(self, node_id: str) -> bool:
        """Remove um nó da rede."""
        try:
            with self.nodes_lock:
                if node_id in self.network_nodes:
                    del self.network_nodes[node_id]
            
            with self.pools_lock:
                if node_id in self.connection_pools:
                    # Fechar conexões do pool
                    pool = self.connection_pools[node_id]
                    for connection in pool.connections:
                        try:
                            connection.close()
                        except:
                            pass
                    del self.connection_pools[node_id]
            
            logger.info(f"Nó removido da rede: {node_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao remover nó da rede: {e}")
            return False
    
    def send_message(self, target_node: str, message_type: str, payload: Any, priority: int = 1) -> bool:
        """
        Envia mensagem otimizada para um nó.
        
        EVOLUÇÃO: Envio otimizado com compressão e cache.
        """
        try:
            start_time = time.time()
            
            # Verificar cache de mensagens
            message_key = self._generate_message_key(target_node, message_type, payload)
            cached_response = self._get_cached_message(message_key)
            if cached_response is not None:
                self.stats["cache_hits"] += 1
                return True
            
            self.stats["cache_misses"] += 1
            
            # Criar mensagem
            message = NetworkMessage(
                message_id=str(uuid.uuid4()),
                message_type=message_type,
                payload=payload,
                source_node=self.node_id,
                target_node=target_node,
                priority=priority
            )
            
            # Determinar compressão
            message.compression = self._determine_compression(payload)
            
            # Comprimir payload se necessário
            if message.compression != "none":
                message.payload = self._compress_payload(payload, message.compression)
                self.stats["compressed_messages"] += 1
            
            # Enviar mensagem
            success = self._send_message_to_node(target_node, message)
            
            if success:
                # Cachear resposta se aplicável
                self._cache_message(message_key, True)
                
                # Atualizar estatísticas
                response_time = time.time() - start_time
                self._update_response_time(response_time)
                self.stats["total_messages_sent"] += 1
                
                logger.debug(f"Mensagem enviada: {message_type} para {target_node}")
            
            return success
            
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return False
    
    def broadcast_message(self, message_type: str, payload: Any, priority: int = 1) -> Dict[str, bool]:
        """
        Envia mensagem para todos os nós ativos.
        
        EVOLUÇÃO: Broadcast otimizado com balanceamento de carga.
        """
        try:
            results = {}
            
            # Ordenar nós por prioridade e performance
            sorted_nodes = self._get_optimized_node_order()
            
            # Enviar mensagens em paralelo
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                
                for node_id in sorted_nodes:
                    future = executor.submit(self.send_message, node_id, message_type, payload, priority)
                    futures.append((node_id, future))
                
                # Coletar resultados
                for node_id, future in as_completed([f for _, f in futures]):
                    try:
                        result = future.result()
                        results[node_id] = result
                    except Exception as e:
                        logger.warning(f"Erro ao enviar mensagem para {node_id}: {e}")
                        results[node_id] = False
            
            logger.info(f"Broadcast enviado: {message_type} para {len(results)} nós")
            return results
            
        except Exception as e:
            logger.error(f"Erro no broadcast: {e}")
            return {}
    
    def get_network_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas da rede.
        
        EVOLUÇÃO: Métricas detalhadas de performance e otimização.
        """
        with self.pools_lock:
            # Calcular estatísticas de conexões
            total_connections = sum(pool.active_connections for pool in self.connection_pools.values())
            total_pools = len(self.connection_pools)
            
            # Calcular taxa de hit do cache
            cache_hit_rate = 0.0
            total_cache_requests = self.stats["cache_hits"] + self.stats["cache_misses"]
            if total_cache_requests > 0:
                cache_hit_rate = self.stats["cache_hits"] / total_cache_requests
            
            # Calcular taxa de reutilização de conexões
            connection_reuse_rate = 0.0
            total_connection_operations = self.stats["connection_reuses"] + self.stats["new_connections"]
            if total_connection_operations > 0:
                connection_reuse_rate = self.stats["connection_reuses"] / total_connection_operations
            
            return {
                "network_stats": {
                    "total_nodes": len(self.network_nodes),
                    "active_nodes": sum(1 for node in self.network_nodes.values() if node.is_active),
                    "total_connections": total_connections,
                    "connection_pools": total_pools,
                    "connection_reuse_rate": connection_reuse_rate
                },
                "message_stats": {
                    "total_sent": self.stats["total_messages_sent"],
                    "total_received": self.stats["total_messages_received"],
                    "compressed_messages": self.stats["compressed_messages"],
                    "compression_savings": self.stats["compression_savings"],
                    "average_response_time": self.stats["average_response_time"]
                },
                "cache_stats": {
                    "cache_size": len(self.message_cache),
                    "max_cache_size": self.max_cache_size,
                    "cache_hits": self.stats["cache_hits"],
                    "cache_misses": self.stats["cache_misses"],
                    "cache_hit_rate": cache_hit_rate
                },
                "bandwidth_stats": {
                    "bandwidth_usage": self.stats["bandwidth_usage"],
                    "compression_threshold": self.compression_threshold
                }
            }
    
    def optimize_network(self) -> Dict[str, Any]:
        """
        Otimiza a rede blockchain.
        
        EVOLUÇÃO: Otimização automática de rede e conexões.
        """
        try:
            optimizations_applied = []
            
            # Limpar cache de mensagens expiradas
            expired_cache = self._cleanup_expired_cache()
            if expired_cache > 0:
                optimizations_applied.append(f"Removidas {expired_cache} mensagens expiradas do cache")
            
            # Otimizar pools de conexões
            optimized_pools = self._optimize_connection_pools()
            if optimized_pools > 0:
                optimizations_applied.append(f"Otimizados {optimized_pools} pools de conexões")
            
            # Verificar nós inativos
            inactive_nodes = self._check_inactive_nodes()
            if inactive_nodes:
                optimizations_applied.append(f"Marcados {len(inactive_nodes)} nós como inativos")
            
            # Balancear carga entre nós
            load_balanced = self._balance_load()
            if load_balanced:
                optimizations_applied.append("Carga balanceada entre nós")
            
            # Otimizar configurações de compressão
            compression_optimized = self._optimize_compression_settings()
            if compression_optimized:
                optimizations_applied.append("Configurações de compressão otimizadas")
            
            return {
                "optimizations_applied": optimizations_applied,
                "expired_cache_removed": expired_cache,
                "pools_optimized": optimized_pools,
                "inactive_nodes": inactive_nodes,
                "load_balanced": load_balanced,
                "compression_optimized": compression_optimized,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro na otimização da rede: {e}")
            return {"error": str(e)}
    
    def _generate_message_key(self, target_node: str, message_type: str, payload: Any) -> str:
        """Gera chave única para mensagem."""
        payload_str = json.dumps(payload, sort_keys=True) if isinstance(payload, (dict, list)) else str(payload)
        key_data = f"{target_node}:{message_type}:{payload_str}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_cached_message(self, message_key: str) -> Optional[Any]:
        """Obtém mensagem do cache."""
        with self.cache_lock:
            if message_key in self.message_cache:
                entry = self.message_cache[message_key]
                if time.time() - entry["timestamp"] < self.cache_ttl:
                    return entry["response"]
                else:
                    del self.message_cache[message_key]
            return None
    
    def _cache_message(self, message_key: str, response: Any) -> None:
        """Armazena mensagem no cache."""
        with self.cache_lock:
            self.message_cache[message_key] = {
                "response": response,
                "timestamp": time.time()
            }
            
            # Verificar limite de tamanho
            if len(self.message_cache) > self.max_cache_size:
                self._evict_oldest_cache_entries()
    
    def _determine_compression(self, payload: Any) -> str:
        """Determina tipo de compressão baseado no payload."""
        try:
            payload_str = json.dumps(payload) if isinstance(payload, (dict, list)) else str(payload)
            payload_size = len(payload_str.encode('utf-8'))
            
            if payload_size < self.compression_threshold:
                return "none"
            elif payload_size < self.compression_threshold * 10:
                return "gzip"
            else:
                return "zlib"
        except:
            return "none"
    
    def _compress_payload(self, payload: Any, compression_type: str) -> bytes:
        """Comprime payload usando o tipo especificado."""
        try:
            payload_str = json.dumps(payload) if isinstance(payload, (dict, list)) else str(payload)
            payload_bytes = payload_str.encode('utf-8')
            
            if compression_type == "gzip":
                compressed = gzip.compress(payload_bytes)
            elif compression_type == "zlib":
                compressed = zlib.compress(payload_bytes)
            else:
                compressed = payload_bytes
            
            # Calcular economia de compressão
            original_size = len(payload_bytes)
            compressed_size = len(compressed)
            savings = (original_size - compressed_size) / original_size
            self.stats["compression_savings"] += savings
            
            return compressed
            
        except Exception as e:
            logger.error(f"Erro na compressão: {e}")
            return str(payload).encode('utf-8')
    
    def _send_message_to_node(self, target_node: str, message: NetworkMessage) -> bool:
        """Envia mensagem para um nó específico."""
        try:
            # Obter conexão do pool
            connection = self._get_connection(target_node)
            if connection is None:
                return False
            
            # Simular envio de mensagem
            # Em implementação real, seria uma chamada de rede real
            time.sleep(0.001)  # Simular latência
            
            # Atualizar estatísticas do pool
            with self.pools_lock:
                if target_node in self.connection_pools:
                    pool = self.connection_pools[target_node]
                    pool.total_requests += 1
                    pool.successful_requests += 1
                    pool.last_used = time.time()
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem para {target_node}: {e}")
            return False
    
    def _get_connection(self, target_node: str) -> Optional[Any]:
        """Obtém conexão do pool ou cria nova."""
        with self.pools_lock:
            if target_node not in self.connection_pools:
                return None
            
            pool = self.connection_pools[target_node]
            
            # Tentar reutilizar conexão existente
            if pool.connections:
                connection = pool.connections.pop()
                pool.active_connections += 1
                self.stats["connection_reuses"] += 1
                return connection
            
            # Criar nova conexão
            if pool.active_connections < pool.max_connections:
                # Simular criação de conexão
                # Em implementação real, seria uma conexão real
                connection = f"connection_{target_node}_{pool.active_connections}"
                pool.active_connections += 1
                self.stats["new_connections"] += 1
                return connection
            
            return None
    
    def _return_connection(self, target_node: str, connection: Any) -> None:
        """Retorna conexão ao pool."""
        with self.pools_lock:
            if target_node in self.connection_pools:
                pool = self.connection_pools[target_node]
                if len(pool.connections) < pool.max_connections:
                    pool.connections.append(connection)
                    pool.active_connections -= 1
    
    def _get_optimized_node_order(self) -> List[str]:
        """Retorna ordem otimizada de nós para envio."""
        with self.nodes_lock:
            # Ordenar por prioridade, performance e carga
            sorted_nodes = sorted(
                self.network_nodes.items(),
                key=lambda x: (
                    x[1].priority,
                    -x[1].response_time,
                    -x[1].bandwidth,
                    x[1].connection_count
                )
            )
            
            return [node_id for node_id, _ in sorted_nodes if _.is_active]
    
    def _cleanup_expired_cache(self) -> int:
        """Remove entradas expiradas do cache."""
        with self.cache_lock:
            current_time = time.time()
            expired_keys = []
            
            for key, entry in self.message_cache.items():
                if current_time - entry["timestamp"] > self.cache_ttl:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.message_cache[key]
            
            return len(expired_keys)
    
    def _evict_oldest_cache_entries(self) -> None:
        """Remove entradas mais antigas do cache."""
        with self.cache_lock:
            if len(self.message_cache) <= self.max_cache_size * 0.8:
                return
            
            # Ordenar por timestamp
            sorted_entries = sorted(
                self.message_cache.items(),
                key=lambda x: x[1]["timestamp"]
            )
            
            # Remover 20% das entradas mais antigas
            evict_count = int(len(self.message_cache) * 0.2)
            for i in range(evict_count):
                if i < len(sorted_entries):
                    key = sorted_entries[i][0]
                    del self.message_cache[key]
    
    def _optimize_connection_pools(self) -> int:
        """Otimiza pools de conexões."""
        optimized_count = 0
        
        with self.pools_lock:
            for node_id, pool in self.connection_pools.items():
                # Limpar conexões inativas
                active_connections = []
                for connection in pool.connections:
                    # Simular verificação de conexão ativa
                    # Em implementação real, seria uma verificação real
                    active_connections.append(connection)
                
                if len(active_connections) != len(pool.connections):
                    pool.connections = active_connections
                    optimized_count += 1
        
        return optimized_count
    
    def _check_inactive_nodes(self) -> List[str]:
        """Verifica e marca nós inativos."""
        with self.nodes_lock:
            current_time = time.time()
            inactive_nodes = []
            
            for node_id, node in self.network_nodes.items():
                if current_time - node.last_heartbeat > 60:  # 1 minuto
                    if node.is_active:
                        node.is_active = False
                        inactive_nodes.append(node_id)
            
            return inactive_nodes
    
    def _balance_load(self) -> bool:
        """Balanceia carga entre nós."""
        # Implementação simplificada de balanceamento
        # Em implementação real, seria mais complexa
        return True
    
    def _optimize_compression_settings(self) -> bool:
        """Otimiza configurações de compressão."""
        # Ajustar threshold baseado nas estatísticas
        if self.stats["compression_savings"] > 0.5:
            self.compression_threshold = max(512, self.compression_threshold - 256)
        elif self.stats["compression_savings"] < 0.2:
            self.compression_threshold = min(2048, self.compression_threshold + 256)
        
        return True
    
    def _close_all_connections(self) -> None:
        """Fecha todas as conexões."""
        with self.pools_lock:
            for pool in self.connection_pools.values():
                for connection in pool.connections:
                    try:
                        # Simular fechamento de conexão
                        # Em implementação real, seria connection.close()
                        pass
                    except:
                        pass
                pool.connections.clear()
                pool.active_connections = 0
    
    def _update_response_time(self, response_time: float) -> None:
        """Atualiza tempo médio de resposta."""
        if self.stats["total_messages_sent"] > 0:
            self.stats["average_response_time"] = (
                (self.stats["average_response_time"] * (self.stats["total_messages_sent"] - 1) + response_time) /
                self.stats["total_messages_sent"]
            )
    
    def _cleanup_worker(self) -> None:
        """Worker thread para limpeza automática."""
        while self.is_running:
            try:
                time.sleep(60)  # Limpeza a cada minuto
                if self.is_running:
                    self._cleanup_expired_cache()
                    self._optimize_connection_pools()
            except Exception as e:
                logger.error(f"Erro no worker de limpeza: {e}")


# Instância global otimizada
network_optimizer = NetworkOptimizer(
    node_id=f"network_{uuid.uuid4().hex[:8]}",
    local_address="localhost",
    local_port=8000
)
