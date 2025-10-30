import types
import pytest

from services.transaction_service import TransactionService


class DummyWallet:
    def __init__(self, endereco: str, saldo: float):
        self.endereco = endereco
        self.saldo = saldo
        self.public_key = "PUB"
        self.private_key = "PRIV"

    def criar_transacao(self, destinatario, valor, dados_extra):
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente")
        return {
            "remetente": self.endereco,
            "destinatario": destinatario,
            "valor": valor,
            "timestamp": 1.0,
            "dados_extra": dados_extra,
            "assinatura": "sig",
            "chave_publica": self.public_key,
        }


class DummyWalletManager:
    def __init__(self):
        self.carteiras = {"a": DummyWallet("A", 10.0)}


class DummyDB:
    def __init__(self):
        self.saved = []

    def obter_saldo_carteira(self, endereco):
        return 10.0

    def salvar_transacao(self, t):
        self.saved.append(t)
        return True


class DummyValidator:
    def __init__(self):
        pass

    def validar_transacao(self, t):
        return {"valida": True, "erros": [], "avisos": []}

    def processar_transacao(self, t):
        return True

    def _gerar_hash_transacao(self, t):
        return "HASH"


def test_transaction_service_happy_path():
    svc = TransactionService(DummyDB(), DummyWalletManager(), DummyValidator())
    result = svc.create_and_process("A", "B", 1.0, {"memo": "x"}, taxa=0.001)
    assert result["sucesso"] is True
    assert result["hash_transacao"] == "HASH"
