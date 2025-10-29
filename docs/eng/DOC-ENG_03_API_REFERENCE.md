# 📡 DOC-ENG_03_API_REFERENCE
## Referência Completa da API REST - CoinBalance Enterprise v3.0.0

**Versão:** 1.0  
**Data de Criação:** 29 de outubro de 2025  
**Última Atualização:** 29 de outubro de 2025  
**Autor:** Engenharia de Documentação Sênior  
**Status:** ✅ **COMPLETO**

---

## 📋 Sumário Executivo

Este documento fornece referência completa da API REST do CoinBalance Enterprise, incluindo todos os endpoints, schemas de dados, autenticação, exemplos de uso e códigos de erro.

---

## 🌐 Visão Geral das APIs

### **Base URL**

```
Produção: https://api.coinbalance.com/api/v1
Desenvolvimento: http://localhost:8000/api/v1
```

### **Versionamento**

A API utiliza versionamento por URL:
- **v1**: Versão atual estável
- Endpoints futuros: `/api/v2/...`

### **Formato de Resposta Padrão**

```json
{
  "success": true,
  "data": { ... },
  "message": "Operação realizada com sucesso",
  "timestamp": 1698624000.0
}
```

### **Códigos de Status HTTP**

| Código | Descrição | Uso |
|--------|-----------|-----|
| **200** | OK | Operação bem-sucedida |
| **201** | Created | Recurso criado com sucesso |
| **400** | Bad Request | Erro de validação |
| **401** | Unauthorized | Não autenticado |
| **403** | Forbidden | Não autorizado |
| **404** | Not Found | Recurso não encontrado |
| **422** | Unprocessable Entity | Erro de validação Pydantic |
| **500** | Internal Server Error | Erro interno do servidor |

---

## 🔐 Autenticação e Autorização

### **Autenticação JWT**

A API utiliza JSON Web Tokens (JWT) para autenticação.

#### **Obter Token**

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "usuario",
  "password": "senha"
}
```

**Resposta:**

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600
  }
}
```

#### **Usar Token**

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### **Roles e Permissões**

| Role | Permissões |
|------|------------|
| **admin** | Acesso completo |
| **user** | Operações básicas |
| **viewer** | Apenas leitura |

---

## 📚 Endpoints por Categoria

### **1. Health & Info**

#### **GET /** - Informações Básicas

```http
GET /
```

**Resposta:**

```json
{
  "name": "CoinBalance Enterprise",
  "version": "3.0.0",
  "status": "operational"
}
```

#### **GET /health** - Health Check

```http
GET /health
```

**Resposta:**

```json
{
  "status": "healthy",
  "checks": {
    "database": "ok",
    "blockchain": "ok"
  }
}
```

#### **GET /metrics** - Métricas Prometheus

```http
GET /metrics
```

**Resposta:** Formato Prometheus

---

### **2. Autenticação**

#### **POST /api/v1/auth/login** - Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "usuario",
  "password": "senha"
}
```

#### **POST /api/v1/auth/register** - Registro

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "novo_usuario",
  "password": "senha_segura",
  "email": "usuario@example.com"
}
```

#### **POST /api/v1/auth/refresh** - Refresh Token

```http
POST /api/v1/auth/refresh
Authorization: Bearer {refresh_token}
```

---

### **3. Carteiras (Wallets)**

#### **GET /api/v1/wallets** - Listar Carteiras

```http
GET /api/v1/wallets?page=1&limit=20
Authorization: Bearer {token}
```

**Query Parameters:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `page` | integer | Página (padrão: 1) |
| `limit` | integer | Itens por página (padrão: 20) |
| `is_active` | boolean | Filtrar por status |

**Resposta:**

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "name": "Minha Carteira",
        "balance_cnb": 1000.0,
        "balance_satoshi": 100000000,
        "is_active": true,
        "created_at": 1698624000.0
      }
    ],
    "total": 50,
    "page": 1,
    "limit": 20
  }
}
```

#### **POST /api/v1/wallets** - Criar Carteira

```http
POST /api/v1/wallets
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Nova Carteira"
}
```

**Resposta:**

```json
{
  "success": true,
  "data": {
    "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "name": "Nova Carteira",
    "balance_cnb": 0.0,
    "created_at": 1698624000.0
  }
}
```

#### **GET /api/v1/wallets/{address}** - Obter Carteira

```http
GET /api/v1/wallets/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
Authorization: Bearer {token}
```

#### **PUT /api/v1/wallets/{address}** - Atualizar Carteira

```http
PUT /api/v1/wallets/{address}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Nome Atualizado"
}
```

---

### **4. Transações**

#### **POST /api/v1/transactions** - Criar Transação

```http
POST /api/v1/transactions
Authorization: Bearer {token}
Content-Type: application/json

