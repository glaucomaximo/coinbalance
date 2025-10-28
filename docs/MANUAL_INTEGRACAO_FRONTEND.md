# 🌐 Manual de Integração Front-End - CoinBalance

## 📋 Índice

### Parte I - Visão Geral e Conceito
1. [O que é CoinBalance](#o-que-é-coinbalance)
2. [Visão do Produto](#visão-do-produto)
3. [Arquitetura do Frontend](#arquitetura-do-frontend)

### Parte II - Design e Experiência do Usuário
4. [Design System](#design-system)
5. [Interface Responsiva](#interface-responsiva)
6. [Experiência Imersiva](#experiência-imersiva)
7. [Componentes UI](#componentes-ui)

### Parte III - Implementação Técnica
8. [Configuração Inicial](#configuração-inicial)
9. [Autenticação e Autorização](#autenticação-e-autorização)
10. [Módulos da API](#módulos-da-api)
11. [Exemplos de Integração](#exemplos-de-integração)

### Parte IV - Qualidade e Manutenção
12. [Tratamento de Erros](#tratamento-de-erros)
13. [Boas Práticas](#boas-práticas)
14. [SDK JavaScript/TypeScript](#sdk-javascripttypescript)
15. [Testes e Debugging](#testes-e-debugging)

### Parte V - Referência
16. [Referência Completa de Endpoints](#referência-completa-de-endpoints)
17. [Roadmap de Implementação](#roadmap-de-implementação)

---

# PARTE I - VISÃO GERAL E CONCEITO

## 🚀 O que é CoinBalance

### Visão Geral do Projeto

**CoinBalance** é uma **plataforma blockchain enterprise completa** que representa a próxima geração de economia digital consciente e descentralizada. O projeto combina tecnologia blockchain nativa, inteligência artificial avançada e integração Web3 para criar um ecossistema financeiro digital revolucionário.

### 🎯 Missão e Propósito

> "Democratizar o acesso à tecnologia blockchain através de uma plataforma enterprise intuitiva, segura e altamente escalável, capacitando indivíduos e organizações a participarem da economia digital do futuro."

### 🏆 Características Principais do Ecossistema

#### 1. **Blockchain Enterprise Nativa**
- **Proof of Work Real**: Sistema de mineração paralela com threading otimizado
- **Escalabilidade Horizontal**: Sharding automático com 1000x mais performance
- **Validação Incremental**: Cache inteligente com 80%+ de taxa de acerto
- **Busca O(1)**: Índices múltiplos para consultas instantâneas

#### 2. **Inteligência Artificial Integrada**
- **6 Modelos ML Especializados**: RandomForest, GradientBoosting, Ridge, LinearRegression
- **Predição de Mercado**: Análise preditiva em 8 timeframes diferentes
- **Economia Autônoma**: Sistema que toma decisões econômicas automaticamente
- **Criação de Tokens IA**: Geração automática de criptomoedas inteligentes

#### 3. **Web3 Completo**
- **Cross-Chain Bridge**: Integração com Ethereum, BSC, Polygon, Arbitrum, Optimism
- **DeFi Protocols**: Yield farming, staking, liquidity pools
- **NFT Marketplace**: Suporte ERC-721, ERC-1155, ERC-4907
- **DAO Governance**: Governança descentralizada com votação on-chain

#### 4. **Segurança Enterprise**
- **Conformidade LGPD**: Sistema completo de proteção de dados
- **Auditoria Completa**: Logging estruturado de todas as operações
- **Criptografia Avançada**: AES-256-GCM e RSA 2048+
- **Autenticação JWT**: Tokens com escopos granulares e refresh automático

#### 5. **Monitoramento em Tempo Real**
- **Prometheus & Grafana**: Dashboards personalizáveis
- **Métricas Avançadas**: CPU, memória, rede, blockchain, IA, Web3
- **Alertas Inteligentes**: Sistema de notificações com múltiplos níveis
- **Análise de Tendências**: Detecção de anomalias e padrões

### 📊 Estatísticas e Métricas

| Métrica | Valor | Descrição |
|---------|-------|-----------|
| **Arquivos de Código** | 235+ | Componentes mapeados e documentados |
| **Requisitos** | 62 | 39 funcionais + 23 não-funcionais |
| **Cobertura de Testes** | 100% | 81/81 testes unitários passando |
| **Endpoints API** | 244+ | Endpoints REST completos |
| **Manutenibilidade** | 8.9/10 | Código limpo e bem estruturado |
| **Performance** | 1000x | Escalabilidade horizontal |
| **Modelos IA** | 6 | Modelos de ML especializados |

### 🎨 Stack Tecnológico Backend

```
┌─────────────────────────────────────────────────────────┐
│                    COINBALANCE BACKEND                   │
├─────────────────────────────────────────────────────────┤
│ • Python 3.11+                                           │
│ • FastAPI (Framework Web)                                │
│ • SQLAlchemy (ORM)                                       │
│ • PostgreSQL / SQLite (Database)                         │
│ • Redis (Cache Distribuído)                              │
│ • Scikit-learn (Machine Learning)                        │
│ • Web3.py (Integração Blockchain)                        │
│ • Prometheus (Métricas)                                  │
│ • Docker & Docker Compose (Containerização)              │
└─────────────────────────────────────────────────────────┘
```

### 🏗️ Arquitetura Enterprise

O CoinBalance segue os mais rigorosos padrões de arquitetura enterprise:

- **Domain-Driven Design (DDD)**: Modelagem baseada no domínio
- **Clean Architecture**: Separação clara de responsabilidades
- **CQRS**: Separação de comandos e consultas
- **Event Sourcing**: Auditoria completa de eventos
- **Repository Pattern**: Abstração de persistência
- **Dependency Injection**: Inversão de dependências

```
┌─────────────────────────────────────────────────────────┐
│                   CAMADA DE APRESENTAÇÃO                 │
│              (API REST, WebSocket, GraphQL)              │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  CAMADA DE APLICAÇÃO                     │
│           (Use Cases, Serviços, Handlers)                │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    CAMADA DE DOMÍNIO                     │
│        (Entidades, Value Objects, Domain Events)         │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                CAMADA DE INFRAESTRUTURA                  │
│     (Repositórios, Web3, IA, Monitoramento, Cache)       │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Visão do Produto

### Frontend CoinBalance - Plataforma Web Imersiva

O **Frontend CoinBalance** é uma aplicação web moderna, responsiva e imersiva que serve como interface principal para todo o ecossistema blockchain. Desenvolvido com as tecnologias mais avançadas do mercado, oferece uma experiência de usuário excepcional tanto para iniciantes quanto para usuários avançados.

### 🌟 Características do Frontend

#### 1. **Interface Moderna e Intuitiva**
- Design minimalista e clean
- Tipografia hierárquica clara
- Paleta de cores profissional
- Animações sutis e fluidas
- Feedback visual imediato

#### 2. **Totalmente Responsivo**
- Mobile-first design
- Breakpoints otimizados (320px - 4K)
- Touch gestures para mobile
- PWA (Progressive Web App)
- Offline-first quando possível

#### 3. **Experiência Imersiva**
- Transições suaves entre páginas
- Loading states elegantes
- Real-time updates via WebSocket
- Gráficos interativos e animados
- Dashboards personalizáveis

#### 4. **Acessibilidade (WCAG 2.1 AA)**
- Suporte a leitores de tela
- Navegação por teclado completa
- Contraste de cores adequado
- Labels e ARIA attributes
- Modo de alto contraste

#### 5. **Performance Otimizada**
- Code splitting automático
- Lazy loading de componentes
- Image optimization
- Bundle size < 500KB (inicial)
- Time to Interactive < 3s

### 🎯 Módulos Principais do Frontend

#### 1. **Dashboard Executivo**
```
┌─────────────────────────────────────────────────────────┐
│  DASHBOARD - VISÃO GERAL                                 │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│
│  │ Saldo    │  │ Volume   │  │ Transações│  │ Blocos   ││
│  │ Total    │  │ 24h      │  │ Pendentes │  │ Minerados││
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘│
│                                                           │
│  ┌─────────────────────────────────────────────────────┐│
│  │ Gráfico de Saldo (7 dias)                            ││
│  │ [Área chart com gradiente]                           ││
│  └─────────────────────────────────────────────────────┘│
│                                                           │
│  ┌────────────────────┐  ┌──────────────────────────┐  │
│  │ Atividade Recente  │  │ Quick Actions            │  │
│  │ • Transferência... │  │ [Transferir] [Receber]   │  │
│  │ • Crédito...       │  │ [Minerar] [Stake]        │  │
│  └────────────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

#### 2. **Carteiras Digitais**
- Listagem de todas as carteiras
- Criação de novas carteiras
- Detalhes e histórico por carteira
- QR Code para recebimento
- Exportação de chaves

#### 3. **Transferências e Transações**
- Formulário de transferência intuitivo
- Histórico completo paginado
- Filtros avançados (data, tipo, status)
- Exportação para CSV/PDF
- Detalhes de cada transação

#### 4. **Blockchain Explorer**
- Visualização de blocos em tempo real
- Detalhes de cada bloco
- Estatísticas da blockchain
- Gráficos de performance
- Validação de transações

#### 5. **Mineração**
- Dashboard de mineração
- Estatísticas de hashrate
- Pool de mineração
- Recompensas acumuladas
- Controle de mineração

#### 6. **Web3 e DeFi**
- Conexão com carteiras externas (MetaMask)
- Yield farming e staking
- NFT marketplace
- Cross-chain bridge
- DAO governance

#### 7. **IA e Analytics**
- Predições de mercado
- Análise de sentimento
- Recomendações automáticas
- Gráficos preditivos
- Insights personalizados

#### 8. **Configurações e Perfil**
- Gerenciamento de conta
- Preferências de notificação
- Temas (Light/Dark/Auto)
- Configurações de segurança
- Logs de atividade

### 🎨 Stack Tecnológico Frontend

```
┌─────────────────────────────────────────────────────────┐
│                   COINBALANCE FRONTEND                   │
├─────────────────────────────────────────────────────────┤
│ Core Framework                                           │
│ • React 18+ ou Next.js 14+                               │
│ • TypeScript 5+                                          │
│ • Vite ou Next.js (Build Tool)                           │
│                                                           │
│ State Management                                         │
│ • Zustand ou Redux Toolkit                               │
│ • React Query (TanStack Query)                           │
│ • Jotai (Atomic State)                                   │
│                                                           │
│ UI & Styling                                             │
│ • Tailwind CSS 3+                                        │
│ • Shadcn/ui ou Radix UI                                  │
│ • Framer Motion (Animações)                              │
│ • Lucide React (Ícones)                                  │
│                                                           │
│ Data Visualization                                       │
│ • Recharts ou Victory Charts                             │
│ • D3.js (Visualizações avançadas)                        │
│ • React Flow (Grafos)                                    │
│                                                           │
│ Forms & Validation                                       │
│ • React Hook Form                                        │
│ • Zod (Schema Validation)                                │
│                                                           │
│ Web3 Integration                                         │
│ • Wagmi                                                  │
│ • Viem                                                   │
│ • RainbowKit                                             │
│                                                           │
│ Testing                                                  │
│ • Vitest ou Jest                                         │
│ • React Testing Library                                  │
│ • Playwright (E2E)                                       │
│                                                           │
│ DevOps                                                   │
│ • Docker                                                 │
│ • Nginx                                                  │
│ • Vercel/Netlify/AWS                                     │
└─────────────────────────────────────────────────────────┘
```

### 📱 Responsividade - Breakpoints

```css
/* Mobile First Approach */
/* Extra Small Devices (Phones, < 576px) */
@media (max-width: 575.98px) { }

/* Small Devices (Landscape Phones, >= 576px) */
@media (min-width: 576px) { }

/* Medium Devices (Tablets, >= 768px) */
@media (min-width: 768px) { }

/* Large Devices (Desktops, >= 992px) */
@media (min-width: 992px) { }

/* Extra Large Devices (Large Desktops, >= 1200px) */
@media (min-width: 1200px) { }

/* XXL Devices (4K Screens, >= 1400px) */
@media (min-width: 1400px) { }
```

---

## 🏛️ Arquitetura do Frontend

### Estrutura de Diretórios Recomendada

```
coinbalance-frontend/
├── public/                      # Arquivos estáticos
│   ├── favicon.ico
│   ├── logo.svg
│   └── manifest.json
│
├── src/
│   ├── app/                     # Next.js App Router (ou pages/)
│   │   ├── (auth)/             # Rotas de autenticação
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── (dashboard)/        # Rotas do dashboard
│   │   │   ├── page.tsx
│   │   │   ├── wallets/
│   │   │   ├── transactions/
│   │   │   ├── blockchain/
│   │   │   ├── mining/
│   │   │   ├── web3/
│   │   │   ├── ai/
│   │   │   └── settings/
│   │   ├── layout.tsx          # Layout principal
│   │   └── providers.tsx       # Providers globais
│   │
│   ├── components/              # Componentes reutilizáveis
│   │   ├── ui/                 # Componentes base (shadcn/ui)
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── input.tsx
│   │   │   ├── table.tsx
│   │   │   └── ...
│   │   ├── layout/             # Componentes de layout
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Navigation.tsx
│   │   ├── wallet/             # Componentes de carteira
│   │   │   ├── WalletCard.tsx
│   │   │   ├── WalletList.tsx
│   │   │   ├── CreateWalletModal.tsx
│   │   │   └── WalletBalance.tsx
│   │   ├── transaction/        # Componentes de transação
│   │   │   ├── TransactionList.tsx
│   │   │   ├── TransactionDetails.tsx
│   │   │   ├── TransferForm.tsx
│   │   │   └── TransactionStatus.tsx
│   │   ├── blockchain/         # Componentes blockchain
│   │   │   ├── BlockList.tsx
│   │   │   ├── BlockDetails.tsx
│   │   │   └── BlockchainStats.tsx
│   │   ├── charts/             # Componentes de gráficos
│   │   │   ├── LineChart.tsx
│   │   │   ├── AreaChart.tsx
│   │   │   ├── BarChart.tsx
│   │   │   └── PieChart.tsx
│   │   └── common/             # Componentes comuns
│   │       ├── Loading.tsx
│   │       ├── ErrorBoundary.tsx
│   │       ├── Toast.tsx
│   │       └── Empty.tsx
│   │
│   ├── lib/                    # Bibliotecas e utilitários
│   │   ├── api/                # Cliente API
│   │   │   ├── client.ts
│   │   │   ├── endpoints.ts
│   │   │   └── types.ts
│   │   ├── hooks/              # React Hooks customizados
│   │   │   ├── useAuth.ts
│   │   │   ├── useWallet.ts
│   │   │   ├── useTransaction.ts
│   │   │   └── useWebSocket.ts
│   │   ├── utils/              # Funções utilitárias
│   │   │   ├── format.ts
│   │   │   ├── validation.ts
│   │   │   ├── crypto.ts
│   │   │   └── date.ts
│   │   └── constants/          # Constantes
│   │       ├── routes.ts
│   │       ├── config.ts
│   │       └── theme.ts
│   │
│   ├── services/               # Serviços de negócio
│   │   ├── auth.service.ts
│   │   ├── wallet.service.ts
│   │   ├── transaction.service.ts
│   │   ├── blockchain.service.ts
│   │   └── web3.service.ts
│   │
│   ├── store/                  # State Management
│   │   ├── slices/
│   │   │   ├── auth.slice.ts
│   │   │   ├── wallet.slice.ts
│   │   │   └── ui.slice.ts
│   │   └── index.ts
│   │
│   ├── types/                  # TypeScript Types
│   │   ├── api.types.ts
│   │   ├── wallet.types.ts
│   │   ├── transaction.types.ts
│   │   └── blockchain.types.ts
│   │
│   ├── styles/                 # Estilos globais
│   │   ├── globals.css
│   │   ├── variables.css
│   │   └── animations.css
│   │
│   └── middleware.ts           # Next.js Middleware
│
├── tests/                      # Testes
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── .env.example                # Variáveis de ambiente exemplo
├── .eslintrc.json             # ESLint config
├── .prettierrc                # Prettier config
├── next.config.js             # Next.js config
├── tailwind.config.ts         # Tailwind config
├── tsconfig.json              # TypeScript config
├── package.json
└── README.md
```

### 🔄 Fluxo de Dados

```
┌──────────────┐
│   USUÁRIO    │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│              COMPONENTES REACT                        │
│  (Apresentação, Interação, Validação)                │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│              HOOKS CUSTOMIZADOS                       │
│  (Lógica de Negócio, Side Effects)                   │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│           SERVIÇOS / SDK COINBALANCE                  │
│  (Abstração da API, Transformação de Dados)          │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│              CLIENTE HTTP (AXIOS)                     │
│  (Interceptors, Headers, Error Handling)             │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│            API COINBALANCE BACKEND                    │
│  (FastAPI, PostgreSQL, Redis, ML)                    │
└──────────────────────────────────────────────────────┘
```

---

# PARTE II - DESIGN E EXPERIÊNCIA DO USUÁRIO

## 🎨 Design System

### Paleta de Cores

```css
/* Primary Colors - Identidade da Marca */
--primary-50: #f0f9ff;
--primary-100: #e0f2fe;
--primary-200: #bae6fd;
--primary-300: #7dd3fc;
--primary-400: #38bdf8;
--primary-500: #0ea5e9;  /* Primary Main */
--primary-600: #0284c7;
--primary-700: #0369a1;
--primary-800: #075985;
--primary-900: #0c4a6e;

/* Secondary Colors - Acentos */
--secondary-50: #faf5ff;
--secondary-100: #f3e8ff;
--secondary-200: #e9d5ff;
--secondary-300: #d8b4fe;
--secondary-400: #c084fc;
--secondary-500: #a855f7;  /* Secondary Main */
--secondary-600: #9333ea;
--secondary-700: #7e22ce;
--secondary-800: #6b21a8;
--secondary-900: #581c87;

/* Success */
--success-500: #10b981;
--success-600: #059669;

/* Warning */
--warning-500: #f59e0b;
--warning-600: #d97706;

/* Error */
--error-500: #ef4444;
--error-600: #dc2626;

/* Neutral Colors */
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-400: #9ca3af;
--gray-500: #6b7280;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-800: #1f2937;
--gray-900: #111827;

/* Dark Mode */
--dark-bg: #0a0a0a;
--dark-surface: #141414;
--dark-border: #262626;
```

### Tipografia

```css
/* Font Families */
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;

/* Font Sizes */
--text-xs: 0.75rem;     /* 12px */
--text-sm: 0.875rem;    /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg: 1.125rem;    /* 18px */
--text-xl: 1.25rem;     /* 20px */
--text-2xl: 1.5rem;     /* 24px */
--text-3xl: 1.875rem;   /* 30px */
--text-4xl: 2.25rem;    /* 36px */
--text-5xl: 3rem;       /* 48px */

/* Font Weights */
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* Line Heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

### Espaçamento

```css
/* Spacing Scale (8px base) */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
```

### Sombras e Elevações

```css
/* Shadows */
--shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
--shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);

/* Glow Effects */
--glow-primary: 0 0 20px rgba(14, 165, 233, 0.4);
--glow-secondary: 0 0 20px rgba(168, 85, 247, 0.4);
```

### Bordas e Raios

```css
/* Border Radius */
--radius-sm: 0.25rem;   /* 4px */
--radius-md: 0.375rem;  /* 6px */
--radius-lg: 0.5rem;    /* 8px */
--radius-xl: 0.75rem;   /* 12px */
--radius-2xl: 1rem;     /* 16px */
--radius-full: 9999px;

/* Border Widths */
--border-1: 1px;
--border-2: 2px;
--border-4: 4px;
```

### Animações e Transições

```css
/* Durations */
--duration-fast: 150ms;
--duration-normal: 300ms;
--duration-slow: 500ms;

/* Easing Functions */
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);

/* Transitions */
--transition-all: all var(--duration-normal) var(--ease-in-out);
--transition-colors: color var(--duration-fast) var(--ease-in-out),
                     background-color var(--duration-fast) var(--ease-in-out),
                     border-color var(--duration-fast) var(--ease-in-out);
```

---

## 📱 Interface Responsiva

### Princípios de Design Responsivo

#### 1. **Mobile First**
Começar o design pela menor tela e progressivamente adicionar funcionalidades para telas maiores.

```tsx
// Exemplo de componente responsivo
export const WalletCard = ({ wallet }: Props) => {
  return (
    <div className="
      /* Mobile (padrão) */
      p-4 
      space-y-3
      
      /* Tablet */
      md:p-6 
      md:space-y-4
      
      /* Desktop */
      lg:p-8 
      lg:flex 
      lg:items-center 
      lg:justify-between
      lg:space-y-0
    ">
      {/* Conteúdo */}
    </div>
  );
};
```

#### 2. **Layouts Flexíveis**
Usar Grid e Flexbox para layouts adaptativos.

```tsx
// Grid responsivo
<div className="
  grid 
  grid-cols-1 
  gap-4
  
  sm:grid-cols-2
  md:grid-cols-3
  lg:grid-cols-4
  xl:grid-cols-6
">
  {wallets.map(wallet => (
    <WalletCard key={wallet.id} wallet={wallet} />
  ))}
</div>
```

#### 3. **Imagens Responsivas**
```tsx
<Image
  src="/wallet-bg.jpg"
  alt="Wallet Background"
  width={800}
  height={600}
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  className="object-cover"
/>
```

#### 4. **Navegação Adaptativa**

```tsx
// Desktop: Sidebar permanente
// Tablet: Sidebar colapsável
// Mobile: Menu hambúrguer com drawer

export const Navigation = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  
  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex lg:w-64 lg:flex-col">
        <SidebarContent />
      </aside>
      
      {/* Mobile Header */}
      <header className="lg:hidden">
        <button onClick={() => setIsMobileMenuOpen(true)}>
          <Menu />
        </button>
      </header>
      
      {/* Mobile Drawer */}
      <Drawer 
        open={isMobileMenuOpen} 
        onClose={() => setIsMobileMenuOpen(false)}
      >
        <SidebarContent />
      </Drawer>
    </>
  );
};
```

### Componentes Responsivos Essenciais

#### 1. **Cards Adaptativos**
```tsx
export const StatCard = ({ title, value, trend }: Props) => {
  return (
    <Card className="
      /* Mobile: Stack vertical */
      flex flex-col space-y-2
      
      /* Desktop: Horizontal com mais espaço */
      lg:flex-row lg:items-center lg:justify-between lg:space-y-0
    ">
      <div>
        <h3 className="text-sm md:text-base text-gray-600">{title}</h3>
        <p className="text-2xl md:text-3xl lg:text-4xl font-bold">{value}</p>
      </div>
      <TrendIndicator trend={trend} />
    </Card>
  );
};
```

#### 2. **Tabelas Responsivas**
```tsx
export const TransactionTable = ({ transactions }: Props) => {
  return (
    <>
      {/* Desktop: Tabela completa */}
      <div className="hidden md:block overflow-x-auto">
        <table className="min-w-full">
          <thead>
            <tr>
              <th>ID</th>
              <th>De</th>
              <th>Para</th>
              <th>Valor</th>
              <th>Data</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map(tx => (
              <TransactionRow key={tx.id} transaction={tx} />
            ))}
          </tbody>
        </table>
      </div>
      
      {/* Mobile: Cards */}
      <div className="md:hidden space-y-3">
        {transactions.map(tx => (
          <TransactionCard key={tx.id} transaction={tx} />
        ))}
      </div>
    </>
  );
};
```

---

## 🌈 Experiência Imersiva

### Princípios de UX Imersiva

#### 1. **Micro-Interações**
Feedback visual imediato para cada ação do usuário.

```tsx
// Botão com feedback tátil
export const Button = ({ children, ...props }: Props) => {
  return (
    <button
      className="
        /* Estado normal */
        px-6 py-3 
        bg-primary-500 
        text-white 
        rounded-lg
        
        /* Hover */
        hover:bg-primary-600 
        hover:shadow-lg
        hover:-translate-y-0.5
        
        /* Active (pressed) */
        active:translate-y-0
        active:shadow-md
        
        /* Focus */
        focus:outline-none 
        focus:ring-2 
        focus:ring-primary-400
        focus:ring-offset-2
        
        /* Transições */
        transition-all 
        duration-200
      "
      {...props}
    >
      {children}
    </button>
  );
};
```

#### 2. **Loading States**
Estados de carregamento elegantes e informativos.

```tsx
export const WalletListSkeleton = () => {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map(i => (
        <div key={i} className="animate-pulse">
          <div className="h-24 bg-gray-200 rounded-lg" />
        </div>
      ))}
    </div>
  );
};

// Uso
{isLoading ? <WalletListSkeleton /> : <WalletList wallets={wallets} />}
```

#### 3. **Animações de Entrada/Saída**
```tsx
import { motion, AnimatePresence } from 'framer-motion';

export const Modal = ({ isOpen, children }: Props) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 backdrop-blur-sm"
        >
          <motion.div
            initial={{ scale: 0.95, y: 20 }}
            animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.95, y: 20 }}
            className="bg-white rounded-2xl p-8 max-w-md mx-auto mt-20"
          >
            {children}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
```

#### 4. **Transições de Página**
```tsx
// app/layout.tsx
import { PageTransition } from '@/components/PageTransition';

export default function RootLayout({ children }: Props) {
  return (
    <html>
      <body>
        <PageTransition>
          {children}
        </PageTransition>
      </body>
    </html>
  );
}

// components/PageTransition.tsx
export const PageTransition = ({ children }: Props) => {
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 20 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
};
```

#### 5. **Feedback de Sucesso/Erro**
```tsx
import { toast } from 'sonner';

// Sucesso
toast.success('Transferência realizada com sucesso!', {
  description: `${amount} CNB enviados para ${recipient}`,
  action: {
    label: 'Ver Detalhes',
    onClick: () => router.push(`/transactions/${txId}`),
  },
});

// Erro
toast.error('Erro ao processar transferência', {
  description: error.message,
  action: {
    label: 'Tentar Novamente',
    onClick: () => retryTransfer(),
  },
});
```

#### 6. **Modo Escuro Suave**
```tsx
// Tema com transição suave
export const ThemeProvider = ({ children }: Props) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  
  return (
    <div 
      className={theme}
      style={{
        transition: 'background-color 300ms ease-in-out, color 300ms ease-in-out'
      }}
    >
      {children}
    </div>
  );
};
```

#### 7. **Gráficos Animados**
```tsx
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export const BalanceChart = ({ data }: Props) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <defs>
          <linearGradient id="colorBalance" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.8}/>
            <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
          </linearGradient>
        </defs>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line 
          type="monotone" 
          dataKey="balance" 
          stroke="#0ea5e9" 
          strokeWidth={2}
          fill="url(#colorBalance)"
          animationDuration={1500}
          animationEasing="ease-in-out"
        />
      </LineChart>
    </ResponsiveContainer>
  );
};
```

---

## 🎯 Componentes UI

### Biblioteca de Componentes Base

#### 1. **Button Component**
```tsx
// components/ui/button.tsx
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  // Base styles
  "inline-flex items-center justify-center rounded-lg font-medium transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none",
  {
    variants: {
      variant: {
        primary: "bg-primary-500 text-white hover:bg-primary-600 focus:ring-primary-400",
        secondary: "bg-secondary-500 text-white hover:bg-secondary-600 focus:ring-secondary-400",
        outline: "border-2 border-primary-500 text-primary-500 hover:bg-primary-50 focus:ring-primary-400",
        ghost: "text-gray-700 hover:bg-gray-100 focus:ring-gray-400",
        danger: "bg-red-500 text-white hover:bg-red-600 focus:ring-red-400",
      },
      size: {
        sm: "text-sm px-3 py-1.5",
        md: "text-base px-4 py-2",
        lg: "text-lg px-6 py-3",
        xl: "text-xl px-8 py-4",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  isLoading?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, isLoading, children, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        disabled={isLoading}
        {...props}
      >
        {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        {children}
      </button>
    );
  }
);
```

#### 2. **Card Component**
```tsx
// components/ui/card.tsx
export const Card = ({ children, className, ...props }: Props) => {
  return (
    <div
      className={cn(
        "bg-white rounded-xl shadow-md border border-gray-200",
        "hover:shadow-lg transition-shadow duration-300",
        "dark:bg-dark-surface dark:border-dark-border",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader = ({ children, className }: Props) => {
  return (
    <div className={cn("p-6 border-b border-gray-200", className)}>
      {children}
    </div>
  );
};

export const CardBody = ({ children, className }: Props) => {
  return (
    <div className={cn("p-6", className)}>
      {children}
    </div>
  );
};

export const CardFooter = ({ children, className }: Props) => {
  return (
    <div className={cn("p-6 border-t border-gray-200", className)}>
      {children}
    </div>
  );
};
```

#### 3. **Input Component**
```tsx
// components/ui/input.tsx
export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, leftIcon, rightIcon, className, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {label}
          </label>
        )}
        
        <div className="relative">
          {leftIcon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
              {leftIcon}
            </div>
          )}
          
          <input
            ref={ref}
            className={cn(
              "w-full px-4 py-2 border rounded-lg",
              "focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent",
              "transition-all duration-200",
              error && "border-red-500 focus:ring-red-400",
              leftIcon && "pl-10",
              rightIcon && "pr-10",
              className
            )}
            {...props}
          />
          
          {rightIcon && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
              {rightIcon}
            </div>
          )}
        </div>
        
        {error && (
          <p className="mt-1 text-sm text-red-500">{error}</p>
        )}
        
        {helperText && !error && (
          <p className="mt-1 text-sm text-gray-500">{helperText}</p>
        )}
      </div>
    );
  }
);
```

---

# PARTE III - IMPLEMENTAÇÃO TÉCNICA

## 📖 Introdução à API

Este manual fornece todas as informações necessárias para integrar sua aplicação front-end com a API do **CoinBalance**, uma blockchain enterprise completa com recursos de carteira digital, transações, IA, Web3 e muito mais.

### Características da API

- **Arquitetura REST**: Endpoints RESTful padronizados
- **Autenticação JWT**: Tokens seguros com escopos granulares
- **Documentação Interativa**: Swagger UI e ReDoc disponíveis
- **Rate Limiting**: Proteção contra abuso
- **CORS Configurado**: Suporte a requisições cross-origin
- **Versionamento**: API versionada (v1)

### URLs Base

```
Desenvolvimento: http://localhost:8000
Produção: https://api.coinbalance.com
```

### Documentação Interativa

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## ⚙️ Configuração Inicial

### 1. Requisitos

- Node.js 16+ ou navegador moderno
- Axios, Fetch API ou biblioteca HTTP de sua escolha
- TypeScript (recomendado)

### 2. Instalação de Dependências

```bash
# Com npm
npm install axios

# Com yarn
yarn add axios

# Com pnpm
pnpm add axios
```

### 3. Configuração Base

Crie um arquivo de configuração para a API:

```typescript
// src/config/api.ts
export const API_CONFIG = {
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
};

export const API_ENDPOINTS = {
  // Autenticação
  LOGIN: '/api/v1/auth/login',
  LOGOUT: '/api/v1/auth/logout',
  REGISTER: '/api/v1/auth/users',
  ME: '/api/v1/auth/me',
  
  // Carteiras
  WALLETS: '/api/v1/carteiras',
  WALLET_BY_ADDRESS: (address: string) => `/api/v1/carteiras/${address}`,
  WALLET_CREDIT: (address: string) => `/api/v1/carteiras/${address}/creditar`,
  WALLET_DEBIT: (address: string) => `/api/v1/carteiras/${address}/debitar`,
  
  // Transações
  TRANSACTIONS: '/api/v1/transferencias',
  TRANSACTION_HISTORY: '/api/v1/transacoes/historico',
  TRANSACTION_STATS: '/api/v1/transacoes/stats',
  
  // Blockchain
  BLOCKCHAIN_STATS: '/api/v1/blockchain/stats',
  BLOCKCHAIN_BLOCKS: '/api/v1/blockchain/blocks',
  BLOCKCHAIN_MINE: '/api/v1/blockchain/mine',
  
  // Health & Monitoring
  HEALTH: '/api/v1/health',
  METRICS: '/api/v1/metrics',
  
  // Web3
  WEB3_BALANCE: '/api/v1/web3/balance',
  WEB3_NFT: '/api/v1/web3/nft',
  
  // IA
  AI_PREDICT: '/api/v1/ai-advanced/predict',
  AI_TRAIN: '/api/v1/ai-advanced/train-model',
};
```

### 4. Cliente HTTP com Axios

```typescript
// src/services/apiClient.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { API_CONFIG } from '../config/api';

class ApiClient {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.client = axios.create(API_CONFIG);
    
    // Interceptor para adicionar token em todas as requisições
    this.client.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Interceptor para tratamento de respostas
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token expirado ou inválido
          this.clearToken();
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  setToken(token: string): void {
    this.token = token;
    localStorage.setItem('authToken', token);
  }

  clearToken(): void {
    this.token = null;
    localStorage.removeItem('authToken');
  }

  loadToken(): void {
    const token = localStorage.getItem('authToken');
    if (token) {
      this.token = token;
    }
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }
}

export const apiClient = new ApiClient();
```

---

## 🔐 Autenticação e Autorização

### 1. Sistema de Autenticação

A API utiliza **JWT (JSON Web Tokens)** para autenticação com escopos de permissão granulares.

### 2. Fluxo de Autenticação

```typescript
// src/services/authService.ts
import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '../config/api';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: string;
    username: string;
    email: string;
    role: string;
    permissions: string[];
  };
}

