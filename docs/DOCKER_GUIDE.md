# Guia de Docker para CoinBalance
# ================================

## 🐳 Visão Geral

O projeto CoinBalance está completamente containerizado usando Docker e Docker Compose, garantindo:

- ✅ **Isolamento de Ambiente**: Cada serviço roda em seu próprio container
- ✅ **Reprodutibilidade**: Mesmo ambiente em desenvolvimento e produção
- ✅ **Facilidade de Deploy**: Um comando para subir toda a infraestrutura
- ✅ **Escalabilidade**: Fácil adicionar/remover serviços

---

## 📦 Serviços Containerizados

### **1. CoinBalance Backend** (`coinbalance`)
- **Porta**: 8000
- **Health Check**: `/api/v1/health/live`
- **Dependências**: Redis, PostgreSQL

### **2. Redis** (`redis`)
- **Porta**: 6379
- **Uso**: Cache e sessões
- **Persistência**: AOF habilitado

### **3. PostgreSQL** (`postgres`)
- **Porta**: 5432
- **Uso**: Banco de dados principal (opcional)
- **Volume**: `postgres_data`

### **4. Nginx** (`nginx`)
- **Portas**: 80, 443
- **Uso**: Reverse proxy e load balancing

### **5. Prometheus** (`prometheus`)
- **Porta**: 9090
- **Uso**: Coleta de métricas

### **6. Grafana** (`grafana`)
- **Porta**: 3000
- **Uso**: Visualização de métricas
- **Credenciais**: admin/admin (padrão)

---

## 🚀 Início Rápido

### **1. Pré-requisitos**

```bash
# Docker Desktop (Windows/Mac) ou Docker Engine (Linux)
docker --version
docker-compose --version
```

### **2. Configuração Inicial**

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar variáveis de ambiente (IMPORTANTE!)
# Especialmente as chaves de segurança
nano .env  # ou use seu editor preferido
```

### **3. Iniciar Serviços**

```bash
# Construir e iniciar todos os serviços
docker-compose up -d

# Ou usar o script de inicialização
chmod +x scripts/docker-start.sh
./scripts/docker-start.sh
```

### **4. Verificar Status**

```bash
# Ver status dos containers
docker-compose ps

# Ver logs
docker-compose logs -f coinbalance

# Verificar saúde
curl http://localhost:8000/api/v1/health/live
```

---

## 🔧 Comandos Úteis

### **Gerenciamento de Containers**

```bash
# Iniciar serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Reconstruir após mudanças no código
docker-compose build --no-cache coinbalance
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f coinbalance

# Entrar no container
docker-compose exec coinbalance bash

# Executar comandos dentro do container
docker-compose exec coinbalance python -m pytest tests/
```

### **Desenvolvimento**

```bash
# Modo desenvolvimento com hot reload
docker-compose up coinbalance

# Executar testes
docker-compose run --rm coinbalance pytest tests/ -v

# Executar comandos Python
docker-compose exec coinbalance python main.py --help
```

### **Produção**

```bash
# Usar docker-compose.production.yml
docker-compose -f docker-compose.production.yml up -d

# Verificar saúde de todos os serviços
docker-compose ps
```

---

## 📝 Variáveis de Ambiente

### **Variáveis Críticas**

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `SECRET_KEY` | Chave secreta da aplicação | **OBRIGATÓRIA** |
| `JWT_SECRET_KEY` | Chave para tokens JWT | **OBRIGATÓRIA** |
| `ENCRYPTION_KEY` | Chave de criptografia | **OBRIGATÓRIA** |
| `DATABASE_URL` | URL do banco de dados | `sqlite:///./data/blockchain.db` |
| `REDIS_URL` | URL do Redis | `redis://redis:6379/0` |

### **Configuração de Ambiente**

```bash
# Desenvolvimento
ENVIRONMENT=development
DEBUG=false

# Produção
ENVIRONMENT=production
DEBUG=false
```

---

## 🏥 Health Checks

### **Verificar Saúde dos Serviços**

```bash
# API
curl http://localhost:8000/api/v1/health/live

# Redis
docker-compose exec redis redis-cli ping

# PostgreSQL
docker-compose exec postgres pg_isready -U coinbalance

# Prometheus
curl http://localhost:9090/-/healthy

# Grafana
curl http://localhost:3000/api/health
```

---

## 🔍 Troubleshooting

### **Problema: Container não inicia**

```bash
# Ver logs detalhados
docker-compose logs coinbalance

# Verificar se porta está em uso
netstat -an | grep 8000

# Reconstruir imagem
docker-compose build --no-cache coinbalance
```

### **Problema: Banco de dados não conecta**

```bash
# Verificar se PostgreSQL está rodando
docker-compose ps postgres

# Ver logs do PostgreSQL
docker-compose logs postgres

# Conectar manualmente
docker-compose exec postgres psql -U coinbalance -d coinbalance
```

### **Problema: Redis não conecta**

```bash
# Verificar se Redis está rodando
docker-compose ps redis

# Testar conexão
docker-compose exec redis redis-cli ping
```

### **Problema: Permissões de Volume**

```bash
# Ajustar permissões
sudo chown -R $USER:$USER data backups logs
```

---

## 📊 Monitoramento

### **Acessar Dashboards**

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

### **Métricas**

```bash
# Métricas da aplicação
curl http://localhost:8000/api/v1/metrics

# Métricas do Prometheus
curl http://localhost:9090/api/v1/query?query=up
```

---

## 🗄️ Volumes e Persistência

### **Volumes Definidos**

| Volume | Descrição | Localização |
|--------|-----------|-------------|
| `postgres_data` | Dados do PostgreSQL | `/var/lib/postgresql/data` |
| `redis_data` | Dados do Redis | `/data` |
| `prometheus_data` | Dados do Prometheus | `/prometheus` |
| `grafana_data` | Dados do Grafana | `/var/lib/grafana` |

### **Volumes Locais**

| Diretório | Descrição |
|-----------|-----------|
| `./data` | Banco de dados SQLite e dados da aplicação |
| `./backups` | Backups do sistema |
| `./logs` | Logs da aplicação |

---

## 🔒 Segurança

### **Boas Práticas**

1. ✅ **Nunca commitar arquivos `.env`**
2. ✅ **Usar chaves fortes em produção**
3. ✅ **Habilitar HTTPS em produção**
4. ✅ **Limitar exposição de portas**
5. ✅ **Usar usuário não-root nos containers**

### **Checklist de Segurança**

- [ ] Todas as chaves secretas configuradas
- [ ] `DEBUG=false` em produção
- [ ] `SECRET_KEY` com pelo menos 32 caracteres
- [ ] Senhas do PostgreSQL alteradas
- [ ] CORS configurado corretamente
- [ ] Firewall configurado

---

## 📚 Referências

- [Dockerfile](Dockerfile)
- [docker-compose.yml](docker-compose.yml)
- [docker-compose.production.yml](docker-compose.production.yml)
- [Documentação Docker](https://docs.docker.com/)
- [Documentação Docker Compose](https://docs.docker.com/compose/)

---

**Status:** ✅ **Backend Completamente Containerizado**

