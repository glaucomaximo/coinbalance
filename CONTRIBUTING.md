# 🤝 Guia de Contribuição - CoinBalance

## 📋 **VISÃO GERAL**

Este documento estabelece os padrões de desenvolvimento e contribuição para o projeto CoinBalance, garantindo qualidade, consistência e manutenibilidade do código.

---

## 🎯 **PRINCÍPIOS FUNDAMENTAIS**

### **1. Qualidade de Código**
- ✅ **SOLID Principles** rigorosamente aplicados
- ✅ **Clean Code** em todas as implementações
- ✅ **Testes automatizados** obrigatórios
- ✅ **Documentação clara** e precisa

### **2. Arquitetura**
- ✅ **Domain-Driven Design (DDD)**
- ✅ **Clean Architecture**
- ✅ **Hexagonal Architecture (Ports & Adapters)**
- ✅ **CQRS Pattern**

### **3. Segurança**
- ✅ **OWASP Top 10** compliance
- ✅ **Validação rigorosa** de entrada
- ✅ **Princípio do menor privilégio**
- ✅ **Logging seguro**

---

## 🛠️ **CONFIGURAÇÃO DO AMBIENTE**

### **Pré-requisitos**
```bash
# Python 3.10+
python --version

# Git
git --version

# Docker (opcional)
docker --version
```

## 🛠️ **CONFIGURAÇÃO DO AMBIENTE**

### **Pré-requisitos**
```bash
# Python 3.10+
python --version

# Git
git --version

# Docker (opcional)
docker --version
```

### **Instalação**
```bash
# 1. Clonar repositório
git clone https://github.com/coinbalance/coinbalance.git
cd coinbalance

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Instalar ferramentas de qualidade
pip install black isort flake8 mypy bandit coverage

# 4. Instalar pre-commit hooks
pre-commit install

# 5. Verificar qualidade do projeto
./scripts/quality-check.sh  # Linux/Mac
# ou
./scripts/quality-check.ps1  # Windows

# 6. Verificar instalação
python main.py --help
```

### **Estrutura do Projeto**
```
coinbalance/
├── src/                          # 🏗️ Código fonte principal
│   ├── domain/                   # 💎 Camada de Domínio (DDD)
│   ├── application/              # 🎯 Camada de Aplicação (CQRS)
│   ├── infrastructure/           # 🔧 Camada de Infraestrutura
│   └── presentation/              # 🌐 Camada de Apresentação
├── tests/                        # 🧪 Testes automatizados
├── docs/                         # 📚 Documentação
├── scripts/                      # 🔧 Scripts utilitários
├── .github/workflows/            # 🚀 CI/CD Pipeline
├── pyproject.toml               # ⚙️ Configurações de qualidade
├── .pre-commit-config.yaml      # 🔍 Pre-commit hooks
└── requirements.txt              # 📦 Dependências
```

---

## ⚠️ **PROTOCOLO OBRIGATÓRIO DE MANUTENÇÃO**

### **🚨 REGRA FUNDAMENTAL**
> **NENHUMA MANUTENÇÃO PODE SER INICIADA SEM COMPLETAR 100% DO PROTOCOLO**

### **📋 Processo Obrigatório**
Antes de qualquer manutenção, consulte **OBRIGATORIAMENTE**:

1. **[docs/PROTOCOLO_MANUTENCAO.md](docs/PROTOCOLO_MANUTENCAO.md)** - Processo completo de 6 fases
2. **[docs/SISTEMA_ORGANIZACIONAL.md](docs/SISTEMA_ORGANIZACIONAL.md)** - Sistema de qualidade
3. **[docs/ARQUITETURA_DETALHADA.md](docs/ARQUITETURA_DETALHADA.md)** - Arquitetura técnica
4. **[docs/DECISOES_ARQUITETURAIS.md](docs/DECISOES_ARQUITETURAIS.md)** - ADRs

### **🔍 Scripts de Verificação**
```bash
# Verificação completa de qualidade
./scripts/quality-check.sh  # Linux/Mac
./scripts/quality-check.ps1  # Windows

# Verificação arquitetural específica
python scripts/check_architecture.py

# Validação de mudanças
python scripts/validate_change.py

# Geração de relatórios
python scripts/generate_reports.py
```

### **🚨 Gates de Bloqueio**
- ❌ **Documentação** não consultada → BLOQUEIA
- ❌ **Qualidade** insuficiente → BLOQUEIA
- ❌ **Arquitetura** não conforme → BLOQUEIA
- ❌ **Segurança** comprometida → BLOQUEIA

---

## 📝 **PADRÕES DE CÓDIGO**

