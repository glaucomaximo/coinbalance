# CoinBalance API Documentation

## 🚀 Visão Geral

A API do CoinBalance é um sistema de carteira digital robusto construído com FastAPI, oferecendo endpoints seguros e bem documentados para gerenciamento de carteiras, transferências e autenticação.

### Base URL
```
http://localhost:8001
```

### Autenticação
A API utiliza JWT (JSON Web Tokens) para autenticação. Inclua o token no header:
```
Authorization: Bearer <seu_token>
```

## 📋 Endpoints da API

### 🔐 Autenticação

#### POST /api/v1/auth/register
Registrar um novo usuário.

**Request Body:**
```json
{
  "username": "usuario123",
  "email": "usuario@email.com",
  "password": "senha123456"
}
```

**Response (201):**
```json
{
  "message": "Usuário registrado com sucesso",
  "user_id": "uuid-do-usuario"
}
```

#### POST /api/v1/auth/login
Fazer login e obter token JWT.

**Request Body:**
```json
{
  "username": "usuario123",
  "password": "senha123456"
}
```

**Response (200):**
```json
{
  "access_token": "jwt-token-aqui",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### GET /api/v1/auth/me
Obter informações do usuário autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "user_id": "uuid-do-usuario",
  "username": "usuario123",
  "email": "usuario@email.com"
}
```

### 💰 Carteiras

#### POST /api/v1/carteiras/
Criar uma nova carteira.

**Request Body:**
```json
{
  "name": "Minha Carteira",
  "password": "senha123456"
}
```

**Response (201):**
```json
{
  "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
  "public_key": "04a1b2c3d4e5f6...",
  "balance": 0.0,
  "created_at": "2024-10-27T10:30:00Z"
}
```

#### GET /api/v1/carteiras/{address}
Obter informações de uma carteira específica.

**Path Parameters:**
- `address` (string): Endereço da carteira

**Response (200):**
```json
{
  "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
  "public_key": "04a1b2c3d4e5f6...",
  "balance_cnb": 100.0,
  "balance_satoshi": 10000000000,
  "created_at": "2024-10-27T10:30:00Z"
}
```

#### GET /api/v1/carteiras/
Listar todas as carteiras.

**Response (200):**
```json
{
  "wallets": [
    {
      "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
      "public_key": "04a1b2c3d4e5f6...",
      "balance_cnb": 100.0,
      "balance_satoshi": 10000000000,
      "created_at": "2024-10-27T10:30:00Z"
    }
  ],
  "total": 1
}
```

#### POST /api/v1/carteiras/{address}/creditar
Creditar saldo em uma carteira.

**Path Parameters:**
- `address` (string): Endereço da carteira

**Request Body:**
```json
{
  "amount": 50.0,
  "description": "Depósito inicial"
}
```

**Response (200):**
```json
{
  "message": "Saldo creditado com sucesso",
  "new_balance": 150.0
}
```

#### POST /api/v1/carteiras/{address}/debitar
Debitar saldo de uma carteira.

**Path Parameters:**
- `address` (string): Endereço da carteira

**Request Body:**
```json
{
  "amount": 25.0,
  "description": "Pagamento de serviço"
}
```

**Response (200):**
```json
{
  "message": "Saldo debitado com sucesso",
  "new_balance": 125.0
}
```

### 🔄 Transferências

#### POST /api/v1/transferencias/
Realizar transferência entre carteiras.

**Request Body:**
```json
{
  "from_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
  "to_address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
  "amount": 10.0,
  "description": "Transferência entre carteiras"
}
```

**Response (200):**
```json
{
  "transaction_id": "uuid-da-transacao",
  "from_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
  "to_address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
  "amount": 10.0,
  "status": "completed",
  "timestamp": "2024-10-27T10:30:00Z"
}
```

### 📊 Histórico de Transações

#### GET /api/v1/transacoes/historico
Obter histórico de transações.

**Query Parameters:**
- `address` (string, opcional): Filtrar por endereço específico
- `limit` (integer, opcional): Limite de resultados (padrão: 50)
- `offset` (integer, opcional): Offset para paginação (padrão: 0)

