# 🌐 Manual de Integração Front-End - CoinBalance

## 📋 Índice

1. [Introdução](#introdução)
2. [Configuração Inicial](#configuração-inicial)
3. [Autenticação e Autorização](#autenticação-e-autorização)
4. [Módulos da API](#módulos-da-api)
5. [Exemplos de Integração](#exemplos-de-integração)
6. [Tratamento de Erros](#tratamento-de-erros)
7. [Boas Práticas](#boas-práticas)
8. [SDK JavaScript/TypeScript](#sdk-javascripttypescript)
9. [Testes e Debugging](#testes-e-debugging)
10. [Referência Completa de Endpoints](#referência-completa-de-endpoints)

---

## 📖 Introdução

Este manual fornece todas as informações necessárias para integrar sua aplicação front-end com a API do **CoinBalance**, uma blockchain enterprise completa com recursos de carteira digital, transações, IA, Web3 e muito mais.

### Características da API

- **Arquitetura REST**: Endpoints RESTful padronizados
- **Autenticação JWT**: Tokens seguros com escopos granulares
- **Documentação Interativa**: Swagger UI e ReDoc disponíveis
- **Rate Limiting**: Proteção contra abuso
- **CORS Configurado**: Suporte a requisições cross-origin
- **Versionamento**: API versionada (v1)

### URLs Base

```
Desenvolvimento: http://localhost:8000
Produção: https://api.coinbalance.com
```

### Documentação Interativa

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## ⚙️ Configuração Inicial

### 1. Requisitos

- Node.js 16+ ou navegador moderno
- Axios, Fetch API ou biblioteca HTTP de sua escolha
- TypeScript (recomendado)

### 2. Instalação de Dependências

```bash
# Com npm
npm install axios

# Com yarn
yarn add axios

# Com pnpm
pnpm add axios
```

### 3. Configuração Base

Crie um arquivo de configuração para a API:

```typescript
// src/config/api.ts
export const API_CONFIG = {
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
};

export const API_ENDPOINTS = {
  // Autenticação
  LOGIN: '/api/v1/auth/login',
  LOGOUT: '/api/v1/auth/logout',
  REGISTER: '/api/v1/auth/users',
  ME: '/api/v1/auth/me',
  
  // Carteiras
  WALLETS: '/api/v1/carteiras',
  WALLET_BY_ADDRESS: (address: string) => `/api/v1/carteiras/${address}`,
  WALLET_CREDIT: (address: string) => `/api/v1/carteiras/${address}/creditar`,
  WALLET_DEBIT: (address: string) => `/api/v1/carteiras/${address}/debitar`,
  
  // Transações
  TRANSACTIONS: '/api/v1/transferencias',
  TRANSACTION_HISTORY: '/api/v1/transacoes/historico',
  TRANSACTION_STATS: '/api/v1/transacoes/stats',
  
  // Blockchain
  BLOCKCHAIN_STATS: '/api/v1/blockchain/stats',
  BLOCKCHAIN_BLOCKS: '/api/v1/blockchain/blocks',
  BLOCKCHAIN_MINE: '/api/v1/blockchain/mine',
  
  // Health & Monitoring
  HEALTH: '/api/v1/health',
  METRICS: '/api/v1/metrics',
  
  // Web3
  WEB3_BALANCE: '/api/v1/web3/balance',
  WEB3_NFT: '/api/v1/web3/nft',
  
  // IA
  AI_PREDICT: '/api/v1/ai-advanced/predict',
  AI_TRAIN: '/api/v1/ai-advanced/train-model',
};
```

### 4. Cliente HTTP com Axios

```typescript
// src/services/apiClient.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { API_CONFIG } from '../config/api';

class ApiClient {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.client = axios.create(API_CONFIG);
    
    // Interceptor para adicionar token em todas as requisições
    this.client.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Interceptor para tratamento de respostas
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token expirado ou inválido
          this.clearToken();
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  setToken(token: string): void {
    this.token = token;
    localStorage.setItem('authToken', token);
  }

  clearToken(): void {
    this.token = null;
    localStorage.removeItem('authToken');
  }

  loadToken(): void {
    const token = localStorage.getItem('authToken');
    if (token) {
      this.token = token;
    }
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }
}

export const apiClient = new ApiClient();
```

---

## 🔐 Autenticação e Autorização

### 1. Sistema de Autenticação

A API utiliza **JWT (JSON Web Tokens)** para autenticação com escopos de permissão granulares.

### 2. Fluxo de Autenticação

```typescript
// src/services/authService.ts
import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '../config/api';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: string;
    username: string;
    email: string;
    role: string;
    permissions: string[];
  };
}

export interface UserInfo {
  id: string;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: number;
  last_login: number | null;
  permissions: string[];
}

export interface CreateUserRequest {
  username: string;
  email: string;
  password: string;
  role: string;
  metadata?: Record<string, any>;
}

export class AuthService {
  /**
   * Realiza login do usuário
   */
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>(
      API_ENDPOINTS.LOGIN,
      credentials
    );
    
    // Salvar token
    apiClient.setToken(response.access_token);
    
    return response;
  }

  /**
   * Realiza logout do usuário
   */
  async logout(): Promise<void> {
    try {
      await apiClient.post(API_ENDPOINTS.LOGOUT);
    } finally {
      apiClient.clearToken();
    }
  }

  /**
   * Obtém informações do usuário atual
   */
  async getCurrentUser(): Promise<UserInfo> {
    return apiClient.get<UserInfo>(API_ENDPOINTS.ME);
  }

  /**
   * Cria novo usuário (requer permissão users:create)
   */
  async createUser(userData: CreateUserRequest): Promise<any> {
    return apiClient.post(API_ENDPOINTS.REGISTER, userData);
  }

  /**
   * Verifica se o usuário está autenticado
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('authToken');
  }

  /**
   * Inicializa super admin (apenas primeira vez)
   */
  async initSuperAdmin(): Promise<any> {
    return apiClient.post('/api/v1/auth/init-super-admin');
  }
}

export const authService = new AuthService();
```

### 3. Exemplo de Uso - Login Component (React)

```tsx
// src/components/Login.tsx
import React, { useState } from 'react';
import { authService } from '../services/authService';

export const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authService.login({ username, password });
      
      // Login bem-sucedido
      console.log('Login bem-sucedido:', response.user);
      
      // Redirecionar para dashboard
      window.location.href = '/dashboard';
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        'Erro ao fazer login. Verifique suas credenciais.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <h2>Login - CoinBalance</h2>
      
      {error && <div className="error">{error}</div>}
      
      <input
        type="text"
        placeholder="Usuário"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      
      <input
        type="password"
        placeholder="Senha"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      
      <button type="submit" disabled={loading}>
        {loading ? 'Entrando...' : 'Entrar'}
      </button>
    </form>
  );
};
```

### 4. Proteção de Rotas (React Router)

```tsx
// src/components/ProtectedRoute.tsx
import React from 'react';
import { Navigate } from 'react-router-dom';
import { authService } from '../services/authService';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  if (!authService.isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};
```

---

## 📦 Módulos da API

### 1. Módulo de Carteiras

```typescript
// src/services/walletService.ts
import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '../config/api';

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

export interface WalletOperationRequest {
  amount: number;
  reason: string;
}

export class WalletService {
  /**
   * Cria uma nova carteira
   */
  async createWallet(data: CreateWalletRequest): Promise<WalletResponse> {
    return apiClient.post<WalletResponse>(API_ENDPOINTS.WALLETS, data);
  }

  /**
   * Obtém informações de uma carteira
   */
  async getWallet(address: string): Promise<WalletResponse> {
    return apiClient.get<WalletResponse>(
      API_ENDPOINTS.WALLET_BY_ADDRESS(address)
    );
  }

  /**
   * Lista todas as carteiras
   */
  async listWallets(): Promise<{ wallets: WalletResponse[]; total: number }> {
    return apiClient.get(API_ENDPOINTS.WALLETS);
  }

  /**
   * Credita saldo em uma carteira
   */
  async creditWallet(
    address: string,
    data: WalletOperationRequest
  ): Promise<any> {
    return apiClient.post(API_ENDPOINTS.WALLET_CREDIT(address), data);
  }

  /**
   * Debita saldo de uma carteira
   */
  async debitWallet(
    address: string,
    data: WalletOperationRequest
  ): Promise<any> {
    return apiClient.post(API_ENDPOINTS.WALLET_DEBIT(address), data);
  }

  /**
   * Obtém saldo detalhado de uma carteira
   */
  async getWalletBalance(address: string): Promise<any> {
    return apiClient.get(`${API_ENDPOINTS.WALLETS}/${address}/balance`);
  }
}

export const walletService = new WalletService();
```

### 2. Módulo de Transações

```typescript
// src/services/transactionService.ts
import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '../config/api';

export interface CreateTransferRequest {
  from_address: string;
  to_address: string;
  amount: string | number;
  fee?: string | number;
  memo?: string;
  metadata?: Record<string, any>;
}

export interface TransactionResponse {
  id: string;
  from_address: string | null;
  to_address: string;
  amount_cnb: string;
  fee_cnb: string;
  transaction_type: string;
  status: string;
  created_at: number;
  confirmed_at: number | null;
  block_height: number | null;
  transaction_hash: string | null;
  memo: string | null;
  metadata: Record<string, any>;
}

export interface TransactionListParams {
  address?: string;
  limit?: number;
  offset?: number;
}

export class TransactionService {
  /**
   * Cria uma nova transferência
   */
  async createTransfer(
    data: CreateTransferRequest
  ): Promise<TransactionResponse> {
    return apiClient.post<TransactionResponse>(
      API_ENDPOINTS.TRANSACTIONS,
      data
    );
  }

  /**
   * Obtém histórico de transações
   */
  async getTransactionHistory(params?: TransactionListParams): Promise<{
    transactions: TransactionResponse[];
    total: number;
    limit: number;
    offset: number;
  }> {
    return apiClient.get(API_ENDPOINTS.TRANSACTION_HISTORY, { params });
  }

  /**
   * Obtém estatísticas de transações
   */
  async getTransactionStats(): Promise<any> {
    return apiClient.get(API_ENDPOINTS.TRANSACTION_STATS);
  }

  /**
   * Obtém detalhes de uma transação específica
   */
  async getTransaction(id: string): Promise<TransactionResponse> {
    return apiClient.get(`${API_ENDPOINTS.TRANSACTIONS}/${id}`);
  }
}

export const transactionService = new TransactionService();
```

### 3. Módulo de Blockchain

```typescript
// src/services/blockchainService.ts
import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '../config/api';

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

export interface BlockResponse {
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

export interface MineBlockRequest {
  miner_address: string;
  max_transactions?: number;
}

export class BlockchainService {
  /**
   * Obtém estatísticas da blockchain
   */
  async getStats(): Promise<BlockchainStats> {
    return apiClient.get<BlockchainStats>(API_ENDPOINTS.BLOCKCHAIN_STATS);
  }

  /**
   * Lista todos os blocos
   */
  async getBlocks(): Promise<BlockResponse[]> {
    return apiClient.get<BlockResponse[]>(API_ENDPOINTS.BLOCKCHAIN_BLOCKS);
  }

  /**
   * Obtém um bloco específico por altura
   */
  async getBlock(height: number): Promise<BlockResponse> {
    return apiClient.get<BlockResponse>(
      `${API_ENDPOINTS.BLOCKCHAIN_BLOCKS}/${height}`
    );
  }

  /**
   * Minera um novo bloco
   */
  async mineBlock(data: MineBlockRequest): Promise<BlockResponse> {
    return apiClient.post<BlockResponse>(API_ENDPOINTS.BLOCKCHAIN_MINE, data);
  }

  /**
   * Valida a blockchain
   */
  async validateChain(): Promise<{ valid: boolean; errors?: string[] }> {
    return apiClient.get('/api/v1/blockchain/validate');
  }
}

export const blockchainService = new BlockchainService();
```

### 4. Módulo de Monitoramento

```typescript
// src/services/monitoringService.ts
import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '../config/api';

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  environment: string;
  timestamp: number;
}

export interface MetricsResponse {
  timestamp: number;
  version: string;
  environment: string;
  system: {
    cpu_percent: number;
    memory_percent: number;
    memory_used_mb: number;
    memory_total_mb: number;
  };
  config: {
    debug: boolean;
    workers: number;
    rate_limit_enabled: boolean;
  };
}

export class MonitoringService {
  /**
   * Verifica saúde da API
   */
  async checkHealth(): Promise<HealthResponse> {
    return apiClient.get<HealthResponse>(API_ENDPOINTS.HEALTH);
  }

  /**
   * Obtém métricas do sistema
   */
  async getMetrics(): Promise<MetricsResponse> {
    return apiClient.get<MetricsResponse>(API_ENDPOINTS.METRICS);
  }

  /**
   * Obtém dashboard de monitoramento
   */
  async getDashboard(): Promise<any> {
    return apiClient.get('/api/v1/monitoring/dashboard');
  }
}

export const monitoringService = new MonitoringService();
```

---

## 💡 Exemplos de Integração

### 1. Dashboard de Carteira (React)

```tsx
// src/components/WalletDashboard.tsx
import React, { useEffect, useState } from 'react';
import { walletService, WalletResponse } from '../services/walletService';
import { transactionService, TransactionResponse } from '../services/transactionService';

export const WalletDashboard: React.FC = () => {
  const [wallets, setWallets] = useState<WalletResponse[]>([]);
  const [selectedWallet, setSelectedWallet] = useState<WalletResponse | null>(null);
  const [transactions, setTransactions] = useState<TransactionResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadWallets();
  }, []);

  useEffect(() => {
    if (selectedWallet) {
      loadTransactions(selectedWallet.address);
    }
  }, [selectedWallet]);

  const loadWallets = async () => {
    try {
      const response = await walletService.listWallets();
      setWallets(response.wallets);
      
      if (response.wallets.length > 0) {
        setSelectedWallet(response.wallets[0]);
      }
    } catch (error) {
      console.error('Erro ao carregar carteiras:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadTransactions = async (address: string) => {
    try {
      const response = await transactionService.getTransactionHistory({
        address,
        limit: 10,
      });
      setTransactions(response.transactions);
    } catch (error) {
      console.error('Erro ao carregar transações:', error);
    }
  };

  const handleCreateWallet = async () => {
    const name = prompt('Nome da carteira:');
    if (!name) return;

    try {
      const newWallet = await walletService.createWallet({ name });
      setWallets([...wallets, newWallet]);
      alert('Carteira criada com sucesso!');
    } catch (error) {
      alert('Erro ao criar carteira');
    }
  };

  if (loading) {
    return <div>Carregando...</div>;
  }

  return (
    <div className="wallet-dashboard">
      <h1>Minhas Carteiras</h1>
      
      <button onClick={handleCreateWallet}>+ Nova Carteira</button>

      <div className="wallets-list">
        {wallets.map((wallet) => (
          <div
            key={wallet.address}
            className={`wallet-card ${selectedWallet?.address === wallet.address ? 'active' : ''}`}
            onClick={() => setSelectedWallet(wallet)}
          >
            <h3>{wallet.name}</h3>
            <p>Saldo: {wallet.balance_cnb} CNB</p>
            <small>{wallet.address.substring(0, 20)}...</small>
          </div>
        ))}
      </div>

      {selectedWallet && (
        <div className="wallet-details">
          <h2>{selectedWallet.name}</h2>
          <div className="balance">
            <h3>{selectedWallet.balance_cnb} CNB</h3>
            <p>{selectedWallet.balance_satoshi} satoshis</p>
          </div>

          <h3>Transações Recentes</h3>
          <div className="transactions-list">
            {transactions.map((tx) => (
              <div key={tx.id} className="transaction-item">
                <div>
                  <strong>{tx.transaction_type}</strong>
                  <p>{tx.memo || 'Sem descrição'}</p>
                </div>
                <div>
                  <span className={tx.from_address === selectedWallet.address ? 'debit' : 'credit'}>
                    {tx.from_address === selectedWallet.address ? '-' : '+'}
                    {tx.amount_cnb} CNB
                  </span>
                  <small>{tx.status}</small>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
```

### 2. Formulário de Transferência

```tsx
// src/components/TransferForm.tsx
import React, { useState } from 'react';
import { transactionService, CreateTransferRequest } from '../services/transactionService';

interface TransferFormProps {
  fromAddress: string;
  onSuccess?: () => void;
}

export const TransferForm: React.FC<TransferFormProps> = ({ fromAddress, onSuccess }) => {
  const [formData, setFormData] = useState({
    to_address: '',
    amount: '',
    memo: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const transferData: CreateTransferRequest = {
        from_address: fromAddress,
        to_address: formData.to_address,
        amount: formData.amount,
        memo: formData.memo || undefined,
      };

      await transactionService.createTransfer(transferData);
      
      alert('Transferência realizada com sucesso!');
      
      // Limpar formulário
      setFormData({ to_address: '', amount: '', memo: '' });
      
      if (onSuccess) {
        onSuccess();
      }
    } catch (err: any) {
      setError(
        err.response?.data?.detail?.error || 
        'Erro ao realizar transferência'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="transfer-form">
      <h2>Nova Transferência</h2>

      {error && <div className="error">{error}</div>}

      <div className="form-group">
        <label>De:</label>
        <input type="text" value={fromAddress} disabled />
      </div>

      <div className="form-group">
        <label>Para:</label>
        <input
          type="text"
          placeholder="Endereço de destino"
          value={formData.to_address}
          onChange={(e) => setFormData({ ...formData, to_address: e.target.value })}
          required
        />
      </div>

      <div className="form-group">
        <label>Valor (CNB):</label>
        <input
          type="number"
          step="0.00000001"
          min="0"
          placeholder="0.00"
          value={formData.amount}
          onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
          required
        />
      </div>

      <div className="form-group">
        <label>Descrição (opcional):</label>
        <input
          type="text"
          placeholder="Descrição da transferência"
          value={formData.memo}
          onChange={(e) => setFormData({ ...formData, memo: e.target.value })}
        />
      </div>

      <button type="submit" disabled={loading}>
        {loading ? 'Enviando...' : 'Transferir'}
      </button>
    </form>
  );
};
```

### 3. Dashboard de Blockchain

```tsx
// src/components/BlockchainDashboard.tsx
import React, { useEffect, useState } from 'react';
import { blockchainService, BlockchainStats, BlockResponse } from '../services/blockchainService';

export const BlockchainDashboard: React.FC = () => {
  const [stats, setStats] = useState<BlockchainStats | null>(null);
  const [blocks, setBlocks] = useState<BlockResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    
    // Atualizar a cada 30 segundos
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const [statsData, blocksData] = await Promise.all([
        blockchainService.getStats(),
        blockchainService.getBlocks(),
      ]);
      
      setStats(statsData);
      setBlocks(blocksData.slice(-10)); // Últimos 10 blocos
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !stats) {
    return <div>Carregando...</div>;
  }

  return (
    <div className="blockchain-dashboard">
      <h1>Blockchain CoinBalance</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total de Blocos</h3>
          <p className="stat-value">{stats.total_blocks}</p>
        </div>

        <div className="stat-card">
          <h3>Total de Transações</h3>
          <p className="stat-value">{stats.total_transactions}</p>
        </div>

        <div className="stat-card">
          <h3>Dificuldade Atual</h3>
          <p className="stat-value">{stats.current_difficulty}</p>
        </div>

        <div className="stat-card">
          <h3>Supply Total</h3>
          <p className="stat-value">{stats.total_supply.toFixed(2)} CNB</p>
        </div>

        <div className="stat-card">
          <h3>Recompensa por Bloco</h3>
          <p className="stat-value">{stats.current_block_reward} CNB</p>
        </div>

        <div className="stat-card">
          <h3>Tempo Médio de Bloco</h3>
          <p className="stat-value">{stats.average_block_time.toFixed(2)}s</p>
        </div>
      </div>

      <h2>Blocos Recentes</h2>
      <div className="blocks-list">
        {blocks.map((block) => (
          <div key={block.height} className="block-card">
            <div className="block-header">
              <h3>Bloco #{block.height}</h3>
              <span className="block-time">
                {new Date(block.timestamp * 1000).toLocaleString()}
              </span>
            </div>
            <div className="block-details">
              <p><strong>Hash:</strong> {block.hash.substring(0, 20)}...</p>
              <p><strong>Transações:</strong> {block.transactions_count}</p>
              <p><strong>Tempo de Mineração:</strong> {block.mining_time.toFixed(2)}s</p>
              <p><strong>Recompensa:</strong> {block.block_reward} CNB</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

---

## ⚠️ Tratamento de Erros

### 1. Códigos de Status HTTP

| Código | Significado | Descrição |
|--------|-------------|-----------|
| 200 | OK | Requisição bem-sucedida |
| 201 | Created | Recurso criado com sucesso |
| 400 | Bad Request | Dados inválidos ou faltando |
| 401 | Unauthorized | Token inválido ou ausente |
| 403 | Forbidden | Sem permissão para acessar |
| 404 | Not Found | Recurso não encontrado |
| 409 | Conflict | Conflito (ex: carteira já existe) |
| 422 | Unprocessable Entity | Validação falhou |
| 429 | Too Many Requests | Rate limit excedido |
| 500 | Internal Server Error | Erro interno do servidor |

### 2. Formato de Erro Padrão

```typescript
interface ApiError {
  detail: {
    error: string;
    code: string;
    message?: string;
  };
}
```

### 3. Tratamento de Erros Centralizado

```typescript
// src/utils/errorHandler.ts
export class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export const handleApiError = (error: any): ApiError => {
  if (error.response) {
    // Erro da API
    const status = error.response.status;
    const detail = error.response.data?.detail;
    
    if (typeof detail === 'object' && detail.error) {
      return new ApiError(status, detail.code || 'UNKNOWN', detail.error);
    } else if (typeof detail === 'string') {
      return new ApiError(status, 'UNKNOWN', detail);
    }
    
    return new ApiError(status, 'UNKNOWN', 'Erro desconhecido');
  } else if (error.request) {
    // Sem resposta do servidor
    return new ApiError(0, 'NETWORK_ERROR', 'Erro de conexão com o servidor');
  } else {
    // Erro na configuração da requisição
    return new ApiError(0, 'REQUEST_ERROR', error.message);
  }
};

export const getErrorMessage = (error: any): string => {
  const apiError = handleApiError(error);
  
  switch (apiError.code) {
    case 'WALLET_NOT_FOUND':
      return 'Carteira não encontrada';
    case 'INSUFFICIENT_BALANCE':
      return 'Saldo insuficiente';
    case 'INVALID_ADDRESS':
      return 'Endereço inválido';
    case 'DUPLICATE_WALLET':
      return 'Carteira já existe';
    case 'NETWORK_ERROR':
      return 'Erro de conexão. Verifique sua internet.';
    default:
      return apiError.message;
  }
};
```

### 4. Hook para Tratamento de Erros (React)

```typescript
// src/hooks/useApiError.ts
import { useState, useCallback } from 'react';
import { getErrorMessage } from '../utils/errorHandler';

export const useApiError = () => {
  const [error, setError] = useState<string | null>(null);

  const handleError = useCallback((err: any) => {
    const message = getErrorMessage(err);
    setError(message);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return { error, handleError, clearError };
};
```

---

## ✨ Boas Práticas

### 1. Segurança

```typescript
// ✅ BOM: Token no header Authorization
apiClient.setToken(token);
const wallet = await walletService.getWallet(address);

// ❌ RUIM: Token na URL
const wallet = await fetch(`/api/wallets?token=${token}`);
```

### 2. Performance

```typescript
// ✅ BOM: Carregar dados em paralelo
const [wallets, transactions, stats] = await Promise.all([
  walletService.listWallets(),
  transactionService.getTransactionHistory(),
  blockchainService.getStats(),
]);

// ❌ RUIM: Carregar dados sequencialmente
const wallets = await walletService.listWallets();
const transactions = await transactionService.getTransactionHistory();
const stats = await blockchainService.getStats();
```

### 3. Paginação

```typescript
// ✅ BOM: Usar paginação para listas grandes
const transactions = await transactionService.getTransactionHistory({
  limit: 50,
  offset: page * 50,
});

// ❌ RUIM: Carregar todos os dados de uma vez
const transactions = await transactionService.getTransactionHistory();
```

### 4. Cache de Dados

```typescript
// src/hooks/useWalletCache.ts
import { useState, useEffect, useRef } from 'react';
import { walletService, WalletResponse } from '../services/walletService';

export const useWalletCache = (address: string, cacheTime: number = 60000) => {
  const [wallet, setWallet] = useState<WalletResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const cacheRef = useRef<{ data: WalletResponse; timestamp: number } | null>(null);

  useEffect(() => {
    const loadWallet = async () => {
      // Verificar cache
      if (cacheRef.current && Date.now() - cacheRef.current.timestamp < cacheTime) {
        setWallet(cacheRef.current.data);
        setLoading(false);
        return;
      }

      // Carregar do servidor
      try {
        const data = await walletService.getWallet(address);
        setWallet(data);
        cacheRef.current = { data, timestamp: Date.now() };
      } catch (error) {
        console.error('Erro ao carregar carteira:', error);
      } finally {
        setLoading(false);
      }
    };

    loadWallet();
  }, [address, cacheTime]);

  return { wallet, loading };
};
```

### 5. Retry Logic

```typescript
// src/utils/retry.ts
export async function retryRequest<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error: any) {
      // Não fazer retry em erros 4xx (exceto 429)
      if (error.response?.status >= 400 && error.response?.status < 500 && error.response?.status !== 429) {
        throw error;
      }

      if (i === maxRetries - 1) {
        throw error;
      }

      // Aguardar antes de tentar novamente (exponential backoff)
      await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, i)));
    }
  }

  throw new Error('Max retries exceeded');
}
```

### 6. WebSocket para Updates em Tempo Real (Se disponível)

```typescript
// src/services/websocketService.ts
export class WebSocketService {
  private ws: WebSocket | null = null;
  private listeners: Map<string, Set<(data: any) => void>> = new Map();

  connect(url: string): void {
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      console.log('WebSocket conectado');
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const listeners = this.listeners.get(data.type);
      
      if (listeners) {
        listeners.forEach(listener => listener(data));
      }
    };

    this.ws.onerror = (error) => {
      console.error('Erro no WebSocket:', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket desconectado');
      // Reconectar após 5 segundos
      setTimeout(() => this.connect(url), 5000);
    };
  }

  on(event: string, callback: (data: any) => void): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);
  }

  off(event: string, callback: (data: any) => void): void {
    const listeners = this.listeners.get(event);
    if (listeners) {
      listeners.delete(callback);
    }
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

export const wsService = new WebSocketService();
```

---

## 🛠️ SDK JavaScript/TypeScript

### SDK Completo (Opcional)

Para facilitar ainda mais a integração, você pode criar um SDK completo:

```typescript
// src/sdk/coinbalance-sdk.ts
import { apiClient } from '../services/apiClient';
import { authService } from '../services/authService';
import { walletService } from '../services/walletService';
import { transactionService } from '../services/transactionService';
import { blockchainService } from '../services/blockchainService';
import { monitoringService } from '../services/monitoringService';

export class CoinBalanceSDK {
  public auth = authService;
  public wallets = walletService;
  public transactions = transactionService;
  public blockchain = blockchainService;
  public monitoring = monitoringService;

  constructor(baseURL?: string, token?: string) {
    if (baseURL) {
      // Configurar URL base personalizada
    }
    
    if (token) {
      apiClient.setToken(token);
    } else {
      // Tentar carregar token do localStorage
      apiClient.loadToken();
    }
  }

  /**
   * Configura o token de autenticação
   */
  setToken(token: string): void {
    apiClient.setToken(token);
  }

  /**
   * Remove o token de autenticação
   */
  clearToken(): void {
    apiClient.clearToken();
  }
}

// Exportar instância singleton
export const coinbalance = new CoinBalanceSDK();

// Uso:
// import { coinbalance } from './sdk/coinbalance-sdk';
// await coinbalance.auth.login({ username: 'admin', password: 'admin123' });
// const wallets = await coinbalance.wallets.listWallets();
```

---

## 🧪 Testes e Debugging

### 1. Testes Unitários (Jest)

```typescript
// src/services/__tests__/walletService.test.ts
import { walletService } from '../walletService';
import { apiClient } from '../apiClient';

jest.mock('../apiClient');

describe('WalletService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('deve criar uma carteira', async () => {
    const mockWallet = {
      address: 'abc123',
      name: 'Test Wallet',
      public_key: 'pub123',
      balance_cnb: 0,
      balance_satoshi: 0,
      created_at: Date.now(),
      updated_at: Date.now(),
      is_active: true,
      metadata: {},
    };

    (apiClient.post as jest.Mock).mockResolvedValue(mockWallet);

    const result = await walletService.createWallet({ name: 'Test Wallet' });

    expect(result).toEqual(mockWallet);
    expect(apiClient.post).toHaveBeenCalledWith(
      '/api/v1/carteiras',
      { name: 'Test Wallet' }
    );
  });

  it('deve listar carteiras', async () => {
    const mockResponse = {
      wallets: [],
      total: 0,
    };

    (apiClient.get as jest.Mock).mockResolvedValue(mockResponse);

    const result = await walletService.listWallets();

    expect(result).toEqual(mockResponse);
    expect(apiClient.get).toHaveBeenCalledWith('/api/v1/carteiras');
  });
});
```

### 2. Debug Mode

```typescript
// src/config/api.ts
export const API_CONFIG = {
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
};

// Habilitar logs de debug em desenvolvimento
if (process.env.NODE_ENV === 'development') {
  const originalPost = apiClient.post;
  apiClient.post = async function(...args: any[]) {
    console.log('[API POST]', args[0], args[1]);
    const result = await originalPost.apply(this, args);
    console.log('[API RESPONSE]', result);
    return result;
  };
}
```

### 3. Ferramentas de Debug

- **Postman/Insomnia**: Para testar endpoints manualmente
- **Swagger UI**: `http://localhost:8000/docs` - Interface interativa
- **Browser DevTools**: Network tab para inspecionar requisições
- **React DevTools**: Para debug de componentes React

---

## 📚 Referência Completa de Endpoints

### Autenticação (`/api/v1/auth`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/login` | Login do usuário | Não |
| POST | `/logout` | Logout do usuário | Sim |
| GET | `/me` | Informações do usuário atual | Sim |
| POST | `/users` | Criar novo usuário | Sim (users:create) |
| GET | `/users` | Listar usuários | Sim (users:view) |
| POST | `/change-password` | Alterar senha | Sim |
| GET | `/audit-logs` | Logs de auditoria | Sim (audit:logs) |
| POST | `/init-super-admin` | Inicializar super admin | Não |

### Carteiras (`/api/v1/carteiras`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/` | Criar carteira | Sim |
| GET | `/` | Listar carteiras | Sim |
| GET | `/{address}` | Obter carteira | Sim |
| POST | `/{address}/creditar` | Creditar saldo | Sim |
| POST | `/{address}/debitar` | Debitar saldo | Sim |
| GET | `/{address}/balance` | Saldo detalhado | Sim |

### Transações (`/api/v1/transferencias`, `/api/v1/transacoes`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/transferencias/` | Criar transferência | Sim |
| GET | `/transacoes/historico` | Histórico de transações | Sim |
| GET | `/transacoes/stats` | Estatísticas | Sim |
| GET | `/transacoes/{id}` | Detalhes da transação | Sim |

### Blockchain (`/api/v1/blockchain`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/stats` | Estatísticas da blockchain | Não |
| GET | `/blocks` | Listar blocos | Não |
| GET | `/blocks/{height}` | Obter bloco | Não |
| POST | `/mine` | Minerar bloco | Sim |
| GET | `/validate` | Validar blockchain | Não |

### Monitoramento (`/api/v1`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/health` | Health check | Não |
| GET | `/health/live` | Liveness probe | Não |
| GET | `/health/ready` | Readiness probe | Não |
| GET | `/metrics` | Métricas do sistema | Não |
| GET | `/info` | Informações da API | Não |
| GET | `/monitoring/dashboard` | Dashboard | Sim |

### Web3 (`/api/v1/web3`, `/api/v1/web3-advanced`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/web3/balance` | Saldo de token | Sim |
| GET | `/web3/nft` | Informações de NFT | Sim |
| POST | `/web3-advanced/connect-network` | Conectar rede | Sim |
| GET | `/web3-advanced/token-balance` | Saldo de token ERC20 | Sim |

### IA (`/api/v1/ai-advanced`, `/api/v1/ai-crypto`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/ai-advanced/train-model` | Treinar modelo | Sim |
| POST | `/ai-advanced/predict` | Fazer predição | Sim |
| POST | `/ai-crypto/create` | Criar criptomoeda | Sim |

---

## 🎓 Conclusão

Este manual fornece uma base sólida para integrar sua aplicação front-end com a API do CoinBalance. Para mais informações:

- **Documentação Interativa**: http://localhost:8000/docs
- **Código-fonte**: GitHub do projeto
- **Suporte**: Issues no GitHub ou Discord

### Próximos Passos

1. Configurar ambiente de desenvolvimento
2. Implementar sistema de autenticação
3. Criar componentes de carteira
4. Adicionar funcionalidade de transferências
5. Implementar dashboard de blockchain
6. Adicionar testes automatizados

### Recursos Adicionais

- TypeScript para type safety
- React Query para gerenciamento de estado de servidor
- Zod para validação de dados
- TanStack Table para tabelas de dados
- Chart.js para gráficos e visualizações

---

**Desenvolvido com ❤️ pela equipe CoinBalance**

**Versão do Manual**: 1.0.0  
**Última Atualização**: 2025-10-28
