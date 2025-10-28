// Auth Types
export interface User {
  id: string;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: number;
  last_login: number | null;
  permissions: string[];
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

// Wallet Types
export interface Wallet {
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

export interface CreateWalletData {
  name: string;
  password?: string;
  metadata?: Record<string, any>;
}

// Transaction Types
export interface Transaction {
  id: string;
  from_address: string | null;
  to_address: string;
  amount_cnb: string;
  fee_cnb: string;
  transaction_type: string;
  status: 'pending' | 'confirmed' | 'failed';
  created_at: number;
  confirmed_at: number | null;
  block_height: number | null;
  transaction_hash: string | null;
  memo: string | null;
  metadata: Record<string, any>;
}

export interface CreateTransferData {
  from_address: string;
  to_address: string;
  amount: string | number;
  fee?: string | number;
  memo?: string;
  metadata?: Record<string, any>;
}

// Blockchain Types
export interface Block {
  height: number;
  hash: string;
  previous_hash: string | null;
  timestamp: number;
  nonce: number;
  difficulty: number;
  mining_time: number;
  miner_address: string | null;
  block_reward: string;
  total_fees: string;
  transactions_count: number;
}

export interface BlockchainStats {
  name: string;
  version: string;
  total_blocks: number;
  total_transactions: number;
  current_difficulty: number;
  average_block_time: number;
  total_mining_time: number;
  current_block_reward: number;
  total_supply: number;
  chain_valid: boolean;
  latest_block_height: number;
}

// API Response Types
export interface ApiError {
  detail: {
    error: string;
    code: string;
    message?: string;
  };
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

// Common Types
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface SelectOption {
  label: string;
  value: string;
}
