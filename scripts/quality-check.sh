#!/bin/bash

# 🔍 **SCRIPT DE VERIFICAÇÃO DE QUALIDADE - COINBALANCE**
# Este script executa todas as verificações de qualidade de software

set -e  # Exit on any error

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Função para executar comando e capturar resultado
run_check() {
    local name="$1"
    local command="$2"
    local expected_exit_code="${3:-0}"
    
    log "Executando: $name"
    
    if eval "$command" > /dev/null 2>&1; then
        if [ $? -eq $expected_exit_code ]; then
            success "$name - PASSOU"
            return 0
        else
            error "$name - FALHOU (código de saída: $?)"
            return 1
        fi
    else
        error "$name - FALHOU"
        return 1
    fi
}

# Função para verificar se comando existe
check_command() {
    if ! command -v "$1" &> /dev/null; then
        error "Comando '$1' não encontrado. Instale com: pip install $1"
        return 1
    fi
    return 0
}

# Função para verificar se arquivo existe
check_file() {
    if [ ! -f "$1" ]; then
        error "Arquivo '$1' não encontrado"
        return 1
    fi
    return 0
}

# Função para verificar se diretório existe
check_directory() {
    if [ ! -d "$1" ]; then
        error "Diretório '$1' não encontrado"
        return 1
    fi
    return 0
}

