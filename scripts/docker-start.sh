#!/usr/bin/env bash
# Script de inicialização Docker para CoinBalance
# ================================================

set -e

echo "🐳 Iniciando CoinBalance no Docker..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env a partir de .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "⚠️  Arquivo .env criado. Por favor, configure as variáveis de ambiente antes de continuar."
        echo "   Especialmente as chaves de segurança (SECRET_KEY, JWT_SECRET_KEY, etc.)"
    else
        echo "⚠️  Arquivo .env.example não encontrado. Criando .env básico..."
        cat > .env << EOF
ENVIRONMENT=development
DEBUG=false
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production
ENCRYPTION_KEY=dev-encryption-key-change-in-production
COINBALANCE_MASTER_KEY=dev-master-key-change-in-production
DATABASE_URL=sqlite:///./data/blockchain.db
REDIS_URL=redis://redis:6379/0
LOG_LEVEL=info
EOF
    fi
fi

# Criar diretórios necessários
echo "📁 Criando diretórios necessários..."
mkdir -p data backups logs

# Construir imagens
echo "🔨 Construindo imagens Docker..."
docker-compose build --no-cache coinbalance

# Iniciar serviços
echo "🚀 Iniciando serviços..."
docker-compose up -d

# Aguardar serviços ficarem prontos
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 10

# Verificar saúde dos serviços
echo "🏥 Verificando saúde dos serviços..."
docker-compose ps

# Verificar logs
echo "📋 Últimas linhas dos logs:"
docker-compose logs --tail=20 coinbalance

echo ""
echo "✅ CoinBalance iniciado com sucesso!"
echo ""
echo "📊 Serviços disponíveis:"
echo "   - API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Prometheus: http://localhost:9090"
echo "   - Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo "Para ver os logs: docker-compose logs -f coinbalance"
echo "Para parar: docker-compose down"