export interface UserInfo {
  id: string;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: number;
  last_login: number | null;
  permissions: string[];
}

export interface CreateUserRequest {
  username: string;
  email: string;
  password: string;
  role: string;
  metadata?: Record<string, any>;
}

export class AuthService {
  /**
   * Realiza login do usuário
   */
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>(
      API_ENDPOINTS.LOGIN,
      credentials
    );
    
    // Salvar token
    apiClient.setToken(response.access_token);
    
    return response;
  }

  /**
   * Realiza logout do usuário
   */
  async logout(): Promise<void> {
    try {
      await apiClient.post(API_ENDPOINTS.LOGOUT);
    } finally {
      apiClient.clearToken();
    }
  }

  /**
   * Obtém informações do usuário atual
   */
  async getCurrentUser(): Promise<UserInfo> {
    return apiClient.get<UserInfo>(API_ENDPOINTS.ME);
  }

  /**
   * Cria novo usuário (requer permissão users:create)
   */
  async createUser(userData: CreateUserRequest): Promise<any> {
    return apiClient.post(API_ENDPOINTS.REGISTER, userData);
  }

  /**
   * Verifica se o usuário está autenticado
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('authToken');
  }

  /**
   * Inicializa super admin (apenas primeira vez)
   */
  async initSuperAdmin(): Promise<any> {
    return apiClient.post('/api/v1/auth/init-super-admin');
  }
}

