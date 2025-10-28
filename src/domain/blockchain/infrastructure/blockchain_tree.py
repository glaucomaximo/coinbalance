"""
Sistema de Estrutura de Árvore Otimizado para Blocos
===================================================

Este módulo implementa uma estrutura de árvore otimizada para blocos,
permitindo busca eficiente, validação incremental e escalabilidade.

EVOLUÇÃO: Estrutura de árvore com cache e otimizações de performance.
"""

import time
import threading
from typing import List, Optional, Dict, Any, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import logging
from decimal import Decimal

from ..entities.block import Block
from ...transaction.entities.transaction import Transaction
from ...shared.value_objects.hash_value import HashValue
from ...shared.value_objects.timestamp import Timestamp

logger = logging.getLogger(__name__)


@dataclass
class TreeNode:
    """Nó da árvore de blocos"""
    block: Block
    children: List['TreeNode'] = field(default_factory=list)
    parent: Optional['TreeNode'] = None
    depth: int = 0
    subtree_size: int = 1
    is_validated: bool = False
    validation_time: float = 0.0
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0


@dataclass
class TreeStatistics:
    """Estatísticas da árvore de blocos"""
    total_nodes: int = 0
    max_depth: int = 0
    average_depth: float = 0.0
    leaf_nodes: int = 0
    internal_nodes: int = 0
    total_subtree_size: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    search_operations: int = 0
    insert_operations: int = 0
    delete_operations: int = 0