### **1. Formatação**
```bash
# Formatação automática com Black
black .

# Organização de imports com isort
isort .

# Verificação de formatação
black --check .
isort --check-only .
```

### **2. Linting**
```bash
# Verificação de qualidade com Flake8
flake8 .

# Verificação de tipos com MyPy
mypy src/

# Verificação de segurança com Bandit
bandit -r src/
```

### **3. Convenções de Nomenclatura**

#### **Classes e Interfaces**
```python
# ✅ CORRETO
class WalletRepository(ABC):
    pass

class CreateWalletCommand:
    pass

# ❌ INCORRETO
class wallet_repository:
    pass
```

#### **Funções e Métodos**
```python
# ✅ CORRETO
def create_wallet(name: str) -> Wallet:
    pass

async def find_by_address(address: str) -> Optional[Wallet]:
    pass

# ❌ INCORRETO
def CreateWallet(name: str):
    pass
```

#### **Constantes**
```python
# ✅ CORRETO
MAX_WALLET_BALANCE = 1000000
DEFAULT_CURRENCY = "CNB"

# ❌ INCORRETO
maxWalletBalance = 1000000
```

### **4. Documentação**

#### **Docstrings**
```python
def create_wallet(name: str, password: Optional[str] = None) -> Wallet:
    """
    Cria uma nova carteira com nome e senha opcional.
    
    Args:
        name: Nome da carteira (obrigatório)
        password: Senha para proteção (opcional)
        
    Returns:
        Wallet: Nova instância de carteira
        
    Raises:
        ValidationError: Se o nome for inválido
        DuplicateEntityError: Se já existir carteira com mesmo nome
        
    Example:
        >>> wallet = create_wallet("Minha Carteira", "senha123")
        >>> print(wallet.name)
        Minha Carteira
    """
    pass
```

#### **Type Hints**
```python
from typing import Optional, List, Dict, Any

def process_transaction(
    amount: float,
    from_wallet: str,
    to_wallet: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Transaction:
    pass
```

---

## 🧪 **ESTRATÉGIA DE TESTES**

### **1. Estrutura de Testes**
```
tests/
├── unit/                         # 🧪 Testes unitários
│   ├── domain/                   # Testes de domínio
│   ├── application/              # Testes de aplicação
│   └── infrastructure/           # Testes de infraestrutura
├── integration/                  # 🔗 Testes de integração
├── e2e/                          # 🌐 Testes end-to-end
├── performance/                  # ⚡ Testes de performance
├── fixtures/                     # 🎭 Fixtures e helpers
└── conftest.py                   # ⚙️ Configuração global
```

### **2. Tipos de Testes**

#### **Testes Unitários**
```python
import pytest
from src.domain.wallet.entities.wallet import Wallet

@pytest.mark.unit
class TestWallet:
    def test_create_wallet_with_valid_name(self):
        """Testa criação de carteira com nome válido"""
        wallet = Wallet.create("Test Wallet")
        assert wallet.name == "Test Wallet"
        assert wallet.is_active is True
        
    def test_create_wallet_with_invalid_name_raises_error(self):
        """Testa que nome inválido gera exceção"""
        with pytest.raises(ValidationError):
            Wallet.create("")
```

#### **Testes de Integração**
```python
import pytest
from src.application.wallet.commands.create_wallet import CreateWalletCommandHandler

@pytest.mark.integration
class TestCreateWalletIntegration:
    async def test_create_wallet_command_handler(self, mock_wallet_repository):
        """Testa handler de comando de criação"""
        handler = CreateWalletCommandHandler(mock_wallet_repository)
        command = CreateWalletCommand(name="Test Wallet")
        
        result = await handler.execute(command)
        
        assert result.name == "Test Wallet"
        mock_wallet_repository.save.assert_called_once()
```

#### **Testes E2E**
```python
import pytest
from fastapi.testclient import TestClient

@pytest.mark.e2e
class TestWalletAPI:
    def test_create_wallet_endpoint(self, async_client):
        """Testa endpoint de criação de carteira"""
        response = async_client.post(
            "/api/v1/wallets/",
            json={"name": "Test Wallet", "password": "test123"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Wallet"
```

### **3. Execução de Testes**
```bash
# Todos os testes
pytest

# Testes unitários apenas
pytest -m unit

# Testes de integração
pytest -m integration

# Testes E2E
pytest -m e2e

# Testes de performance
pytest -m performance

# Com cobertura
pytest --cov=src --cov-report=html

# Testes específicos
pytest tests/unit/domain/entities/test_wallet.py
```

---

## 🔄 **WORKFLOW DE DESENVOLVIMENTO**