{
  "from_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
  "to_address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
  "amount_cnb": 10.5
}
```

**Resposta:**

```json
{
  "success": true,
  "data": {
    "id": "tx_abc123...",
    "from_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "to_address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
    "amount_cnb": 10.5,
    "status": "pending",
    "created_at": 1698624000.0
  }
}
```

#### **GET /api/v1/transactions** - Listar Transações

```http
GET /api/v1/transactions?page=1&limit=20&status=confirmed
Authorization: Bearer {token}
```

**Query Parameters:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `page` | integer | Página |
| `limit` | integer | Itens por página |
| `status` | string | Filtrar por status (pending, confirmed, failed) |
| `from_address` | string | Filtrar por endereço origem |
| `to_address` | string | Filtrar por endereço destino |

#### **GET /api/v1/transactions/{id}** - Obter Transação

```http
GET /api/v1/transactions/tx_abc123...
Authorization: Bearer {token}
```

---

### **5. Blockchain**

#### **GET /api/v1/blockchain** - Informações da Blockchain

```http
GET /api/v1/blockchain
Authorization: Bearer {token}
```

**Resposta:**

```json
{
  "success": true,
  "data": {
    "height": 12345,
    "total_blocks": 12345,
    "total_transactions": 98765,
    "total_supply": 21000000.0,
    "difficulty": 5,
    "last_block_hash": "00000abc123..."
  }
}
```

#### **GET /api/v1/blockchain/blocks** - Listar Blocos

```http
GET /api/v1/blockchain/blocks?page=1&limit=20
Authorization: Bearer {token}
```

#### **GET /api/v1/blockchain/blocks/{height}** - Obter Bloco

```http
GET /api/v1/blockchain/blocks/12345
Authorization: Bearer {token}
```

**Resposta:**

```json
{
  "success": true,
  "data": {
    "height": 12345,
    "hash": "00000abc123...",
    "previous_hash": "00000def456...",
    "merkle_root": "789ghi...",
    "timestamp": 1698624000.0,
    "nonce": 123456,
    "difficulty": 5,
    "transactions_count": 10,
    "transactions": [...]
  }
}
```

#### **POST /api/v1/blockchain/mine** - Minerar Bloco

```http
POST /api/v1/blockchain/mine
Authorization: Bearer {token}
Content-Type: application/json

{
  "miner_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
}
```

---

### **6. Consenso**

#### **GET /api/v1/consensus/validators** - Listar Validadores

```http
GET /api/v1/consensus/validators
Authorization: Bearer {token}
```

#### **POST /api/v1/consensus/validators** - Registrar Validador

```http
POST /api/v1/consensus/validators
Authorization: Bearer {token}
Content-Type: application/json

{
  "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
  "stake": 1000.0
}
```

#### **GET /api/v1/consensus/stats** - Estatísticas de Consenso

```http
GET /api/v1/consensus/stats
Authorization: Bearer {token}
```

---

### **7. Web3**

#### **GET /api/v1/web3/networks** - Listar Redes Suportadas

```http
GET /api/v1/web3/networks
Authorization: Bearer {token}
```

**Resposta:**

```json
{
  "success": true,
  "data": {
    "networks": [
      {
        "name": "Ethereum",
        "chain_id": 1,
        "rpc_url": "https://eth-mainnet.g.alchemy.com/v2/...",
        "status": "active"
      },
      {
        "name": "BSC",
        "chain_id": 56,
        "rpc_url": "https://bsc-dataseed.binance.org/",
        "status": "active"
      }
    ]
  }
}
```

#### **GET /api/v1/web3/balance/{address}** - Consultar Saldo Web3

```http
GET /api/v1/web3/balance/{address}?network=ethereum
Authorization: Bearer {token}
```

---

### **8. Monitoramento**

#### **GET /api/v1/monitoring/health** - Health Check Detalhado

```http
GET /api/v1/monitoring/health
Authorization: Bearer {token}
```

#### **GET /api/v1/monitoring/metrics** - Métricas do Sistema

```http
GET /api/v1/monitoring/metrics
Authorization: Bearer {token}
```

#### **GET /api/v1/monitoring/alerts** - Alertas Ativos

```http
GET /api/v1/monitoring/alerts
Authorization: Bearer {token}
```

---

### **9. LGPD Compliance**

#### **POST /api/v1/lgpd/data-subject-request** - Solicitação de Dados

```http
POST /api/v1/lgpd/data-subject-request
Authorization: Bearer {token}
Content-Type: application/json

