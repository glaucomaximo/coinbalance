# 🚀 Guia de Deploy - Frontend CoinBalance

## Deploy em Produção Completo

Este guia cobre todo o processo de deploy do frontend CoinBalance em diversos ambientes.

---

## 📋 Índice

1. [Preparação para Produção](#preparação-para-produção)
2. [Deploy na Vercel](#deploy-na-vercel)
3. [Deploy na Netlify](#deploy-na-netlify)
4. [Deploy com Docker](#deploy-com-docker)
5. [Deploy em AWS](#deploy-em-aws)
6. [CI/CD com GitHub Actions](#cicd-com-github-actions)
7. [Monitoramento](#monitoramento)

---

## 🔧 Preparação para Produção

### 1. Build Otimizado

```bash
# Instalar dependências
npm ci

# Build para produção
npm run build

# Verificar build
npm run start
```

### 2. Variáveis de Ambiente

Crie `.env.production`:

```bash
# API
NEXT_PUBLIC_API_URL=https://api.coinbalance.com
NEXT_PUBLIC_WS_URL=wss://api.coinbalance.com/ws

# App
NEXT_PUBLIC_APP_NAME=CoinBalance
NEXT_PUBLIC_APP_VERSION=1.0.0
NEXT_PUBLIC_APP_ENV=production

# Analytics
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
NEXT_PUBLIC_SENTRY_DSN=https://...

# Features
NEXT_PUBLIC_ENABLE_WEB3=true
NEXT_PUBLIC_ENABLE_AI=true
```

### 3. Otimizações

```typescript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Compressão
  compress: true,
  
  // Otimização de imagens
  images: {
    formats: ['image/avif', 'image/webp'],
    domains: ['api.coinbalance.com'],
    minimumCacheTTL: 60,
  },

  // Headers de segurança
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on'
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload'
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block'
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin'
          },
        ],
      },
    ];
  },

  // Rewrites para API
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://api.coinbalance.com/api/:path*',
      },
    ];
  },

  // PWA
  pwa: {
    dest: 'public',
    register: true,
    skipWaiting: true,
    disable: process.env.NODE_ENV === 'development',
  },

  // Bundle Analyzer
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        fs: false,
        net: false,
        tls: false,
      };
    }
    return config;
  },
};

module.exports = nextConfig;
```

### 4. Checklist Pré-Deploy

- [ ] Todos os testes passando (`npm test`)
- [ ] Build sem erros (`npm run build`)
- [ ] Lighthouse score > 90
- [ ] Sem vulnerabilidades críticas (`npm audit`)
- [ ] TypeScript sem erros (`npx tsc --noEmit`)
- [ ] ESLint sem erros (`npm run lint`)
- [ ] Variáveis de ambiente configuradas
- [ ] SSL/TLS configurado
- [ ] CDN configurado (se aplicável)
- [ ] Backup strategy definida

---

## 🔷 Deploy na Vercel

### Opção 1: Via CLI

```bash
# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy preview
vercel

# Deploy produção
vercel --prod
```

### Opção 2: Via GitHub Integration

1. Acesse https://vercel.com
2. Clique em "Import Project"
3. Conecte seu repositório GitHub
4. Configure variáveis de ambiente
5. Deploy automático!

### Configuração Vercel

```json
// vercel.json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm ci",
  "framework": "nextjs",
  "regions": ["gru1"],
  "env": {
    "NEXT_PUBLIC_API_URL": "@api-url-production",
    "NEXT_PUBLIC_APP_ENV": "production"
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/home",
      "destination": "/",
      "permanent": true
    }
  ],
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://api.coinbalance.com/api/:path*"
    }
  ]
}
```

### Configurar Domínio Custom

```bash
# Adicionar domínio
vercel domains add coinbalance.com

# Verificar DNS
vercel domains inspect coinbalance.com
```

---

## 🟢 Deploy na Netlify

### Opção 1: Via CLI

```bash
# Instalar Netlify CLI
npm i -g netlify-cli

# Login
netlify login

# Inicializar
netlify init

# Deploy
netlify deploy --prod
```

### Opção 2: Via Git

1. Acesse https://netlify.com
2. "New site from Git"
3. Conecte repositório
4. Configurações:
   - Build command: `npm run build`
   - Publish directory: `.next`
5. Deploy!

### Configuração Netlify

```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = ".next"

[build.environment]
  NODE_VERSION = "18"
  NPM_VERSION = "9"

[[redirects]]
  from = "/api/*"
  to = "https://api.coinbalance.com/api/:splat"
  status = 200
  force = true

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    X-XSS-Protection = "1; mode=block"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/static/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```

---

## 🐳 Deploy com Docker

### Dockerfile

```dockerfile
# Dockerfile
FROM node:18-alpine AS base

# Dependências
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

# Builder
FROM base AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1

RUN npm run build

# Runner
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=https://api.coinbalance.com
      - NODE_ENV=production
    restart: unless-stopped
    networks:
      - coinbalance

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
      - coinbalance

networks:
  coinbalance:
    driver: bridge
```

### Nginx Config

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }

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
        ssl_ciphers HIGH:!aNULL:!MD5;

        gzip on;
        gzip_types text/plain text/css application/json application/javascript;
        gzip_min_length 1000;

        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /_next/static/ {
            proxy_pass http://frontend;
            proxy_cache_valid 200 365d;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### Deploy

```bash
# Build e deploy
docker-compose build
docker-compose up -d

# Ver logs
docker-compose logs -f frontend

# Parar
docker-compose down
```

---

## ☁️ Deploy em AWS

### Usando AWS Amplify

```bash
# Instalar Amplify CLI
npm install -g @aws-amplify/cli

# Configurar
amplify configure

# Inicializar
amplify init

# Add hosting
amplify add hosting

# Deploy
amplify publish
```

### Usando EC2 + Nginx

```bash
# SSH na instância
ssh -i key.pem ubuntu@ec2-xx-xxx-xxx-xxx.compute.amazonaws.com

# Instalar Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Instalar Nginx
sudo apt-get install nginx

# Clonar repositório
git clone https://github.com/seu-usuario/coinbalance-frontend
cd coinbalance-frontend

# Instalar dependências e build
npm ci
npm run build

# Configurar PM2
npm install -g pm2
pm2 start npm --name "coinbalance-frontend" -- start
pm2 startup
pm2 save

# Configurar Nginx (ver configuração acima)
sudo nano /etc/nginx/sites-available/coinbalance
sudo ln -s /etc/nginx/sites-available/coinbalance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔄 CI/CD com GitHub Actions

### Workflow Completo

```yaml
# .github/workflows/deploy.yml
name: Deploy Frontend

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run tests
        run: npm run test:ci
      
      - name: Run build
        run: npm run build

  deploy-preview:
    needs: test
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Vercel Preview
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}

  deploy-production:
    needs: test
    if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Vercel Production
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID}}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
      
      - name: Send Slack notification
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Deploy to production completed!'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
        if: always()
```

---

## 📊 Monitoramento

### 1. Sentry (Error Tracking)

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NEXT_PUBLIC_APP_ENV,
  tracesSampleRate: 1.0,
  beforeSend(event) {
    // Filtrar dados sensíveis
    if (event.request?.headers?.authorization) {
      delete event.request.headers.authorization;
    }
    return event;
  },
});
```

### 2. Google Analytics

```typescript
// lib/analytics.ts
export const GA_TRACKING_ID = process.env.NEXT_PUBLIC_GA_ID;

export const pageview = (url: string) => {
  window.gtag('config', GA_TRACKING_ID, {
    page_path: url,
  });
};

export const event = ({ action, category, label, value }: any) => {
  window.gtag('event', action, {
    event_category: category,
    event_label: label,
    value: value,
  });
};
```

### 3. Monitoring Dashboard

```typescript
// lib/monitoring.ts
export const logMetric = (name: string, value: number) => {
  if (typeof window !== 'undefined' && 'performance' in window) {
    const metric = {
      name,
      value,
      timestamp: Date.now(),
    };
    
    // Enviar para endpoint de métricas
    fetch('/api/metrics', {
      method: 'POST',
      body: JSON.stringify(metric),
    }).catch(console.error);
  }
};

export const reportWebVitals = ({ id, name, value }: any) => {
  logMetric(name, value);
};
```

---

## ✅ Checklist Final de Deploy

### Pré-Deploy
- [ ] Testes passando (unit + e2e)
- [ ] Build sem erros
- [ ] Lighthouse score > 90
- [ ] TypeScript sem erros
- [ ] ESLint sem warnings críticos
- [ ] Dependências atualizadas
- [ ] Sem vulnerabilidades críticas

### Configuração
- [ ] Variáveis de ambiente configuradas
- [ ] SSL/TLS certificado
- [ ] Domínio DNS configurado
- [ ] CDN configurado
- [ ] Headers de segurança
- [ ] CORS configurado
- [ ] Rate limiting (se aplicável)

### Monitoramento
- [ ] Sentry configurado
- [ ] Analytics configurado
- [ ] Logs centralizados
- [ ] Alertas configurados
- [ ] Uptime monitoring
- [ ] Performance monitoring

### Pós-Deploy
- [ ] Smoke tests passando
- [ ] Rollback plan pronto
- [ ] Documentação atualizada
- [ ] Equipe notificada
- [ ] Monitoring dashboard verificado

---

**Versão**: 1.0.0  
**Última Atualização**: 2025-10-28
