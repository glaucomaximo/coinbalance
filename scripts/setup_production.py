"""
Configuração de Produção para CoinBalance Web3
Configurações otimizadas para ambiente de produção
"""

import os
from pathlib import Path

# Configurações de Produção
PRODUCTION_CONFIG = {
    # Segurança
    "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY", "CHANGE_ME_IN_PRODUCTION"),
    "COINBALANCE_MASTER_KEY": os.getenv("COINBALANCE_MASTER_KEY", "CHANGE_ME_IN_PRODUCTION"),
    "CORS_ORIGINS": os.getenv("CORS_ORIGINS", '["https://coinbalance.com", "https://www.coinbalance.com"]'),
    
    # Database
    "DATABASE_URL": os.getenv("DATABASE_URL", "sqlite:///./coinbalance_prod.db"),
    "DATABASE_POOL_SIZE": int(os.getenv("DATABASE_POOL_SIZE", "20")),
    "DATABASE_MAX_OVERFLOW": int(os.getenv("DATABASE_MAX_OVERFLOW", "30")),
    
    # Web3
    "WEB3_PROVIDER_URL": os.getenv("WEB3_PROVIDER_URL", "https://mainnet.infura.io/v3/YOUR_PROJECT_ID"),
    "WEB3_PRIVATE_KEY": os.getenv("WEB3_PRIVATE_KEY", ""),
    "WEB3_GAS_LIMIT": int(os.getenv("WEB3_GAS_LIMIT", "21000")),
    "WEB3_GAS_PRICE": int(os.getenv("WEB3_GAS_PRICE", "20")),
    
    # Blockchain Networks
    "ETHEREUM_RPC_URL": os.getenv("ETHEREUM_RPC_URL", "https://mainnet.infura.io/v3/YOUR_PROJECT_ID"),
    "POLYGON_RPC_URL": os.getenv("POLYGON_RPC_URL", "https://polygon-rpc.com"),
    "BSC_RPC_URL": os.getenv("BSC_RPC_URL", "https://bsc-dataseed.binance.org"),
    "AVALANCHE_RPC_URL": os.getenv("AVALANCHE_RPC_URL", "https://api.avax.network/ext/bc/C/rpc"),
    
    # Performance
    "WORKER_COUNT": int(os.getenv("WORKER_COUNT", "4")),
    "MAX_CONNECTIONS": int(os.getenv("MAX_CONNECTIONS", "1000")),
    "TIMEOUT": int(os.getenv("TIMEOUT", "30")),
    
    # Cache
    "CACHE_SIZE": os.getenv("CACHE_SIZE", "1GB"),
    "CACHE_TTL": int(os.getenv("CACHE_TTL", "3600")),
    
    # Monitoring
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
    "ENABLE_METRICS": os.getenv("ENABLE_METRICS", "true").lower() == "true",
    "METRICS_PORT": int(os.getenv("METRICS_PORT", "9090")),
    
    # Rate Limiting
    "RATE_LIMIT_REQUESTS": int(os.getenv("RATE_LIMIT_REQUESTS", "1000")),
    "RATE_LIMIT_WINDOW": int(os.getenv("RATE_LIMIT_WINDOW", "3600")),
    
    # Security
    "ENABLE_HTTPS": os.getenv("ENABLE_HTTPS", "true").lower() == "true",
    "SSL_CERT_PATH": os.getenv("SSL_CERT_PATH", ""),
    "SSL_KEY_PATH": os.getenv("SSL_KEY_PATH", ""),
    
    # Backup
    "BACKUP_ENABLED": os.getenv("BACKUP_ENABLED", "true").lower() == "true",
    "BACKUP_INTERVAL": int(os.getenv("BACKUP_INTERVAL", "86400")),  # 24 hours
    "BACKUP_RETENTION": int(os.getenv("BACKUP_RETENTION", "7")),  # 7 days
}

def create_production_env():
    """Cria arquivo .env para produção"""
    env_content = "# CoinBalance Web3 Production Environment\n"
    env_content += "# Generated automatically - DO NOT COMMIT TO VERSION CONTROL\n\n"
    
    for key, value in PRODUCTION_CONFIG.items():
        if isinstance(value, str) and not value.startswith('['):
            env_content += f"{key}=\"{value}\"\n"
        else:
            env_content += f"{key}={value}\n"
    
    env_content += "\n# Additional Production Settings\n"
    env_content += "ENVIRONMENT=production\n"
    env_content += "DEBUG=false\n"
    env_content += "RELOAD=false\n"
    
    with open(".env.production", "w") as f:
        f.write(env_content)
    
    print("✅ Arquivo .env.production criado com sucesso!")

