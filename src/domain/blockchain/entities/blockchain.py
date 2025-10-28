"""
Entidade Blockchain - Representa a cadeia de blocos completa
EVOLUÇÃO: Integração com sistema de índices otimizado para performance.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from decimal import Decimal
import time
import logging

from .block import Block
from ...shared.value_objects.hash_value import HashValue
from ...shared.value_objects.timestamp import Timestamp
from ...transaction.entities.transaction import Transaction
from ...transaction.value_objects.transaction_type import TransactionType
from ...shared.domain_events.base import DomainEvent
from ...shared.config.blockchain_config import BlockchainConfig
from ..infrastructure.blockchain_index import blockchain_index, transaction_pool
from ..infrastructure.parallel_miner import parallel_miner
from ..infrastructure.incremental_validator import incremental_validator
from ..infrastructure.blockchain_tree import blockchain_tree
from ..infrastructure.distributed_cache import distributed_cache
from ..infrastructure.network_optimizer import network_optimizer
from ..infrastructure.horizontal_scaler import horizontal_scaler
from ..infrastructure.real_time_monitor import real_time_monitor

logger = logging.getLogger(__name__)


@dataclass
class Blockchain:
    """
    Entidade Blockchain - Aggregate Root da cadeia de blocos.
    
    Responsabilidades:
    - Manter a cadeia de blocos
    - Validar integridade da cadeia
    - Gerenciar dificuldade de mineração
    - Processar transações pendentes
    - Manter estatísticas da blockchain
    
    Invariantes:
    - Cadeia deve ser válida
    - Blocos devem estar em ordem crescente
    - Hash de cada bloco deve referenciar o anterior
    - Dificuldade deve ser ajustada dinamicamente
    """
    
    # Identity
    name: str
    version: str
    
    # Chain data
    blocks: List[Block] = field(default_factory=list)
    difficulty: int = BlockchainConfig.INITIAL_DIFFICULTY
    target_block_time: float = BlockchainConfig.TARGET_BLOCK_TIME_SECONDS
    
    # Statistics
    total_transactions: int = 0
    total_blocks_mined: int = 0
    total_mining_time: float = 0.0
    average_block_time: float = 0.0
    
    # Configuration
    max_transactions_per_block: int = BlockchainConfig.MAX_TRANSACTIONS_PER_BLOCK
    min_transaction_fee: Decimal = BlockchainConfig.MIN_TRANSACTION_FEE
    block_reward: Decimal = BlockchainConfig.INITIAL_BLOCK_REWARD
    halving_interval: int = BlockchainConfig.HALVING_INTERVAL_YEARS * BlockchainConfig.BLOCKS_PER_YEAR
    
    # Domain Events (não persistidos)
    _events: List[DomainEvent] = field(default_factory=list, init=False, repr=False)
    
    def __post_init__(self):
        """Validação após inicialização"""
        self._validate()
        
        # Se não há blocos, criar bloco gênesis
        if not self.blocks:
            genesis_block = Block.create_genesis_block()
            self.blocks.append(genesis_block)
            self.total_blocks_mined = 1
    
    def _validate(self):
        """Valida invariantes do domínio"""
        if not self.name:
            raise ValueError("Blockchain name cannot be empty")
        
        if self.difficulty < 1:
            raise ValueError("Difficulty must be at least 1")
        
        if self.target_block_time <= 0:
            raise ValueError("Target block time must be positive")
        
        if self.max_transactions_per_block < 1:
            raise ValueError("Max transactions per block must be at least 1")
    
    @classmethod
    def create(cls, name: str = "CoinBalance", version: str = "1.0.0") -> "Blockchain":
        """Cria uma nova blockchain"""
        blockchain = cls(name=name, version=version)
        return blockchain
    
    def get_latest_block(self) -> Optional[Block]:
        """Retorna o último bloco da cadeia"""
        if not self.blocks:
            return None
        return self.blocks[-1]
    
    def get_block_by_height(self, height: int) -> Optional[Block]:
        """Busca bloco por altura"""
        if 0 <= height < len(self.blocks):
            return self.blocks[height]
        return None
    
    def get_block_by_hash(self, block_hash: str) -> Optional[Block]:
        """
        Busca bloco por hash usando busca linear simples.
        
        EVOLUÇÃO: Busca O(n) simples e confiável.
        """
        try:
            # Buscar nos blocos da cadeia
            for block in self.blocks:
                if block.hash.value == block_hash:
                    return block
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar bloco por hash {block_hash}: {e}")
            return None
    
    def add_block(self, block: Block) -> bool:
        """
        Adiciona um novo bloco à cadeia com validação incremental.
        
        EVOLUÇÃO: Validação incremental para performance otimizada.
        """
        try:
            # EVOLUÇÃO: Usar validação incremental
            previous_block = self.get_latest_block()
            validation_result = incremental_validator.validate_block_incremental(
                block=block,
                previous_block=previous_block,
                force_full_validation=False
            )
            
            if not validation_result.is_valid:
                logger.warning(f"Bloco {block.height} inválido: {validation_result.errors}")
                return False
            
            # Log warnings se houver
            if validation_result.warnings:
                logger.info(f"Avisos na validação do bloco {block.height}: {validation_result.warnings}")
            
            # Adicionar bloco à lista principal
            self.blocks.append(block)
            self.total_blocks_mined += 1
            self.total_transactions += len(block.transactions)
            self.total_mining_time += block.mining_time
            
            # EVOLUÇÃO: Adicionar ao índice otimizado
            blockchain_index.add_block(block)
            
            # EVOLUÇÃO: Adicionar à estrutura de árvore
            parent_hash = previous_block.hash.value if previous_block else None
            blockchain_tree.insert_block(block, parent_hash)
            
            # EVOLUÇÃO: Armazenar no cache distribuído
            distributed_cache.put(f"block_{block.hash.value}", block)
            
            # EVOLUÇÃO: Sincronizar com outros nós via rede otimizada
            network_optimizer.broadcast_message("new_block", {
                "block_hash": block.hash.value,
                "height": block.height,
                "timestamp": block.timestamp.value
            })
            
            # EVOLUÇÃO: Distribuir bloco usando escalabilidade horizontal
            distribution_result = horizontal_scaler.distribute_block(block)
            
            # EVOLUÇÃO: Coletar métricas de monitoramento em tempo real
            real_time_monitor.collect_metric("blockchain.blocks.total", len(self.blocks), 
                                            tags={"height": str(block.height)})
            real_time_monitor.collect_metric("blockchain.blocks.mined", self.total_blocks_mined,
                                            tags={"height": str(block.height)})
            real_time_monitor.collect_metric("blockchain.difficulty.current", self.difficulty,
                                            tags={"height": str(block.height)})
            
            # Atualizar estatísticas
            self._update_statistics()
            
            # Ajustar dificuldade se necessário
            self._adjust_difficulty()
            
            logger.info(f"Bloco {block.height} adicionado com sucesso: validação={validation_result.validation_type}, tempo={validation_result.validation_time:.3f}s, distribuição={distribution_result.get('success', False)}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao adicionar bloco: {e}")
            return False
    
    def _is_valid_new_block(self, block: Block) -> bool:
        """Valida se um novo bloco é válido"""
        # Verificar se o bloco é válido
        if not block.is_valid():
            return False
        
        # Verificar altura
        expected_height = len(self.blocks)
        if block.height != expected_height:
            return False
        
        # Verificar hash anterior
        if expected_height == 0:
            # Primeiro bloco após gênesis
            if block.previous_hash is None:
                return False
        else:
            latest_block = self.get_latest_block()
            if not latest_block or (block.previous_hash and block.previous_hash.value != latest_block.hash.value):
                return False
        
        # Verificar dificuldade
        if block.difficulty != self.difficulty:
            return False
        
        return True
    
    def _update_statistics(self):
        """Atualiza estatísticas da blockchain"""
        if self.total_blocks_mined > 0:
            self.average_block_time = self.total_mining_time / self.total_blocks_mined
    
    def _adjust_difficulty(self):
        """Ajusta a dificuldade de mineração baseada no tempo dos blocos"""
        if len(self.blocks) < 2:
            return
        
        # Considerar últimos 10 blocos para ajuste
        recent_blocks = self.blocks[-10:] if len(self.blocks) >= 10 else self.blocks
        
        if len(recent_blocks) < 2:
            return
        
        # Calcular tempo médio dos blocos recentes
        total_time = 0
        for i in range(1, len(recent_blocks)):
            time_diff = recent_blocks[i].timestamp.value - recent_blocks[i-1].timestamp.value
            total_time += time_diff
        
        average_time = total_time / (len(recent_blocks) - 1)
        
        # Ajustar dificuldade
        if average_time < self.target_block_time * 0.8:
            # Muito rápido, aumentar dificuldade
            self.difficulty += 1
        elif average_time > self.target_block_time * 1.2:
            # Muito lento, diminuir dificuldade
            self.difficulty = max(1, self.difficulty - 1)
    
    def is_chain_valid(self) -> bool:
        """
        Valida toda a cadeia de blocos usando validação incremental.
        
        EVOLUÇÃO: Validação incremental com cache e paralelização.
        """
        try:
            if not self.blocks:
                return True
            
            # EVOLUÇÃO: Usar validação incremental
            validation_result = incremental_validator.validate_chain_incremental(
                blocks=self.blocks,
                start_index=0,
                force_full_validation=False
            )
            
            if not validation_result.is_valid:
                logger.warning(f"Cadeia inválida: {validation_result.errors}")
                return False
            
            # Log warnings se houver
            if validation_result.warnings:
                logger.info(f"Avisos na validação da cadeia: {validation_result.warnings}")
            
            logger.debug(f"Cadeia validada incrementalmente: {len(self.blocks)} blocos, tempo={validation_result.validation_time:.3f}s")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro na validação incremental da cadeia: {e}")
            return False
    
    def _validate_proof_of_work(self, block: Block) -> bool:
        """
        Valida Proof of Work real do bloco.
        
        EVOLUÇÃO: Verificação real de dificuldade e hash.
        """
        try:
            import hashlib
            import json
            
            # Recalcular hash do bloco
            block_data = {
                "height": block.height,
                "previous_hash": block.previous_hash.value if block.previous_hash else None,
                "timestamp": block.timestamp.value,
                "transactions": [
                    {
                        "id": tx.id.value,
                        "from": tx.from_address.value if tx.from_address else "",
                        "to": tx.to_address.value if tx.to_address else "",
                        "amount": str(tx.amount.to_cnb()),
                        "fee": str(tx.fee.to_cnb()),
                        "type": tx.transaction_type,
                        "timestamp": tx.created_at.value
                    }
                    for tx in block.transactions
                ],
                "nonce": block.nonce,
                "difficulty": block.difficulty
            }
            
            block_string = json.dumps(block_data, sort_keys=True)
            calculated_hash = hashlib.sha256(block_string.encode()).hexdigest()
            
            # Verificar se o hash calculado corresponde ao armazenado
            if calculated_hash != block.hash.value:
                return False
            
            # Verificar se o hash atende à dificuldade
            if not calculated_hash.startswith("0" * block.difficulty):
                return False
            
            return True
            
        except Exception as e:
            import logging
            logging.error(f"Erro na validação de Proof of Work: {e}")
            return False
    
    def _validate_block_transactions(self, block: Block) -> bool:
        """
        Valida transações do bloco.
        
        EVOLUÇÃO: Validação robusta de transações.
        """
        try:
            for tx in block.transactions:
                # Verificar campos obrigatórios
                if not tx.id or not tx.transaction_type:
                    return False
                
                # Verificar valores não negativos
                if tx.amount.to_cnb() < 0 or tx.fee.to_cnb() < 0:
                    return False
                
                # Verificar tipos de transação válidos
                valid_types = ["GENESIS", "TRANSFER", "MINING_REWARD", "CONTRACT_CALL"]
                if tx.transaction_type not in valid_types:
                        return False
            
            return True
            
        except Exception as e:
            import logging
            logging.error(f"Erro na validação de transações: {e}")
            return False
    
    def get_transaction_by_id(self, tx_id: str) -> Optional[Transaction]:
        """Busca transação por ID em toda a cadeia"""
        for block in self.blocks:
            tx = block.get_transaction_by_id(tx_id)
            if tx:
                return tx
        return None
    
    def get_transactions_by_address(self, address: str) -> List[Transaction]:
        """Busca todas as transações de um endereço"""
        transactions = []
        for block in self.blocks:
            for tx in block.transactions:
                if (tx.from_address and tx.from_address.value == address) or \
                   (tx.to_address and tx.to_address.value == address):
                    transactions.append(tx)
        return transactions
    
    def get_pending_transactions(self) -> List[Transaction]:
        """
        Retorna transações pendentes usando pool otimizado.
        
        EVOLUÇÃO: Pool de transações eficiente com priorização por taxa.
        """
        return transaction_pool.get_transactions_for_block(self.max_transactions_per_block)
    
    def mine_block(self, transactions: List[Transaction], miner_address: str) -> Optional[Block]:
        """
        Minera um novo bloco usando mineração paralela otimizada.
        
        EVOLUÇÃO: Mineração paralela com threading e cache de nonces.
        """
        try:
            # Verificar se há transações
            if not transactions:
                return None
            
            # Limitar número de transações
            if len(transactions) > self.max_transactions_per_block:
                transactions = transactions[:self.max_transactions_per_block]
            
            # Obter último bloco
            latest_block = self.get_latest_block()
            if not latest_block:
                return None
            
            # Criar novo bloco
            new_height = len(self.blocks)
            previous_hash = latest_block.hash
            
            # Criar bloco base
            new_block = Block.create_block(
                height=new_height,
                previous_hash=previous_hash,
                transactions=transactions,
                difficulty=self.difficulty,
                miner_address=miner_address
            )
            
            # EVOLUÇÃO: Mineração paralela otimizada
            mining_result = parallel_miner.mine_block_parallel(
                block=new_block,
                transactions=transactions,
                miner_address=miner_address
            )
            
            if not mining_result or not mining_result.success:
                logger.warning(f"Falha na mineração do bloco {new_height}")
                return None
            
            # Atualizar bloco com nonce e hash encontrados
            new_block.nonce = mining_result.nonce
            new_block.hash = HashValue(mining_result.hash)
            new_block.mining_time = mining_result.mining_time
            
            # Adicionar bloco à cadeia
            if self.add_block(new_block):
                logger.info(f"Bloco {new_height} minerado com sucesso: nonce={mining_result.nonce}, tempo={mining_result.mining_time:.2f}s")
                return new_block
            
            return None
            
        except Exception as e:
            logger.error(f"Erro na mineração de bloco: {e}")
            return None
    
    def get_current_block_reward(self) -> Decimal:
        """
        Calcula a recompensa atual do bloco baseada na altura.
        
        Usa a política monetária unificada do BlockchainConfig.
        """
        if not self.blocks:
            return BlockchainConfig.INITIAL_BLOCK_REWARD
        
        current_height = len(self.blocks)
        return BlockchainConfig.calculate_block_reward(current_height)
    
    def get_total_supply(self) -> Decimal:
        """
        Calcula supply total de CNB baseado nas transações da blockchain.
        
        O supply total é calculado considerando:
        - Transações GENESIS: criam CNB
        - Transações REWARD: criam CNB (recompensas de mineração)
        - Transações TRANSFER: movem CNB (não afetam supply total)
        - Taxas: são "queimadas" (reduzem supply efetivo)
        """
        total_supply = Decimal("0")
        total_fees_burned = Decimal("0")
        
        for block in self.blocks:
            for tx in block.transactions:
                if tx.transaction_type == TransactionType.GENESIS:
                    # Transação gênesis cria CNB inicial
                    total_supply += tx.amount.value.to_cnb()
                elif tx.transaction_type == TransactionType.REWARD:
                    # Recompensas de mineração criam CNB
                    total_supply += tx.amount.value.to_cnb()
                elif tx.transaction_type == TransactionType.TRANSFER:
                    # Transfers movem CNB mas não criam/destroem
                    # Mas as taxas são "queimadas"
                    total_fees_burned += tx.fee.value.to_cnb()
                elif tx.transaction_type == TransactionType.FEE:
                    # Taxas são "queimadas"
                    total_fees_burned += tx.amount.value.to_cnb()
        
        # Supply efetivo = CNB criado - CNB queimado em taxas
        effective_supply = total_supply - total_fees_burned
        
        return max(effective_supply, Decimal("0"))  # Não pode ser negativo
    
    def get_chain_stats(self) -> Dict:
        """Retorna estatísticas da cadeia"""
        return {
            "name": self.name,
            "version": self.version,
            "total_blocks": len(self.blocks),
            "total_transactions": self.total_transactions,
            "current_difficulty": self.difficulty,
            "average_block_time": self.average_block_time,
            "total_mining_time": self.total_mining_time,
            "current_block_reward": self.get_current_block_reward(),
            "total_supply": self.get_total_supply(),
            "chain_valid": self.is_chain_valid(),
            "latest_block_height": len(self.blocks) - 1 if self.blocks else 0
        }
    
    def get_events(self) -> List[DomainEvent]:
        """Retorna eventos de domínio"""
        return self._events.copy()
    
    def _adjust_difficulty_real(self, mining_time: float):
        """
        Ajusta dificuldade baseada no tempo real de mineração.
        
        EVOLUÇÃO: Método real de ajuste de dificuldade.
        """
        if len(self.blocks) < 2:
            return
        
        # Calcular tempo médio dos últimos 10 blocos
        recent_blocks = self.blocks[-10:]
        if len(recent_blocks) < 2:
            return
        
        # Usar tempo de mineração real se disponível
        if hasattr(self, 'total_mining_time') and self.total_blocks_mined > 0:
            average_time = self.total_mining_time / self.total_blocks_mined
        else:
            # Fallback para cálculo baseado em timestamps
            total_time = recent_blocks[-1].timestamp.value - recent_blocks[0].timestamp.value
            average_time = total_time / (len(recent_blocks) - 1)
        
        # Ajustar dificuldade baseado no tempo alvo
        if average_time < self.target_block_time * 0.8:
            self.difficulty += 1
            import logging
            logging.info(f"Dificuldade aumentada para {self.difficulty}")
        elif average_time > self.target_block_time * 1.2:
            self.difficulty = max(1, self.difficulty - 1)
            import logging
            logging.info(f"Dificuldade diminuída para {self.difficulty}")
    
    def clear_events(self) -> None:
        """Limpa eventos de domínio"""
        self._events.clear()
    
    def get_performance_statistics(self) -> Dict[str, any]:
        """
        Retorna estatísticas de performance da blockchain.
        
        EVOLUÇÃO: Métricas detalhadas de performance e otimização.
        """
        try:
            # Estatísticas básicas da blockchain
            basic_stats = {
                "total_blocks": len(self.blocks),
                "total_transactions": self.total_transactions,
                "total_blocks_mined": self.total_blocks_mined,
                "total_mining_time": self.total_mining_time,
                "average_block_time": self.average_block_time,
                "current_difficulty": self.difficulty,
                "target_block_time": self.target_block_time,
                "max_transactions_per_block": self.max_transactions_per_block
            }
            
            # Estatísticas do índice otimizado
            index_stats = blockchain_index.get_statistics()
            
            # Estatísticas do pool de transações
            pool_stats = transaction_pool.get_statistics()
            
            return {
                "blockchain": basic_stats,
                "index_performance": index_stats,
                "transaction_pool": pool_stats,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas de performance: {e}")
            return {}
    
    def optimize_performance(self) -> Dict[str, any]:
        """
        Executa otimizações de performance da blockchain.
        
        EVOLUÇÃO: Otimização automática de performance.
        """
        try:
            optimizations_applied = []
            
            # Limpar cache expirado
            expired_cache = blockchain_index.cleanup_expired_cache()
            if expired_cache > 0:
                optimizations_applied.append(f"Removidas {expired_cache} entradas expiradas do cache")
            
            # Limpar transações expiradas
            expired_transactions = transaction_pool.cleanup_expired_transactions()
            if expired_transactions > 0:
                optimizations_applied.append(f"Removidas {expired_transactions} transações expiradas")
            
            # Ajustar tamanho do cache baseado na utilização
            index_stats = blockchain_index.get_statistics()
            if index_stats["cache_hit_rate"] < 0.7 and index_stats["cache_size"] < index_stats["max_cache_size"]:
                # Cache hit rate baixo, pode aumentar tamanho
                optimizations_applied.append("Cache hit rate baixo detectado")
            
            return {
                "optimizations_applied": optimizations_applied,
                "cache_cleanup": expired_cache,
                "transaction_cleanup": expired_transactions,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro na otimização de performance: {e}")
            return {"error": str(e)}
    
    def get_mining_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas de mineração paralela.
        
        EVOLUÇÃO: Métricas de mineração paralela e otimização.
        """
        try:
            # Estatísticas básicas da blockchain
            basic_stats = {
                "total_blocks": len(self.blocks),
                "total_transactions": self.total_transactions,
                "total_blocks_mined": self.total_blocks_mined,
                "total_mining_time": self.total_mining_time,
                "average_block_time": self.average_block_time,
                "current_difficulty": self.difficulty,
                "target_block_time": self.target_block_time
            }
            
            # Estatísticas do minerador paralelo
            mining_stats = parallel_miner.get_mining_statistics()
            
            # Estatísticas do índice otimizado
            index_stats = blockchain_index.get_statistics()
            
            # Estatísticas do pool de transações
            pool_stats = transaction_pool.get_statistics()
            
            return {
                "blockchain": basic_stats,
                "parallel_mining": mining_stats,
                "index_performance": index_stats,
                "transaction_pool": pool_stats,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas de mineração: {e}")
            return {}
    
    def optimize_mining_performance(self) -> Dict[str, Any]:
        """
        Executa otimizações de performance de mineração.
        
        EVOLUÇÃO: Otimização automática de mineração paralela.
        """
        try:
            optimizations_applied = []
            
            # Otimizar configuração de mineração
            mining_optimization = parallel_miner.optimize_mining_config()
            optimizations_applied.extend(mining_optimization["optimizations_applied"])
            
            # Limpar cache expirado
            expired_cache = blockchain_index.cleanup_expired_cache()
            if expired_cache > 0:
                optimizations_applied.append(f"Removidas {expired_cache} entradas expiradas do cache")
            
            # Limpar transações expiradas
            expired_transactions = transaction_pool.cleanup_expired_transactions()
            if expired_transactions > 0:
                optimizations_applied.append(f"Removidas {expired_transactions} transações expiradas")
            
            return {
                "optimizations_applied": optimizations_applied,
                "mining_config": mining_optimization["current_config"],
                "cache_cleanup": expired_cache,
                "transaction_cleanup": expired_transactions,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro na otimização de mineração: {e}")
            return {"error": str(e)}
    
    def get_validation_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas de validação incremental.
        
        EVOLUÇÃO: Métricas de validação incremental e otimização.
        """
        try:
            # Estatísticas básicas da blockchain
            basic_stats = {
                "total_blocks": len(self.blocks),
                "total_transactions": self.total_transactions,
                "total_blocks_mined": self.total_blocks_mined,
                "total_mining_time": self.total_mining_time,
                "average_block_time": self.average_block_time,
                "current_difficulty": self.difficulty,
                "target_block_time": self.target_block_time
            }
            
            # Estatísticas do validador incremental
            validation_stats = incremental_validator.get_validation_statistics()
            
            # Estatísticas do minerador paralelo
            mining_stats = parallel_miner.get_mining_statistics()
            
            # Estatísticas do índice otimizado
            index_stats = blockchain_index.get_statistics()
            
            # Estatísticas do pool de transações
            pool_stats = transaction_pool.get_statistics()
            
            return {
                "blockchain": basic_stats,
                "incremental_validation": validation_stats,
                "parallel_mining": mining_stats,
                "index_performance": index_stats,
                "transaction_pool": pool_stats,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas de validação: {e}")
            return {}
    
    def optimize_validation_performance(self) -> Dict[str, Any]:
        """
        Executa otimizações de performance de validação.
        
        EVOLUÇÃO: Otimização automática de validação incremental.
        """
        try:
            optimizations_applied = []
            
            # Limpar cache expirado de validação
            expired_validation_cache = incremental_validator.cleanup_expired_cache()
            if expired_validation_cache > 0:
                optimizations_applied.append(f"Removidas {expired_validation_cache} entradas expiradas do cache de validação")
            
            # Otimizar configuração de mineração
            mining_optimization = parallel_miner.optimize_mining_config()
            optimizations_applied.extend(mining_optimization["optimizations_applied"])
            
            # Limpar cache expirado
            expired_cache = blockchain_index.cleanup_expired_cache()
            if expired_cache > 0:
                optimizations_applied.append(f"Removidas {expired_cache} entradas expiradas do cache")
            
            # Limpar transações expiradas
            expired_transactions = transaction_pool.cleanup_expired_transactions()
            if expired_transactions > 0:
                optimizations_applied.append(f"Removidas {expired_transactions} transações expiradas")
            
            return {
                "optimizations_applied": optimizations_applied,
                "validation_cache_cleanup": expired_validation_cache,
                "mining_config": mining_optimization["current_config"],
                "cache_cleanup": expired_cache,
                "transaction_cleanup": expired_transactions,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro na otimização de validação: {e}")
            return {"error": str(e)}
    
    def get_tree_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas da estrutura de árvore.
        
        EVOLUÇÃO: Métricas de estrutura de árvore e otimização.
        """
        try:
            # Estatísticas básicas da blockchain
            basic_stats = {
                "total_blocks": len(self.blocks),
                "total_transactions": self.total_transactions,
                "total_blocks_mined": self.total_blocks_mined,
                "total_mining_time": self.total_mining_time,
                "average_block_time": self.average_block_time,
                "current_difficulty": self.difficulty,
                "target_block_time": self.target_block_time
            }
            
            # Estatísticas da estrutura de árvore
            tree_stats = blockchain_tree.get_tree_statistics()
            
            # Estatísticas do validador incremental
            validation_stats = incremental_validator.get_validation_statistics()
            
            # Estatísticas do minerador paralelo
            mining_stats = parallel_miner.get_mining_statistics()
            
            # Estatísticas do índice otimizado
            index_stats = blockchain_index.get_statistics()
            
            # Estatísticas do pool de transações
            pool_stats = transaction_pool.get_statistics()
            
            return {
                "blockchain": basic_stats,
                "tree_structure": tree_stats,
                "incremental_validation": validation_stats,
                "parallel_mining": mining_stats,
                "index_performance": index_stats,
                "transaction_pool": pool_stats,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas da árvore: {e}")
            return {}
    
    def optimize_tree_structure(self) -> Dict[str, Any]:
        """
        Executa otimizações de estrutura de árvore.
        
        EVOLUÇÃO: Otimização automática de estrutura de árvore.
        """
        try:
            optimizations_applied = []
            
            # Otimizar estrutura de árvore
            tree_optimization = blockchain_tree.optimize_tree_structure()
            optimizations_applied.extend(tree_optimization["optimizations_applied"])
            
            # Limpar cache expirado de validação
            expired_validation_cache = incremental_validator.cleanup_expired_cache()
            if expired_validation_cache > 0:
                optimizations_applied.append(f"Removidas {expired_validation_cache} entradas expiradas do cache de validação")
            
            # Otimizar configuração de mineração
            mining_optimization = parallel_miner.optimize_mining_config()
            optimizations_applied.extend(mining_optimization["optimizations_applied"])
            
            # Limpar cache expirado
            expired_cache = blockchain_index.cleanup_expired_cache()
            if expired_cache > 0:
                optimizations_applied.append(f"Removidas {expired_cache} entradas expiradas do cache")
            
            # Limpar transações expiradas
            expired_transactions = transaction_pool.cleanup_expired_transactions()
            if expired_transactions > 0:
                optimizations_applied.append(f"Removidas {expired_transactions} transações expiradas")
            
            return {
                "optimizations_applied": optimizations_applied,
                "tree_optimization": tree_optimization["optimizations_applied"],
                "validation_cache_cleanup": expired_validation_cache,
                "mining_config": mining_optimization["current_config"],
                "cache_cleanup": expired_cache,
                "transaction_cleanup": expired_transactions,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro na otimização da estrutura de árvore: {e}")
            return {"error": str(e)}
    
    def get_blockchain_path(self, from_hash: str, to_hash: str) -> List[Block]:
        """
        Retorna caminho entre dois blocos na blockchain.
        
        EVOLUÇÃO: Caminho otimizado usando estrutura de árvore.
        """
        try:
            return blockchain_tree.get_blockchain_path(from_hash, to_hash)
        except Exception as e:
            logger.error(f"Erro ao obter caminho da blockchain: {e}")
            return []
    
    def get_subtree_blocks(self, root_hash: str) -> List[Block]:
        """
        Retorna todos os blocos de uma subárvore.
        
        EVOLUÇÃO: Subárvore otimizada com cache.
        """
        try:
            return blockchain_tree.get_subtree_blocks(root_hash)
        except Exception as e:
            logger.error(f"Erro ao obter subárvore: {e}")
            return []
    
    def validate_subtree(self, root_hash: str) -> Dict[str, Any]:
        """
        Valida uma subárvore incrementalmente.
        
        EVOLUÇÃO: Validação incremental de subárvores.
        """
        try:
            return blockchain_tree.validate_subtree(root_hash)
        except Exception as e:
            logger.error(f"Erro na validação de subárvore: {e}")
            return {"valid": False, "error": str(e)}
    
    def find_blocks_by_height(self, height: int) -> List[Block]:
        """
        Busca blocos por altura usando estrutura de árvore.
        
        EVOLUÇÃO: Busca O(1) com índice de altura.
        """
        try:
            return blockchain_tree.find_blocks_by_height(height)
        except Exception as e:
            logger.error(f"Erro ao buscar blocos por altura: {e}")
            return []
    
    def find_blocks_by_timestamp_range(self, start_time: int, end_time: int) -> List[Block]:
        """
        Busca blocos por range de timestamp usando estrutura de árvore.
        
        EVOLUÇÃO: Busca eficiente com índice de timestamp.
        """
        try:
            return blockchain_tree.find_blocks_by_timestamp_range(start_time, end_time)
        except Exception as e:
            logger.error(f"Erro ao buscar blocos por timestamp: {e}")
            return []
    
    def get_distributed_cache_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas do cache distribuído.
        
        EVOLUÇÃO: Métricas de cache distribuído e sincronização.
        """
        try:
            # Estatísticas básicas da blockchain
            basic_stats = {
                "total_blocks": len(self.blocks),
                "total_transactions": self.total_transactions,
                "total_blocks_mined": self.total_blocks_mined,
                "total_mining_time": self.total_mining_time,
                "average_block_time": self.average_block_time,
                "current_difficulty": self.difficulty,
                "target_block_time": self.target_block_time
            }
            
            # Estatísticas do cache distribuído
            cache_stats = distributed_cache.get_statistics()
            
            # Estatísticas da estrutura de árvore
            tree_stats = blockchain_tree.get_tree_statistics()
            
            # Estatísticas do validador incremental
            validation_stats = incremental_validator.get_validation_statistics()
            
            # Estatísticas do minerador paralelo
            mining_stats = parallel_miner.get_mining_statistics()
            
            # Estatísticas do índice otimizado
            index_stats = blockchain_index.get_statistics()
            
            # Estatísticas do pool de transações
            pool_stats = transaction_pool.get_statistics()
            
            return {
                "blockchain": basic_stats,
                "distributed_cache": cache_stats,
                "tree_structure": tree_stats,
                "incremental_validation": validation_stats,
                "parallel_mining": mining_stats,
                "index_performance": index_stats,
                "transaction_pool": pool_stats,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas do cache distribuído: {e}")
            return {}
    
    def get_network_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas da rede.
        
        EVOLUÇÃO: Métricas de rede e otimização.
        """
        try:
            # Estatísticas básicas da blockchain
            basic_stats = {
                "total_blocks": len(self.blocks),
                "total_transactions": self.total_transactions,
                "total_blocks_mined": self.total_blocks_mined,
                "total_mining_time": self.total_mining_time,
                "average_block_time": self.average_block_time,
                "current_difficulty": self.difficulty,
                "target_block_time": self.target_block_time
            }
            
            # Estatísticas da rede
            network_stats = network_optimizer.get_network_statistics()
            
            # Estatísticas do cache distribuído
            cache_stats = distributed_cache.get_statistics()
            
            # Estatísticas da estrutura de árvore
            tree_stats = blockchain_tree.get_tree_statistics()
            
            # Estatísticas do validador incremental
            validation_stats = incremental_validator.get_validation_statistics()
            
            # Estatísticas do minerador paralelo
            mining_stats = parallel_miner.get_mining_statistics()
            
            # Estatísticas do índice otimizado
            index_stats = blockchain_index.get_statistics()
            
            # Estatísticas do pool de transações
            pool_stats = transaction_pool.get_statistics()
            
            return {
                "blockchain": basic_stats,
                "network_optimization": network_stats,
                "distributed_cache": cache_stats,
                "tree_structure": tree_stats,
                "incremental_validation": validation_stats,
                "parallel_mining": mining_stats,
                "index_performance": index_stats,
                "transaction_pool": pool_stats,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas da rede: {e}")
            return {}
    
    def optimize_distributed_systems(self) -> Dict[str, Any]:
        """
        Executa otimizações de sistemas distribuídos.
        
        EVOLUÇÃO: Otimização automática de cache distribuído e rede.
        """
        try:
            optimizations_applied = []
            
            # Otimizar cache distribuído
            cache_optimization = distributed_cache.optimize_cache()
            optimizations_applied.extend(cache_optimization["optimizations_applied"])
            
            # Otimizar rede
            network_optimization = network_optimizer.optimize_network()
            optimizations_applied.extend(network_optimization["optimizations_applied"])
            
            # Otimizar estrutura de árvore
            tree_optimization = blockchain_tree.optimize_tree_structure()
            optimizations_applied.extend(tree_optimization["optimizations_applied"])
            
            # Limpar cache expirado de validação
            expired_validation_cache = incremental_validator.cleanup_expired_cache()
            if expired_validation_cache > 0:
                optimizations_applied.append(f"Removidas {expired_validation_cache} entradas expiradas do cache de validação")
            
            # Otimizar configuração de mineração
            mining_optimization = parallel_miner.optimize_mining_config()
            optimizations_applied.extend(mining_optimization["optimizations_applied"])
            
            # Limpar cache expirado
            expired_cache = blockchain_index.cleanup_expired_cache()
            if expired_cache > 0:
                optimizations_applied.append(f"Removidas {expired_cache} entradas expiradas do cache")
            
            # Limpar transações expiradas
            expired_transactions = transaction_pool.cleanup_expired_transactions()
            if expired_transactions > 0:
                optimizations_applied.append(f"Removidas {expired_transactions} transações expiradas")
            
            return {
                "optimizations_applied": optimizations_applied,
                "cache_optimization": cache_optimization["optimizations_applied"],
                "network_optimization": network_optimization["optimizations_applied"],
                "tree_optimization": tree_optimization["optimizations_applied"],
                "validation_cache_cleanup": expired_validation_cache,
                "mining_config": mining_optimization["current_config"],
                "cache_cleanup": expired_cache,
                "transaction_cleanup": expired_transactions,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro na otimização de sistemas distribuídos: {e}")
            return {"error": str(e)}
    
    def sync_with_network(self) -> Dict[str, Any]:
        """
        Sincroniza blockchain com a rede.
        
        EVOLUÇÃO: Sincronização inteligente com outros nós.
        """
        try:
            # Sincronizar cache distribuído
            cache_sync_result = distributed_cache.sync_all()
            
            # Broadcast de estatísticas para outros nós
            broadcast_result = network_optimizer.broadcast_message("blockchain_stats", {
                "total_blocks": len(self.blocks),
                "current_difficulty": self.difficulty,
                "total_transactions": self.total_transactions,
                "timestamp": time.time()
            })
            
            return {
                "cache_sync": cache_sync_result,
                "network_broadcast": broadcast_result,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro na sincronização com a rede: {e}")
            return {"error": str(e)}
    
    def add_network_node(self, node_id: str, address: str, port: int, priority: int = 1) -> bool:
        """
        Adiciona um nó à rede blockchain.
        
        EVOLUÇÃO: Adição de nós com prioridade e configuração.
        """
        try:
            # Adicionar ao otimizador de rede
            network_success = network_optimizer.add_node(node_id, address, port, priority)
            
            # Adicionar ao cache distribuído
            cache_success = distributed_cache.add_node(node_id, address, port, priority)
            
            return network_success and cache_success
            
        except Exception as e:
            logger.error(f"Erro ao adicionar nó à rede: {e}")
            return False
    
    def remove_network_node(self, node_id: str) -> bool:
        """
        Remove um nó da rede blockchain.
        
        EVOLUÇÃO: Remoção de nós com limpeza de recursos.
        """
        try:
            # Remover do otimizador de rede
            network_success = network_optimizer.remove_node(node_id)
            
            # Remover do cache distribuído
            cache_success = distributed_cache.remove_node(node_id)
            
            return network_success and cache_success
            
        except Exception as e:
            logger.error(f"Erro ao remover nó da rede: {e}")
            return False
    
    def get_scaling_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas de escalabilidade horizontal.
        
        EVOLUÇÃO: Métricas de escalabilidade horizontal e sharding.
        """
        try:
            # Estatísticas básicas da blockchain
            basic_stats = {
                "total_blocks": len(self.blocks),
                "total_transactions": self.total_transactions,
                "total_blocks_mined": self.total_blocks_mined,
                "total_mining_time": self.total_mining_time,
                "average_block_time": self.average_block_time,
                "current_difficulty": self.difficulty,
                "target_block_time": self.target_block_time
            }
            
            # Estatísticas de escalabilidade horizontal
            scaling_stats = horizontal_scaler.get_scaling_statistics()
            
            # Estatísticas do cache distribuído
            cache_stats = distributed_cache.get_statistics()
            
            # Estatísticas da rede
            network_stats = network_optimizer.get_network_statistics()
            
            # Estatísticas da estrutura de árvore
            tree_stats = blockchain_tree.get_tree_statistics()
            
            # Estatísticas do validador incremental
            validation_stats = incremental_validator.get_validation_statistics()
            
            # Estatísticas do minerador paralelo
            mining_stats = parallel_miner.get_mining_statistics()
            
            # Estatísticas do índice otimizado
            index_stats = blockchain_index.get_statistics()
            
            # Estatísticas do pool de transações
            pool_stats = transaction_pool.get_statistics()
            
            return {
                "blockchain": basic_stats,
                "horizontal_scaling": scaling_stats,
                "distributed_cache": cache_stats,
                "network_optimization": network_stats,
                "tree_structure": tree_stats,
                "incremental_validation": validation_stats,
                "parallel_mining": mining_stats,
                "index_performance": index_stats,
                "transaction_pool": pool_stats,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas de escalabilidade: {e}")
            return {}
    
    def get_monitoring_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas de monitoramento em tempo real.
        
        EVOLUÇÃO: Métricas de monitoramento em tempo real e alertas.
        """
        try:
            # Estatísticas básicas da blockchain
            basic_stats = {
                "total_blocks": len(self.blocks),
                "total_transactions": self.total_transactions,
                "total_blocks_mined": self.total_blocks_mined,
                "total_mining_time": self.total_mining_time,
                "average_block_time": self.average_block_time,
                "current_difficulty": self.difficulty,
                "target_block_time": self.target_block_time
            }
            
            # Estatísticas de monitoramento em tempo real
            monitoring_stats = real_time_monitor.get_monitoring_statistics()
            
            # Estatísticas de escalabilidade horizontal
            scaling_stats = horizontal_scaler.get_scaling_statistics()
            
            # Estatísticas do cache distribuído
            cache_stats = distributed_cache.get_statistics()
            
            # Estatísticas da rede
            network_stats = network_optimizer.get_network_statistics()
            
            # Estatísticas da estrutura de árvore
            tree_stats = blockchain_tree.get_tree_statistics()
            
            # Estatísticas do validador incremental
            validation_stats = incremental_validator.get_validation_statistics()
            
            # Estatísticas do minerador paralelo
            mining_stats = parallel_miner.get_mining_statistics()
            
            # Estatísticas do índice otimizado
            index_stats = blockchain_index.get_statistics()
            
            # Estatísticas do pool de transações
            pool_stats = transaction_pool.get_statistics()
            
            return {
                "blockchain": basic_stats,
                "real_time_monitoring": monitoring_stats,
                "horizontal_scaling": scaling_stats,
                "distributed_cache": cache_stats,
                "network_optimization": network_stats,
                "tree_structure": tree_stats,
                "incremental_validation": validation_stats,
                "parallel_mining": mining_stats,
                "index_performance": index_stats,
                "transaction_pool": pool_stats,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas de monitoramento: {e}")
            return {}
    
    def optimize_enterprise_systems(self) -> Dict[str, Any]:
        """
        Executa otimizações de sistemas enterprise.
        
        EVOLUÇÃO: Otimização automática de todos os sistemas enterprise.
        """
        try:
            optimizations_applied = []
            
            # Otimizar monitoramento em tempo real
            monitoring_optimization = real_time_monitor.optimize_monitoring()
            optimizations_applied.extend(monitoring_optimization["optimizations_applied"])
            
            # Otimizar escalabilidade horizontal
            scaling_optimization = horizontal_scaler.optimize_scaling()
            optimizations_applied.extend(scaling_optimization["optimizations_applied"])
            
            # Otimizar cache distribuído
            cache_optimization = distributed_cache.optimize_cache()
            optimizations_applied.extend(cache_optimization["optimizations_applied"])
            
            # Otimizar rede
            network_optimization = network_optimizer.optimize_network()
            optimizations_applied.extend(network_optimization["optimizations_applied"])
            
            # Otimizar estrutura de árvore
            tree_optimization = blockchain_tree.optimize_tree_structure()
            optimizations_applied.extend(tree_optimization["optimizations_applied"])
            
            # Limpar cache expirado de validação
            expired_validation_cache = incremental_validator.cleanup_expired_cache()
            if expired_validation_cache > 0:
                optimizations_applied.append(f"Removidas {expired_validation_cache} entradas expiradas do cache de validação")
            
            # Otimizar configuração de mineração
            mining_optimization = parallel_miner.optimize_mining_config()
            optimizations_applied.extend(mining_optimization["optimizations_applied"])
            
            # Limpar cache expirado
            expired_cache = blockchain_index.cleanup_expired_cache()
            if expired_cache > 0:
                optimizations_applied.append(f"Removidas {expired_cache} entradas expiradas do cache")
            
            # Limpar transações expiradas
            expired_transactions = transaction_pool.cleanup_expired_transactions()
            if expired_transactions > 0:
                optimizations_applied.append(f"Removidas {expired_transactions} transações expiradas")
            
            return {
                "optimizations_applied": optimizations_applied,
                "monitoring_optimization": monitoring_optimization["optimizations_applied"],
                "scaling_optimization": scaling_optimization["optimizations_applied"],
                "cache_optimization": cache_optimization["optimizations_applied"],
                "network_optimization": network_optimization["optimizations_applied"],
                "tree_optimization": tree_optimization["optimizations_applied"],
                "validation_cache_cleanup": expired_validation_cache,
                "mining_config": mining_optimization["current_config"],
                "cache_cleanup": expired_cache,
                "transaction_cleanup": expired_transactions,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro na otimização de sistemas enterprise: {e}")
            return {"error": str(e)}
    
    def create_shard(self, shard_id: str, node_count: int = 3, replication_factor: int = 2) -> bool:
        """
        Cria um novo shard para escalabilidade horizontal.
        
        EVOLUÇÃO: Criação de shards com configuração personalizada.
        """
        try:
            from .infrastructure.horizontal_scaler import ShardConfig
            
            config = ShardConfig(
                shard_id=shard_id,
                node_count=node_count,
                replication_factor=replication_factor
            )
            
            success = horizontal_scaler.create_shard(shard_id, config)
            
            if success:
                # Coletar métrica de shard criado
                real_time_monitor.collect_metric("blockchain.shards.total", 
                                                horizontal_scaler.stats["total_shards"],
                                                tags={"shard_id": shard_id})
            
            return success
            
        except Exception as e:
            logger.error(f"Erro ao criar shard {shard_id}: {e}")
            return False
    
    def add_node_to_shard(self, shard_id: str, node_id: str, address: str, port: int, priority: int = 1) -> bool:
        """
        Adiciona um nó a um shard.
        
        EVOLUÇÃO: Adição de nós com prioridade e configuração.
        """
        try:
            success = horizontal_scaler.add_node_to_shard(shard_id, node_id, address, port, priority)
            
            if success:
                # Coletar métrica de nó adicionado
                real_time_monitor.collect_metric("blockchain.nodes.total",
                                                horizontal_scaler.stats["total_nodes"],
                                                tags={"shard_id": shard_id, "node_id": node_id})
            
            return success
            
        except Exception as e:
            logger.error(f"Erro ao adicionar nó {node_id} ao shard {shard_id}: {e}")
            return False
    
    def create_alert_rule(self, rule_id: str, name: str, metric_name: str, condition: str, 
                         threshold: float, level: str = "warning") -> bool:
        """
        Cria uma regra de alerta para monitoramento.
        
        EVOLUÇÃO: Criação de regras de alerta com condições personalizadas.
        """
        try:
            from .infrastructure.real_time_monitor import AlertLevel
            
            alert_level = AlertLevel(level.lower())
            success = real_time_monitor.create_alert_rule(rule_id, name, metric_name, condition, threshold, alert_level)
            
            if success:
                # Coletar métrica de regra criada
                real_time_monitor.collect_metric("blockchain.alert_rules.total",
                                                len(real_time_monitor.alert_rules),
                                                tags={"rule_id": rule_id, "level": level})
            
            return success
            
        except Exception as e:
            logger.error(f"Erro ao criar regra de alerta {rule_id}: {e}")
            return False
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """
        Obtém alertas ativos do monitoramento.
        
        EVOLUÇÃO: Lista de alertas ativos com informações detalhadas.
        """
        try:
            alerts = real_time_monitor.get_active_alerts()
            return [
                {
                    "alert_id": alert.alert_id,
                    "name": alert.name,
                    "level": alert.level.value,
                    "message": alert.message,
                    "timestamp": alert.timestamp,
                    "tags": alert.tags
                }
                for alert in alerts
            ]
            
        except Exception as e:
            logger.error(f"Erro ao obter alertas ativos: {e}")
            return []
    
    def resolve_alert(self, alert_id: str) -> bool:
        """
        Resolve um alerta.
        
        EVOLUÇÃO: Resolução de alertas com timestamp.
        """
        try:
            success = real_time_monitor.resolve_alert(alert_id)
            
            if success:
                # Coletar métrica de alerta resolvido
                real_time_monitor.collect_metric("blockchain.alerts.resolved",
                                                real_time_monitor.stats["resolved_alerts"],
                                                tags={"alert_id": alert_id})
            
            return success
            
        except Exception as e:
            logger.error(f"Erro ao resolver alerta {alert_id}: {e}")
            return False
    
    def __str__(self) -> str:
        """Representação string da blockchain"""
        return f"Blockchain(name={self.name}, blocks={len(self.blocks)}, difficulty={self.difficulty})"
