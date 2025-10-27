# 📚 Documentação da API Coinbalance

## Visão Geral

A API Coinbalance é uma interface RESTful completa para interagir com a blockchain moderna e sistema de transações fracionadas. Todos os endpoints retornam JSON e seguem padrões REST.

**Base URL**: `http://localhost:8000`  
**Versão**: `2.1.0`  
**Formato**: JSON  
**Precisão**: 8 casas decimais (0.00000001 CNB = 1 satoshi)

## 🔐 Autenticação

A API usa autenticação baseada em JWT (JSON Web Tokens).

```http
Authorization: Bearer <seu_token_jwt>
```

## 📋 Endpoints

### 🔑 Carteiras

#### Criar Carteira
```http
POST /carteiras/criar
```

**Body:**
```json
{
  "nome": "minha_carteira",
  "senha": "senha_segura"
}
```

**Resposta:**
```json
{
  "endereco": "CRYPTO_abc123def456",
  "saldo": 0.0,
  "chave_publica": "-----BEGIN PUBLIC KEY-----...",
  "criado_em": 1640995200.0
}
```

#### Obter Carteira
```http
GET /carteiras/{nome}
```

**Resposta:**
```json
{
  "endereco": "CRYPTO_abc123def456",
  "saldo": 100.0,
  "chave_publica": "-----BEGIN PUBLIC KEY-----...",
  "criado_em": 1640995200.0
}
```

### 💸 Transações

#### Criar Transação
```http
POST /transacoes/criar
```

**Body:**
```json
{
  "remetente": "CNB_abc123def456",
  "destinatario": "CNB_xyz789ghi012",
  "valor": 100.0,
  "taxa": 0.001,
  "unidade": "cnb",
  "dados_extra": {
    "memo": "Pagamento de serviços"
  }
}
```

**Resposta:**
```json
{
  "sucesso": true,
  "mensagem": "Transação criada e processada com sucesso",
  "hash_transacao": "a1b2c3d4e5f6...",
  "valor_formatado": "100.00000000 CNB",
  "validacao": {
    "valida": true,
    "erros": [],
    "avisos": []
  }
}
```

#### Criar Transação Fracionada
```http
POST /transacoes/fracionada
```

**Body:**
```json
{
  "remetente": "CNB_abc123def456",
  "destinatario": "CNB_xyz789ghi012",
  "valor": 0.00000001,
  "unidade": "cnb",
  "dados_extra": {
    "memo": "Microtransação de 1 satoshi"
  }
}
```

**Resposta:**
```json
{
  "sucesso": true,
  "mensagem": "Transação fracionada criada e processada com sucesso",
  "hash_transacao": "a1b2c3d4e5f6...",
  "valor_original": "0.00000001 CNB",
  "valor_cnb": "0.00000001 CNB",
  "validacao": {
    "valida": true,
    "erros": [],
    "avisos": []
  }
}
```

#### Calcular Taxa de Transação
```http
GET /transacoes/calcular-taxa?valor=0.001&unidade=cnb
```

**Resposta:**
```json
{
  "valor_original": "0.001 CNB",
  "valor_cnb": "0.00100000 CNB",
  "taxa_cnb": "0.00000001 CNB",
  "taxa_satoshi": "1 sat",
  "taxa_mcnb": "0.000010 mCNB",
  "total_necessario": "0.00100001 CNB",
  "timestamp": 1640995200.0
}
```

#### Obter Histórico de Transações
```http
GET /transacoes/historico/{endereco}
```

**Resposta:**
```json
[
  {
    "hash": "a1b2c3d4e5f6...",
    "remetente": "CNB_abc123def456",
    "destinatario": "CNB_xyz789ghi012",
    "valor": 0.00000001,
    "taxa": 0.00000001,
    "timestamp": 1640995200.0,
    "status": "confirmada"
  }
]
```

### 🔄 Conversão de Unidades

#### Converter Unidades
```http
POST /conversao/unidades
```

**Body:**
```json
{
  "valor": 1.5,
  "unidade_origem": "cnb",
  "unidade_destino": "satoshi"
}
```

