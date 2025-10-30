from __future__ import annotations
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Text, ForeignKey, JSON, TIMESTAMP, UniqueConstraint


class Base(DeclarativeBase):
    pass


class Block(Base):
    __tablename__ = "blocos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    indice: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    timestamp: Mapped[float] = mapped_column(Float, nullable=False)
    hash_anterior: Mapped[Optional[str]] = mapped_column(String(128))
    hash_atual: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    prova: Mapped[int] = mapped_column(Integer, nullable=False)
    dados: Mapped[dict] = mapped_column(JSON, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)


class Transaction(Base):
    __tablename__ = "transacoes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hash_transacao: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    bloco_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("blocos.id"))
    remetente: Mapped[str] = mapped_column(String(128), nullable=False)
    destinatario: Mapped[str] = mapped_column(String(128), nullable=False)
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    taxa: Mapped[float] = mapped_column(Float, default=0.0)
    assinatura: Mapped[str] = mapped_column(Text, nullable=False)
    chave_publica: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[float] = mapped_column(Float, nullable=False)
    dados_extra: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(32), default="pendente")


class Wallet(Base):
    __tablename__ = "carteiras"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    endereco: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    saldo: Mapped[float] = mapped_column(Float, default=0.0)
    chave_publica: Mapped[str] = mapped_column(Text, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    atualizado_em: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)


class User(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String(32), default="user")
    criado_em: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)


class Node(Base):
    __tablename__ = "nos_rede"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    endereco: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    ultima_sincronizacao: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
    status: Mapped[str] = mapped_column(String(32), default="ativo")
    criado_em: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
