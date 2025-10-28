import { apiClient } from '@/lib/api/client';

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

export interface WalletListResponse {
  wallets: WalletResponse[];
  total: number;
}

export interface WalletOperationRequest {
  amount: number;
  reason: string;
}

export class WalletService {
  async createWallet(data: CreateWalletRequest): Promise<WalletResponse> {
    return apiClient.post<WalletResponse>('/api/v1/carteiras', data);
  }

  async getWallet(address: string): Promise<WalletResponse> {
    return apiClient.get<WalletResponse>(`/api/v1/carteiras/${address}`);
  }

  async listWallets(): Promise<WalletListResponse> {
    return apiClient.get<WalletListResponse>('/api/v1/carteiras');
  }

  async creditWallet(
    address: string,
    data: WalletOperationRequest
  ): Promise<any> {
    return apiClient.post(`/api/v1/carteiras/${address}/creditar`, data);
  }

  async debitWallet(
    address: string,
    data: WalletOperationRequest
  ): Promise<any> {
    return apiClient.post(`/api/v1/carteiras/${address}/debitar`, data);
  }
}

export const walletService = new WalletService();