export const authService = new AuthService();
```

### 3. Exemplo de Uso - Login Component (React)

```tsx
// src/components/Login.tsx
import React, { useState } from 'react';
import { authService } from '../services/authService';

export const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authService.login({ username, password });
      
      // Login bem-sucedido
      console.log('Login bem-sucedido:', response.user);
      
      // Redirecionar para dashboard
      window.location.href = '/dashboard';
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        'Erro ao fazer login. Verifique suas credenciais.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <h2>Login - CoinBalance</h2>
      
      {error && <div className="error">{error}</div>}
      
      <input
        type="text"
        placeholder="Usuário"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      
      <input
        type="password"
        placeholder="Senha"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      
      <button type="submit" disabled={loading}>
        {loading ? 'Entrando...' : 'Entrar'}
      </button>
    </form>
  );
};
```

### 4. Proteção de Rotas (React Router)

```tsx
// src/components/ProtectedRoute.tsx
import React from 'react';
import { Navigate } from 'react-router-dom';
import { authService } from '../services/authService';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  if (!authService.isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};
```

---

## 📦 Módulos da API

### 1. Módulo de Carteiras

```typescript
// src/services/walletService.ts
import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '../config/api';

export interface CreateWalletRequest {
  name: string;
  password?: string;
  metadata?: Record<string, any>;
}

