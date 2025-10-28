# 🔧 Troubleshooting e FAQ - Frontend CoinBalance

## Guia de Resolução de Problemas

Este guia ajuda a resolver os problemas mais comuns no desenvolvimento do frontend CoinBalance.

---

## 📋 Índice

1. [Problemas de Instalação](#problemas-de-instalação)
2. [Erros de Build](#erros-de-build)
3. [Problemas de Runtime](#problemas-de-runtime)
4. [Integração com API](#integração-com-api)
5. [Performance](#performance)
6. [FAQ Geral](#faq-geral)

---

## 🔨 Problemas de Instalação

### Erro: "npm install" falha

**Sintomas:**
```
npm ERR! code ERESOLVE
npm ERR! ERESOLVE could not resolve
```

**Solução:**
```bash
# Limpar cache
npm cache clean --force

# Remover node_modules e package-lock.json
rm -rf node_modules package-lock.json

# Reinstalar com --legacy-peer-deps
npm install --legacy-peer-deps

# Ou usar --force como último recurso
npm install --force
```

### Erro: Versão do Node.js incompatível

**Sintomas:**
```
error This project requires Node.js version >=18.0.0
```

**Solução:**
```bash
# Verificar versão atual
node --version

# Instalar NVM (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Instalar e usar Node 18
nvm install 18
nvm use 18

# Verificar
node --version  # deve mostrar v18.x.x
```

### Erro: "gyp ERR!" durante instalação

**Sintomas:**
```
gyp ERR! build error
gyp ERR! stack Error: not found: make
```

**Solução (macOS):**
```bash
xcode-select --install
```

**Solução (Linux):**
```bash
sudo apt-get install build-essential
```

**Solução (Windows):**
```bash
npm install --global windows-build-tools
```

---

## 🏗️ Erros de Build

### Erro: "Module not found"

**Sintomas:**
```
Module not found: Can't resolve '@/components/...'
```

**Solução:**

1. Verificar `tsconfig.json`:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

2. Reiniciar servidor:
```bash
# Ctrl+C para parar
npm run dev
```

### Erro: TypeScript type errors

**Sintomas:**
```
Type 'string' is not assignable to type 'number'
```

**Solução:**

1. Verificar tipos:
```typescript
// ❌ Errado
const age: number = "25";

// ✅ Correto
const age: number = 25;
```

2. Usar type assertions quando necessário:
```typescript
const value = localStorage.getItem('key') as string;
```

3. Skip lib check temporariamente (não recomendado para produção):
```json
// tsconfig.json
{
  "compilerOptions": {
    "skipLibCheck": true
  }
}
```

### Erro: "Failed to compile"

**Sintomas:**
```
./src/app/page.tsx
Syntax error: Unexpected token
```

**Solução:**

1. Verificar sintaxe do arquivo
2. Verificar imports:
```typescript
// ❌ Import inválido
import Button from '@/components/ui/button'

// ✅ Import correto
import { Button } from '@/components/ui/button'
```

3. Limpar cache e rebuild:
```bash
rm -rf .next
npm run build
```

### Erro: "FATAL ERROR: ... JavaScript heap out of memory"

**Sintomas:**
```
FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed
```

**Solução:**

1. Aumentar memória do Node:
```bash
# package.json
{
  "scripts": {
    "build": "NODE_OPTIONS='--max-old-space-size=4096' next build"
  }
}
```

2. Otimizar imports:
```typescript
// ❌ Importa biblioteca inteira
import _ from 'lodash';

// ✅ Import específico
import debounce from 'lodash/debounce';
```

---

## ⚠️ Problemas de Runtime

### Erro: "Hydration failed"

**Sintomas:**
```
Warning: Text content did not match. Server: "X" Client: "Y"
Error: Hydration failed because the initial UI does not match what was rendered on the server.
```

**Solução:**

1. Evitar código que depende do browser no server:
```typescript
// ❌ Errado - pode causar hydration error
function Component() {
  const [isClient, setIsClient] = useState(false);
  
  return <div>{window.innerWidth}</div>;
}

// ✅ Correto
function Component() {
  const [isClient, setIsClient] = useState(false);
  
  useEffect(() => {
    setIsClient(true);
  }, []);
  
  if (!isClient) return null;
  
  return <div>{window.innerWidth}</div>;
}
```

2. Usar `'use client'` quando necessário:
```typescript
'use client';

import { useState } from 'react';

export function ClientComponent() {
  const [count, setCount] = useState(0);
  // ...
}
```

### Erro: "window is not defined"

**Sintomas:**
```
ReferenceError: window is not defined
```

**Solução:**

1. Verificar se está no cliente:
```typescript
if (typeof window !== 'undefined') {
  // Código que usa window
  localStorage.setItem('key', 'value');
}
```

2. Usar useEffect:
```typescript
useEffect(() => {
  // Código que usa window
  const width = window.innerWidth;
}, []);
```

3. Dynamic import com SSR disabled:
```typescript
import dynamic from 'next/dynamic';

const ComponentWithWindow = dynamic(
  () => import('./ComponentWithWindow'),
  { ssr: false }
);
```

### Erro: "Cannot read property of undefined"

**Sintomas:**
```
TypeError: Cannot read property 'name' of undefined
```

**Solução:**

1. Usar optional chaining:
```typescript
// ❌ Pode quebrar
const name = user.profile.name;

// ✅ Seguro
const name = user?.profile?.name;
```

2. Usar nullish coalescing:
```typescript
// ❌ Pode quebrar
const name = user.name || 'Guest';

// ✅ Melhor
const name = user.name ?? 'Guest';
```

3. Verificar antes de usar:
```typescript
if (user && user.profile) {
  const name = user.profile.name;
}
```

---

## 🌐 Integração com API

### Erro: CORS

**Sintomas:**
```
Access to fetch at 'http://localhost:8000/api/...' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solução:**

1. Backend deve ter CORS configurado:
```python
# FastAPI
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. Ou usar proxy no Next.js:
```typescript
// next.config.js
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
};
```

### Erro: 401 Unauthorized

**Sintomas:**
```
Error: Request failed with status code 401
```

**Solução:**

1. Verificar se token está sendo enviado:
```typescript
// Verificar interceptor do Axios
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

2. Verificar se token não expirou:
```typescript
const isTokenExpired = (token: string) => {
  try {
    const decoded = JSON.parse(atob(token.split('.')[1]));
    return decoded.exp * 1000 < Date.now();
  } catch {
    return true;
  }
};
```

3. Implementar refresh token:
```typescript
axios.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      try {
        const newToken = await refreshToken();
        error.config.headers.Authorization = `Bearer ${newToken}`;
        return axios(error.config);
      } catch {
        // Redirect to login
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
```

### Erro: Network Error / Timeout

**Sintomas:**
```
Error: Network Error
Error: timeout of 30000ms exceeded
```

**Solução:**

1. Verificar se API está rodando:
```bash
curl http://localhost:8000/api/v1/health
```

2. Aumentar timeout:
```typescript
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 60000, // 60 segundos
});
```

3. Implementar retry:
```typescript
import axios from 'axios';
import axiosRetry from 'axios-retry';

axiosRetry(apiClient, {
  retries: 3,
  retryDelay: axiosRetry.exponentialDelay,
  retryCondition: (error) => {
    return axiosRetry.isNetworkOrIdempotentRequestError(error) || error.response?.status === 429;
  },
});
```

---

## ⚡ Performance

### Problema: Página carrega lentamente

**Diagnóstico:**
```bash
# Lighthouse audit
npm run build
npm run start
# Abra Chrome DevTools > Lighthouse
```

**Soluções:**

1. **Lazy Loading de Componentes:**
```typescript
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />,
  ssr: false,
});
```

2. **Otimizar Imagens:**
```typescript
import Image from 'next/image';

// ❌ img tag normal
<img src="/large-image.jpg" />

// ✅ Next.js Image component
<Image
  src="/large-image.jpg"
  width={800}
  height={600}
  alt="Description"
  priority // para imagens above the fold
/>
```

3. **Code Splitting:**
```typescript
// ❌ Import tudo de uma vez
import { Chart1, Chart2, Chart3 } from 'recharts';

// ✅ Import sob demanda
const Chart1 = lazy(() => import('recharts').then(m => ({ default: m.Chart1 })));
```

4. **Memoização:**
```typescript
import { useMemo, useCallback, memo } from 'react';

// Memoizar cálculos pesados
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(data);
}, [data]);

// Memoizar callbacks
const handleClick = useCallback(() => {
  // handler
}, [dependencies]);

// Memoizar componentes
const MemoizedComponent = memo(Component);
```

### Problema: Re-renders desnecessários

**Diagnóstico:**
```typescript
// React DevTools Profiler
// ou
import { useWhyDidYouUpdate } from '@/hooks/useWhyDidYouUpdate';

function Component(props) {
  useWhyDidYouUpdate('Component', props);
  // ...
}
```

**Solução:**

1. Usar `React.memo`:
```typescript
const ExpensiveComponent = memo(({ data }: Props) => {
  // ...
}, (prevProps, nextProps) => {
  // Retornar true se props são iguais (não renderizar)
  return prevProps.data.id === nextProps.data.id;
});
```

2. Usar `useMemo` e `useCallback`:
```typescript
const Parent = () => {
  // ❌ Cria nova função toda renderização
  const handleClick = () => console.log('click');
  
  // ✅ Memoiza função
  const handleClick = useCallback(() => {
    console.log('click');
  }, []);
  
  return <Child onClick={handleClick} />;
};
```

---

## ❓ FAQ Geral

### Como debugar a aplicação?

**VS Code Debug:**
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js: debug server-side",
      "type": "node-terminal",
      "request": "launch",
      "command": "npm run dev"
    },
    {
      "name": "Next.js: debug client-side",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000"
    }
  ]
}
```

**Browser DevTools:**
- F12 para abrir DevTools
- Sources tab > Breakpoints
- Console para logs
- Network tab para requisições

### Como limpar cache completamente?

```bash
# Limpar .next
rm -rf .next

# Limpar node_modules
rm -rf node_modules package-lock.json

# Limpar cache do npm
npm cache clean --force

# Reinstalar
npm install

# Rebuild
npm run build
```

### Como atualizar dependências?

```bash
# Verificar outdated
npm outdated

# Atualizar minor/patch versions
npm update

# Atualizar major versions (cuidado!)
npm install package@latest

# Ou usar npx
npx npm-check-updates -u
npm install
```

### Como fazer login na aplicação pela primeira vez?

```bash
# 1. Inicializar super admin (apenas primeira vez)
curl -X POST http://localhost:8000/api/v1/auth/init-super-admin

# 2. Fazer login com credenciais padrão
Username: admin
Password: admin123

# 3. IMPORTANTE: Alterar senha após primeiro login!
```

### A página está em branco, o que fazer?

1. Verificar console do browser (F12)
2. Verificar se há erros de JavaScript
3. Verificar se `npm run dev` está rodando
4. Verificar se API está rodando
5. Limpar cache e reload (Ctrl + Shift + R)

### Como adicionar um novo componente shadcn/ui?

```bash
# Listar componentes disponíveis
npx shadcn-ui@latest add

# Adicionar componente específico
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add tabs
```

### Como fazer autenticação persistir entre reloads?

```typescript
// hooks/useAuth.ts
export const useAuth = () => {
  useEffect(() => {
    // Carregar token do localStorage ao montar
    const token = localStorage.getItem('authToken');
    if (token) {
      apiClient.setToken(token);
      // Verificar validade
      apiClient.get('/api/v1/auth/me')
        .then(user => setUser(user))
        .catch(() => {
          localStorage.removeItem('authToken');
        });
    }
  }, []);
};
```

### Como implementar dark mode?

```typescript
// Usar next-themes
npm install next-themes

// app/providers.tsx
import { ThemeProvider } from 'next-themes';

export function Providers({ children }: Props) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  );
}

// Usar em componente
import { useTheme } from 'next-themes';

function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  
  return (
    <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
      Toggle Theme
    </button>
  );
}
```

---

## 🆘 Ainda com Problemas?

### Recursos de Ajuda

1. **Documentação Oficial:**
   - [Next.js Docs](https://nextjs.org/docs)
   - [React Docs](https://react.dev)
   - [TypeScript Docs](https://www.typescriptlang.org/docs)

2. **Comunidade:**
   - Discord do CoinBalance
   - GitHub Issues
   - Stack Overflow

3. **Ferramentas de Debug:**
   - React DevTools
   - Redux DevTools (se usar)
   - Next.js DevTools

4. **Logs Detalhados:**
```bash
# Next.js debug mode
DEBUG=* npm run dev

# Verbose logging
npm run dev -- --debug
```

### Template de Issue

Ao reportar um problema, inclua:

```markdown
## Descrição
[Descreva o problema]

## Passos para Reproduzir
1. ...
2. ...
3. ...

## Comportamento Esperado
[O que deveria acontecer]

## Comportamento Atual
[O que está acontecendo]

## Screenshots
[Se aplicável]

## Ambiente
- OS: [e.g. macOS 13.0]
- Browser: [e.g. Chrome 120]
- Node: [e.g. 18.17.0]
- npm: [e.g. 9.6.7]
- Next.js: [e.g. 14.0.0]

## Logs
```
[Cole os logs relevantes]
```

## Tentativas de Solução
[O que já tentou]
```

---

**Versão**: 1.0.0  
**Última Atualização**: 2025-10-28  
**Mantenedor**: Equipe CoinBalance