{
  "request_type": "access",
  "data_subject": "usuario@example.com"
}
```

**Request Types:**
- `access` - Acesso aos dados
- `rectification` - Retificação
- `erasure` - Exclusão
- `opposition` - Oposição ao tratamento

---

## 📊 Schemas de Dados

### **Wallet Schema**

```json
{
  "address": "string (26-62 caracteres)",
  "name": "string (3-50 caracteres)",
  "balance_cnb": "float (>= 0)",
  "balance_satoshi": "integer (>= 0)",
  "is_active": "boolean",
  "created_at": "float (timestamp)"
}
```

### **Transaction Schema**

```json
{
  "id": "string (>= 16 caracteres)",
  "from_address": "string (opcional, 26-62 caracteres)",
  "to_address": "string (obrigatório, 26-62 caracteres)",
  "amount_cnb": "float (> 0)",
  "amount_satoshi": "integer (> 0)",
  "fee_cnb": "float (>= 0)",
  "status": "string (pending|confirmed|failed)",
  "created_at": "float (timestamp)"
}
```

### **Block Schema**

```json
{
  "height": "integer (>= 0)",
  "hash": "string (64 caracteres hex)",
  "previous_hash": "string (64 caracteres hex ou null)",
  "merkle_root": "string (64 caracteres hex)",
  "timestamp": "float (timestamp)",
  "nonce": "integer (>= 0)",
  "difficulty": "integer (> 0)",
  "transactions_count": "integer (>= 0)"
}
```

---

## ⚠️ Códigos de Erro

### **Erros de Validação (422)**

```json
{
  "success": false,
  "error": "Validation error",
  "code": "VALIDATION_ERROR",
  "details": [
    {
      "field": "amount_cnb",
      "message": "must be greater than 0",
      "type": "value_error"
    }
  ]
}
```

### **Erros de Domínio (400)**

```json
{
  "success": false,
  "error": "Insufficient balance",
  "code": "INSUFFICIENT_BALANCE",
  "message": "Wallet does not have enough balance",
  "timestamp": 1698624000.0
}
```

### **Erros de Autenticação (401)**

```json
{
  "success": false,
  "error": "Unauthorized",
  "code": "UNAUTHORIZED",
  "message": "Invalid or expired token"
}
```

### **Erros de Autorização (403)**

```json
{
  "success": false,
  "error": "Forbidden",
  "code": "FORBIDDEN",
  "message": "Insufficient permissions"
}
```

### **Erros Internos (500)**

```json
{
  "success": false,
  "error": "Internal server error",
  "code": "INTERNAL_ERROR",
  "message": "An error occurred"
}
```

---

## 📝 Exemplos de Uso

### **Exemplo Completo: Criar Carteira e Fazer Transação**

```bash
# 1. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "senha"}'

# Resposta: {"access_token": "eyJ..."}

# 2. Criar Carteira
curl -X POST http://localhost:8000/api/v1/wallets \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{"name": "Minha Carteira"}'

# Resposta: {"address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", ...}

# 3. Criar Transação
curl -X POST http://localhost:8000/api/v1/transactions \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "from_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "to_address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
    "amount_cnb": 10.5
  }'
```

---

## 📊 Rate Limiting

### **Limites por Endpoint**

| Endpoint | Limite | Período |
|----------|--------|---------|
| `/api/v1/auth/login` | 5 | 1 minuto |
| `/api/v1/wallets` (POST) | 10 | 1 minuto |
| `/api/v1/transactions` (POST) | 20 | 1 minuto |
| Outros endpoints | 100 | 1 minuto |

### **Headers de Rate Limiting**

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1698624060
```

---

## ✅ Histórico de Versões

| Versão | Data | Alterações | Autor |
|--------|------|------------|-------|
| 1.0 | 29/10/2025 | Criação da referência completa de API | Eng. Documentação Sênior |

---

**Status:** ✅ **FASE 3 PARCIAL - API REFERENCE COMPLETA**