export interface WalletResponse {
  address: string;
  name: string;
  public_key: string;
  balance_cnb: number;
  balance_satoshi: number;
  created_at: number;
  updated_at: number;
  is_active: boolean;
  metadata: Record<string, any>;
}

export interface WalletOperationRequest {
  amount: number;
  reason: string;
}

export class WalletService {
  /**
   * Cria uma nova carteira
   */
  async createWallet(data: CreateWalletRequest): Promise<WalletResponse> {
    return apiClient.post<WalletResponse>(API_ENDPOINTS.WALLETS, data);
  }

  /**
   * Obtém informações de uma carteira
   */
  async getWallet(address: string): Promise<WalletResponse> {
    return apiClient.get<WalletResponse>(
      API_ENDPOINTS.WALLET_BY_ADDRESS(address)
    );
  }

  /**
   * Lista todas as carteiras
   */
  async listWallets(): Promise<{ wallets: WalletResponse[]; total: number }> {
    return apiClient.get(API_ENDPOINTS.WALLETS);
  }

  /**
   * Credita saldo em uma carteira
   */
  async creditWallet(
    address: string,
    data: WalletOperationRequest
  ): Promise<any> {
    return apiClient.post(API_ENDPOINTS.WALLET_CREDIT(address), data);
  }

  /**
   * Debita saldo de uma carteira
   */
  async debitWallet(
    address: string,
    data: WalletOperationRequest
  ): Promise<any> {
    return apiClient.post(API_ENDPOINTS.WALLET_DEBIT(address), data);
  }

  /**
   * Obtém saldo detalhado de uma carteira
   */
  async getWalletBalance(address: string): Promise<any> {
    return apiClient.get(`${API_ENDPOINTS.WALLETS}/${address}/balance`);
  }
}

