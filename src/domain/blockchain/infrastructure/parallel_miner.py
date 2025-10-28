"""
Sistema de Mineração Paralela Otimizado
=======================================

Este módulo implementa mineração paralela com threading para otimizar
a performance do Proof of Work da blockchain.

EVOLUÇÃO: Mineração paralela com otimização de recursos e cache de nonces.
"""

import hashlib
import time
import threading
import multiprocessing
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import logging
from decimal import Decimal

from ..entities.block import Block
from ...transaction.entities.transaction import Transaction
from ...shared.value_objects.hash_value import HashValue
from ...shared.value_objects.timestamp import Timestamp

logger = logging.getLogger(__name__)


@dataclass
class MiningResult:
    """Resultado de uma tentativa de mineração"""
    success: bool
    nonce: Optional[int] = None
    hash: Optional[str] = None
    mining_time: float = 0.0
    attempts: int = 0
    thread_id: Optional[int] = None
    process_id: Optional[int] = None


@dataclass
class MiningConfig:
    """Configuração para mineração paralela"""
    max_threads: int = multiprocessing.cpu_count()
    max_processes: int = max(1, multiprocessing.cpu_count() // 2)
    batch_size: int = 10000
    timeout_seconds: int = 300  # 5 minutos
    cache_nonces: bool = True
    cache_size: int = 1000
    adaptive_difficulty: bool = True


class NonceCache:
    """
    Cache inteligente de nonces para otimizar mineração.
    
    EVOLUÇÃO: Cache de nonces com padrões de sucesso.
    """
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: Dict[str, List[int]] = {}
        self.success_patterns: Dict[str, int] = {}
        self._lock = threading.RLock()
    
    def get_candidate_nonces(self, block_data: str, difficulty: int) -> List[int]:
        """
        Retorna nonces candidatos baseados em padrões de sucesso.
        
        EVOLUÇÃO: Nonces inteligentes baseados em histórico.
        """
        with self._lock:
            cache_key = f"{hashlib.sha256(block_data.encode()).hexdigest()[:16]}_{difficulty}"
            
            if cache_key in self.cache:
                return self.cache[cache_key].copy()
            
            # Gerar nonces baseados em padrões de sucesso
            candidates = []
            
            # Nonces baseados em padrões conhecidos
            if difficulty in self.success_patterns:
                base_nonce = self.success_patterns[difficulty]
                candidates.extend(range(base_nonce, base_nonce + 1000, 1))
            
            # Nonces aleatórios para exploração
            import random
            random.seed(int(time.time()))
            candidates.extend(random.sample(range(0, 2**32), min(100, self.max_size)))
            
            # Limitar tamanho do cache
            if len(candidates) > self.max_size:
                candidates = candidates[:self.max_size]
            
            self.cache[cache_key] = candidates
            return candidates.copy()
    
    def record_success(self, difficulty: int, nonce: int) -> None:
        """Registra nonce de sucesso para futuras tentativas."""
        with self._lock:
            self.success_patterns[difficulty] = nonce
    
    def clear_cache(self) -> None:
        """Limpa o cache de nonces."""
        with self._lock:
            self.cache.clear()
            self.success_patterns.clear()


class ParallelMiner:
    """
    Minerador paralelo otimizado para blockchain.
    
    EVOLUÇÃO: Mineração paralela com threading e multiprocessing.
    
    Funcionalidades:
    - Mineração paralela com múltiplas threads/processos
    - Cache inteligente de nonces
    - Ajuste dinâmico de dificuldade
    - Otimização de recursos
    - Estatísticas detalhadas
    """
    
    def __init__(self, config: MiningConfig = None):
        self.config = config or MiningConfig()
        self.nonce_cache = NonceCache(self.config.cache_size)
        self.mining_stats = {
            "total_attempts": 0,
            "successful_mines": 0,
            "total_mining_time": 0.0,
            "average_mining_time": 0.0,
            "thread_utilization": 0.0,
            "cache_hit_rate": 0.0
        }
        self._lock = threading.RLock()
        
        logger.info(f"ParallelMiner inicializado com {self.config.max_threads} threads e {self.config.max_processes} processos")
    
    def mine_block_parallel(
        self, 
        block: Block, 
        transactions: List[Transaction],
        miner_address: str
    ) -> Optional[MiningResult]:
        """
        Minera bloco usando mineração paralela otimizada.
        
        EVOLUÇÃO: Mineração paralela com múltiplas estratégias.
        """
        try:
            start_time = time.time()
            
            # Preparar dados do bloco para mineração
            block_data = self._prepare_block_data(block, transactions, miner_address)
            
            # Obter nonces candidatos do cache
            candidate_nonces = self.nonce_cache.get_candidate_nonces(
                block_data, block.difficulty
            )
            
            # Tentar mineração com diferentes estratégias
            result = None
            
            # Estratégia 1: Mineração com threads (para dificuldades baixas/médias)
            if block.difficulty <= 10:
                result = self._mine_with_threads(block_data, block.difficulty, candidate_nonces)
            
            # Estratégia 2: Mineração com processos (para dificuldades altas)
            elif block.difficulty <= 20:
                result = self._mine_with_processes(block_data, block.difficulty, candidate_nonces)
            
            # Estratégia 3: Mineração híbrida (para dificuldades muito altas)
            else:
                result = self._mine_hybrid(block_data, block.difficulty, candidate_nonces)
            
            if result and result.success:
                # Registrar sucesso no cache
                self.nonce_cache.record_success(block.difficulty, result.nonce)
                
                # Atualizar estatísticas
                self._update_mining_stats(result)
                
                logger.info(f"Bloco minerado com sucesso: nonce={result.nonce}, tempo={result.mining_time:.2f}s")
                return result
            
            return None
            
        except Exception as e:
            logger.error(f"Erro na mineração paralela: {e}")
            return None
    
    def _prepare_block_data(
        self, 
        block: Block, 
        transactions: List[Transaction], 
        miner_address: str
    ) -> str:
        """Prepara dados do bloco para mineração."""
        # Criar string de dados do bloco (usar mesmo formato do Block.is_valid())
        block_data = {
            "height": block.height,
            "previous_hash": block.previous_hash.value if block.previous_hash else "0",
            "merkle_root": block.merkle_root.value,
            "timestamp": block.timestamp.value,
            "nonce": 0,  # Será substituído durante a mineração
            "difficulty": block.difficulty,
            "transactions_count": len(transactions)
        }
        
        import json
        return json.dumps(block_data, sort_keys=True)
    
    def _mine_with_threads(
        self, 
        block_data: str, 
        difficulty: int, 
        candidate_nonces: List[int]
    ) -> Optional[MiningResult]:
        """
        Minera usando múltiplas threads.
        
        EVOLUÇÃO: Mineração paralela com threads otimizada.
        """
        try:
            target = "0" * difficulty
            
            # Dividir nonces entre threads
            nonces_per_thread = len(candidate_nonces) // self.config.max_threads
            if nonces_per_thread == 0:
                nonces_per_thread = 1
            
            results = []
            
            with ThreadPoolExecutor(max_workers=self.config.max_threads) as executor:
                futures = []
                
                for i in range(self.config.max_threads):
                    start_idx = i * nonces_per_thread
                    end_idx = min(start_idx + nonces_per_thread, len(candidate_nonces))
                    
                    if start_idx < len(candidate_nonces):
                        thread_nonces = candidate_nonces[start_idx:end_idx]
                        future = executor.submit(
                            self._mine_nonce_range_thread,
                            block_data, target, thread_nonces, i
                        )
                        futures.append(future)
                
                # Aguardar resultados
                for future in as_completed(futures, timeout=self.config.timeout_seconds):
                    result = future.result()
                    if result and result.success:
                        return result
            
            return None
            
        except Exception as e:
            logger.error(f"Erro na mineração com threads: {e}")
            return None
    
    def _mine_with_processes(
        self, 
        block_data: str, 
        difficulty: int, 
        candidate_nonces: List[int]
    ) -> Optional[MiningResult]:
        """
        Minera usando múltiplos processos.
        
        EVOLUÇÃO: Mineração paralela com processos para CPU intensivo.
        """
        try:
            target = "0" * difficulty
            
            # Dividir nonces entre processos
            nonces_per_process = len(candidate_nonces) // self.config.max_processes
            if nonces_per_process == 0:
                nonces_per_process = 1
            
            with ProcessPoolExecutor(max_workers=self.config.max_processes) as executor:
                futures = []
                
                for i in range(self.config.max_processes):
                    start_idx = i * nonces_per_process
                    end_idx = min(start_idx + nonces_per_process, len(candidate_nonces))
                    
                    if start_idx < len(candidate_nonces):
                        process_nonces = candidate_nonces[start_idx:end_idx]
                        future = executor.submit(
                            self._mine_nonce_range_process,
                            block_data, target, process_nonces, i
                        )
                        futures.append(future)
                
                # Aguardar resultados
                for future in as_completed(futures, timeout=self.config.timeout_seconds):
                    result = future.result()
                    if result and result.success:
                        return result
            
            return None
            
        except Exception as e:
            logger.error(f"Erro na mineração com processos: {e}")
            return None
    
    def _mine_hybrid(
        self, 
        block_data: str, 
        difficulty: int, 
        candidate_nonces: List[int]
    ) -> Optional[MiningResult]:
        """
        Mineração híbrida usando threads e processos.
        
        EVOLUÇÃO: Estratégia híbrida para dificuldades muito altas.
        """
        try:
            target = "0" * difficulty
            
            # Usar processos para a maior parte dos nonces
            process_nonces = candidate_nonces[:len(candidate_nonces)//2]
            thread_nonces = candidate_nonces[len(candidate_nonces)//2:]
            
            # Executar processos e threads simultaneamente
            with ThreadPoolExecutor(max_workers=self.config.max_threads) as thread_executor, \
                 ProcessPoolExecutor(max_workers=self.config.max_processes) as process_executor:
                
                # Submeter tarefas
                thread_future = thread_executor.submit(
                    self._mine_nonce_range_thread,
                    block_data, target, thread_nonces, 0
                )
                
                process_future = process_executor.submit(
                    self._mine_nonce_range_process,
                    block_data, target, process_nonces, 0
                )
                
                # Aguardar primeiro resultado
                for future in as_completed([thread_future, process_future], timeout=self.config.timeout_seconds):
                    result = future.result()
                    if result and result.success:
                        return result
            
            return None
            
        except Exception as e:
            logger.error(f"Erro na mineração híbrida: {e}")
            return None
    
    def _mine_nonce_range_thread(
        self, 
        block_data: str, 
        target: str, 
        nonces: List[int], 
        thread_id: int
    ) -> Optional[MiningResult]:
        """Minera um range de nonces em uma thread."""
        start_time = time.time()
        attempts = 0
        
        for nonce in nonces:
            attempts += 1
            
            # Criar hash com nonce (usar mesmo formato do Block.is_valid())
            import json
            block_data_dict = json.loads(block_data)
            block_data_dict["nonce"] = nonce
            data_to_hash = json.dumps(block_data_dict, sort_keys=True)
            block_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
            
            # Verificar se atende à dificuldade
            if block_hash.startswith(target):
                mining_time = time.time() - start_time
                return MiningResult(
                    success=True,
                    nonce=nonce,
                    hash=block_hash,
                    mining_time=mining_time,
                    attempts=attempts,
                    thread_id=thread_id
                )
        
        return None
    
    def _mine_nonce_range_process(
        self, 
        block_data: str, 
        target: str, 
        nonces: List[int], 
        process_id: int
    ) -> Optional[MiningResult]:
        """Minera um range de nonces em um processo."""
        start_time = time.time()
        attempts = 0
        
        for nonce in nonces:
            attempts += 1
            
            # Criar hash com nonce (usar mesmo formato do Block.is_valid())
            import json
            block_data_dict = json.loads(block_data)
            block_data_dict["nonce"] = nonce
            data_to_hash = json.dumps(block_data_dict, sort_keys=True)
            block_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
            
            # Verificar se atende à dificuldade
            if block_hash.startswith(target):
                mining_time = time.time() - start_time
                return MiningResult(
                    success=True,
                    nonce=nonce,
                    hash=block_hash,
                    mining_time=mining_time,
                    attempts=attempts,
                    process_id=process_id
                )
        
        return None
    
    def _update_mining_stats(self, result: MiningResult) -> None:
        """Atualiza estatísticas de mineração."""
        with self._lock:
            self.mining_stats["total_attempts"] += result.attempts
            self.mining_stats["successful_mines"] += 1
            self.mining_stats["total_mining_time"] += result.mining_time
            
            if self.mining_stats["successful_mines"] > 0:
                self.mining_stats["average_mining_time"] = (
                    self.mining_stats["total_mining_time"] / 
                    self.mining_stats["successful_mines"]
                )
    
    def get_mining_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de mineração."""
        with self._lock:
            stats = self.mining_stats.copy()
            
            # Calcular taxa de utilização de threads
            if stats["total_attempts"] > 0:
                stats["thread_utilization"] = min(1.0, stats["total_attempts"] / (self.config.max_threads * 1000))
            
            # Calcular taxa de hit do cache
            cache_stats = self.nonce_cache.cache
            if cache_stats:
                stats["cache_hit_rate"] = len(cache_stats) / self.config.cache_size
            
            return stats
    
    def optimize_mining_config(self) -> Dict[str, Any]:
        """
        Otimiza configuração de mineração baseada em estatísticas.
        
        EVOLUÇÃO: Otimização automática de configuração.
        """
        with self._lock:
            optimizations = []
            
            # Ajustar número de threads baseado na utilização
            if self.mining_stats["thread_utilization"] < 0.5:
                new_threads = max(1, self.config.max_threads - 1)
                if new_threads != self.config.max_threads:
                    self.config.max_threads = new_threads
                    optimizations.append(f"Reduzido threads para {new_threads}")
            
            elif self.mining_stats["thread_utilization"] > 0.9:
                new_threads = min(multiprocessing.cpu_count(), self.config.max_threads + 1)
                if new_threads != self.config.max_threads:
                    self.config.max_threads = new_threads
                    optimizations.append(f"Aumentado threads para {new_threads}")
            
            # Ajustar tamanho do cache baseado na taxa de hit
            if self.mining_stats["cache_hit_rate"] < 0.3:
                new_cache_size = min(5000, self.config.cache_size * 2)
                if new_cache_size != self.config.cache_size:
                    self.config.cache_size = new_cache_size
                    self.nonce_cache.max_size = new_cache_size
                    optimizations.append(f"Aumentado cache para {new_cache_size}")
            
            # Ajustar timeout baseado no tempo médio de mineração
            if self.mining_stats["average_mining_time"] > self.config.timeout_seconds * 0.8:
                new_timeout = int(self.mining_stats["average_mining_time"] * 1.5)
                if new_timeout != self.config.timeout_seconds:
                    self.config.timeout_seconds = new_timeout
                    optimizations.append(f"Aumentado timeout para {new_timeout}s")
            
            return {
                "optimizations_applied": optimizations,
                "current_config": {
                    "max_threads": self.config.max_threads,
                    "max_processes": self.config.max_processes,
                    "cache_size": self.config.cache_size,
                    "timeout_seconds": self.config.timeout_seconds
                }
            }


# Instância global otimizada
parallel_miner = ParallelMiner()
