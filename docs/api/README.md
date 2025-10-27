# 🔌 API Reference - CoinBalance

## 📋 **Visão Geral**

A API CoinBalance fornece endpoints RESTful para gerenciamento de carteiras digitais e operações de criptomoeda.

**Base URL**: `http://localhost:8001/api/v1`

---

## 🚀 **Endpoints Disponíveis**

### **1. Carteiras**

#### **Criar Carteira**
```http
POST /api/v1/carteiras/
```

**Request Body**:
```json
{
  "name": "Minha Carteira",
  "password": "senha12345",
  "metadata": {
    "description": "Carteira principal"
  }
}
```

**Response** (201 Created):
```json
{
  "address": "a1b2c3d4e5f6...",
  "name": "Minha Carteira",
  "public_key": "pub_key_here",
  "balance_cnb": 0.0,
  "balance_satoshi": 0,
  "created_at": 1761582890.0854228,
  "updated_at": 1761582890.0854228,
  "is_active": true,
  "metadata": {
    "description": "Carteira principal"
  }
}
```

#### **Buscar Carteira por Endereço**
```http
GET /api/v1/carteiras/{address}
```

**Response** (200 OK):
```json
{
  "address": "a1b2c3d4e5f6...",
  "name": "Minha Carteira",
  "public_key": "pub_key_here",
  "balance_cnb": 100.0,
  "balance_satoshi": 10000000000,
  "created_at": 1761582890.0854228,
  "updated_at": 1761582890.0854228,
  "is_active": true,
  "metadata": {
    "description": "Carteira principal"
  }
}
```

#### **Listar Todas as Carteiras**
```http
GET /api/v1/carteiras/
```

**Response** (200 OK):
```json
{
  "wallets": [
    {
      "address": "a1b2c3d4e5f6...",
      "name": "Carteira 1",
      "public_key": "pub_key_1",
      "balance_cnb": 50.0,
      "balance_satoshi": 5000000000,
      "created_at": 1761582890.0854228,
      "updated_at": 1761582890.0854228,
      "is_active": true,
      "metadata": {}
    }
  ],
  "total": 1
}
```

#### **Creditar Saldo**
```http
POST /api/v1/carteiras/{address}/credit
```

**Request Body**:
```json
{
  "amount": 100.0,
  "reason": "Depósito inicial"
}
```

**Response** (200 OK):
```json
{
  "address": "a1b2c3d4e5f6...",
  "name": "Minha Carteira",
  "public_key": "pub_key_here",
  "balance_cnb": 100.0,
  "balance_satoshi": 10000000000,
  "created_at": 1761582890.0854228,
  "updated_at": 1761582890.0854228,
  "is_active": true,
  "metadata": {}
}
```

#### **Debitar Saldo**
```http
POST /api/v1/carteiras/{address}/debit
```

**Request Body**:
```json
{
  "amount": 50.0,
  "reason": "Pagamento de serviço"
}
```

**Response** (200 OK):
```json
{
  "address": "a1b2c3d4e5f6...",
  "name": "Minha Carteira",
  "public_key": "pub_key_here",
  "balance_cnb": 50.0,
  "balance_satoshi": 5000000000,
  "created_at": 1761582890.0854228,
  "updated_at": 1761582890.0854228,
  "is_active": true,
  "metadata": {}
}
```

---

## 📊 **Códigos de Status HTTP**

| Código | Descrição | Uso |
|--------|-----------|-----|
| `200` | OK | Operação bem-sucedida |
| `201` | Created | Carteira criada com sucesso |
| `400` | Bad Request | Dados inválidos |
| `404` | Not Found | Carteira não encontrada |
| `409` | Conflict | Nome de carteira já existe |
| `422` | Unprocessable Entity | Erro de validação |
| `500` | Internal Server Error | Erro interno do servidor |

---

## ⚠️ **Tratamento de Erros**