# Função principal
main() {
    echo "🔍 COINBALANCE - VERIFICAÇÃO DE QUALIDADE DE SOFTWARE"
    echo "=================================================="
    echo ""
    
    local total_checks=0
    local passed_checks=0
    local failed_checks=0
    
    # Verificar pré-requisitos
    log "Verificando pré-requisitos..."
    
    check_command "python3" || exit 1
    check_command "pip" || exit 1
    check_directory "src" || exit 1
    check_directory "tests" || exit 1
    
    success "Pré-requisitos verificados"
    echo ""
    
    # 1. VERIFICAÇÕES DE FORMATAÇÃO
    log "📝 VERIFICAÇÕES DE FORMATAÇÃO"
    echo "------------------------"
    
    # Black
    if check_command "black"; then
        total_checks=$((total_checks + 1))
        if run_check "Black - Formatação de código" "black --check --diff src/ tests/"; then
            passed_checks=$((passed_checks + 1))
        else
            failed_checks=$((failed_checks + 1))
            warning "Execute 'black src/ tests/' para corrigir formatação"
        fi
    else
        error "Black não instalado. Instale com: pip install black"
        failed_checks=$((failed_checks + 1))
    fi
    
    # isort
    if check_command "isort"; then
        total_checks=$((total_checks + 1))
        if run_check "isort - Organização de imports" "isort --check-only --diff src/ tests/"; then
            passed_checks=$((passed_checks + 1))
        else
            failed_checks=$((failed_checks + 1))
            warning "Execute 'isort src/ tests/' para corrigir imports"
        fi
    else
        error "isort não instalado. Instale com: pip install isort"
        failed_checks=$((failed_checks + 1))
    fi
    
    echo ""
    
    # 2. VERIFICAÇÕES DE LINTING
    log "🔍 VERIFICAÇÕES DE LINTING"
    echo "----------------------"
    
    # Flake8
    if check_command "flake8"; then
        total_checks=$((total_checks + 1))
        if run_check "Flake8 - Linting de código" "flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503"; then
            passed_checks=$((passed_checks + 1))
        else
            failed_checks=$((failed_checks + 1))
        fi
    else
        error "Flake8 não instalado. Instale com: pip install flake8"
        failed_checks=$((failed_checks + 1))
    fi
    
    # MyPy
    if check_command "mypy"; then
        total_checks=$((total_checks + 1))
        if run_check "MyPy - Verificação de tipos" "mypy src/ --ignore-missing-imports --strict"; then
            passed_checks=$((passed_checks + 1))
        else
            failed_checks=$((failed_checks + 1))
        fi
    else
        error "MyPy não instalado. Instale com: pip install mypy"
        failed_checks=$((failed_checks + 1))
    fi
    
    # Pylint
    if check_command "pylint"; then
        total_checks=$((total_checks + 1))
        if run_check "Pylint - Análise de código" "pylint src/ --rcfile=.pylintrc"; then
            passed_checks=$((passed_checks + 1))
        else
            failed_checks=$((failed_checks + 1))
        fi
    else
        error "Pylint não instalado. Instale com: pip install pylint"
        failed_checks=$((failed_checks + 1))
    fi
    
    echo ""
    
    # 3. VERIFICAÇÕES DE SEGURANÇA
    log "🔒 VERIFICAÇÕES DE SEGURANÇA"
    echo "------------------------"
    
    # Bandit
    if check_command "bandit"; then
        total_checks=$((total_checks + 1))
        if run_check "Bandit - Análise de segurança" "bandit -r src/ -ll"; then
            passed_checks=$((passed_checks + 1))
        else
            failed_checks=$((failed_checks + 1))
        fi
    else
        error "Bandit não instalado. Instale com: pip install bandit"
        failed_checks=$((failed_checks + 1))
    fi
    
    # Safety
    if check_command "safety"; then
        total_checks=$((total_checks + 1))
        if run_check "Safety - Vulnerabilidades de dependências" "safety check"; then
            passed_checks=$((passed_checks + 1))
        else
            failed_checks=$((failed_checks + 1))
        fi
    else
        error "Safety não instalado. Instale com: pip install safety"
        failed_checks=$((failed_checks + 1))
    fi
    
    echo ""
    
    # 4. VERIFICAÇÕES DE COMPLEXIDADE
    log "📊 VERIFICAÇÕES DE COMPLEXIDADE"
    echo "----------------------------"
    
    # Radon
    if check_command "radon"; then
        total_checks=$((total_checks + 1))
        if run_check "Radon - Análise de complexidade" "radon cc src/ -a"; then
            passed_checks=$((passed_checks + 1))
        else
            failed_checks=$((failed_checks + 1))
        fi
    else
        error "Radon não instalado. Instale com: pip install radon"
        failed_checks=$((failed_checks + 1))
    fi
    
    # Xenon
    if check_command "xenon"; then
        total_checks=$((total_checks + 1))
        if run_check "Xenon - Monitoramento de complexidade" "xenon --max-absolute B --max-modules A --max-average A src/"; then
            passed_checks=$((passed_checks + 1))
        else
            failed_checks=$((failed_checks + 1))
        fi
    else
        error "Xenon não instalado. Instale com: pip install xenon"
        failed_checks=$((failed_checks + 1))
    fi
    
    echo ""
    
    # 5. VERIFICAÇÕES DE TESTES
    log "🧪 VERIFICAÇÕES DE TESTES"
    echo "----------------------"
    
    # Pytest
    if check_command "pytest"; then
        total_checks=$((total_checks + 1))
        if run_check "Pytest - Execução de testes" "pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=95"; then
            passed_checks=$((passed_checks + 1))
        else
            failed_checks=$((failed_checks + 1))
        fi
    else
        error "Pytest não instalado. Instale com: pip install pytest pytest-cov"
        failed_checks=$((failed_checks + 1))
    fi
    
    echo ""
    
    # 6. VERIFICAÇÕES DE CONFIGURAÇÃO
    log "⚙️ VERIFICAÇÕES DE CONFIGURAÇÃO"
    echo "----------------------------"
    
    # Pre-commit
    if check_file ".pre-commit-config.yaml"; then
        total_checks=$((total_checks + 1))
        if check_command "pre-commit"; then
            if run_check "Pre-commit - Configuração de hooks" "pre-commit run --all-files"; then
                passed_checks=$((passed_checks + 1))
            else
                failed_checks=$((failed_checks + 1))
            fi
        else
            warning "Pre-commit não instalado. Instale com: pip install pre-commit"
            failed_checks=$((failed_checks + 1))
        fi
    else
        warning "Arquivo .pre-commit-config.yaml não encontrado"
        failed_checks=$((failed_checks + 1))
    fi
    
    # GitHub Workflows
    if check_directory ".github/workflows"; then
        total_checks=$((total_checks + 1))
        if [ -f ".github/workflows/quality-pipeline.yml" ]; then
            success "GitHub Workflow de qualidade encontrado"
            passed_checks=$((passed_checks + 1))
        else
            warning "GitHub Workflow de qualidade não encontrado"
            failed_checks=$((failed_checks + 1))
        fi
    else
        warning "Diretório .github/workflows não encontrado"
        failed_checks=$((failed_checks + 1))
    fi
    
    echo ""
    
    # 7. VERIFICAÇÕES DE DOCUMENTAÇÃO
    log "📚 VERIFICAÇÕES DE DOCUMENTAÇÃO"
    echo "----------------------------"
    
    # README
    if check_file "README.md"; then
        total_checks=$((total_checks + 1))
        if grep -q "## 🌟 \*\*VISÃO GERAL\*\*" README.md; then
            success "README.md contém seções obrigatórias"
            passed_checks=$((passed_checks + 1))
        else
            warning "README.md não contém seções obrigatórias"
            failed_checks=$((failed_checks + 1))
        fi
    else
        error "README.md não encontrado"
        failed_checks=$((failed_checks + 1))
    fi
    
    # Documentação de qualidade
    if check_file "docs/FRAMEWORK_QUALIDADE_SOFTWARE.md"; then
        total_checks=$((total_checks + 1))
        success "Documentação de qualidade encontrada"
        passed_checks=$((passed_checks + 1))
    else
        warning "Documentação de qualidade não encontrada"
        failed_checks=$((failed_checks + 1))
    fi
    
    echo ""
    
    # RELATÓRIO FINAL
    echo "=================================================="
    echo "📊 RELATÓRIO FINAL DE QUALIDADE"
    echo "=================================================="
    echo ""
    
    local success_rate=$((passed_checks * 100 / total_checks))
    
    echo "✅ Verificações Passou: $passed_checks/$total_checks"
    echo "❌ Verificações Falhou: $failed_checks/$total_checks"
    echo "📈 Taxa de Sucesso: $success_rate%"
    echo ""
    
    if [ $success_rate -ge 90 ]; then
        success "🎉 EXCELENTE! Qualidade de software está em nível enterprise"
        echo ""
        echo "📋 Próximos passos recomendados:"
        echo "   - Manter qualidade atual"
        echo "   - Implementar melhorias contínuas"
        echo "   - Monitorar métricas regularmente"
        exit 0
    elif [ $success_rate -ge 70 ]; then
        warning "⚠️ BOM! Qualidade de software está boa, mas pode melhorar"
        echo ""
        echo "📋 Ações recomendadas:"
        echo "   - Corrigir verificações que falharam"
        echo "   - Implementar ferramentas faltantes"
        echo "   - Melhorar configurações"
        exit 1
    else
        error "❌ CRÍTICO! Qualidade de software precisa de atenção imediata"
        echo ""
        echo "📋 Ações críticas:"
        echo "   - Instalar ferramentas de qualidade"
        echo "   - Configurar pipeline de qualidade"
        echo "   - Implementar testes básicos"
        echo "   - Corrigir problemas de segurança"
        exit 2
    fi
}

