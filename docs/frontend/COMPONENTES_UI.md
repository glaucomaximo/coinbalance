# 🎨 Guia de Componentes UI - CoinBalance

## Biblioteca Completa de Componentes

Este guia apresenta todos os componentes UI do CoinBalance com exemplos de uso e variações.

---

## 📋 Índice

1. [Buttons](#buttons)
2. [Cards](#cards)
3. [Inputs e Forms](#inputs-e-forms)
4. [Modals e Dialogs](#modals-e-dialogs)
5. [Tables](#tables)
6. [Charts](#charts)
7. [Navigation](#navigation)
8. [Feedback](#feedback)
9. [Loading States](#loading-states)
10. [Layout](#layout)

---

## 🔘 Buttons

### Button Base

```tsx
import { Button } from '@/components/ui/button';

// Variantes
<Button variant="primary">Primary Button</Button>
<Button variant="secondary">Secondary Button</Button>
<Button variant="outline">Outline Button</Button>
<Button variant="ghost">Ghost Button</Button>
<Button variant="danger">Danger Button</Button>

// Tamanhos
<Button size="sm">Small</Button>
<Button size="md">Medium</Button>
<Button size="lg">Large</Button>
<Button size="xl">Extra Large</Button>

// Com loading
<Button isLoading>Processing...</Button>

// Com ícone
import { Wallet } from 'lucide-react';
<Button>
  <Wallet className="mr-2 h-4 w-4" />
  Nova Carteira
</Button>

// Disabled
<Button disabled>Disabled Button</Button>
```

### Button Group

```tsx
export const ButtonGroup = () => {
  return (
    <div className="inline-flex rounded-lg border border-gray-200">
      <Button variant="ghost" className="rounded-r-none">
        Dia
      </Button>
      <Button variant="ghost" className="rounded-none border-x">
        Semana
      </Button>
      <Button variant="ghost" className="rounded-l-none">
        Mês
      </Button>
    </div>
  );
};
```

### Icon Button

```tsx
import { Settings, Bell, User } from 'lucide-react';

export const IconButtons = () => {
  return (
    <div className="flex gap-2">
      <Button variant="ghost" size="sm" className="w-10 h-10 p-0">
        <Settings className="h-4 w-4" />
      </Button>
      <Button variant="ghost" size="sm" className="w-10 h-10 p-0 relative">
        <Bell className="h-4 w-4" />
        <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
      </Button>
      <Button variant="ghost" size="sm" className="w-10 h-10 p-0">
        <User className="h-4 w-4" />
      </Button>
    </div>
  );
};
```

---

## 🎴 Cards

### Card Básico

```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';

export const BasicCard = () => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Título do Card</CardTitle>
        <CardDescription>Descrição do card</CardDescription>
      </CardHeader>
      <CardContent>
        <p>Conteúdo do card vai aqui</p>
      </CardContent>
      <CardFooter>
        <Button>Ação</Button>
      </CardFooter>
    </Card>
  );
};
```

### Wallet Card

```tsx
import { Wallet, TrendingUp, Copy } from 'lucide-react';

export const WalletCard = ({ wallet }: { wallet: any }) => {
  return (
    <Card className="hover:shadow-lg transition-shadow cursor-pointer">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
              <Wallet className="w-6 h-6 text-white" />
            </div>
            <div>
              <CardTitle className="text-lg">{wallet.name}</CardTitle>
              <CardDescription className="flex items-center gap-1">
                {wallet.address.substring(0, 10)}...
                <Copy className="w-3 h-3 cursor-pointer hover:text-primary" />
              </CardDescription>
            </div>
          </div>
          <span className="text-xs text-green-500 flex items-center gap-1">
            <TrendingUp className="w-3 h-3" />
            +2.5%
          </span>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <div>
            <p className="text-sm text-gray-500">Saldo</p>
            <p className="text-2xl font-bold">{wallet.balance_cnb} CNB</p>
            <p className="text-xs text-gray-400">{wallet.balance_satoshi} satoshis</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
```

### Stat Card

```tsx
export const StatCard = ({ title, value, change, icon: Icon }: any) => {
  const isPositive = change >= 0;
  
  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-500 mb-1">{title}</p>
            <p className="text-3xl font-bold">{value}</p>
            <p className={`text-sm mt-1 ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
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
```

---

## 📝 Inputs e Forms

### Input Base

```tsx
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export const InputExample = () => {
  return (
    <div className="space-y-2">
      <Label htmlFor="email">Email</Label>
      <Input 
        id="email" 
        type="email" 
        placeholder="seu@email.com"
      />
    </div>
  );
};
```

### Input com Ícone

```tsx
import { Search, Mail, Lock } from 'lucide-react';

export const InputWithIcon = () => {
  return (
    <div className="space-y-4">
      {/* Left Icon */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
        <Input placeholder="Buscar..." className="pl-10" />
      </div>

      {/* Right Icon */}
      <div className="relative">
        <Input type="email" placeholder="Email" />
        <Mail className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
      </div>
    </div>
  );
};
```

### Form com Validação (React Hook Form + Zod)

```tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

const transferSchema = z.object({
  from_address: z.string().min(1, 'Selecione uma carteira'),
  to_address: z.string().min(10, 'Endereço inválido'),
  amount: z.number().positive('Valor deve ser maior que zero'),
  memo: z.string().optional(),
});

type TransferFormData = z.infer<typeof transferSchema>;

export const TransferForm = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<TransferFormData>({
    resolver: zodResolver(transferSchema),
  });

  const onSubmit = (data: TransferFormData) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <Label htmlFor="from">De</Label>
        <Input {...register('from_address')} />
        {errors.from_address && (
          <p className="text-sm text-red-500 mt-1">{errors.from_address.message}</p>
        )}
      </div>

      <div>
        <Label htmlFor="to">Para</Label>
        <Input {...register('to_address')} placeholder="Endereço de destino" />
        {errors.to_address && (
          <p className="text-sm text-red-500 mt-1">{errors.to_address.message}</p>
        )}
      </div>

      <div>
        <Label htmlFor="amount">Valor (CNB)</Label>
        <Input 
          {...register('amount', { valueAsNumber: true })} 
          type="number" 
          step="0.00000001"
          placeholder="0.00"
        />
        {errors.amount && (
          <p className="text-sm text-red-500 mt-1">{errors.amount.message}</p>
        )}
      </div>

      <div>
        <Label htmlFor="memo">Descrição (opcional)</Label>
        <Input {...register('memo')} placeholder="Descrição da transferência" />
      </div>

      <Button type="submit" className="w-full">
        Transferir
      </Button>
    </form>
  );
};
```

### Select / Dropdown

```tsx
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

export const SelectExample = () => {
  return (
    <Select>
      <SelectTrigger className="w-full">
        <SelectValue placeholder="Selecione uma carteira" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="wallet1">Carteira Principal</SelectItem>
        <SelectItem value="wallet2">Carteira Secundária</SelectItem>
        <SelectItem value="wallet3">Carteira de Investimentos</SelectItem>
      </SelectContent>
    </Select>
  );
};
```

---

## 🪟 Modals e Dialogs

### Dialog Base

```tsx
'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';

export const DialogExample = () => {
  const [open, setOpen] = useState(false);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Abrir Modal</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Título do Modal</DialogTitle>
          <DialogDescription>
            Descrição do modal vai aqui.
          </DialogDescription>
        </DialogHeader>
        <div className="py-4">
          {/* Conteúdo do modal */}
        </div>
      </DialogContent>
    </Dialog>
  );
};
```

### Create Wallet Modal

```tsx
export const CreateWalletModal = () => {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');

  const handleCreate = async () => {
    // Lógica de criação
    setOpen(false);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Wallet className="mr-2 h-4 w-4" />
          Nova Carteira
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Criar Nova Carteira</DialogTitle>
          <DialogDescription>
            Crie uma nova carteira digital segura.
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-4 py-4">
          <div>
            <Label htmlFor="name">Nome da Carteira</Label>
            <Input 
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Minha Carteira"
            />
          </div>
          <div>
            <Label htmlFor="password">Senha (opcional)</Label>
            <Input 
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
            <p className="text-xs text-gray-500 mt-1">
              Recomendado para maior segurança
            </p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="flex-1" onClick={() => setOpen(false)}>
            Cancelar
          </Button>
          <Button className="flex-1" onClick={handleCreate}>
            Criar Carteira
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};
```

---

## 📊 Tables

### Table Responsiva

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

export const TransactionsTable = ({ transactions }: any) => {
  return (
    <>
      {/* Desktop */}
      <div className="hidden md:block rounded-lg border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>De</TableHead>
              <TableHead>Para</TableHead>
              <TableHead>Valor</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Data</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {transactions.map((tx: any) => (
              <TableRow key={tx.id}>
                <TableCell className="font-mono text-sm">
                  {tx.id.substring(0, 8)}...
                </TableCell>
                <TableCell>{tx.from_address.substring(0, 10)}...</TableCell>
                <TableCell>{tx.to_address.substring(0, 10)}...</TableCell>
                <TableCell className="font-semibold">{tx.amount_cnb} CNB</TableCell>
                <TableCell>
                  <StatusBadge status={tx.status} />
                </TableCell>
                <TableCell>{new Date(tx.created_at).toLocaleDateString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {/* Mobile */}
      <div className="md:hidden space-y-3">
        {transactions.map((tx: any) => (
          <Card key={tx.id}>
            <CardContent className="p-4">
              <div className="flex justify-between items-start mb-2">
                <span className="font-mono text-xs text-gray-500">
                  {tx.id.substring(0, 12)}...
                </span>
                <StatusBadge status={tx.status} />
              </div>
              <div className="space-y-1">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">Valor:</span>
                  <span className="font-semibold">{tx.amount_cnb} CNB</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">Data:</span>
                  <span className="text-sm">{new Date(tx.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </>
  );
};

const StatusBadge = ({ status }: { status: string }) => {
  const colors = {
    pending: 'bg-yellow-100 text-yellow-800',
    confirmed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
  };

  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status as keyof typeof colors]}`}>
      {status}
    </span>
  );
};
```

---

## 📈 Charts

### Balance Chart (Recharts)

```tsx
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';

export const BalanceChart = ({ data }: any) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Saldo (Últimos 7 dias)</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorBalance" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <XAxis 
              dataKey="date" 
              stroke="#888888"
              fontSize={12}
            />
            <YAxis 
              stroke="#888888"
              fontSize={12}
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
              }}
            />
            <Area 
              type="monotone" 
              dataKey="balance" 
              stroke="#0ea5e9" 
              strokeWidth={2}
              fill="url(#colorBalance)"
              animationDuration={1500}
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};
```

---

## 🧭 Navigation

### Sidebar

```tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Wallet, ArrowRightLeft, Box, Settings } from 'lucide-react';

const navItems = [
  { href: '/dashboard', icon: Home, label: 'Dashboard' },
  { href: '/wallets', icon: Wallet, label: 'Carteiras' },
  { href: '/transactions', icon: ArrowRightLeft, label: 'Transações' },
  { href: '/blockchain', icon: Box, label: 'Blockchain' },
  { href: '/settings', icon: Settings, label: 'Configurações' },
];

export const Sidebar = () => {
  const pathname = usePathname();

  return (
    <aside className="hidden lg:flex lg:w-64 lg:flex-col border-r bg-white">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-primary">CoinBalance</h1>
      </div>
      <nav className="flex-1 px-4 space-y-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive 
                  ? 'bg-primary text-white' 
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <item.icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
};
```

---

## 💬 Feedback

### Toast / Notifications

```tsx
import { useToast } from '@/components/ui/use-toast';

export const ToastExample = () => {
  const { toast } = useToast();

  return (
    <div className="space-x-2">
      <Button onClick={() => {
        toast({
          title: "Sucesso!",
          description: "Operação realizada com sucesso.",
        });
      }}>
        Success Toast
      </Button>

      <Button onClick={() => {
        toast({
          variant: "destructive",
          title: "Erro",
          description: "Ocorreu um erro ao processar.",
        });
      }}>
        Error Toast
      </Button>
    </div>
  );
};
```

---

## ⏳ Loading States

### Skeleton Loader

```tsx
export const WalletListSkeleton = () => {
  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
      {[1, 2, 3].map((i) => (
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
};
```

### Spinner

```tsx
export const Spinner = ({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <div className={`${sizes[size]} animate-spin rounded-full border-4 border-gray-200 border-t-primary`} />
  );
};
```

---

**Total de Componentes**: 20+  
**Versão**: 1.0.0  
**Última Atualização**: 2025-10-28
