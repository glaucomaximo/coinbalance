# 🧪 Guia de Testes - Frontend CoinBalance

## Estratégia de Testes Completa

Este guia cobre todas as práticas de testes para garantir qualidade do frontend CoinBalance.

---

## 📋 Índice

1. [Setup de Testes](#setup-de-testes)
2. [Testes Unitários](#testes-unitários)
3. [Testes de Integração](#testes-de-integração)
4. [Testes E2E](#testes-e2e)
5. [Testes de Acessibilidade](#testes-de-acessibilidade)
6. [Coverage e Relatórios](#coverage-e-relatórios)

---

## ⚙️ Setup de Testes

### Instalar Dependências

```bash
# Vitest (Jest replacement mais rápido)
npm install -D vitest @vitejs/plugin-react

# React Testing Library
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event

# Playwright (E2E)
npm install -D @playwright/test

# MSW (Mock Service Worker)
npm install -D msw

# Axe para testes de acessibilidade
npm install -D @axe-core/react
```

### Configurar Vitest

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.config.*',
        '**/*.d.ts',
      ],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

### Setup File

```typescript
// tests/setup.ts
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach, vi } from 'vitest';

// Cleanup após cada teste
afterEach(() => {
  cleanup();
});

// Mock de next/navigation
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    back: vi.fn(),
  }),
  usePathname: () => '/dashboard',
  useSearchParams: () => new URLSearchParams(),
}));

// Mock de window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});
```

---

## 🔬 Testes Unitários

### Testando Componentes

```typescript
// components/ui/button.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './button';

describe('Button Component', () => {
  it('deve renderizar corretamente', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('deve executar onClick quando clicado', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('deve estar desabilitado quando disabled=true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });

  it('deve mostrar loading state', () => {
    render(<Button isLoading>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
    // Verifica se tem spinner
    expect(document.querySelector('.animate-spin')).toBeInTheDocument();
  });

  it('deve aplicar variantes corretamente', () => {
    const { rerender } = render(<Button variant="primary">Button</Button>);
    expect(screen.getByText('Button')).toHaveClass('bg-primary-500');

    rerender(<Button variant="secondary">Button</Button>);
    expect(screen.getByText('Button')).toHaveClass('bg-secondary-500');
  });
});
```

### Testando Hooks Customizados

```typescript
// hooks/useAuth.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAuth } from './useAuth';

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('useAuth Hook', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('deve retornar user null quando não autenticado', () => {
    const { result } = renderHook(() => useAuth(), {
      wrapper: createWrapper(),
    });

    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('deve fazer login com sucesso', async () => {
    const { result } = renderHook(() => useAuth(), {
      wrapper: createWrapper(),
    });

    await result.current.login({
      username: 'testuser',
      password: 'password123',
    });

    await waitFor(() => {
      expect(result.current.isAuthenticated).toBe(true);
      expect(result.current.user).not.toBeNull();
    });
  });

  it('deve fazer logout corretamente', async () => {
    const { result } = renderHook(() => useAuth(), {
      wrapper: createWrapper(),
    });

    // Fazer login primeiro
    await result.current.login({
      username: 'testuser',
      password: 'password123',
    });

    await waitFor(() => {
      expect(result.current.isAuthenticated).toBe(true);
    });

    // Fazer logout
    await result.current.logout();

    await waitFor(() => {
      expect(result.current.isAuthenticated).toBe(false);
      expect(result.current.user).toBeNull();
    });
  });
});
```

### Testando Serviços

```typescript
// services/wallet.service.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { walletService } from './wallet.service';
import { apiClient } from '@/lib/api/client';

// Mock do apiClient
vi.mock('@/lib/api/client', () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('WalletService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('deve listar carteiras', async () => {
    const mockWallets = {
      wallets: [
        { address: 'abc123', name: 'Test Wallet', balance_cnb: 100 },
      ],
      total: 1,
    };

    (apiClient.get as any).mockResolvedValue(mockWallets);

    const result = await walletService.listWallets();

    expect(apiClient.get).toHaveBeenCalledWith('/api/v1/carteiras');
    expect(result).toEqual(mockWallets);
  });

  it('deve criar uma carteira', async () => {
    const newWallet = { name: 'New Wallet', password: 'secure123' };
    const mockResponse = {
      address: 'xyz789',
      name: 'New Wallet',
      balance_cnb: 0,
    };

    (apiClient.post as any).mockResolvedValue(mockResponse);

    const result = await walletService.createWallet(newWallet);

    expect(apiClient.post).toHaveBeenCalledWith('/api/v1/carteiras', newWallet);
    expect(result).toEqual(mockResponse);
  });

  it('deve lançar erro quando criar carteira falhar', async () => {
    (apiClient.post as any).mockRejectedValue(new Error('Network error'));

    await expect(
      walletService.createWallet({ name: 'Test' })
    ).rejects.toThrow('Network error');
  });
});
```

---

## 🔗 Testes de Integração

### Testando Página Completa

```typescript
// app/(dashboard)/wallets/page.test.tsx
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import WalletsPage from './page';
import { walletService } from '@/services/wallet.service';

vi.mock('@/services/wallet.service');

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('WalletsPage Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('deve renderizar lista de carteiras', async () => {
    const mockWallets = {
      wallets: [
        { address: 'abc123', name: 'Wallet 1', balance_cnb: 100 },
        { address: 'def456', name: 'Wallet 2', balance_cnb: 200 },
      ],
      total: 2,
    };

    (walletService.listWallets as any).mockResolvedValue(mockWallets);

    render(<WalletsPage />, { wrapper: createWrapper() });

    await waitFor(() => {
      expect(screen.getByText('Wallet 1')).toBeInTheDocument();
      expect(screen.getByText('Wallet 2')).toBeInTheDocument();
    });
  });

  it('deve filtrar carteiras por busca', async () => {
    const mockWallets = {
      wallets: [
        { address: 'abc123', name: 'Personal Wallet', balance_cnb: 100 },
        { address: 'def456', name: 'Business Wallet', balance_cnb: 200 },
      ],
      total: 2,
    };

    (walletService.listWallets as any).mockResolvedValue(mockWallets);

    render(<WalletsPage />, { wrapper: createWrapper() });

    await waitFor(() => {
      expect(screen.getByText('Personal Wallet')).toBeInTheDocument();
    });

    const searchInput = screen.getByPlaceholderText('Buscar carteira...');
    fireEvent.change(searchInput, { target: { value: 'Personal' } });

    expect(screen.getByText('Personal Wallet')).toBeInTheDocument();
    expect(screen.queryByText('Business Wallet')).not.toBeInTheDocument();
  });

  it('deve mostrar estado vazio quando não há carteiras', async () => {
    (walletService.listWallets as any).mockResolvedValue({
      wallets: [],
      total: 0,
    });

    render(<WalletsPage />, { wrapper: createWrapper() });

    await waitFor(() => {
      expect(screen.getByText('Nenhuma carteira encontrada')).toBeInTheDocument();
    });
  });
});
```

### Mock Service Worker (MSW)

```typescript
// tests/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  // Mock de login
  http.post('/api/v1/auth/login', async ({ request }) => {
    const body = await request.json();
    
    if (body.username === 'testuser' && body.password === 'password123') {
      return HttpResponse.json({
        access_token: 'mock-token',
        token_type: 'bearer',
        user: {
          id: '1',
          username: 'testuser',
          email: 'test@example.com',
        },
      });
    }
    
    return HttpResponse.json(
      { detail: 'Invalid credentials' },
      { status: 401 }
    );
  }),

  // Mock de listagem de carteiras
  http.get('/api/v1/carteiras', () => {
    return HttpResponse.json({
      wallets: [
        { address: 'abc123', name: 'Test Wallet', balance_cnb: 100 },
      ],
      total: 1,
    });
  }),

  // Mock de criação de carteira
  http.post('/api/v1/carteiras', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      address: 'new-wallet-address',
      name: body.name,
      balance_cnb: 0,
      created_at: Date.now(),
    });
  }),
];

// tests/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

```typescript
// tests/setup.ts (adicionar ao setup existente)
import { server } from './mocks/server';
import { beforeAll, afterAll, afterEach } from 'vitest';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

---

## 🎭 Testes E2E (Playwright)

### Configurar Playwright

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    // Mobile
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Testes E2E

```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Autenticação', () => {
  test('deve fazer login com sucesso', async ({ page }) => {
    await page.goto('/login');

    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Dashboard');
  });

  test('deve mostrar erro com credenciais inválidas', async ({ page }) => {
    await page.goto('/login');

    await page.fill('input[name="username"]', 'wronguser');
    await page.fill('input[name="password"]', 'wrongpass');
    await page.click('button[type="submit"]');

    await expect(page.locator('[role="alert"]')).toContainText('Credenciais inválidas');
  });

  test('deve fazer logout', async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('/dashboard');

    // Logout
    await page.click('button[aria-label="Menu do usuário"]');
    await page.click('text=Sair');

    await expect(page).toHaveURL('/login');
  });
});
```

```typescript
// tests/e2e/wallet.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Carteiras', () => {
  test.beforeEach(async ({ page }) => {
    // Login antes de cada teste
    await page.goto('/login');
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/dashboard');
  });

  test('deve criar nova carteira', async ({ page }) => {
    await page.goto('/wallets');

    await page.click('text=Nova Carteira');
    await page.fill('input[name="name"]', 'Test Wallet');
    await page.fill('input[name="password"]', 'secure123');
    await page.click('text=Criar Carteira');

    await expect(page.locator('text=Carteira criada com sucesso')).toBeVisible();
    await expect(page.locator('text=Test Wallet')).toBeVisible();
  });

  test('deve visualizar detalhes da carteira', async ({ page }) => {
    await page.goto('/wallets');

    await page.click('text=Test Wallet').first();

    await expect(page).toHaveURL(/\/wallets\/.+/);
    await expect(page.locator('h1')).toContainText('Test Wallet');
  });

  test('deve realizar transferência', async ({ page }) => {
    await page.goto('/wallets');

    await page.click('text=Transferir');
    await page.selectOption('select[name="from_address"]', 'wallet1');
    await page.fill('input[name="to_address"]', 'abc123def456');
    await page.fill('input[name="amount"]', '10.5');
    await page.fill('input[name="memo"]', 'Test transfer');
    await page.click('button[type="submit"]');

    await expect(page.locator('text=Transferência realizada com sucesso')).toBeVisible();
  });
});
```

---

## ♿ Testes de Acessibilidade

```typescript
// tests/accessibility/button.a11y.test.tsx
import { describe, it } from 'vitest';
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { Button } from '@/components/ui/button';

expect.extend(toHaveNoViolations);

describe('Button Accessibility', () => {
  it('deve não ter violações de acessibilidade', async () => {
    const { container } = render(<Button>Click me</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('deve ter aria-label quando só tem ícone', async () => {
    const { container } = render(
      <Button aria-label="Settings">
        <SettingsIcon />
      </Button>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

---

## 📊 Coverage e Relatórios

### Executar Testes com Coverage

```bash
# Todos os testes com coverage
npm run test:coverage

# Apenas unitários
npm run test:unit

# Apenas E2E
npm run test:e2e

# Watch mode para desenvolvimento
npm run test:watch
```

### package.json Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:unit": "vitest run",
    "test:watch": "vitest --watch",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:report": "playwright show-report"
  }
}
```

### Metas de Coverage

```json
{
  "jest": {
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

---

## 🎯 Best Practices

### ✅ Fazer

- Testar comportamento, não implementação
- Usar data-testid apenas quando necessário
- Simular interações do usuário realisticamente
- Manter testes independentes
- Usar MSW para mocks de API
- Testar casos de erro
- Testar responsividade

### ❌ Evitar

- Testar detalhes de implementação
- Testes acoplados
- Mocks excessivos
- Ignorar casos de borda
- Testes lentos sem necessidade
- Testes frágeis (que quebram facilmente)

---

**Cobertura Alvo**: 80%+  
**Versão**: 1.0.0  
**Última Atualização**: 2025-10-28
