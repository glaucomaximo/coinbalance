"""
Implementação do repositório de validadores usando SQLite
"""

import sqlite3
import json
from typing import List, Optional
from decimal import Decimal

from src.domain.consensus.entities.validator import Validator
from src.domain.consensus.repositories.validator_repository import ValidatorRepository
from src.domain.consensus.value_objects.validator_id import ValidatorId
from src.domain.shared.value_objects.wallet_address import WalletAddress
from src.domain.shared.value_objects.timestamp import Timestamp
from src.domain.consensus.value_objects.stake_amount import StakeAmount
from src.domain.shared.value_objects.money import Money


class SQLiteValidatorRepository(ValidatorRepository):
    """
    Implementação do repositório de validadores usando SQLite.
    
    Esta implementação persiste os dados de validadores
    em uma base de dados SQLite local.
    """
    
    def __init__(self, db_path: str = "blockchain.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """Inicializa a base de dados com as tabelas necessárias"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Criar tabela de validadores
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS validators (
                    id TEXT PRIMARY KEY,
                    wallet_address TEXT UNIQUE NOT NULL,
                    stake_amount_cnb TEXT NOT NULL,
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    blocks_validated INTEGER NOT NULL DEFAULT 0,
                    total_rewards_cnb TEXT NOT NULL DEFAULT '0',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    last_validation_at TEXT,
                    metadata TEXT
                )
            """)
            
            conn.commit()
    
    async def save(self, validator: Validator) -> None:
        """Salva um validador no repositório"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO validators (
                    id, wallet_address, stake_amount_cnb, is_active,
                    blocks_validated, total_rewards_cnb, created_at,
                    updated_at, last_validation_at, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(validator.id),
                str(validator.wallet_address),
                str(validator.stake_amount.to_cnb()),
                1 if validator.is_active else 0,
                validator.blocks_validated,
                str(validator.total_rewards),
                str(validator.created_at.value),
                str(validator.updated_at.value),
                str(validator.last_validation_at.value) if validator.last_validation_at else None,
                json.dumps(validator.metadata)
            ))
            
            conn.commit()
    
    async def find_by_id(self, validator_id: ValidatorId) -> Optional[Validator]:
        """Busca um validador por ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, wallet_address, stake_amount_cnb, is_active,
                       blocks_validated, total_rewards_cnb, created_at,
                       updated_at, last_validation_at, metadata
                FROM validators WHERE id = ?
            """, (str(validator_id),))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return self._row_to_validator(row)
    
    async def find_by_wallet_address(self, wallet_address: WalletAddress) -> Optional[Validator]:
        """Busca um validador por endereço de carteira"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, wallet_address, stake_amount_cnb, is_active,
                       blocks_validated, total_rewards_cnb, created_at,
                       updated_at, last_validation_at, metadata
                FROM validators WHERE wallet_address = ?
            """, (str(wallet_address),))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return self._row_to_validator(row)
    
    async def find_all_active(self) -> List[Validator]:
        """Busca todos os validadores ativos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, wallet_address, stake_amount_cnb, is_active,
                       blocks_validated, total_rewards_cnb, created_at,
                       updated_at, last_validation_at, metadata
                FROM validators WHERE is_active = 1
                ORDER BY stake_amount_cnb DESC
            """)
            
            rows = cursor.fetchall()
            return [self._row_to_validator(row) for row in rows]
    
    async def find_all(self) -> List[Validator]:
        """Busca todos os validadores"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, wallet_address, stake_amount_cnb, is_active,
                       blocks_validated, total_rewards_cnb, created_at,
                       updated_at, last_validation_at, metadata
                FROM validators
                ORDER BY created_at DESC
            """)
            
            rows = cursor.fetchall()
            return [self._row_to_validator(row) for row in rows]
    
    async def delete(self, validator_id: ValidatorId) -> None:
        """Remove um validador do repositório"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM validators WHERE id = ?", (str(validator_id),))
            conn.commit()
    
    async def count(self) -> int:
        """Conta o número total de validadores"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM validators")
            return cursor.fetchone()[0]
    
    async def count_active(self) -> int:
        """Conta o número de validadores ativos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM validators WHERE is_active = 1")
            return cursor.fetchone()[0]
    
    def _row_to_validator(self, row: tuple) -> Validator:
        """Converte uma linha da base de dados em um objeto Validator"""
        (
            id_str, wallet_address_str, stake_amount_str, is_active,
            blocks_validated, total_rewards_str, created_at_str,
            updated_at_str, last_validation_at_str, metadata_str
        ) = row
        
        # Converter strings de volta para objetos de domínio
        validator_id = ValidatorId(id_str)
        wallet_address = WalletAddress(wallet_address_str)
        stake_amount = StakeAmount(Money(Decimal(stake_amount_str)))
        created_at = Timestamp(Decimal(created_at_str))
        updated_at = Timestamp(Decimal(updated_at_str))
        last_validation_at = Timestamp(Decimal(last_validation_at_str)) if last_validation_at_str else None
        metadata = json.loads(metadata_str) if metadata_str else {}
        
        return Validator(
            id=validator_id,
            wallet_address=wallet_address,
            stake_amount=stake_amount,
            is_active=bool(is_active),
            created_at=created_at,
            updated_at=updated_at,
            blocks_validated=blocks_validated,
            total_rewards=Decimal(total_rewards_str),
            last_validation_at=last_validation_at,
            metadata=metadata
        )
