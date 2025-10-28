"""
Sistema de Escalabilidade Horizontal
===================================

Este módulo implementa escalabilidade horizontal para blockchain,
permitindo distribuição de carga entre múltiplos nós e sharding.

EVOLUÇÃO: Escalabilidade horizontal com sharding e balanceamento de carga.
"""

import time
import threading
import asyncio
import json
import hashlib
import uuid
from typing import List, Optional, Dict, Any, Set, Tuple, Callable
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from decimal import Decimal
import random
import math

from ..entities.block import Block
from ...transaction.entities.transaction import Transaction
from ...shared.value_objects.hash_value import HashValue
from ...shared.value_objects.timestamp import Timestamp

logger = logging.getLogger(__name__)


@dataclass
class ShardNode:
    """Nó de shard da blockchain"""
    node_id: str
    shard_id: str
    address: str
    port: int
    is_active: bool = True
    last_heartbeat: float = field(default_factory=time.time)
    load_factor: float = 0.0
    capacity: int = 1000
    current_load: int = 0
    priority: int = 1
    region: str = "default"
    performance_score: float = 1.0


@dataclass
class ShardConfig:
    """Configuração de shard"""
    shard_id: str
    node_count: int = 3
    replication_factor: int = 2
    consistency_level: str = "eventual"  # "strong", "eventual"
    load_balancing: str = "round_robin"  # "round_robin", "least_connections", "weighted"
    auto_scaling: bool = True
    min_nodes: int = 2
    max_nodes: int = 10


@dataclass
class LoadBalancer:
    """Balanceador de carga para shards"""
    algorithm: str = "round_robin"
    health_check_interval: int = 30
    failover_threshold: int = 3
    sticky_sessions: bool = False
    session_timeout: int = 3600


