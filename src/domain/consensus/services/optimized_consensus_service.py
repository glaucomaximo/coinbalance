"""
Sistema Otimizado de Seleção de Validadores
"""

import heapq
import threading
from typing import List, Optional, Dict, Tuple
from decimal import Decimal
import random

from ..entities.validator import Validator
from ..value_objects.validator_id import ValidatorId
from ...shared.value_objects.wallet_address import WalletAddress


class OptimizedValidatorSelector:
    """
    Sistema otimizado para seleção de validadores.
    
    Usa estruturas de dados eficientes para evitar O(N²):
    - Heap para manter validadores ordenados por stake
    - Cache de seleções para evitar recálculos
    - Thread-safe operations
    """
    
    def __init__(self):
        # Heap máximo para manter validadores ordenados por stake (maior primeiro)
        self._validator_heap: List[Tuple[Decimal, ValidatorId, Validator]] = []
        self._heap_lock = threading.RLock()
        
        # Cache de seleções para evitar recálculos
        self._selection_cache: Dict[int, Validator] = {}
        self._cache_lock = threading.RLock()
        
        # Mapa para busca rápida por ID
        self._validator_map: Dict[ValidatorId, Validator] = {}
        self._map_lock = threading.RLock()
        
        # Flag para indicar se o heap precisa ser reconstruído
        self._heap_dirty = False
    
    def add_validator(self, validator: Validator) -> None:
        """Adiciona validador ao sistema"""
        with self._heap_lock, self._map_lock:
            # Adicionar ao mapa
            self._validator_map[validator.id] = validator
            
            # Marcar heap como dirty para reconstrução
            self._heap_dirty = True
            
            # Limpar cache de seleções
            with self._cache_lock:
                self._selection_cache.clear()
    
    def remove_validator(self, validator_id: ValidatorId) -> None:
        """Remove validador do sistema"""
        with self._heap_lock, self._map_lock:
            # Remover do mapa
            if validator_id in self._validator_map:
                del self._validator_map[validator_id]
            
            # Marcar heap como dirty para reconstrução
            self._heap_dirty = True
            
            # Limpar cache de seleções
            with self._cache_lock:
                self._selection_cache.clear()
    
    def update_validator_stake(self, validator_id: ValidatorId, new_stake: Decimal) -> None:
        """Atualiza stake de um validador"""
        with self._map_lock:
            if validator_id in self._validator_map:
                validator = self._validator_map[validator_id]
                validator.stake_amount = new_stake
                
                # Marcar heap como dirty
                with self._heap_lock:
                    self._heap_dirty = True
                
                # Limpar cache
                with self._cache_lock:
                    self._selection_cache.clear()
    
    def _rebuild_heap_if_needed(self) -> None:
        """Reconstrói o heap se necessário"""
        if not self._heap_dirty:
            return
        
        with self._heap_lock, self._map_lock:
            # Limpar heap atual
            self._validator_heap.clear()
            
            # Reconstruir heap com validadores ativos
            for validator in self._validator_map.values():
                if validator.is_active:
                    # Usar stake negativo para heap máximo (Python usa heap mínimo)
                    stake_power = validator.get_staking_power()
                    heapq.heappush(self._validator_heap, (-stake_power, validator.id, validator))
            
            self._heap_dirty = False
    
    def select_validator_for_round(self, round_number: int) -> Optional[Validator]:
        """
        Seleciona validador para uma rodada específica usando algoritmo otimizado.
        
        Complexidade: O(log N) para seleção, O(N log N) apenas quando heap é reconstruído
        """
        # Verificar cache primeiro
        with self._cache_lock:
            if round_number in self._selection_cache:
                return self._selection_cache[round_number]
        
        # Reconstruir heap se necessário
        self._rebuild_heap_if_needed()
        
        with self._heap_lock:
            if not self._validator_heap:
                return None
            
            # Calcular stake total para seleção probabilística
            total_stake = sum(-stake for stake, _, _ in self._validator_heap)
            
            if total_stake == 0:
                return None
            
            # Usar round_number como seed para determinismo
            random.seed(round_number)
            
            # Seleção ponderada por stake usando heap
            target = random.uniform(0, float(total_stake))
            current_sum = Decimal("0")
            
            # Criar cópia do heap para não modificar o original
            heap_copy = self._validator_heap.copy()
            
            while heap_copy:
                stake, validator_id, validator = heapq.heappop(heap_copy)
                stake_power = -stake  # Converter de volta para positivo
                
                current_sum += stake_power
                if current_sum >= Decimal(str(target)):
                    # Cachear resultado
                    with self._cache_lock:
                        self._selection_cache[round_number] = validator
                    return validator
            
            # Fallback: retornar validador com maior stake
            if self._validator_heap:
                _, _, validator = heapq.heappop(self._validator_heap)
                with self._cache_lock:
                    self._selection_cache[round_number] = validator
                return validator
        
        return None
    
    def get_top_validators(self, limit: int = 10) -> List[Validator]:
        """Retorna os top N validadores por stake"""
        self._rebuild_heap_if_needed()
        
        with self._heap_lock:
            # Criar cópia do heap
            heap_copy = self._validator_heap.copy()
            
            top_validators = []
            for _ in range(min(limit, len(heap_copy))):
                if heap_copy:
                    _, _, validator = heapq.heappop(heap_copy)
                    top_validators.append(validator)
            
            return top_validators
    
    def get_validator_count(self) -> int:
        """Retorna número de validadores ativos"""
        with self._map_lock:
            return sum(1 for v in self._validator_map.values() if v.is_active)
    
    def get_total_stake(self) -> Decimal:
        """Retorna stake total de todos os validadores ativos"""
        self._rebuild_heap_if_needed()
        
        with self._heap_lock:
            return sum(-stake for stake, _, _ in self._validator_heap)
    
    def clear_cache(self) -> None:
        """Limpa cache de seleções"""
        with self._cache_lock:
            self._selection_cache.clear()
    
    def get_validator_by_id(self, validator_id: ValidatorId) -> Optional[Validator]:
        """Busca validador por ID"""
        with self._map_lock:
            return self._validator_map.get(validator_id)


