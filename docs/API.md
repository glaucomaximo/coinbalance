# 📚 Documentação da API CryptoChain

## Visão Geral

A API CryptoChain é uma interface RESTful completa para interagir com a blockchain moderna. Todos os endpoints retornam JSON e seguem padrões REST.

**Base URL**: `http://localhost:8000`  
**Versão**: `2.0.0`  
**Formato**: JSON

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
  "remetente": "CRYPTO_abc123def456",
  "destinatario": "CRYPTO_xyz789ghi012",
  "valor": 100.0,
  "taxa": 0.001,
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
  "validacao": {
    "valida": true,
    "erros": [],
    "avisos": []
  }
}
```

#### Obter Histórico de Transações
```http
GET /transacoes/historico/{endereco}
```

**Resposta:**
```json
{
  "endereco": "CRYPTO_abc123def456",
  "transacoes": [
    {
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