**Response (200):**
```json
{
  "transactions": [
    {
      "transaction_id": "uuid-da-transacao",
      "from_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
      "to_address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
      "amount": 10.0,
      "status": "completed",
      "timestamp": "2024-10-27T10:30:00Z"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

### 🔍 Monitoramento

#### GET /api/v1/health
Health check da API.

**Response (200):**
```json
{
  "status": "healthy",
  "timestamp": "2024-10-27T10:30:00Z",
  "version": "2.1.1"
}
```

#### GET /api/v1/monitoring/dashboard
Dashboard de monitoramento do sistema.

**Response (200):**
```json
{
  "system_info": {
    "cpu_percent": 15.2,
    "memory_percent": 45.8,
    "disk_percent": 23.1
  },
  "api_stats": {
    "total_requests": 1250,
    "successful_requests": 1200,
    "failed_requests": 50,
    "average_response_time": 0.15
  },
  "database_stats": {
    "total_wallets": 150,
    "total_transactions": 500,
    "database_size_mb": 2.5
  }
}
```

#### GET /api/v1/monitoring/metrics
Métricas detalhadas do sistema.

**Response (200):**
```json
{
  "performance": {
    "cpu_usage": 15.2,
    "memory_usage": 45.8,
    "disk_usage": 23.1
  },
  "api_metrics": {
    "requests_per_minute": 25,
    "average_response_time": 0.15,
    "error_rate": 0.04
  },
  "business_metrics": {
    "active_wallets": 150,
    "total_transactions": 500,
    "total_volume": 10000.0
  }
}
```

## 🚨 Códigos de Erro

### 400 Bad Request
```json
{
  "detail": {
    "error": "Dados inválidos fornecidos",
    "code": "INVALID_DATA"
  }
}
```

### 401 Unauthorized
```json
{
  "detail": {
    "error": "Token de autenticação inválido",
    "code": "INVALID_TOKEN"
  }
}
```

### 404 Not Found
```json
{
  "detail": {
    "error": "Carteira não encontrada",
    "code": "WALLET_NOT_FOUND"
  }
}
```

### 409 Conflict
```json
{
  "detail": {
    "error": "Nome de carteira já existe",
    "code": "WALLET_NAME_EXISTS"
  }
}
```

### 422 Unprocessable Content
```json
{
  "detail": [
    {
      "field": "amount",
      "message": "Valor deve ser positivo",
      "type": "value_error"
    }
  ]
}
```

### 429 Too Many Requests
```json
{
  "detail": {
    "error": "Muitas requisições. Tente novamente em alguns minutos",
    "code": "RATE_LIMIT_EXCEEDED"
  }
}
```

### 500 Internal Server Error
```json
{
  "detail": {
    "error": "Erro interno do servidor",
    "code": "INTERNAL_ERROR"
  }
}
```

## 🔧 Exemplos de Uso

### Criar Carteira e Fazer Transferência

```bash
# 1. Criar carteira
curl -X POST "http://localhost:8001/api/v1/carteiras/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Minha Carteira",
    "password": "senha123456"
  }'

# 2. Creditar saldo
curl -X POST "http://localhost:8001/api/v1/carteiras/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa/creditar" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100.0,
    "description": "Depósito inicial"
  }'

# 3. Fazer transferência
curl -X POST "http://localhost:8001/api/v1/transferencias/" \
  -H "Content-Type: application/json" \
  -d '{
    "from_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "to_address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
    "amount": 10.0,
    "description": "Transferência entre carteiras"
  }'
```

### Autenticação e Acesso Protegido

```bash
# 1. Registrar usuário
curl -X POST "http://localhost:8001/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario123",
    "email": "usuario@email.com",
    "password": "senha123456"
  }'

# 2. Fazer login
curl -X POST "http://localhost:8001/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario123",
    "password": "senha123456"
  }'

# 3. Usar token para acessar endpoint protegido
curl -X GET "http://localhost:8001/api/v1/auth/me" \
  -H "Authorization: Bearer <seu_token_aqui>"
```

## 📚 Recursos Adicionais

### Documentação Interativa
- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc

### Rate Limiting
- **Limite padrão:** 100 requisições por minuto
- **Burst limit:** 50 requisições simultâneas
- **Headers de resposta:**
  ```
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1640995200
  ```

### Logs Estruturados
Todos os logs são gerados em formato JSON para facilitar análise:
```json
{
  "timestamp": "2024-10-27T10:30:00Z",
  "level": "INFO",
  "message": "Carteira criada com sucesso",
  "wallet_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
  "user_id": "uuid-do-usuario"
}
```

## 🚀 Próximos Passos

1. **Implementar cache** para melhorar performance
2. **Adicionar mais endpoints** de relatórios
3. **Implementar webhooks** para notificações
4. **Adicionar suporte** a múltiplas moedas

---

**📞 Suporte:** Para dúvidas sobre a API, consulte a documentação interativa em `/docs` ou abra uma issue no repositório.