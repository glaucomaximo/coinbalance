#!/bin/bash
# 🔍 SCRIPT DE VERIFICAÇÃO DE QUALIDADE - CoinBalance
# Executa todos os gates de qualidade obrigatórios

set -e  # Falha em qualquer erro

echo "🪙 CoinBalance - Verificação de Qualidade"
echo "========================================"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        exit 1
    fi
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Verificar se estamos no diretório correto
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Execute este script na raiz do projeto CoinBalance${NC}"
    exit 1
fi

print_info "Iniciando verificação de qualidade..."

# Gate 1: Formatação de Código
echo ""
echo "🎨 GATE 1: Formatação de Código"
echo "--------------------------------"

print_info "Verificando formatação com Black..."
black --check --diff . > /dev/null 2>&1
print_status $? "Black - Formatação OK"

print_info "Verificando organização de imports com isort..."
isort --check-only --diff . > /dev/null 2>&1
print_status $? "isort - Imports organizados"

# Gate 2: Linting e Type Checking
echo ""
echo "🔍 GATE 2: Linting e Type Checking"
echo "-----------------------------------"

print_info "Executando linting com Flake8..."
flake8 . > /dev/null 2>&1
print_status $? "Flake8 - Linting OK"

print_info "Executando type checking com MyPy..."
mypy src/ > /dev/null 2>&1
print_status $? "MyPy - Type checking OK"

# Gate 3: Segurança
echo ""
echo "🔒 GATE 3: Verificação de Segurança"
echo "-----------------------------------"

print_info "Executando verificação de segurança com Bandit..."
bandit -r src/ -f json -o bandit-report.json > /dev/null 2>&1
print_status $? "Bandit - Segurança OK"

print_info "Verificando dependências com Safety..."
if command -v safety &> /dev/null; then
    safety check > /dev/null 2>&1
    print_status $? "Safety - Dependências seguras"
else
    print_warning "Safety não instalado - pulando verificação de dependências"
fi

# Gate 4: Testes
echo ""
echo "🧪 GATE 4: Testes Automatizados"
echo "-------------------------------"

print_info "Executando testes unitários..."
pytest tests/unit/ -v --tb=short > /dev/null 2>&1
print_status $? "Testes unitários OK"

print_info "Executando testes de integração..."
pytest tests/integration/ -v --tb=short > /dev/null 2>&1
print_status $? "Testes de integração OK"

print_info "Verificando cobertura de testes..."
coverage run -m pytest tests/ > /dev/null 2>&1
coverage report --fail-under=80 > /dev/null 2>&1
print_status $? "Cobertura de testes ≥80%"

# Gate 5: Arquitetura
echo ""
echo "🏗️ GATE 5: Verificação Arquitetural"
echo "------------------------------------"

print_info "Verificando estrutura DDD..."
if [ -d "src/domain" ] && [ -d "src/application" ] && [ -d "src/infrastructure" ] && [ -d "src/presentation" ]; then
    print_status 0 "Estrutura DDD OK"
else
    print_status 1 "Estrutura DDD incorreta"
fi

print_info "Verificando imports do domínio..."
python -c "
import sys
sys.path.append('src')
try:
    from domain.wallet.entities.wallet import Wallet
    from domain.wallet.value_objects.balance import Balance
    print('✅ Imports do domínio OK')
    sys.exit(0)
except ImportError as e:
    print(f'❌ Erro nos imports do domínio: {e}')
    sys.exit(1)
" > /dev/null 2>&1
print_status $? "Imports do domínio OK"

# Gate 6: Performance
echo ""
echo "⚡ GATE 6: Verificação de Performance"
echo "-------------------------------------"

print_info "Executando testes de performance..."
if [ -d "tests/performance" ]; then
    pytest tests/performance/ -m performance --durations=10 > /dev/null 2>&1
    print_status $? "Testes de performance OK"
else
    print_warning "Diretório de testes de performance não encontrado"
fi

# Gate 7: Documentação
echo ""
echo "📚 GATE 7: Verificação de Documentação"
echo "--------------------------------------"

print_info "Verificando documentação obrigatória..."
required_docs=("README.md" "CONTRIBUTING.md" "CHANGELOG.md" "docs/RESUMO_REFATORACAO_DDD.md" "docs/ARQUITETURA_DETALHADA.md")
for doc in "${required_docs[@]}"; do
    if [ -f "$doc" ]; then
        print_status 0 "$doc existe"
    else
        print_status 1 "$doc não encontrado"
    fi
done

# Relatório Final
echo ""
echo "📊 RELATÓRIO FINAL"
echo "=================="

# Gerar relatório de cobertura
print_info "Gerando relatório de cobertura..."
coverage html -d htmlcov > /dev/null 2>&1
print_status $? "Relatório de cobertura gerado em htmlcov/"

# Gerar relatório de segurança
if [ -f "bandit-report.json" ]; then
    print_info "Relatório de segurança salvo em bandit-report.json"
fi

# Verificar se todos os gates passaram
echo ""
echo -e "${GREEN}🎉 TODOS OS GATES DE QUALIDADE PASSARAM!${NC}"
echo ""
echo "✅ Formatação de código OK"
echo "✅ Linting e type checking OK"
echo "✅ Segurança verificada"
echo "✅ Testes passaram"
echo "✅ Arquitetura validada"
echo "✅ Performance OK"
echo "✅ Documentação completa"
echo ""
echo -e "${BLUE}📁 Relatórios gerados:${NC}"
echo "  - htmlcov/ (cobertura de testes)"
echo "  - bandit-report.json (segurança)"
echo ""
echo -e "${GREEN}🚀 Projeto pronto para manutenção!${NC}"
