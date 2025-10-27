"""
Implementação simplificada do repositório de transações usando SQLite
"""

import sqlite3
import json
from typing import List, Optional
from decimal import Decimal

from src.domain.transaction.entities.transaction import Transaction, TransactionStatus, TransactionType
from src.domain.transaction.repositories.transaction_repository import TransactionRepository
from src.domain.transaction.value_objects.transaction_id import TransactionId
from src.domain.transaction.value_objects.transaction_amount import TransactionAmount
from src.domain.transaction.value_objects.transaction_fee import TransactionFee
from src.domain.shared.value_objects.wallet_address import WalletAddress
from src.domain.shared.value_objects.timestamp import Timestamp
from src.domain.shared.value_objects.money import Money


class SQLiteTransactionRepository(TransactionRepository):
    """
    Implementação simplificada do repositório de transações usando SQLite.
    
    Esta implementação usa a estrutura existente da tabela transactions.
    """
    
    def __init__(self, db_path: str = "blockchain.db"):
        self.db_path = db_path
    
    async def save(self, transaction: Transaction) -> None:
        """Salva uma transação no repositório"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO transactions (
                    id, from_address, to_address, amount_cnb, amount_satoshi,
                    fee_cnb, fee_satoshi, status, metadata, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(transaction.id),
                str(transaction.from_address) if transaction.from_address else None,
                str(transaction.to_address),
                float(transaction.amount.to_cnb()),
                transaction.amount.to_satoshi(),
                float(transaction.fee.to_cnb()),
                transaction.fee.to_satoshi(),
                transaction.status.value,
                json.dumps(transaction.metadata),
                float(transaction.created_at.value),
                float(transaction.updated_at.value)
            ))
            
            conn.commit()
    
    async def find_by_id(self, transaction_id: TransactionId) -> Optional[Transaction]:
        """Busca uma transação por ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, from_address, to_address, amount_cnb, amount_satoshi,
                       fee_cnb, fee_satoshi, status, metadata, created_at, updated_at
                FROM transactions WHERE id = ?
            """, (str(transaction_id),))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return self._row_to_transaction(row)
    
    async def find_by_hash(self, transaction_hash: str) -> Optional[Transaction]:
        """Busca uma transação por hash - não implementado na estrutura atual"""
        return None
    
    async def find_by_address(
        self, 
        address: WalletAddress, 
        limit: int = 50,
        offset: int = 0
    ) -> List[Transaction]:
        """Busca transações relacionadas a um endereço"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, from_address, to_address, amount_cnb, amount_satoshi,
                       fee_cnb, fee_satoshi, status, metadata, created_at, updated_at
                FROM transactions 
                WHERE from_address = ? OR to_address = ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (str(address), str(address), limit, offset))
            
            rows = cursor.fetchall()
            return [self._row_to_transaction(row) for row in rows]
    
    async def find_pending_transactions(self) -> List[Transaction]:
        """Busca todas as transações pendentes"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, from_address, to_address, amount_cnb, amount_satoshi,
                       fee_cnb, fee_satoshi, status, metadata, created_at, updated_at
                FROM transactions 
                WHERE status = ?
                ORDER BY created_at ASC
            """, (TransactionStatus.PENDING.value,))
            
            rows = cursor.fetchall()
            return [self._row_to_transaction(row) for row in rows]
    
    async def find_by_block_height(self, block_height: int) -> List[Transaction]:
        """Busca transações de um bloco específico - não implementado"""
        return []
    
    async def count_by_address(self, address: WalletAddress) -> int:
        """Conta o número de transações de um endereço"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) FROM transactions 
                WHERE from_address = ? OR to_address = ?
            """, (str(address), str(address)))
            
            return cursor.fetchone()[0]
    
    async def get_total_volume(self) -> Decimal:
        """Retorna o volume total de transações"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT SUM(amount_cnb) FROM transactions 
                WHERE status = ?
            """, (TransactionStatus.CONFIRMED.value,))
            
            result = cursor.fetchone()[0]
            return Decimal(str(result)) if result else Decimal("0")
    
    async def get_transaction_stats(self) -> dict:
        """Retorna estatísticas das transações"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total de transações
            cursor.execute("SELECT COUNT(*) FROM transactions")
            total_transactions = cursor.fetchone()[0]
            
            # Volume total
            cursor.execute("""
                SELECT SUM(amount_cnb) FROM transactions 
                WHERE status = ?
            """, (TransactionStatus.CONFIRMED.value,))
            total_volume = cursor.fetchone()[0] or 0
            
            # Taxas totais
            cursor.execute("""
                SELECT SUM(fee_cnb) FROM transactions 
                WHERE status = ?
            """, (TransactionStatus.CONFIRMED.value,))
            total_fees = cursor.fetchone()[0] or 0
            
            # Transações pendentes
            cursor.execute("SELECT COUNT(*) FROM transactions WHERE status = ?", (TransactionStatus.PENDING.value,))
            pending_transactions = cursor.fetchone()[0]
            
            # Transações confirmadas
            cursor.execute("SELECT COUNT(*) FROM transactions WHERE status = ?", (TransactionStatus.CONFIRMED.value,))
            confirmed_transactions = cursor.fetchone()[0]
            
            # Transações falhadas
            cursor.execute("SELECT COUNT(*) FROM transactions WHERE status = ?", (TransactionStatus.FAILED.value,))
            failed_transactions = cursor.fetchone()[0]
            
            return {
                "total_transactions": total_transactions,
                "total_volume_cnb": Decimal(str(total_volume)),
                "total_fees_cnb": Decimal(str(total_fees)),
                "pending_transactions": pending_transactions,
                "confirmed_transactions": confirmed_transactions,
                "failed_transactions": failed_transactions
            }
    
    def _row_to_transaction(self, row: tuple) -> Transaction:
        """Converte uma linha da base de dados em um objeto Transaction"""
        (
            id_str, from_address_str, to_address_str, amount_cnb, amount_satoshi,
            fee_cnb, fee_satoshi, status_str, metadata_str, created_at, updated_at
        ) = row
        
        # Converter strings de volta para objetos de domínio
        transaction_id = TransactionId(id_str)
        from_address = WalletAddress(from_address_str) if from_address_str else None
        to_address = WalletAddress(to_address_str)
        amount = TransactionAmount(Money(Decimal(str(amount_cnb))))
        fee = TransactionFee(Money(Decimal(str(fee_cnb))))
        status = TransactionStatus(status_str)
        created_at_timestamp = Timestamp(Decimal(str(created_at)))
        updated_at_timestamp = Timestamp(Decimal(str(updated_at)))
        metadata = json.loads(metadata_str) if metadata_str else {}
        
        # Criar transação simplificada (sem campos que não existem na tabela atual)
        return Transaction(
            id=transaction_id,
            from_address=from_address,
            to_address=to_address,
            amount=amount,
            fee=fee,
            transaction_type=TransactionType.TRANSFER,  # Default
            status=status,
            created_at=created_at_timestamp,
            confirmed_at=None,  # Não existe na tabela atual
            block_height=None,  # Não existe na tabela atual
            transaction_hash=None,  # Não existe na tabela atual
            memo=None,  # Não existe na tabela atual
            metadata=metadata
        )