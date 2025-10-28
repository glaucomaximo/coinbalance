# 🚀 GUIA DE DEPLOY OTIMIZADO - COINBALANCE BLOCKCHAIN

## 🎯 **VISÃO GERAL**

Este guia fornece instruções completas para deploy otimizado do CoinBalance Blockchain em ambientes de produção, incluindo configurações de performance, segurança e monitoramento.

---

## 📋 **PRÉ-REQUISITOS**

### **Requisitos de Sistema**

#### **Mínimo**
- **CPU:** 2 cores (2.0 GHz)
- **RAM:** 4 GB
- **Disco:** 50 GB SSD
- **Rede:** 100 Mbps
- **OS:** Linux (Ubuntu 20.04+), macOS, Windows

#### **Recomendado**
- **CPU:** 8 cores (3.0 GHz)
- **RAM:** 16 GB
- **Disco:** 200 GB NVMe SSD
- **Rede:** 1 Gbps
- **OS:** Linux (Ubuntu 22.04 LTS)

#### **Enterprise**
- **CPU:** 16+ cores (3.5 GHz)
- **RAM:** 64+ GB
- **Disco:** 1 TB NVMe SSD
- **Rede:** 10 Gbps
- **OS:** Linux (Ubuntu 22.04 LTS)

### **Software Necessário**
```bash
# Python 3.11+
python3 --version

# Docker e Docker Compose
docker --version
docker-compose --version

# Git
git --version

# Node.js (para frontend futuro)
node --version
npm --version
```

---

## 🔧 **CONFIGURAÇÃO DO AMBIENTE**

### **1. Clonagem do Repositório**
```bash
git clone https://github.com/coinbalance/coinbalance.git
cd coinbalance
```

### **2. Configuração de Variáveis de Ambiente**

#### **Arquivo `.env` (Desenvolvimento)**
```bash
# Segurança
JWT_SECRET_KEY=dev-secret-key-change-in-production
MASTER_KEY=dev-master-key-change-in-production

# Banco de dados
DATABASE_URL=sqlite:///./coinbalance.db

# Blockchain
BLOCKCHAIN_NAME=CoinBalance
TARGET_BLOCK_TIME=10.0
DIFFICULTY_ADJUSTMENT_INTERVAL=10

# Cache
CACHE_TTL=3600
MAX_CACHE_SIZE=10000
DISTRIBUTED_CACHE_ENABLED=true

# Rede
MAX_CONNECTIONS=100
CONNECTION_TIMEOUT=30
COMPRESSION_ENABLED=true

# Monitoramento
MONITORING_ENABLED=true
LOG_LEVEL=INFO
AUDIT_LOGGING=true

# LGPD
LGPD_COMPLIANCE=true
DATA_RETENTION_DAYS=365
```

#### **Arquivo `production.env` (Produção)**
```bash
# Segurança (GERAR CHAVES SEGURAS)
JWT_SECRET_KEY=$(openssl rand -base64 64)
MASTER_KEY=$(openssl rand -base64 64)

# Banco de dados
DATABASE_URL=postgresql://user:password@localhost:5432/coinbalance

# Blockchain
BLOCKCHAIN_NAME=CoinBalance-Production
TARGET_BLOCK_TIME=10.0
DIFFICULTY_ADJUSTMENT_INTERVAL=10

# Cache
CACHE_TTL=7200
MAX_CACHE_SIZE=50000
DISTRIBUTED_CACHE_ENABLED=true

# Rede
MAX_CONNECTIONS=1000
CONNECTION_TIMEOUT=30
COMPRESSION_ENABLED=true

# Monitoramento
MONITORING_ENABLED=true
LOG_LEVEL=WARNING
AUDIT_LOGGING=true

# LGPD
LGPD_COMPLIANCE=true
DATA_RETENTION_DAYS=2555  # 7 anos

# Escalabilidade
HORIZONTAL_SCALING_ENABLED=true
MAX_SHARDS=16
AUTO_SCALING_ENABLED=true

# Performance
PARALLEL_MINING_ENABLED=true
MAX_MINING_THREADS=16
INCREMENTAL_VALIDATION_ENABLED=true
```

### **3. Instalação de Dependências**

#### **Desenvolvimento**
```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt
```

#### **Produção**
```bash
# Usar Docker (recomendado)
docker build -t coinbalance:latest .

# Ou instalação direta
pip install -r requirements.txt --no-cache-dir
```

---

## 🐳 **DEPLOY COM DOCKER**

### **1. Dockerfile Otimizado**

