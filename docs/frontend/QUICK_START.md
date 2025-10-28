# 🚀 Quick Start - Frontend CoinBalance

## Guia de Início Rápido (15 minutos)

Este guia vai te ajudar a ter o frontend CoinBalance rodando localmente em menos de 15 minutos.

---

## 📋 Pré-requisitos

Certifique-se de ter instalado:

- **Node.js**: 18.0.0 ou superior
- **npm** ou **yarn** ou **pnpm**
- **Git**
- **VS Code** (recomendado)

### Verificar Instalações

```bash
node --version  # deve ser v18+
npm --version   # deve ser 9+
git --version
```

---

## 🎯 Passo 1: Criar Projeto Next.js

```bash
# Criar projeto com TypeScript
npx create-next-app@latest coinbalance-frontend

# Responder as perguntas:
✔ Would you like to use TypeScript? … Yes
✔ Would you like to use ESLint? … Yes
✔ Would you like to use Tailwind CSS? … Yes
✔ Would you like to use `src/` directory? … Yes
✔ Would you like to use App Router? … Yes
✔ Would you like to customize the default import alias? … No

# Entrar no diretório
cd coinbalance-frontend
```

---

## 🎨 Passo 2: Instalar Dependências

```bash
# Dependências principais
npm install axios zustand react-query @tanstack/react-query
npm install framer-motion lucide-react
npm install react-hook-form zod @hookform/resolvers
npm install recharts date-fns

# Shadcn/ui (componentes)
npx shadcn-ui@latest init

# Responder:
✔ Which style would you like to use? › Default
✔ Which color would you like to use as base color? › Slate
✔ Would you like to use CSS variables for colors? › Yes

# Adicionar componentes base do shadcn/ui
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add table
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add tabs
```

---

## 📁 Passo 3: Estrutura de Diretórios

Crie a seguinte estrutura:

```bash
mkdir -p src/lib/{api,hooks,utils,constants}
mkdir -p src/services
mkdir -p src/components/{ui,layout,wallet,transaction,blockchain,charts,common}
mkdir -p src/types
mkdir -p src/store/slices
```

---

## ⚙️ Passo 4: Configurar Variáveis de Ambiente

Crie o arquivo `.env.local`:

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=CoinBalance
NEXT_PUBLIC_APP_VERSION=1.0.0
```

---

## 🔧 Passo 5: Configurar API Client

Crie `src/lib/api/client.ts`:

```typescript
// src/lib/api/client.ts
import axios, { AxiosInstance } from 'axios';

class ApiClient {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.clearToken();
          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('authToken', token);
    }
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('authToken');
    }
  }

  loadToken() {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('authToken');
      if (token) {
        this.token = token;
      }
    }
  }

  async get<T>(url: string, config?: any): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: any): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: any): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: any): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }
}

export const apiClient = new ApiClient();
```

---

## 🎨 Passo 6: Criar Layout Principal

Crie `src/app/layout.tsx`:

```typescript
// src/app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'CoinBalance - Blockchain Enterprise',
  description: 'Plataforma blockchain com IA e Web3',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

Crie `src/app/providers.tsx`:

```typescript
// src/app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';
import { Toaster } from '@/components/ui/toaster';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000, // 1 minuto
        refetchOnWindowFocus: false,
      },
    },
  }));

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <Toaster />
    </QueryClientProvider>
  );
}
```

---

## 🏠 Passo 7: Criar Página Inicial

Crie `src/app/page.tsx`:

```typescript
// src/app/page.tsx
'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Wallet, ArrowRightLeft, Box, TrendingUp } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-primary">CoinBalance</h1>
          <nav className="space-x-4">
            <Link href="/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/register">
              <Button>Começar</Button>
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h2 className="text-5xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          Blockchain Enterprise com IA e Web3
        </h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Plataforma completa de blockchain com inteligência artificial integrada,
          carteiras digitais seguras e recursos Web3 avançados.
        </p>
        <div className="flex gap-4 justify-center">
          <Link href="/dashboard">
            <Button size="lg" className="text-lg">
              Acessar Dashboard
            </Button>
          </Link>
          <Link href="/docs">
            <Button size="lg" variant="outline" className="text-lg">
              Documentação
            </Button>
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 py-20">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="border-2 hover:border-primary transition-colors">
            <CardHeader>
              <Wallet className="w-12 h-12 text-primary mb-4" />
              <CardTitle>Carteiras Digitais</CardTitle>
              <CardDescription>
                Crie e gerencie carteiras com segurança enterprise
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-2 hover:border-primary transition-colors">
            <CardHeader>
              <ArrowRightLeft className="w-12 h-12 text-primary mb-4" />
              <CardTitle>Transferências</CardTitle>
              <CardDescription>
                Realize transferências rápidas e seguras
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-2 hover:border-primary transition-colors">
            <CardHeader>
              <Box className="w-12 h-12 text-primary mb-4" />
              <CardTitle>Blockchain</CardTitle>
              <CardDescription>
                Explore blocos e transações em tempo real
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-2 hover:border-primary transition-colors">
            <CardHeader>
              <TrendingUp className="w-12 h-12 text-primary mb-4" />
              <CardTitle>IA & Analytics</CardTitle>
              <CardDescription>
                Predições e análises com inteligência artificial
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-white/80 backdrop-blur-sm mt-20">
        <div className="container mx-auto px-4 py-8 text-center text-gray-600">
          <p>© 2025 CoinBalance. Desenvolvido com ❤️ pela equipe CoinBalance.</p>
        </div>
      </footer>
    </div>
  );
}
```

---

## 🚦 Passo 8: Executar o Projeto

```bash
# Iniciar servidor de desenvolvimento
npm run dev

# Abrir no navegador
# http://localhost:3000
```

---

## ✅ Verificar Instalação

Você deve ver:

1. ✅ Página inicial com design moderno
2. ✅ Gradientes e animações suaves
3. ✅ Cards de features
4. ✅ Navegação funcionando
5. ✅ Sem erros no console

---

## 🎯 Próximos Passos

Agora que você tem o projeto base rodando, siga estes passos:

1. **Autenticação**: Implemente páginas de login/registro
2. **Dashboard**: Crie o dashboard principal
3. **Carteiras**: Implemente o módulo de carteiras
4. **API Integration**: Conecte com o backend CoinBalance

### Recursos Úteis

- 📖 [Manual Completo](MANUAL_INTEGRACAO_FRONTEND.md)
- 🎨 [Guia de Componentes](COMPONENTES_UI.md)
- 🔧 [Exemplos Completos](EXEMPLOS_COMPLETOS.md)
- 📊 [Roadmap de Implementação](MANUAL_INTEGRACAO_FRONTEND.md#roadmap-de-implementação)

---

## 🐛 Problemas Comuns

### Erro: "Module not found"
```bash
# Limpar cache e reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Erro: "Port 3000 already in use"
```bash
# Usar porta diferente
npm run dev -- -p 3001
```

### Erro de TypeScript
```bash
# Verificar tsconfig.json
npx tsc --noEmit
```

---

## 🎉 Parabéns!

Você configurou com sucesso o projeto frontend CoinBalance! 

**Tempo total**: ~15 minutos  
**Status**: ✅ Pronto para desenvolvimento

Agora você pode começar a desenvolver as funcionalidades seguindo o roadmap de 19 semanas do manual principal.

---

**Desenvolvido com ❤️ pela equipe CoinBalance**
