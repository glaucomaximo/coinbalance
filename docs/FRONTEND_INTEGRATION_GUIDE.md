# 🎨 Guia de Integração Frontend Web3 - CoinBalance

## 🌐 Visão Geral

Este guia fornece exemplos práticos para integrar as funcionalidades Web3 do CoinBalance em aplicações frontend (React, Vue, Angular, etc.).

## 🔧 Configuração Inicial

### Instalação de Dependências

```bash
# React
npm install axios @walletconnect/web3-provider ethers

# Vue
npm install axios @walletconnect/web3-provider ethers vue-composition-api

# Angular
npm install axios @walletconnect/web3-provider ethers
```

### Configuração Base

```javascript
// config/web3.js
const WEB3_CONFIG = {
  apiBaseUrl: 'https://api.coinbalance.com/api/v1',
  web3ProviderUrl: 'https://mainnet.infura.io/v3/YOUR_PROJECT_ID',
  walletConnectBridge: 'https://bridge.walletconnect.org',
  supportedChains: {
    ethereum: 1,
    polygon: 137,
    bsc: 56,
    avalanche: 43114
  }
};

export default WEB3_CONFIG;
```

## 🔐 Autenticação

### Serviço de Autenticação

```javascript
// services/auth.js
import axios from 'axios';
import WEB3_CONFIG from '../config/web3';

class AuthService {
  constructor() {
    this.api = axios.create({
      baseURL: WEB3_CONFIG.apiBaseUrl,
      timeout: 10000
    });
    
    // Interceptor para adicionar token
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('jwt_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  async login(username, password) {
    try {
      const response = await this.api.post('/auth/login', {
        username,
        password
      });
      
      const { access_token } = response.data;
      localStorage.setItem('jwt_token', access_token);
      
      return { success: true, token: access_token };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  }

  async logout() {
    try {
      await this.api.post('/auth/logout');
      localStorage.removeItem('jwt_token');
      return { success: true };
    } catch (error) {
      localStorage.removeItem('jwt_token');
      return { success: true }; // Logout local mesmo com erro
    }
  }

  isAuthenticated() {
    return !!localStorage.getItem('jwt_token');
  }
}

export default new AuthService();
```

## 🎨 NFT Marketplace

### Serviço NFT

```javascript
// services/nft.js
import axios from 'axios';
import WEB3_CONFIG from '../config/web3';

class NFTService {
  constructor() {
    this.api = axios.create({
      baseURL: WEB3_CONFIG.apiBaseUrl,
      timeout: 30000
    });
    
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('jwt_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  async createNFT(nftData) {
    try {
      const response = await this.api.post('/web3/nft/create', {
        contract_address: nftData.contractAddress,
        token_id: nftData.tokenId,
        owner: nftData.owner,
        creator: nftData.creator,
        name: nftData.name,
        description: nftData.description,
        image_url: nftData.imageUrl
      });
      
      return { success: true, nft: response.data.nft };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to create NFT' };
    }
  }

  async listNFT(listingData) {
    try {
      const response = await this.api.post('/web3/nft/list', {
        nft_key: listingData.nftKey,
        seller: listingData.seller,
        listing_type: listingData.listingType,
        price: listingData.price,
        currency: listingData.currency || 'CNB'
      });
      
      return { success: true, listing: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to list NFT' };
    }
  }

  async buyNFT(listingId, amount) {
    try {
      const response = await this.api.post('/web3/nft/buy', {
        listing_id: listingId,
        amount: amount
      });
      
      return { success: true, transaction: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to buy NFT' };
    }
  }

  async searchNFTs(query, filters = {}) {
    try {
      const params = new URLSearchParams({ query, ...filters });
      const response = await this.api.get(`/web3/nft/search?${params}`);
      
      return { success: true, nfts: response.data.nfts };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to search NFTs' };
    }
  }

  async getTrendingNFTs(limit = 10) {
    try {
      const response = await this.api.get(`/web3/nft/trending?limit=${limit}`);
      
      return { success: true, nfts: response.data.nfts };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to get trending NFTs' };
    }
  }
}

export default new NFTService();
```

