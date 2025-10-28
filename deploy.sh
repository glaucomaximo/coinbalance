#!/bin/bash
# CoinBalance Web3 Production Deploy Script

set -e

echo "🚀 Iniciando deploy do CoinBalance Web3..."

# Verificar se está no diretório correto
if [ ! -f "main.py" ]; then
    echo "❌ Execute este script no diretório raiz do projeto"
    exit 1
fi

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose -f docker-compose.production.yml down

# Construir nova imagem
echo "🔨 Construindo nova imagem..."
docker-compose -f docker-compose.production.yml build --no-cache

# Iniciar serviços
echo "▶️ Iniciando serviços..."
docker-compose -f docker-compose.production.yml up -d

# Aguardar saúde dos serviços
echo "⏳ Aguardando serviços ficarem saudáveis..."
sleep 30

# Verificar saúde
echo "🏥 Verificando saúde dos serviços..."
curl -f http://localhost:8001/health/live || {
    echo "❌ Serviço não está saudável"
    docker-compose -f docker-compose.production.yml logs
    exit 1
}

echo "✅ Deploy concluído com sucesso!"
echo "🌐 Aplicação disponível em: https://coinbalance.com"
echo "📊 Métricas disponíveis em: http://localhost:9090"
