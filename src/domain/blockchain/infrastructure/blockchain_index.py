"""
BlockchainIndex - Sistema de Índices Otimizado para Blockchain
============================================================

Este módulo implementa índices otimizados para busca rápida de blocos,
cache de validações e otimização de performance da blockchain.

EVOLUÇÃO: Implementação de estrutura de dados otimizada para performance.
"""

import time
import threading
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import OrderedDict
import logging
from decimal import Decimal

from ..entities.block import Block
from ...transaction.entities.transaction import Transaction

logger = logging.getLogger(__name__)


@dataclass
class IndexEntry:
    """Entrada no índice com metadados"""
    block: Block
    validation_status: bool = False
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0


class BlockchainIndex:
    """
    Sistema de índices otimizado para blockchain.
    
    EVOLUÇÃO: Implementação de busca O(1) e cache inteligente.
    
    Funcionalidades:
    - Busca O(1) por hash de bloco
    - Busca O(1) por altura de bloco
    - Cache de validações
    - Cache LRU para blocos frequentemente acessados
    - Estatísticas de acesso
    """
    
    def __init__(self, max_cache_size: int = 10000):
        self.max_cache_size = max_cache_size
        
        # Índices principais
        self.hash_to_block: Dict[str, IndexEntry] = {}
        self.height_to_block: Dict[int, IndexEntry] = {}
        
        # Cache LRU para blocos frequentemente acessados
        self.lru_cache: OrderedDict[str, IndexEntry] = OrderedDict()
        
        # Cache de validações
        self.validation_cache: Dict[str, bool] = {}
        self.validation_timestamps: Dict[str, float] = {}
        self.validation_ttl: int = 3600  # 1 hora
        
        # Estatísticas
        self.stats = {
            "hash_lookups": 0,
            "height_lookups": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "validations_cached": 0,
            "validations_computed": 0
        }
        
        # Thread safety
        self._lock = threading.RLock()
        
        logger.info(f"BlockchainIndex inicializado com cache de {max_cache_size} blocos")
    
    def add_block(self, block: Block) -> None:
        """
        Adiciona bloco ao índice.
        
        EVOLUÇÃO: Adição otimizada com cache LRU.
        """
        with self._lock:
            try:
                # Criar entrada do índice
                entry = IndexEntry(block=block)
                
                # Adicionar aos índices principais
                self.hash_to_block[block.hash.value] = entry
                self.height_to_block[block.height] = entry
                
                # Adicionar ao cache LRU
                self._add_to_lru_cache(block.hash.value, entry)
                
                logger.debug(f"Bloco {block.height} adicionado ao índice")
                
            except Exception as e:
                logger.error(f"Erro ao adicionar bloco ao índice: {e}")
                raise
    
    def get_block_by_hash(self, block_hash: str) -> Optional[Block]:
        """
        Busca bloco por hash com cache LRU.
        
        EVOLUÇÃO: Busca O(1) com cache inteligente.
        """
        with self._lock:
            self.stats["hash_lookups"] += 1
            
            # Verificar cache LRU primeiro
            if block_hash in self.lru_cache:
                entry = self.lru_cache[block_hash]
                entry.last_accessed = time.time()
                entry.access_count += 1
                
                # Mover para o final (mais recente)
                self.lru_cache.move_to_end(block_hash)
                self.stats["cache_hits"] += 1
                
                return entry.block
            
            # Buscar no índice principal
            if block_hash in self.hash_to_block:
                entry = self.hash_to_block[block_hash]
                entry.last_accessed = time.time()
                entry.access_count += 1
                
                # Adicionar ao cache LRU
                self._add_to_lru_cache(block_hash, entry)
                self.stats["cache_misses"] += 1
                
                return entry.block
            
            return None
    
    def get_block_by_height(self, height: int) -> Optional[Block]:
        """
        Busca bloco por altura com cache LRU.
        
        EVOLUÇÃO: Busca O(1) com cache inteligente.
        """
        with self._lock:
            self.stats["height_lookups"] += 1
            
            # Buscar no índice de altura
            if height in self.height_to_block:
                entry = self.height_to_block[height]
                entry.last_accessed = time.time()
                entry.access_count += 1
                
                # Adicionar ao cache LRU
                self._add_to_lru_cache(entry.block.hash.value, entry)
                
                return entry.block
            
            return None
    
    def is_block_validated(self, block_hash: str) -> Optional[bool]:
        """
        Verifica se bloco já foi validado (com cache).
        
        EVOLUÇÃO: Cache de validações para evitar recálculos.
        """
        with self._lock:
            # Verificar cache de validação
            if block_hash in self.validation_cache:
                # Verificar TTL
                if time.time() - self.validation_timestamps[block_hash] < self.validation_ttl:
                    self.stats["validations_cached"] += 1
                    return self.validation_cache[block_hash]
                else:
                    # Cache expirado, remover
                    del self.validation_cache[block_hash]
                    del self.validation_timestamps[block_hash]
            
            return None
    
    def cache_validation(self, block_hash: str, is_valid: bool) -> None:
        """
        Cache resultado de validação.
        
        EVOLUÇÃO: Cache inteligente de validações.
        """
        with self._lock:
            self.validation_cache[block_hash] = is_valid
            self.validation_timestamps[block_hash] = time.time()
            self.stats["validations_computed"] += 1
    
    def get_blocks_in_range(self, start_height: int, end_height: int) -> List[Block]:
        """
        Busca blocos em um range de alturas.
        
        EVOLUÇÃO: Busca otimizada para ranges.
        """
        with self._lock:
            blocks = []
            for height in range(start_height, end_height + 1):
                if height in self.height_to_block:
                    entry = self.height_to_block[height]
                    entry.last_accessed = time.time()
                    entry.access_count += 1
                    blocks.append(entry.block)
            
            return blocks
    
    def get_recent_blocks(self, count: int = 10) -> List[Block]:
        """
        Retorna blocos mais recentemente acessados.
        
        EVOLUÇÃO: Acesso otimizado a blocos recentes.
        """
        with self._lock:
            # Ordenar por altura (mais recente primeiro)
            sorted_heights = sorted(self.height_to_block.keys(), reverse=True)
            recent_heights = sorted_heights[:count]
            
            blocks = []
            for height in recent_heights:
                entry = self.height_to_block[height]
                entry.last_accessed = time.time()
                entry.access_count += 1
                blocks.append(entry.block)
            
            return blocks
    
    def get_most_accessed_blocks(self, count: int = 10) -> List[Tuple[Block, int]]:
        """
        Retorna blocos mais acessados com contadores.
        
        EVOLUÇÃO: Análise de padrões de acesso.
        """
        with self._lock:
            # Ordenar por contador de acesso
            sorted_entries = sorted(
                self.height_to_block.values(),
                key=lambda entry: entry.access_count,
                reverse=True
            )
            
            result = []
            for entry in sorted_entries[:count]:
                result.append((entry.block, entry.access_count))
            
            return result
    
    def _add_to_lru_cache(self, block_hash: str, entry: IndexEntry) -> None:
        """
        Adiciona entrada ao cache LRU.
        
        EVOLUÇÃO: Cache LRU inteligente.
        """
        # Se já existe, mover para o final
        if block_hash in self.lru_cache:
            self.lru_cache.move_to_end(block_hash)
            return
        
        # Se cache está cheio, remover o mais antigo
        if len(self.lru_cache) >= self.max_cache_size:
            # Remover o primeiro (mais antigo)
            oldest_hash = next(iter(self.lru_cache))
            del self.lru_cache[oldest_hash]
        
        # Adicionar nova entrada
        self.lru_cache[block_hash] = entry
    
    def cleanup_expired_cache(self) -> int:
        """
        Remove entradas expiradas do cache.
        
        EVOLUÇÃO: Limpeza automática de cache.
        """
        with self._lock:
            current_time = time.time()
            expired_keys = []
            
            # Encontrar chaves expiradas
            for key, timestamp in self.validation_timestamps.items():
                if current_time - timestamp > self.validation_ttl:
                    expired_keys.append(key)
            
            # Remover entradas expiradas
            for key in expired_keys:
                if key in self.validation_cache:
                    del self.validation_cache[key]
                if key in self.validation_timestamps:
                    del self.validation_timestamps[key]
            
            logger.info(f"Removidas {len(expired_keys)} entradas expiradas do cache")
            return len(expired_keys)
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Retorna estatísticas do índice.
        
        EVOLUÇÃO: Métricas detalhadas de performance.
        """
        with self._lock:
            cache_hit_rate = 0.0
            if self.stats["hash_lookups"] > 0:
                cache_hit_rate = self.stats["cache_hits"] / self.stats["hash_lookups"]
            
            validation_cache_hit_rate = 0.0
            total_validations = self.stats["validations_cached"] + self.stats["validations_computed"]
            if total_validations > 0:
                validation_cache_hit_rate = self.stats["validations_cached"] / total_validations
            
            return {
                "index_size": len(self.hash_to_block),
                "cache_size": len(self.lru_cache),
                "validation_cache_size": len(self.validation_cache),
                "hash_lookups": self.stats["hash_lookups"],
                "height_lookups": self.stats["height_lookups"],
                "cache_hits": self.stats["cache_hits"],
                "cache_misses": self.stats["cache_misses"],
                "cache_hit_rate": cache_hit_rate,
                "validations_cached": self.stats["validations_cached"],
                "validations_computed": self.stats["validations_computed"],
                "validation_cache_hit_rate": validation_cache_hit_rate,
                "max_cache_size": self.max_cache_size
            }
    
    def clear_cache(self) -> None:
        """
        Limpa todos os caches.
        
        EVOLUÇÃO: Limpeza completa de cache.
        """
        with self._lock:
            self.lru_cache.clear()
            self.validation_cache.clear()
            self.validation_timestamps.clear()
            
            # Reset estatísticas
            self.stats = {
                "hash_lookups": 0,
                "height_lookups": 0,
                "cache_hits": 0,
                "cache_misses": 0,
                "validations_cached": 0,
                "validations_computed": 0
            }
            
            logger.info("Cache limpo completamente")


class TransactionPool:
    """
    Pool de transações pendentes otimizado.
    
    EVOLUÇÃO: Pool eficiente com priorização por taxa.
    
    Funcionalidades:
    - Armazenamento eficiente de transações pendentes
    - Priorização por taxa de transação
    - Validação de transações duplicadas
    - Limpeza automática de transações expiradas
    """
    
    def __init__(self, max_pool_size: int = 10000):
        self.max_pool_size = max_pool_size
        
        # Pool principal
        self.pending_transactions: Dict[str, Transaction] = {}
        
        # Índices para busca rápida
        self.address_to_transactions: Dict[str, Set[str]] = {}
        self.fee_priority_queue: List[Tuple[Decimal, str]] = []
        
        # Configurações
        self.min_fee_threshold: Decimal = Decimal('0.00000001')
        self.transaction_ttl: int = 3600  # 1 hora
        
        # Estatísticas
        self.stats = {
            "transactions_added": 0,
            "transactions_removed": 0,
            "duplicate_rejections": 0,
            "expired_cleanups": 0
        }
        
        # Thread safety
        self._lock = threading.RLock()
        
        logger.info(f"TransactionPool inicializado com capacidade de {max_pool_size} transações")
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """
        Adiciona transação ao pool.
        
        EVOLUÇÃO: Adição otimizada com validação de duplicatas.
        """
        with self._lock:
            try:
                # Verificar se já existe
                if transaction.transaction_id in self.pending_transactions:
                    self.stats["duplicate_rejections"] += 1
                    return False
                
                # Verificar taxa mínima
                if transaction.fee < self.min_fee_threshold:
                    return False
                
                # Verificar capacidade do pool
                if len(self.pending_transactions) >= self.max_pool_size:
                    # Remover transação com menor taxa
                    self._remove_lowest_fee_transaction()
                
                # Adicionar transação
                self.pending_transactions[transaction.transaction_id] = transaction
                
                # Atualizar índices
                self._update_address_index(transaction, add=True)
                self._update_fee_priority_queue(transaction, add=True)
                
                self.stats["transactions_added"] += 1
                logger.debug(f"Transação {transaction.transaction_id} adicionada ao pool")
                
                return True
                
            except Exception as e:
                logger.error(f"Erro ao adicionar transação ao pool: {e}")
                return False
    
    def get_transactions_for_block(self, max_count: int = 1000) -> List[Transaction]:
        """
        Retorna transações para mineração (ordenadas por taxa).
        
        EVOLUÇÃO: Seleção otimizada por prioridade de taxa.
        """
        with self._lock:
            # Ordenar por taxa (maior primeiro)
            sorted_transactions = sorted(
                self.fee_priority_queue,
                key=lambda x: x[0],
                reverse=True
            )
            
            transactions = []
            for fee, tx_id in sorted_transactions[:max_count]:
                if tx_id in self.pending_transactions:
                    transactions.append(self.pending_transactions[tx_id])
            
            return transactions
    
    def remove_transaction(self, transaction_id: str) -> bool:
        """
        Remove transação do pool.
        
        EVOLUÇÃO: Remoção otimizada com atualização de índices.
        """
        with self._lock:
            if transaction_id not in self.pending_transactions:
                return False
            
            transaction = self.pending_transactions[transaction_id]
            
            # Remover dos índices
            self._update_address_index(transaction, add=False)
            self._update_fee_priority_queue(transaction, add=False)
            
            # Remover do pool
            del self.pending_transactions[transaction_id]
            
            self.stats["transactions_removed"] += 1
            return True
    
    def get_transactions_by_address(self, address: str) -> List[Transaction]:
        """
        Retorna transações de um endereço específico.
        
        EVOLUÇÃO: Busca otimizada por endereço.
        """
        with self._lock:
            if address not in self.address_to_transactions:
                return []
            
            transactions = []
            for tx_id in self.address_to_transactions[address]:
                if tx_id in self.pending_transactions:
                    transactions.append(self.pending_transactions[tx_id])
            
            return transactions
    
    def cleanup_expired_transactions(self) -> int:
        """
        Remove transações expiradas do pool.
        
        EVOLUÇÃO: Limpeza automática de transações expiradas.
        """
        with self._lock:
            current_time = time.time()
            expired_transactions = []
            
            for tx_id, transaction in self.pending_transactions.items():
                if current_time - transaction.timestamp.value > self.transaction_ttl:
                    expired_transactions.append(tx_id)
            
            for tx_id in expired_transactions:
                self.remove_transaction(tx_id)
            
            self.stats["expired_cleanups"] += len(expired_transactions)
            logger.info(f"Removidas {len(expired_transactions)} transações expiradas")
            
            return len(expired_transactions)
    
    def _remove_lowest_fee_transaction(self) -> None:
        """Remove transação com menor taxa."""
        if not self.fee_priority_queue:
            return
        
        # Ordenar por taxa (menor primeiro)
        sorted_queue = sorted(self.fee_priority_queue, key=lambda x: x[0])
        lowest_fee, tx_id = sorted_queue[0]
        
        self.remove_transaction(tx_id)
    
    def _update_address_index(self, transaction: Transaction, add: bool) -> None:
        """Atualiza índice de endereços."""
        addresses = []
        
        if transaction.from_address:
            addresses.append(transaction.from_address.value)
        if transaction.to_address:
            addresses.append(transaction.to_address.value)
        
        for address in addresses:
            if add:
                if address not in self.address_to_transactions:
                    self.address_to_transactions[address] = set()
                self.address_to_transactions[address].add(transaction.transaction_id)
            else:
                if address in self.address_to_transactions:
                    self.address_to_transactions[address].discard(transaction.transaction_id)
                    if not self.address_to_transactions[address]:
                        del self.address_to_transactions[address]
    
    def _update_fee_priority_queue(self, transaction: Transaction, add: bool) -> None:
        """Atualiza fila de prioridade por taxa."""
        if add:
            self.fee_priority_queue.append((transaction.fee, transaction.transaction_id))
        else:
            self.fee_priority_queue = [
                (fee, tx_id) for fee, tx_id in self.fee_priority_queue
                if tx_id != transaction.transaction_id
            ]
    
    def get_statistics(self) -> Dict[str, any]:
        """Retorna estatísticas do pool."""
        with self._lock:
            return {
                "pool_size": len(self.pending_transactions),
                "max_pool_size": self.max_pool_size,
                "unique_addresses": len(self.address_to_transactions),
                "transactions_added": self.stats["transactions_added"],
                "transactions_removed": self.stats["transactions_removed"],
                "duplicate_rejections": self.stats["duplicate_rejections"],
                "expired_cleanups": self.stats["expired_cleanups"],
                "min_fee_threshold": float(self.min_fee_threshold),
                "transaction_ttl": self.transaction_ttl
            }


# Instâncias globais otimizadas
blockchain_index = BlockchainIndex()
transaction_pool = TransactionPool()
