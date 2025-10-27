"""
Entidade Blockchain - Representa a cadeia de blocos completa
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from decimal import Decimal

from .block import Block
from ...shared.value_objects.hash_value import HashValue
from ...shared.value_objects.timestamp import Timestamp
from ...transaction.entities.transaction import Transaction
from ...shared.domain_events.base import DomainEvent
from ...shared.config.blockchain_config import BlockchainConfig


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
        """Busca bloco por hash"""
        for block in self.blocks:
            if block.hash.value == block_hash:
                return block
        return None
    
    def add_block(self, block: Block) -> bool:
        """Adiciona um novo bloco à cadeia"""
        try:
            # Validar bloco
            if not self._is_valid_new_block(block):
                return False
            
            # Adicionar bloco
            self.blocks.append(block)
            self.total_blocks_mined += 1
            self.total_transactions += len(block.transactions)
            self.total_mining_time += block.mining_time
            
            # Atualizar estatísticas
            self._update_statistics()
            
            # Ajustar dificuldade se necessário
            self._adjust_difficulty()
            
            return True
            
        except Exception:
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
            if not latest_block or block.previous_hash.value != latest_block.hash.value:
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
        """Valida toda a cadeia de blocos"""
        try:
            for i, block in enumerate(self.blocks):
                # Verificar se o bloco é válido
                if not block.is_valid():
                    return False
                
                # Verificar altura
                if block.height != i:
                    return False
                
                # Verificar hash anterior (exceto gênesis)
                if i > 0:
                    previous_block = self.blocks[i-1]
                    if block.previous_hash.value != previous_block.hash.value:
                        return False
            
            return True
            
        except Exception:
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
        """Retorna transações pendentes (não incluídas em blocos)"""
        # Em uma implementação real, isso viria de um pool de transações
        # Por enquanto, retornamos lista vazia
        return []
    
    def mine_block(self, transactions: List[Transaction], miner_address: str) -> Optional[Block]:
        """Mina um novo bloco com as transações fornecidas"""
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
            
            new_block = Block.create_block(
                height=new_height,
                previous_hash=previous_hash,
                transactions=transactions,
                difficulty=self.difficulty,
                miner_address=miner_address
            )
            
            # Adicionar à cadeia
            if self.add_block(new_block):
                return new_block
            
            return None
            
        except Exception:
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
    
    def clear_events(self) -> None:
        """Limpa eventos de domínio"""
        self._events.clear()
    
    def __str__(self) -> str:
        """Representação string da blockchain"""
        return f"Blockchain(name={self.name}, blocks={len(self.blocks)}, difficulty={self.difficulty})"
