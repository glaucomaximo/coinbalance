# 🌐 API Consciente CoinBalance

<div align="center">

![API](https://img.shields.io/badge/API-Conscious%20Fractal-FF6B6B?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-4ECDC4?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-2.1.0-00D4AA?style=for-the-badge)

**A API que Evolui, Aprende e se Adapta**

</div>

---

## 🌟 **Visão Geral**

A **API Consciente CoinBalance** representa uma revolução na forma como construímos interfaces de programação. Não é apenas uma API tradicional, mas um sistema vivo que evolui, aprende e se adapta às necessidades dos desenvolvedores e usuários.

### 🧠 **Características da API Consciente**

- **Adaptação Inteligente**: A API se adapta aos padrões de uso
- **Aprendizado Contínuo**: Melhoria constante baseada em feedback
- **Predição de Necessidades**: Antecipação de requisições futuras
- **Otimização Automática**: Otimização automática de performance
- **Consciência Contextual**: Respostas baseadas em contexto

---

## 🚀 **Início Rápido**

### **Base URL**

```
http://localhost:8001
```

### **Documentação Interativa**

- 📖 **Swagger UI**: http://localhost:8001/docs
- 📋 **ReDoc**: http://localhost:8001/redoc
- 🔍 **OpenAPI Schema**: http://localhost:8001/openapi.json

### **Autenticação**

```bash
# Obter token de acesso
curl -X POST "http://localhost:8001/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "password"}'

# Usar token nas requisições
curl -X GET "http://localhost:8001/wallets" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🏗️ **Arquitetura da API**

### **Estrutura de Endpoints**

```
┌─────────────────────────────────────────────────────────────┐
│                    🌐 API CONSCIOUS LAYER                   │
│                   (Adaptação Inteligente)                   │
├─────────────────────────────────────────────────────────────┤
│  🔐 AUTH  │  💰 WALLETS  │  📊 TRANSACTIONS  │  🧠 CONSCIOUS │
│  (Auth)   │  (Carteiras) │  (Transações)     │  (Sistemas)   │
├─────────────────────────────────────────────────────────────┤
│  🏗️ BLOCKCHAIN  │  ⚖️ CONSENSUS  │  🔍 MONITORING  │  🛡️ SECURITY │
│  (Blockchain)   │  (Consenso)     │  (Monitoramento) │  (Segurança) │
└─────────────────────────────────────────────────────────────┘
```

### **Camadas da API**

#### **1. Camada de Apresentação**
- **FastAPI**: Framework web moderno e rápido
- **Pydantic**: Validação de dados automática
- **Swagger/OpenAPI**: Documentação automática
- **CORS**: Suporte a requisições cross-origin

#### **2. Camada de Aplicação**
- **Use Cases**: Lógica de negócio isolada
- **Commands**: Operações que modificam estado
- **Queries**: Operações de consulta
- **Handlers**: Manipuladores de casos de uso

#### **3. Camada de Domínio**
- **Entities**: Entidades de negócio
- **Value Objects**: Objetos de valor
- **Services**: Serviços de domínio
- **Events**: Eventos de domínio

#### **4. Camada de Infraestrutura**
- **Repositories**: Acesso a dados
- **External Services**: Serviços externos
- **Database**: Persistência de dados
- **Monitoring**: Monitoramento e logs

---

## 🔐 **Autenticação e Autorização**

### **Endpoints de Autenticação**

#### **POST /auth/login**
```json
{
  "username": "string",
  "password": "string"
}
```

**Resposta:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "expires_in": 1800,
  "refresh_token": "string"
}
```

#### **POST /auth/refresh**
```json
{
  "refresh_token": "string"
}
```

#### **POST /auth/logout**
```json
{
  "access_token": "string"
}
```

### **Autorização por Escopo**

```python
# Exemplo de uso de escopos
@router.get("/wallets")
@require_scope("wallets:read")
async def get_wallets(current_user: AuthenticatedUser = Depends(get_current_user)):
    pass
```

**Escopos Disponíveis:**
- `wallets:read` - Leitura de carteiras
- `wallets:write` - Escrita de carteiras
- `transactions:read` - Leitura de transações
- `transactions:write` - Escrita de transações
- `blockchain:read` - Leitura da blockchain
- `admin:all` - Acesso administrativo completo

---

## 💰 **API de Carteiras**

### **Endpoints de Carteiras**

#### **GET /wallets**
Lista todas as carteiras do usuário autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Resposta:**
```json
{
  "wallets": [
    {
      "id": "wallet_123",
      "name": "Minha Carteira",
      "address": "CNB1abc...def",
      "balance": {
        "total": 1000.50,
        "available": 950.25,
        "locked": 50.25
      },
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20
}
```

#### **POST /wallets**
Cria uma nova carteira.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Body:**
```json
{
  "name": "Nova Carteira",
  "description": "Carteira para testes"
}
```

**Resposta:**
```json
{
  "id": "wallet_456",
  "name": "Nova Carteira",
  "address": "CNB2xyz...abc",
  "balance": {
    "total": 0.0,
    "available": 0.0,
    "locked": 0.0
  },
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "private_key": "encrypted_private_key"
}
```

#### **GET /wallets/{wallet_id}**
Obtém detalhes de uma carteira específica.

**Resposta:**
```json
{
  "id": "wallet_123",
  "name": "Minha Carteira",
  "address": "CNB1abc...def",
  "balance": {
    "total": 1000.50,
    "available": 950.25,
    "locked": 50.25
  },
  "transactions_count": 15,
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### **PUT /wallets/{wallet_id}**
Atualiza uma carteira existente.

**Body:**
```json
{
  "name": "Carteira Atualizada",
  "description": "Nova descrição"
}
```

#### **DELETE /wallets/{wallet_id}**
Desativa uma carteira (soft delete).

---

## 📊 **API de Transações**

### **Endpoints de Transações**

#### **GET /transactions**
Lista transações do usuário autenticado.

**Query Parameters:**
- `page`: Número da página (padrão: 1)
- `per_page`: Itens por página (padrão: 20)
- `status`: Filtro por status (`pending`, `confirmed`, `failed`)
- `type`: Filtro por tipo (`transfer`, `deposit`, `withdrawal`)
- `from_date`: Data inicial (ISO 8601)
- `to_date`: Data final (ISO 8601)

**Resposta:**
```json
{
  "transactions": [
    {
      "id": "tx_123",
      "type": "transfer",
      "status": "confirmed",
      "from_address": "CNB1abc...def",
      "to_address": "CNB2xyz...abc",
      "amount": 100.50,
      "fee": 0.10,
      "block_height": 12345,
      "created_at": "2024-01-01T00:00:00Z",
      "confirmed_at": "2024-01-01T00:01:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20
}
```

#### **POST /transactions/transfer**
Cria uma nova transação de transferência.

**Body:**
```json
{
  "from_wallet_id": "wallet_123",
  "to_address": "CNB2xyz...abc",
  "amount": 100.50,
  "memo": "Pagamento de serviços"
}
```

**Resposta:**
```json
{
  "id": "tx_456",
  "type": "transfer",
  "status": "pending",
  "from_address": "CNB1abc...def",
  "to_address": "CNB2xyz...abc",
  "amount": 100.50,
  "fee": 0.10,
  "memo": "Pagamento de serviços",
  "created_at": "2024-01-01T00:00:00Z",
  "estimated_confirmation": "2024-01-01T00:05:00Z"
}
```

#### **GET /transactions/{transaction_id}**
Obtém detalhes de uma transação específica.

**Resposta:**
```json
{
  "id": "tx_123",
  "type": "transfer",
  "status": "confirmed",
  "from_address": "CNB1abc...def",
  "to_address": "CNB2xyz...abc",
  "amount": 100.50,
  "fee": 0.10,
  "memo": "Pagamento de serviços",
  "block_height": 12345,
  "block_hash": "abc123...def456",
  "transaction_hash": "def456...ghi789",
  "created_at": "2024-01-01T00:00:00Z",
  "confirmed_at": "2024-01-01T00:01:00Z"
}
```

---

## 🏗️ **API de Blockchain**

### **Endpoints de Blockchain**

#### **GET /blockchain/status**
Obtém status atual da blockchain.

**Resposta:**
```json
{
  "height": 12345,
  "hash": "abc123...def456",
  "previous_hash": "def456...ghi789",
  "timestamp": "2024-01-01T00:00:00Z",
  "transactions_count": 150,
  "difficulty": 4,
  "nonce": 1234567890,
  "merkle_root": "ghi789...jkl012"
}
```

#### **GET /blockchain/blocks**
Lista blocos da blockchain.

**Query Parameters:**
- `page`: Número da página
- `per_page`: Itens por página
- `from_height`: Altura inicial
- `to_height`: Altura final

**Resposta:**
```json
{
  "blocks": [
    {
      "height": 12345,
      "hash": "abc123...def456",
      "previous_hash": "def456...ghi789",
      "timestamp": "2024-01-01T00:00:00Z",
      "transactions_count": 150,
      "difficulty": 4,
      "nonce": 1234567890,
      "merkle_root": "ghi789...jkl012"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20
}
```

#### **GET /blockchain/blocks/{height}**
Obtém detalhes de um bloco específico.

**Resposta:**
```json
{
  "height": 12345,
  "hash": "abc123...def456",
  "previous_hash": "def456...ghi789",
  "timestamp": "2024-01-01T00:00:00Z",
  "transactions_count": 150,
  "difficulty": 4,
  "nonce": 1234567890,
  "merkle_root": "ghi789...jkl012",
  "transactions": [
    {
      "id": "tx_123",
      "hash": "def456...ghi789",
      "from_address": "CNB1abc...def",
      "to_address": "CNB2xyz...abc",
      "amount": 100.50,
      "fee": 0.10
    }
  ]
}
```

---

## ⚖️ **API de Consenso**

### **Endpoints de Consenso**

#### **GET /consensus/validators**
Lista validadores ativos.

**Resposta:**
```json
{
  "validators": [
    {
      "id": "validator_123",
      "address": "CNB1validator...abc",
      "stake": 10000.0,
      "commission_rate": 0.05,
      "status": "active",
      "uptime": 99.5,
      "last_activity": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

#### **POST /consensus/register-validator**
Registra um novo validador.

**Body:**
```json
{
  "wallet_id": "wallet_123",
  "stake_amount": 1000.0,
  "commission_rate": 0.05
}
```

**Resposta:**
```json
{
  "validator_id": "validator_456",
  "address": "CNB1validator...xyz",
  "stake": 1000.0,
  "commission_rate": 0.05,
  "status": "pending",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### **POST /consensus/increase-stake**
Aumenta stake de um validador.

**Body:**
```json
{
  "validator_id": "validator_123",
  "additional_stake": 500.0
}
```

---

## 🧠 **API de Sistemas Conscientes**

### **Endpoints de Consciência**

#### **GET /conscious/status**
Obtém status dos sistemas conscientes.

**Resposta:**
```json
{
  "consciousness_level": 0.85,
  "active_systems": 13,
  "total_systems": 13,
  "learning_rate": 0.01,
  "adaptation_rate": 0.05,
  "prediction_accuracy": 0.92,
  "systems": {
    "monitoring": {
      "status": "active",
      "consciousness": 0.90,
      "anomaly_detection_accuracy": 0.95
    },
    "cache": {
      "status": "active",
      "consciousness": 0.80,
      "hit_rate": 0.85
    },
    "load_balancer": {
      "status": "active",
      "consciousness": 0.75,
      "distribution_efficiency": 0.90
    }
  }
}
```

#### **GET /conscious/metrics**
Obtém métricas detalhadas dos sistemas conscientes.

**Query Parameters:**
- `system`: Nome do sistema específico
- `metric`: Nome da métrica específica
- `time_range`: Período de tempo (`1h`, `24h`, `7d`, `30d`)

**Resposta:**
```json
{
  "metrics": {
    "consciousness_level": {
      "current": 0.85,
      "trend": "increasing",
      "history": [
        {"timestamp": "2024-01-01T00:00:00Z", "value": 0.80},
        {"timestamp": "2024-01-01T01:00:00Z", "value": 0.82}
      ]
    },
    "learning_rate": {
      "current": 0.01,
      "trend": "stable",
      "history": [
        {"timestamp": "2024-01-01T00:00:00Z", "value": 0.01},
        {"timestamp": "2024-01-01T01:00:00Z", "value": 0.01}
      ]
    }
  }
}
```

#### **POST /conscious/learn**
Força aprendizado dos sistemas conscientes.

**Body:**
```json
{
  "data": [
    {"metric": "cpu_usage", "value": 75.5, "timestamp": "2024-01-01T00:00:00Z"},
    {"metric": "memory_usage", "value": 60.2, "timestamp": "2024-01-01T00:00:00Z"}
  ],
  "context": {
    "user_id": "user_123",
    "action": "heavy_computation"
  }
}
```

#### **GET /conscious/predictions**
Obtém predições dos sistemas conscientes.

**Resposta:**
```json
{
  "predictions": [
    {
      "type": "load_spike",
      "confidence": 0.85,
      "predicted_time": "2024-01-01T02:00:00Z",
      "description": "Pico de carga previsto em 2 horas"
    },
    {
      "type": "failure_risk",
      "confidence": 0.70,
      "predicted_time": "2024-01-01T03:00:00Z",
      "description": "Risco de falha em sistema de cache"
    }
  ]
}
```

---

## 🔍 **API de Monitoramento**

### **Endpoints de Monitoramento**

#### **GET /monitoring/health**
Verifica saúde do sistema.

**Resposta:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "services": {
    "database": "healthy",
    "cache": "healthy",
    "blockchain": "healthy",
    "consensus": "healthy"
  },
  "metrics": {
    "cpu_usage": 45.2,
    "memory_usage": 60.8,
    "disk_usage": 25.5,
    "network_latency": 12.3
  }
}
```

#### **GET /monitoring/metrics**
Obtém métricas de sistema.

**Query Parameters:**
- `metric`: Nome da métrica
- `time_range`: Período de tempo
- `aggregation`: Tipo de agregação (`avg`, `max`, `min`, `sum`)

**Resposta:**
```json
{
  "metrics": {
    "cpu_usage": {
      "current": 45.2,
      "average": 42.1,
      "maximum": 78.5,
      "minimum": 25.3,
      "history": [
        {"timestamp": "2024-01-01T00:00:00Z", "value": 45.2},
        {"timestamp": "2024-01-01T00:01:00Z", "value": 44.8}
      ]
    }
  }
}
```

#### **GET /monitoring/alerts**
Lista alertas ativos.

**Resposta:**
```json
{
  "alerts": [
    {
      "id": "alert_123",
      "type": "high_cpu_usage",
      "severity": "warning",
      "message": "CPU usage above 80%",
      "timestamp": "2024-01-01T00:00:00Z",
      "status": "active"
    }
  ],
  "total": 1
}
```

---

## 🛡️ **API de Segurança**

### **Endpoints de Segurança**

#### **GET /security/events**
Lista eventos de segurança.

**Query Parameters:**
- `severity`: Filtro por severidade (`low`, `medium`, `high`, `critical`)
- `type`: Filtro por tipo de evento
- `time_range`: Período de tempo

**Resposta:**
```json
{
  "events": [
    {
      "id": "event_123",
      "type": "failed_login",
      "severity": "medium",
      "message": "Failed login attempt from IP 192.168.1.100",
      "timestamp": "2024-01-01T00:00:00Z",
      "ip_address": "192.168.1.100",
      "user_agent": "Mozilla/5.0..."
    }
  ],
  "total": 1
}
```

#### **POST /security/report-threat**
Reporta uma ameaça de segurança.

**Body:**
```json
{
  "type": "suspicious_activity",
  "description": "Multiple failed login attempts",
  "severity": "high",
  "ip_address": "192.168.1.100",
  "evidence": {
    "failed_attempts": 5,
    "time_window": "5 minutes"
  }
}
```

---

## 📊 **Códigos de Status HTTP**

### **Sucesso (2xx)**
- `200 OK` - Requisição bem-sucedida
- `201 Created` - Recurso criado com sucesso
- `202 Accepted` - Requisição aceita para processamento
- `204 No Content` - Requisição bem-sucedida sem conteúdo

### **Redirecionamento (3xx)**
- `301 Moved Permanently` - Recurso movido permanentemente
- `302 Found` - Recurso encontrado temporariamente

### **Erro do Cliente (4xx)**
- `400 Bad Request` - Requisição inválida
- `401 Unauthorized` - Não autorizado
- `403 Forbidden` - Acesso negado
- `404 Not Found` - Recurso não encontrado
- `409 Conflict` - Conflito de recursos
- `422 Unprocessable Entity` - Entidade não processável
- `429 Too Many Requests` - Muitas requisições

### **Erro do Servidor (5xx)**
- `500 Internal Server Error` - Erro interno do servidor
- `502 Bad Gateway` - Gateway inválido
- `503 Service Unavailable` - Serviço indisponível
- `504 Gateway Timeout` - Timeout do gateway

---

## 🔧 **Configuração e Personalização**

### **Variáveis de Ambiente**

```bash
# Configurações da API
API_HOST=0.0.0.0
API_PORT=8001
API_WORKERS=1
API_RELOAD=true
API_LOG_LEVEL=info

# Configurações de CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://localhost:8001
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_ALLOW_HEADERS=*

# Configurações de Segurança
JWT_SECRET_KEY=your-secure-jwt-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Configurações de Banco de Dados
DATABASE_URL=sqlite:///./blockchain.db
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Configurações de Cache
CACHE_SIZE=256MB
CACHE_TTL=3600
CACHE_DISTRIBUTION=auto

# Configurações de Monitoramento
MONITORING_ENABLED=true
METRICS_COLLECTION_INTERVAL=60
ALERT_THRESHOLD_CPU=80
ALERT_THRESHOLD_MEMORY=85
```

### **Configuração de Rate Limiting**

```python
# Configuração de rate limiting
RATE_LIMIT_CONFIG = {
    "default": "100/minute",
    "auth": "10/minute",
    "transactions": "50/minute",
    "monitoring": "200/minute"
}
```

### **Configuração de Logging**

```python
# Configuração de logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "logs/coinbalance.log",
            "formatter": "default"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "INFO"
        }
    }
}
```

---

## 🧪 **Testes da API**

### **Testes Unitários**

```python
# Exemplo de teste unitário
def test_create_wallet():
    response = client.post("/wallets", json={
        "name": "Test Wallet",
        "description": "Test wallet for unit tests"
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Test Wallet"
```

### **Testes de Integração**

```python
# Exemplo de teste de integração
def test_transfer_transaction():
    # Criar carteiras
    wallet1 = create_wallet("Wallet 1")
    wallet2 = create_wallet("Wallet 2")
    
    # Fazer transferência
    response = client.post("/transactions/transfer", json={
        "from_wallet_id": wallet1["id"],
        "to_address": wallet2["address"],
        "amount": 100.0
    })
    
    assert response.status_code == 201
    assert response.json()["status"] == "pending"
```

### **Testes de Performance**

```python
# Exemplo de teste de performance
def test_api_performance():
    start_time = time.time()
    
    # Executar 1000 requisições
    for i in range(1000):
        response = client.get("/wallets")
        assert response.status_code == 200
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Verificar que 1000 requisições foram processadas em menos de 10 segundos
    assert duration < 10.0
    assert duration / 1000 < 0.01  # Menos de 10ms por requisição
```

---

## 📈 **Monitoramento e Observabilidade**

### **Métricas da API**

- **Request Rate**: Taxa de requisições por segundo
- **Response Time**: Tempo de resposta médio
- **Error Rate**: Taxa de erros
- **Active Connections**: Conexões ativas
- **Memory Usage**: Uso de memória
- **CPU Usage**: Uso de CPU

### **Dashboards**

- **API Performance**: Performance geral da API
- **Error Analysis**: Análise de erros
- **User Activity**: Atividade dos usuários
- **System Health**: Saúde do sistema

### **Alertas**

- **High Error Rate**: Taxa de erro alta
- **Slow Response Time**: Tempo de resposta lento
- **High Memory Usage**: Uso alto de memória
- **Failed Authentication**: Falhas de autenticação

---

## 🔮 **Futuro da API**

### **Evolução Planejada**

1. **API Adaptativa**: API que se adapta aos padrões de uso
2. **Predição de Requisições**: Antecipação de requisições futuras
3. **Otimização Automática**: Otimização automática de endpoints
4. **IA Generativa**: Geração automática de documentação

### **Recursos Futuros**

- **GraphQL Support**: Suporte a GraphQL
- **WebSocket Support**: Suporte a WebSockets
- **gRPC Support**: Suporte a gRPC
- **API Versioning**: Versionamento automático de API

---

## 🏆 **Benefícios da API Consciente**

### **Técnicos**
- ✅ **Adaptação Inteligente**: Adaptação aos padrões de uso
- ✅ **Performance Otimizada**: Performance otimizada automaticamente
- ✅ **Documentação Viva**: Documentação que evolui com a API
- ✅ **Monitoramento Avançado**: Monitoramento inteligente

### **Estratégicos**
- ✅ **Developer Experience**: Experiência superior para desenvolvedores
- ✅ **Reduced Maintenance**: Redução de manutenção
- ✅ **Faster Development**: Desenvolvimento mais rápido
- ✅ **Better Reliability**: Maior confiabilidade

---

<div align="center">

**🌐 API Consciente CoinBalance - Onde a Interface Encontra a Inteligência**

![API](https://img.shields.io/badge/API-Adaptive-FF6B6B?style=for-the-badge)
![Intelligence](https://img.shields.io/badge/Intelligence-Emergent-4ECDC4?style=for-the-badge)
![Performance](https://img.shields.io/badge/Performance-Optimized-00D4AA?style=for-the-badge)

</div>