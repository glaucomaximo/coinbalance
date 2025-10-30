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
        # Governance & DeFi
        self.db.propostas.create_index([("id", ASCENDING)], unique=True)
        self.db.propostas.create_index([("status", ASCENDING)])
        self.db.votos.create_index([("proposta_id", ASCENDING)])
        self.db.staking.create_index([("endereco", ASCENDING)], unique=True)
        self.db.lending.create_index([("endereco", ASCENDING)], unique=True)

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

    # --- Otimizados (aggregations) ---
    def obter_blocos_otimizado(self, limite: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        cur = self.db.blocos.find({}, {"_id": 0, "indice": 1, "timestamp": 1, "hash_anterior": 1, "hash_atual": 1, "prova": 1}) \
            .sort("indice", DESCENDING).skip(offset).limit(limite)
        return list(cur)

    def obter_transacoes_otimizado(self, remetente: Optional[str], destinatario: Optional[str], limite: int, offset: int) -> List[Dict[str, Any]]:
        filt: Dict[str, Any] = {}
        if remetente:
            filt["remetente"] = remetente
        if destinatario:
            filt["destinatario"] = destinatario
        cur = self.db.transacoes.find(filt, {"_id": 0, "id": 0}).sort("timestamp", DESCENDING).skip(offset).limit(limite)
        return list(cur)

    # --- Governance ---
    def governance_criar_proposta(self, titulo: str, descricao: str, tipo: str, parametros: Dict[str, Any], criador: str) -> Dict[str, Any]:
        pid = f"PROP_{int(self.db.command('hostInfo')['system']['currentTime'].timestamp())}"
        doc = {
            "id": pid,
            "titulo": titulo,
            "descricao": descricao,
            "tipo": tipo,
            "parametros": parametros,
            "criador": criador,
            "timestamp": None,
            "status": "ativa",
            "votos_favor": 0.0,
            "votos_contra": 0.0,
            "total_votos": 0.0,
        }
        self.db.propostas.insert_one(doc)
        return {"sucesso": True, "proposta_id": pid}

    def governance_votar(self, proposta_id: str, voto: bool, votante: str, peso_voto: float) -> Dict[str, Any]:
        prop = self.db.propostas.find_one({"id": proposta_id})
        if not prop or prop.get("status") != "ativa":
            return {"sucesso": False, "erro": "Proposta não encontrada/ativa"}
        self.db.votos.insert_one({"proposta_id": proposta_id, "voto": voto, "votante": votante, "peso_voto": peso_voto})
        inc = {"total_votos": peso_voto}
        if voto:
            inc["votos_favor"] = peso_voto
        else:
            inc["votos_contra"] = peso_voto
        self.db.propostas.update_one({"id": proposta_id}, {"$inc": inc})
        return {"sucesso": True, "voto_registrado": True}

    def governance_listar_ativas(self) -> List[Dict[str, Any]]:
        return list(self.db.propostas.find({"status": "ativa"}, {"_id": 0}))

    def governance_estatisticas(self) -> Dict[str, Any]:
        total = self.db.propostas.count_documents({})
        ativas = self.db.propostas.count_documents({"status": "ativa"})
        aprovadas = self.db.propostas.count_documents({"status": "aprovada"})
        return {"total_propostas": total, "propostas_ativas": ativas, "propostas_aprovadas": aprovadas}

    # --- DeFi (staking) ---
    def staking_stake(self, endereco: str, valor: float) -> Dict[str, Any]:
        doc = self.db.staking.find_one({"endereco": endereco}) or {"endereco": endereco, "valor": 0.0, "timestamp": 0.0}
        novo = float(doc.get("valor", 0.0)) + float(valor)
        self.db.staking.update_one({"endereco": endereco}, {"$set": {"valor": novo, "timestamp": 0.0}}, upsert=True)
        total_rede = self.db.staking.aggregate([{ "$group": {"_id": None, "total": {"$sum": "$valor"}}}])
        total_staked_rede = next(total_rede, {}).get("total", 0.0)
        return {"sucesso": True, "mensagem": f"Stake de {valor} tokens realizado", "total_staked": novo, "total_staked_rede": total_staked_rede}

    def staking_info(self, endereco: str) -> Dict[str, Any]:
        doc = self.db.staking.find_one({"endereco": endereco}) or {"valor": 0.0}
        total_rede = self.db.staking.aggregate([{ "$group": {"_id": None, "total": {"$sum": "$valor"}}}])
        total_staked_rede = next(total_rede, {}).get("total", 0.0)
        return {"sucesso": True, "stake_atual": float(doc.get("valor", 0.0)), "recompensas_pendentes": 0.0, "apy": 12.0, "total_staked_rede": total_staked_rede}

    # --- DeFi (lending) ---
    def lending_borrow(self, endereco: str, valor: float, colateral: float) -> Dict[str, Any]:
        # Simples: aprova se colateral >= 1.5x
        if float(colateral) < float(valor) * 1.5:
            return {"sucesso": False, "erro": "Colateral insuficiente"}
        self.db.lending.update_one({"endereco": endereco}, {"$set": {"valor": float(valor), "colateral": float(colateral), "juros": 0.05, "timestamp": 0.0}}, upsert=True)
        return {"sucesso": True, "mensagem": f"Empréstimo de {valor} tokens aprovado", "colateral_necessario": colateral, "taxa_juros": 5.0}
    
    def lending_info(self, endereco: str) -> Dict[str, Any]:
        doc = self.db.lending.find_one({"endereco": endereco})
        if not doc:
            return {"sucesso": True, "tem_emprestimo": False, "reservas_disponiveis": 0.0}
        return {"sucesso": True, "tem_emprestimo": True, "valor_emprestado": float(doc.get("valor", 0.0)), "juros_acumulados": 0.0, "valor_total_devido": float(doc.get("valor", 0.0)), "reservas_disponiveis": 0.0}

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