import { apiClient } from '@/lib/api/client';
import type { Transaction, CreateTransferData } from '@/types';

export interface TransactionListParams {
  address?: string;
  limit?: number;
  offset?: number;
}

export interface TransactionListResponse {
  transactions: Transaction[];
  total: number;
  limit: number;
  offset: number;
}

export interface TransactionStats {
  total_transactions: number;
  total_volume_cnb: string;
  total_fees_cnb: string;
  pending_transactions: number;
  confirmed_transactions: number;
  failed_transactions: number;
}

export class TransactionService {
  async createTransfer(data: CreateTransferData): Promise<Transaction> {
    return apiClient.post<Transaction>('/api/v1/transferencias', data);
  }

  async getTransactionHistory(
    params?: TransactionListParams
  ): Promise<TransactionListResponse> {
    return apiClient.get<TransactionListResponse>(
      '/api/v1/transacoes/historico',
      { params }
    );
  }

  async getTransaction(id: string): Promise<Transaction> {
    return apiClient.get<Transaction>(`/api/v1/transacoes/${id}`);
  }

  async getTransactionStats(): Promise<TransactionStats> {
    return apiClient.get<TransactionStats>('/api/v1/transacoes/stats');
  }
}

export const transactionService = new TransactionService();