#### **Dockerfile.production**
```dockerfile
# Multi-stage build para otimização
FROM python:3.11-slim as builder

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN groupadd -r coinbalance && useradd -r -g coinbalance coinbalance

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage de produção
FROM python:3.11-slim

# Instalar dependências mínimas
RUN apt-get update && apt-get install -y \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário
RUN groupadd -r coinbalance && useradd -r -g coinbalance coinbalance

# Copiar dependências do builder
COPY --from=builder /root/.local /home/coinbalance/.local

# Definir diretório de trabalho
WORKDIR /app

# Copiar código
COPY --chown=coinbalance:coinbalance . .

# Criar diretórios necessários
RUN mkdir -p /app/logs /app/data /app/backups && \
    chown -R coinbalance:coinbalance /app

# Configurar PATH
ENV PATH=/home/coinbalance/.local/bin:$PATH

# Mudar para usuário não-root
USER coinbalance

# Expor porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Comando de inicialização
CMD ["python", "main.py"]
```

### **2. Docker Compose para Produção**

#### **docker-compose.production.yml**
```yaml
version: '3.8'

services:
  coinbalance:
    build:
      context: .
      dockerfile: Dockerfile.production
    container_name: coinbalance-prod
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://coinbalance:${DB_PASSWORD}@postgres:5432/coinbalance
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - MASTER_KEY=${MASTER_KEY}
      - LOG_LEVEL=WARNING
      - MONITORING_ENABLED=true
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./backups:/app/backups
    depends_on:
      - postgres
      - redis
    networks:
      - coinbalance-network
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 8G
        reservations:
          cpus: '2.0'
          memory: 4G

  postgres:
    image: postgres:15-alpine
    container_name: coinbalance-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_DB=coinbalance
      - POSTGRES_USER=coinbalance
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    networks:
      - coinbalance-network
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G

  redis:
    image: redis:7-alpine
    container_name: coinbalance-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 2gb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - coinbalance-network
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G

  nginx:
    image: nginx:alpine
    container_name: coinbalance-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - coinbalance
    networks:
      - coinbalance-network

  prometheus:
    image: prom/prometheus:latest
    container_name: coinbalance-prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    networks:
      - coinbalance-network

  grafana:
    image: grafana/grafana:latest
    container_name: coinbalance-grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    networks:
      - coinbalance-network

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:

networks:
  coinbalance-network:
    driver: bridge
```

### **3. Scripts de Deploy**

#### **deploy.sh**
```bash
#!/bin/bash

set -e

echo "🚀 Iniciando deploy do CoinBalance Blockchain..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado"
    exit 1
fi

# Verificar se arquivo .env existe
if [ ! -f "production.env" ]; then
    echo "❌ Arquivo production.env não encontrado"
    echo "📝 Copie production.env.example para production.env e configure as variáveis"
    exit 1
fi

# Carregar variáveis de ambiente
export $(cat production.env | xargs)

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose -f docker-compose.production.yml down

# Remover imagens antigas
echo "🗑️ Removendo imagens antigas..."
docker image prune -f

# Build da nova imagem
echo "🔨 Construindo nova imagem..."
docker-compose -f docker-compose.production.yml build --no-cache

# Iniciar serviços
echo "🚀 Iniciando serviços..."
docker-compose -f docker-compose.production.yml up -d

# Aguardar serviços ficarem prontos
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 30

# Verificar saúde dos serviços
echo "🏥 Verificando saúde dos serviços..."
docker-compose -f docker-compose.production.yml ps

# Testar endpoint de saúde
echo "🔍 Testando endpoint de saúde..."
curl -f http://localhost:8000/api/v1/health || {
    echo "❌ Falha no teste de saúde"
    docker-compose -f docker-compose.production.yml logs coinbalance
    exit 1
}

echo "✅ Deploy concluído com sucesso!"
echo "🌐 Aplicação disponível em: http://localhost:8000"
echo "📊 Grafana disponível em: http://localhost:3000"
echo "📈 Prometheus disponível em: http://localhost:9090"
```

#### **backup.sh**
```bash
#!/bin/bash

set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="coinbalance_backup_${TIMESTAMP}.tar.gz"

echo "💾 Iniciando backup do CoinBalance..."

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# Backup do banco de dados
echo "🗄️ Fazendo backup do banco de dados..."
docker-compose -f docker-compose.production.yml exec postgres pg_dump -U coinbalance coinbalance > $BACKUP_DIR/database_${TIMESTAMP}.sql

# Backup dos dados da aplicação
echo "📁 Fazendo backup dos dados da aplicação..."
tar -czf $BACKUP_DIR/$BACKUP_FILE \
    --exclude='./backups' \
    --exclude='./logs' \
    --exclude='./.git' \
    --exclude='./venv' \
    --exclude='./__pycache__' \
    .

echo "✅ Backup concluído: $BACKUP_DIR/$BACKUP_FILE"

# Limpar backups antigos (manter últimos 7 dias)
echo "🧹 Limpando backups antigos..."
find $BACKUP_DIR -name "coinbalance_backup_*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "database_*.sql" -mtime +7 -delete

echo "✅ Limpeza concluída"
```