### Componente React NFT

```jsx
// components/NFTMarketplace.jsx
import React, { useState, useEffect } from 'react';
import NFTService from '../services/nft';

const NFTMarketplace = () => {
  const [nfts, setNfts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadTrendingNFTs();
  }, []);

  const loadTrendingNFTs = async () => {
    setLoading(true);
    const result = await NFTService.getTrendingNFTs();
    
    if (result.success) {
      setNfts(result.nfts);
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  const handleCreateNFT = async (nftData) => {
    setLoading(true);
    const result = await NFTService.createNFT(nftData);
    
    if (result.success) {
      // Atualizar lista de NFTs
      loadTrendingNFTs();
      alert('NFT criado com sucesso!');
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  const handleBuyNFT = async (listingId, price) => {
    if (!window.confirm(`Confirmar compra por ${price} CNB?`)) return;
    
    setLoading(true);
    const result = await NFTService.buyNFT(listingId, price);
    
    if (result.success) {
      alert('NFT comprado com sucesso!');
      loadTrendingNFTs();
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  if (loading) return <div>Carregando...</div>;
  if (error) return <div>Erro: {error}</div>;

  return (
    <div className="nft-marketplace">
      <h2>🎨 NFT Marketplace</h2>
      
      <div className="nft-grid">
        {nfts.map(nft => (
          <div key={nft.token_id} className="nft-card">
            <img src={nft.image} alt={nft.name} />
            <h3>{nft.name}</h3>
            <p>{nft.description}</p>
            <div className="nft-price">
              <span>{nft.floor_price} CNB</span>
              <button onClick={() => handleBuyNFT(nft.listing_id, nft.floor_price)}>
                Comprar
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NFTMarketplace;
```

## 🏛️ DAO Governance

### Serviço DAO

```javascript
// services/dao.js
import axios from 'axios';
import WEB3_CONFIG from '../config/web3';

class DAOService {
  constructor() {
    this.api = axios.create({
      baseURL: WEB3_CONFIG.apiBaseUrl,
      timeout: 30000
    });
    
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('jwt_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  async createProposal(proposalData) {
    try {
      const response = await this.api.post('/web3/dao/proposal', {
        proposer: proposalData.proposer,
        title: proposalData.title,
        description: proposalData.description,
        proposal_type: proposalData.type,
        targets: proposalData.targets,
        values: proposalData.values,
        calldatas: proposalData.calldatas
      });
      
      return { success: true, proposal: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to create proposal' };
    }
  }

  async castVote(voteData) {
    try {
      const response = await this.api.post('/web3/dao/vote', {
        voter: voteData.voter,
        proposal_id: voteData.proposalId,
        vote_type: voteData.voteType,
        reason: voteData.reason
      });
      
      return { success: true, vote: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to cast vote' };
    }
  }

  async getProposal(proposalId) {
    try {
      const response = await this.api.get(`/web3/dao/proposal/${proposalId}`);
      
      return { success: true, proposal: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to get proposal' };
    }
  }

  async getTreasuryBalance() {
    try {
      const response = await this.api.get('/web3/dao/treasury');
      
      return { success: true, treasury: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to get treasury' };
    }
  }
}

export default new DAOService();
```

### Componente React DAO

