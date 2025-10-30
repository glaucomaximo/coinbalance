import os
import pytest
from fastapi.testclient import TestClient

import api_moderna
from database_manager import DatabaseManager


def setup_module(module):
    # Isolar com um banco de testes
    test_db = "test_blockchain_tx.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    api_moderna.db_manager = DatabaseManager(test_db)


def teardown_module(module):
    # Limpar banco de testes
    test_db = "test_blockchain_tx.db"
    if os.path.exists(test_db):
        os.remove(test_db)


def test_criar_transacao_atualiza_saldos_e_persiste():
    client = TestClient(api_moderna.app)

    # Criar carteiras origem e destino
    resp1 = client.post("/carteiras/criar", json={"nome": "origem", "senha": "x"})
    assert resp1.status_code == 200
    carteira_origem = resp1.json()

    resp2 = client.post("/carteiras/criar", json={"nome": "destino", "senha": "y"})
    assert resp2.status_code == 200
    carteira_destino = resp2.json()

    # Dar saldo à carteira origem diretamente no DB
    origem_endereco = carteira_origem["endereco"]
    destino_endereco = carteira_destino["endereco"]

    assert api_moderna.db_manager.atualizar_saldo_carteira(origem_endereco, 10.0)
    assert api_moderna.db_manager.atualizar_saldo_carteira(destino_endereco, 0.0)

    # Criar transação
    payload = {
        "remetente": origem_endereco,
        "destinatario": destino_endereco,
        "valor": 1.0,
        # taxa opcional; default deve passar na validação
    }
    resp_tx = client.post("/transacoes/criar", json=payload)
    assert resp_tx.status_code == 200, resp_tx.text
    body = resp_tx.json()
    assert body["sucesso"] is True
    assert "hash_transacao" in body

    # Verificar saldos atualizados no DB
    saldo_origem = api_moderna.db_manager.obter_saldo_carteira(origem_endereco)
    saldo_destino = api_moderna.db_manager.obter_saldo_carteira(destino_endereco)

    assert saldo_destino >= 1.0
    assert saldo_origem <= 9.0  # desconta valor + taxa

    # Conferir listagem otimizada não falha
    resp_list = client.get("/transacoes/otimizado", params={"remetente": origem_endereco, "limite": 10})
    assert resp_list.status_code == 200
    data_list = resp_list.json()
    assert data_list["status"] == "success"
