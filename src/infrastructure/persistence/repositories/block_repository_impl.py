"""
Implementação do BlockRepository usando SQLite
"""

import json
from typing import List, Optional
from src.domain.blockchain.entities.block import Block
from src.domain.blockchain.repositories.block_repository import BlockRepository
from src.domain.shared.value_objects.hash_value import HashValue
from src.domain.shared.value_objects.timestamp import Timestamp
from src.domain.transaction.entities.transaction import Transaction, TransactionId, TransactionAmount, TransactionFee, TransactionType, TransactionStatus
from src.domain.shared.value_objects.wallet_address import WalletAddress
from src.infrastructure.persistence.database_manager import DatabaseManager


class SQLiteBlockRepository(BlockRepository):
    """Implementação de BlockRepository usando SQLite"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self._init_table()
    
    def _init_table(self):
        """Inicializa tabela de blocos"""
        with self.db.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS blocks (
                    height INTEGER PRIMARY KEY,
                    hash TEXT NOT NULL UNIQUE,
                    previous_hash TEXT,
                    merkle_root TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    nonce INTEGER NOT NULL,
                    difficulty INTEGER NOT NULL,
                    mining_time REAL NOT NULL,
                    miner_address TEXT,
                    block_reward REAL NOT NULL,
                    total_fees REAL NOT NULL,
                    transactions_count INTEGER NOT NULL,
                    created_at REAL NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS block_transactions (
                    block_height INTEGER NOT NULL,
                    transaction_id TEXT NOT NULL,
                    transaction_order INTEGER NOT NULL,
                    PRIMARY KEY (block_height, transaction_id),
                    FOREIGN KEY (block_height) REFERENCES blocks (height),
                    FOREIGN KEY (transaction_id) REFERENCES transactions (id)
                )
            """)
            
            conn.commit()
    
    async def save(self, block: Block) -> None:
        """Salva um bloco"""
        block_data = self._to_persistence(block)
        
        with self.db.get_connection() as conn:
            # Salvar bloco
            conn.execute("""
                INSERT OR REPLACE INTO blocks
                (height, hash, previous_hash, merkle_root, timestamp, nonce,
                 difficulty, mining_time, miner_address, block_reward, total_fees,
                 transactions_count, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                block_data["height"],
                block_data["hash"],
                block_data["previous_hash"],
                block_data["merkle_root"],
                block_data["timestamp"],
                block_data["nonce"],
                block_data["difficulty"],
                block_data["mining_time"],
                block_data["miner_address"],
                block_data["block_reward"],
                block_data["total_fees"],
                block_data["transactions_count"],
                block_data["created_at"]
            ))
            
            # Salvar relacionamento com transações
            conn.execute("DELETE FROM block_transactions WHERE block_height = ?", (block.height,))
            
            for i, tx in enumerate(block.transactions):
                conn.execute("""
                    INSERT INTO block_transactions (block_height, transaction_id, transaction_order)
                    VALUES (?, ?, ?)
                """, (block.height, tx.id.value, i))
            
            conn.commit()
    
    async def find_by_height(self, height: int) -> Optional[Block]:
        """Busca bloco por altura"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM blocks WHERE height = ?", (height,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return await self._from_persistence(dict(row))
    
    async def find_by_hash(self, block_hash: str) -> Optional[Block]:
        """Busca bloco por hash"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM blocks WHERE hash = ?", (block_hash,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return await self._from_persistence(dict(row))
    
    async def find_latest(self) -> Optional[Block]:
        """Busca o último bloco"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM blocks ORDER BY height DESC LIMIT 1")
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return await self._from_persistence(dict(row))
    
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Block]:
        """Lista todos os blocos"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM blocks 
                ORDER BY height ASC 
                LIMIT ? OFFSET ?
            """, (limit, skip))
            
            rows = cursor.fetchall()
            blocks = []
            
            for row in rows:
                block = await self._from_persistence(dict(row))
                blocks.append(block)
            
            return blocks
    
    async def count(self) -> int:
        """Conta total de blocos"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM blocks")
            row = cursor.fetchone()
            return row["count"] if row else 0
    
    async def exists(self, height: int) -> bool:
        """Verifica se bloco existe"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT 1 FROM blocks WHERE height = ?", (height,))
            return cursor.fetchone() is not None
    
    def _to_persistence(self, block: Block) -> dict:
        """Converte entidade para formato de persistência"""
        return {
            "height": block.height,
            "hash": block.hash.value,
            "previous_hash": block.previous_hash.value if block.previous_hash else None,
            "merkle_root": block.merkle_root.value,
            "timestamp": block.timestamp.value,
            "nonce": block.nonce,
            "difficulty": block.difficulty,
            "mining_time": block.mining_time,
            "miner_address": block.miner_address,
            "block_reward": float(block.block_reward),
            "total_fees": float(block.total_fees),
            "transactions_count": len(block.transactions),
            "created_at": block.timestamp.value
        }
    
    async def _from_persistence(self, data: dict) -> Block:
        """Reconstrói entidade a partir de dados persistidos"""
        # Buscar transações do bloco
        transactions = await self._get_block_transactions(data["height"])
        
        return Block(
            height=data["height"],
            hash=HashValue.create(data["hash"]),
            previous_hash=HashValue.create(data["previous_hash"]) if data["previous_hash"] else None,
            transactions=transactions,
            merkle_root=HashValue.create(data["merkle_root"]),
            timestamp=Timestamp.from_seconds(data["timestamp"]),
            nonce=data["nonce"],
            difficulty=data["difficulty"],
            mining_time=data["mining_time"],
            miner_address=data["miner_address"],
            block_reward=Decimal(str(data["block_reward"])),
            total_fees=Decimal(str(data["total_fees"]))
        )
    
    async def _get_block_transactions(self, block_height: int) -> List[Transaction]:
        """Busca transações de um bloco"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT t.* FROM transactions t
                JOIN block_transactions bt ON t.id = bt.transaction_id
                WHERE bt.block_height = ?
                ORDER BY bt.transaction_order
            """, (block_height,))
            
            rows = cursor.fetchall()
            transactions = []
            
            for row in rows:
                tx_data = dict(row)
                transaction = Transaction(
                    id=TransactionId(tx_data["id"]),
                    from_address=WalletAddress(tx_data["from_address"]) if tx_data["from_address"] else None,
                    to_address=WalletAddress(tx_data["to_address"]),
                    amount=TransactionAmount(Decimal(str(tx_data["amount_cnb"]))),
                    fee=TransactionFee(Decimal(str(tx_data["fee_cnb"]))),
                    transaction_type=TransactionType(tx_data.get("transaction_type", "transfer")),
                    status=TransactionStatus(tx_data["status"]),
                    created_at=Timestamp.from_seconds(tx_data["created_at"]),
                    confirmed_at=Timestamp.from_seconds(tx_data["confirmed_at"]) if tx_data["confirmed_at"] else None,
                    block_height=tx_data.get("block_height"),
                    transaction_hash=tx_data.get("transaction_hash"),
                    memo=tx_data.get("memo"),
                    metadata=json.loads(tx_data["metadata"]) if tx_data["metadata"] else {}
                )
                transactions.append(transaction)
            
            return transactions
