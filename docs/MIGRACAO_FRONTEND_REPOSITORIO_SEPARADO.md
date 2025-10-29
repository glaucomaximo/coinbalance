# 📋 Plano de Desacoplamento do Frontend - CoinBalance
## Migração para Repositório Separado

**Data de Criação:** 29 de outubro de 2025  
**Versão do Documento:** 1.0.0  
**Status:** 📝 Planejamento  
**Responsável:** Engenharia de Software

---

## 📊 Sumário Executivo

Este documento descreve o plano completo para desacoplar o frontend do repositório principal `coinbalance` e criar um repositório separado `coinbalance-frontend` para versionamento independente.

### Objetivos

1. ✅ **Separação de Responsabilidades**: Frontend e backend como projetos independentes
2. ✅ **Versionamento Independente**: Ciclos de release separados
3. ✅ **Deploy Independente**: Deploy frontend sem necessidade de rebuild do backend
4. ✅ **Escalabilidade**: Equipes podem trabalhar independentemente
5. ✅ **Manutenibilidade**: Menor complexidade em cada repositório

### Benefícios Esperados

- 🚀 **Deploy mais rápido**: Frontend pode ser deployado independentemente
- 🔄 **CI/CD separado**: Pipelines independentes para cada projeto
- 👥 **Paralelização**: Equipes frontend e backend trabalham sem conflitos
- 📦 **Tamanho reduzido**: Cada repositório menor e mais focado
- 🎯 **Foco**: Cada repositório com responsabilidades claras

---

## 🔍 Análise de Dependências

### Dependências do Frontend com o Backend

#### ✅ **Acoplamento via API (Baixo)**
- Frontend se comunica apenas via HTTP/REST
- Não há imports diretos de código Python
- Configuração via variáveis de ambiente

**Arquivos Afetados:**
- `frontend/src/lib/api/client.ts` - Cliente HTTP independente
- `frontend/src/services/*.service.ts` - Serviços baseados em API
- `frontend/next.config.js` - Rewrites para API (opcional)

#### ⚠️ **Documentação Compartilhada (Médio)**
- `docs/frontend/` - Documentação específica do frontend
- `docs/MANUAL_INTEGRACAO_FRONTEND.md` - Manual de integração
- Referências cruzadas em README.md

#### ✅ **Zero Dependências Código (Nenhuma)**
- Não há imports de código Python no frontend
- Não há imports de código TypeScript no backend
- Builds completamente independentes

### Estrutura Atual

```
coinbalance/
├── frontend/              # 🎯 SERÁ MOVIDO
│   ├── src/              # Código fonte Next.js
│   ├── package.json     # Dependências npm
│   └── ...
├── src/                  # Backend Python
├── docs/
│   ├── frontend/         # 🎯 SERÁ MOVIDO
│   └── ...
├── docker-compose.yml    # ⚠️ PRECISA ATUALIZAR
├── .gitignore            # ⚠️ PRECISA ATUALIZAR
└── README.md             # ⚠️ PRECISA ATUALIZAR
```

### Estrutura Proposta

```
# Repositório: coinbalance (Backend)
coinbalance/
├── src/                  # Backend Python
├── docs/
│   └── api/              # Docs da API
├── docker-compose.yml    # Apenas backend
└── README.md             # Focado em backend

# Repositório: coinbalance-frontend (Novo)
coinbalance-frontend/
├── src/                  # Frontend Next.js
├── docs/                 # Docs específicas do frontend
├── public/               # Assets estáticos
├── package.json
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## ✅ Checklist Pré-Migração

### Análise e Preparação

- [x] ✅ Análise de dependências concluída
- [x] ✅ Identificação de arquivos a migrar
- [x] ✅ Identificação de documentação a migrar
- [ ] ⏳ Verificação de referências no código backend
- [ ] ⏳ Backup completo do repositório atual
- [ ] ⏳ Comunicação com equipe sobre migração

### Verificações Técnicas

- [ ] ⏳ Testes do frontend passando (100%)
- [ ] ⏳ Build do frontend funcionando
- [ ] ⏳ Todas as dependências instaladas
- [ ] ⏳ Variáveis de ambiente documentadas
- [ ] ⏳ CI/CD funcionando (se existir)

### Documentação

- [x] ✅ Este plano de migração criado
- [ ] ⏳ README.md para novo repositório preparado
- [ ] ⏳ Guia de migração para desenvolvedores
- [ ] ⏳ Changelog atualizado

---

## 📝 Plano de Migração Detalhado

### Fase 1: Preparação do Novo Repositório

#### Etapa 1.1: Criar Estrutura Base do Novo Repositório

```bash
# Criar novo diretório temporário para preparação
mkdir coinbalance-frontend-migration
cd coinbalance-frontend-migration

