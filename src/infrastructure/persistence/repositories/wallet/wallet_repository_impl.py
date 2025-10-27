"""
Implementação SQLite do repositório de carteiras
"""

import sqlite3
import json
from typing import Optional, List
from decimal import Decimal

from src.domain.wallet.entities.wallet import Wallet
from src.domain.wallet.repositories.wallet_repository import WalletRepository
from src.domain.wallet.value_objects.wallet_address import WalletAddress
from src.domain.wallet.value_objects.private_key import PrivateKey
from src.domain.wallet.value_objects.public_key import PublicKey
from src.domain.wallet.value_objects.balance import Balance
from src.domain.shared.value_objects.timestamp import Timestamp
from src.domain.shared.value_objects.money import Money


class SQLiteWalletRepository(WalletRepository):
    """
    Implementação SQLite do repositório de carteiras.
    """
    
    def __init__(self, db_path: str = "blockchain.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """Inicializa a base de dados com as tabelas necessárias"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Criar tabela de carteiras
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wallets (
                    address TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    public_key TEXT NOT NULL,
                    private_key TEXT NOT NULL,
                    balance_cnb TEXT NOT NULL DEFAULT '0',
                    balance_satoshi INTEGER NOT NULL DEFAULT 0,
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    metadata TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            conn.commit()
    
    async def save(self, wallet: Wallet) -> None:
        """Salva uma carteira no repositório"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO wallets (
                    address, name, public_key, private_key, balance_cnb,
                    balance_satoshi, is_active, metadata, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(wallet.address),
                wallet.name,
                str(wallet.public_key),
                str(wallet.private_key),
                str(wallet.balance.to_cnb()),
                wallet.balance.to_satoshi(),
                1 if wallet.is_active else 0,
                json.dumps(wallet.metadata),
                str(wallet.created_at.value),
                str(wallet.updated_at.value)
            ))
            
            conn.commit()
    
    async def find_by_address(self, address: WalletAddress) -> Optional[Wallet]:
        """Busca uma carteira por endereço"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT address, name, public_key, private_key, balance_cnb,
                       balance_satoshi, is_active, metadata, created_at, updated_at
                FROM wallets WHERE address = ?
            """, (str(address),))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return self._row_to_wallet(row)
    
    async def find_by_name(self, name: str) -> Optional[Wallet]:
        """Busca uma carteira por nome"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT address, name, public_key, private_key, balance_cnb,
                       balance_satoshi, is_active, metadata, created_at, updated_at
                FROM wallets WHERE name = ?
            """, (name,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return self._row_to_wallet(row)
    
    async def find_all(self) -> List[Wallet]:
        """Busca todas as carteiras"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT address, name, public_key, private_key, balance_cnb,
                       balance_satoshi, is_active, metadata, created_at, updated_at
                FROM wallets ORDER BY created_at DESC
            """)
            
            rows = cursor.fetchall()
            return [self._row_to_wallet(row) for row in rows]
    
    async def count(self) -> int:
        """Conta o número total de carteiras"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM wallets")
            return cursor.fetchone()[0]
    
    def _row_to_wallet(self, row: tuple) -> Wallet:
        """Converte uma linha da base de dados em um objeto Wallet"""
        (
            address_str, name, public_key_str, private_key_str, balance_cnb_str,
            balance_satoshi, is_active, metadata_str, created_at_str, updated_at_str
        ) = row
        
        # Converter strings de volta para objetos de domínio
        address = WalletAddress(address_str)
        public_key = PublicKey(public_key_str)
        private_key = PrivateKey(private_key_str)
        balance = Balance(Money(Decimal(balance_cnb_str)))
        created_at = Timestamp(float(created_at_str))
        updated_at = Timestamp(float(updated_at_str))
        metadata = json.loads(metadata_str) if metadata_str else {}
        
        return Wallet(
            address=address,
            name=name,
            public_key=public_key,
            private_key=private_key,
            balance=balance,
            created_at=created_at,
            updated_at=updated_at,
            is_active=bool(is_active),
            metadata=metadata
        )
    
    async def delete(self, address: WalletAddress) -> None:
        """Remove uma carteira do repositório"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM wallets WHERE address = ?", (str(address),))
            conn.commit()
    
    async def exists(self, address: WalletAddress) -> bool:
        """Verifica se uma carteira existe"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM wallets WHERE address = ?", (str(address),))
            return cursor.fetchone()[0] > 0
    
    async def find_active(self) -> List[Wallet]:
        """Busca todas as carteiras ativas"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT address, name, public_key, private_key, balance_cnb,
                       balance_satoshi, is_active, metadata, created_at, updated_at
                FROM wallets WHERE is_active = 1 ORDER BY created_at DESC
            """)
            
            rows = cursor.fetchall()
            return [self._row_to_wallet(row) for row in rows]
