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
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or "blockchain.db"
        self._local = threading.local()
        self._init_database()

    def _init_database(self):
        """Inicializa o banco de dados e cria tabelas necessárias"""
        with self.get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS wallets (
                    address TEXT PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    public_key TEXT NOT NULL,
                    private_key TEXT NOT NULL,
                    balance_cnb REAL NOT NULL DEFAULT 0.0,
                    balance_satoshi INTEGER NOT NULL DEFAULT 0,
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    metadata TEXT,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    from_address TEXT,
                    to_address TEXT NOT NULL,
                    amount_cnb REAL NOT NULL,
                    amount_satoshi INTEGER NOT NULL,
                    fee_cnb REAL NOT NULL DEFAULT 0.0,
                    fee_satoshi INTEGER NOT NULL DEFAULT 0,
                    status TEXT NOT NULL DEFAULT 'pending',
                    metadata TEXT,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    FOREIGN KEY (from_address) REFERENCES wallets (address),
                    FOREIGN KEY (to_address) REFERENCES wallets (address)
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS blocks (
                    id TEXT PRIMARY KEY,
                    previous_hash TEXT,
                    merkle_root TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    nonce INTEGER NOT NULL DEFAULT 0,
                    difficulty INTEGER NOT NULL DEFAULT 1,
                    transactions_count INTEGER NOT NULL DEFAULT 0,
                    created_at REAL NOT NULL
                )
            """
            )

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
