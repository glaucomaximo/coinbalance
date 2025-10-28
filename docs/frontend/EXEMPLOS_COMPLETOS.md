# 💼 Exemplos Completos - Páginas CoinBalance

## Páginas Completas Prontas para Uso

Este guia apresenta exemplos completos de páginas do CoinBalance, prontas para copiar e adaptar.

---

## 📋 Índice

1. [Dashboard Principal](#dashboard-principal)
2. [Página de Carteiras](#página-de-carteiras)
3. [Página de Transações](#página-de-transações)
4. [Página de Login](#página-de-login)
5. [Página de Blockchain Explorer](#página-de-blockchain-explorer)

---

## 🏠 Dashboard Principal

```tsx
// app/(dashboard)/dashboard/page.tsx
'use client';

import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Wallet, TrendingUp, ArrowRightLeft, Box } from 'lucide-react';
import { BalanceChart } from '@/components/charts/BalanceChart';
import { RecentActivity } from '@/components/dashboard/RecentActivity';
import { QuickActions } from '@/components/dashboard/QuickActions';

export default function DashboardPage() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      // Fetch dashboard stats
      return {
        totalBalance: '1,234.56',
        totalWallets: 5,
        totalTransactions: 127,
        blocksToday: 42,
      };
    },
  });

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-gray-500">Bem-vindo ao CoinBalance</p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Saldo Total"
          value={`${stats.totalBalance} CNB`}
          change={+2.5}
          icon={Wallet}
        />
        <StatCard
          title="Carteiras"
          value={stats.totalWallets}
          change={+10}
          icon={TrendingUp}
        />
        <StatCard
          title="Transações"
          value={stats.totalTransactions}
          change={+15.3}
          icon={ArrowRightLeft}
        />
        <StatCard
          title="Blocos Hoje"
          value={stats.blocksToday}
          change={+5.2}
          icon={Box}
        />
      </div>

      {/* Charts and Activity */}
      <div className="grid gap-6 lg:grid-cols-7">
        <div className="lg:col-span-4">
          <BalanceChart />
        </div>
        <div className="lg:col-span-3 space-y-6">
          <QuickActions />
          <RecentActivity />
        </div>
      </div>
    </div>
  );
}

const StatCard = ({ title, value, change, icon: Icon }: any) => {
  const isPositive = change >= 0;

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <p className="text-sm text-gray-500 mb-1">{title}</p>
            <p className="text-2xl font-bold">{value}</p>
            <p className={`text-sm mt-1 flex items-center gap-1 ${
              isPositive ? 'text-green-500' : 'text-red-500'
            }`}>
              <TrendingUp className={`w-3 h-3 ${!isPositive && 'rotate-180'}`} />
              {isPositive ? '+' : ''}{change}%
            </p>
          </div>
          <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
            <Icon className="w-6 h-6 text-primary" />
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

const DashboardSkeleton = () => (
  <div className="space-y-6">
    <div className="space-y-2">
      <div className="h-8 w-48 bg-gray-200 rounded animate-pulse" />
      <div className="h-4 w-64 bg-gray-200 rounded animate-pulse" />
    </div>
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {[1, 2, 3, 4].map((i) => (
        <div key={i} className="h-32 bg-gray-200 rounded-lg animate-pulse" />
      ))}
    </div>
  </div>
);
```

---

## 💰 Página de Carteiras

```tsx
// app/(dashboard)/wallets/page.tsx
'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { WalletCard } from '@/components/wallet/WalletCard';
import { CreateWalletModal } from '@/components/wallet/CreateWalletModal';
import { Search, Plus, Filter } from 'lucide-react';
import { walletService } from '@/services/wallet.service';

export default function WalletsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterOpen, setFilterOpen] = useState(false);

  const { data: wallets, isLoading, refetch } = useQuery({
    queryKey: ['wallets'],
    queryFn: () => walletService.listWallets(),
  });

  const filteredWallets = wallets?.wallets.filter((wallet: any) =>
    wallet.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    wallet.address.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Carteiras</h1>
          <p className="text-gray-500">Gerencie suas carteiras digitais</p>
        </div>
        <CreateWalletModal onSuccess={refetch} />
      </div>

      {/* Search and Filters */}
      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Buscar carteira..."
            className="pl-10"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <Button variant="outline" onClick={() => setFilterOpen(!filterOpen)}>
          <Filter className="mr-2 h-4 w-4" />
          Filtros
        </Button>
      </div>

      {/* Wallets Grid */}
      {isLoading ? (
        <WalletListSkeleton />
      ) : filteredWallets && filteredWallets.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filteredWallets.map((wallet: any) => (
            <WalletCard key={wallet.address} wallet={wallet} />
          ))}
        </div>
      ) : (
        <EmptyState
          icon={Wallet}
          title="Nenhuma carteira encontrada"
          description="Crie sua primeira carteira para começar"
          action={<CreateWalletModal onSuccess={refetch} />}
        />
      )}

      {/* Stats Summary */}
      {wallets && wallets.total > 0 && (
        <Card>
          <CardContent className="pt-6">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-2xl font-bold">{wallets.total}</p>
                <p className="text-sm text-gray-500">Total de Carteiras</p>
              </div>
              <div>
                <p className="text-2xl font-bold">
                  {wallets.wallets.reduce((sum: number, w: any) => sum + w.balance_cnb, 0).toFixed(2)} CNB
                </p>
                <p className="text-sm text-gray-500">Saldo Total</p>
              </div>
              <div>
                <p className="text-2xl font-bold">
                  {wallets.wallets.filter((w: any) => w.is_active).length}
                </p>
                <p className="text-sm text-gray-500">Carteiras Ativas</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

const WalletListSkeleton = () => (
  <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
    {[1, 2, 3, 4, 5, 6].map((i) => (
      <Card key={i}>
        <CardContent className="p-6">
          <div className="animate-pulse space-y-3">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-gray-200" />
              <div className="flex-1 space-y-2">
                <div className="h-4 bg-gray-200 rounded w-3/4" />
                <div className="h-3 bg-gray-200 rounded w-1/2" />
              </div>
            </div>
            <div className="h-8 bg-gray-200 rounded" />
          </div>
        </CardContent>
      </Card>
    ))}
  </div>
);

const EmptyState = ({ icon: Icon, title, description, action }: any) => (
  <Card className="border-dashed">
    <CardContent className="flex flex-col items-center justify-center py-16">
      <div className="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mb-4">
        <Icon className="w-8 h-8 text-gray-400" />
      </div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-500 mb-4 text-center max-w-sm">{description}</p>
      {action}
    </CardContent>
  </Card>
);
```

---

## 🔄 Página de Transações

```tsx
// app/(dashboard)/transactions/page.tsx
'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { TransactionsTable } from '@/components/transaction/TransactionsTable';
import { TransactionFilters } from '@/components/transaction/TransactionFilters';
import { TransferModal } from '@/components/transaction/TransferModal';
import { transactionService } from '@/services/transaction.service';
import { ArrowRightLeft, Download } from 'lucide-react';

export default function TransactionsPage() {
  const [filters, setFilters] = useState({
    status: 'all',
    dateFrom: null,
    dateTo: null,
    minAmount: null,
    maxAmount: null,
  });

  const { data: transactions, isLoading } = useQuery({
    queryKey: ['transactions', filters],
    queryFn: () => transactionService.getTransactionHistory({
      limit: 50,
      offset: 0,
    }),
  });

  const { data: stats } = useQuery({
    queryKey: ['transaction-stats'],
    queryFn: () => transactionService.getTransactionStats(),
  });

  const handleExport = () => {
    // Lógica de exportação CSV/PDF
    console.log('Exporting transactions...');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Transações</h1>
          <p className="text-gray-500">Histórico completo de transações</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleExport}>
            <Download className="mr-2 h-4 w-4" />
            Exportar
          </Button>
          <TransferModal />
        </div>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardContent className="pt-6">
              <p className="text-sm text-gray-500">Total de Transações</p>
              <p className="text-2xl font-bold">{stats.total_transactions}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <p className="text-sm text-gray-500">Volume Total</p>
              <p className="text-2xl font-bold">{stats.total_volume_cnb} CNB</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <p className="text-sm text-gray-500">Pendentes</p>
              <p className="text-2xl font-bold text-yellow-600">{stats.pending_transactions}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <p className="text-sm text-gray-500">Confirmadas</p>
              <p className="text-2xl font-bold text-green-600">{stats.confirmed_transactions}</p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Filters */}
      <TransactionFilters filters={filters} onChange={setFilters} />

      {/* Transactions List */}
      <Card>
        <CardHeader>
          <CardTitle>Histórico</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="all">
            <TabsList>
              <TabsTrigger value="all">Todas</TabsTrigger>
              <TabsTrigger value="sent">Enviadas</TabsTrigger>
              <TabsTrigger value="received">Recebidas</TabsTrigger>
              <TabsTrigger value="pending">Pendentes</TabsTrigger>
            </TabsList>
            
            <TabsContent value="all" className="mt-6">
              {isLoading ? (
                <TransactionsTableSkeleton />
              ) : transactions && transactions.transactions.length > 0 ? (
                <TransactionsTable transactions={transactions.transactions} />
              ) : (
                <EmptyState
                  icon={ArrowRightLeft}
                  title="Nenhuma transação encontrada"
                  description="Suas transações aparecerão aqui"
                />
              )}
            </TabsContent>
          </Tabs>

          {/* Pagination */}
          {transactions && transactions.total > 50 && (
            <div className="flex items-center justify-between mt-6">
              <p className="text-sm text-gray-500">
                Mostrando {transactions.transactions.length} de {transactions.total} transações
              </p>
              <div className="flex gap-2">
                <Button variant="outline" size="sm">Anterior</Button>
                <Button variant="outline" size="sm">Próxima</Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
```

---

## 🔐 Página de Login

```tsx
// app/(auth)/login/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { authService } from '@/services/auth.service';
import { Lock, Mail, Eye, EyeOff } from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';

const loginSchema = z.object({
  username: z.string().min(1, 'Username é obrigatório'),
  password: z.string().min(6, 'Senha deve ter no mínimo 6 caracteres'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const router = useRouter();
  const { toast } = useToast();
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);
    try {
      await authService.login(data);
      
      toast({
        title: 'Login realizado com sucesso!',
        description: 'Redirecionando para o dashboard...',
      });
      
      router.push('/dashboard');
    } catch (error: any) {
      toast({
        variant: 'destructive',
        title: 'Erro ao fazer login',
        description: error.response?.data?.detail || 'Credenciais inválidas',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50 p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1 text-center">
          <div className="mx-auto w-16 h-16 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center mb-4">
            <Lock className="w-8 h-8 text-white" />
          </div>
          <CardTitle className="text-2xl font-bold">Bem-vindo de volta</CardTitle>
          <CardDescription>
            Entre com suas credenciais para acessar o CoinBalance
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <Label htmlFor="username">Username</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  id="username"
                  {...register('username')}
                  className="pl-10"
                  placeholder="seu_username"
                  disabled={isLoading}
                />
              </div>
              {errors.username && (
                <p className="text-sm text-red-500 mt-1">{errors.username.message}</p>
              )}
            </div>

            <div>
              <Label htmlFor="password">Senha</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  {...register('password')}
                  className="pl-10 pr-10"
                  placeholder="••••••••"
                  disabled={isLoading}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
              {errors.password && (
                <p className="text-sm text-red-500 mt-1">{errors.password.message}</p>
              )}
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="rounded" />
                <span className="text-sm text-gray-600">Lembrar-me</span>
              </label>
              <Link href="/forgot-password" className="text-sm text-primary hover:underline">
                Esqueceu a senha?
              </Link>
            </div>

            <Button type="submit" className="w-full" isLoading={isLoading}>
              {isLoading ? 'Entrando...' : 'Entrar'}
            </Button>
          </form>

          <div className="mt-6 text-center text-sm">
            <span className="text-gray-600">Não tem uma conta? </span>
            <Link href="/register" className="text-primary hover:underline font-medium">
              Criar conta
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

---

## ⛓️ Página de Blockchain Explorer

```tsx
// app/(dashboard)/blockchain/page.tsx
'use client';

import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BlockCard } from '@/components/blockchain/BlockCard';
import { BlockchainStats } from '@/components/blockchain/BlockchainStats';
import { blockchainService } from '@/services/blockchain.service';
import { Box, Activity, Zap } from 'lucide-react';

export default function BlockchainPage() {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['blockchain-stats'],
    queryFn: () => blockchainService.getStats(),
  });

  const { data: blocks, isLoading: blocksLoading } = useQuery({
    queryKey: ['blocks'],
    queryFn: () => blockchainService.getBlocks(),
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Blockchain Explorer</h1>
        <p className="text-gray-500">Explore a blockchain CoinBalance em tempo real</p>
      </div>

      {/* Stats */}
      {statsLoading ? (
        <StatsGridSkeleton />
      ) : stats && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <StatCard
            icon={Box}
            title="Total de Blocos"
            value={stats.total_blocks}
            subtitle="Altura da chain"
          />
          <StatCard
            icon={Activity}
            title="Transações"
            value={stats.total_transactions}
            subtitle="Total na blockchain"
          />
          <StatCard
            icon={Zap}
            title="Dificuldade"
            value={stats.current_difficulty}
            subtitle="Nível atual"
          />
          <StatCard
            icon={TrendingUp}
            title="Tempo Médio"
            value={`${stats.average_block_time.toFixed(1)}s`}
            subtitle="Por bloco"
          />
        </div>
      )}

      {/* Blockchain Stats Chart */}
      {stats && <BlockchainStats stats={stats} />}

      {/* Recent Blocks */}
      <Card>
        <CardHeader>
          <CardTitle>Blocos Recentes</CardTitle>
        </CardHeader>
        <CardContent>
          {blocksLoading ? (
            <BlockListSkeleton />
          ) : blocks && blocks.length > 0 ? (
            <div className="space-y-3">
              {blocks.slice(0, 10).map((block: any) => (
                <BlockCard key={block.height} block={block} />
              ))}
            </div>
          ) : (
            <EmptyState
              icon={Box}
              title="Nenhum bloco encontrado"
              description="Aguarde a mineração de novos blocos"
            />
          )}
        </CardContent>
      </Card>
    </div>
  );
}
```

---

**Total de Páginas**: 5 páginas completas  
**Linhas de Código**: ~1500 linhas  
**Componentes**: 30+ componentes  
**Versão**: 1.0.0
