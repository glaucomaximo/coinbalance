import { apiClient } from '@/lib/api/client';
import type { Block, BlockchainStats } from '@/types';

export interface MineBlockRequest {
  miner_address: string;
  max_transactions?: number;
}

export interface MiningStats {
  blocks_mined: number;
  total_mining_time: number;
  average_mining_time: number;
  current_difficulty: number;
  current_reward: string;
  estimated_hash_rate: number;
  pool_size: number;
  estimated_mining_time: number;
}

export class BlockchainService {
  async getStats(): Promise<BlockchainStats> {
    return apiClient.get<BlockchainStats>('/api/v1/blockchain/stats');
  }

  async getBlocks(): Promise<Block[]> {
    return apiClient.get<Block[]>('/api/v1/blockchain/blocks');
  }

  async getBlock(height: number): Promise<Block> {
    return apiClient.get<Block>(`/api/v1/blockchain/blocks/${height}`);
  }

  async mineBlock(data: MineBlockRequest): Promise<Block> {
    return apiClient.post<Block>('/api/v1/blockchain/mine', data);
  }

  async validateChain(): Promise<{ valid: boolean; errors?: string[] }> {
    return apiClient.get('/api/v1/blockchain/validate');
  }

  async getMiningStats(): Promise<MiningStats> {
    return apiClient.get<MiningStats>('/api/v1/blockchain/mining/stats');
  }
}

export const blockchainService = new BlockchainService();
