"""
Serviço de Mineração - Implementa algoritmo de mineração
"""

import time
import hashlib
import threading
from typing import List, Optional, Dict
from decimal import Decimal

from ..entities.block import Block
from ..entities.blockchain import Blockchain
from ...transaction.entities.transaction import Transaction
from ...shared.value_objects.hash_value import HashValue
from ...shared.value_objects.timestamp import Timestamp


class MiningService:
    """
    Serviço de Mineração - Gerencia o processo de mineração.
    
    Responsabilidades:
    - Coordenar processo de mineração
    - Gerenciar pool de transações
    - Calcular dificuldade dinâmica
    - Distribuir recompensas
    - Monitorar performance de mineração
    """
    
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.transaction_pool: List[Transaction] = []
        self._pool_lock = threading.RLock()  # Lock para thread safety
        self.mining_stats: Dict = {
            "blocks_mined": 0,
            "total_mining_time": 0.0,
            "average_mining_time": 0.0,
            "hash_rate": 0.0
        }
        self._stats_lock = threading.RLock()  # Lock para estatísticas
    
    def add_transaction_to_pool(self, transaction: Transaction) -> bool:
        """Adiciona transação ao pool de mineração"""
        try:
            with self._pool_lock:
                # Validar transação
                if not transaction.is_valid():
                    return False
                
                # Verificar se já existe
                for tx in self.transaction_pool:
                    if tx.id.value == transaction.id.value:
                        return False
                
                # Adicionar ao pool
                self.transaction_pool.append(transaction)
                return True
                
        except Exception:
            return False
    
    def remove_transaction_from_pool(self, tx_id: str) -> bool:
        """Remove transação do pool"""
        with self._pool_lock:
            for i, tx in enumerate(self.transaction_pool):
                if tx.id.value == tx_id:
                    del self.transaction_pool[i]
                    return True
            return False
    
    def get_transaction_pool(self) -> List[Transaction]:
        """Retorna pool de transações"""
        with self._pool_lock:
            return self.transaction_pool.copy()
    
    def mine_block(self, miner_address: str, max_transactions: Optional[int] = None) -> Optional[Block]:
        """Mina um novo bloco"""
        try:
            # Selecionar transações do pool (thread-safe)
            transactions_to_mine = self._select_transactions_for_mining(max_transactions)
            
            if not transactions_to_mine:
                return None
            
            # Minerar bloco
            mined_block = self.blockchain.mine_block(transactions_to_mine, miner_address)
            
            if mined_block:
                # Atualizar estatísticas (thread-safe)
                self._update_mining_stats(mined_block)
                
                # Remover transações do pool (thread-safe)
                with self._pool_lock:
                    for tx in transactions_to_mine:
                        for i, pool_tx in enumerate(self.transaction_pool):
                            if pool_tx.id.value == tx.id.value:
                                del self.transaction_pool[i]
                                break
                
                return mined_block
            
            return None
            
        except Exception:
            return None
    
    def _select_transactions_for_mining(self, max_transactions: Optional[int] = None) -> List[Transaction]:
        """Seleciona transações do pool para mineração"""
        with self._pool_lock:
            if not self.transaction_pool:
                return []
            
            # Ordenar por taxa (maior taxa primeiro)
            sorted_transactions = sorted(
                self.transaction_pool,
                key=lambda tx: tx.fee.value,
                reverse=True
            )
            
            # Limitar número de transações
            limit = max_transactions or self.blockchain.max_transactions_per_block
            return sorted_transactions[:limit]
    
    def _update_mining_stats(self, block: Block):
        """Atualiza estatísticas de mineração"""
        with self._stats_lock:
            self.mining_stats["blocks_mined"] += 1
            self.mining_stats["total_mining_time"] += block.mining_time
            
            if self.mining_stats["blocks_mined"] > 0:
                self.mining_stats["average_mining_time"] = (
                    self.mining_stats["total_mining_time"] / self.mining_stats["blocks_mined"]
                )
    
    def calculate_hash_rate(self, sample_time: float = 60.0) -> float:
        """Calcula hash rate estimado"""
        if not self.blockchain.blocks:
            return 0.0
        
        # Usar últimos blocos para estimar hash rate
        recent_blocks = self.blockchain.blocks[-10:] if len(self.blockchain.blocks) >= 10 else self.blockchain.blocks
        
        if len(recent_blocks) < 2:
            return 0.0
        
        total_hashes = 0
        total_time = 0
        
        for block in recent_blocks:
            # Estimar número de hashes baseado na dificuldade
            estimated_hashes = 2 ** block.difficulty
            total_hashes += estimated_hashes
            total_time += block.mining_time
        
        if total_time > 0:
            hash_rate = total_hashes / total_time
            return hash_rate
        
        return 0.0
    
    def get_mining_difficulty(self) -> int:
        """Retorna dificuldade atual de mineração"""
        return self.blockchain.difficulty
    
    def estimate_mining_time(self, difficulty: Optional[int] = None) -> float:
        """Estima tempo de mineração para uma dificuldade"""
        target_difficulty = difficulty or self.blockchain.difficulty
        
        # Estimativa baseada em tentativas médias
        # Para encontrar um hash com N zeros, precisamos de ~2^N tentativas
        estimated_attempts = 2 ** target_difficulty
        
        # Assumir que cada tentativa leva ~0.000001 segundos
        time_per_attempt = 0.000001
        
        return estimated_attempts * time_per_attempt
    
    def get_mining_reward(self) -> Decimal:
        """Retorna recompensa atual de mineração"""
        return self.blockchain.get_current_block_reward()
    
    def get_mining_stats(self) -> Dict:
        """Retorna estatísticas de mineração"""
        return {
            **self.mining_stats,
            "current_difficulty": self.get_mining_difficulty(),
            "current_reward": self.get_mining_reward(),
            "estimated_hash_rate": self.calculate_hash_rate(),
            "pool_size": len(self.transaction_pool),
            "estimated_mining_time": self.estimate_mining_time()
        }
    
    def validate_mining_result(self, block: Block) -> bool:
        """Valida resultado de mineração"""
        try:
            # Verificar se o bloco é válido
            if not block.is_valid():
                return False
            
            # Verificar se o hash atende à dificuldade
            target_prefix = "0" * block.difficulty
            if not block.hash.value.startswith(target_prefix):
                return False
            
            # Verificar se o nonce é válido
            block_data = block._create_block_data_for_hash()
            calculated_hash = hashlib.sha256(block_data.encode()).hexdigest()
            
            if calculated_hash != block.hash.value:
                return False
            
            return True
            
        except Exception:
            return False
    
    def simulate_mining(self, difficulty: int, max_time: float = 10.0) -> Dict:
        """Simula processo de mineração para testes"""
        start_time = time.time()
        attempts = 0
        target_prefix = "0" * difficulty
        
        while time.time() - start_time < max_time:
            attempts += 1
            
            # Simular cálculo de hash
            test_data = f"test_data_{attempts}"
            test_hash = hashlib.sha256(test_data.encode()).hexdigest()
            
            # Verificar se atende à dificuldade
            if test_hash.startswith(target_prefix):
                mining_time = time.time() - start_time
                return {
                    "success": True,
                    "attempts": attempts,
                    "mining_time": mining_time,
                    "hash": test_hash,
                    "difficulty": difficulty
                }
        
        return {
            "success": False,
            "attempts": attempts,
            "mining_time": max_time,
            "difficulty": difficulty
        }
