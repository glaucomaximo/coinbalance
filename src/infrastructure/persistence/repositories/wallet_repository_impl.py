"""
Implementação concreta do WalletRepository

Este é o ADAPTER no padrão Hexagonal Architecture.
Implementa a interface (PORT) definida no domínio.
"""

from typing import Optional, List
import json

from src.domain.wallet.repositories.wallet_repository import WalletRepository
from src.domain.wallet.entities.wallet import Wallet
from src.domain.wallet.value_objects.wallet_address import WalletAddress
from src.domain.wallet.value_objects.private_key import PrivateKey
from src.domain.wallet.value_objects.public_key import PublicKey
from src.domain.wallet.value_objects.balance import Balance
from src.domain.shared.value_objects.timestamp import Timestamp
from src.infrastructure.persistence.database_manager import DatabaseManager
from src.infrastructure.security.encryption import EncryptionService


class WalletRepositoryImpl(WalletRepository):
    """
    Implementação de WalletRepository usando o DatabaseManager existente.

    Responsabilidades:
    - Mapear entidades de domínio para formato de persistência
    - Mapear dados persistidos para entidades de domínio
    - Gerenciar conexões com banco de dados
    """

    def __init__(self, db_manager):
        """
        Args:
            db_manager: Instância do DatabaseManager (legado)
        """
        self.db = db_manager
        self._cache: dict[str, Wallet] = {}
        self._encryption_service = EncryptionService()

    async def save(self, wallet: Wallet) -> None:
        """Salva ou atualiza carteira"""
        # Serializar para formato do banco
        wallet_data = self._to_persistence(wallet)

        # Salvar no banco usando o novo DatabaseManager
        query = """
            INSERT OR REPLACE INTO wallets
            (address, name, public_key, private_key, balance_cnb, balance_satoshi,
             is_active, metadata, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            wallet_data["address"],
            wallet_data["name"],
            wallet_data["public_key"],
            wallet_data["private_key"],
            wallet_data["balance_cnb"],
            wallet_data["balance_satoshi"],
            wallet_data["is_active"],
            wallet_data["metadata"],
            wallet_data["created_at"],
            wallet_data["updated_at"],
        )

        self.db.execute_insert(query, params)

        # Atualizar cache
        self._cache[wallet.address.value] = wallet

    async def find_by_address(self, address: WalletAddress) -> Optional[Wallet]:
        """Busca por endereço"""
        # Verificar cache
        if address.value in self._cache:
            return self._cache[address.value]

        # Buscar no banco usando o novo DatabaseManager
        query = "SELECT * FROM wallets WHERE address = ?"
        results = self.db.execute_query(query, (address.value,))

        if not results:
            return None

        # Reconstruir entidade
        wallet = self._from_persistence(dict(results[0]))

        # Atualizar cache
        self._cache[address.value] = wallet
        return wallet

    async def find_by_name(self, name: str) -> Optional[Wallet]:
        """Busca por nome"""
        # Buscar no banco usando o novo DatabaseManager
        query = "SELECT * FROM wallets WHERE name = ?"
        results = self.db.execute_query(query, (name,))

        if not results:
            return None

        # Reconstruir entidade
        wallet = self._from_persistence(dict(results[0]))

        # Atualizar cache
        self._cache[wallet.address.value] = wallet
        return wallet

    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Wallet]:
        """Lista todas as carteiras"""
        query = "SELECT * FROM wallets ORDER BY created_at DESC LIMIT ? OFFSET ?"
        results = self.db.execute_query(query, (limit, skip))

        wallets = []
        for row in results:
            wallet = self._from_persistence(dict(row))
            wallets.append(wallet)
            # Atualizar cache
            self._cache[wallet.address.value] = wallet

        return wallets

    async def find_active(self, skip: int = 0, limit: int = 100) -> List[Wallet]:
        """Lista carteiras ativas"""
        query = "SELECT * FROM wallets WHERE is_active = 1 ORDER BY created_at DESC LIMIT ? OFFSET ?"
        results = self.db.execute_query(query, (limit, skip))

        wallets = []
        for row in results:
            wallet = self._from_persistence(dict(row))
            wallets.append(wallet)
            # Atualizar cache
            self._cache[wallet.address.value] = wallet

        return wallets

    async def exists(self, address: WalletAddress) -> bool:
        """Verifica existência"""
        if address.value in self._cache:
            return True

        query = "SELECT 1 FROM wallets WHERE address = ?"
        results = self.db.execute_query(query, (address.value,))
        return len(results) > 0

    async def delete(self, address: WalletAddress) -> None:
        """Remove carteira"""
        if address.value in self._cache:
            del self._cache[address.value]

        query = "DELETE FROM wallets WHERE address = ?"
        self.db.execute_update(query, (address.value,))

    async def count(self) -> int:
        """Conta carteiras"""
        query = "SELECT COUNT(*) as count FROM wallets"
        results = self.db.execute_query(query)
        return results[0]["count"] if results else 0

    # ========== MAPEAMENTO ==========

    def _to_persistence(self, wallet: Wallet) -> dict:
        """Converte entidade para formato de persistência"""
        return {
            "address": wallet.address.value,
            "name": wallet.name,
            "public_key": wallet.public_key.value,
            "private_key": self._encryption_service.encrypt_private_key(wallet.private_key.reveal()),
            "balance_cnb": float(wallet.balance.to_cnb()),
            "balance_satoshi": wallet.balance.to_satoshi(),
            "created_at": wallet.created_at.value,
            "updated_at": wallet.updated_at.value,
            "is_active": wallet.is_active,
            "metadata": json.dumps(wallet.metadata),
        }

    def _from_persistence(self, data: dict) -> Wallet:
        """Reconstrói entidade a partir de dados persistidos"""
        return Wallet(
            address=WalletAddress.create(data["address"]),
            name=data["name"],
            public_key=PublicKey.create(data["public_key"]),
            private_key=(
                PrivateKey.from_string(self._encryption_service.decrypt_private_key(data["private_key"]))
                if data["private_key"]
                else PrivateKey.generate()
            ),
            balance=Balance.from_cnb(data["balance_cnb"]),
            created_at=Timestamp.from_seconds(data.get("created_at", 0)),
            updated_at=Timestamp.from_seconds(data.get("updated_at", 0)),
            is_active=data.get("is_active", True),
            metadata=(
                json.loads(data["metadata"])
                if isinstance(data.get("metadata"), str)
                else data.get("metadata", {})
            ),
        )
