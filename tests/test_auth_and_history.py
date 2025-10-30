from fastapi.testclient import TestClient
import api_moderna

def test_auth_required_on_defi_and_history_endpoint_works():
    client = TestClient(api_moderna.app)

    # Criar carteiras
    r1 = client.post("/carteiras/criar", json={"nome": "a", "senha": "x"})
    r2 = client.post("/carteiras/criar", json={"nome": "b", "senha": "y"})
    assert r1.status_code == 200 and r2.status_code == 200
    a = r1.json()["endereco"]
    b = r2.json()["endereco"]

    # Dar saldo a 'a'
    api_moderna.db_manager.atualizar_saldo_carteira(a, 5.0)

    # Sem token, deve bloquear /defi/stake
    resp_no_auth = client.post("/defi/stake", json={"valor": 1.0, "contrato": "STAKING_CONTRACT_001"})
    assert resp_no_auth.status_code in (401, 403)

    # Obter token
    tok = client.post("/auth/token", data={"username": "tester"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {tok}"}

    # Criar uma transação para gerar histórico
    resp_tx = client.post("/transacoes/criar", json={
        "remetente": a,
        "destinatario": b,
        "valor": 1.0,
        "taxa": 0.001
    })
    assert resp_tx.status_code == 200

    # Histórico deve responder
    hist = client.get(f"/transacoes/historico/{a}")
    assert hist.status_code == 200
    arr = hist.json()
    assert isinstance(arr, list)
    if arr:
        assert "taxa" in arr[0]

    # Com token, stake deve responder (mesmo que lógica interna falhe, deve responder 200/400 controlado)
    resp_stake = client.post("/defi/stake", json={"valor": 0.5, "contrato": "STAKING_CONTRACT_001"}, headers=headers)
    assert resp_stake.status_code in (200, 400)