---

## ⚙️ **CONFIGURAÇÕES DE PERFORMANCE**

### **1. Configuração do Sistema**

#### **Limites do Sistema (Linux)**
```bash
# /etc/security/limits.conf
coinbalance soft nofile 65536
coinbalance hard nofile 65536
coinbalance soft nproc 32768
coinbalance hard nproc 32768

# /etc/sysctl.conf
net.core.somaxconn = 65535
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_max_syn_backlog = 65535
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_intvl = 60
net.ipv4.tcp_keepalive_probes = 3
vm.swappiness = 10
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
```

#### **Configuração do Python**
```bash
# Variáveis de ambiente para otimização
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=random
export PYTHONPATH=/app:$PYTHONPATH

# Otimizações de memória
export MALLOC_ARENA_MAX=2
export MALLOC_MMAP_THRESHOLD_=131072
export MALLOC_TRIM_THRESHOLD_=131072
export MALLOC_TOP_PAD_=131072
export MALLOC_MMAP_MAX_=65536
```

### **2. Configuração do Banco de Dados**

#### **PostgreSQL (production.env)**
```bash
# Configurações de performance do PostgreSQL
POSTGRES_SHARED_BUFFERS=2GB
POSTGRES_EFFECTIVE_CACHE_SIZE=6GB
POSTGRES_WORK_MEM=64MB
POSTGRES_MAINTENANCE_WORK_MEM=512MB
POSTGRES_CHECKPOINT_COMPLETION_TARGET=0.9
POSTGRES_WAL_BUFFERS=16MB
POSTGRES_DEFAULT_STATISTICS_TARGET=100
POSTGRES_RANDOM_PAGE_COST=1.1
POSTGRES_EFFECTIVE_IO_CONCURRENCY=200
```

#### **Redis (redis.conf)**
```bash
# Configurações de performance do Redis
maxmemory 2gb
maxmemory-policy allkeys-lru
tcp-keepalive 60
timeout 300
save 900 1
save 300 10
save 60 10000
```

### **3. Configuração do Nginx**

#### **nginx.conf**
```nginx
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 16M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/s;

    # Upstream
    upstream coinbalance {
        server coinbalance:8000;
        keepalive 32;
    }

    # HTTP to HTTPS redirect
    server {
        listen 80;
        server_name _;
        return 301 https://$host$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name _;

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # API endpoints
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://coinbalance;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }

        # Login endpoint
        location /api/v1/auth/login {
            limit_req zone=login burst=5 nodelay;
            proxy_pass http://coinbalance;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            proxy_pass http://coinbalance/api/v1/health;
            access_log off;
        }

        # Static files (futuro)
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

---

## 📊 **MONITORAMENTO E OBSERVABILIDADE**

### **1. Configuração do Prometheus**

#### **prometheus.yml**
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'coinbalance'
    static_configs:
      - targets: ['coinbalance:8000']
    metrics_path: '/api/v1/metrics'
    scrape_interval: 10s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:9113']
```

### **2. Configuração do Grafana**

#### **Datasource (datasources.yml)**
```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

### **3. Dashboards de Monitoramento**

#### **Dashboard Principal**
- Métricas de blockchain (blocos/min, dificuldade, hash rate)
- Métricas de sistema (CPU, memória, disco, rede)
- Métricas de aplicação (requests/s, latência, erros)
- Métricas de banco de dados (conexões, queries, locks)
- Métricas de cache (hit rate, miss rate, tamanho)

#### **Alertas Configurados**
- CPU > 80% por 5 minutos
- Memória > 90% por 2 minutos
- Taxa de erro > 5% por 1 minuto
- Latência > 1s por 2 minutos
- Falhas de autenticação > 10 por minuto
- Espaço em disco < 10%

---

## 🔒 **SEGURANÇA**

### **1. Configurações de Segurança**

#### **Firewall (UFW)**
```bash
# Permitir apenas portas necessárias
ufw allow 22/tcp    # SSH
ufw allow 80/tcp     # HTTP
ufw allow 443/tcp    # HTTPS
ufw allow 3000/tcp   # Grafana (opcional)
ufw allow 9090/tcp   # Prometheus (opcional)

