# 📋 Artefatos - CoinBalance

## 📋 **Índice de Artefatos**

Esta seção contém todos os artefatos de documentação do projeto CoinBalance.

---

## 📊 **Artefatos Principais**

### **Inventário do Software**
- **Arquivo**: [software-inventory.md](software-inventory.md)
- **Descrição**: Inventário completo de componentes, funcionalidades e status do projeto
- **Última Atualização**: 27 de Outubro de 2024
- **Status**: ✅ Atualizado

---

## 📁 **Estrutura de Artefatos**

### **Documentação Técnica**
- **Arquitetura**: [../architecture/README.md](../architecture/README.md)
- **API Reference**: [../api/README.md](../api/README.md)
- **Requisitos**: [../requirements/](../requirements/)

### **Relatórios**
- **Qualidade**: [../reports/quality-report.md](../reports/quality-report.md)
- **Testes**: [../reports/test-report.md](../reports/test-report.md)

### **Logs e Dados**
- **Logs do Sistema**: [../../logs/](../../logs/)
- **Dados do Sistema**: [../../data/](../../data/)

---

## 📊 **Inventário de Componentes**

### **Código Fonte**
- **Domain Layer**: `src/domain/` (4 módulos)
- **Application Layer**: `src/application/` (3 módulos)
- **Infrastructure Layer**: `src/infrastructure/` (4 módulos)
- **Presentation Layer**: `src/presentation/` (2 módulos)

### **Testes**
- **E2E Tests**: `tests/e2e/` (15 testes)
- **Integration Tests**: `tests/integration/` (8 testes)
- **Performance Tests**: `tests/performance/` (8 testes)
- **Unit Tests**: `tests/unit/` (64 testes)

### **Documentação**
- **README**: `README.md`
- **Changelog**: `CHANGELOG.md`
- **Contributing**: `CONTRIBUTING.md`
- **Documentação**: `docs/` (estrutura completa)

---

## 🔧 **Ferramentas e Scripts**

### **Scripts de Qualidade**
- **Linux/Mac**: `scripts/quality-check.sh`
- **Windows**: `scripts/quality-check.ps1`
- **Validação**: `scripts/validate_*.py`

### **Configuração**
- **Dependências**: `requirements.txt`
- **Projeto**: `pyproject.toml`
- **Testes**: `pytest.ini`
- **Pre-commit**: `.pre-commit-config.yaml`

---

## 📈 **Métricas dos Artefatos**

### **Estatísticas de Código**
- **Total de Arquivos Python**: ~50
- **Total de Testes**: 95
- **Total de Documentos**: ~20
- **Tamanho do Projeto**: ~2MB

### **Qualidade**
- **Taxa de Sucesso dos Testes**: 100%
- **Cobertura Estimada**: ~85%
- **Arquitetura**: DDD + Clean Architecture
- **Padrões**: CQRS, Repository, DI

---

## 🔄 **Manutenção dos Artefatos**

### **Atualizações Automáticas**
- ✅ Testes (após cada execução)
- ✅ Logs (durante execução)
- ✅ Changelog (após mudanças)

### **Atualizações Manuais**
- ✅ Documentação técnica
- ✅ Relatórios de qualidade
- ✅ Inventário do software

### **Frequência de Atualização**
- **Diária**: Logs e testes
- **Semanal**: Relatórios de qualidade
- **Mensal**: Documentação técnica
- **Por Release**: Changelog e inventário

---

## 🎯 **Como Usar**

### **Visualizar Inventário**
```bash
# Abrir inventário completo
cat docs/artifacts/software-inventory.md

# Visualizar estrutura do projeto
tree -I '__pycache__|*.pyc|.git' -L 3
```

### **Atualizar Artefatos**
```bash
# Executar testes e atualizar relatórios
python -m pytest tests/ --tb=short -q

# Verificar qualidade e atualizar relatórios
./scripts/quality-check.sh
```

### **Gerar Novos Artefatos**
```bash
# Gerar documentação da API
python -c "from src.presentation.api.app import app; print(app.openapi())"

# Gerar relatório de dependências
pip list --format=freeze > requirements-detailed.txt
```

---

## 📋 **Checklist de Artefatos**

### **Artefatos Obrigatórios**
- ✅ README.md
- ✅ CHANGELOG.md
- ✅ requirements.txt
- ✅ pyproject.toml
- ✅ pytest.ini

### **Artefatos de Qualidade**
- ✅ Documentação da API
- ✅ Relatórios de testes
- ✅ Relatórios de qualidade
- ✅ Inventário do software

### **Artefatos de Desenvolvimento**
- ✅ Contributing.md
- ✅ Arquitetura do sistema
- ✅ Requisitos funcionais
- ✅ Requisitos não-funcionais

---

*Índice de artefatos atualizado em 27 de Outubro de 2024*
