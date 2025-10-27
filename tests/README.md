"""
Estratégia de Testes para CoinBalance - Arquitetura DDD

Esta estratégia segue os princípios de engenharia de software e padrões de teste
para arquitetura Domain-Driven Design (DDD) com Clean Architecture.

PIRÂMIDE DE TESTES:
1. Testes Unitários (Base) - Domain Layer
2. Testes de Integração (Meio) - Application Layer  
3. Testes End-to-End (Topo) - Presentation Layer
4. Testes de Performance (Específicos)

PADRÕES UTILIZADOS:
- AAA Pattern (Arrange, Act, Assert)
- Given-When-Then (BDD)
- Test Doubles (Mocks, Stubs, Fakes)
- Test Data Builders
- Page Object Model (para E2E)
- Test Containers (para integração)

ESTRUTURA DE DIRETÓRIOS:
tests/
├── unit/                    # Testes unitários
│   ├── domain/              # Domain layer tests
│   │   ├── entities/        # Entity tests
│   │   ├── value_objects/   # Value object tests
│   │   ├── services/        # Domain service tests
│   │   └── events/          # Domain event tests
│   └── shared/              # Shared domain tests
├── integration/              # Testes de integração
│   ├── application/         # Application layer tests
│   │   ├── commands/        # Command handler tests
│   │   ├── queries/         # Query handler tests
│   │   └── services/        # Application service tests
│   ├── infrastructure/     # Infrastructure layer tests
│   │   ├── repositories/    # Repository implementation tests
│   │   ├── external/        # External service tests
│   │   └── persistence/     # Database tests
│   └── shared/              # Shared integration tests
├── e2e/                     # Testes end-to-end
│   ├── api/                 # API endpoint tests
│   ├── workflows/           # Business workflow tests
│   └── scenarios/           # User scenario tests
├── performance/             # Testes de performance
│   ├── load/                # Load tests
│   ├── stress/               # Stress tests
│   └── benchmarks/           # Benchmark tests
├── fixtures/                # Test fixtures e dados
├── helpers/                  # Test helpers e utilities
└── conftest.py              # Pytest configuration

FERRAMENTAS:
- pytest: Framework principal
- pytest-asyncio: Para testes assíncronos
- pytest-mock: Para mocks
- pytest-cov: Para cobertura
- factory-boy: Para factories de dados
- httpx: Para testes de API
- testcontainers: Para containers de teste

MÉTRICAS DE QUALIDADE:
- Cobertura de código: >90%
- Testes unitários: >70% dos testes
- Testes de integração: 20-25% dos testes
- Testes E2E: 5-10% dos testes
- Tempo de execução: <5min para suite completa
"""