# Inicializar git
git init
git remote add origin https://github.com/coinbalance/coinbalance-frontend.git
```

#### Etapa 1.2: Copiar Arquivos do Frontend

**Arquivos a Copiar:**

```bash
# Estrutura completa do frontend
cp -r ../coinbalance/frontend/* .

# Arquivos raiz importantes
cp ../coinbalance/frontend/.gitignore .
cp ../coinbalance/frontend/.env.example .
cp ../coinbalance/frontend/.eslintrc.json .
cp ../coinbalance/frontend/.prettierrc .
```

#### Etapa 1.3: Copiar Documentação Específica

```bash
# Criar estrutura de docs
mkdir -p docs

# Copiar documentação específica do frontend
cp -r ../coinbalance/docs/frontend/* docs/

# Copiar manual de integração (referência futura)
cp ../coinbalance/docs/MANUAL_INTEGRACAO_FRONTEND.md docs/

# Copiar arquivos de overview
cp ../coinbalance/frontend/README.md .
cp ../coinbalance/frontend/OVERVIEW.md docs/
cp ../coinbalance/frontend/INSTRUCOES.md docs/
cp ../coinbalance/FRONTEND_COMPLETO.md docs/
```

#### Etapa 1.4: Criar .gitignore Específico

```bash
# Criar .gitignore otimizado para Next.js
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/
.nyc_output

# Next.js
.next/
out/
build/
dist/

# Production
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env*.local
.env

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
```

### Fase 2: Configuração do Novo Repositório

#### Etapa 2.1: Atualizar package.json

**Mudanças Necessárias:**

```json
{
  "name": "@coinbalance/frontend",
  "version": "1.0.0",
  "description": "Frontend da plataforma CoinBalance - Blockchain Enterprise",
  "repository": {
    "type": "git",
    "url": "https://github.com/coinbalance/coinbalance-frontend.git"
  },
  "keywords": [
    "coinbalance",
    "blockchain",
    "frontend",
    "nextjs",
    "react",
    "typescript"
  ],
  "author": "CoinBalance Team",
  "license": "MIT",
  "homepage": "https://github.com/coinbalance/coinbalance-frontend#readme"
}
```

#### Etapa 2.2: Criar README.md do Novo Repositório

**Estrutura Proposta:**

```markdown
# 🌐 CoinBalance Frontend

Frontend da plataforma CoinBalance - Blockchain Enterprise.

> **Nota:** Este é um repositório independente. Para o backend, consulte [coinbalance/coinbalance](https://github.com/coinbalance/coinbalance).

## 🚀 Início Rápido

[Instruções completas...]
```

#### Etapa 2.3: Criar Dockerfile Independente

```dockerfile
# Dockerfile para frontend standalone
FROM node:18-alpine AS base

# Dependencies
FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

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
CMD ["node", "server.js"]
```

#### Etapa 2.4: Criar docker-compose.yml Independente

```yaml
version: '3.8'

services:
  frontend:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=${API_URL:-http://localhost:8000}
      - NODE_ENV=production
    restart: unless-stopped
```

### Fase 3: Atualização do Repositório Backend

#### Etapa 3.1: Remover Diretório Frontend

```bash
# NO REPOSITÓRIO BACKEND (coinbalance)
git rm -r frontend/
git commit -m "refactor: remove frontend directory (migrated to separate repo)"
```

#### Etapa 3.2: Remover Documentação Frontend

```bash
# Remover docs específicas do frontend
git rm -r docs/frontend/
git rm docs/MANUAL_INTEGRACAO_FRONTEND.md  # ou mover para seção de referência
git commit -m "docs: remove frontend-specific documentation"
```

#### Etapa 3.3: Atualizar .gitignore

**Remover:**
```gitignore
# Node.js (mantido para compatibilidade futura se necessário)
node_modules/
npm-debug.log*
```

**Adicionar:**
```gitignore
# Frontend (não mais necessário, mas mantido para referência)
# frontend/ node_modules/ - removido após migração
```

#### Etapa 3.4: Atualizar README.md do Backend

**Mudanças Necessárias:**

1. **Seção Frontend:**
   - Alterar de "Frontend: http://localhost:3000 🌐 **NOVO!**"
   - Para: "Frontend: Veja [coinbalance-frontend](https://github.com/coinbalance/coinbalance-frontend)"

2. **Estrutura do Projeto:**
   - Remover seção `frontend/` da estrutura
   - Adicionar nota sobre repositório separado

3. **Instalação:**
   - Remover seção "Instalação do Frontend"
   - Adicionar link para repositório frontend

4. **Adicionar Seção:**

```markdown
## 🌐 Frontend

O frontend do CoinBalance está em um repositório separado:

- **Repositório**: [coinbalance-frontend](https://github.com/coinbalance/coinbalance-frontend)
- **Documentação**: [docs frontend](https://github.com/coinbalance/coinbalance-frontend/blob/main/README.md)
- **API Backend**: http://localhost:8000
```

#### Etapa 3.5: Atualizar docker-compose.yml (Backend)

**Remover serviço frontend** (se existir):

```yaml
# REMOVER:
# frontend:
#   build: ./frontend
#   ...
```

**Atualizar grafana porta** (se conflitar):

```yaml
grafana:
  ports:
    - "3001:3000"  # Mudar de 3000 para 3001 para evitar conflito
```

### Fase 4: Validação e Testes

#### Etapa 4.1: Validar Novo Repositório

```bash
cd coinbalance-frontend

# Instalar dependências
npm install

# Executar testes
npm test

# Build de produção
npm run build

# Verificar build
npm start
```

#### Etapa 4.2: Testar Integração com Backend

1. **Backend rodando em localhost:8000**
2. **Frontend rodando em localhost:3000**
3. **Testar fluxos:**
   - Login
   - Dashboard
   - Carteiras
   - Transações
   - Blockchain explorer

#### Etapa 4.3: Validar Documentação

- [ ] README.md completo e funcional
- [ ] Links quebrados corrigidos
- [ ] Instruções de instalação claras
- [ ] Variáveis de ambiente documentadas

### Fase 5: Migração de Histórico Git (Opcional)

Se necessário preservar histórico:

```bash
# No repositório backend
git subtree push --prefix=frontend origin frontend-extracted

# Ou usar git filter-branch
git filter-branch --subdirectory-filter frontend -- --all
```

**Nota:** Por simplicidade, pode-se criar novo histórico no repositório frontend.

### Fase 6: CI/CD e Deploy

#### Etapa 6.1: Configurar CI/CD no Novo Repositório

**GitHub Actions (.github/workflows/ci.yml):**

```yaml
name: Frontend CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run build
      # Deploy para Vercel/Netlify/etc
```

### Fase 7: Comunicação e Documentação

#### Etapa 7.1: Atualizar Links Externos

- [ ] README.md principal atualizado
- [ ] Documentação de API atualizada
- [ ] Wiki atualizado (se existir)
- [ ] Comunidade informada (Discord, etc.)

#### Etapa 7.2: Criar Guia de Migração para Desenvolvedores

Documento para desenvolvedores que precisam adaptar seus workflows.

---

## 📦 Arquivos a Migrar

### Código Fonte (100% do diretório frontend/)

```
frontend/
├── src/                    ✅ Migrar tudo
├── public/                 ✅ Migrar tudo (se existir)
├── package.json           ✅ Migrar e atualizar
├── package-lock.json      ✅ Migrar
├── tsconfig.json          ✅ Migrar
├── next.config.js         ✅ Migrar e atualizar
├── tailwind.config.ts     ✅ Migrar
├── postcss.config.js      ✅ Migrar
├── .eslintrc.json         ✅ Migrar (se existir)
├── .prettierrc            ✅ Migrar (se existir)
├── .env.example           ✅ Migrar
├── README.md              ✅ Migrar e atualizar
├── OVERVIEW.md            ✅ Migrar
├── INSTRUCOES.md          ✅ Migrar
└── test-connection.js     ✅ Migrar (se necessário)
```

### Documentação Específica

```
docs/frontend/             ✅ Migrar tudo
├── README.md
├── QUICK_START.md
├── COMPONENTES_UI.md
├── GUIA_TESTES.md
├── GUIA_DEPLOY.md
├── EXEMPLOS_COMPLETOS.md
└── TROUBLESHOOTING.md
```

### Documentação de Referência

```
docs/MANUAL_INTEGRACAO_FRONTEND.md  ⚠️ Migrar ou manter como referência
FRONTEND_COMPLETO.md                 ⚠️ Migrar ou manter como referência
```

### Arquivos de Configuração

```
.gitignore                  ✅ Criar novo específico
.env.example                ✅ Migrar
.env.local                  ❌ Não migrar (gitignored)
```

---

## 🔄 Mudanças Necessárias em Arquivos

### 1. `frontend/src/lib/api/client.ts`

**Mudança:** Nenhuma - já usa variáveis de ambiente

**Verificar:**
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
```

### 2. `frontend/next.config.js`

**Mudança:** Opcional - remover rewrites se não necessário

**Atual:**
```javascript
async rewrites() {
  return [
    {
      source: '/api/:path*',
      destination: `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/:path*`,
    },
  ];
}
```

**Pode manter ou remover** dependendo da estratégia de deploy.

### 3. `frontend/README.md`

**Mudanças Necessárias:**

1. **Remover referências a `../docs/`**
2. **Atualizar links para documentação local**
3. **Adicionar seção sobre repositório backend**
4. **Atualizar instruções de instalação**

**Exemplo:**

```markdown
## 📚 Documentação

Toda a documentação está no próprio repositório:

- [Quick Start](docs/QUICK_START.md)
- [Componentes UI](docs/COMPONENTES_UI.md)
- [Guia de Testes](docs/GUIA_TESTES.md)
- [Guia de Deploy](docs/GUIA_DEPLOY.md)

## 🔗 Backend

Este frontend consome a API do backend CoinBalance:

- **Repositório Backend**: [coinbalance/coinbalance](https://github.com/coinbalance/coinbalance)
- **API URL**: Configure via `NEXT_PUBLIC_API_URL`
- **Documentação API**: http://localhost:8000/docs (quando backend rodando)
```

### 4. Documentação de Referência Cruzada

**Arquivos a Atualizar no Backend:**

- `README.md` - Adicionar seção sobre frontend separado
- `CONTRIBUTING.md` - Atualizar instruções
- `docs/README.md` - Atualizar índices

---

## 🚨 Plano de Rollback

Se houver problemas, fazer rollback:

### Rollback Completo

```bash
# 1. Restaurar frontend no repositório backend
git checkout <commit-anterior> -- frontend/
git commit -m "revert: restore frontend directory"

# 2. Remover novo repositório (se necessário)
# 3. Atualizar README.md para estado anterior
```

### Rollback Parcial

- Manter ambos repositórios temporariamente
- Migrar gradualmente
- Remover frontend do backend após validação completa

---

## 📋 Checklist Final de Migração

### Antes da Migração

- [ ] Backup completo do repositório atual
- [ ] Testes do frontend passando (100%)
- [ ] Build funcionando
- [ ] Documentação atualizada
- [ ] Equipe informada

### Durante a Migração

- [ ] Criar novo repositório
- [ ] Copiar todos os arquivos
- [ ] Atualizar configurações
- [ ] Criar README.md completo
- [ ] Configurar CI/CD
- [ ] Validar build e testes

### Após Migração

- [ ] Remover frontend do repositório backend
- [ ] Atualizar README.md do backend
- [ ] Atualizar .gitignore do backend
- [ ] Atualizar docker-compose.yml do backend
- [ ] Testar integração completa
- [ ] Atualizar links externos
- [ ] Comunicação com equipe

### Validação Final

- [ ] Frontend builda corretamente
- [ ] Frontend conecta com backend
- [ ] Todos os fluxos funcionam
- [ ] Documentação está correta
- [ ] CI/CD funcionando
- [ ] Deploy de teste bem-sucedido

---

## 📚 Estrutura Final do Novo Repositório

```
coinbalance-frontend/
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD
├── docs/                       # Documentação específica
│   ├── README.md
│   ├── QUICK_START.md
│   ├── COMPONENTES_UI.md
│   ├── GUIA_TESTES.md
│   ├── GUIA_DEPLOY.md
│   ├── EXEMPLOS_COMPLETOS.md
│   ├── TROUBLESHOOTING.md
│   ├── OVERVIEW.md
│   ├── INSTRUCOES.md
│   └── MANUAL_INTEGRACAO_FRONTEND.md
├── public/                     # Assets estáticos
├── src/                        # Código fonte
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── services/
│   └── types/
├── .env.example                # Variáveis de ambiente exemplo
├── .gitignore                  # Git ignore específico
├── .eslintrc.json              # ESLint config
├── .prettierrc                 # Prettier config
├── Dockerfile                  # Docker para produção
├── docker-compose.yml          # Docker Compose independente
├── next.config.js              # Next.js config
├── package.json                # Dependências npm
├── package-lock.json           # Lock file
├── postcss.config.js           # PostCSS config
├── tailwind.config.ts          # Tailwind config
├── tsconfig.json               # TypeScript config
└── README.md                   # README principal
```

---

## 🎯 Estratégia de Versionamento

### Convenções de Versionamento

**Frontend:**
- `v1.0.0` - Versão inicial após migração
- Semver: `MAJOR.MINOR.PATCH`
- Tags: `v1.0.0`, `v1.1.0`, etc.

**Backend:**
- Continuar com `v3.0.0+`
- Frontend e backend podem ter versões diferentes

### Compatibilidade de Versões

**Documentar no README:**

```markdown
## 🔗 Compatibilidade

| Frontend Version | Backend Version | Status |
|------------------|-----------------|--------|
| 1.0.0           | 3.0.0+          | ✅ Compatível |
```

---

## 📝 Template de README.md para Novo Repositório

```markdown
# 🌐 CoinBalance Frontend

Frontend da plataforma CoinBalance - Blockchain Enterprise com IA e Web3.

> **📦 Backend:** Este frontend consome a API do backend CoinBalance.  
> Consulte [coinbalance/coinbalance](https://github.com/coinbalance/coinbalance) para o backend.

## 🚀 Início Rápido

[Conteúdo do README atual...]

## 🔗 Links Importantes

- **Backend API**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs
- **Repositório Backend**: [coinbalance/coinbalance](https://github.com/coinbalance/coinbalance)
```

---

## ✅ Lista de Verificação Pré-Execução

Antes de executar a migração, verificar:

- [ ] ✅ Todos os testes passando
- [ ] ✅ Build funcionando
- [ ] ✅ Dependências instaladas
- [ ] ✅ Documentação revisada
- [ ] ✅ Equipe informada
- [ ] ✅ Backup realizado
- [ ] ✅ Plano de rollback definido
- [ ] ✅ Novo repositório preparado
- [ ] ✅ CI/CD configurado
- [ ] ✅ Aprovação do plano

---

## 📅 Timeline Estimado

| Fase | Duração | Responsável |
|------|---------|-------------|
| **Fase 1**: Preparação | 1-2 horas | DevOps |
| **Fase 2**: Configuração | 2-3 horas | Frontend Lead |
| **Fase 3**: Atualização Backend | 1-2 horas | Backend Lead |
| **Fase 4**: Validação | 2-3 horas | QA |
| **Fase 5**: Migração Git | 1 hora | DevOps |
| **Fase 6**: CI/CD | 2-3 horas | DevOps |
| **Fase 7**: Comunicação | 1 hora | Tech Lead |
| **Total** | **10-16 horas** | Equipe |

---

## 🎯 Próximos Passos

1. **Revisar este plano** com a equipe
2. **Criar novo repositório** no GitHub
3. **Executar migração** seguindo este plano
4. **Validar** todos os pontos do checklist
5. **Comunicar** mudanças para stakeholders

---

**Versão do Documento:** 1.0.0  
**Última Atualização:** 29 de outubro de 2025  
**Status:** ✅ Pronto para Execução

