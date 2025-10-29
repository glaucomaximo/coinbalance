# 🗺️ DOC-ENG_07_MAPA_ARQUITETURA_ATUAL
## Mapa de Arquitetura Atual - Engenharia Reversa

**Versão:** 1.0  
**Data de Criação:** 29 de outubro de 2025  
**Última Atualização:** 29 de outubro de 2025  
**Autor:** Engenharia de Documentação Sênior  
**Status:** ✅ **COMPLETO**

---

## 📋 Sumário Executivo

Este documento apresenta o mapa completo da arquitetura atual do sistema CoinBalance, obtido através de engenharia reversa do código-fonte. Inclui diagramas C4 detalhados, fluxos principais e mapeamento de componentes.

---

## 🏗️ Arquitetura de Alto Nível

### **Camadas Arquiteturais**

```mermaid
graph TB
    subgraph "Presentation Layer"
        API[FastAPI REST API]
        ROUTERS[27 Routers]
    end
    
    subgraph "Application Layer"
        COMMANDS[Commands]
        QUERIES[Queries]
        USECASES[Use Cases]
    end
    
    subgraph "Domain Layer"
        ENTITIES[Entities]
        VALUES[Value Objects]
        SERVICES[Domain Services]
        EVENTS[Domain Events]
    end
    
    subgraph "Infrastructure Layer"
        REPOS[Repositories]
        SECURITY[Security]
        MONITORING[Monitoring]
        WEB3[Web3 Clients]
        AI[ML Engine]
    end
    
    API --> COMMANDS
    API --> QUERIES
    COMMANDS --> ENTITIES
    QUERIES --> ENTITIES
    ENTITIES --> SERVICES
    SERVICES --> REPOS
    SERVICES --> WEB3
    SERVICES --> AI
    REPOS --> SECURITY
    ENTITIES --> EVENTS
```

---

## 📦 Componentes Principais por Camada

### **Presentation Layer (27 Routers)**

| Router | Endpoints | Propósito |
|--------|-----------|-----------|
| `wallet_router` | 2 | Gerenciamento de carteiras |
| `blockchain_router` | 5+ | Operações blockchain |
| `transaction_router` | 4+ | Transações |
| `consensus_router` | 5+ | Consenso distribuído |
| `web3_router` | 8+ | Integração Web3 |
| `monitoring_router` | 6+ | Monitoramento |
| `auth_router` | 3 | Autenticação |
| `security_router` | 4+ | Segurança |
| `ai_advanced_router` | 15+ | IA avançada |
| `web3_advanced_router` | 20+ | Web3 avançado |
| `lgpd_router` | 8 | Conformidade LGPD |
| Outros | 50+ | Funcionalidades diversas |

**Total de Endpoints Identificados:** ~250+ endpoints REST

---

### **Application Layer**

#### **Commands (CQRS)**

```python
# Wallet Commands
CreateWalletCommand
UpdateWalletCommand

# Transaction Commands
CreateTransferCommand
CreateTransactionCommand

# Consensus Commands
RegisterValidatorCommand
StakeCommand
```

#### **Queries (CQRS)**

```python
# Wallet Queries
GetWalletQuery
ListWalletsQuery

# Transaction Queries
GetTransactionQuery
ListTransactionsQuery
GetTransactionHistoryQuery

# Blockchain Queries
GetBlockchainStatsQuery
GetBlockQuery
ListBlocksQuery
```

---

### **Domain Layer**

#### **Aggregate Roots**

```mermaid
classDiagram
    class Blockchain {
        +blocks: List[Block]
        +mine_block()
        +validate_chain()
        +add_transaction()
    }
    
    class Block {
        +height: int
        +hash: HashValue
        +transactions: List[Transaction]
        +mine()
        +validate()
    }
    
    class Transaction {
        +id: str
        +from_address: WalletAddress
        +to_address: WalletAddress
        +amount: Money
        +validate()
    }
    
    class Wallet {
        +address: WalletAddress
        +balance: Money
        +credit()
        +debit()
    }
    
    class Validator {
        +address: WalletAddress
        +stake: Money
        +vote()
    }
    
    Blockchain "1" --> "*" Block
    Block "1" --> "*" Transaction
    Transaction --> Wallet
```

---

### **Infrastructure Layer**

#### **Repositories**

```python
# Implementações
SQLiteWalletRepository
SQLiteTransactionRepository
SQLiteBlockRepository
SQLiteValidatorRepository
```

#### **Serviços de Infraestrutura**

| Serviço | Localização | Propósito |
|---------|------------|-----------|
| **MiningService** | `domain/blockchain/services/` | Mineração paralela |
| **ConsensusService** | `domain/consensus/services/` | Consenso distribuído |
| **Web3Service** | `infrastructure/web3/` | Integração Web3 |
| **MLService** | `infrastructure/ai/` | Machine Learning |
| **SecurityService** | `infrastructure/security/` | Segurança |
| **MonitoringService** | `infrastructure/monitoring/` | Monitoramento |

---

## 🔄 Fluxos Principais

### **Fluxo de Criação de Transação**

```mermaid
sequenceDiagram
    participant U as Usuário
    participant API as API REST
    participant CMD as CreateTransactionCommand
    participant TX as Transaction Entity
    participant VAL as Validator
    participant BC as Blockchain
    participant REPO as Repository
    
    U->>API: POST /api/v1/transactions
    API->>CMD: execute(data)
    CMD->>TX: Transaction.create()
    TX->>TX: validate()
    TX->>VAL: check_balance()
    VAL-->>TX: balance_ok
    CMD->>BC: add_transaction()
    BC->>BC: validate_transaction()
    BC->>REPO: save(transaction)
    REPO-->>BC: saved
    BC-->>CMD: transaction_id
    CMD-->>API: response
    API-->>U: 201 Created
```

---

### **Fluxo de Mineração**

```mermaid
sequenceDiagram
    participant API as API REST
    participant CMD as MineBlockCommand
    participant BC as Blockchain
    participant MS as MiningService
    participant PM as ParallelMiner
    participant BLOCK as Block
    participant REPO as Repository
    
    API->>CMD: execute(miner_address)
    CMD->>BC: mine_block(transactions)
    BC->>MS: mine_block()
    MS->>PM: mine_parallel(16 threads)
    PM->>PM: calculate_hash()
    PM-->>MS: hash_found
    MS->>BLOCK: Block.create(hash, nonce)
    BLOCK->>BLOCK: validate()
    BC->>BC: validate_block()
    BC->>REPO: save(block)
    REPO-->>BC: saved
    BC-->>CMD: block
    CMD-->>API: response
```

---

## 📊 Mapeamento de Dependências

### **Dependências Principais**

```mermaid
graph LR
    A[FastAPI] --> B[Domain]
    A --> C[Application]
    C --> B
    C --> D[Infrastructure]
    B --> D
    D --> E[SQLite]
    D --> F[Web3]
    D --> G[ML]
    D --> H[Security]
```

---

## ✅ Histórico de Versões

| Versão | Data | Alterações | Autor |
|--------|------|------------|-------|
| 1.0 | 29/10/2025 | Criação do mapa de arquitetura atual | Eng. Documentação Sênior |

---

**Status:** ✅ **FASE 3 COMPLETA - MAPA DE ARQUITETURA CRIADO**