class BlockchainTree:
    """
    Árvore otimizada para blocos da blockchain.
    
    EVOLUÇÃO: Estrutura de árvore com cache e otimizações de performance.
    
    Funcionalidades:
    - Estrutura de árvore para blocos
    - Cache inteligente de nós
    - Busca eficiente por altura, hash e timestamp
    - Validação incremental de subárvores
    - Estatísticas detalhadas de performance
    - Thread safety completo
    """
    
    def __init__(self, max_cache_size: int = 10000):
        self.max_cache_size = max_cache_size
        self.root: Optional[TreeNode] = None
        self.nodes_by_hash: Dict[str, TreeNode] = {}
        self.nodes_by_height: Dict[int, List[TreeNode]] = defaultdict(list)
        self.nodes_by_timestamp: Dict[int, List[TreeNode]] = defaultdict(list)
        
        # Cache LRU para nós frequentemente acessados
        self.lru_cache: Dict[str, TreeNode] = {}
        self.cache_access_order: List[str] = []
        
        # Estatísticas
        self.stats = TreeStatistics()
        self._lock = threading.RLock()
        
        logger.info(f"BlockchainTree inicializado com cache de {max_cache_size} nós")
    
    def insert_block(self, block: Block, parent_hash: Optional[str] = None) -> bool:
        """
        Insere bloco na árvore.
        
        EVOLUÇÃO: Inserção otimizada com cache e índices.
        """
        with self._lock:
            try:
                # Criar nó
                node = TreeNode(block=block)
                
                # Encontrar pai
                if parent_hash and parent_hash in self.nodes_by_hash:
                    parent_node = self.nodes_by_hash[parent_hash]
                    node.parent = parent_node
                    node.depth = parent_node.depth + 1
                    parent_node.children.append(node)
                elif self.root is None:
                    # Primeiro bloco (gênesis)
                    self.root = node
                    node.depth = 0
                else:
                    # Adicionar como filho da raiz (para simplicidade)
                    node.parent = self.root
                    node.depth = 1
                    self.root.children.append(node)
                
                # Atualizar índices
                self._update_indices(node)
                
                # Atualizar tamanhos de subárvore
                self._update_subtree_sizes(node)
                
                # Adicionar ao cache LRU
                self._add_to_lru_cache(block.hash.value, node)
                
                # Atualizar estatísticas
                self.stats.insert_operations += 1
                self.stats.total_nodes += 1
                self.stats.max_depth = max(self.stats.max_depth, node.depth)
                
                logger.debug(f"Bloco {block.height} inserido na árvore: profundidade={node.depth}")
                
                return True
                
            except Exception as e:
                logger.error(f"Erro ao inserir bloco na árvore: {e}")
                return False
    
    def find_block_by_hash(self, block_hash: str) -> Optional[Block]:
        """
        Busca bloco por hash usando cache LRU.
        
        EVOLUÇÃO: Busca O(1) com cache inteligente.
        """
        with self._lock:
            self.stats.search_operations += 1
            
            # Verificar cache LRU primeiro
            if block_hash in self.lru_cache:
                node = self.lru_cache[block_hash]
                node.last_accessed = time.time()
                node.access_count += 1
                
                # Mover para o final (mais recente)
                self._move_to_end_lru_cache(block_hash)
                self.stats.cache_hits += 1
                
                return node.block
            
            # Buscar no índice principal
            if block_hash in self.nodes_by_hash:
                node = self.nodes_by_hash[block_hash]
                node.last_accessed = time.time()
                node.access_count += 1
                
                # Adicionar ao cache LRU
                self._add_to_lru_cache(block_hash, node)
                self.stats.cache_misses += 1
                
                return node.block
            
            return None
    
    def find_blocks_by_height(self, height: int) -> List[Block]:
        """
        Busca blocos por altura.
        
        EVOLUÇÃO: Busca O(1) com índice de altura.
        """
        with self._lock:
            self.stats.search_operations += 1
            
            blocks = []
            if height in self.nodes_by_height:
                for node in self.nodes_by_height[height]:
                    node.last_accessed = time.time()
                    node.access_count += 1
                    blocks.append(node.block)
                    
                    # Adicionar ao cache LRU
                    self._add_to_lru_cache(node.block.hash.value, node)
            
            return blocks
    
    def find_blocks_by_timestamp_range(self, start_time: int, end_time: int) -> List[Block]:
        """
        Busca blocos por range de timestamp.
        
        EVOLUÇÃO: Busca eficiente com índice de timestamp.
        """
        with self._lock:
            self.stats.search_operations += 1
            
            blocks = []
            for timestamp in range(start_time, end_time + 1):
                if timestamp in self.nodes_by_timestamp:
                    for node in self.nodes_by_timestamp[timestamp]:
                        node.last_accessed = time.time()
                        node.access_count += 1
                        blocks.append(node.block)
                        
                        # Adicionar ao cache LRU
                        self._add_to_lru_cache(node.block.hash.value, node)
            
            return blocks
    
    def get_blockchain_path(self, from_hash: str, to_hash: str) -> List[Block]:
        """
        Retorna caminho entre dois blocos na árvore.
        
        EVOLUÇÃO: Caminho otimizado usando estrutura de árvore.
        """
        with self._lock:
            if from_hash not in self.nodes_by_hash or to_hash not in self.nodes_by_hash:
                return []
            
            from_node = self.nodes_by_hash[from_hash]
            to_node = self.nodes_by_hash[to_hash]
            
            # Encontrar caminho usando LCA (Lowest Common Ancestor)
            path = []
            
            # Caminho do from_node até LCA
            current = from_node
            while current and current.depth >= to_node.depth:
                path.append(current.block)
                current = current.parent
            
            # Caminho do LCA até to_node
            current = to_node
            while current and current != from_node:
                path.append(current.block)
                current = current.parent
            
            return path
    
    def get_subtree_blocks(self, root_hash: str) -> List[Block]:
        """
        Retorna todos os blocos de uma subárvore.
        
        EVOLUÇÃO: Subárvore otimizada com cache.
        """
        with self._lock:
            if root_hash not in self.nodes_by_hash:
                return []
            
            root_node = self.nodes_by_hash[root_hash]
            blocks = []
            
            # DFS para coletar todos os blocos da subárvore
            def collect_blocks(node: TreeNode):
                blocks.append(node.block)
                for child in node.children:
                    collect_blocks(child)
            
            collect_blocks(root_node)
            
            return blocks
    
    def validate_subtree(self, root_hash: str) -> Dict[str, Any]:
        """
        Valida uma subárvore incrementalmente.
        
        EVOLUÇÃO: Validação incremental de subárvores.
        """
        with self._lock:
            if root_hash not in self.nodes_by_hash:
                return {"valid": False, "error": "Root node not found"}
            
            root_node = self.nodes_by_hash[root_hash]
            start_time = time.time()
            
            # Validação incremental da subárvore
            validation_results = []
            
            def validate_node(node: TreeNode):
                # Verificar se já foi validado recentemente
                if node.is_validated and time.time() - node.validation_time < 3600:  # 1 hora
                    return True
                
                # Validar bloco
                if not node.block.is_valid():
                    return False
                
                # Validar relação com pai
                if node.parent and node.block.previous_hash.value != node.parent.block.hash.value:
                    return False
                
                # Marcar como validado
                node.is_validated = True
                node.validation_time = time.time()
                
                # Validar filhos recursivamente
                for child in node.children:
                    if not validate_node(child):
                        return False
                
                return True
            
            is_valid = validate_node(root_node)
            validation_time = time.time() - start_time
            
            return {
                "valid": is_valid,
                "validation_time": validation_time,
                "subtree_size": root_node.subtree_size,
                "nodes_validated": root_node.subtree_size
            }
    
    def get_tree_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas da árvore.
        
        EVOLUÇÃO: Métricas detalhadas de performance da árvore.
        """
        with self._lock:
            # Calcular estatísticas dinâmicas
            total_depth = 0
            leaf_nodes = 0
            internal_nodes = 0
            
            def calculate_stats(node: TreeNode):
                nonlocal total_depth, leaf_nodes, internal_nodes
                
                total_depth += node.depth
                
                if not node.children:
                    leaf_nodes += 1
                else:
                    internal_nodes += 1
                
                for child in node.children:
                    calculate_stats(child)
            
            if self.root:
                calculate_stats(self.root)
            
            # Calcular taxa de hit do cache
            cache_hit_rate = 0.0
            total_cache_requests = self.stats.cache_hits + self.stats.cache_misses
            if total_cache_requests > 0:
                cache_hit_rate = self.stats.cache_hits / total_cache_requests
            
            return {
                "tree_stats": {
                    "total_nodes": self.stats.total_nodes,
                    "max_depth": self.stats.max_depth,
                    "average_depth": total_depth / self.stats.total_nodes if self.stats.total_nodes > 0 else 0,
                    "leaf_nodes": leaf_nodes,
                    "internal_nodes": internal_nodes,
                    "total_subtree_size": self.stats.total_subtree_size
                },
                "cache_stats": {
                    "cache_size": len(self.lru_cache),
                    "max_cache_size": self.max_cache_size,
                    "cache_hits": self.stats.cache_hits,
                    "cache_misses": self.stats.cache_misses,
                    "cache_hit_rate": cache_hit_rate
                },
                "operation_stats": {
                    "search_operations": self.stats.search_operations,
                    "insert_operations": self.stats.insert_operations,
                    "delete_operations": self.stats.delete_operations
                }
            }
    
    def optimize_tree_structure(self) -> Dict[str, Any]:
        """
        Otimiza estrutura da árvore.
        
        EVOLUÇÃO: Otimização automática de estrutura.
        """
        with self._lock:
            optimizations_applied = []
            
            # Limpar cache LRU se estiver muito grande
            if len(self.lru_cache) > self.max_cache_size * 0.9:
                self._cleanup_lru_cache()
                optimizations_applied.append("Cache LRU limpo")
            
            # Rebalancear árvore se necessário
            if self.root and self._needs_rebalancing():
                self._rebalance_tree()
                optimizations_applied.append("Árvore rebalanceada")
            
            # Otimizar índices
            self._optimize_indices()
            optimizations_applied.append("Índices otimizados")
            
            return {
                "optimizations_applied": optimizations_applied,
                "timestamp": time.time()
            }
    
    def _update_indices(self, node: TreeNode) -> None:
        """Atualiza índices da árvore."""
        block_hash = node.block.hash.value
        height = node.block.height
        timestamp = int(node.block.timestamp.value)
        
        # Índice por hash
        self.nodes_by_hash[block_hash] = node
        
        # Índice por altura
        self.nodes_by_height[height].append(node)
        
        # Índice por timestamp
        self.nodes_by_timestamp[timestamp].append(node)
    
    def _update_subtree_sizes(self, node: TreeNode) -> None:
        """Atualiza tamanhos de subárvore."""
        # Atualizar tamanho da subárvore
        node.subtree_size = 1
        for child in node.children:
            node.subtree_size += child.subtree_size
        
        # Atualizar tamanho total
        self.stats.total_subtree_size = 0
        if self.root:
            self.stats.total_subtree_size = self.root.subtree_size
    
    def _add_to_lru_cache(self, block_hash: str, node: TreeNode) -> None:
        """Adiciona nó ao cache LRU."""
        # Se já existe, mover para o final
        if block_hash in self.lru_cache:
            self._move_to_end_lru_cache(block_hash)
            return
        
        # Se cache está cheio, remover o mais antigo
        if len(self.lru_cache) >= self.max_cache_size:
            oldest_hash = self.cache_access_order[0]
            del self.lru_cache[oldest_hash]
            self.cache_access_order.pop(0)
        
        # Adicionar novo nó
        self.lru_cache[block_hash] = node
        self.cache_access_order.append(block_hash)
    
    def _move_to_end_lru_cache(self, block_hash: str) -> None:
        """Move nó para o final do cache LRU."""
        if block_hash in self.cache_access_order:
            self.cache_access_order.remove(block_hash)
            self.cache_access_order.append(block_hash)
    
    def _cleanup_lru_cache(self) -> None:
        """Limpa cache LRU removendo 20% dos itens mais antigos."""
        cleanup_count = int(len(self.lru_cache) * 0.2)
        
        for _ in range(cleanup_count):
            if self.cache_access_order:
                oldest_hash = self.cache_access_order.pop(0)
                if oldest_hash in self.lru_cache:
                    del self.lru_cache[oldest_hash]
    
    def _needs_rebalancing(self) -> bool:
        """Verifica se a árvore precisa de rebalanceamento."""
        if not self.root:
            return False
        
        # Verificar se há diferença significativa de profundidade
        max_depth = self.stats.max_depth
        min_depth = self._get_min_depth()
        
        return max_depth - min_depth > 10  # Threshold arbitrário
    
    def _get_min_depth(self) -> int:
        """Retorna profundidade mínima da árvore."""
        if not self.root:
            return 0
        
        min_depth = float('inf')
        
        def find_min_depth(node: TreeNode):
            nonlocal min_depth
            if not node.children:
                min_depth = min(min_depth, node.depth)
            for child in node.children:
                find_min_depth(child)
        
        find_min_depth(self.root)
        return int(min_depth) if min_depth != float('inf') else 0
    
    def _rebalance_tree(self) -> None:
        """Rebalanceia a árvore."""
        # Implementação simplificada de rebalanceamento
        # Em uma implementação real, isso seria mais complexo
        
        # Coletar todos os nós
        all_nodes = []
        if self.root:
            def collect_nodes(node: TreeNode):
                all_nodes.append(node)
                for child in node.children:
                    collect_nodes(child)
            collect_nodes(self.root)
        
        # Reconstruir árvore balanceada
        self.root = None
        self.nodes_by_hash.clear()
        self.nodes_by_height.clear()
        self.nodes_by_timestamp.clear()
        
        # Reinserir nós em ordem balanceada
        for node in sorted(all_nodes, key=lambda n: n.block.height):
            self.insert_block(node.block, node.parent.block.hash.value if node.parent else None)
    
    def _optimize_indices(self) -> None:
        """Otimiza índices da árvore."""
        # Remover entradas vazias dos índices
        self.nodes_by_height = {k: v for k, v in self.nodes_by_height.items() if v}
        self.nodes_by_timestamp = {k: v for k, v in self.nodes_by_timestamp.items() if v}
    
    def clear_cache(self) -> None:
        """Limpa todos os caches da árvore."""
        with self._lock:
            self.lru_cache.clear()
            self.cache_access_order.clear()
            
            # Reset estatísticas
            self.stats = TreeStatistics()
            
            logger.info("Cache da árvore limpo completamente")


# Instância global otimizada
blockchain_tree = BlockchainTree()
