# 🌐 CoinBalance Frontend

Frontend da plataforma CoinBalance - Blockchain Enterprise com IA e Web3.

> **📦 Backend:** Este frontend consome a API do backend CoinBalance.  
> Consulte [coinbalance/coinbalance](https://github.com/coinbalance/coinbalance) para o backend.

## 📋 Sobre Este Template

Este é um template para o README do repositório frontend separado (`coinbalance-frontend`). Quando usado, substitua os valores de exemplo pelos reais do seu projeto.

### **Parâmetros para Personalização**

- `[nome-do-projeto]`: Nome do repositório frontend (ex: `coinbalance-frontend`)
- `[url-do-backend]`: URL do repositório backend (ex: `https://github.com/coinbalance/coinbalance`)
- `[versao]`: Versão do frontend (ex: `1.0.0`)
- `[porta]`: Porta padrão do frontend (ex: `3000`)
- `[api-url]`: URL da API backend (ex: `http://localhost:8000`)

[![Next.js](https://img.shields.io/badge/Next.js-14.0-black)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-18.2-blue)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38bdf8)](https://tailwindcss.com/)

---

## 🚀 Início Rápido

### Pré-requisitos

- **Node.js** 18+ 
- **npm** 9+

### Instalação

```bash
# Clonar repositório
git clone https://github.com/coinbalance/coinbalance-frontend.git
cd coinbalance-frontend

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env.local

# Editar .env.local com suas configurações
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Desenvolvimento

```bash
# Iniciar servidor de desenvolvimento
npm run dev

# Abrir http://localhost:3000
```

### Build Produção

```bash
# Build para produção
npm run build

# Executar build de produção
npm start
```

---

## 📚 Documentação

Toda a documentação está disponível no próprio repositório:

- 📖 [Quick Start](docs/QUICK_START.md) - Guia rápido de início
- 🧩 [Componentes UI](docs/COMPONENTES_UI.md) - Documentação de componentes
- 🧪 [Guia de Testes](docs/GUIA_TESTES.md) - Como executar testes
- 🚀 [Guia de Deploy](docs/GUIA_DEPLOY.md) - Deploy em produção
- 📝 [Exemplos Completos](docs/EXEMPLOS_COMPLETOS.md) - Exemplos de uso
- 🔧 [Troubleshooting](docs/TROUBLESHOOTING.md) - Solução de problemas
- 📋 [Manual de Integração](docs/MANUAL_INTEGRACAO_FRONTEND.md) - Integração com backend

---

## 🔗 Links Importantes

- **Backend API**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs (quando backend rodando)
- **Repositório Backend**: [coinbalance/coinbalance](https://github.com/coinbalance/coinbalance)
- **Health Check Backend**: http://localhost:8000/api/v1/health

---

## 🏗️ Estrutura do Projeto

```
coinbalance-frontend/
├── src/
│   ├── app/                # Next.js App Router
│   │   ├── page.tsx       # Home page
│   │   ├── login/         # Login page
│   │   └── dashboard/     # Dashboard pages
│   ├── components/         # Componentes React
│   │   ├── ui/            # UI Components base
│   │   └── layout/        # Layout components
│   ├── lib/               # Utilitários
│   │   ├── api/          # API client
│   │   └── utils.ts      # Funções utilitárias
│   ├── services/          # Serviços de integração
│   └── types/             # TypeScript types
├── public/                 # Assets estáticos
├── docs/                   # Documentação
└── ...
```

---

## 🛠️ Stack Tecnológico

- **Framework**: Next.js 14 + React 18
- **Linguagem**: TypeScript 5
- **Styling**: Tailwind CSS 3
- **State Management**: Zustand + React Query
- **Forms**: React Hook Form + Zod
- **Charts**: Recharts
- **Testing**: Vitest + Playwright
- **Animations**: Framer Motion
- **Icons**: Lucide React

---

## 🧪 Testes

```bash
# Testes unitários
npm test

# Testes com UI
npm run test:ui

# Coverage
npm run test:coverage

# Testes E2E
npm run test:e2e

# Testes E2E com UI
npm run test:e2e:ui
```

---

## 📦 Deploy

Este frontend pode ser deployado em várias plataformas:

- **Vercel** (recomendado para Next.js)
- **Netlify**
- **Docker**
- **AWS Amplify**
- **Azure Static Web Apps**

Veja [Guia de Deploy](docs/GUIA_DEPLOY.md) para instruções detalhadas.

### Deploy com Docker

```bash
# Build da imagem
docker build -t coinbalance-frontend .

# Executar container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  coinbalance-frontend
```

### Deploy com Docker Compose

```bash
docker-compose up -d
```

---

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env.local` na raiz do projeto:

```env
# API Backend URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# API Version (opcional)
NEXT_PUBLIC_API_VERSION=v1

# JWT Storage Key (opcional)
NEXT_PUBLIC_JWT_STORAGE_KEY=authToken
```

### Configuração de Build

O Next.js já está configurado para produção. Para builds otimizados:

```bash
# Build standalone para Docker
npm run build
```

---

## 🔗 Compatibilidade

| Frontend Version | Backend Version | Status |
|------------------|-----------------|--------|
| 1.0.0           | 3.0.0+          | ✅ Compatível |

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE.md](LICENSE.md) para mais detalhes.

---

## 👥 Equipe

Desenvolvido pela equipe CoinBalance.

---

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/coinbalance/coinbalance-frontend/issues)
- **Documentação**: [docs/](docs/)
- **Backend**: [coinbalance/coinbalance](https://github.com/coinbalance/coinbalance)

---

**Versão:** 1.0.0  
**Última Atualização:** Outubro 2025