```jsx
// components/DAOGovernance.jsx
import React, { useState, useEffect } from 'react';
import DAOService from '../services/dao';

const DAOGovernance = () => {
  const [proposals, setProposals] = useState([]);
  const [treasury, setTreasury] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadTreasury();
  }, []);

  const loadTreasury = async () => {
    const result = await DAOService.getTreasuryBalance();
    if (result.success) {
      setTreasury(result.treasury);
    }
  };

  const handleCreateProposal = async (proposalData) => {
    setLoading(true);
    const result = await DAOService.createProposal(proposalData);
    
    if (result.success) {
      alert('Proposta criada com sucesso!');
      // Recarregar propostas
    } else {
      alert(`Erro: ${result.error}`);
    }
    setLoading(false);
  };

  const handleVote = async (proposalId, voteType) => {
    const result = await DAOService.castVote({
      voter: '0xabcd...', // Endereço do usuário
      proposalId,
      voteType,
      reason: 'Concordo com a proposta'
    });
    
    if (result.success) {
      alert('Voto registrado com sucesso!');
    } else {
      alert(`Erro: ${result.error}`);
    }
  };

  return (
    <div className="dao-governance">
      <h2>🏛️ DAO Governance</h2>
      
      {treasury && (
        <div className="treasury-info">
          <h3>Tesouro DAO</h3>
          <p>Saldo: {treasury.CNB} CNB</p>
        </div>
      )}
      
      <div className="proposals">
        <h3>Propostas Ativas</h3>
        {proposals.map(proposal => (
          <div key={proposal.id} className="proposal-card">
            <h4>{proposal.title}</h4>
            <p>{proposal.description}</p>
            <div className="proposal-votes">
              <span>Votos a favor: {proposal.for_votes}</span>
              <span>Votos contra: {proposal.against_votes}</span>
            </div>
            <div className="proposal-actions">
              <button onClick={() => handleVote(proposal.id, 'for')}>
                Votar a Favor
              </button>
              <button onClick={() => handleVote(proposal.id, 'against')}>
                Votar Contra
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DAOGovernance;
```

## 🌉 Cross-Chain Bridge

### Serviço Bridge

```javascript
// services/bridge.js
import axios from 'axios';
import WEB3_CONFIG from '../config/web3';

class BridgeService {
  constructor() {
    this.api = axios.create({
      baseURL: WEB3_CONFIG.apiBaseUrl,
      timeout: 60000
    });
    
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('jwt_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  async initiateBridge(bridgeData) {
    try {
      const response = await this.api.post('/web3/bridge/initiate', {
        source_chain: bridgeData.sourceChain,
        target_chain: bridgeData.targetChain,
        sender: bridgeData.sender,
        receiver: bridgeData.receiver,
        token: bridgeData.token,
        amount: bridgeData.amount
      });
      
      return { success: true, transaction: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to initiate bridge' };
    }
  }

  async getBridgeStatus(txId) {
    try {
      const response = await this.api.get(`/web3/bridge/status/${txId}`);
      
      return { success: true, status: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to get bridge status' };
    }
  }

  async getBridgeFees(token, amount) {
    try {
      const response = await this.api.get(`/web3/bridge/fees?token=${token}&amount=${amount}`);
      
      return { success: true, fees: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to get bridge fees' };
    }
  }

  async getSupportedTokens(chain) {
    try {
      const response = await this.api.get(`/web3/bridge/supported-tokens?chain=${chain}`);
      
      return { success: true, tokens: response.data.tokens };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to get supported tokens' };
    }
  }
}

export default new BridgeService();
```

### Componente React Bridge