# Ativar firewall
ufw enable
```

#### **Fail2Ban**
```bash
# Instalar fail2ban
apt-get install fail2ban

# Configurar jail para nginx
cat > /etc/fail2ban/jail.d/nginx.conf << EOF
[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 10
EOF

# Reiniciar fail2ban
systemctl restart fail2ban
```

### **2. Certificados SSL**

#### **Let's Encrypt (Certbot)**
```bash
# Instalar certbot
apt-get install certbot python3-certbot-nginx

# Obter certificado
certbot --nginx -d yourdomain.com

# Renovação automática
echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
```

### **3. Backup de Segurança**

#### **Backup Automático**
```bash
# Crontab para backup diário
0 2 * * * /path/to/backup.sh

# Backup semanal completo
0 3 * * 0 /path/to/full-backup.sh
```

---

## 🚀 **COMANDOS DE DEPLOY**

### **Deploy Completo**
```bash
# 1. Preparar ambiente
chmod +x deploy.sh backup.sh
cp production.env.example production.env
# Editar production.env com suas configurações

# 2. Executar deploy
./deploy.sh

# 3. Verificar status
docker-compose -f docker-compose.production.yml ps
docker-compose -f docker-compose.production.yml logs -f coinbalance
```

### **Comandos Úteis**
```bash
# Ver logs
docker-compose -f docker-compose.production.yml logs -f

# Reiniciar serviço
docker-compose -f docker-compose.production.yml restart coinbalance

# Atualizar aplicação
git pull
docker-compose -f docker-compose.production.yml build --no-cache coinbalance
docker-compose -f docker-compose.production.yml up -d coinbalance

# Backup
./backup.sh

# Restore
docker-compose -f docker-compose.production.yml exec postgres psql -U coinbalance coinbalance < backups/database_YYYYMMDD_HHMMSS.sql
```

---

## 📈 **OTIMIZAÇÕES DE PRODUÇÃO**

### **1. Configurações de Performance**

#### **Blockchain**
```python
# Configurações otimizadas para produção
BLOCKCHAIN_CONFIG = {
    "target_block_time": 10.0,
    "difficulty_adjustment_interval": 10,
    "max_transactions_per_block": 1000,
    "parallel_mining_enabled": True,
    "max_mining_threads": 16,
    "incremental_validation_enabled": True,
    "distributed_cache_enabled": True,
    "horizontal_scaling_enabled": True
}
```

#### **Cache**
```python
# Configurações de cache para produção
CACHE_CONFIG = {
    "ttl": 7200,  # 2 horas
    "max_size": 50000,
    "distributed_cache_enabled": True,
    "compression_enabled": True,
    "lru_cache_size": 10000
}
```

### **2. Monitoramento de Performance**

#### **Métricas Importantes**
- **Throughput:** Transações por segundo
- **Latência:** Tempo de resposta médio
- **Disponibilidade:** Uptime do sistema
- **Erros:** Taxa de erro por endpoint
- **Recursos:** CPU, memória, disco, rede

#### **Alertas Críticos**
- Sistema indisponível
- Taxa de erro > 10%
- Latência > 5s
- Uso de memória > 95%
- Espaço em disco < 5%

---

## 🔧 **MANUTENÇÃO**

### **1. Atualizações**
```bash
# Atualização de segurança
apt-get update && apt-get upgrade -y

# Atualização da aplicação
git pull
docker-compose -f docker-compose.production.yml build --no-cache
docker-compose -f docker-compose.production.yml up -d

# Limpeza de recursos
docker system prune -f
docker volume prune -f
```

### **2. Monitoramento de Logs**
```bash
# Logs da aplicação
tail -f logs/blockchain.log
tail -f logs/security.log
tail -f logs/performance.log

# Logs do Docker
docker-compose -f docker-compose.production.yml logs -f coinbalance
```

### **3. Troubleshooting**

#### **Problemas Comuns**
1. **Alto uso de CPU:** Verificar mineração paralela
2. **Alto uso de memória:** Verificar cache e conexões
3. **Lentidão:** Verificar banco de dados e rede
4. **Erros de conexão:** Verificar firewall e DNS

#### **Comandos de Diagnóstico**
```bash
# Status dos containers
docker-compose -f docker-compose.production.yml ps

# Recursos do sistema
htop
df -h
free -h

# Conectividade
curl -f http://localhost:8000/api/v1/health
telnet localhost 8000
```

---

*Guia de Deploy gerado em: 2024-12-19*  
*Versão: 1.0.0*  
*Status: ✅ DEPLOY OTIMIZADO COMPLETO*
