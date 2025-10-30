"""
MongoDatabaseManager - Persistência com MongoDB para CoinBalance.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
import threading
import json
import hashlib
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError


class MongoDatabaseManager:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "coinbalance"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.lock = threading.Lock()
        self._ensure_indexes()

    def _ensure_indexes(self):
        self.db.blocos.create_index([("indice", ASCENDING)], unique=True)
        self.db.blocos.create_index([("hash_atual", ASCENDING)], unique=True)
        self.db.transacoes.create_index([("hash_transacao", ASCENDING)], unique=True)
        self.db.transacoes.create_index([("remetente", ASCENDING)])
        self.db.transacoes.create_index([("destinatario", ASCENDING)])
        self.db.carteiras.create_index([("endereco", ASCENDING)], unique=True)
        self.db.usuarios.create_index([("username", ASCENDING)], unique=True)

    # --- Blocos ---
    def salvar_bloco(self, bloco: Dict[str, Any]) -> bool:
        try:
            doc = dict(bloco)
            # Normalizar campos
            doc["indice"] = bloco.get("indice")
            doc["hash_atual"] = bloco.get("hash_atual")
            self.db.blocos.update_one({"indice": doc["indice"]}, {"$set": doc}, upsert=True)
            return True
        except Exception:
            return False

    def obter_bloco(self, indice: int) -> Optional[Dict[str, Any]]:
        return self.db.blocos.find_one({"indice": indice}, {"_id": 0})

    def obter_ultimo_bloco(self) -> Optional[Dict[str, Any]]:
        return self.db.blocos.find_one(sort=[("indice", DESCENDING)], projection={"_id": 0})

    def obter_todos_blocos(self) -> List[Dict[str, Any]]:
        return list(self.db.blocos.find({}, {"_id": 0}).sort("indice", ASCENDING))

    # --- Transações ---
    def _gerar_hash_transacao(self, transacao: Dict[str, Any]) -> str:
        transacao_str = json.dumps({k: v for k, v in transacao.items() if k != "assinatura"}, sort_keys=True)
        return hashlib.sha256(transacao_str.encode()).hexdigest()

    def salvar_transacao(self, transacao: Dict[str, Any], bloco_id: int | None = None) -> bool:
        try:
            h = self._gerar_hash_transacao(transacao)
            doc = dict(transacao)
            doc["hash_transacao"] = h
            if bloco_id is not None:
                doc["bloco_id"] = bloco_id
                doc["status"] = "confirmada"
            else:
                doc.setdefault("status", "pendente")
            self.db.transacoes.update_one({"hash_transacao": h}, {"$set": doc}, upsert=True)
            return True
        except Exception:
            return False

    def obter_transacao_por_hash(self, hash_transacao: str) -> Optional[Dict[str, Any]]:
        return self.db.transacoes.find_one({"hash_transacao": hash_transacao}, {"_id": 0})

    def obter_historico_transacoes(self, endereco: str, limite: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        cur = self.db.transacoes.find({"$or": [{"remetente": endereco}, {"destinatario": endereco}]}, {"_id": 0}) \
            .sort("timestamp", DESCENDING).skip(offset).limit(limite)
        return list(cur)

    # --- Carteiras ---
    def atualizar_saldo_carteira(self, endereco: str, novo_saldo: float) -> bool:
        res = self.db.carteiras.update_one(
            {"endereco": endereco},
            {"$set": {"endereco": endereco, "saldo": float(novo_saldo)}},
            upsert=True,
        )
        return res.acknowledged

    def obter_saldo_carteira(self, endereco: str) -> float:
        doc = self.db.carteiras.find_one({"endereco": endereco}, {"_id": 0, "saldo": 1})
        return float(doc.get("saldo", 0.0)) if doc else 0.0

    # --- Usuários ---
    def criar_usuario(self, username: str, password_hash: str, role: str = "user") -> bool:
        try:
            self.db.usuarios.insert_one({
                "username": username,
                "password_hash": password_hash,
                "role": role,
                "criado_em": None,
            })
            return True
        except Exception:
            return False

    def obter_usuario(self, username: str) -> Optional[Dict[str, Any]]:
        doc = self.db.usuarios.find_one({"username": username}, {"_id": 0})
        return dict(doc) if doc else None
*** End Patch