export const walletService = new WalletService();
```

### 2. Módulo de Transações

```typescript
// src/services/transactionService.ts
import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '../config/api';

export interface CreateTransferRequest {
  from_address: string;
  to_address: string;
  amount: string | number;
  fee?: string | number;
  memo?: string;
  metadata?: Record<string, any>;
}

export interface TransactionResponse {
  id: string;
  from_address: string | null;
  to_address: string;
  amount_cnb: string;
  fee_cnb: string;
  transaction_type: string;
  status: string;
  created_at: number;
  confirmed_at: number | null;
  block_height: number | null;
  transaction_hash: string | null;
  memo: string | null;
  metadata: Record<string, any>;
}

export interface TransactionListParams {
  address?: string;
  limit?: number;
  offset?: number;
}

export class TransactionService {
  /**
   * Cria uma nova transferência
   */
  async createTransfer(
    data: CreateTransferRequest
  ): Promise<TransactionResponse> {
    return apiClient.post<TransactionResponse>(
      API_ENDPOINTS.TRANSACTIONS,
      data
    );
  }

  /**
   * Obtém histórico de transações
   */
  async getTransactionHistory(params?: TransactionListParams): Promise<{
    transactions: TransactionResponse[];
    total: number;
    limit: number;
    offset: number;
  }> {
    return apiClient.get(API_ENDPOINTS.TRANSACTION_HISTORY, { params });
  }

  /**
   * Obtém estatísticas de transações
   */
  async getTransactionStats(): Promise<any> {
    return apiClient.get(API_ENDPOINTS.TRANSACTION_STATS);
  }

  /**
   * Obtém detalhes de uma transação específica
   */
  async getTransaction(id: string): Promise<TransactionResponse> {
    return apiClient.get(`${API_ENDPOINTS.TRANSACTIONS}/${id}`);
  }
}

export const transactionService = new TransactionService();
```

### 3. Módulo de Blockchain

```typescript
// src/services/blockchainService.ts
import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '../config/api';

export interface BlockchainStats {
  name: string;
  version: string;
  total_blocks: number;
  total_transactions: number;
  current_difficulty: number;
  average_block_time: number;
  total_mining_time: number;
  current_block_reward: number;
  total_supply: number;
  chain_valid: boolean;
  latest_block_height: number;
}

export interface BlockResponse {
  height: number;
  hash: string;
  previous_hash: string | null;
  timestamp: number;
  nonce: number;
  difficulty: number;
  mining_time: number;
  miner_address: string | null;
  block_reward: string;
  total_fees: string;
  transactions_count: number;
}

export interface MineBlockRequest {
  miner_address: string;
  max_transactions?: number;
}

export class BlockchainService {
  /**
   * Obtém estatísticas da blockchain
   */
  async getStats(): Promise<BlockchainStats> {
    return apiClient.get<BlockchainStats>(API_ENDPOINTS.BLOCKCHAIN_STATS);
  }

  /**
   * Lista todos os blocos
   */
  async getBlocks(): Promise<BlockResponse[]> {
    return apiClient.get<BlockResponse[]>(API_ENDPOINTS.BLOCKCHAIN_BLOCKS);
  }

  /**
   * Obtém um bloco específico por altura
   */
  async getBlock(height: number): Promise<BlockResponse> {
    return apiClient.get<BlockResponse>(
      `${API_ENDPOINTS.BLOCKCHAIN_BLOCKS}/${height}`
    );
  }

  /**
   * Minera um novo bloco
   */
  async mineBlock(data: MineBlockRequest): Promise<BlockResponse> {
    return apiClient.post<BlockResponse>(API_ENDPOINTS.BLOCKCHAIN_MINE, data);
  }

  /**
   * Valida a blockchain
   */
  async validateChain(): Promise<{ valid: boolean; errors?: string[] }> {
    return apiClient.get('/api/v1/blockchain/validate');
  }
}

export const blockchainService = new BlockchainService();
```

### 4. Módulo de Monitoramento

```typescript
// src/services/monitoringService.ts
import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '../config/api';

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  environment: string;
  timestamp: number;
}

export interface MetricsResponse {
  timestamp: number;
  version: string;
  environment: string;
  system: {
    cpu_percent: number;
    memory_percent: number;
    memory_used_mb: number;
    memory_total_mb: number;
  };
  config: {
    debug: boolean;
    workers: number;
    rate_limit_enabled: boolean;
  };
}

export class MonitoringService {
  /**
   * Verifica saúde da API
   */
  async checkHealth(): Promise<HealthResponse> {
    return apiClient.get<HealthResponse>(API_ENDPOINTS.HEALTH);
  }

  /**
   * Obtém métricas do sistema
   */
  async getMetrics(): Promise<MetricsResponse> {
    return apiClient.get<MetricsResponse>(API_ENDPOINTS.METRICS);
  }

  /**
   * Obtém dashboard de monitoramento
   */
  async getDashboard(): Promise<any> {
    return apiClient.get('/api/v1/monitoring/dashboard');
  }
}

export const monitoringService = new MonitoringService();
```

---

## 💡 Exemplos de Integração

### 1. Dashboard de Carteira (React)

```tsx
// src/components/WalletDashboard.tsx
import React, { useEffect, useState } from 'react';
import { walletService, WalletResponse } from '../services/walletService';
import { transactionService, TransactionResponse } from '../services/transactionService';

