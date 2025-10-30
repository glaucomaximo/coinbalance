from fastapi.testclient import TestClient
import api_moderna

def test_governanca_fluxo_basico():
    client = TestClient(api_moderna.app)

    # Criar proposta de mudança de taxa
    payload = {
        "titulo": "Aumentar taxa base",
        "descricao": "Alterar taxa base para 0.002",
        "tipo": "mudanca_taxa",
        "parametros": {"nova_taxa": 0.002},
        "criador": "SYSTEM"
    }
    resp = client.post("/governance/proposta", json=payload)
    assert resp.status_code == 200, resp.text
    proposta_id = resp.json().get("proposta_id")
    assert proposta_id

    # Votar (peso pequeno, sem atingir quorum inicialmente)
    vote = {
        "proposta_id": proposta_id,
        "voto": True,
        "peso_voto": 1.0,
        "votante": "USER1"
    }
    resp_voto = client.post("/governance/votar", json=vote)
    assert resp_voto.status_code == 200, resp_voto.text
    data_voto = resp_voto.json()
    assert data_voto.get("sucesso") is True

    # Listar propostas ativas
    resp_list = client.get("/governance/propostas")
    assert resp_list.status_code == 200
    data_list = resp_list.json()
    assert "propostas" in data_list

    # Estatísticas
    resp_stats = client.get("/governance/estatisticas")
    assert resp_stats.status_code == 200
    assert "total_propostas" in resp_stats.json()