```jsx
// components/CrossChainBridge.jsx
import React, { useState, useEffect } from 'react';
import BridgeService from '../services/bridge';
import WEB3_CONFIG from '../config/web3';

const CrossChainBridge = () => {
  const [bridgeData, setBridgeData] = useState({
    sourceChain: 'ethereum',
    targetChain: 'polygon',
    token: 'CNB',
    amount: ''
  });
  const [fees, setFees] = useState(null);
  const [bridgeStatus, setBridgeStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (bridgeData.token && bridgeData.amount) {
      loadFees();
    }
  }, [bridgeData.token, bridgeData.amount]);

  const loadFees = async () => {
    const result = await BridgeService.getBridgeFees(bridgeData.token, bridgeData.amount);
    if (result.success) {
      setFees(result.fees);
    }
  };

  const handleBridge = async () => {
    if (!bridgeData.amount || !fees) return;
    
    setLoading(true);
    const result = await BridgeService.initiateBridge({
      ...bridgeData,
      sender: '0xabcd...', // Endereço do usuário
      receiver: '0xabcd...' // Mesmo endereço
    });
    
    if (result.success) {
      setBridgeStatus(result.status);
      alert('Bridge iniciado com sucesso!');
    } else {
      alert(`Erro: ${result.error}`);
    }
    setLoading(false);
  };

  const checkBridgeStatus = async (txId) => {
    const result = await BridgeService.getBridgeStatus(txId);
    if (result.success) {
      setBridgeStatus(result.status);
    }
  };

  return (
    <div className="cross-chain-bridge">
      <h2>🌉 Cross-Chain Bridge</h2>
      
      <div className="bridge-form">
        <div className="form-group">
          <label>Chain de Origem:</label>
          <select 
            value={bridgeData.sourceChain}
            onChange={(e) => setBridgeData({...bridgeData, sourceChain: e.target.value})}
          >
            <option value="ethereum">Ethereum</option>
            <option value="polygon">Polygon</option>
            <option value="bsc">BSC</option>
            <option value="avalanche">Avalanche</option>
          </select>
        </div>
        
        <div className="form-group">
          <label>Chain de Destino:</label>
          <select 
            value={bridgeData.targetChain}
            onChange={(e) => setBridgeData({...bridgeData, targetChain: e.target.value})}
          >
            <option value="ethereum">Ethereum</option>
            <option value="polygon">Polygon</option>
            <option value="bsc">BSC</option>
            <option value="avalanche">Avalanche</option>
          </select>
        </div>
        
        <div className="form-group">
          <label>Token:</label>
          <select 
            value={bridgeData.token}
            onChange={(e) => setBridgeData({...bridgeData, token: e.target.value})}
          >
            <option value="CNB">CNB</option>
            <option value="USDC">USDC</option>
          </select>
        </div>
        
        <div className="form-group">
          <label>Quantidade:</label>
          <input 
            type="number"
            value={bridgeData.amount}
            onChange={(e) => setBridgeData({...bridgeData, amount: e.target.value})}
            placeholder="Digite a quantidade"
          />
        </div>
        
        {fees && (
          <div className="fees-info">
            <p>Taxa: {fees.fee_amount} {bridgeData.token}</p>
            <p>Valor após taxa: {fees.amount_after_fee} {bridgeData.token}</p>
          </div>
        )}
        
        <button 
          onClick={handleBridge}
          disabled={loading || !bridgeData.amount}
        >
          {loading ? 'Processando...' : 'Iniciar Bridge'}
        </button>
      </div>
      
      {bridgeStatus && (
        <div className="bridge-status">
          <h3>Status do Bridge</h3>
          <p>Status: {bridgeStatus.status}</p>
          <p>TX ID: {bridgeStatus.tx_id}</p>
          <p>Taxa: {bridgeStatus.fee} {bridgeData.token}</p>
        </div>
      )}
    </div>
  );
};

export default CrossChainBridge;
```

## 📊 Web3 Analytics

### Serviço Analytics

```javascript
// services/analytics.js
import axios from 'axios';
import WEB3_CONFIG from '../config/web3';

class AnalyticsService {
  constructor() {
    this.api = axios.create({
      baseURL: WEB3_CONFIG.apiBaseUrl,
      timeout: 30000
    });
    
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('jwt_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  async getPriceChart(token, timeRange = '24h') {
    try {
      const response = await this.api.get(`/web3/analytics/price/${token}?time_range=${timeRange}`);
      
      return { success: true, chart: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to get price chart' };
    }
  }

  async getMarketOverview() {
    try {
      const response = await this.api.get('/web3/analytics/market-overview');
      
      return { success: true, overview: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to get market overview' };
    }
  }

  async getUserAnalytics(userAddress) {
    try {
      const response = await this.api.get(`/web3/analytics/user/${userAddress}`);
      
      return { success: true, analytics: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to get user analytics' };
    }
  }

  async generateReport(metricType, timeRange, title) {
    try {
      const response = await this.api.post('/web3/analytics/report', {
        metric_type: metricType,
        time_range: timeRange,
        title: title
      });
      
      return { success: true, report: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to generate report' };
    }
  }
}

export default new AnalyticsService();
```

