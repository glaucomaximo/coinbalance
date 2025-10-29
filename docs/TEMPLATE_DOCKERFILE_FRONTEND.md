# Multi-stage Dockerfile para Frontend Next.js
## Template para CoinBalance Frontend

## 📋 Sobre Este Template

Este é um template para Dockerfile do frontend Next.js. Ao usar este template:

### **Parâmetros para Personalização**

- `NODE_VERSION`: Versão do Node.js (padrão: `18-alpine`)
- `PORT`: Porta de exposição (padrão: `3000`)
- `NEXT_PUBLIC_API_URL`: URL da API backend (configurar via variável de ambiente)

### **Configuração de Variáveis de Ambiente**

Configure as seguintes variáveis de ambiente no ambiente de execução:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
NODE_ENV=production
```

### **Build Arguments**

Você pode passar os seguintes build arguments:

```bash
docker build \
  --build-arg NODE_VERSION=18-alpine \
  --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000 \
  -t coinbalance-frontend .
```

### **Uso**

1. Copie este arquivo para `Dockerfile` no diretório raiz do projeto frontend
2. Personalize os parâmetros conforme necessário
3. Execute: `docker build -t coinbalance-frontend .`
4. Execute: `docker run -p 3000:3000 coinbalance-frontend`

---

# Multi-stage Dockerfile para Next.js
# Otimizado para produção com standalone output

FROM node:18-alpine AS base

# Instalar dependências apenas quando necessário
FROM base AS deps
# Verificar https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Instalar dependências baseado no gerenciador de pacotes preferido
COPY package.json package-lock.json* ./
RUN npm ci

# Reconstruir código fonte apenas quando necessário
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Desabilitar telemetria do Next.js durante build
ENV NEXT_TELEMETRY_DISABLED 1

# Build da aplicação
RUN npm run build

# Imagem de produção, copiar todos os arquivos e executar next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copiar arquivos necessários para produção
COPY --from=builder /app/public ./public

# Configurar standalone output
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]

