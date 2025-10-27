"""
Entidade Block - Representa um bloco na blockchain
"""

import hashlib
import json
from dataclasses import dataclass, field
from typing import List, Optional
from decimal import Decimal

from ...shared.value_objects.hash_value import HashValue
from ...shared.value_objects.timestamp import Timestamp
from ...transaction.entities.transaction import Transaction, TransactionType
from ...shared.domain_events.base import DomainEvent


@dataclass
class Block:
    """
    Entidade Block - Representa um bloco na blockchain.
    
    Responsabilidades:
    - Armazenar transações
    - Manter integridade da cadeia
    - Implementar mineração (Proof of Work)
    - Validar hash do bloco anterior
    
    Invariantes:
    - Hash deve ser válido
    - Nonce deve ser encontrado via mineração
    - Transações devem ser válidas
    - Timestamp deve ser consistente
    """
    
    # Identity
    height: int
    hash: HashValue
    previous_hash: Optional[HashValue]
    
    # Block data
    transactions: List[Transaction]
    merkle_root: HashValue
    timestamp: Timestamp
    nonce: int
    
    # Mining data
    difficulty: int
    mining_time: float  # Tempo gasto na mineração
    
    # Metadata
    miner_address: Optional[str] = None
    block_reward: Decimal = Decimal("50.0")
    total_fees: Decimal = Decimal("0.0")
    
    # Domain Events (não persistidos)
    _events: List[DomainEvent] = field(default_factory=list, init=False, repr=False)
    
    def __post_init__(self):
        """Validação após inicialização"""
        self._validate()
    
    def _validate(self):
        """Valida invariantes do domínio"""
        if self.height < 0:
            raise ValueError("Block height cannot be negative")
        
        if not self.transactions:
            raise ValueError("Block must contain at least one transaction")
        
        if self.difficulty < 1:
            raise ValueError("Difficulty must be at least 1")
        
        if self.nonce < 0:
            raise ValueError("Nonce cannot be negative")
    
    @classmethod
    def create_genesis_block(cls) -> "Block":
        """Cria o bloco gênesis (primeiro bloco da blockchain)"""
        from ...transaction.entities.transaction import Transaction, TransactionId, TransactionAmount, TransactionFee, TransactionType, TransactionStatus
        from ...shared.value_objects.wallet_address import WalletAddress
        from ...shared.value_objects.money import Money
        
        # Criar transação gênesis
        genesis_transaction = Transaction(
            id=TransactionId.generate(),
            from_address=None,  # Sistema cria CNB do nada
            to_address=WalletAddress("0000000000000000000000000000000000000000"),  # Endereço especial
            amount=TransactionAmount(Money(Decimal("21000000"))),  # Supply total inicial
            fee=TransactionFee(Money(Decimal("0"))),
            transaction_type=TransactionType.GENESIS,
            status=TransactionStatus.CONFIRMED,
            created_at=Timestamp.now(),
            confirmed_at=Timestamp.now(),
            block_height=0,
            transaction_hash="genesis_transaction_hash",
            memo="Genesis block - Initial CNB supply"
        )
        
        # Criar bloco gênesis
        genesis_block = cls(
            height=0,
            hash=HashValue.create("0000000000000000000000000000000000000000000000000000000000000000"),
            previous_hash=None,
            transactions=[genesis_transaction],
            merkle_root=cls._calculate_merkle_root([genesis_transaction]),
            timestamp=Timestamp.now(),
            nonce=0,
            difficulty=1,
            mining_time=0.0,
            miner_address="system",
            block_reward=Decimal("0.0")
        )
        
        return genesis_block
    
    @classmethod
    def create_block(
        cls,
        height: int,
        previous_hash: HashValue,
        transactions: List[Transaction],
        difficulty: int,
        miner_address: Optional[str] = None
    ) -> "Block":
        """Cria um novo bloco"""
        import time
        
        # Calcular merkle root
        merkle_root = cls._calculate_merkle_root(transactions)
        
        # Criar bloco temporário para mineração
        temp_block = cls(
            height=height,
            hash=HashValue.create("temp_hash"),
            previous_hash=previous_hash,
            transactions=transactions,
            merkle_root=merkle_root,
            timestamp=Timestamp.now(),
            nonce=0,
            difficulty=difficulty,
            mining_time=0.0,
            miner_address=miner_address
        )
        
        # Minerar bloco (encontrar nonce válido)
        start_time = time.time()
        mined_block = temp_block._mine_block()
        mining_time = time.time() - start_time
        
        # Atualizar tempo de mineração
        mined_block.mining_time = mining_time
        
        return mined_block
    
    def _mine_block(self) -> "Block":
        """Mina o bloco encontrando um nonce válido"""
        import hashlib
        
        target_prefix = "0" * self.difficulty
        
        while True:
            # Criar dados do bloco para hash
            block_data = self._create_block_data_for_hash()
            
            # Calcular hash
            block_hash = hashlib.sha256(block_data.encode()).hexdigest()
            
            # Verificar se hash atende à dificuldade
            if block_hash.startswith(target_prefix):
                # Criar novo bloco com hash válido
                return Block(
                    height=self.height,
                    hash=HashValue.create(block_hash),
                    previous_hash=self.previous_hash,
                    transactions=self.transactions,
                    merkle_root=self.merkle_root,
                    timestamp=self.timestamp,
                    nonce=self.nonce,
                    difficulty=self.difficulty,
                    mining_time=self.mining_time,
                    miner_address=self.miner_address,
                    block_reward=self.block_reward,
                    total_fees=self.total_fees
                )
            
            # Incrementar nonce para próxima tentativa
            self.nonce += 1
    
    def _create_block_data_for_hash(self) -> str:
        """Cria string de dados do bloco para cálculo de hash"""
        data = {
            "height": self.height,
            "previous_hash": self.previous_hash.value if self.previous_hash else "0",
            "merkle_root": self.merkle_root.value,
            "timestamp": self.timestamp.value,
            "nonce": self.nonce,
            "difficulty": self.difficulty,
            "transactions_count": len(self.transactions)
        }
        return json.dumps(data, sort_keys=True)
    
    @staticmethod
    def _calculate_merkle_root(transactions: List[Transaction]) -> HashValue:
        """Calcula a raiz Merkle das transações"""
        import hashlib
        
        if not transactions:
            return HashValue.create("0" * 64)
        
        if len(transactions) == 1:
            tx_hash = hashlib.sha256(str(transactions[0].id.value).encode()).hexdigest()
            return HashValue.create(tx_hash)
        
        # Calcular hashes das transações
        tx_hashes = []
        for tx in transactions:
            tx_hash = hashlib.sha256(str(tx.id.value).encode()).hexdigest()
            tx_hashes.append(tx_hash)
        
        # Construir árvore Merkle
        while len(tx_hashes) > 1:
            next_level = []
            for i in range(0, len(tx_hashes), 2):
                left = tx_hashes[i]
                right = tx_hashes[i + 1] if i + 1 < len(tx_hashes) else tx_hashes[i]
                combined = hashlib.sha256((left + right).encode()).hexdigest()
                next_level.append(combined)
            tx_hashes = next_level
        
        return HashValue.create(tx_hashes[0])
    
    def is_valid(self) -> bool:
        """Valida se o bloco é válido"""
        try:
            # Bloco gênesis tem validação especial
            if self.height == 0:
                return self._validate_genesis_block()
            
            # Verificar se o hash está correto
            expected_hash = self._create_block_data_for_hash()
            calculated_hash = hashlib.sha256(expected_hash.encode()).hexdigest()
            
            if calculated_hash != self.hash.value:
                return False
            
            # Verificar se o hash atende à dificuldade
            target_prefix = "0" * self.difficulty
            if not self.hash.value.startswith(target_prefix):
                return False
            
            # Verificar se as transações são válidas (exceto bloco gênesis)
            if self.height > 0:
                for tx in self.transactions:
                    if not tx.is_valid():
                        return False
            
            # Verificar se a raiz Merkle está correta
            expected_merkle_root = self._calculate_merkle_root(self.transactions)
            if expected_merkle_root.value != self.merkle_root.value:
                return False
            
            return True
            
        except Exception:
            return False
    
    def _validate_genesis_block(self) -> bool:
        """Validação especial para o bloco gênesis"""
        try:
            # Verificar altura
            if self.height != 0:
                return False
            
            # Verificar que não tem bloco anterior
            if self.previous_hash is not None:
                return False
            
            # Verificar que tem pelo menos uma transação
            if not self.transactions:
                return False
            
            # Verificar se a transação é do tipo GENESIS
            if self.transactions[0].transaction_type != TransactionType.GENESIS:
                return False
            
            # Verificar se a raiz Merkle está correta
            expected_merkle_root = self._calculate_merkle_root(self.transactions)
            if expected_merkle_root.value != self.merkle_root.value:
                return False
            
            return True
            
        except Exception:
            return False
    
    def get_transaction_by_id(self, tx_id: str) -> Optional[Transaction]:
        """Busca transação por ID"""
        for tx in self.transactions:
            if tx.id.value == tx_id:
                return tx
        return None
    
    def get_total_transaction_fees(self) -> Decimal:
        """Calcula total de taxas das transações"""
        total_fees = Decimal("0")
        for tx in self.transactions:
            total_fees += tx.fee.value.to_cnb()
        return total_fees
    
    def get_events(self) -> List[DomainEvent]:
        """Retorna eventos de domínio"""
        return self._events.copy()
    
    def clear_events(self) -> None:
        """Limpa eventos de domínio"""
        self._events.clear()
    
    def __str__(self) -> str:
        """Representação string do bloco"""
        return f"Block(height={self.height}, hash={self.hash.value[:8]}..., tx_count={len(self.transactions)})"