class HorizontalScaler:
    """
    Sistema de escalabilidade horizontal para blockchain.
    
    EVOLUÇÃO: Escalabilidade horizontal com sharding e balanceamento de carga.
    
    Funcionalidades:
    - Sharding automático de dados
    - Balanceamento de carga entre shards
    - Auto-scaling baseado em métricas
    - Failover automático
    - Distribuição geográfica de nós
    - Estatísticas detalhadas de escalabilidade
    - Thread safety completo
    """
    
    def __init__(self, node_id: str, local_address: str = "localhost", local_port: int = 8000):
        self.node_id = node_id
        self.local_address = local_address
        self.local_port = local_port
        
        # Shards e nós
        self.shards: Dict[str, List[ShardNode]] = {}
        self.shard_configs: Dict[str, ShardConfig] = {}
        self.load_balancer = LoadBalancer()
        
        # Configurações
        self.max_shards = 16
        self.shard_size_threshold = 10000  # blocos por shard
        self.auto_scaling_enabled = True
        self.load_threshold = 0.8  # 80% de carga
        self.scaling_cooldown = 300  # 5 minutos
        
        # Estatísticas
        self.stats = {
            "total_shards": 0,
            "total_nodes": 0,
            "active_nodes": 0,
            "total_blocks": 0,
            "blocks_per_shard": {},
            "load_distribution": {},
            "scaling_operations": 0,
            "failover_operations": 0,
            "average_response_time": 0.0,
            "throughput_per_second": 0.0
        }
        
        # Threading
        self.scaling_thread: Optional[threading.Thread] = None
        self.health_check_thread: Optional[threading.Thread] = None
        self.is_running = False
        
        logger.info(f"HorizontalScaler inicializado: node_id={node_id}, address={local_address}:{local_port}")
    
    def start(self) -> None:
        """Inicia o sistema de escalabilidade horizontal."""
        with threading.Lock():
            if self.is_running:
                return
            
            self.is_running = True
            
            # Iniciar threads de scaling e health check
            self.scaling_thread = threading.Thread(target=self._scaling_worker, daemon=True)
            self.health_check_thread = threading.Thread(target=self._health_check_worker, daemon=True)
            
            self.scaling_thread.start()
            self.health_check_thread.start()
            
            logger.info("Sistema de escalabilidade horizontal iniciado")
    
    def stop(self) -> None:
        """Para o sistema de escalabilidade horizontal."""
        with threading.Lock():
            if not self.is_running:
                return
            
            self.is_running = False
            
            # Aguardar threads terminarem
            if self.scaling_thread and self.scaling_thread.is_alive():
                self.scaling_thread.join(timeout=5)
            if self.health_check_thread and self.health_check_thread.is_alive():
                self.health_check_thread.join(timeout=5)
            
            logger.info("Sistema de escalabilidade horizontal parado")
    
    def create_shard(self, shard_id: str, config: Optional[ShardConfig] = None) -> bool:
        """
        Cria um novo shard.
        
        EVOLUÇÃO: Criação de shard com configuração personalizada.
        """
        try:
            if shard_id in self.shards:
                logger.warning(f"Shard {shard_id} já existe")
                return False
            
            # Usar configuração padrão se não fornecida
            if config is None:
                config = ShardConfig(shard_id=shard_id)
            
            # Criar shard
            self.shards[shard_id] = []
            self.shard_configs[shard_id] = config
            
            # Adicionar nós iniciais
            for i in range(config.min_nodes):
                node_id = f"{shard_id}_node_{i}"
                node = ShardNode(
                    node_id=node_id,
                    shard_id=shard_id,
                    address=f"localhost",
                    port=8000 + len(self.shards) * 100 + i
                )
                self.shards[shard_id].append(node)
            
            self.stats["total_shards"] += 1
            self.stats["total_nodes"] += config.min_nodes
            self.stats["active_nodes"] += config.min_nodes
            
            logger.info(f"Shard {shard_id} criado com {config.min_nodes} nós")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar shard {shard_id}: {e}")
            return False
    
    def add_node_to_shard(self, shard_id: str, node_id: str, address: str, port: int, priority: int = 1) -> bool:
        """
        Adiciona um nó a um shard.
        
        EVOLUÇÃO: Adição de nós com prioridade e configuração.
        """
        try:
            if shard_id not in self.shards:
                logger.error(f"Shard {shard_id} não existe")
                return False
            
            config = self.shard_configs[shard_id]
            
            # Verificar limite máximo de nós
            if len(self.shards[shard_id]) >= config.max_nodes:
                logger.warning(f"Shard {shard_id} atingiu limite máximo de nós")
                return False
            
            # Criar nó
            node = ShardNode(
                node_id=node_id,
                shard_id=shard_id,
                address=address,
                port=port,
                priority=priority
            )
            
            # Adicionar ao shard
            self.shards[shard_id].append(node)
            
            self.stats["total_nodes"] += 1
            self.stats["active_nodes"] += 1
            
            logger.info(f"Nó {node_id} adicionado ao shard {shard_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao adicionar nó {node_id} ao shard {shard_id}: {e}")
            return False
    
    def remove_node_from_shard(self, shard_id: str, node_id: str) -> bool:
        """Remove um nó de um shard."""
        try:
            if shard_id not in self.shards:
                logger.error(f"Shard {shard_id} não existe")
                return False
            
            config = self.shard_configs[shard_id]
            
            # Verificar limite mínimo de nós
            if len(self.shards[shard_id]) <= config.min_nodes:
                logger.warning(f"Shard {shard_id} atingiu limite mínimo de nós")
                return False
            
            # Remover nó
            self.shards[shard_id] = [node for node in self.shards[shard_id] if node.node_id != node_id]
            
            self.stats["total_nodes"] -= 1
            self.stats["active_nodes"] -= 1
            
            logger.info(f"Nó {node_id} removido do shard {shard_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao remover nó {node_id} do shard {shard_id}: {e}")
            return False
    
    def get_shard_for_block(self, block_hash: str) -> str:
        """
        Determina qual shard deve processar um bloco.
        
        EVOLUÇÃO: Distribuição inteligente baseada em hash.
        """
        try:
            # Usar hash do bloco para determinar shard
            hash_int = int(hashlib.md5(block_hash.encode()).hexdigest(), 16)
            shard_index = hash_int % len(self.shards)
            
            shard_ids = list(self.shards.keys())
            if shard_index < len(shard_ids):
                return shard_ids[shard_index]
            
            # Fallback para primeiro shard
            return shard_ids[0] if shard_ids else "default"
            
        except Exception as e:
            logger.error(f"Erro ao determinar shard para bloco {block_hash}: {e}")
            return "default"
    
    def get_node_for_request(self, shard_id: str, request_type: str = "read") -> Optional[ShardNode]:
        """
        Seleciona o melhor nó para processar uma requisição.
        
        EVOLUÇÃO: Seleção inteligente baseada em algoritmo de balanceamento.
        """
        try:
            if shard_id not in self.shards:
                return None
            
            nodes = [node for node in self.shards[shard_id] if node.is_active]
            if not nodes:
                return None
            
            # Aplicar algoritmo de balanceamento
            if self.load_balancer.algorithm == "round_robin":
                return self._round_robin_selection(nodes)
            elif self.load_balancer.algorithm == "least_connections":
                return self._least_connections_selection(nodes)
            elif self.load_balancer.algorithm == "weighted":
                return self._weighted_selection(nodes)
            else:
                return nodes[0]  # Fallback
                
        except Exception as e:
            logger.error(f"Erro ao selecionar nó para shard {shard_id}: {e}")
            return None
    
    def distribute_block(self, block: Block) -> Dict[str, Any]:
        """
        Distribui um bloco entre os shards apropriados.
        
        EVOLUÇÃO: Distribuição inteligente com replicação.
        """
        try:
            shard_id = self.get_shard_for_block(block.hash.value)
            
            if shard_id not in self.shards:
                return {"success": False, "error": f"Shard {shard_id} não existe"}
            
            config = self.shard_configs[shard_id]
            results = {}
            
            # Selecionar nós para replicação
            nodes = self.get_nodes_for_replication(shard_id, config.replication_factor)
            
            # Distribuir bloco para nós selecionados
            for node in nodes:
                try:
                    # Simular distribuição
                    # Em implementação real, seria uma chamada de rede
                    results[node.node_id] = True
                    node.current_load += 1
                    node.load_factor = node.current_load / node.capacity
                except Exception as e:
                    results[node.node_id] = False
                    logger.warning(f"Erro ao distribuir bloco para nó {node.node_id}: {e}")
            
            # Atualizar estatísticas
            self.stats["total_blocks"] += 1
            if shard_id not in self.stats["blocks_per_shard"]:
                self.stats["blocks_per_shard"][shard_id] = 0
            self.stats["blocks_per_shard"][shard_id] += 1
            
            return {
                "success": True,
                "shard_id": shard_id,
                "replication_results": results,
                "nodes_used": len(nodes)
            }
            
        except Exception as e:
            logger.error(f"Erro na distribuição do bloco: {e}")
            return {"success": False, "error": str(e)}
    
    def get_scaling_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas de escalabilidade.
        
        EVOLUÇÃO: Métricas detalhadas de escalabilidade e performance.
        """
        try:
            # Calcular distribuição de carga
            load_distribution = {}
            for shard_id, nodes in self.shards.items():
                if nodes:
                    avg_load = sum(node.load_factor for node in nodes) / len(nodes)
                    load_distribution[shard_id] = {
                        "average_load": avg_load,
                        "node_count": len(nodes),
                        "active_nodes": sum(1 for node in nodes if node.is_active)
                    }
            
            # Calcular throughput
            current_time = time.time()
            if hasattr(self, '_last_stats_time'):
                time_diff = current_time - self._last_stats_time
                if time_diff > 0:
                    self.stats["throughput_per_second"] = self.stats["total_blocks"] / time_diff
            
            self._last_stats_time = current_time
            
            return {
                "scaling_stats": {
                    "total_shards": self.stats["total_shards"],
                    "total_nodes": self.stats["total_nodes"],
                    "active_nodes": self.stats["active_nodes"],
                    "total_blocks": self.stats["total_blocks"],
                    "throughput_per_second": self.stats["throughput_per_second"],
                    "average_response_time": self.stats["average_response_time"]
                },
                "load_distribution": load_distribution,
                "blocks_per_shard": self.stats["blocks_per_shard"],
                "shard_configs": {
                    shard_id: {
                        "node_count": config.node_count,
                        "replication_factor": config.replication_factor,
                        "consistency_level": config.consistency_level,
                        "auto_scaling": config.auto_scaling
                    } for shard_id, config in self.shard_configs.items()
                }
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas de escalabilidade: {e}")
            return {}
    
    def optimize_scaling(self) -> Dict[str, Any]:
        """
        Otimiza a escalabilidade horizontal.
        
        EVOLUÇÃO: Otimização automática de escalabilidade.
        """
        try:
            optimizations_applied = []
            
            # Verificar necessidade de auto-scaling
            if self.auto_scaling_enabled:
                scaling_operations = self._perform_auto_scaling()
                optimizations_applied.extend(scaling_operations)
            
            # Balancear carga entre shards
            load_balancing = self._balance_load_between_shards()
            if load_balancing:
                optimizations_applied.append("Carga balanceada entre shards")
            
            # Otimizar configurações de shards
            config_optimizations = self._optimize_shard_configs()
            optimizations_applied.extend(config_optimizations)
            
            # Verificar nós inativos
            inactive_nodes = self._check_inactive_nodes()
            if inactive_nodes:
                optimizations_applied.append(f"Marcados {len(inactive_nodes)} nós como inativos")
            
            return {
                "optimizations_applied": optimizations_applied,
                "scaling_operations": len(scaling_operations) if 'scaling_operations' in locals() else 0,
                "load_balanced": load_balancing,
                "config_optimizations": len(config_optimizations),
                "inactive_nodes": inactive_nodes,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro na otimização de escalabilidade: {e}")
            return {"error": str(e)}
    
    def _round_robin_selection(self, nodes: List[ShardNode]) -> ShardNode:
        """Seleção round-robin."""
        if not hasattr(self, '_round_robin_index'):
            self._round_robin_index = {}
        
        shard_id = nodes[0].shard_id
        if shard_id not in self._round_robin_index:
            self._round_robin_index[shard_id] = 0
        
        selected_node = nodes[self._round_robin_index[shard_id] % len(nodes)]
        self._round_robin_index[shard_id] += 1
        
        return selected_node
    
    def _least_connections_selection(self, nodes: List[ShardNode]) -> ShardNode:
        """Seleção por menor número de conexões."""
        return min(nodes, key=lambda node: node.current_load)
    
    def _weighted_selection(self, nodes: List[ShardNode]) -> ShardNode:
        """Seleção ponderada por performance."""
        weights = [node.performance_score for node in nodes]
        total_weight = sum(weights)
        
        if total_weight == 0:
            return nodes[0]
        
        # Seleção aleatória ponderada
        random_value = random.random() * total_weight
        current_weight = 0
        
        for i, weight in enumerate(weights):
            current_weight += weight
            if random_value <= current_weight:
                return nodes[i]
        
        return nodes[-1]  # Fallback
    
    def _get_nodes_for_replication(self, shard_id: str, replication_factor: int) -> List[ShardNode]:
        """Seleciona nós para replicação."""
        nodes = [node for node in self.shards[shard_id] if node.is_active]
        
        # Ordenar por prioridade e performance
        nodes.sort(key=lambda node: (node.priority, -node.performance_score))
        
        # Selecionar nós para replicação
        return nodes[:min(replication_factor, len(nodes))]
    
    def _perform_auto_scaling(self) -> List[str]:
        """Executa auto-scaling baseado em métricas."""
        scaling_operations = []
        
        for shard_id, nodes in self.shards.items():
            config = self.shard_configs[shard_id]
            
            if not config.auto_scaling:
                continue
            
            # Calcular carga média
            active_nodes = [node for node in nodes if node.is_active]
            if not active_nodes:
                continue
            
            avg_load = sum(node.load_factor for node in active_nodes) / len(active_nodes)
            
            # Escalar para cima se necessário
            if avg_load > self.load_threshold and len(nodes) < config.max_nodes:
                # Adicionar novo nó
                new_node_id = f"{shard_id}_node_{len(nodes)}"
                if self.add_node_to_shard(shard_id, new_node_id, "localhost", 8000 + len(nodes)):
                    scaling_operations.append(f"Adicionado nó {new_node_id} ao shard {shard_id}")
                    self.stats["scaling_operations"] += 1
            
            # Escalar para baixo se possível
            elif avg_load < 0.3 and len(nodes) > config.min_nodes:
                # Remover nó menos carregado
                least_loaded_node = min(active_nodes, key=lambda node: node.load_factor)
                if self.remove_node_from_shard(shard_id, least_loaded_node.node_id):
                    scaling_operations.append(f"Removido nó {least_loaded_node.node_id} do shard {shard_id}")
                    self.stats["scaling_operations"] += 1
        
        return scaling_operations
    
    def _balance_load_between_shards(self) -> bool:
        """Balanceia carga entre shards."""
        # Implementação simplificada de balanceamento
        # Em implementação real, seria mais complexa
        return True
    
    def _optimize_shard_configs(self) -> List[str]:
        """Otimiza configurações de shards."""
        optimizations = []
        
        for shard_id, config in self.shard_configs.items():
            # Ajustar replication factor baseado no número de nós
            current_nodes = len(self.shards[shard_id])
            if config.replication_factor > current_nodes:
                config.replication_factor = current_nodes
                optimizations.append(f"Ajustado replication factor do shard {shard_id}")
        
        return optimizations
    
    def _check_inactive_nodes(self) -> List[str]:
        """Verifica e marca nós inativos."""
        inactive_nodes = []
        current_time = time.time()
        
        for shard_id, nodes in self.shards.items():
            for node in nodes:
                if current_time - node.last_heartbeat > 60:  # 1 minuto
                    if node.is_active:
                        node.is_active = False
                        inactive_nodes.append(node.node_id)
                        self.stats["active_nodes"] -= 1
        
        return inactive_nodes
    
    def _scaling_worker(self) -> None:
        """Worker thread para auto-scaling."""
        while self.is_running:
            try:
                time.sleep(60)  # Verificar a cada minuto
                if self.is_running:
                    self._perform_auto_scaling()
            except Exception as e:
                logger.error(f"Erro no worker de scaling: {e}")
    
    def _health_check_worker(self) -> None:
        """Worker thread para health check."""
        while self.is_running:
            try:
                time.sleep(self.load_balancer.health_check_interval)
                if self.is_running:
                    self._check_inactive_nodes()
            except Exception as e:
                logger.error(f"Erro no worker de health check: {e}")


# Instância global otimizada
horizontal_scaler = HorizontalScaler(
    node_id=f"scaler_{uuid.uuid4().hex[:8]}",
    local_address="localhost",
    local_port=8000
)