**Resposta:**
```json
{
  "sucesso": true,
  "conversao": {
    "valor_origem": "1.5 CNB",
    "valor_cnb": "1.50000000 CNB",
    "valor_destino": "150000000.00000000 SATOSHI",
    "taxa_conversao": "1 CNB = 100000000.00000000 SATOSHI"
  },
  "timestamp": 1640995200.0
}
```

#### Informações sobre Unidades
```http
GET /conversao/info
```

**Resposta:**
```json
{
  "unidades_disponiveis": {
    "cnb": {
      "nome": "Coinbalance",
      "descricao": "Unidade principal da moeda",
      "precisao": 8,
      "simbolo": "CNB"
    },
    "satoshi": {
      "nome": "Satoshi",
      "descricao": "Menor unidade (1 CNB = 100,000,000 satoshis)",
      "precisao": 0,
      "simbolo": "sat"
    },
    "mcnb": {
      "nome": "Micro CNB",
      "descricao": "Unidade intermediária (1 CNB = 1,000,000 mCNB)",
      "precisao": 6,
      "simbolo": "mCNB"
    }
  },
  "taxas_conversao": {
    "cnb_para_satoshi": 100000000,
    "cnb_para_mcnb": 1000000,
    "satoshi_para_cnb": 0.00000001,
    "mcnb_para_cnb": 0.000001
  },
  "precisao_decimal": 8,
  "valor_minimo": "0.00000001 CNB (1 satoshi)",
  "timestamp": 1640995200.0
}
```

### 💳 Carteiras Avançadas

#### Saldo Detalhado
```http
GET /carteiras/{endereco}/saldo/detalhado
```

**Resposta:**
```json
{
  "endereco": "CNB_abc123def456",
  "saldo": {
    "cnb": "1.50000000 CNB",
    "satoshi": "150000000 sat",
    "mcnb": "1500000.000000 mCNB"
  },
  "unidades": {
    "cnb": 1.5,
    "satoshi": 150000000,
    "mcnb": 1500000.0
  },
  "timestamp": 1640995200.0
}
```

## 🔢 Unidades e Precisão

### Unidades Disponíveis

| Unidade | Símbolo | Precisão | Conversão |
|---------|---------|----------|-----------|
| **CNB** | CNB | 8 casas | 1 CNB = 1 CNB |
| **Satoshi** | sat | 0 casas | 1 CNB = 100,000,000 sat |
| **mCNB** | mCNB | 6 casas | 1 CNB = 1,000,000 mCNB |

### Exemplos de Conversão

```python
# 1 CNB = 100,000,000 satoshis
1.0 CNB = 100000000 sat

# 1 satoshi = 0.00000001 CNB
1 sat = 0.00000001 CNB

# 1 CNB = 1,000,000 mCNB
1.0 CNB = 1000000.0 mCNB

# 1 mCNB = 0.000001 CNB
1.0 mCNB = 0.000001 CNB
```

### Valores Mínimos e Máximos

- **Valor mínimo**: 0.00000001 CNB (1 satoshi)
- **Valor máximo**: 100,000,000 CNB
- **Precisão**: 8 casas decimais
- **Taxa mínima**: 0.00000001 CNB (1 satoshi)

## 🚨 Códigos de Erro

| Código | Descrição |
|--------|-----------|
| `400` | Bad Request - Dados inválidos |
| `401` | Unauthorized - Token inválido |
| `403` | Forbidden - Acesso negado |
| `404` | Not Found - Recurso não encontrado |
| `422` | Unprocessable Entity - Validação falhou |
| `429` | Too Many Requests - Rate limit excedido |
| `500` | Internal Server Error - Erro interno |

## 📊 Exemplos de Uso

### Transação Mínima
```bash
curl -X POST "http://localhost:8000/transacoes/fracionada" \
  -H "Content-Type: application/json" \
  -d '{
    "remetente": "CNB_abc123...",
    "destinatario": "CNB_def456...",
    "valor": 0.00000001,
    "unidade": "cnb"
  }'
```

### Conversão de Unidades
```bash
curl -X POST "http://localhost:8000/conversao/unidades" \
  -H "Content-Type: application/json" \
  -d '{
    "valor": 1.5,
    "unidade_origem": "cnb",
    "unidade_destino": "satoshi"
  }'
```