def create_docker_compose_prod():
    """Cria docker-compose para produção"""
    docker_compose = """
version: '3.8'

services:
  coinbalance-web3:
    build:
      context: .
      dockerfile: Dockerfile.production
    ports:
      - "8001:8001"
      - "9090:9090"  # Metrics
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://coinbalance:${DB_PASSWORD}@postgres:5432/coinbalance_prod
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env.production
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3
    volumes:
      - ./logs:/app/logs
      - ./backups:/app/backups

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=coinbalance_prod
      - POSTGRES_USER=coinbalance
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U coinbalance"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - coinbalance-web3
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
"""
    
    with open("docker-compose.production.yml", "w") as f:
        f.write(docker_compose)
    
    print("✅ Arquivo docker-compose.production.yml criado com sucesso!")

def create_nginx_config():
    """Cria configuração do Nginx"""
    nginx_config = """
events {
    worker_connections 1024;
}

http {
    upstream coinbalance_backend {
        server coinbalance-web3:8001;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=web3:10m rate=5r/s;

    server {
        listen 80;
        server_name coinbalance.com www.coinbalance.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name coinbalance.com www.coinbalance.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # API endpoints
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://coinbalance_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_timeout 30s;
        }

        # Web3 endpoints (higher rate limit)
        location /api/v1/web3/ {
            limit_req zone=web3 burst=10 nodelay;
            proxy_pass http://coinbalance_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_timeout 60s;
        }

        # Health check
        location /health/ {
            proxy_pass http://coinbalance_backend;
            access_log off;
        }

        # Static files
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
"""
    
    os.makedirs("nginx", exist_ok=True)
    with open("nginx/nginx.conf", "w") as f:
        f.write(nginx_config)
    
    print("✅ Configuração do Nginx criada com sucesso!")

def create_dockerfile_production():
    """Cria Dockerfile para produção"""
    dockerfile = """
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Create necessary directories
RUN mkdir -p logs backups

# Expose ports
EXPOSE 8001 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8001/health/live || exit 1

# Run the application
CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"]
"""
    
    with open("Dockerfile.production", "w") as f:
        f.write(dockerfile)
    
    print("✅ Dockerfile.production criado com sucesso!")

def create_production_scripts():
    """Cria scripts para produção"""
    
    # Script de deploy
    deploy_script = """#!/bin/bash
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
"""
    
    with open("deploy.sh", "w", encoding="utf-8") as f:
        f.write(deploy_script)
    
    # Tornar executável (apenas no Unix/Linux)
    if os.name != 'nt':
        os.chmod("deploy.sh", 0o755)
    
    # Script de backup
    backup_script = """#!/bin/bash
# CoinBalance Web3 Backup Script

set -e

BACKUP_DIR="/app/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="coinbalance_backup_${TIMESTAMP}.sql"

echo "💾 Iniciando backup do banco de dados..."

# Criar backup do PostgreSQL
docker-compose -f docker-compose.production.yml exec -T postgres \\
    pg_dump -U coinbalance coinbalance_prod > "${BACKUP_DIR}/${BACKUP_FILE}"

# Comprimir backup
gzip "${BACKUP_DIR}/${BACKUP_FILE}"

# Remover backups antigos (manter apenas últimos 7 dias)
find "${BACKUP_DIR}" -name "coinbalance_backup_*.sql.gz" -mtime +7 -delete

echo "✅ Backup concluído: ${BACKUP_FILE}.gz"
"""
    
    with open("backup.sh", "w", encoding="utf-8") as f:
        f.write(backup_script)
    
    # Tornar executável (apenas no Unix/Linux)
    if os.name != 'nt':
        os.chmod("backup.sh", 0o755)
    
    print("✅ Scripts de produção criados com sucesso!")

if __name__ == "__main__":
    print("🏗️ Configurando ambiente de produção para CoinBalance Web3...")
    
    create_production_env()
    create_docker_compose_prod()
    create_nginx_config()
    create_dockerfile_production()
    create_production_scripts()
    
    print("\n🎉 Configuração de produção concluída!")
    print("\n📋 Próximos passos:")
    print("1. Configure as variáveis de ambiente em .env.production")
    print("2. Configure certificados SSL em nginx/ssl/")
    print("3. Execute: ./deploy.sh")
    print("4. Configure backup automático: crontab -e")
    print("5. Monitore logs: docker-compose -f docker-compose.production.yml logs -f")
