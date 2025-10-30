from __future__ import annotations
from typing import Any, Dict, List, Optional
import json
import hashlib
from contextlib import contextmanager
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from orm.models import Base, Block, Transaction, Wallet, User
import os


DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///blockchain.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    Base.metadata.create_all(engine)


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class SqlAlchemyDatabaseManager:
    def __init__(self):
        init_db()

    # ---- Helpers ----
    def _hash_transacao(self, transacao: Dict[str, Any]) -> str:
        transacao_str = json.dumps(transacao, sort_keys=True)
        return hashlib.sha256(transacao_str.encode()).hexdigest()

    # ---- Carteiras ----
    def atualizar_saldo_carteira(self, endereco: str, novo_saldo: float) -> bool:
        with get_session() as s:
            w = s.execute(select(Wallet).where(Wallet.endereco == endereco)).scalar_one_or_none()
            if not w:
                w = Wallet(endereco=endereco, saldo=float(novo_saldo), chave_publica="")
                s.add(w)
            else:
                w.saldo = float(novo_saldo)
            return True

    def obter_saldo_carteira(self, endereco: str) -> float:
        with get_session() as s:
            w = s.execute(select(Wallet.saldo).where(Wallet.endereco == endereco)).scalar_one_or_none()
            return float(w) if w is not None else 0.0

    # ---- Blocos ----
    def obter_todos_blocos(self) -> List[Dict[str, Any]]:
        with get_session() as s:
            rows = s.execute(select(Block).order_by(Block.indice)).scalars().all()
            return [b.dados for b in rows]

    def obter_bloco(self, indice: int) -> Optional[Dict[str, Any]]:
        with get_session() as s:
            b = s.execute(select(Block).where(Block.indice == indice)).scalar_one_or_none()
            return b.dados if b else None

    # ---- Transações ----
    def salvar_transacao(self, transacao: Dict[str, Any], bloco_id: int | None = None) -> bool:
        with get_session() as s:
            h = self._hash_transacao(transacao)
            t = s.execute(select(Transaction).where(Transaction.hash_transacao == h)).scalar_one_or_none()
            if not t:
                t = Transaction(
                    hash_transacao=h,
                    bloco_id=bloco_id,
                    remetente=transacao["remetente"],
                    destinatario=transacao["destinatario"],
                    valor=float(transacao["valor"]),
                    taxa=float(transacao.get("taxa", 0.0)),
                    assinatura=transacao.get("assinatura", ""),
                    chave_publica=transacao.get("chave_publica", ""),
                    timestamp=float(transacao["timestamp"]),
                    dados_extra=transacao.get("dados_extra", {}),
                    status="confirmada" if bloco_id else "pendente",
                )
                s.add(t)
            else:
                t.bloco_id = bloco_id
                t.status = "confirmada" if bloco_id else t.status
            return True

    def obter_transacao_por_hash(self, hash_transacao: str) -> Optional[Dict[str, Any]]:
        with get_session() as s:
            t = s.execute(select(Transaction).where(Transaction.hash_transacao == hash_transacao)).scalar_one_or_none()
            if not t:
                return None
            return {
                "id": t.id,
                "hash_transacao": t.hash_transacao,
                "remetente": t.remetente,
                "destinatario": t.destinatario,
                "valor": t.valor,
                "taxa": t.taxa,
                "timestamp": t.timestamp,
                "status": t.status,
            }

    def obter_historico_transacoes(self, endereco: str, limite: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        with get_session() as s:
            q = (
                select(Transaction)
                .where((Transaction.remetente == endereco) | (Transaction.destinatario == endereco))
                .order_by(Transaction.timestamp.desc())
                .offset(offset)
                .limit(limite)
            )
            rows = s.execute(q).scalars().all()
            return [
                {
                    "id": t.id,
                    "hash_transacao": t.hash_transacao,
                    "remetente": t.remetente,
                    "destinatario": t.destinatario,
                    "valor": t.valor,
                    "taxa": t.taxa,
                    "timestamp": t.timestamp,
                    "status": t.status,
                }
                for t in rows
            ]

    # ---- Usuários ----
    def criar_usuario(self, username: str, password_hash: str, role: str = "user") -> bool:
        with get_session() as s:
            u = s.execute(select(User).where(User.username == username)).scalar_one_or_none()
            if u:
                return False
            s.add(User(username=username, password_hash=password_hash, role=role))
            return True

    def obter_usuario(self, username: str) -> Optional[Dict[str, Any]]:
        with get_session() as s:
            u = s.execute(select(User).where(User.username == username)).scalar_one_or_none()
            return {"id": u.id, "username": u.username, "password_hash": u.password_hash, "role": u.role} if u else None
