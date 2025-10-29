'use client';

import { useEffect, useState } from 'react';
import { Box, Activity, Clock, Zap } from 'lucide-react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '@/components/ui/table';
import { blockchainService } from '@/services/blockchain.service';
import type { Block, BlockchainStats } from '@/types';
import { formatCurrency, formatDateTime, truncateAddress } from '@/lib/utils';

export default function BlockchainPage() {
  const [stats, setStats] = useState<BlockchainStats | null>(null);
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [statsData, blocksData] = await Promise.all([
          blockchainService.getStats(),
          blockchainService.getBlocks(),
        ]);

        setStats(statsData);
        setBlocks(blocksData.slice(0, 20)); // Últimos 20 blocos
      } catch (error) {
        console.error('Failed to load blockchain data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  return (
    <DashboardLayout>
      <div className="p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Blockchain Explorer</h1>
          <p className="text-gray-600 mt-1">
            Explore blocos e estatísticas da blockchain
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="border-2 hover:border-blue-500 transition-colors">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center gap-2">
                <Box className="w-4 h-4" />
                Total de Blocos
              </CardTitle>
            </CardHeader>
            <CardContent>
              {loading ? (
                <Skeleton className="h-8 w-20" />
              ) : (
                <div className="text-2xl font-bold text-gray-900">
                  {stats?.total_blocks || 0}
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="border-2 hover:border-purple-500 transition-colors">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center gap-2">
                <Activity className="w-4 h-4" />
                Transações
              </CardTitle>
            </CardHeader>
            <CardContent>
              {loading ? (
                <Skeleton className="h-8 w-20" />
              ) : (
                <div className="text-2xl font-bold text-gray-900">
                  {stats?.total_transactions || 0}
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="border-2 hover:border-green-500 transition-colors">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center gap-2">
                <Clock className="w-4 h-4" />
                Tempo Médio
              </CardTitle>
            </CardHeader>
            <CardContent>
              {loading ? (
                <Skeleton className="h-8 w-20" />
              ) : (
                <div className="text-2xl font-bold text-gray-900">
                  {stats?.average_block_time?.toFixed(2) || 0}s
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="border-2 hover:border-orange-500 transition-colors">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center gap-2">
                <Zap className="w-4 h-4" />
                Dificuldade
              </CardTitle>
            </CardHeader>
            <CardContent>
              {loading ? (
                <Skeleton className="h-8 w-20" />
              ) : (
                <div className="text-2xl font-bold text-gray-900">
                  {stats?.current_difficulty || 0}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Additional Stats */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <Card>
            <CardHeader>
              <CardTitle>Informações da Blockchain</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between items-center py-2 border-b">
                <span className="text-sm text-gray-600">Nome</span>
                <span className="font-medium">{stats?.name || '-'}</span>
              </div>
              <div className="flex justify-between items-center py-2 border-b">
                <span className="text-sm text-gray-600">Versão</span>
                <span className="font-medium">{stats?.version || '-'}</span>
              </div>
              <div className="flex justify-between items-center py-2 border-b">
                <span className="text-sm text-gray-600">Supply Total</span>
                <span className="font-medium">
                  {formatCurrency(stats?.total_supply || 0)} CNB
                </span>
              </div>
              <div className="flex justify-between items-center py-2 border-b">
                <span className="text-sm text-gray-600">Recompensa por Bloco</span>
                <span className="font-medium">
                  {stats?.current_block_reward || 0} CNB
                </span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span className="text-sm text-gray-600">Status da Chain</span>
                <span className={`font-medium ${stats?.chain_valid ? 'text-green-600' : 'text-red-600'}`}>
                  {stats?.chain_valid ? 'Válida' : 'Inválida'}
                </span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Últimas Atividades</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center gap-3 p-3 rounded-lg bg-blue-50">
                <Box className="w-5 h-5 text-blue-600" />
                <div className="flex-1">
                  <p className="text-sm font-medium">Último Bloco Minerado</p>
                  <p className="text-xs text-gray-600">
                    Bloco #{stats?.latest_block_height || 0}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 rounded-lg bg-green-50">
                <Activity className="w-5 h-5 text-green-600" />
                <div className="flex-1">
                  <p className="text-sm font-medium">Tempo Total de Mineração</p>
                  <p className="text-xs text-gray-600">
                    {stats?.total_mining_time?.toFixed(2) || 0} segundos
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 rounded-lg bg-purple-50">
                <Zap className="w-5 h-5 text-purple-600" />
                <div className="flex-1">
                  <p className="text-sm font-medium">Dificuldade Atual</p>
                  <p className="text-xs text-gray-600">
                    Nível {stats?.current_difficulty || 0}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Blocks Table */}
        <Card>
          <CardHeader>
            <CardTitle>Blocos Recentes</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-3">
                {[1, 2, 3, 4, 5].map((i) => (
                  <Skeleton key={i} className="h-16 w-full" />
                ))}
              </div>
            ) : blocks.length === 0 ? (
              <div className="text-center py-12">
                <Box className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-600">Nenhum bloco encontrado</p>
              </div>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Altura</TableHead>
                    <TableHead>Hash</TableHead>
                    <TableHead>Transações</TableHead>
                    <TableHead>Minerador</TableHead>
                    <TableHead>Tempo</TableHead>
                    <TableHead>Data</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {blocks.map((block) => (
                    <TableRow key={block.height}>
                      <TableCell className="font-bold">
                        #{block.height}
                      </TableCell>
                      <TableCell className="font-mono text-xs">
                        {truncateAddress(block.hash, 8, 8)}
                      </TableCell>
                      <TableCell>
                        <span className="inline-flex items-center px-2 py-1 rounded-md bg-blue-100 text-blue-700 text-xs font-medium">
                          {block.transactions_count}
                        </span>
                      </TableCell>
                      <TableCell className="font-mono text-xs">
                        {block.miner_address ? truncateAddress(block.miner_address) : '-'}
                      </TableCell>
                      <TableCell className="text-sm">
                        {block.mining_time.toFixed(2)}s
                      </TableCell>
                      <TableCell className="text-xs text-gray-600">
                        {formatDateTime(block.timestamp)}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
