"""
Sistema de Validação Incremental Otimizado
==========================================

Este módulo implementa validação incremental de blocos para otimizar
a performance da blockchain, evitando validação completa desnecessária.

EVOLUÇÃO: Validação incremental com cache e paralelização.
"""

import time
import threading
from typing import List, Optional, Dict, Any, Set, Tuple
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from decimal import Decimal

from ..entities.block import Block
from ...transaction.entities.transaction import Transaction
from ...shared.value_objects.hash_value import HashValue
from ...shared.value_objects.timestamp import Timestamp

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Resultado de uma validação"""
    is_valid: bool
    validation_time: float = 0.0
    validation_type: str = ""
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    validated_components: Set[str] = field(default_factory=set)


@dataclass
class ValidationCache:
    """Cache de validações para evitar recálculos"""
    block_validations: Dict[str, ValidationResult] = field(default_factory=dict)
    transaction_validations: Dict[str, ValidationResult] = field(default_factory=dict)
    chain_validations: Dict[str, ValidationResult] = field(default_factory=dict)
    timestamps: Dict[str, float] = field(default_factory=dict)
    ttl: int = 3600  # 1 hora


class IncrementalValidator:
    """
    Validador incremental otimizado para blockchain.
    
    EVOLUÇÃO: Validação incremental com cache e paralelização.
    
    Funcionalidades:
    - Validação incremental de blocos
    - Cache de validações para evitar recálculos
    - Validação paralela de componentes
    - Validação inteligente baseada em mudanças
    - Estatísticas detalhadas de validação
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.validation_cache = ValidationCache()
        self.validation_stats = {
            "total_validations": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "parallel_validations": 0,
            "incremental_validations": 0,
            "total_validation_time": 0.0,
            "average_validation_time": 0.0
        }
        self._lock = threading.RLock()
        
        logger.info(f"IncrementalValidator inicializado com {max_workers} workers")
    
    def validate_block_incremental(
        self, 
        block: Block, 
        previous_block: Optional[Block] = None,
        force_full_validation: bool = False
    ) -> ValidationResult:
        """
        Valida bloco usando validação incremental.
        
        EVOLUÇÃO: Validação inteligente baseada em mudanças.
        """
        try:
            start_time = time.time()
            
            # Verificar cache primeiro
            if not force_full_validation:
                cached_result = self._get_cached_validation(block.hash.value, "block")
                if cached_result:
                    self.validation_stats["cache_hits"] += 1
                    return cached_result
            
            self.validation_stats["cache_misses"] += 1
            
            # Determinar tipo de validação necessário
            validation_type = self._determine_validation_type(block, previous_block)
            
            if validation_type == "incremental":
                result = self._validate_block_incremental(block, previous_block)
                self.validation_stats["incremental_validations"] += 1
            else:
                result = self._validate_block_full(block)
            
            # Cache resultado
            self._cache_validation(block.hash.value, "block", result)
            
            # Atualizar estatísticas
            validation_time = time.time() - start_time
            result.validation_time = validation_time
            self._update_validation_stats(validation_time)
            
            logger.debug(f"Bloco {block.height} validado: {validation_type}, tempo={validation_time:.3f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na validação incremental do bloco: {e}")
            return ValidationResult(
                is_valid=False,
                validation_type="error",
                errors=[str(e)]
            )
    
    def validate_chain_incremental(
        self, 
        blocks: List[Block], 
        start_index: int = 0,
        force_full_validation: bool = False
    ) -> ValidationResult:
        """
        Valida cadeia usando validação incremental.
        
        EVOLUÇÃO: Validação paralela de blocos com cache inteligente.
        """
        try:
            start_time = time.time()
            
            if not blocks:
                return ValidationResult(is_valid=True, validation_type="empty_chain")
            
            # Verificar cache da cadeia
            chain_key = f"{blocks[0].hash.value}_{len(blocks)}_{start_index}"
            if not force_full_validation:
                cached_result = self._get_cached_validation(chain_key, "chain")
                if cached_result:
                    self.validation_stats["cache_hits"] += 1
                    return cached_result
            
            self.validation_stats["cache_misses"] += 1
            
            # Validação paralela de blocos
            validation_results = []
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = []
                
                for i, block in enumerate(blocks[start_index:], start_index):
                    previous_block = blocks[i-1] if i > 0 else None
                    future = executor.submit(
                        self.validate_block_incremental, 
                        block, 
                        previous_block, 
                        force_full_validation
                    )
                    futures.append((i, future))
                
                # Coletar resultados
                for future in as_completed([f for _, f in futures]):
                    result = future.result()
                    # Encontrar o índice correspondente
                    for i, f in futures:
                        if f == future:
                            validation_results.append((i, result))
                            break
                    
                    # Se algum bloco é inválido, parar validação
                    if not result.is_valid:
                        break
            
            # Verificar se todos os blocos são válidos
            all_valid = all(result.is_valid for _, result in validation_results)
            
            # Coletar erros e warnings
            all_errors = []
            all_warnings = []
            validated_components = set()
            
            for _, result in validation_results:
                all_errors.extend(result.errors)
                all_warnings.extend(result.warnings)
                validated_components.update(result.validated_components)
            
            # Criar resultado final
            final_result = ValidationResult(
                is_valid=all_valid,
                validation_type="incremental_chain",
                errors=all_errors,
                warnings=all_warnings,
                validated_components=validated_components
            )
            
            # Cache resultado
            self._cache_validation(chain_key, "chain", final_result)
            
            # Atualizar estatísticas
            validation_time = time.time() - start_time
            final_result.validation_time = validation_time
            self.validation_stats["parallel_validations"] += 1
            self._update_validation_stats(validation_time)
            
            logger.info(f"Cadeia validada incrementalmente: {len(blocks)} blocos, tempo={validation_time:.3f}s")
            
            return final_result
            
        except Exception as e:
            logger.error(f"Erro na validação incremental da cadeia: {e}")
            return ValidationResult(
                is_valid=False,
                validation_type="error",
                errors=[str(e)]
            )
    
    def validate_transactions_incremental(
        self, 
        transactions: List[Transaction],
        existing_transactions: Optional[Set[str]] = None
    ) -> ValidationResult:
        """
        Valida transações usando validação incremental.
        
        EVOLUÇÃO: Validação inteligente de transações duplicadas.
        """
        try:
            start_time = time.time()
            
            if not transactions:
                return ValidationResult(is_valid=True, validation_type="empty_transactions")
            
            # Verificar transações duplicadas
            transaction_ids = set()
            duplicate_transactions = []
            
            for tx in transactions:
                if tx.id.value in transaction_ids:
                    duplicate_transactions.append(tx.id.value)
                else:
                    transaction_ids.add(tx.id.value)
            
            # Verificar contra transações existentes
            if existing_transactions:
                conflicting_transactions = transaction_ids.intersection(existing_transactions)
                if conflicting_transactions:
                    return ValidationResult(
                        is_valid=False,
                        validation_type="incremental_transactions",
                        errors=[f"Transações conflitantes: {conflicting_transactions}"]
                    )
            
            # Validação paralela de transações individuais
            validation_results = []
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = []
                
                for tx in transactions:
                    future = executor.submit(self._validate_single_transaction, tx)
                    futures.append(future)
                
                # Coletar resultados
                for future in as_completed(futures):
                    result = future.result()
                    validation_results.append(result)
            
            # Verificar se todas as transações são válidas
            all_valid = all(result.is_valid for result in validation_results)
            
            # Coletar erros e warnings
            all_errors = []
            all_warnings = []
            
            if duplicate_transactions:
                all_errors.append(f"Transações duplicadas: {duplicate_transactions}")
            
            for result in validation_results:
                all_errors.extend(result.errors)
                all_warnings.extend(result.warnings)
            
            # Criar resultado final
            final_result = ValidationResult(
                is_valid=all_valid,
                validation_type="incremental_transactions",
                errors=all_errors,
                warnings=all_warnings,
                validated_components={"transactions"}
            )
            
            # Atualizar estatísticas
            validation_time = time.time() - start_time
            final_result.validation_time = validation_time
            self._update_validation_stats(validation_time)
            
            logger.debug(f"Transações validadas incrementalmente: {len(transactions)}, tempo={validation_time:.3f}s")
            
            return final_result
            
        except Exception as e:
            logger.error(f"Erro na validação incremental de transações: {e}")
            return ValidationResult(
                is_valid=False,
                validation_type="error",
                errors=[str(e)]
            )
    
    def _determine_validation_type(self, block: Block, previous_block: Optional[Block]) -> str:
        """Determina o tipo de validação necessário."""
        if not previous_block:
            return "full"  # Primeiro bloco sempre validação completa
        
        # Verificar se há mudanças significativas
        if (block.difficulty != previous_block.difficulty or 
            block.timestamp.value - previous_block.timestamp.value > 3600):  # 1 hora
            return "full"
        
        return "incremental"
    
    def _validate_block_incremental(self, block: Block, previous_block: Optional[Block]) -> ValidationResult:
        """Valida bloco usando validação incremental."""
        errors = []
        warnings = []
        validated_components = set()
        
        # Validação básica do bloco
        if not block.is_valid():
            errors.append("Bloco inválido")
            return ValidationResult(is_valid=False, errors=errors)
        
        validated_components.add("block_structure")
        
        # Validação incremental de altura
        if previous_block and block.height != previous_block.height + 1:
            errors.append(f"Altura incorreta: esperado {previous_block.height + 1}, encontrado {block.height}")
        
        validated_components.add("height")
        
        # Validação incremental de hash anterior
        if previous_block and block.previous_hash and block.previous_hash.value != previous_block.hash.value:
            errors.append("Hash anterior incorreto")
        
        validated_components.add("previous_hash")
        
        # Validação incremental de timestamp
        if previous_block and block.timestamp.value <= previous_block.timestamp.value:
            warnings.append("Timestamp não é estritamente crescente")
        
        validated_components.add("timestamp")
        
        # Validação incremental de dificuldade
        if previous_block and abs(block.difficulty - previous_block.difficulty) > 1:
            warnings.append("Mudança de dificuldade muito grande")
        
        validated_components.add("difficulty")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            validation_type="incremental",
            errors=errors,
            warnings=warnings,
            validated_components=validated_components
        )
    
    def _validate_block_full(self, block: Block) -> ValidationResult:
        """Valida bloco usando validação completa."""
        errors = []
        warnings = []
        validated_components = set()
        
        # Validação completa do bloco
        if not block.is_valid():
            errors.append("Bloco inválido")
            return ValidationResult(is_valid=False, errors=errors)
        
        validated_components.add("block_structure")
        
        # Validação completa de Proof of Work
        if not self._validate_proof_of_work(block):
            errors.append("Proof of Work inválido")
        
        validated_components.add("proof_of_work")
        
        # Validação completa de transações
        if block.transactions:
            tx_result = self.validate_transactions_incremental(block.transactions)
            if not tx_result.is_valid:
                errors.extend(tx_result.errors)
            warnings.extend(tx_result.warnings)
            validated_components.update(tx_result.validated_components)
        
        validated_components.add("transactions")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            validation_type="full",
            errors=errors,
            warnings=warnings,
            validated_components=validated_components
        )
    
    def _validate_single_transaction(self, transaction: Transaction) -> ValidationResult:
        """Valida uma única transação."""
        errors = []
        warnings = []
        
        # Validação básica da transação
        if not transaction.is_valid():
            errors.append("Transação inválida")
            return ValidationResult(is_valid=False, errors=errors)
        
        # Validação de valores não negativos
        if transaction.amount.value.to_cnb() < 0:
            errors.append("Valor negativo não permitido")
        
        if transaction.fee.value.to_cnb() < 0:
            errors.append("Taxa negativa não permitida")
        
        # Validação de endereços
        if not transaction.from_address and not transaction.to_address:
            errors.append("Pelo menos um endereço deve ser especificado")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            validation_type="single_transaction",
            errors=errors,
            warnings=warnings,
            validated_components={"transaction"}
        )
    
    def _validate_proof_of_work(self, block: Block) -> bool:
        """Valida Proof of Work do bloco."""
        try:
            # Bloco genesis sempre é válido
            if block.height == 0:
                return True
                
            import hashlib
            
            # Criar dados do bloco para hash (usar mesmo método do Block)
            block_data = {
                "height": block.height,
                "previous_hash": block.previous_hash.value if block.previous_hash else "0",
                "merkle_root": block.merkle_root.value,
                "timestamp": block.timestamp.value,
                "nonce": block.nonce,
                "difficulty": block.difficulty,
                "transactions_count": len(block.transactions)
            }
            
            import json
            block_string = json.dumps(block_data, sort_keys=True)
            block_hash = hashlib.sha256(block_string.encode()).hexdigest()
            
            # Verificar se atende à dificuldade
            target = "0" * block.difficulty
            return block_hash.startswith(target)
            
        except Exception as e:
            logger.error(f"Erro na validação de Proof of Work: {e}")
            return False
    
    def _get_cached_validation(self, key: str, validation_type: str) -> Optional[ValidationResult]:
        """Obtém validação do cache."""
        with self._lock:
            cache_dict = getattr(self.validation_cache, f"{validation_type}_validations")
            
            if key in cache_dict:
                # Verificar TTL
                if time.time() - self.validation_cache.timestamps.get(key, 0) < self.validation_cache.ttl:
                    return cache_dict[key]
                else:
                    # Cache expirado, remover
                    del cache_dict[key]
                    if key in self.validation_cache.timestamps:
                        del self.validation_cache.timestamps[key]
            
            return None
    
    def _cache_validation(self, key: str, validation_type: str, result: ValidationResult) -> None:
        """Cache resultado de validação."""
        with self._lock:
            cache_dict = getattr(self.validation_cache, f"{validation_type}_validations")
            cache_dict[key] = result
            self.validation_cache.timestamps[key] = time.time()
    
    def _update_validation_stats(self, validation_time: float) -> None:
        """Atualiza estatísticas de validação."""
        with self._lock:
            self.validation_stats["total_validations"] += 1
            self.validation_stats["total_validation_time"] += validation_time
            
            if self.validation_stats["total_validations"] > 0:
                self.validation_stats["average_validation_time"] = (
                    self.validation_stats["total_validation_time"] / 
                    self.validation_stats["total_validations"]
                )
    
    def get_validation_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de validação."""
        with self._lock:
            stats = self.validation_stats.copy()
            
            # Calcular taxa de hit do cache
            total_cache_requests = stats["cache_hits"] + stats["cache_misses"]
            if total_cache_requests > 0:
                stats["cache_hit_rate"] = stats["cache_hits"] / total_cache_requests
            else:
                stats["cache_hit_rate"] = 0.0
            
            # Estatísticas do cache
            stats["cache_sizes"] = {
                "block_validations": len(self.validation_cache.block_validations),
                "transaction_validations": len(self.validation_cache.transaction_validations),
                "chain_validations": len(self.validation_cache.chain_validations)
            }
            
            return stats
    
    def cleanup_expired_cache(self) -> int:
        """Remove entradas expiradas do cache."""
        with self._lock:
            current_time = time.time()
            expired_keys = []
            
            # Encontrar chaves expiradas
            for key, timestamp in self.validation_cache.timestamps.items():
                if current_time - timestamp > self.validation_cache.ttl:
                    expired_keys.append(key)
            
            # Remover entradas expiradas
            for key in expired_keys:
                # Remover de todos os caches
                for cache_name in ["block_validations", "transaction_validations", "chain_validations"]:
                    cache_dict = getattr(self.validation_cache, cache_name)
                    if key in cache_dict:
                        del cache_dict[key]
                
                # Remover timestamp
                if key in self.validation_cache.timestamps:
                    del self.validation_cache.timestamps[key]
            
            logger.info(f"Removidas {len(expired_keys)} entradas expiradas do cache de validação")
            return len(expired_keys)
    
    def clear_cache(self) -> None:
        """Limpa todos os caches de validação."""
        with self._lock:
            self.validation_cache.block_validations.clear()
            self.validation_cache.transaction_validations.clear()
            self.validation_cache.chain_validations.clear()
            self.validation_cache.timestamps.clear()
            
            logger.info("Cache de validação limpo completamente")


# Instância global otimizada
incremental_validator = IncrementalValidator()
