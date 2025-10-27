"""
Sistema de Histórico de Transações para CoinBalance
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from enum import Enum

from src.domain.shared.value_objects.wallet_address import WalletAddress
from src.domain.shared.value_objects.money import Money
from src.domain.shared.value_objects.timestamp import Timestamp

class TransactionType(Enum):
    """Tipos de transação"""
    TRANSFER = "transfer"
    CREDIT = "credit"
    DEBIT = "debit"
    FEE = "fee"

class TransactionStatus(Enum):
    """Status da transação"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class TransactionRecord:
    """Registro de transação no histórico"""
    
    id: str
    type: TransactionType
    status: TransactionStatus
    
    # Endereços
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    
    # Valores
    amount: Decimal = Decimal('0')
    fee: Decimal = Decimal('0')
    total_amount: Decimal = Decimal('0')
    
    # Metadados
    reason: str = ""
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Timestamps
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    updated_at: float = field(default_factory=lambda: datetime.now().timestamp())
    
    # Informações adicionais
    block_height: Optional[int] = None
    transaction_hash: Optional[str] = None
    confirmations: int = 0

class TransactionHistoryService:
    """Serviço para gerenciar histórico de transações"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self._setup_database()
    
    def _setup_database(self):
        """Configura tabela de histórico de transações"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS transaction_history (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            status TEXT NOT NULL,
            from_address TEXT,
            to_address TEXT,
            amount REAL NOT NULL,
            fee REAL NOT NULL,
            total_amount REAL NOT NULL,
            reason TEXT NOT NULL,
            description TEXT,
            metadata TEXT,
            created_at REAL NOT NULL,
            updated_at REAL NOT NULL,
            block_height INTEGER,
            transaction_hash TEXT,
            confirmations INTEGER DEFAULT 0
        )
        """
        
        # Índices para consultas eficientes
        create_indexes_sql = [
            "CREATE INDEX IF NOT EXISTS idx_transaction_from_address ON transaction_history(from_address)",
            "CREATE INDEX IF NOT EXISTS idx_transaction_to_address ON transaction_history(to_address)",
            "CREATE INDEX IF NOT EXISTS idx_transaction_type ON transaction_history(type)",
            "CREATE INDEX IF NOT EXISTS idx_transaction_status ON transaction_history(status)",
            "CREATE INDEX IF NOT EXISTS idx_transaction_created_at ON transaction_history(created_at)",
        ]
        
        self.db_manager.execute_update(create_table_sql)
        for index_sql in create_indexes_sql:
            self.db_manager.execute_update(index_sql)
    
    def record_transfer(
        self,
        transaction_id: str,
        from_address: str,
        to_address: str,
        amount: Decimal,
        fee: Decimal,
        reason: str,
        status: TransactionStatus = TransactionStatus.COMPLETED,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TransactionRecord:
        """Registra uma transferência no histórico"""
        
        if metadata is None:
            metadata = {}
        
        record = TransactionRecord(
            id=transaction_id,
            type=TransactionType.TRANSFER,
            status=status,
            from_address=from_address,
            to_address=to_address,
            amount=amount,
            fee=fee,
            total_amount=amount + fee,
            reason=reason,
            description=f"Transfer from {from_address[:8]}... to {to_address[:8]}...",
            metadata=metadata
        )
        
        self._save_record(record)
        return record
    
    def record_wallet_operation(
        self,
        transaction_id: str,
        wallet_address: str,
        operation_type: TransactionType,
        amount: Decimal,
        reason: str,
        status: TransactionStatus = TransactionStatus.COMPLETED,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TransactionRecord:
        """Registra uma operação de carteira no histórico"""
        
        if metadata is None:
            metadata = {}
        
        # Determinar endereços baseado no tipo de operação
        if operation_type == TransactionType.CREDIT:
            from_address = None
            to_address = wallet_address
            description = f"Credit to {wallet_address[:8]}..."
        elif operation_type == TransactionType.DEBIT:
            from_address = wallet_address
            to_address = None
            description = f"Debit from {wallet_address[:8]}..."
        else:
            from_address = wallet_address
            to_address = wallet_address
            description = f"{operation_type.value} for {wallet_address[:8]}..."
        
        record = TransactionRecord(
            id=transaction_id,
            type=operation_type,
            status=status,
            from_address=from_address,
            to_address=to_address,
            amount=amount,
            fee=Decimal('0'),
            total_amount=amount,
            reason=reason,
            description=description,
            metadata=metadata
        )
        
        self._save_record(record)
        return record
    
    def _save_record(self, record: TransactionRecord):
        """Salva registro no banco de dados"""
        import json
        
        sql = """
        INSERT OR REPLACE INTO transaction_history (
            id, type, status, from_address, to_address, amount, fee, total_amount,
            reason, description, metadata, created_at, updated_at,
            block_height, transaction_hash, confirmations
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        values = (
            record.id,
            record.type.value,
            record.status.value,
            record.from_address,
            record.to_address,
            float(record.amount),
            float(record.fee),
            float(record.total_amount),
            record.reason,
            record.description,
            json.dumps(record.metadata),
            record.created_at,
            record.updated_at,
            record.block_height,
            record.transaction_hash,
            record.confirmations
        )
        
        self.db_manager.execute_update(sql, values)
    
    def get_wallet_history(
        self,
        wallet_address: str,
        limit: int = 50,
        offset: int = 0,
        transaction_type: Optional[TransactionType] = None,
        status: Optional[TransactionStatus] = None
    ) -> List[TransactionRecord]:
        """Obtém histórico de uma carteira"""
        
        # Construir query base
        where_conditions = ["(from_address = ? OR to_address = ?)"]
        params = [wallet_address, wallet_address]
        
        # Adicionar filtros opcionais
        if transaction_type:
            where_conditions.append("type = ?")
            params.append(transaction_type.value)
        
        if status:
            where_conditions.append("status = ?")
            params.append(status.value)
        
        # Query final
        where_clause = " AND ".join(where_conditions)
        sql = f"""
        SELECT * FROM transaction_history 
        WHERE {where_clause}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """
        
        params.extend([limit, offset])
        results = self.db_manager.execute_query(sql, params)
        
        return [self._row_to_record(row) for row in results]
    
    def get_transaction_by_id(self, transaction_id: str) -> Optional[TransactionRecord]:
        """Obtém transação por ID"""
        sql = "SELECT * FROM transaction_history WHERE id = ?"
        results = self.db_manager.execute_query(sql, (transaction_id,))
        
        if results:
            return self._row_to_record(results[0])
        return None
    
    def get_recent_transactions(
        self,
        limit: int = 20,
        transaction_type: Optional[TransactionType] = None
    ) -> List[TransactionRecord]:
        """Obtém transações recentes"""
        
        where_clause = ""
        params = []
        
        if transaction_type:
            where_clause = "WHERE type = ?"
            params.append(transaction_type.value)
        
        sql = f"""
        SELECT * FROM transaction_history 
        {where_clause}
        ORDER BY created_at DESC
        LIMIT ?
        """
        
        params.append(limit)
        results = self.db_manager.execute_query(sql, params)
        
        return [self._row_to_record(row) for row in results]
    
    def get_transaction_stats(
        self,
        wallet_address: Optional[str] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """Obtém estatísticas de transações"""
        
        # Calcular timestamp de início
        from datetime import datetime, timedelta
        start_time = (datetime.now() - timedelta(days=days)).timestamp()
        
        # Query base
        where_conditions = ["created_at >= ?"]
        params = [start_time]
        
        if wallet_address:
            where_conditions.append("(from_address = ? OR to_address = ?)")
            params.extend([wallet_address, wallet_address])
        
        where_clause = " AND ".join(where_conditions)
        
        # Estatísticas gerais
        stats_sql = f"""
        SELECT 
            COUNT(*) as total_transactions,
            SUM(CASE WHEN type = 'transfer' THEN 1 ELSE 0 END) as transfers,
            SUM(CASE WHEN type = 'credit' THEN 1 ELSE 0 END) as credits,
            SUM(CASE WHEN type = 'debit' THEN 1 ELSE 0 END) as debits,
            SUM(amount) as total_amount,
            SUM(fee) as total_fees,
            AVG(amount) as avg_amount
        FROM transaction_history 
        WHERE {where_clause}
        """
        
        results = self.db_manager.execute_query(stats_sql, params)
        if results:
            row = results[0]
            return {
                "total_transactions": row["total_transactions"] or 0,
                "transfers": row["transfers"] or 0,
                "credits": row["credits"] or 0,
                "debits": row["debits"] or 0,
                "total_amount": float(row["total_amount"] or 0),
                "total_fees": float(row["total_fees"] or 0),
                "avg_amount": float(row["avg_amount"] or 0),
                "period_days": days
            }
        
        return {
            "total_transactions": 0,
            "transfers": 0,
            "credits": 0,
            "debits": 0,
            "total_amount": 0.0,
            "total_fees": 0.0,
            "avg_amount": 0.0,
            "period_days": days
        }
    
    def _row_to_record(self, row: Dict[str, Any]) -> TransactionRecord:
        """Converte linha do banco para TransactionRecord"""
        import json
        
        metadata = {}
        if row["metadata"]:
            try:
                metadata = json.loads(row["metadata"])
            except json.JSONDecodeError:
                metadata = {}
        
        return TransactionRecord(
            id=row["id"],
            type=TransactionType(row["type"]),
            status=TransactionStatus(row["status"]),
            from_address=row["from_address"],
            to_address=row["to_address"],
            amount=Decimal(str(row["amount"])),
            fee=Decimal(str(row["fee"])),
            total_amount=Decimal(str(row["total_amount"])),
            reason=row["reason"],
            description=row["description"],
            metadata=metadata,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            block_height=row["block_height"],
            transaction_hash=row["transaction_hash"],
            confirmations=row["confirmations"]
        )
    
    def update_transaction_status(
        self,
        transaction_id: str,
        status: TransactionStatus,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Atualiza status de uma transação"""
        
        update_fields = ["status = ?", "updated_at = ?"]
        params = [status.value, datetime.now().timestamp()]
        
        if metadata:
            import json
            update_fields.append("metadata = ?")
            params.append(json.dumps(metadata))
        
        sql = f"""
        UPDATE transaction_history 
        SET {', '.join(update_fields)}
        WHERE id = ?
        """
        
        params.append(transaction_id)
        self.db_manager.execute_update(sql, params)
        
        return True
