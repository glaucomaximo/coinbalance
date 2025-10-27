# ⚙️ GESTÃO DE CONFIGURAÇÃO - CoinBalance

## 📋 **VISÃO GERAL**

Este documento estabelece o processo completo de gestão de configuração para o projeto CoinBalance, garantindo controle de versão, rastreabilidade e integridade de todos os artefatos do projeto.

---

## 🎯 **OBJETIVOS**

- ✅ **Controle de Versão**: Gerenciamento de todas as versões de artefatos
- ✅ **Rastreabilidade**: Histórico completo de mudanças
- ✅ **Integridade**: Garantia de consistência entre artefatos
- ✅ **Reprodutibilidade**: Capacidade de reproduzir builds
- ✅ **Auditoria**: Controle de acesso e mudanças

---

## 📊 **ESCOPO DA GESTÃO DE CONFIGURAÇÃO**

### **🔧 Artefatos Controlados**

#### **Código Fonte**
- ✅ **Arquivos Python**: `src/` (100% controlado)
- ✅ **Scripts**: `scripts/` (100% controlado)
- ✅ **Testes**: `tests/` (100% controlado)
- ✅ **Configurações**: `pyproject.toml`, `.pre-commit-config.yaml`

#### **Documentação**
- ✅ **README.md**: Documentação principal
- ✅ **CONTRIBUTING.md**: Guia de contribuição
- ✅ **CHANGELOG.md**: Histórico de mudanças
- ✅ **docs/**: Documentação técnica completa

#### **Configurações**
- ✅ **requirements.txt**: Dependências Python
- ✅ **pyproject.toml**: Configurações de ferramentas
- ✅ **.github/workflows/**: CI/CD pipeline
- ✅ **Dockerfile**: Containerização

#### **Artefatos de Build**
- ✅ **Logs**: `logs/` (rotacionados)
- ✅ **Relatórios**: `htmlcov/`, `bandit-report.json`
- ✅ **Cache**: `.pytest_cache/`, `.mypy_cache/`

---

## 🔄 **PROCESSO DE GESTÃO DE CONFIGURAÇÃO**

### **📋 1. Identificação de Configuração**

#### **Baseline de Configuração**
```
coinbalance-v2.1.0-ddd/
├── src/                          # Código fonte (v2.1.0)
├── tests/                        # Testes (v2.1.0)
├── docs/                         # Documentação (v2.1.0)
├── scripts/                      # Scripts (v2.1.0)
├── pyproject.toml               # Configurações (v2.1.0)
├── requirements.txt              # Dependências (v2.1.0)
├── .github/workflows/            # CI/CD (v2.1.0)
└── Dockerfile                    # Container (v2.1.0)
```

#### **Identificadores de Versão**
- **Formato**: `v{major}.{minor}.{patch}-{suffix}`
- **Exemplo**: `v2.1.0-ddd`
- **Semantic Versioning**: Seguindo padrão semver
- **Tags Git**: Cada release marcado com tag

### **📊 2. Controle de Versão**

#### **Estratégia de Branching**
```
main (production)
├── develop (integration)
├── feature/wallet-transactions
├── feature/blockchain-domain
├── bugfix/security-patch
└── hotfix/critical-fix
```

#### **Convenções de Commit**
```bash
# Formato: tipo(escopo): descrição
feat(wallet): adiciona criação de carteira
fix(api): corrige validação de entrada
docs(readme): atualiza instruções de instalação
test(wallet): adiciona testes unitários
refactor(domain): reorganiza value objects
chore(deps): atualiza dependências
```

#### **Controle de Mudanças**
- **Pull Requests**: Obrigatórios para mudanças
- **Code Review**: Mínimo 2 aprovações
- **CI/CD**: Builds automáticos em cada PR
- **Gates de Qualidade**: Bloqueio automático

### **🔄 3. Auditoria de Configuração**

#### **Log de Mudanças**
```bash
# Histórico detalhado de mudanças
git log --oneline --graph --all
git log --stat --author="developer@coinbalance.com"
git log --grep="feat\|fix\|docs" --oneline
```

#### **Rastreabilidade**
- **Issue → Commit**: Cada commit referencia issue
- **Commit → Build**: Cada commit gera build
- **Build → Deploy**: Cada build pode ser deployado
- **Deploy → Monitoramento**: Cada deploy é monitorado

---

## 🛠️ **FERRAMENTAS DE GESTÃO DE CONFIGURAÇÃO**

### **📦 Git (Versionamento)**
```bash
# Configuração inicial
git config --global user.name "CoinBalance Developer"
git config --global user.email "dev@coinbalance.com"

# Workflow padrão
git checkout -b feature/nova-funcionalidade
git add .
git commit -m "feat(domain): implementa nova funcionalidade"
git push origin feature/nova-funcionalidade
```

### **🔍 Pre-commit Hooks**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
```

### **🚀 GitHub Actions (CI/CD)**
```yaml
# .github/workflows/ci.yml
name: 🪙 CoinBalance CI/CD
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run quality checks
        run: ./scripts/quality-check.sh
```

---

## 📊 **CONFIGURAÇÃO POR AMBIENTE**

### **🌍 Ambientes Configurados**

#### **Development**
```python
# src/infrastructure/config/settings.py
@dataclass(frozen=True)
class DevelopmentSettings(Settings):
    environment: str = "development"
    debug: bool = True
    database_url: str = "sqlite:///blockchain.db"
    log_level: str = "DEBUG"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
```

#### **Staging**
```python
@dataclass(frozen=True)
class StagingSettings(Settings):
    environment: str = "staging"
    debug: bool = False
    database_url: str = "postgresql://user:pass@staging-db/coinbalance"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
```

#### **Production**
```python
@dataclass(frozen=True)
class ProductionSettings(Settings):
    environment: str = "production"
    debug: bool = False
    database_url: str = "postgresql://user:pass@prod-db/coinbalance"
    log_level: str = "WARNING"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    workers: int = 4
```

### **🔐 Gestão de Secrets**
```bash
# Variáveis de ambiente por ambiente
# .env.development
DATABASE_URL=sqlite:///blockchain.db
SECRET_KEY=dev-secret-key
DEBUG=true

# .env.staging
DATABASE_URL=postgresql://user:pass@staging-db/coinbalance
SECRET_KEY=staging-secret-key
DEBUG=false

# .env.production
DATABASE_URL=postgresql://user:pass@prod-db/coinbalance
SECRET_KEY=production-secret-key
DEBUG=false
```

---

## 📈 **CONTROLE DE BUILD E RELEASE**

### **🏗️ Processo de Build**

#### **Build Automatizado**
```bash
# Script de build
#!/bin/bash
# scripts/build.sh

echo "🏗️ Building CoinBalance v2.1.0"

# 1. Verificar qualidade
./scripts/quality-check.sh

# 2. Executar testes
pytest tests/ --cov=src --cov-report=html

# 3. Gerar relatórios
python scripts/generate_reports.py

# 4. Build Docker
docker build -t coinbalance:v2.1.0 .

# 5. Tag release
git tag -a v2.1.0 -m "Release version 2.1.0"
git push origin v2.1.0

echo "✅ Build completed successfully"
```

#### **Versionamento Automático**
```python
# src/infrastructure/config/settings.py
import os
from pathlib import Path

def get_version():
    """Obtém versão do projeto"""
    version_file = Path(__file__).parent.parent.parent.parent / "VERSION"
    if version_file.exists():
        return version_file.read_text().strip()
    return "2.1.0"

VERSION = get_version()
```

### **📦 Gestão de Releases**

#### **Release Notes**
```markdown
# CHANGELOG.md
## [2.1.0] - 2025-10-27

### 🆕 Adicionado
- Sistema completo de gestão de configuração
- Arquitetura DDD implementada
- Scripts de qualidade automatizados
- Documentação técnica completa

### 🔧 Modificado
- Estrutura do projeto reorganizada
- Configurações centralizadas
- Processo de build otimizado

### 🔒 Segurança
- Gestão de secrets implementada
- Controle de acesso configurado
- Auditoria de mudanças ativa
```

#### **Release Checklist**
- [ ] ✅ Todos os testes passando
- [ ] ✅ Qualidade verificada (gates passaram)
- [ ] ✅ Documentação atualizada
- [ ] ✅ Changelog atualizado
- [ ] ✅ Version bump realizado
- [ ] ✅ Tag criada e enviada
- [ ] ✅ Release notes publicadas
- [ ] ✅ Deploy em staging testado

---

## 🔍 **AUDITORIA E RASTREABILIDADE**

### **📊 Relatórios de Auditoria**

#### **Relatório de Mudanças**
```bash
# Gerar relatório de mudanças
git log --since="2025-10-01" --until="2025-10-31" \
  --pretty=format:"%h %an %ad %s" --date=short > changes-report.txt
```

#### **Relatório de Commits por Desenvolvedor**
```bash
# Commits por desenvolvedor
git shortlog -sn --since="2025-10-01"
```

#### **Relatório de Arquivos Modificados**
```bash
# Arquivos mais modificados
git log --since="2025-10-01" --name-only --pretty=format: | \
  sort | uniq -c | sort -rn | head -20
```

### **🔐 Controle de Acesso**

#### **Permissões por Ambiente**
- **Development**: Todos os desenvolvedores
- **Staging**: Desenvolvedores sênior + QA
- **Production**: DevOps + CTO apenas

#### **Auditoria de Acesso**
```bash
# Log de acessos ao repositório
git log --pretty=format:"%an %ae %ad %s" --date=iso
```

---

## 📊 **MÉTRICAS DE CONFIGURAÇÃO**

### **📈 Métricas de Controle**
- **Commits por dia**: 5-10 commits
- **Pull Requests por semana**: 10-15 PRs
- **Builds por dia**: 20-30 builds
- **Deploys por semana**: 2-3 deploys

### **📊 Métricas de Qualidade**
- **Build Success Rate**: 95%+
- **Code Review Coverage**: 100%
- **Test Coverage**: 80%+
- **Security Scan**: 0 vulnerabilidades críticas

---

## 🚨 **GESTÃO DE INCIDENTES**

### **🔧 Processo de Rollback**
```bash
# Rollback para versão anterior
git checkout v2.0.0
git checkout -b hotfix/rollback-v2.1.0
git push origin hotfix/rollback-v2.1.0
```

### **🚨 Hotfix Process**
```bash
# Criar hotfix
git checkout main
git checkout -b hotfix/critical-security-fix
# Fazer correção
git commit -m "fix(security): corrige vulnerabilidade crítica"
git push origin hotfix/critical-security-fix
# Merge para main e develop
```

---

## 📚 **ARTEFATOS DE CONFIGURAÇÃO**

### **📋 Documentos Principais**
- **Plano de Configuração**: Este documento
- **Política de Versionamento**: `docs/engenharia/versionamento.md`
- **Processo de Release**: `docs/engenharia/release-process.md`
- **Auditoria**: `docs/engenharia/auditoria.md`

### **🔧 Configurações**
- **Git**: `.gitignore`, `.gitattributes`
- **Pre-commit**: `.pre-commit-config.yaml`
- **CI/CD**: `.github/workflows/`
- **Docker**: `Dockerfile`, `docker-compose.yml`

---

## ✅ **COMPLIANCE E VALIDAÇÃO**

### **🎯 Padrões Seguidos**
- ✅ **ISO/IEC 12207**: Processos de ciclo de vida
- ✅ **IEEE 828**: Padrão para gestão de configuração
- ✅ **GitFlow**: Fluxo de trabalho Git
- ✅ **Semantic Versioning**: Versionamento semântico

### **📋 Checklist de Validação**
- [ ] ✅ Todos os artefatos estão versionados
- [ ] ✅ Processo de build é reproduzível
- [ ] ✅ Auditoria de mudanças ativa
- [ ] ✅ Controle de acesso implementado
- [ ] ✅ Rollback é possível

---

**Versão**: 1.0  
**Data**: 27 de Outubro de 2025  
**Status**: ✅ ATIVO  
**Próxima Revisão**: 2025-11-27  
**Responsável**: CTO - CoinBalance
