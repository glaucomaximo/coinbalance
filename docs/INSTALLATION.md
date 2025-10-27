# 🚀 Guia de Instalação e Configuração

<div align="center">

![Installation](https://img.shields.io/badge/Installation-Guide-FF6B6B?style=for-the-badge)
![Configuration](https://img.shields.io/badge/Configuration-Complete-4ECDC4?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-00D4AA?style=for-the-badge)

**Instalação e Configuração do CoinBalance Fractal Consciente**

</div>

---

## 🌟 **Visão Geral**

Este guia fornece instruções completas para instalar e configurar o **CoinBalance**, uma blockchain consciente e infinitamente escalável baseada em arquitetura fractal. O sistema é projetado para ser facilmente instalado e configurado em diferentes ambientes.

### 🎯 **Objetivos da Instalação**

- ✅ **Instalação Simples**: Processo de instalação simplificado
- ✅ **Configuração Automática**: Configuração automática de componentes
- ✅ **Ambiente Flexível**: Suporte a diferentes ambientes
- ✅ **Produção Ready**: Pronto para produção

---

## 📋 **Pré-requisitos**

### **Sistema Operacional**

- **Windows**: Windows 10/11 (64-bit)
- **macOS**: macOS 10.15+ (64-bit)
- **Linux**: Ubuntu 20.04+, CentOS 8+, Debian 11+

### **Software Necessário**

- **Python**: 3.11+ (recomendado: 3.11.5)
- **Git**: 2.30+
- **Docker**: 20.10+ (opcional)
- **Node.js**: 18+ (para desenvolvimento frontend)

### **Recursos do Sistema**

- **RAM**: Mínimo 4GB, Recomendado 8GB+
- **CPU**: Mínimo 2 cores, Recomendado 4+ cores
- **Armazenamento**: Mínimo 10GB livre
- **Rede**: Conexão com internet para dependências

---

## 🔧 **Instalação**

### **Método 1: Instalação Manual**

#### **1. Clone do Repositório**

```bash
# Clone o repositório
git clone https://github.com/coinbalance/coinbalance.git
cd coinbalance

# Verificar versão do Python
python --version
# Deve ser 3.11+

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

#### **2. Instalação de Dependências**

```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt

# Verificar instalação
pip list
```

#### **3. Configuração Inicial**

```bash
# Copiar arquivo de configuração
cp env.example .env

# Editar configurações (opcional)
# Windows
notepad .env
# macOS/Linux
nano .env
```

### **Método 2: Instalação com Docker**

#### **1. Build da Imagem**

```bash
# Build da imagem Docker
docker build -t coinbalance:latest .

# Verificar imagem criada
docker images | grep coinbalance
```

#### **2. Executar Container**

```bash
# Executar container
docker run -d \
  --name coinbalance \
  -p 8001:8001 \
  -e JWT_SECRET_KEY="your-secure-jwt-key" \
  -e COINBALANCE_MASTER_KEY="your-secure-master-key" \
  coinbalance:latest

# Verificar status
docker ps | grep coinbalance
```

### **Método 3: Instalação com Docker Compose**

#### **1. Configurar Docker Compose**

```yaml
# docker-compose.yml
version: '3.8'
services:
  coinbalance:
    build: .
    ports:
      - "8001:8001"
    environment:
      - JWT_SECRET_KEY=your-secure-jwt-key
      - COINBALANCE_MASTER_KEY=your-secure-master-key
      - CORS_ORIGINS=http://localhost:3000,http://localhost:8000
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

#### **2. Executar com Docker Compose**

```bash
# Executar serviços
docker-compose up -d

# Verificar logs
docker-compose logs -f coinbalance

# Parar serviços
docker-compose down
```

---

## ⚙️ **Configuração**

### **Variáveis de Ambiente**

#### **Configurações Básicas**

```bash
# .env
# ========== API CONFIGURATION ==========
API_HOST=0.0.0.0
API_PORT=8001
API_WORKERS=1
API_RELOAD=true
API_LOG_LEVEL=info

# ========== DATABASE ==========
DATABASE_URL=sqlite:///./blockchain.db
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# ========== SECURITY ==========
JWT_SECRET_KEY=dev-secret-key-change-in-production-32-chars-long
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Crypto
COINBALANCE_MASTER_KEY=dev-master-key-change-in-production-32-chars-long

# ========== CORS ==========
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://localhost:8001
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_ALLOW_HEADERS=*

# ========== FRACTAL SYSTEMS ==========
FRACTAL_CONSCIOUSNESS_LEVEL=0.8
FRACTAL_LEARNING_RATE=0.01
FRACTAL_ANOMALY_THRESHOLD=2.0

# Cache Fractal
FRACTAL_CACHE_SIZE=256MB
FRACTAL_CACHE_DISTRIBUTION=auto

# Load Balancer
FRACTAL_LB_STRATEGY=round_robin
FRACTAL_LB_HEALTH_CHECK_INTERVAL=30

# Machine Learning
FRACTAL_ML_ENABLED=true
FRACTAL_ML_MODEL_TYPE=distributed
FRACTAL_ML_TRAINING_INTERVAL=3600

# Genetic Optimization
FRACTAL_GENETIC_ENABLED=true
FRACTAL_GENETIC_POPULATION_SIZE=100
FRACTAL_GENETIC_MUTATION_RATE=0.1

# Geographic Distribution
FRACTAL_GEO_ENABLED=true
FRACTAL_GEO_REGIONS=us-east,eu-west,asia-pacific

# Auto-scaling
FRACTAL_AUTO_SCALING_ENABLED=true
FRACTAL_SCALE_UP_THRESHOLD=80
FRACTAL_SCALE_DOWN_THRESHOLD=20

# ========== MONITORING ==========
MONITORING_ENABLED=true
METRICS_COLLECTION_INTERVAL=60
ALERT_THRESHOLD_CPU=80
ALERT_THRESHOLD_MEMORY=85

# ========== LOGGING ==========
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=logs/coinbalance.log
LOG_ROTATION=daily
LOG_RETENTION_DAYS=30
```

#### **Configurações de Produção**

```bash
# .env.production
# ========== PRODUCTION SETTINGS ==========
ENVIRONMENT=production
DEBUG=false
API_WORKERS=4

# ========== SECURITY (PRODUCTION) ==========
JWT_SECRET_KEY=your-super-secure-jwt-key-32-chars-long
COINBALANCE_MASTER_KEY=your-super-secure-master-key-32-chars-long

# ========== DATABASE (PRODUCTION) ==========
DATABASE_URL=postgresql://user:password@localhost:5432/coinbalance
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30

# ========== REDIS (PRODUCTION) ==========
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=your-redis-password

# ========== MONITORING (PRODUCTION) ==========
PROMETHEUS_ENABLED=true
PROMETHEUS_PORT=9090
GRAFANA_ENABLED=true
GRAFANA_PORT=3000

# ========== BACKUP ==========
BACKUP_ENABLED=true
BACKUP_INTERVAL=24h
BACKUP_RETENTION_DAYS=30
BACKUP_S3_BUCKET=coinbalance-backups
```

### **Configuração do Banco de Dados**

#### **SQLite (Desenvolvimento)**

```python
# Configuração automática - não requer configuração adicional
DATABASE_URL=sqlite:///./blockchain.db
```

#### **PostgreSQL (Produção)**

```bash
# Instalar PostgreSQL
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install postgresql-server postgresql-contrib

# Criar banco de dados
sudo -u postgres createdb coinbalance
sudo -u postgres createuser coinbalance_user
sudo -u postgres psql -c "ALTER USER coinbalance_user PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE coinbalance TO coinbalance_user;"

# Configurar conexão
DATABASE_URL=postgresql://coinbalance_user:secure_password@localhost:5432/coinbalance
```

#### **MySQL (Alternativa)**

```bash
# Instalar MySQL
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# CentOS/RHEL
sudo yum install mysql-server

# Criar banco de dados
sudo mysql -e "CREATE DATABASE coinbalance;"
sudo mysql -e "CREATE USER 'coinbalance_user'@'localhost' IDENTIFIED BY 'secure_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON coinbalance.* TO 'coinbalance_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Configurar conexão
DATABASE_URL=mysql://coinbalance_user:secure_password@localhost:3306/coinbalance
```

### **Configuração de Cache**

#### **Cache em Memória (Desenvolvimento)**

```python
# Configuração automática
CACHE_TYPE=memory
CACHE_SIZE=256MB
```

#### **Redis (Produção)**

```bash
# Instalar Redis
# Ubuntu/Debian
sudo apt update
sudo apt install redis-server

# CentOS/RHEL
sudo yum install redis

# Configurar Redis
sudo systemctl start redis
sudo systemctl enable redis

# Configurar conexão
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=your-redis-password
```

### **Configuração de Monitoramento**

#### **Prometheus + Grafana**

```bash
# Instalar Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.40.0/prometheus-2.40.0.linux-amd64.tar.gz
tar xvfz prometheus-2.40.0.linux-amd64.tar.gz
cd prometheus-2.40.0.linux-amd64

# Configurar Prometheus
cat > prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'coinbalance'
    static_configs:
      - targets: ['localhost:8001']
EOF

# Executar Prometheus
./prometheus --config.file=prometheus.yml

# Instalar Grafana
wget https://dl.grafana.com/oss/release/grafana-9.3.0.linux-amd64.tar.gz
tar -zxvf grafana-9.3.0.linux-amd64.tar.gz
cd grafana-9.3.0

# Executar Grafana
./bin/grafana-server
```

---

## 🚀 **Execução**

### **Desenvolvimento**

```bash
# Ativar ambiente virtual
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Executar em modo desenvolvimento
python main.py --port 8001 --reload --log-level info

# Ou usando uvicorn diretamente
uvicorn src.presentation.api.app:app --host 0.0.0.0 --port 8001 --reload
```

### **Produção**

```bash
# Executar com Gunicorn (Linux/macOS)
gunicorn src.presentation.api.app:app \
  --bind 0.0.0.0:8001 \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --log-level info

# Executar com systemd (Linux)
sudo systemctl start coinbalance
sudo systemctl enable coinbalance
```

### **Docker**

```bash
# Executar container
docker run -d \
  --name coinbalance \
  -p 8001:8001 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  coinbalance:latest

# Verificar logs
docker logs -f coinbalance

# Parar container
docker stop coinbalance
docker rm coinbalance
```

---

## 🧪 **Testes**

### **Executar Testes**

```bash
# Instalar dependências de teste
pip install pytest pytest-cov pytest-asyncio

# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=src --cov-report=html

# Executar testes específicos
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
pytest tests/performance/

# Executar testes com verbose
pytest -v

# Executar testes com paralelização
pytest -n auto
```

### **Testes de API**

```bash
# Instalar dependências para testes de API
pip install httpx pytest-httpx

# Executar testes de API
pytest tests/api/ -v

# Executar testes de performance
pytest tests/performance/ -v --benchmark-only
```

---

## 📊 **Monitoramento**

### **Health Check**

```bash
# Verificar saúde do sistema
curl http://localhost:8001/health

# Resposta esperada
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "services": {
    "database": "healthy",
    "cache": "healthy",
    "blockchain": "healthy"
  }
}
```

### **Métricas**

```bash
# Verificar métricas
curl http://localhost:8001/monitoring/metrics

# Verificar status dos sistemas conscientes
curl http://localhost:8001/conscious/status
```

### **Logs**

```bash
# Verificar logs em tempo real
tail -f logs/coinbalance.log

# Verificar logs de erro
grep "ERROR" logs/coinbalance.log

# Verificar logs de acesso
tail -f logs/access.log
```

---

## 🔧 **Troubleshooting**

### **Problemas Comuns**

#### **1. Erro de Porta em Uso**

```bash
# Verificar processos usando a porta 8001
# Windows
netstat -ano | findstr :8001
# macOS/Linux
lsof -i :8001

# Matar processo
# Windows
taskkill /PID <PID> /F
# macOS/Linux
kill -9 <PID>
```

#### **2. Erro de Dependências**

```bash
# Reinstalar dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Verificar versão do Python
python --version
# Deve ser 3.11+

# Verificar pip
pip --version
```

#### **3. Erro de Banco de Dados**

```bash
# Verificar conexão com banco
python -c "import sqlite3; print('SQLite OK')"

# Recriar banco de dados
rm blockchain.db
python main.py --init-db
```

#### **4. Erro de Permissões**

```bash
# Verificar permissões de arquivo
ls -la logs/
ls -la data/

# Corrigir permissões
chmod 755 logs/
chmod 755 data/
chmod 644 logs/*.log
```

### **Logs de Debug**

```bash
# Executar com debug
python main.py --port 8001 --log-level debug

# Verificar logs detalhados
tail -f logs/coinbalance.log | grep DEBUG
```

---

## 🔒 **Segurança**

### **Configurações de Segurança**

#### **Chaves de Segurança**

```bash
# Gerar chaves seguras
# JWT Secret Key (32 caracteres)
openssl rand -hex 32

# Master Key (32 caracteres)
openssl rand -hex 32

# Configurar no .env
JWT_SECRET_KEY=generated-jwt-secret-key-here
COINBALANCE_MASTER_KEY=generated-master-key-here
```

#### **Firewall**

```bash
# Configurar firewall (Linux)
sudo ufw allow 8001/tcp
sudo ufw enable

# Configurar firewall (Windows)
netsh advfirewall firewall add rule name="CoinBalance API" dir=in action=allow protocol=TCP localport=8001
```

#### **SSL/TLS**

```bash
# Gerar certificado SSL
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Configurar HTTPS
API_SSL_ENABLED=true
API_SSL_CERT=cert.pem
API_SSL_KEY=key.pem
```

---

## 📈 **Performance**

### **Otimizações de Performance**

#### **Configurações de Produção**

```bash
# Aumentar workers
API_WORKERS=4

# Configurar pool de conexões
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30

# Configurar cache
CACHE_SIZE=512MB
CACHE_TTL=3600

# Configurar sistemas fractais
FRACTAL_CACHE_SIZE=512MB
FRACTAL_ML_ENABLED=true
FRACTAL_AUTO_SCALING_ENABLED=true
```

#### **Monitoramento de Performance**

```bash
# Instalar ferramentas de monitoramento
pip install psutil memory-profiler

# Monitorar uso de memória
python -m memory_profiler main.py

# Monitorar CPU
htop
```

---

## 🔄 **Backup e Restore**

### **Backup**

```bash
# Backup do banco de dados
cp blockchain.db blockchain_backup_$(date +%Y%m%d_%H%M%S).db

# Backup completo
tar -czf coinbalance_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
  blockchain.db \
  logs/ \
  data/ \
  .env
```

### **Restore**

```bash
# Restaurar banco de dados
cp blockchain_backup_20240101_120000.db blockchain.db

# Restaurar backup completo
tar -xzf coinbalance_backup_20240101_120000.tar.gz
```

---

## 🚀 **Deploy**

### **Deploy Manual**

```bash
# Preparar ambiente de produção
export ENVIRONMENT=production
export DEBUG=false

# Executar migrações
python -m alembic upgrade head

# Executar sistema
gunicorn src.presentation.api.app:app \
  --bind 0.0.0.0:8001 \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker
```

### **Deploy com Docker**

```bash
# Build da imagem de produção
docker build -t coinbalance:production .

# Executar em produção
docker run -d \
  --name coinbalance-prod \
  -p 8001:8001 \
  --env-file .env.production \
  --restart unless-stopped \
  coinbalance:production
```

### **Deploy com Kubernetes**

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: coinbalance
spec:
  replicas: 3
  selector:
    matchLabels:
      app: coinbalance
  template:
    metadata:
      labels:
        app: coinbalance
    spec:
      containers:
      - name: coinbalance
        image: coinbalance:production
        ports:
        - containerPort: 8001
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: coinbalance-secrets
              key: jwt-secret-key
---
apiVersion: v1
kind: Service
metadata:
  name: coinbalance-service
spec:
  selector:
    app: coinbalance
  ports:
  - port: 8001
    targetPort: 8001
  type: LoadBalancer
```

---

## 🎯 **Próximos Passos**

### **Após Instalação**

1. **Verificar Sistema**: Acesse http://localhost:8001/docs
2. **Configurar Monitoramento**: Configure Prometheus e Grafana
3. **Testar API**: Execute testes de integração
4. **Configurar Backup**: Configure backup automático
5. **Otimizar Performance**: Ajuste configurações para seu ambiente

### **Desenvolvimento**

1. **Explorar Código**: Estude a arquitetura fractal
2. **Contribuir**: Faça contribuições para o projeto
3. **Documentar**: Documente suas descobertas
4. **Compartilhar**: Compartilhe com a comunidade

---

## 🏆 **Suporte**

### **Recursos de Ajuda**

- 📖 **Documentação**: [docs/](docs/)
- 🐛 **Issues**: [GitHub Issues](https://github.com/coinbalance/coinbalance/issues)
- 💬 **Discord**: [Discord Server](https://discord.gg/coinbalance)
- 📧 **Email**: support@coinbalance.com

### **Comunidade**

- 🌟 **GitHub**: [coinbalance/coinbalance](https://github.com/coinbalance/coinbalance)
- 🐦 **Twitter**: [@coinbalance](https://twitter.com/coinbalance)
- 📺 **YouTube**: [CoinBalance Channel](https://youtube.com/coinbalance)

---

<div align="center">

**🚀 CoinBalance - Instalação e Configuração Completas**

![Installation](https://img.shields.io/badge/Installation-Success-4ECDC4?style=for-the-badge)
![Configuration](https://img.shields.io/badge/Configuration-Complete-00D4AA?style=for-the-badge)
![Ready](https://img.shields.io/badge/Ready-Production-FF6B6B?style=for-the-badge)

</div>