### Calcular Taxa
```bash
curl -X GET "http://localhost:8000/transacoes/calcular-taxa?valor=0.001&unidade=cnb"
```

## 🔗 Links Úteis

- **Documentação Swagger**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`
- **Métricas**: `http://localhost:8000/metrics`

---

**Coinbalance API v2.1.0** - A Economia da Consciência 💚
      "hash": "a1b2c3d4e5f6...",
      "tipo": "enviada",
      "destinatario": "CRYPTO_xyz789ghi012",
      "valor": 100.0,
      "timestamp": 1640995200.0,
      "status": "confirmada"
    }
  ],
  "total": 1
}
```

### ⛓️ Blockchain

#### Obter Blockchain Completa
```http
GET /blockchain
```

**Resposta:**
```json
{
  "blockchain": [
    {
      "indice": 1,
      "timestamp": 1640995200.0,
      "hash_anterior": "0000000000000000",
      "hash_atual": "a1b2c3d4e5f6...",
      "prova": 12345,
      "transacoes": []
    }
  ],
  "comprimento": 1,
  "hash_ultimo_bloco": "a1b2c3d4e5f6..."
}
```

#### Obter Bloco Específico
```http
GET /blockchain/{indice}
```

**Resposta:**
```json
{
  "indice": 1,
  "timestamp": 1640995200.0,
  "hash_anterior": "0000000000000000",
  "hash_atual": "a1b2c3d4e5f6...",
  "prova": 12345,
  "transacoes": [],
  "tempo_mineracao": 2.5
}
```

#### Minerar Bloco
```http
POST /mineracao/minerar
```

**Resposta:**
```json
{
  "sucesso": true,
  "mensagem": "Mineração iniciada",
  "timestamp": 1640995200.0,
  "bloco_minerado": {
    "indice": 2,
    "hash": "b2c3d4e5f6g7...",
    "transacoes_incluidas": 5
  }
}
```

### 🏦 DeFi

#### Fazer Stake
```http
POST /defi/stake
```

**Body:**
```json
{
  "valor": 1000.0,
  "contrato": "STAKING_CONTRACT_001"
}
```

**Resposta:**
```json
{
  "sucesso": true,
  "mensagem": "Stake de 1000.0 tokens realizado",
  "total_staked": 1000.0,
  "apy": 12.0
}
```

#### Solicitar Empréstimo
```http
POST /defi/borrow
```

**Body:**
```json
{
  "valor": 500.0,
  "colateral": 750.0
}
```

**Resposta:**
```json
{
  "sucesso": true,
  "mensagem": "Empréstimo de 500.0 tokens aprovado",
  "colateral_necessario": 750.0,
  "taxa_juros": 5.0
}
```

#### Obter Informações de Staking
```http
GET /defi/stake/info
```

**Resposta:**
```json
{
  "sucesso": true,
  "stake_atual": 1000.0,
  "recompensas_pendentes": 25.5,
  "apy": 12.0,
  "total_staked_rede": 50000.0
}
```

#### Listar Contratos DeFi
```http
GET /defi/contratos
```

**Resposta:**
```json
{
  "contratos": [
    {
      "endereco": "STAKING_CONTRACT_001",
      "tipo": "StakingContract",
      "criador": "SYSTEM",
      "criado_em": 1640995200.0
    },
    {
      "endereco": "LENDING_CONTRACT_001",
      "tipo": "LendingContract",
      "criador": "SYSTEM",
      "criado_em": 1640995200.0
    }
  ],
  "total": 2
}
```

### 🏛️ Governança

#### Criar Proposta
```http
POST /governance/proposta
```

**Body:**
```json
{
  "titulo": "Aumentar taxa de staking",
  "descricao": "Proposta para aumentar APY de 12% para 15%",
  "tipo": "mudanca_taxa",
  "parametros": {
    "nova_taxa": 0.15
  }
}
```

**Resposta:**
```json
{
  "sucesso": true,
  "proposta_id": "PROP_1640995200",
  "mensagem": "Proposta criada com sucesso"
}
```

#### Votar em Proposta
```http
POST /governance/votar
```

**Body:**
```json
{
  "proposta_id": "PROP_1640995200",
  "voto": true,
  "peso_voto": 1000.0
}
```

**Resposta:**
```json
{
  "sucesso": true,
  "voto_registrado": true,
  "resultado": {
    "aprovada": false,
    "motivo": "Ainda não atingiu quorum"
  }
}
```

#### Listar Propostas
```http
GET /governance/propostas
```

**Resposta:**
```json
{
  "propostas": [
    {
      "id": "PROP_1640995200",
      "titulo": "Aumentar taxa de staking",
      "descricao": "Proposta para aumentar APY de 12% para 15%",
      "tipo": "mudanca_taxa",
      "status": "ativa",
      "votos_favor": 5000.0,
      "votos_contra": 2000.0,
      "total_votos": 7000.0
    }
  ],
  "total": 1
}
```

### 📊 Estatísticas

#### Obter Estatísticas da Rede
```http
GET /estatisticas
```

**Resposta:**
```json
{
  "blockchain": {
    "total_blocos": 150,
    "ultimo_bloco": {
      "indice": 150,
      "hash": "z9y8x7w6v5u4...",
      "timestamp": 1640995200.0
    },
    "hash_atual": "z9y8x7w6v5u4..."
  },
  "contratos": {
    "total_contratos": 2,
    "tipos": ["StakingContract", "LendingContract"]
  },
  "rede": {
    "status": "ativa",
    "timestamp": 1640995200.0,
    "nos_conectados": 5
  }
}
```

## 🚨 Códigos de Erro

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 201 | Criado com sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |
| 403 | Acesso negado |
| 404 | Não encontrado |
| 409 | Conflito |
| 422 | Dados inválidos |
| 500 | Erro interno do servidor |

## 📝 Exemplos de Uso

### Python
```python
import requests

