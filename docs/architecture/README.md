# 🏗️ Arquitetura do Sistema CoinBalance

## 📋 **Visão Geral**

O CoinBalance implementa uma arquitetura **Domain-Driven Design (DDD)** com **Clean Architecture**, garantindo separação clara de responsabilidades e alta testabilidade.

---

## 🏛️ **Arquitetura em Camadas**

### **1. Domain Layer** (Domínio)
**Localização**: `src/domain/`

**Responsabilidades**:
- Lógica de negócio central
- Entidades e Value Objects
- Regras de domínio
- Eventos de domínio

**Componentes**:
```
domain/
├── wallet/                    # Domínio de carteiras
│   ├── entities/             # Wallet
│   ├── value_objects/        # Address, PrivateKey, PublicKey, Balance
│   ├── events/               # WalletCreated, WalletCredited, WalletDebited
│   └── repositories/          # WalletRepository (interface)
├── consensus/                # Domínio de consenso
│   ├── entities/             # Validator
│   ├── value_objects/        # ValidatorId, StakeAmount, ConsensusRound
│   ├── events/               # ValidatorRegistered, StakeIncreased
│   └── services/             # ConsensusService, MonetaryPolicyService
├── transaction/              # Domínio de transações
└── shared/                   # Componentes compartilhados
    ├── value_objects/        # Money, Timestamp
    ├── domain_events/        # Base, Dispatcher
    └── exceptions.py         # Exceções de domínio
```

### **2. Application Layer** (Aplicação)
**Localização**: `src/application/`

**Responsabilidades**:
- Casos de uso
- Orquestração de domínio
- DTOs e Commands/Queries
- Handlers de eventos

**Componentes**:
```
application/
├── wallet/
│   ├── commands/             # CreateWalletCommand, CreateWalletCommandHandler
│   └── queries/              # GetWalletQuery, GetWalletHandler
├── consensus/
│   ├── commands/             # RegisterValidatorCommand, IncreaseStakeCommand
│   └── dto/                  # ConsensusDTO
├── transaction/
│   ├── commands/             # CreateTransferCommand
│   └── queries/              # GetTransactionQuery
└── common/
    └── interfaces/           # UseCase interface
```

### **3. Infrastructure Layer** (Infraestrutura)
**Localização**: `src/infrastructure/`

**Responsabilidades**:
- Persistência de dados
- Integração com sistemas externos
- Configuração
- Injeção de dependências

**Componentes**:
```
infrastructure/
├── persistence/
│   ├── database_manager.py   # Gerenciamento do SQLite
│   └── repositories/         # Implementações concretas
├── di/
│   └── container.py          # Container de DI
├── config/
│   └── settings.py          # Configurações
├── security/                # Módulos de segurança
└── monitoring/              # Monitoramento
```

### **4. Presentation Layer** (Apresentação)
**Localização**: `src/presentation/`

**Responsabilidades**:
- Interface da API
- Validação de entrada
- Serialização de saída
- Roteamento

**Componentes**:
```
presentation/
├── api/
│   ├── app.py               # Aplicação FastAPI
│   ├── dependencies.py      # Dependências
│   └── routers/             # Routers da API
├── schemas/                 # Schemas Pydantic
└── middleware/             # Middlewares customizados
```

---

## 🔄 **Fluxo de Dados**

### **Criação de Carteira**
```
1. Client → POST /api/v1/carteiras/
2. Presentation → Validação (Pydantic)
3. Application → CreateWalletCommand
4. Domain → Wallet.create()
5. Infrastructure → Persistência (SQLite)
6. Domain → Eventos (WalletCreated)
7. Presentation → Resposta JSON
```

### **Operação de Crédito**
```
1. Client → POST /api/v1/carteiras/{address}/credit
2. Presentation → Validação
3. Application → Busca carteira
4. Domain → wallet.credit()
5. Infrastructure → Atualização
6. Domain → Eventos (WalletCredited)
7. Presentation → Resposta atualizada
```

---

## 🎯 **Padrões de Design**

### **Domain-Driven Design (DDD)**
- **Entities**: Objetos com identidade única
- **Value Objects**: Objetos imutáveis sem identidade
- **Aggregates**: Conjuntos de entidades relacionadas
- **Domain Events**: Eventos que ocorrem no domínio
- **Repositories**: Abstração de persistência

### **Clean Architecture**
- **Independência de frameworks**
- **Testabilidade**
- **Independência de UI**
- **Independência de banco de dados**
- **Independência de agentes externos**

### **CQRS (Command Query Responsibility Segregation)**
- **Commands**: Operações de escrita
- **Queries**: Operações de leitura
- **Handlers**: Processamento de commands/queries

---

## 🔧 **Tecnologias e Ferramentas**

### **Backend**
- **Python 3.13.4**: Linguagem principal
- **FastAPI**: Framework web moderno
- **Pydantic**: Validação e serialização
- **SQLite**: Banco de dados
- **Pytest**: Framework de testes

### **Arquitetura**
- **Dependency Injection**: Container customizado
- **Event Sourcing**: Eventos de domínio
- **Repository Pattern**: Abstração de persistência
- **Factory Pattern**: Criação de objetos

---

## 📊 **Métricas Arquiteturais**

### **Acoplamento**
- **Baixo**: Camadas bem separadas
- **Injeção de dependências**: Desacoplamento
- **Interfaces**: Abstrações claras

### **Coesão**
- **Alta**: Responsabilidades bem definidas
- **Single Responsibility**: Cada classe tem uma responsabilidade
- **Domain Focus**: Foco no domínio de negócio

### **Testabilidade**
- **Unit Tests**: 64 testes
- **Integration Tests**: 8 testes
- **E2E Tests**: 15 testes
- **Performance Tests**: 8 testes

---

## 🚀 **Benefícios da Arquitetura**

### **Manutenibilidade**
- Código organizado e legível
- Separação clara de responsabilidades
- Fácil localização de funcionalidades

### **Testabilidade**
- Testes isolados por camada
- Mocks e stubs facilitados
- Cobertura abrangente

### **Escalabilidade**
- Adição de novas funcionalidades
- Modificação sem impacto
- Extensibilidade

### **Qualidade**
- Código limpo e bem estruturado
- Padrões estabelecidos
- Documentação clara

---

## 🔮 **Evolução da Arquitetura**

### **Próximas Implementações**
- **Event Sourcing**: Histórico completo de eventos
- **CQRS Avançado**: Separar read/write models
- **Microservices**: Decomposição em serviços
- **Event-Driven**: Comunicação assíncrona

### **Melhorias Planejadas**
- **Caching**: Redis para performance
- **Message Queue**: RabbitMQ/Kafka
- **API Gateway**: Kong/Traefik
- **Monitoring**: Prometheus/Grafana

---

*Documentação arquitetural atualizada em 27 de Outubro de 2024*
