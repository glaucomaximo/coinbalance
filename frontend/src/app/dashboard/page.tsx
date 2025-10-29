'use client';

import { useEffect, useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { walletService } from '@/services/wallet.service';
import { transactionService } from '@/services/transaction.service';
import { blockchainService } from '@/services/blockchain.service';
import { formatCurrency } from '@/lib/utils';
import { Wallet, ArrowRightLeft, Box, TrendingUp } from 'lucide-react';

export default function DashboardPage() {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalBalance: 0,
    totalWallets: 0,
    totalTransactions: 0,
    totalBlocks: 0,
  });

  useEffect(() => {
    const loadStats = async () => {
      try {
        const [wallets, transactions, blockchain] = await Promise.all([
          walletService.listWallets(),
          transactionService.getTransactionStats(),
          blockchainService.getStats(),
        ]);

        const totalBalance = wallets.wallets.reduce(
          (sum, wallet) => sum + wallet.balance_cnb,
          0
        );

        setStats({
          totalBalance,
          totalWallets: wallets.total,
          totalTransactions: transactions.total_transactions,
          totalBlocks: blockchain.total_blocks,
        });
      } catch (error) {
        console.error('Failed to load stats:', error);
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, []);

  return (
    <DashboardLayout>
      <div className="p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">
            Visão geral da sua conta e atividades
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Total Balance */}
          <Card className="border-2 hover:border-primary-500 transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                Saldo Total
              </CardTitle>
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
                <Wallet className="w-5 h-5 text-white" />
              </div>
            </CardHeader>
            <CardContent>
              {loading ? (
                <Skeleton className="h-8 w-32" />
              ) : (
                <>
                  <div className="text-2xl font-bold text-gray-900">
                    {formatCurrency(stats.totalBalance)} CNB
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    Em {stats.totalWallets} carteira(s)
                  </p>
                </>
              )}
            </CardContent>
          </Card>

          {/* Total Wallets */}
          <Card className="border-2 hover:border-purple-500 transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                Carteiras
              </CardTitle>
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center">
                <Wallet className="w-5 h-5 text-white" />
              </div>
            </CardHeader>
            <CardContent>
              {loading ? (
                <Skeleton className="h-8 w-20" />
              ) : (
                <>
                  <div className="text-2xl font-bold text-gray-900">
                    {stats.totalWallets}
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    Carteiras ativas
                  </p>
                </>
              )}
            </CardContent>
          </Card>

          {/* Total Transactions */}
          <Card className="border-2 hover:border-green-500 transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                Transações
              </CardTitle>
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center">
                <ArrowRightLeft className="w-5 h-5 text-white" />
              </div>
            </CardHeader>
            <CardContent>
              {loading ? (
                <Skeleton className="h-8 w-20" />
              ) : (
                <>
                  <div className="text-2xl font-bold text-gray-900">
                    {stats.totalTransactions}
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    Transações realizadas
                  </p>
                </>
              )}
            </CardContent>
          </Card>

          {/* Total Blocks */}
          <Card className="border-2 hover:border-orange-500 transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                Blocos
              </CardTitle>
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-orange-500 to-orange-600 flex items-center justify-center">
                <Box className="w-5 h-5 text-white" />
              </div>
            </CardHeader>
            <CardContent>
              {loading ? (
                <Skeleton className="h-8 w-20" />
              ) : (
                <>
                  <div className="text-2xl font-bold text-gray-900">
                    {stats.totalBlocks}
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    Blocos minerados
                  </p>
                </>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Ações Rápidas</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <button className="w-full p-4 rounded-lg border-2 border-gray-200 hover:border-primary-500 hover:bg-primary-50 transition-all text-left">
                <div className="flex items-center gap-3">
                  <Wallet className="w-5 h-5 text-primary-600" />
                  <div>
                    <p className="font-medium">Nova Carteira</p>
                    <p className="text-sm text-gray-500">Criar uma nova carteira digital</p>
                  </div>
                </div>
              </button>
              
              <button className="w-full p-4 rounded-lg border-2 border-gray-200 hover:border-primary-500 hover:bg-primary-50 transition-all text-left">
                <div className="flex items-center gap-3">
                  <ArrowRightLeft className="w-5 h-5 text-primary-600" />
                  <div>
                    <p className="font-medium">Nova Transferência</p>
                    <p className="text-sm text-gray-500">Enviar CNB para outra carteira</p>
                  </div>
                </div>
              </button>
              
              <button className="w-full p-4 rounded-lg border-2 border-gray-200 hover:border-primary-500 hover:bg-primary-50 transition-all text-left">
                <div className="flex items-center gap-3">
                  <Box className="w-5 h-5 text-primary-600" />
                  <div>
                    <p className="font-medium">Minerar Bloco</p>
                    <p className="text-sm text-gray-500">Minerar um novo bloco na blockchain</p>
                  </div>
                </div>
              </button>
            </CardContent>
          </Card>

          {/* System Status */}
          <Card>
            <CardHeader>
              <CardTitle>Status do Sistema</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500" />
                  <span className="text-sm font-medium">Blockchain</span>
                </div>
                <span className="text-sm text-gray-500">Online</span>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500" />
                  <span className="text-sm font-medium">API</span>
                </div>
                <span className="text-sm text-gray-500">Operacional</span>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500" />
                  <span className="text-sm font-medium">Mineração</span>
                </div>
                <span className="text-sm text-gray-500">Ativa</span>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500" />
                  <span className="text-sm font-medium">IA & Analytics</span>
                </div>
                <span className="text-sm text-gray-500">Disponível</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
