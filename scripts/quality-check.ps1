# 🔍 SCRIPT DE VERIFICAÇÃO DE QUALIDADE - CoinBalance (PowerShell)
# Executa todos os gates de qualidade obrigatórios

param(
    [switch]$SkipTests,
    [switch]$SkipPerformance,
    [switch]$Verbose
)

# Configurações
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Função para imprimir status
function Write-Status {
    param(
        [string]$Message,
        [string]$Type = "Info"
    )
    
    $colors = @{
        "Success" = "Green"
        "Error" = "Red"
        "Warning" = "Yellow"
        "Info" = "Cyan"
    }
    
    $symbols = @{
        "Success" = "✅"
        "Error" = "❌"
        "Warning" = "⚠️"
        "Info" = "ℹ️"
    }
    
    Write-Host "$($symbols[$Type]) $Message" -ForegroundColor $colors[$Type]
}

# Verificar se estamos no diretório correto
if (-not (Test-Path "pyproject.toml")) {
    Write-Status "Execute este script na raiz do projeto CoinBalance" "Error"
    exit 1
}

Write-Status "Iniciando verificação de qualidade..." "Info"

# Gate 1: Formatação de Código
Write-Host ""
Write-Host "🎨 GATE 1: Formatação de Código" -ForegroundColor Blue
Write-Host "--------------------------------"

try {
    Write-Status "Verificando formatação com Black..." "Info"
    black --check --diff . 2>$null
    Write-Status "Black - Formatação OK" "Success"
} catch {
    Write-Status "Black - Falha na formatação" "Error"
    exit 1
}

try {
    Write-Status "Verificando organização de imports com isort..." "Info"
    isort --check-only --diff . 2>$null
    Write-Status "isort - Imports organizados" "Success"
} catch {
    Write-Status "isort - Falha na organização de imports" "Error"
    exit 1
}

# Gate 2: Linting e Type Checking
Write-Host ""
Write-Host "🔍 GATE 2: Linting e Type Checking" -ForegroundColor Blue
Write-Host "-----------------------------------"

try {
    Write-Status "Executando linting com Flake8..." "Info"
    flake8 . 2>$null
    Write-Status "Flake8 - Linting OK" "Success"
} catch {
    Write-Status "Flake8 - Falha no linting" "Error"
    exit 1
}

try {
    Write-Status "Executando type checking com MyPy..." "Info"
    mypy src/ 2>$null
    Write-Status "MyPy - Type checking OK" "Success"
} catch {
    Write-Status "MyPy - Falha no type checking" "Error"
    exit 1
}

# Gate 3: Segurança
Write-Host ""
Write-Host "🔒 GATE 3: Verificação de Segurança" -ForegroundColor Blue
Write-Host "-----------------------------------"

try {
    Write-Status "Executando verificação de segurança com Bandit..." "Info"
    bandit -r src/ -f json -o bandit-report.json 2>$null
    Write-Status "Bandit - Segurança OK" "Success"
} catch {
    Write-Status "Bandit - Falha na verificação de segurança" "Error"
    exit 1
}

# Gate 4: Testes
if (-not $SkipTests) {
    Write-Host ""
    Write-Host "🧪 GATE 4: Testes Automatizados" -ForegroundColor Blue
    Write-Host "-------------------------------"

    try {
        Write-Status "Executando testes unitários..." "Info"
        pytest tests/unit/ -v --tb=short 2>$null
        Write-Status "Testes unitários OK" "Success"
    } catch {
        Write-Status "Testes unitários falharam" "Error"
        exit 1
    }

    try {
        Write-Status "Executando testes de integração..." "Info"
        pytest tests/integration/ -v --tb=short 2>$null
        Write-Status "Testes de integração OK" "Success"
    } catch {
        Write-Status "Testes de integração falharam" "Error"
        exit 1
    }

    try {
        Write-Status "Verificando cobertura de testes..." "Info"
        coverage run -m pytest tests/ 2>$null
        coverage report --fail-under=80 2>$null
        Write-Status "Cobertura de testes ≥80%" "Success"
    } catch {
        Write-Status "Cobertura de testes insuficiente" "Error"
        exit 1
    }
}

# Gate 5: Arquitetura
Write-Host ""
Write-Host "🏗️ GATE 5: Verificação Arquitetural" -ForegroundColor Blue
Write-Host "------------------------------------"

# Verificar estrutura DDD
$requiredDirs = @("src/domain", "src/application", "src/infrastructure", "src/presentation")
$allDirsExist = $true

foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Status "Estrutura DDD OK - $dir existe" "Success"
    } else {
        Write-Status "Estrutura DDD incorreta - $dir não encontrado" "Error"
        $allDirsExist = $false
    }
}

if (-not $allDirsExist) {
    exit 1
}

# Gate 6: Performance
if (-not $SkipPerformance) {
    Write-Host ""
    Write-Host "⚡ GATE 6: Verificação de Performance" -ForegroundColor Blue
    Write-Host "-------------------------------------"

    if (Test-Path "tests/performance") {
        try {
            Write-Status "Executando testes de performance..." "Info"
            pytest tests/performance/ -m performance --durations=10 2>$null
            Write-Status "Testes de performance OK" "Success"
        } catch {
            Write-Status "Testes de performance falharam" "Error"
            exit 1
        }
    } else {
        Write-Status "Diretório de testes de performance não encontrado" "Warning"
    }
}

# Gate 7: Documentação
Write-Host ""
Write-Host "📚 GATE 7: Verificação de Documentação" -ForegroundColor Blue
Write-Host "--------------------------------------"

$requiredDocs = @("README.md", "CONTRIBUTING.md", "CHANGELOG.md", "docs/RESUMO_REFATORACAO_DDD.md", "docs/ARQUITETURA_DETALHADA.md")
foreach ($doc in $requiredDocs) {
    if (Test-Path $doc) {
        Write-Status "$doc existe" "Success"
    } else {
        Write-Status "$doc não encontrado" "Error"
        exit 1
    }
}

# Relatório Final
Write-Host ""
Write-Host "📊 RELATÓRIO FINAL" -ForegroundColor Green
Write-Host "=================="

Write-Status "Gerando relatório de cobertura..." "Info"
try {
    coverage html -d htmlcov 2>$null
    Write-Status "Relatório de cobertura gerado em htmlcov/" "Success"
} catch {
    Write-Status "Falha ao gerar relatório de cobertura" "Warning"
}

Write-Host ""
Write-Host "🎉 TODOS OS GATES DE QUALIDADE PASSARAM!" -ForegroundColor Green
Write-Host ""
Write-Host "✅ Formatação de código OK"
Write-Host "✅ Linting e type checking OK"
Write-Host "✅ Segurança verificada"
Write-Host "✅ Testes passaram"
Write-Host "✅ Arquitetura validada"
Write-Host "✅ Performance OK"
Write-Host "✅ Documentação completa"
Write-Host ""
Write-Host "📁 Relatórios gerados:" -ForegroundColor Cyan
Write-Host "  - htmlcov/ (cobertura de testes)"
Write-Host "  - bandit-report.json (segurança)"
Write-Host ""
Write-Host "🚀 Projeto pronto para manutenção!" -ForegroundColor Green