### **1. Branching Strategy**
```
main                    # 🚀 Branch principal (produção)
├── develop            # 🔄 Branch de desenvolvimento
├── feature/nome       # ✨ Features novas
├── bugfix/nome        # 🐛 Correções de bugs
├── hotfix/nome        # 🔥 Correções urgentes
└── release/versao     # 📦 Preparação de releases
```

### **2. Processo de Contribuição**

#### **Passo 1: Preparação**
```bash
# 1. Fork do repositório
# 2. Clone local
git clone https://github.com/seu-usuario/coinbalance.git
cd coinbalance

# 3. Criar branch
git checkout -b feature/nova-funcionalidade

# 4. Instalar pre-commit
pre-commit install
```

#### **Passo 2: Desenvolvimento**
```bash
# 1. Fazer alterações
# 2. Executar testes
pytest

# 3. Verificar qualidade
black --check .
flake8 .
mypy src/

# 4. Commit
git add .
git commit -m "feat: adiciona nova funcionalidade X"
```

#### **Passo 3: Pull Request**
```bash
# 1. Push
git push origin feature/nova-funcionalidade

# 2. Criar PR no GitHub
# 3. Aguardar review
# 4. Fazer correções se necessário
# 5. Merge após aprovação
```

### **3. Convenções de Commit**
```
feat: nova funcionalidade
fix: correção de bug
docs: documentação
style: formatação
refactor: refatoração
test: testes
chore: tarefas de manutenção

Exemplos:
feat: adiciona endpoint de criação de carteira
fix: corrige validação de senha
docs: atualiza README
test: adiciona testes para Wallet entity
```

---

## 🚀 **CI/CD PIPELINE**

### **1. Pre-commit Hooks**
```bash
# Instalar hooks
pre-commit install

# Executar manualmente
pre-commit run --all-files

# Hooks configurados:
# - Black (formatação)
# - isort (imports)
# - Flake8 (linting)
# - MyPy (type checking)
# - Bandit (segurança)
# - pytest (testes)
```

### **2. GitHub Actions**
```yaml
# Workflows automáticos:
# - Code Quality (Black, Flake8, MyPy, Bandit)
# - Tests (Unit, Integration, E2E, Performance)
# - Build & Deploy (Docker, Staging)
# - Notifications (Success/Failure)
```

### **3. Métricas de Qualidade**
- ✅ **Cobertura de testes:** >80%
- ✅ **Complexidade ciclomática:** <10
- ✅ **Duplicação de código:** 0%
- ✅ **Vulnerabilidades:** 0 críticas
- ✅ **Performance:** <100ms por endpoint

---

## 📚 **DOCUMENTAÇÃO**

### **1. Documentação Técnica**
- 📖 **README.md** - Visão geral do projeto
- 🏗️ **docs/ARCHITECTURE.md** - Arquitetura detalhada
- 🚀 **docs/DEPLOYMENT.md** - Guia de deploy
- 🔧 **docs/API.md** - Documentação da API

### **2. Documentação de Código**
- 📝 **Docstrings** em todas as funções públicas
- 🏷️ **Type hints** em todas as funções
- 📋 **Exemplos** nos docstrings
- 🔍 **Comentários** explicativos em código complexo

### **3. Documentação de Decisões**
- 📊 **ADRs** (Architecture Decision Records)
- 🔄 **Changelog** detalhado
- 📈 **Roadmap** do projeto

---

## 🔒 **SEGURANÇA**

### **1. Práticas de Segurança**
- ✅ **Validação rigorosa** de entrada
- ✅ **Sanitização** de dados
- ✅ **Rate limiting** em endpoints
- ✅ **Logging seguro** (sem dados sensíveis)
- ✅ **Princípio do menor privilégio**

### **2. Verificações Automáticas**
```bash
# Verificação de segurança
bandit -r src/

# Verificação de dependências
safety check

# Verificação de secrets
git-secrets --scan
```

### **3. Responsabilidade de Segurança**
- 🚨 **Reportar vulnerabilidades** imediatamente
- 🔒 **Nunca commitar** secrets ou chaves
- 🛡️ **Usar HTTPS** em produção
- 📊 **Monitorar logs** de segurança

---

## 📊 **MÉTRICAS E MONITORAMENTO**

### **🛠️ Sistema de Monitoramento Automatizado**
O CoinBalance possui um **sistema completo de monitoramento** que gera relatórios detalhados:

```bash
# Gerar relatórios completos
python scripts/generate_reports.py

# Relatórios gerados:
# - quality-report.html (Dashboard visual)
# - quality-report.json (Dados estruturados)
# - quality-report.md (Relatório markdown)
```