# Criar carteira
response = requests.post('http://localhost:8000/carteiras/criar', json={
    'nome': 'minha_carteira',
    'senha': 'senha_segura'
})
carteira = response.json()

# Fazer transação
response = requests.post('http://localhost:8000/transacoes/criar', json={
    'remetente': carteira['endereco'],
    'destinatario': 'CRYPTO_destino',
    'valor': 100.0
})
transacao = response.json()

# Fazer stake
response = requests.post('http://localhost:8000/defi/stake', json={
    'valor': 1000.0
})
stake = response.json()
```

### JavaScript
```javascript
// Criar carteira
const carteira = await fetch('http://localhost:8000/carteiras/criar', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    nome: 'minha_carteira',
    senha: 'senha_segura'
  })
}).then(r => r.json());

// Fazer transação
const transacao = await fetch('http://localhost:8000/transacoes/criar', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    remetente: carteira.endereco,
    destinatario: 'CRYPTO_destino',
    valor: 100.0
  })
}).then(r => r.json());
```

### cURL
```bash
# Criar carteira
curl -X POST http://localhost:8000/carteiras/criar \
  -H "Content-Type: application/json" \
  -d '{"nome": "minha_carteira", "senha": "senha_segura"}'

# Fazer transação
curl -X POST http://localhost:8000/transacoes/criar \
  -H "Content-Type: application/json" \
  -d '{"remetente": "CRYPTO_origem", "destinatario": "CRYPTO_destino", "valor": 100.0}'
```

## 🔧 Configuração

### Variáveis de Ambiente
```bash
# Banco de dados
DATABASE_URL=sqlite:///data/blockchain.db

# Redis
REDIS_URL=redis://localhost:6379

# Segurança
SECRET_KEY=sua_chave_secreta
JWT_SECRET=jwt_secret

# Rede
NETWORK_ID=mainnet
PORT=8000
```

### Rate Limiting
- **1000 requests/hora** por IP
- **100 requests/minuto** por usuário
- **10 requests/segundo** por endpoint

## 📞 Suporte

- **Documentação**: [docs.cryptochain.com](https://docs.cryptochain.com)
- **Discord**: [discord.gg/cryptochain](https://discord.gg/cryptochain)
- **Email**: api-support@cryptochain.com
- **GitHub**: [Issues](https://github.com/seu-usuario/cryptochain/issues)