### **Formato Padrão de Erro**
```json
{
  "success": false,
  "error": "Descrição do erro",
  "code": "ERROR_CODE",
  "details": [
    {
      "type": "validation_error",
      "loc": ["body", "field"],
      "msg": "Mensagem específica",
      "input": "valor_inválido"
    }
  ],
  "timestamp": 1761582890.0854228
}
```

### **Exemplos de Erros**

#### **Carteira Não Encontrada** (404)
```json
{
  "success": false,
  "error": "Wallet with address 'invalid_address' not found",
  "code": "WALLET_NOT_FOUND",
  "details": [],
  "timestamp": 1761582890.0854228
}
```

#### **Saldo Insuficiente** (400)
```json
{
  "success": false,
  "error": "Insufficient balance",
  "code": "INSUFFICIENT_BALANCE",
  "details": [
    {
      "type": "business_rule",
      "loc": ["body", "amount"],
      "msg": "Saldo insuficiente para esta operação",
      "input": 1000.0
    }
  ],
  "timestamp": 1761582890.0854228
}
```

#### **Validação de Dados** (422)
```json
{
  "success": false,
  "error": "Validation error",
  "code": "VALIDATION_ERROR",
  "details": [
    {
      "type": "string_too_short",
      "loc": ["body", "password"],
      "msg": "String should have at least 8 characters",
      "input": "123",
      "ctx": {
        "min_length": 8
      }
    }
  ],
  "timestamp": 1761582890.0854228
}
```

---

## 🔒 **Validações**

### **Criação de Carteira**
- **name**: String, obrigatório, 1-100 caracteres
- **password**: String, obrigatório, mínimo 8 caracteres
- **metadata**: Object, opcional

### **Operações Monetárias**
- **amount**: Number, obrigatório, > 0
- **reason**: String, obrigatório, 1-200 caracteres

### **Endereços**
- **address**: String, formato hexadecimal, 40 caracteres

---

## 📈 **Limites e Rate Limiting**

### **Limites Atuais**
- **Criação de carteiras**: Sem limite
- **Operações por minuto**: Sem limite
- **Tamanho de requisição**: 1MB
- **Timeout**: 30 segundos

### **Recomendações**
- Implementar rate limiting em produção
- Adicionar autenticação/autorização
- Implementar logs de auditoria

---

## 🧪 **Exemplos de Uso**

### **Python (requests)**
```python
import requests

base_url = "http://localhost:8001/api/v1"

# Criar carteira
response = requests.post(f"{base_url}/carteiras/", json={
    "name": "Minha Carteira",
    "password": "senha12345"
})
wallet = response.json()

# Creditar saldo
requests.post(f"{base_url}/carteiras/{wallet['address']}/credit", json={
    "amount": 100.0,
    "reason": "Depósito inicial"
})

# Debitar saldo
requests.post(f"{base_url}/carteiras/{wallet['address']}/debit", json={
    "amount": 50.0,
    "reason": "Pagamento"
})
```

### **JavaScript (fetch)**
```javascript
const baseUrl = "http://localhost:8001/api/v1";

// Criar carteira
const createWallet = async () => {
  const response = await fetch(`${baseUrl}/carteiras/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: "Minha Carteira",
      password: "senha12345"
    })
  });
  return await response.json();
};

// Creditar saldo
const creditWallet = async (address, amount) => {
  const response = await fetch(`${baseUrl}/carteiras/${address}/credit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      amount: amount,
      reason: "Depósito"
    })
  });
  return await response.json();
};
```

### **cURL**
```bash
# Criar carteira
curl -X POST "http://localhost:8001/api/v1/carteiras/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Minha Carteira", "password": "senha12345"}'

# Creditar saldo
curl -X POST "http://localhost:8001/api/v1/carteiras/{address}/credit" \
  -H "Content-Type: application/json" \
  -d '{"amount": 100.0, "reason": "Depósito"}'
```

---

## 📚 **Documentação Interativa**

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **OpenAPI Schema**: http://localhost:8001/openapi.json

---

*API Reference atualizada em 27 de Outubro de 2024*
