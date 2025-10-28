# 🌐 CoinBalance Frontend

Frontend da plataforma CoinBalance - Blockchain Enterprise com IA e Web3.

## 🚀 Início Rápido

### Pré-requisitos

- Node.js 18+
- npm 9+

### Instalação

```bash
# Instalar dependências
npm install

# Copiar variáveis de ambiente
cp .env.example .env.local

# Editar .env.local com suas configurações
```

### Desenvolvimento

```bash
# Iniciar servidor de desenvolvimento
npm run dev

# Abrir http://localhost:3000
```

### Build

```bash
# Build para produção
npm run build

# Iniciar servidor de produção
npm start
```

## 📚 Documentação

A documentação completa está disponível em:

- [Documentação Frontend](../docs/frontend/README.md)
- [Manual de Integração](../docs/MANUAL_INTEGRACAO_FRONTEND.md)
- [Quick Start](../docs/frontend/QUICK_START.md)
- [Guia de Componentes](../docs/frontend/COMPONENTES_UI.md)

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
```

## 🏗️ Estrutura do Projeto

```
src/
├── app/                # Next.js App Router
├── components/         # Componentes React
├── lib/               # Utilitários e configurações
├── services/          # Serviços de API
├── types/             # TypeScript types
└── styles/            # Estilos globais
```

## 🛠️ Stack Tecnológico

- **Framework**: Next.js 14 + React 18
- **Linguagem**: TypeScript 5
- **Styling**: Tailwind CSS 3
- **State**: Zustand + React Query
- **Forms**: React Hook Form + Zod
- **Charts**: Recharts
- **Testing**: Vitest + Playwright
- **Animations**: Framer Motion

## 📦 Build e Deploy

Veja o [Guia de Deploy](../docs/frontend/GUIA_DEPLOY.md) para instruções detalhadas sobre como fazer deploy em:

- Vercel
- Netlify  
- Docker
- AWS

## 🤝 Contribuindo

Veja [CONTRIBUTING.md](../CONTRIBUTING.md) para detalhes sobre como contribuir.

## 📄 Licença

MIT License - veja [LICENSE.md](../LICENSE.md) para detalhes.

---

**Desenvolvido com ❤️ pela equipe CoinBalance**
