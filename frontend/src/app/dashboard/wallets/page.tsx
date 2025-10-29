'use client';

import { useEffect, useState } from 'react';
import { Plus, Wallet as WalletIcon, Copy, Check } from 'lucide-react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle, 
  DialogBody, 
  DialogFooter,
  DialogClose
} from '@/components/ui/dialog';
import { useToast } from '@/components/ui/toast';
import { walletService } from '@/services/wallet.service';
import type { Wallet } from '@/types';
import { formatCurrency, truncateAddress, copyToClipboard } from '@/lib/utils';

export default function WalletsPage() {
  const { showToast } = useToast();
  const [wallets, setWallets] = useState<Wallet[]>([]);
  const [loading, setLoading] = useState(true);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [newWalletName, setNewWalletName] = useState('');
  const [creating, setCreating] = useState(false);
  const [copiedAddress, setCopiedAddress] = useState<string | null>(null);

  const loadWallets = async () => {
    try {
      const response = await walletService.listWallets();
      setWallets(response.wallets);
    } catch (error) {
      showToast('Erro ao carregar carteiras', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWallets();
  }, []);

  const handleCreateWallet = async () => {
    if (!newWalletName.trim()) {
      showToast('Digite um nome para a carteira', 'warning');
      return;
    }

    setCreating(true);
    try {
      await walletService.createWallet({ name: newWalletName });
      showToast('Carteira criada com sucesso!', 'success');
      setCreateDialogOpen(false);
      setNewWalletName('');
      loadWallets();
    } catch (error: any) {
      showToast(error.response?.data?.detail || 'Erro ao criar carteira', 'error');
    } finally {
      setCreating(false);
    }
  };

  const handleCopyAddress = async (address: string) => {
    try {
      await copyToClipboard(address);
      setCopiedAddress(address);
      showToast('Endereço copiado!', 'success');
      setTimeout(() => setCopiedAddress(null), 2000);
    } catch (error) {
      showToast('Erro ao copiar endereço', 'error');
    }
  };

  return (
    <DashboardLayout>
      <div className="p-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Carteiras</h1>
            <p className="text-gray-600 mt-1">
              Gerencie suas carteiras digitais
            </p>
          </div>
          <Button onClick={() => setCreateDialogOpen(true)}>
            <Plus className="w-4 h-4 mr-2" />
            Nova Carteira
          </Button>
        </div>

        {/* Wallets Grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <Card key={i}>
                <CardHeader>
                  <Skeleton className="h-6 w-32" />
                </CardHeader>
                <CardContent className="space-y-3">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-8 w-24" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : wallets.length === 0 ? (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <WalletIcon className="w-16 h-16 text-gray-300 mb-4" />
              <p className="text-gray-600 mb-4">Você ainda não tem carteiras</p>
              <Button onClick={() => setCreateDialogOpen(true)}>
                <Plus className="w-4 h-4 mr-2" />
                Criar Primeira Carteira
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {wallets.map((wallet) => (
              <Card 
                key={wallet.address}
                className="hover:shadow-lg transition-shadow border-2 hover:border-primary-500"
              >
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{wallet.name}</CardTitle>
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                      <WalletIcon className="w-5 h-5 text-white" />
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Address */}
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Endereço</p>
                    <div className="flex items-center gap-2">
                      <code className="text-sm font-mono text-gray-700">
                        {truncateAddress(wallet.address, 8, 6)}
                      </code>
                      <button
                        onClick={() => handleCopyAddress(wallet.address)}
                        className="p-1 hover:bg-gray-100 rounded transition-colors"
                      >
                        {copiedAddress === wallet.address ? (
                          <Check className="w-4 h-4 text-green-600" />
                        ) : (
                          <Copy className="w-4 h-4 text-gray-600" />
                        )}
                      </button>
                    </div>
                  </div>

                  {/* Balance */}
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Saldo</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {formatCurrency(wallet.balance_cnb)} CNB
                    </p>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2 pt-2">
                    <Button variant="outline" size="sm" className="flex-1">
                      Enviar
                    </Button>
                    <Button variant="outline" size="sm" className="flex-1">
                      Receber
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Create Wallet Dialog */}
        <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
          <DialogContent>
            <DialogClose onClose={() => setCreateDialogOpen(false)} />
            <DialogHeader>
              <DialogTitle>Criar Nova Carteira</DialogTitle>
            </DialogHeader>
            <DialogBody>
              <div className="space-y-4">
                <div>
                  <label htmlFor="wallet-name" className="text-sm font-medium mb-2 block">
                    Nome da Carteira
                  </label>
                  <Input
                    id="wallet-name"
                    placeholder="Ex: Carteira Principal"
                    value={newWalletName}
                    onChange={(e) => setNewWalletName(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !creating) {
                        handleCreateWallet();
                      }
                    }}
                  />
                </div>
                <p className="text-sm text-gray-500">
                  Uma nova carteira será criada com um par de chaves criptográficas único.
                </p>
              </div>
            </DialogBody>
            <DialogFooter>
              <Button
                variant="outline"
                onClick={() => setCreateDialogOpen(false)}
                disabled={creating}
              >
                Cancelar
              </Button>
              <Button onClick={handleCreateWallet} isLoading={creating}>
                Criar Carteira
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </DashboardLayout>
  );
}