### **📊 Dashboard de Qualidade**
- **[docs/DASHBOARD_QUALIDADE.md](docs/DASHBOARD_QUALIDADE.md)** - Monitoramento em tempo real
- **Score geral**: 95/100 ⭐⭐⭐⭐⭐
- **Arquitetura**: 100/100 ✅
- **Testes**: 87.5% ✅
- **Segurança**: 90/100 ✅
- **Documentação**: 100/100 ✅

### **1. Métricas de Código**
- 📈 **Cobertura de testes** (≥80% obrigatório)
- 🔍 **Complexidade ciclomática** (≤10)
- 📊 **Duplicação de código** (0%)
- ⚡ **Performance dos endpoints** (<100ms)

### **2. Métricas de Qualidade**
- ✅ **Build success rate** (100%)
- 🚀 **Deploy frequency** (Contínuo)
- 🐛 **Bug rate** (Monitorado)
- 📚 **Documentation coverage** (100%)

### **3. Ferramentas de Monitoramento**
- 📊 **Scripts automatizados** - Verificação contínua
- 🔍 **Gates de qualidade** - Bloqueio automático
- 📈 **Relatórios HTML** - Dashboard visual
- 🚨 **Alertas automáticos** - CI/CD pipeline

---

## 🎓 **EDUCAÇÃO E TREINAMENTO**

### **1. Recursos de Aprendizado**
- 📚 **Clean Code** - Robert C. Martin
- 🏗️ **Domain-Driven Design** - Eric Evans
- 🔧 **Clean Architecture** - Robert C. Martin
- 🧪 **Test-Driven Development** - Kent Beck

### **2. Treinamentos Internos**
- 🎯 **Workshops** de arquitetura
- 🧪 **Sessões** de testes
- 🔒 **Treinamentos** de segurança
- 📊 **Code reviews** em grupo

### **3. Certificações**
- 🏆 **Clean Code** certification
- 🔒 **Security** best practices
- 🧪 **Testing** methodologies
- 🏗️ **Architecture** patterns

---

## ✅ **CHECKLIST DE CONTRIBUIÇÃO**

### **⚠️ ANTES de Submeter PR (OBRIGATÓRIO):**
- [ ] ✅ **Protocolo de manutenção** consultado
- [ ] ✅ **Documentação obrigatória** lida
- [ ] ✅ **Verificação de qualidade** executada: `./scripts/quality-check.sh`
- [ ] ✅ **Verificação arquitetural** executada: `python scripts/check_architecture.py`
- [ ] ✅ **Validação de mudanças** executada: `python scripts/validate_change.py`
- [ ] ✅ Código formatado com Black
- [ ] ✅ Imports organizados com isort
- [ ] ✅ Linting passou (Flake8)
- [ ] ✅ Type checking passou (MyPy)
- [ ] ✅ Testes unitários passaram
- [ ] ✅ Testes de integração passaram
- [ ] ✅ Cobertura de testes ≥80%
- [ ] ✅ Documentação atualizada
- [ ] ✅ Commits seguem convenção
- [ ] ✅ Branch atualizada com main

### **Code Review (OBRIGATÓRIO):**
- [ ] ✅ **Arquitetura DDD** respeitada
- [ ] ✅ **SOLID principles** aplicados
- [ ] ✅ **Segurança** verificada
- [ ] ✅ **Performance** adequada
- [ ] ✅ **Testes** abrangentes
- [ ] ✅ **Documentação** clara
- [ ] ✅ **Gates de qualidade** passaram

---

## 🆘 **SUPORTE E CONTATO**

### **Canais de Suporte:**
- 📧 **Email:** dev@coinbalance.com
- 💬 **Slack:** #coinbalance-dev
- 📱 **Discord:** CoinBalance Community
- 🐛 **Issues:** GitHub Issues

### **Horários de Suporte:**
- 🕐 **Segunda a Sexta:** 9h às 18h (BRT)
- 🚨 **Emergências:** 24/7 via Slack

---

**Versão:** 1.0  
**Data:** 27 de Outubro de 2025  
**Status:** ✅ Ativo

---

## 🎯 **RESUMO**

Este guia estabelece os padrões de qualidade e contribuição para o CoinBalance, garantindo:

- ✅ **Código limpo** e manutenível
- ✅ **Arquitetura sólida** e escalável
- ✅ **Testes abrangentes** e confiáveis
- ✅ **Segurança robusta** e monitorada
- ✅ **Documentação clara** e atualizada
- ✅ **Processo eficiente** e colaborativo

**Seguindo estes padrões, garantimos um projeto de qualidade acadêmica e profissional! 🚀**