### Componente React Analytics

```jsx
// components/Web3Analytics.jsx
import React, { useState, useEffect } from 'react';
import AnalyticsService from '../services/analytics';

const Web3Analytics = () => {
  const [marketOverview, setMarketOverview] = useState(null);
  const [priceChart, setPriceChart] = useState(null);
  const [userAnalytics, setUserAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadMarketOverview();
    loadPriceChart();
  }, []);

  const loadMarketOverview = async () => {
    const result = await AnalyticsService.getMarketOverview();
    if (result.success) {
      setMarketOverview(result.overview);
    }
  };

  const loadPriceChart = async () => {
    const result = await AnalyticsService.getPriceChart('CNB', '24h');
    if (result.success) {
      setPriceChart(result.chart);
    }
  };

  const loadUserAnalytics = async (userAddress) => {
    setLoading(true);
    const result = await AnalyticsService.getUserAnalytics(userAddress);
    
    if (result.success) {
      setUserAnalytics(result.analytics);
    }
    setLoading(false);
  };

  return (
    <div className="web3-analytics">
      <h2>📊 Web3 Analytics</h2>
      
      {marketOverview && (
        <div className="market-overview">
          <h3>Visão Geral do Mercado</h3>
          <div className="overview-stats">
            <div className="stat">
              <span>Total de Usuários:</span>
              <span>{marketOverview.total_users}</span>
            </div>
            <div className="stat">
              <span>Total de Transações:</span>
              <span>{marketOverview.total_transactions}</span>
            </div>
            <div className="stat">
              <span>Volume Total:</span>
              <span>{marketOverview.total_volume} CNB</span>
            </div>
          </div>
        </div>
      )}
      
      {priceChart && (
        <div className="price-chart">
          <h3>Gráfico de Preços - CNB</h3>
          <div className="chart-info">
            <p>Preço Atual: {priceChart.current_price} CNB</p>
            <p>Mudança 24h: {priceChart.price_change_percentage}%</p>
            <p>Volume 24h: {priceChart.volume_24h} CNB</p>
          </div>
        </div>
      )}
      
      <div className="user-analytics">
        <h3>Analytics do Usuário</h3>
        <input 
          type="text"
          placeholder="Digite o endereço do usuário"
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              loadUserAnalytics(e.target.value);
            }
          }}
        />
        
        {userAnalytics && (
          <div className="user-stats">
            <p>Total de Transações: {userAnalytics.total_transactions}</p>
            <p>Volume Total: {userAnalytics.total_volume} CNB</p>
            <p>Primeira Atividade: {new Date(userAnalytics.first_activity * 1000).toLocaleDateString()}</p>
            <p>Última Atividade: {new Date(userAnalytics.last_activity * 1000).toLocaleDateString()}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Web3Analytics;
```

## 🔗 Wallet Connect

### Configuração Wallet Connect

```javascript
// services/walletConnect.js
import WalletConnect from '@walletconnect/web3-provider';

class WalletConnectService {
  constructor() {
    this.provider = null;
    this.connector = null;
  }

  async connect() {
    try {
      this.provider = new WalletConnect({
        rpc: {
          1: 'https://mainnet.infura.io/v3/YOUR_PROJECT_ID',
          137: 'https://polygon-rpc.com',
          56: 'https://bsc-dataseed.binance.org',
          43114: 'https://api.avax.network/ext/bc/C/rpc'
        }
      });

      // Conectar
      await this.provider.enable();
      
      return { success: true, provider: this.provider };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  async disconnect() {
    try {
      if (this.provider) {
        await this.provider.disconnect();
        this.provider = null;
      }
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  getAccount() {
    if (this.provider && this.provider.accounts) {
      return this.provider.accounts[0];
    }
    return null;
  }

  getChainId() {
    if (this.provider && this.provider.chainId) {
      return this.provider.chainId;
    }
    return null;
  }
}

export default new WalletConnectService();
```

## 🎯 Exemplo de Aplicação Completa

