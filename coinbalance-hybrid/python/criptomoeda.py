
from blocosencadeados import BlocosEncadeados
from time import time as tempo
from uuid import uuid4
from flask import Flask, jsonify, request

# Ligue o servidor
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Identificador da moeda Coinbalance (CNB)
identificador_do_elo = "Carteira Coinbalance (CNB)"

# Inicia a blockchain Coinbalance
blocosEncadeados = BlocosEncadeados()

@app.route('/mina', methods=['GET'])
def mina():
    # Isso executa nossa prova de algoritmo de trabalho definido acima, 
    # e registra quanto tempo leva para uma solução de força bruta
    horario_inicial = tempo()
    ultimo_bloco = blocosEncadeados.ultimo_bloco
    prova = blocosEncadeados.prova_de_trabalho(ultimo_bloco)
    decorrido = tempo() - horario_inicial

    # Pague algumas moedas CNB para uma sessão de mineração bem-sucedida.
    blocosEncadeados.nova_troca(
        remetente="Recompensa da mineradora Coinbalance",
        recebedor=identificador_do_elo,
        montante=3,
    )

    # Adicione o novo bloco à corrente!
    fragmento_anterior = blocosEncadeados.fragmento(ultimo_bloco)
    bloco = blocosEncadeados.novo_bloco(prova, fragmento_anterior)

    resposta = {
        'mensagem': "Novo bloco extraído e adicionado à blockchain Coinbalance!",
        'indice': bloco['indice'],
        'transacoes': bloco['transacoes'],
        'fragmento_anterior': bloco['fragmento_anterior'],
        'prova_de_trabalho': bloco['prova'],
        'tempo_necessario_segundos': decorrido,
        'moeda': 'CNB',
        'plataforma': 'Coinbalance'
    }
    return jsonify(resposta), 200


@app.route('/transacoes/nova', methods=['POST'])
def nova_troca():
    valores = request.get_json()

    # Verifica se os campos obrigatórios estão nos dados POSTADOS
    requerido = ['remetente', 'recebedor', 'montante']
    if not all(k in valores for k in requerido):
        return 'Valores ausentes', 400

    # Cria uma nova transação
    indice = blocosEncadeados.nova_troca(valores['remetente'], valores['recebedor'], valores['montante'])

    resposta = {
        'mensagem': f'Sucesso! Transação CNB registrada e será incluída no próximo bloco minado.',
        'moeda': 'CNB',
        'plataforma': 'Coinbalance'
    }
    return jsonify(resposta), 201


@app.route('/cadeia', methods=['GET'])
def cadeia_completa():
    resposta = {
        'cadeia': blocosEncadeados.cadeia,
        'comprimento': len(blocosEncadeados.cadeia),
        'moeda': 'CNB',
        'plataforma': 'Coinbalance',
        'framework': 'Coinbalance'
    }
    return jsonify(resposta), 200


@app.route('/elos/resgistrar', methods=['POST'])
def registrar_elos():
    valores = request.get_json()

    elos = valores.get('elos')
    if elos is None:
        return "Erro: forneça uma lista válida de elos", 400

    for elo in elos:
        blocosEncadeados.registrar_elo(elo)

    resposta = {
        'mensagem': 'Novo elo registrado com sucesso!',
        'elos_totais': list(blocosEncadeados.elos),
    }
    return jsonify(resposta), 201


@app.route('/elos/resolver', methods=['GET'])
def consenso():
    substituida = blocosEncadeados.resolver_conflitos()

    if substituida:
        resposta = {
            'mensagem': 'Encontrei uma cadeia mais atual em um elo diferente. Este elo foi atualizado!',
            'nova_cadeia': blocosEncadeados.cadeia
        }
    else:
        resposta = {
            'mensagem': 'Este elo já está atualizado!',
            'cadeia': blocosEncadeados.cadeia
        }

    return jsonify(resposta), 200


if __name__ == '__main__':
    from argparse import ArgumentParser as AnalisarArgumento

    analisador = AnalisarArgumento()
    analisador.add_argument('-p', '--port', default=5000, type=int, help='porta para ouvir')
    argumentos = analisador.parse_args()
    porta = argumentos.port

    app.run(host='0.0.0.0', port=porta)