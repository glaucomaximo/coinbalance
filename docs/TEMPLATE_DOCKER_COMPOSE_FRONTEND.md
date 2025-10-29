# Docker Compose para Frontend Next.js
## Template para CoinBalance Frontend

## 📋 Sobre Este Template

Este é um template para `docker-compose.yml` do frontend Next.js. Ao usar este template:

### **Parâmetros para Personalização**

- `API_URL`: URL da API backend (padrão: `http://localhost:8000`)
- `API_VERSION`: Versão da API (padrão: `v1`)
- `JWT_STORAGE_KEY`: Chave de armazenamento do JWT (padrão: `authToken`)
- `PORT`: Porta de exposição (padrão: `3000`)

### **Configuração via Arquivo .env**

Crie um arquivo `.env` na raiz do projeto com:

```env
API_URL=http://localhost:8000
API_VERSION=v1
JWT_STORAGE_KEY=authToken
```

### **Uso**

1. Copie este arquivo para `docker-compose.yml` no diretório raiz do projeto frontend
2. Crie arquivo `.env` com as configurações
3. Execute: `docker-compose up -d`
4. Acesse: `http://localhost:3000`

---

version: '3.8'

services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=${API_URL:-http://localhost:8000}
      - NEXT_PUBLIC_API_VERSION=${API_VERSION:-v1}
      - NEXT_PUBLIC_JWT_STORAGE_KEY=${JWT_STORAGE_KEY:-authToken}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - frontend-network

  # Opcional: Nginx como reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
    restart: unless-stopped
    networks:
      - frontend-network

networks:
  frontend-network:
    driver: bridge

# Para desenvolvimento local com hot reload:
# docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