### App Principal

```jsx
// App.jsx
import React, { useState, useEffect } from 'react';
import AuthService from './services/auth';
import NFTMarketplace from './components/NFTMarketplace';
import DAOGovernance from './components/DAOGovernance';
import CrossChainBridge from './components/CrossChainBridge';
import Web3Analytics from './components/Web3Analytics';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('nft');

  useEffect(() => {
    setIsAuthenticated(AuthService.isAuthenticated());
  }, []);

  const handleLogin = async (username, password) => {
    const result = await AuthService.login(username, password);
    if (result.success) {
      setIsAuthenticated(true);
      setUser({ username });
    } else {
      alert(`Erro no login: ${result.error}`);
    }
  };

  const handleLogout = async () => {
    await AuthService.logout();
    setIsAuthenticated(false);
    setUser(null);
  };

  if (!isAuthenticated) {
    return (
      <div className="login-page">
        <h1>🌐 CoinBalance Web3</h1>
        <LoginForm onLogin={handleLogin} />
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌐 CoinBalance Web3</h1>
        <div className="user-info">
          <span>Bem-vindo, {user?.username}</span>
          <button onClick={handleLogout}>Sair</button>
        </div>
      </header>
      
      <nav className="app-nav">
        <button 
          className={activeTab === 'nft' ? 'active' : ''}
          onClick={() => setActiveTab('nft')}
        >
          🎨 NFT Marketplace
        </button>
        <button 
          className={activeTab === 'dao' ? 'active' : ''}
          onClick={() => setActiveTab('dao')}
        >
          🏛️ DAO Governance
        </button>
        <button 
          className={activeTab === 'bridge' ? 'active' : ''}
          onClick={() => setActiveTab('bridge')}
        >
          🌉 Cross-Chain Bridge
        </button>
        <button 
          className={activeTab === 'analytics' ? 'active' : ''}
          onClick={() => setActiveTab('analytics')}
        >
          📊 Analytics
        </button>
      </nav>
      
      <main className="app-main">
        {activeTab === 'nft' && <NFTMarketplace />}
        {activeTab === 'dao' && <DAOGovernance />}
        {activeTab === 'bridge' && <CrossChainBridge />}
        {activeTab === 'analytics' && <Web3Analytics />}
      </main>
    </div>
  );
};

const LoginForm = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(username, password);
  };

  return (
    <form onSubmit={handleSubmit} className="login-form">
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
      <button type="submit">Entrar</button>
    </form>
  );
};

export default App;
```

## 🎨 Estilos CSS

```css
/* styles/web3.css */
.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.app-nav {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.app-nav button {
  padding: 10px 20px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  border-radius: 5px;
}

.app-nav button.active {
  background: #007bff;
  color: white;
}

.nft-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.nft-card {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 15px;
  text-align: center;
}

.nft-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 5px;
  margin-bottom: 10px;
}

.nft-price {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.bridge-form {
  max-width: 500px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.fees-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 5px;
  margin: 15px 0;
}

.bridge-status {
  background: #e7f3ff;
  padding: 15px;
  border-radius: 5px;
  margin-top: 20px;
}

.overview-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.stat {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 5px;
  text-align: center;
}

.chart-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 5px;
  margin-top: 15px;
}

.user-stats {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 5px;
  margin-top: 15px;
}

.login-form {
  max-width: 300px;
  margin: 0 auto;
}

.login-form input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.login-form button {
  width: 100%;
  padding: 10px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.login-page {
  text-align: center;
  padding: 50px 20px;
}
```

## 🚀 Deploy Frontend

### Build para Produção

```bash
# React
npm run build

# Vue
npm run build

# Angular
ng build --prod
```

### Configuração Nginx

```nginx
server {
    listen 80;
    server_name app.coinbalance.com;
    
    location / {
        root /var/www/coinbalance-frontend;
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://coinbalance-backend:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

**Este guia fornece uma base sólida para integrar todas as funcionalidades Web3 do CoinBalance em aplicações frontend modernas!** 🎉