class OptimizedConsensusService:
    """
    Serviço de consenso otimizado usando o seletor de validadores eficiente.
    """
    
    def __init__(self):
        self.validator_selector = OptimizedValidatorSelector()
        self.active_validators: List[Validator] = []
        self.current_round: Optional[int] = None
        self.block_time_seconds = 5  # Configuração do BlockchainConfig
    
    def add_validator(self, validator: Validator) -> None:
        """Adiciona validador ao sistema"""
        self.validator_selector.add_validator(validator)
        if validator not in self.active_validators:
            self.active_validators.append(validator)
    
    def remove_validator(self, validator_id: ValidatorId) -> None:
        """Remove validador do sistema"""
        self.validator_selector.remove_validator(validator_id)
        self.active_validators = [v for v in self.active_validators if v.id != validator_id]
    
    def select_validator_for_round(self, round_number: int) -> Optional[Validator]:
        """Seleciona validador para uma rodada específica"""
        return self.validator_selector.select_validator_for_round(round_number)
    
    def validate_block(self, validator: Validator, block_data: dict) -> bool:
        """Valida bloco usando validador"""
        # Verificar se validador tem stake suficiente
        min_stake = Decimal("1000")  # BlockchainConfig.MIN_STAKE_FOR_VALIDATION
        
        if validator.get_staking_power() < min_stake:
            return False
        
        # Validações básicas do bloco
        required_fields = ["height", "hash", "transactions", "timestamp"]
        if not all(field in block_data for field in required_fields):
            return False
        
        # Validar transações
        transactions = block_data.get("transactions", [])
        for tx_data in transactions:
            if not self._validate_transaction(tx_data):
                return False
        
        return True
    
    def _validate_transaction(self, tx_data: dict) -> bool:
        """Valida uma transação"""
        required_fields = ["id", "from_address", "to_address", "amount", "fee"]
        return all(field in tx_data for field in required_fields)
    
    def get_consensus_stats(self) -> dict:
        """Retorna estatísticas do consenso"""
        return {
            "active_validators": self.validator_selector.get_validator_count(),
            "total_stake": float(self.validator_selector.get_total_stake()),
            "current_round": self.current_round,
            "block_time_seconds": self.block_time_seconds
        }