export const WalletDashboard: React.FC = () => {
  const [wallets, setWallets] = useState<WalletResponse[]>([]);
  const [selectedWallet, setSelectedWallet] = useState<WalletResponse | null>(null);
  const [transactions, setTransactions] = useState<TransactionResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadWallets();
  }, []);

  useEffect(() => {
    if (selectedWallet) {
      loadTransactions(selectedWallet.address);
    }
  }, [selectedWallet]);

  const loadWallets = async () => {
    try {
      const response = await walletService.listWallets();
      setWallets(response.wallets);
      
      if (response.wallets.length > 0) {
        setSelectedWallet(response.wallets[0]);
      }
    } catch (error) {
      console.error('Erro ao carregar carteiras:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadTransactions = async (address: string) => {
    try {
      const response = await transactionService.getTransactionHistory({
        address,
        limit: 10,
      });
      setTransactions(response.transactions);
    } catch (error) {
      console.error('Erro ao carregar transações:', error);
    }
  };

  const handleCreateWallet = async () => {
    const name = prompt('Nome da carteira:');
    if (!name) return;

    try {
      const newWallet = await walletService.createWallet({ name });
      setWallets([...wallets, newWallet]);
      alert('Carteira criada com sucesso!');
    } catch (error) {
      alert('Erro ao criar carteira');
    }
  };

  if (loading) {
    return <div>Carregando...</div>;
  }

  return (
    <div className="wallet-dashboard">
      <h1>Minhas Carteiras</h1>
      
      <button onClick={handleCreateWallet}>+ Nova Carteira</button>

      <div className="wallets-list">
        {wallets.map((wallet) => (
          <div
            key={wallet.address}
            className={`wallet-card ${selectedWallet?.address === wallet.address ? 'active' : ''}`}
            onClick={() => setSelectedWallet(wallet)}
          >
            <h3>{wallet.name}</h3>
            <p>Saldo: {wallet.balance_cnb} CNB</p>
            <small>{wallet.address.substring(0, 20)}...</small>
          </div>
        ))}
      </div>

      {selectedWallet && (
        <div className="wallet-details">
          <h2>{selectedWallet.name}</h2>
          <div className="balance">
            <h3>{selectedWallet.balance_cnb} CNB</h3>
            <p>{selectedWallet.balance_satoshi} satoshis</p>
          </div>

          <h3>Transações Recentes</h3>
          <div className="transactions-list">
            {transactions.map((tx) => (
              <div key={tx.id} className="transaction-item">
                <div>
                  <strong>{tx.transaction_type}</strong>
                  <p>{tx.memo || 'Sem descrição'}</p>
                </div>
                <div>
                  <span className={tx.from_address === selectedWallet.address ? 'debit' : 'credit'}>
                    {tx.from_address === selectedWallet.address ? '-' : '+'}
                    {tx.amount_cnb} CNB
                  </span>
                  <small>{tx.status}</small>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
```

### 2. Formulário de Transferência

```tsx
// src/components/TransferForm.tsx
import React, { useState } from 'react';
import { transactionService, CreateTransferRequest } from '../services/transactionService';

interface TransferFormProps {
  fromAddress: string;
  onSuccess?: () => void;
}

export const TransferForm: React.FC<TransferFormProps> = ({ fromAddress, onSuccess }) => {
  const [formData, setFormData] = useState({
    to_address: '',
    amount: '',
    memo: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const transferData: CreateTransferRequest = {
        from_address: fromAddress,
        to_address: formData.to_address,
        amount: formData.amount,
        memo: formData.memo || undefined,
      };

      await transactionService.createTransfer(transferData);
      
      alert('Transferência realizada com sucesso!');
      
      // Limpar formulário
      setFormData({ to_address: '', amount: '', memo: '' });
      
      if (onSuccess) {
        onSuccess();
      }
    } catch (err: any) {
      setError(
        err.response?.data?.detail?.error || 
        'Erro ao realizar transferência'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="transfer-form">
      <h2>Nova Transferência</h2>

      {error && <div className="error">{error}</div>}

      <div className="form-group">
        <label>De:</label>
        <input type="text" value={fromAddress} disabled />
      </div>

      <div className="form-group">
        <label>Para:</label>
        <input
          type="text"
          placeholder="Endereço de destino"
          value={formData.to_address}
          onChange={(e) => setFormData({ ...formData, to_address: e.target.value })}
          required
        />
      </div>

      <div className="form-group">
        <label>Valor (CNB):</label>
        <input
          type="number"
          step="0.00000001"
          min="0"
          placeholder="0.00"
          value={formData.amount}
          onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
          required
        />
      </div>

      <div className="form-group">
        <label>Descrição (opcional):</label>
        <input
          type="text"
          placeholder="Descrição da transferência"
          value={formData.memo}
          onChange={(e) => setFormData({ ...formData, memo: e.target.value })}
        />
      </div>

      <button type="submit" disabled={loading}>
        {loading ? 'Enviando...' : 'Transferir'}
      </button>
    </form>
  );
};
```

### 3. Dashboard de Blockchain

```tsx
// src/components/BlockchainDashboard.tsx
import React, { useEffect, useState } from 'react';
import { blockchainService, BlockchainStats, BlockResponse } from '../services/blockchainService';

export const BlockchainDashboard: React.FC = () => {
  const [stats, setStats] = useState<BlockchainStats | null>(null);
  const [blocks, setBlocks] = useState<BlockResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    
    // Atualizar a cada 30 segundos
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const [statsData, blocksData] = await Promise.all([
        blockchainService.getStats(),
        blockchainService.getBlocks(),
      ]);
      
      setStats(statsData);
      setBlocks(blocksData.slice(-10)); // Últimos 10 blocos
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !stats) {
    return <div>Carregando...</div>;
  }

  return (
    <div className="blockchain-dashboard">
      <h1>Blockchain CoinBalance</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total de Blocos</h3>
          <p className="stat-value">{stats.total_blocks}</p>
        </div>

        <div className="stat-card">
          <h3>Total de Transações</h3>
          <p className="stat-value">{stats.total_transactions}</p>
        </div>

        <div className="stat-card">
          <h3>Dificuldade Atual</h3>
          <p className="stat-value">{stats.current_difficulty}</p>
        </div>

        <div className="stat-card">
          <h3>Supply Total</h3>
          <p className="stat-value">{stats.total_supply.toFixed(2)} CNB</p>
        </div>

        <div className="stat-card">
          <h3>Recompensa por Bloco</h3>
          <p className="stat-value">{stats.current_block_reward} CNB</p>
        </div>

        <div className="stat-card">
          <h3>Tempo Médio de Bloco</h3>
          <p className="stat-value">{stats.average_block_time.toFixed(2)}s</p>
        </div>
      </div>

      <h2>Blocos Recentes</h2>
      <div className="blocks-list">
        {blocks.map((block) => (
          <div key={block.height} className="block-card">
            <div className="block-header">
              <h3>Bloco #{block.height}</h3>
              <span className="block-time">
                {new Date(block.timestamp * 1000).toLocaleString()}
              </span>
            </div>
            <div className="block-details">
              <p><strong>Hash:</strong> {block.hash.substring(0, 20)}...</p>
              <p><strong>Transações:</strong> {block.transactions_count}</p>
              <p><strong>Tempo de Mineração:</strong> {block.mining_time.toFixed(2)}s</p>
              <p><strong>Recompensa:</strong> {block.block_reward} CNB</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

---

## ⚠️ Tratamento de Erros

### 1. Códigos de Status HTTP

| Código | Significado | Descrição |
|--------|-------------|-----------|
| 200 | OK | Requisição bem-sucedida |
| 201 | Created | Recurso criado com sucesso |
| 400 | Bad Request | Dados inválidos ou faltando |
| 401 | Unauthorized | Token inválido ou ausente |
| 403 | Forbidden | Sem permissão para acessar |
| 404 | Not Found | Recurso não encontrado |
| 409 | Conflict | Conflito (ex: carteira já existe) |
| 422 | Unprocessable Entity | Validação falhou |
| 429 | Too Many Requests | Rate limit excedido |
| 500 | Internal Server Error | Erro interno do servidor |

### 2. Formato de Erro Padrão

```typescript
interface ApiError {
  detail: {
    error: string;
    code: string;
    message?: string;
  };
}
```

### 3. Tratamento de Erros Centralizado

```typescript
// src/utils/errorHandler.ts
export class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export const handleApiError = (error: any): ApiError => {
  if (error.response) {
    // Erro da API
    const status = error.response.status;
    const detail = error.response.data?.detail;
    
    if (typeof detail === 'object' && detail.error) {
      return new ApiError(status, detail.code || 'UNKNOWN', detail.error);
    } else if (typeof detail === 'string') {
      return new ApiError(status, 'UNKNOWN', detail);
    }
    
    return new ApiError(status, 'UNKNOWN', 'Erro desconhecido');
  } else if (error.request) {
    // Sem resposta do servidor
    return new ApiError(0, 'NETWORK_ERROR', 'Erro de conexão com o servidor');
  } else {
    // Erro na configuração da requisição
    return new ApiError(0, 'REQUEST_ERROR', error.message);
  }
};

export const getErrorMessage = (error: any): string => {
  const apiError = handleApiError(error);
  
  switch (apiError.code) {
    case 'WALLET_NOT_FOUND':
      return 'Carteira não encontrada';
    case 'INSUFFICIENT_BALANCE':
      return 'Saldo insuficiente';
    case 'INVALID_ADDRESS':
      return 'Endereço inválido';
    case 'DUPLICATE_WALLET':
      return 'Carteira já existe';
    case 'NETWORK_ERROR':
      return 'Erro de conexão. Verifique sua internet.';
    default:
      return apiError.message;
  }
};
```

### 4. Hook para Tratamento de Erros (React)

```typescript
// src/hooks/useApiError.ts
import { useState, useCallback } from 'react';
import { getErrorMessage } from '../utils/errorHandler';

export const useApiError = () => {
  const [error, setError] = useState<string | null>(null);

  const handleError = useCallback((err: any) => {
    const message = getErrorMessage(err);
    setError(message);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return { error, handleError, clearError };
};
```

---

## ✨ Boas Práticas

### 1. Segurança

```typescript
// ✅ BOM: Token no header Authorization
apiClient.setToken(token);
const wallet = await walletService.getWallet(address);

// ❌ RUIM: Token na URL
const wallet = await fetch(`/api/wallets?token=${token}`);
```

### 2. Performance

```typescript
// ✅ BOM: Carregar dados em paralelo
const [wallets, transactions, stats] = await Promise.all([
  walletService.listWallets(),
  transactionService.getTransactionHistory(),
  blockchainService.getStats(),
]);

// ❌ RUIM: Carregar dados sequencialmente
const wallets = await walletService.listWallets();
const transactions = await transactionService.getTransactionHistory();
const stats = await blockchainService.getStats();
```

### 3. Paginação

```typescript
// ✅ BOM: Usar paginação para listas grandes
const transactions = await transactionService.getTransactionHistory({
  limit: 50,
  offset: page * 50,
});

// ❌ RUIM: Carregar todos os dados de uma vez
const transactions = await transactionService.getTransactionHistory();
```

### 4. Cache de Dados

```typescript
// src/hooks/useWalletCache.ts
import { useState, useEffect, useRef } from 'react';
import { walletService, WalletResponse } from '../services/walletService';

export const useWalletCache = (address: string, cacheTime: number = 60000) => {
  const [wallet, setWallet] = useState<WalletResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const cacheRef = useRef<{ data: WalletResponse; timestamp: number } | null>(null);

  useEffect(() => {
    const loadWallet = async () => {
      // Verificar cache
      if (cacheRef.current && Date.now() - cacheRef.current.timestamp < cacheTime) {
        setWallet(cacheRef.current.data);
        setLoading(false);
        return;
      }

      // Carregar do servidor
      try {
        const data = await walletService.getWallet(address);
        setWallet(data);
        cacheRef.current = { data, timestamp: Date.now() };
      } catch (error) {
        console.error('Erro ao carregar carteira:', error);
      } finally {
        setLoading(false);
      }
    };

    loadWallet();
  }, [address, cacheTime]);

  return { wallet, loading };
};
```

### 5. Retry Logic

```typescript
// src/utils/retry.ts
export async function retryRequest<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error: any) {
      // Não fazer retry em erros 4xx (exceto 429)
      if (error.response?.status >= 400 && error.response?.status < 500 && error.response?.status !== 429) {
        throw error;
      }

      if (i === maxRetries - 1) {
        throw error;
      }

      // Aguardar antes de tentar novamente (exponential backoff)
      await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, i)));
    }
  }

  throw new Error('Max retries exceeded');
}
```

### 6. WebSocket para Updates em Tempo Real (Se disponível)

```typescript
// src/services/websocketService.ts
export class WebSocketService {
  private ws: WebSocket | null = null;
  private listeners: Map<string, Set<(data: any) => void>> = new Map();

  connect(url: string): void {
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      console.log('WebSocket conectado');
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const listeners = this.listeners.get(data.type);
      
      if (listeners) {
        listeners.forEach(listener => listener(data));
      }
    };

    this.ws.onerror = (error) => {
      console.error('Erro no WebSocket:', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket desconectado');
      // Reconectar após 5 segundos
      setTimeout(() => this.connect(url), 5000);
    };
  }

  on(event: string, callback: (data: any) => void): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);
  }

  off(event: string, callback: (data: any) => void): void {
    const listeners = this.listeners.get(event);
    if (listeners) {
      listeners.delete(callback);
    }
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

export const wsService = new WebSocketService();
```

---

## 🛠️ SDK JavaScript/TypeScript

### SDK Completo (Opcional)

Para facilitar ainda mais a integração, você pode criar um SDK completo:

```typescript
// src/sdk/coinbalance-sdk.ts
import { apiClient } from '../services/apiClient';
import { authService } from '../services/authService';
import { walletService } from '../services/walletService';
import { transactionService } from '../services/transactionService';
import { blockchainService } from '../services/blockchainService';
import { monitoringService } from '../services/monitoringService';

export class CoinBalanceSDK {
  public auth = authService;
  public wallets = walletService;
  public transactions = transactionService;
  public blockchain = blockchainService;
  public monitoring = monitoringService;

  constructor(baseURL?: string, token?: string) {
    if (baseURL) {
      // Configurar URL base personalizada
    }
    
    if (token) {
      apiClient.setToken(token);
    } else {
      // Tentar carregar token do localStorage
      apiClient.loadToken();
    }
  }

  /**
   * Configura o token de autenticação
   */
  setToken(token: string): void {
    apiClient.setToken(token);
  }

  /**
   * Remove o token de autenticação
   */
  clearToken(): void {
    apiClient.clearToken();
  }
}

// Exportar instância singleton
export const coinbalance = new CoinBalanceSDK();

// Uso:
// import { coinbalance } from './sdk/coinbalance-sdk';
// await coinbalance.auth.login({ username: 'admin', password: 'admin123' });
// const wallets = await coinbalance.wallets.listWallets();
```

---

## 🧪 Testes e Debugging

### 1. Testes Unitários (Jest)

```typescript
// src/services/__tests__/walletService.test.ts
import { walletService } from '../walletService';
import { apiClient } from '../apiClient';

jest.mock('../apiClient');

describe('WalletService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('deve criar uma carteira', async () => {
    const mockWallet = {
      address: 'abc123',
      name: 'Test Wallet',
      public_key: 'pub123',
      balance_cnb: 0,
      balance_satoshi: 0,
      created_at: Date.now(),
      updated_at: Date.now(),
      is_active: true,
      metadata: {},
    };

    (apiClient.post as jest.Mock).mockResolvedValue(mockWallet);

    const result = await walletService.createWallet({ name: 'Test Wallet' });

    expect(result).toEqual(mockWallet);
    expect(apiClient.post).toHaveBeenCalledWith(
      '/api/v1/carteiras',
      { name: 'Test Wallet' }
    );
  });

  it('deve listar carteiras', async () => {
    const mockResponse = {
      wallets: [],
      total: 0,
    };

    (apiClient.get as jest.Mock).mockResolvedValue(mockResponse);

    const result = await walletService.listWallets();

    expect(result).toEqual(mockResponse);
    expect(apiClient.get).toHaveBeenCalledWith('/api/v1/carteiras');
  });
});
```

### 2. Debug Mode

```typescript
// src/config/api.ts
export const API_CONFIG = {
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
};

// Habilitar logs de debug em desenvolvimento
if (process.env.NODE_ENV === 'development') {
  const originalPost = apiClient.post;
  apiClient.post = async function(...args: any[]) {
    console.log('[API POST]', args[0], args[1]);
    const result = await originalPost.apply(this, args);
    console.log('[API RESPONSE]', result);
    return result;
  };
}
```

### 3. Ferramentas de Debug

- **Postman/Insomnia**: Para testar endpoints manualmente
- **Swagger UI**: `http://localhost:8000/docs` - Interface interativa
- **Browser DevTools**: Network tab para inspecionar requisições
- **React DevTools**: Para debug de componentes React

---

## 📚 Referência Completa de Endpoints

### Autenticação (`/api/v1/auth`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/login` | Login do usuário | Não |
| POST | `/logout` | Logout do usuário | Sim |
| GET | `/me` | Informações do usuário atual | Sim |
| POST | `/users` | Criar novo usuário | Sim (users:create) |
| GET | `/users` | Listar usuários | Sim (users:view) |
| POST | `/change-password` | Alterar senha | Sim |
| GET | `/audit-logs` | Logs de auditoria | Sim (audit:logs) |
| POST | `/init-super-admin` | Inicializar super admin | Não |

### Carteiras (`/api/v1/carteiras`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/` | Criar carteira | Sim |
| GET | `/` | Listar carteiras | Sim |
| GET | `/{address}` | Obter carteira | Sim |
| POST | `/{address}/creditar` | Creditar saldo | Sim |
| POST | `/{address}/debitar` | Debitar saldo | Sim |
| GET | `/{address}/balance` | Saldo detalhado | Sim |

### Transações (`/api/v1/transferencias`, `/api/v1/transacoes`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/transferencias/` | Criar transferência | Sim |
| GET | `/transacoes/historico` | Histórico de transações | Sim |
| GET | `/transacoes/stats` | Estatísticas | Sim |
| GET | `/transacoes/{id}` | Detalhes da transação | Sim |

### Blockchain (`/api/v1/blockchain`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/stats` | Estatísticas da blockchain | Não |
| GET | `/blocks` | Listar blocos | Não |
| GET | `/blocks/{height}` | Obter bloco | Não |
| POST | `/mine` | Minerar bloco | Sim |
| GET | `/validate` | Validar blockchain | Não |

### Monitoramento (`/api/v1`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/health` | Health check | Não |
| GET | `/health/live` | Liveness probe | Não |
| GET | `/health/ready` | Readiness probe | Não |
| GET | `/metrics` | Métricas do sistema | Não |
| GET | `/info` | Informações da API | Não |
| GET | `/monitoring/dashboard` | Dashboard | Sim |

### Web3 (`/api/v1/web3`, `/api/v1/web3-advanced`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/web3/balance` | Saldo de token | Sim |
| GET | `/web3/nft` | Informações de NFT | Sim |
| POST | `/web3-advanced/connect-network` | Conectar rede | Sim |
| GET | `/web3-advanced/token-balance` | Saldo de token ERC20 | Sim |

### IA (`/api/v1/ai-advanced`, `/api/v1/ai-crypto`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/ai-advanced/train-model` | Treinar modelo | Sim |
| POST | `/ai-advanced/predict` | Fazer predição | Sim |
| POST | `/ai-crypto/create` | Criar criptomoeda | Sim |

---

## 🎓 Conclusão

Este manual fornece uma base sólida para integrar sua aplicação front-end com a API do CoinBalance. Para mais informações:

- **Documentação Interativa**: http://localhost:8000/docs
- **Código-fonte**: GitHub do projeto
- **Suporte**: Issues no GitHub ou Discord

### Próximos Passos

1. Configurar ambiente de desenvolvimento
2. Implementar sistema de autenticação
3. Criar componentes de carteira
4. Adicionar funcionalidade de transferências
5. Implementar dashboard de blockchain
6. Adicionar testes automatizados

### Recursos Adicionais

- TypeScript para type safety
- React Query para gerenciamento de estado de servidor
- Zod para validação de dados
- TanStack Table para tabelas de dados
- Chart.js para gráficos e visualizações

---

## 🗺️ Roadmap de Implementação

### Fase 1: Setup Inicial (Semana 1-2)

#### Sprint 1: Configuração do Projeto
- [ ] Inicializar projeto Next.js/React com TypeScript
- [ ] Configurar Tailwind CSS e Design System
- [ ] Instalar dependências principais (Axios, React Query, Zustand)
- [ ] Configurar ESLint, Prettier, Husky
- [ ] Setup de ambiente (.env, configurações)

#### Sprint 2: Autenticação Base
- [ ] Implementar tela de login
- [ ] Implementar tela de registro (se necessário)
- [ ] Criar serviço de autenticação
- [ ] Implementar proteção de rotas
- [ ] Gerenciamento de tokens JWT

**Entregáveis**: Sistema de autenticação funcional

---

### Fase 2: Dashboard Principal (Semana 3-4)

#### Sprint 3: Layout e Navegação
- [ ] Criar layout principal (Header, Sidebar, Footer)
- [ ] Implementar navegação responsiva
- [ ] Criar componentes de UI base (Button, Card, Input, etc.)
- [ ] Implementar tema claro/escuro
- [ ] Configurar rotas da aplicação

#### Sprint 4: Dashboard Executivo
- [ ] Criar página de dashboard
- [ ] Implementar cards de estatísticas
- [ ] Adicionar gráfico de saldo
- [ ] Criar seção de atividade recente
- [ ] Implementar quick actions

**Entregáveis**: Dashboard funcional com visão geral

---

### Fase 3: Módulo de Carteiras (Semana 5-6)

#### Sprint 5: Listagem e Criação
- [ ] Implementar listagem de carteiras
- [ ] Criar modal de criação de carteira
- [ ] Implementar componente WalletCard
- [ ] Adicionar filtros e busca
- [ ] Implementar paginação

#### Sprint 6: Detalhes e Operações
- [ ] Criar página de detalhes da carteira
- [ ] Implementar operações de crédito/débito
- [ ] Adicionar QR Code para recebimento
- [ ] Criar gráfico de histórico de saldo
- [ ] Implementar exportação de chaves

**Entregáveis**: Sistema completo de gestão de carteiras

---

### Fase 4: Módulo de Transações (Semana 7-8)

#### Sprint 7: Transferências
- [ ] Criar formulário de transferência
- [ ] Implementar validações de saldo
- [ ] Adicionar seletor de carteira
- [ ] Criar preview de transação
- [ ] Implementar confirmação e feedback

#### Sprint 8: Histórico
- [ ] Criar página de histórico de transações
- [ ] Implementar tabela responsiva
- [ ] Adicionar filtros avançados (data, tipo, status)
- [ ] Criar modal de detalhes da transação
- [ ] Implementar exportação para CSV/PDF

**Entregáveis**: Sistema completo de transações

---

### Fase 5: Blockchain Explorer (Semana 9-10)

#### Sprint 9: Visualização de Blocos
- [ ] Criar página de blockchain explorer
- [ ] Implementar listagem de blocos
- [ ] Criar componente BlockCard
- [ ] Adicionar visualização em tempo real
- [ ] Implementar gráficos de estatísticas

#### Sprint 10: Detalhes e Mineração
- [ ] Criar página de detalhes do bloco
- [ ] Implementar dashboard de mineração
- [ ] Adicionar controle de mineração
- [ ] Criar visualização de recompensas
- [ ] Implementar estatísticas de hashrate

**Entregáveis**: Blockchain explorer funcional

---

### Fase 6: Web3 e DeFi (Semana 11-12)

#### Sprint 11: Integração Web3
- [ ] Integrar Wagmi/RainbowKit
- [ ] Implementar conexão com MetaMask
- [ ] Criar página de Web3 dashboard
- [ ] Implementar consulta de saldos externos
- [ ] Adicionar cross-chain bridge UI

#### Sprint 12: DeFi e NFTs
- [ ] Criar interface de staking
- [ ] Implementar yield farming UI
- [ ] Criar NFT marketplace
- [ ] Adicionar DAO governance
- [ ] Implementar visualização de pools

**Entregáveis**: Integração Web3 completa

---

### Fase 7: IA e Analytics (Semana 13-14)

#### Sprint 13: Predições
- [ ] Criar dashboard de IA
- [ ] Implementar gráficos preditivos
- [ ] Adicionar análise de sentimento
- [ ] Criar recomendações automáticas
- [ ] Implementar insights personalizados

#### Sprint 14: Visualizações Avançadas
- [ ] Criar gráficos interativos com D3.js
- [ ] Implementar heatmaps
- [ ] Adicionar análise de tendências
- [ ] Criar relatórios automatizados
- [ ] Implementar alertas inteligentes

**Entregáveis**: Sistema de IA e analytics

---

### Fase 8: Configurações e Perfil (Semana 15)

#### Sprint 15: Perfil e Configurações
- [ ] Criar página de perfil do usuário
- [ ] Implementar alteração de senha
- [ ] Adicionar preferências de notificação
- [ ] Criar configurações de segurança (2FA)
- [ ] Implementar logs de atividade
- [ ] Adicionar gerenciamento de sessões

**Entregáveis**: Sistema de perfil completo

---

### Fase 9: Performance e Otimização (Semana 16)

#### Sprint 16: Otimizações
- [ ] Implementar code splitting avançado
- [ ] Otimizar bundle size
- [ ] Adicionar lazy loading de imagens
- [ ] Implementar service worker (PWA)
- [ ] Otimizar renderização (React.memo, useMemo)
- [ ] Adicionar prefetching de dados
- [ ] Implementar cache strategies

**Entregáveis**: Performance otimizada < 3s TTI

---

### Fase 10: Testes e QA (Semana 17-18)

#### Sprint 17: Testes Unitários
- [ ] Criar testes unitários de componentes
- [ ] Testar hooks customizados
- [ ] Testar serviços e utils
- [ ] Atingir cobertura > 80%

#### Sprint 18: Testes E2E
- [ ] Criar testes E2E com Playwright
- [ ] Testar fluxos principais (login, transferência, etc.)
- [ ] Testar responsividade
- [ ] Realizar testes de acessibilidade
- [ ] Fazer testes de performance

**Entregáveis**: Cobertura de testes > 80%, QA aprovado

---

### Fase 11: Deploy e DevOps (Semana 19)

#### Sprint 19: CI/CD e Deploy
- [ ] Configurar pipeline CI/CD
- [ ] Setup de ambientes (staging, production)
- [ ] Configurar Docker e Nginx
- [ ] Implementar monitoring (Sentry, analytics)
- [ ] Configurar CDN para assets
- [ ] Deploy em produção

**Entregáveis**: Aplicação em produção

---

### Fase 12: Melhorias Contínuas (Ongoing)

#### Backlog de Melhorias
- [ ] Adicionar mais idiomas (i18n)
- [ ] Implementar notificações push
- [ ] Criar onboarding interativo
- [ ] Adicionar gamificação
- [ ] Implementar modo offline completo
- [ ] Criar app mobile (React Native)
- [ ] Adicionar integrações externas
- [ ] Implementar analytics avançado

---

## 📊 KPIs e Métricas de Sucesso

### Performance
- ✅ Lighthouse Score > 90
- ✅ Time to Interactive < 3s
- ✅ First Contentful Paint < 1.5s
- ✅ Bundle Size < 500KB (inicial)

### Qualidade
- ✅ Cobertura de Testes > 80%
- ✅ Zero erros críticos no Sentry
- ✅ Acessibilidade WCAG 2.1 AA
- ✅ SEO Score > 90

### UX
- ✅ Mobile Usage > 40%
- ✅ Bounce Rate < 30%
- ✅ Session Duration > 5min
- ✅ User Satisfaction > 4.5/5

### Segurança
- ✅ Zero vulnerabilidades críticas
- ✅ HTTPS em 100% das requisições
- ✅ Headers de segurança configurados
- ✅ Conformidade LGPD/GDPR

---

## 🎓 Recursos de Aprendizado

### Documentação Oficial
- [React Documentation](https://react.dev)
- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)

### Tutoriais Recomendados
- [React Query Tutorial](https://tanstack.com/query/latest/docs/react/overview)
- [Framer Motion Guide](https://www.framer.com/motion/introduction)
- [Web3 Integration Guide](https://wagmi.sh)

### Ferramentas de Desenvolvimento
- **VS Code**: Editor recomendado
- **React DevTools**: Debug de componentes
- **Redux DevTools**: Debug de estado
- **Lighthouse**: Audit de performance
- **Axe DevTools**: Audit de acessibilidade

---

## 💼 Considerações Finais

### ✨ Resultado Final Esperado

O **Frontend CoinBalance** será uma plataforma web enterprise de classe mundial que oferece:

1. **Experiência Excepcional**: Interface moderna, intuitiva e responsiva
2. **Performance Otimizada**: Carregamento rápido em qualquer dispositivo
3. **Segurança Robusta**: Autenticação JWT, HTTPS, headers de segurança
4. **Escalabilidade**: Arquitetura preparada para crescimento
5. **Manutenibilidade**: Código limpo, testado e documentado
6. **Acessibilidade**: Inclusivo para todos os usuários
7. **Inovação**: Recursos de IA, Web3 e DeFi integrados

### 🎯 Diferenciais Competitivos

- ✅ **Único no Mercado**: Blockchain + IA + Web3 integrados
- ✅ **Enterprise Ready**: Arquitetura e qualidade enterprise
- ✅ **Open Source**: Comunidade ativa e contribuições
- ✅ **Documentação Completa**: Manual técnico de 3000+ linhas
- ✅ **Suporte Multilíngue**: Português, Inglês, Espanhol
- ✅ **Conformidade**: LGPD, GDPR, SOC 2

### 🚀 Próximos Passos

1. **Revisar Manual**: Ler e entender toda a documentação
2. **Setup Ambiente**: Configurar ambiente de desenvolvimento
3. **Protótipo**: Criar wireframes e protótipos no Figma
4. **Desenvolvimento**: Seguir o roadmap de 19 semanas
5. **Testes**: Garantir qualidade em todas as etapas
6. **Deploy**: Colocar em produção com monitoramento
7. **Feedback**: Coletar feedback e iterar continuamente

### 📞 Suporte e Comunidade

- **Discord**: [discord.gg/coinbalance](https://discord.gg/coinbalance)
- **GitHub**: [github.com/coinbalance](https://github.com/coinbalance)
- **Email**: frontend@coinbalance.com
- **Documentação**: [docs.coinbalance.com](https://docs.coinbalance.com)

---

**Desenvolvido com ❤️ pela equipe CoinBalance**

> "O futuro da economia digital começa aqui. Bem-vindo ao CoinBalance - onde blockchain, IA e Web3 se encontram para criar a próxima geração de aplicações financeiras descentralizadas."

**Versão do Manual**: 2.0.0  
**Última Atualização**: 2025-10-28  
**Autores**: Equipe CoinBalance  
**Licença**: MIT License

---

## 📚 Apêndice

### A. Glossário de Termos

- **Blockchain**: Tecnologia de registro distribuído
- **DeFi**: Finanças Descentralizadas
- **DAO**: Organização Autônoma Descentralizada
- **NFT**: Token Não Fungível
- **Web3**: Nova geração da internet descentralizada
- **Smart Contract**: Contrato inteligente executado na blockchain
- **Gas Fee**: Taxa de transação na blockchain
- **Staking**: Processo de bloquear criptomoedas para validação
- **Yield Farming**: Estratégia de maximização de retornos em DeFi
- **Cross-Chain**: Interoperabilidade entre diferentes blockchains

### B. Referências de API

Para referência completa de todos os endpoints da API CoinBalance, consulte:
- [Swagger UI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)
- [Documentação API](docs/api/README.md)

### C. Changelog

#### v2.0.0 - 2025-10-28
- ✨ Adicionada Parte I: Visão Geral e Conceito
- ✨ Adicionada Parte II: Design e Experiência do Usuário
- ✨ Expandido com Design System completo
- ✨ Adicionado Roadmap de Implementação de 19 semanas
- ✨ Incluídas especificações de frontend responsivo e imersivo
- ✨ Adicionados exemplos de componentes UI
- ✨ Documentação expandida para 3000+ linhas

#### v1.0.0 - 2025-10-28
- 🎉 Lançamento inicial do manual de integração
- 📝 Documentação de autenticação
- 📝 Exemplos de integração com carteiras
- 📝 Referência completa de endpoints

---

**🎉 Parabéns! Você está pronto para desenvolver o Frontend CoinBalance!**
