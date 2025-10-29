#!/bin/bash

# Script de Migração do Frontend para Repositório Separado
# Este script automatiza o processo de migração do frontend

set -e  # Sair em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para imprimir mensagens
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se estamos no diretório correto
if [ ! -d "frontend" ]; then
    error "Diretório 'frontend' não encontrado. Execute este script da raiz do projeto."
    exit 1
fi

info "Iniciando migração do frontend para repositório separado..."

# Diretório de destino
DEST_DIR="../coinbalance-frontend"

# Criar diretório de destino se não existir
if [ ! -d "$DEST_DIR" ]; then
    info "Criando diretório de destino: $DEST_DIR"
    mkdir -p "$DEST_DIR"
fi

# 1. Copiar estrutura do frontend
info "Copiando arquivos do frontend..."
cp -r frontend/* "$DEST_DIR/"

# 2. Copiar documentação específica do frontend
info "Copiando documentação..."
if [ -d "docs/frontend" ]; then
    mkdir -p "$DEST_DIR/docs"
    cp -r docs/frontend/* "$DEST_DIR/docs/"
fi

# Copiar outros arquivos de documentação
if [ -f "docs/MANUAL_INTEGRACAO_FRONTEND.md" ]; then
    cp docs/MANUAL_INTEGRACAO_FRONTEND.md "$DEST_DIR/docs/"
fi

if [ -f "FRONTEND_COMPLETO.md" ]; then
    cp FRONTEND_COMPLETO.md "$DEST_DIR/docs/"
fi

# 3. Copiar arquivos de template
info "Copiando arquivos de template..."
if [ -f "docs/TEMPLATE_README_FRONTEND.md" ]; then
    cp docs/TEMPLATE_README_FRONTEND.md "$DEST_DIR/README.md"
fi

if [ -f "docs/TEMPLATE_GITIGNORE_FRONTEND.md" ]; then
    cp docs/TEMPLATE_GITIGNORE_FRONTEND.md "$DEST_DIR/.gitignore"
fi

if [ -f "docs/TEMPLATE_DOCKERFILE_FRONTEND.md" ]; then
    cp docs/TEMPLATE_DOCKERFILE_FRONTEND.md "$DEST_DIR/Dockerfile"
fi

if [ -f "docs/TEMPLATE_DOCKER_COMPOSE_FRONTEND.md" ]; then
    cp docs/TEMPLATE_DOCKER_COMPOSE_FRONTEND.md "$DEST_DIR/docker-compose.yml"
fi

# 4. Criar .github/workflows se necessário
info "Configurando CI/CD..."
mkdir -p "$DEST_DIR/.github/workflows"
if [ -f "docs/TEMPLATE_GITHUB_ACTIONS.yml" ]; then
    cp docs/TEMPLATE_GITHUB_ACTIONS.yml "$DEST_DIR/.github/workflows/ci.yml"
fi

# 5. Criar arquivo .env.example se não existir
if [ ! -f "$DEST_DIR/.env.example" ]; then
    info "Criando .env.example..."
    cat > "$DEST_DIR/.env.example" << 'EOF'
# API Backend URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# API Version (opcional)
NEXT_PUBLIC_API_VERSION=v1

# JWT Storage Key (opcional)
NEXT_PUBLIC_JWT_STORAGE_KEY=authToken
EOF
fi

# 6. Atualizar package.json (se necessário)
info "Verificando package.json..."
if [ -f "$DEST_DIR/package.json" ]; then
    # Adicionar campos de repositório se não existirem
    if ! grep -q '"repository"' "$DEST_DIR/package.json"; then
        warn "package.json não tem campo 'repository'. Adicione manualmente."
    fi
fi

# 7. Criar CONTRIBUTING.md se não existir
if [ ! -f "$DEST_DIR/CONTRIBUTING.md" ]; then
    info "Criando CONTRIBUTING.md..."
    cat > "$DEST_DIR/CONTRIBUTING.md" << 'EOF'
# Contribuindo

Obrigado por considerar contribuir para o CoinBalance Frontend!

## Como Contribuir

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas mudanças (`git commit -m 'feat: adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Padrões de Código

- Siga os padrões de código definidos no ESLint
- Escreva testes para novas funcionalidades
- Mantenha a documentação atualizada

## Commits

Use o formato Conventional Commits:

- `feat:` para novas funcionalidades
- `fix:` para correções de bugs
- `docs:` para mudanças na documentação
- `style:` para formatação
- `refactor:` para refatorações
- `test:` para testes
- `chore:` para tarefas de manutenção
EOF
fi

# 8. Criar LICENSE.md se não existir
if [ ! -f "$DEST_DIR/LICENSE.md" ]; then
    warn "LICENSE.md não encontrado. Copie do repositório principal se necessário."
fi

# 9. Verificar se há node_modules (não deve copiar)
if [ -d "$DEST_DIR/node_modules" ]; then
    warn "Removendo node_modules (será reinstalado)..."
    rm -rf "$DEST_DIR/node_modules"
fi

# 10. Verificar se há .next (não deve copiar)
if [ -d "$DEST_DIR/.next" ]; then
    warn "Removendo .next (será reconstruído)..."
    rm -rf "$DEST_DIR/.next"
fi

info "Migração concluída!"
info ""
info "Próximos passos:"
info "1. cd $DEST_DIR"
info "2. git init"
info "3. git remote add origin <URL_DO_REPOSITORIO>"
info "4. npm install"
info "5. npm run build (para verificar)"
info "6. git add ."
info "7. git commit -m 'feat: migração inicial do frontend'"
info "8. git push -u origin main"
info ""
warn "Lembre-se de:"
warn "- Atualizar README.md com informações específicas"
warn "- Configurar secrets no GitHub Actions"
warn "- Atualizar repositório backend removendo frontend/"
warn "- Atualizar README.md do backend"

echo ""
info "Migração concluída com sucesso!"

