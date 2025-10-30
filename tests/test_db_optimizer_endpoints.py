import os
from fastapi.testclient import TestClient

import api_moderna
from database_manager import DatabaseManager


def setup_module(module):
    test_db = "test_blockchain_opt.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    api_moderna.db_manager = DatabaseManager(test_db)


def teardown_module(module):
    test_db = "test_blockchain_opt.db"
    if os.path.exists(test_db):
        os.remove(test_db)


def test_endpoints_otimizacao_e_cache():
    client = TestClient(api_moderna.app)

    # Deve responder com sucesso, ainda que base vazia
    resp_perf = client.get("/admin/database/performance")
    assert resp_perf.status_code == 200
    assert resp_perf.json().get("status") in {"success", "error"}

    resp_cache = client.get("/admin/database/cache")
    assert resp_cache.status_code == 200
    assert resp_cache.json().get("status") == "success"

    # executar listagens otimizadas vazias
    resp_blocos = client.get("/blocos/otimizado")
    assert resp_blocos.status_code == 200
    assert resp_blocos.json().get("status") == "success"

    resp_trans = client.get("/transacoes/otimizado", params={"limite": 5})
    assert resp_trans.status_code == 200
    assert resp_trans.json().get("status") == "success"
