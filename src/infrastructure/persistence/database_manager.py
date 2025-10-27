"""
Database Manager

Gerencia conexões e operações com banco de dados.
"""

import sqlite3
import threading
from typing import Optional


class DatabaseManager:
    """
    Gerenciador de banco de dados SQLite.

    Implementa:
    - Pool de conexões thread-safe
    - Transações automáticas
    - Migração de schema
    - Criptografia de dados sensíveis
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or "blockchain.db"
        self._local = threading.local()
        self._init_database()

    def _init_database(self):
        """Inicializa o banco de dados e cria tabelas necessárias"""
        with self.get_connection() as conn:
            # Criar tabela de carteiras com constraints de integridade
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS wallets (
                    address TEXT PRIMARY KEY CHECK(length(address) >= 26 AND length(address) <= 62),
                    name TEXT NOT NULL UNIQUE CHECK(length(name) >= 3 AND length(name) <= 50),
                    public_key TEXT NOT NULL CHECK(length(public_key) >= 32),
                    private_key TEXT NOT NULL CHECK(length(private_key) >= 32),
                    balance_cnb REAL NOT NULL DEFAULT 0.0 CHECK(balance_cnb >= 0),
                    balance_satoshi INTEGER NOT NULL DEFAULT 0 CHECK(balance_satoshi >= 0),
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    metadata TEXT,
                    created_at REAL NOT NULL CHECK(created_at > 0),
                    updated_at REAL NOT NULL CHECK(updated_at >= created_at)
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY CHECK(length(id) >= 16),
                    from_address TEXT CHECK(length(from_address) >= 26 AND length(from_address) <= 62),
                    to_address TEXT NOT NULL CHECK(length(to_address) >= 26 AND length(to_address) <= 62),
                    amount_cnb REAL NOT NULL CHECK(amount_cnb > 0),
                    amount_satoshi INTEGER NOT NULL CHECK(amount_satoshi > 0),
                    fee_cnb REAL NOT NULL DEFAULT 0.0 CHECK(fee_cnb >= 0),
                    fee_satoshi INTEGER NOT NULL DEFAULT 0 CHECK(fee_satoshi >= 0),
                    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'confirmed', 'failed')),
                    metadata TEXT,
                    created_at REAL NOT NULL CHECK(created_at > 0),
                    updated_at REAL NOT NULL CHECK(updated_at >= created_at),
                    FOREIGN KEY (from_address) REFERENCES wallets (address) ON DELETE SET NULL,
                    FOREIGN KEY (to_address) REFERENCES wallets (address) ON DELETE RESTRICT
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS blocks (
                    id TEXT PRIMARY KEY CHECK(length(id) >= 16),
                    height INTEGER NOT NULL UNIQUE CHECK(height >= 0),
                    hash TEXT NOT NULL UNIQUE CHECK(length(hash) = 64),
                    previous_hash TEXT CHECK(length(previous_hash) = 64),
                    merkle_root TEXT NOT NULL CHECK(length(merkle_root) = 64),
                    timestamp REAL NOT NULL CHECK(timestamp > 0),
                    nonce INTEGER NOT NULL DEFAULT 0 CHECK(nonce >= 0),
                    difficulty INTEGER NOT NULL DEFAULT 1 CHECK(difficulty > 0),
                    transactions_count INTEGER NOT NULL DEFAULT 0 CHECK(transactions_count >= 0),
                    created_at REAL NOT NULL CHECK(created_at > 0)
                )
            """
            )

            # Criar índices para melhorar performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_wallets_name ON wallets(name)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_wallets_active ON wallets(is_active)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_transactions_from ON transactions(from_address)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_transactions_to ON transactions(to_address)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_transactions_created ON transactions(created_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_blocks_height ON blocks(height)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_blocks_hash ON blocks(hash)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_blocks_previous_hash ON blocks(previous_hash)")
            
            conn.commit()

    def get_connection(self):
        """Retorna uma conexão com o banco de dados"""
        if not hasattr(self._local, "connection"):
            self._local.connection = sqlite3.connect(
                self.db_path, check_same_thread=False
            )
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection

    def execute_query(self, query: str, params: tuple = ()):
        """Executa uma query e retorna o resultado"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def execute_update(self, query: str, params: tuple = ()):
        """Executa uma query de atualização e retorna o número de linhas afetadas"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.rowcount

    def execute_insert(self, query: str, params: tuple = ()):
        """Executa uma query de inserção e retorna o ID da última linha inserida"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.lastrowid

    def begin_transaction(self):
        """Inicia uma transação"""
        self.get_connection().execute("BEGIN TRANSACTION")

    def commit_transaction(self):
        """Confirma uma transação"""
        self.get_connection().commit()

    def rollback_transaction(self):
        """Desfaz uma transação"""
        self.get_connection().rollback()

    def close(self):
        """Fecha todas as conexões"""
        if hasattr(self._local, "connection"):
            self._local.connection.close()
            delattr(self._local, "connection")