# Função para mostrar ajuda
show_help() {
    echo "🔍 COINBALANCE - VERIFICAÇÃO DE QUALIDADE DE SOFTWARE"
    echo ""
    echo "Uso: $0 [OPÇÕES]"
    echo ""
    echo "Opções:"
    echo "  -h, --help     Mostra esta ajuda"
    echo "  -v, --verbose  Modo verboso (mostra output completo)"
    echo "  -q, --quiet    Modo silencioso (apenas erros)"
    echo ""
    echo "Exemplos:"
    echo "  $0              # Executa todas as verificações"
    echo "  $0 --verbose    # Executa com output detalhado"
    echo "  $0 --quiet      # Executa silenciosamente"
    echo ""
    echo "Ferramentas necessárias:"
    echo "  pip install black isort flake8 mypy pylint bandit safety radon xenon pytest pytest-cov pre-commit"
}

# Função para modo verboso
run_verbose() {
    log "Executando em modo verboso..."
    # Redireciona output para mostrar tudo
    exec 1>&2
    main
}

# Função para modo silencioso
run_quiet() {
    log "Executando em modo silencioso..."
    # Redireciona output para /dev/null exceto erros
    exec 1>/dev/null
    main
}

# Processar argumentos
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    -v|--verbose)
        run_verbose
        ;;
    -q|--quiet)
        run_quiet
        ;;
    "")
        main
        ;;
    *)
        error "Opção desconhecida: $1"
        show_help
        exit 1
        ;;
esac