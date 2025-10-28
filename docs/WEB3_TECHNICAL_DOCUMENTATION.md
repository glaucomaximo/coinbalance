# 📚 Documentação Técnica Web3 - CoinBalance

## 🌐 Visão Geral

O CoinBalance Web3 é um ecossistema completo de funcionalidades Web3 integradas, oferecendo uma experiência unificada para interações com blockchain, NFTs, DeFi, DAO e muito mais.

## 🏗️ Arquitetura

### Estrutura de Módulos

```
src/infrastructure/web3/
├── smart_contracts.py      # Gerenciamento de Smart Contracts
├── wallet_connect.py       # Integração WalletConnect
├── defi_protocols.py       # Protocolos DeFi
├── nft_marketplace.py      # Marketplace de NFTs
├── dao_governance.py       # Governança DAO
├── cross_chain_bridge.py   # Ponte Cross-Chain
└── web3_analytics.py       # Analytics Web3
```

### Padrões Arquiteturais

- **Clean Architecture**: Separação clara de responsabilidades
- **Domain-Driven Design (DDD)**: Modelagem baseada no domínio
- **CQRS**: Separação de comandos e consultas
- **Fractal Architecture**: Escalabilidade infinita

## 🔧 Funcionalidades Implementadas

### 1. 🎨 NFT Marketplace

#### Funcionalidades
- Criação de NFTs (ERC-721, ERC-1155, ERC-4907)
- Listagem para venda (preço fixo, leilões, bundles, aluguel)
- Sistema de royalties automático
- Busca avançada por atributos
- Coleções e metadados

#### Endpoints API
```http
POST /api/v1/web3/nft/create
POST /api/v1/web3/nft/list
GET  /api/v1/web3/nft/search
GET  /api/v1/web3/nft/trending
```

#### Exemplo de Uso
```python
from src.infrastructure.web3.nft_marketplace import nft_marketplace_manager, NFTMetadata

# Criar NFT
metadata = NFTMetadata(
    name="Meu NFT",
    description="Descrição do NFT",
    image="https://example.com/image.jpg"
)

nft = nft_marketplace_manager.create_nft(
    contract_address="0x1234...",
    token_id="1",
    owner="0xabcd...",
    creator="0xabcd...",
    metadata=metadata
)

# Listar para venda
listing = nft_marketplace_manager.list_nft(
    nft_key=f"{nft.contract_address}:{nft.token_id}",
    seller=nft.owner,
    listing_type=ListingType.FIXED_PRICE,
    price=Decimal("100")
)
```

### 2. 🏛️ DAO Governance

#### Funcionalidades
- Criação de propostas de governança
- Sistema de votação com pesos baseados em tokens
- Delegação de votos
- Execução automática de propostas aprovadas
- Gestão do tesouro DAO

#### Endpoints API
```http
POST /api/v1/web3/dao/proposal
POST /api/v1/web3/dao/vote
GET  /api/v1/web3/dao/proposal/{proposal_id}
GET  /api/v1/web3/dao/treasury
```

#### Exemplo de Uso
```python
from src.infrastructure.web3.dao_governance import dao_governance_manager, ProposalType

# Criar proposta
proposal = dao_governance_manager.create_proposal(
    proposer="0xabcd...",
    title="Upgrade do Sistema",
    description="Proposta para upgrade do sistema",
    proposal_type=ProposalType.UPGRADE,
    targets=["0x1234..."],
    values=["0"],
    calldatas=["0x"]
)

# Votar
vote = dao_governance_manager.cast_vote(
    voter="0xabcd...",
    proposal_id=proposal.proposal_id,
    vote_type=VoteType.FOR
)
```

### 3. 🌉 Cross-Chain Bridge

#### Funcionalidades
- Ponte entre múltiplas blockchains (Ethereum, Polygon, BSC, Avalanche)
- Suporte a múltiplos tokens (CNB, USDC, etc.)
- Sistema de taxas configurável
- Rastreamento completo de transações
- Confirmações e validações de segurança

#### Endpoints API
```http
POST /api/v1/web3/bridge/initiate
GET  /api/v1/web3/bridge/status/{tx_id}
GET  /api/v1/web3/bridge/fees
GET  /api/v1/web3/bridge/supported-tokens
```

#### Exemplo de Uso
```python
from src.infrastructure.web3.cross_chain_bridge import cross_chain_bridge_manager, ChainType

# Iniciar bridge
bridge_tx = cross_chain_bridge_manager.initiate_bridge(
    source_chain=ChainType.ETHEREUM,
    target_chain=ChainType.POLYGON,
    sender="0xabcd...",
    receiver="0xabcd...",
    token="CNB",
    amount=Decimal("1000")
)

# Verificar status
status = cross_chain_bridge_manager.get_bridge_status(bridge_tx.tx_id)
```

### 4. 📊 Web3 Analytics

#### Funcionalidades
- Gráficos de preços históricos
- Análise de volume de transações
- Analytics de atividade de usuários
- Visão geral do mercado
- Geração de relatórios personalizados
- Métricas em tempo real

#### Endpoints API
```http
GET /api/v1/web3/analytics/price/{token}
GET /api/v1/web3/analytics/volume/{token}
GET /api/v1/web3/analytics/market-overview
GET /api/v1/web3/analytics/user/{address}
POST /api/v1/web3/analytics/report
```

#### Exemplo de Uso
```python
from src.infrastructure.web3.web3_analytics import web3_analytics_manager, TimeRange

# Gráfico de preços
price_chart = web3_analytics_manager.get_price_chart(
    token="CNB",
    time_range=TimeRange.DAY
)

# Visão geral do mercado
overview = web3_analytics_manager.get_market_overview()

# Analytics do usuário
user_analytics = web3_analytics_manager.get_user_analytics("0xabcd...")
```

## 🔐 Segurança

### Autenticação e Autorização
- JWT tokens para autenticação
- Role-based access control (RBAC)
- Rate limiting por IP e usuário
- Validação de permissões por endpoint

### Validações
- Validação de entrada com Pydantic
- Sanitização de dados
- Verificação de assinaturas
- Validação de contratos inteligentes

### Monitoramento
- Logs de auditoria completos
- Detecção de atividades suspeitas
- Alertas de segurança
- Métricas de performance

## 🚀 Performance

### Otimizações
- Cache inteligente com TTL
- Compressão de dados
- Load balancing automático
- Escalabilidade fractal

### Métricas
- Tempo de resposta < 100ms
- Throughput > 1000 req/s
- Uptime > 99.9%
- Escalabilidade infinita

## 🔧 Configuração

### Variáveis de Ambiente

#### Obrigatórias
```bash
JWT_SECRET_KEY=your-secure-jwt-key
COINBALANCE_MASTER_KEY=your-master-key
WEB3_PROVIDER_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
```

#### Opcionais
```bash
DATABASE_URL=sqlite:///./coinbalance.db
CACHE_SIZE=256MB
WORKER_COUNT=4
LOG_LEVEL=INFO
```

### Configuração de Produção
```bash
# Usar configuração de produção
cp .env.production .env

# Deploy com Docker
docker-compose -f docker-compose.production.yml up -d

# Verificar saúde
curl http://localhost:8001/health/live
```

## 📈 Monitoramento

### Health Checks
```http
GET /health/live    # Liveness probe
GET /health/ready   # Readiness probe
```

### Métricas
```http
GET /metrics        # Prometheus metrics
GET /api/v1/web3/analytics/market-overview
```

### Logs
```bash
# Ver logs em tempo real
docker-compose logs -f coinbalance-web3

# Logs específicos
tail -f logs/coinbalance.log
```

## 🧪 Testes

### Testes Unitários
```bash
python -m pytest tests/unit/
```

### Testes de Integração
```bash
python -m pytest tests/integration/
```

### Testes E2E
```bash
python tests/test_web3_advanced.py
```

### Testes de Performance
```bash
python tests/test_scalability.py
```

## 🔄 Backup e Recuperação

### Backup Automático
```bash
# Configurar cron job
0 2 * * * /app/backup.sh
```

### Restauração
```bash
# Restaurar backup
docker-compose exec postgres psql -U coinbalance -d coinbalance_prod < backup.sql
```

## 🌍 Deploy Multi-Região

### Configuração
```yaml
# docker-compose.global.yml
services:
  coinbalance-web3-us:
    environment:
      - REGION=us-east-1
      - DATABASE_URL=postgresql://us-db:5432/coinbalance
  
  coinbalance-web3-eu:
    environment:
      - REGION=eu-west-1
      - DATABASE_URL=postgresql://eu-db:5432/coinbalance
```

### Load Balancer Global
```nginx
upstream global_backend {
    server coinbalance-web3-us:8001 weight=3;
    server coinbalance-web3-eu:8001 weight=2;
}
```

## 📚 Exemplos de Integração

### Frontend (React)
```javascript
// Criar NFT
const createNFT = async (nftData) => {
  const response = await fetch('/api/v1/web3/nft/create', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(nftData)
  });
  return response.json();
};

// Obter analytics
const getAnalytics = async (token) => {
  const response = await fetch(`/api/v1/web3/analytics/price/${token}`);
  return response.json();
};
```

### Mobile (React Native)
```javascript
// Wallet Connect
import WalletConnect from '@walletconnect/react-native';

const walletConnect = new WalletConnect({
  bridge: 'https://bridge.walletconnect.org',
  clientMeta: {
    name: 'CoinBalance',
    description: 'Web3 Platform',
    url: 'https://coinbalance.com',
    icons: ['https://coinbalance.com/icon.png']
  }
});
```

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão Web3
```bash
# Verificar URL do provedor
echo $WEB3_PROVIDER_URL

# Testar conectividade
curl -X POST -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  $WEB3_PROVIDER_URL
```

#### 2. Erro de Autenticação
```bash
# Verificar JWT secret
echo $JWT_SECRET_KEY

# Testar login
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

#### 3. Erro de Banco de Dados
```bash
# Verificar conexão
docker-compose exec postgres psql -U coinbalance -d coinbalance_prod -c "SELECT 1;"

# Verificar logs
docker-compose logs postgres
```

## 📞 Suporte

### Documentação Adicional
- [API Reference](https://docs.coinbalance.com/api)
- [Web3 Guide](https://docs.coinbalance.com/web3)
- [Deployment Guide](https://docs.coinbalance.com/deploy)

### Comunidade
- [Discord](https://discord.gg/coinbalance)
- [Telegram](https://t.me/coinbalance)
- [GitHub](https://github.com/coinbalance/coinbalance)

### Suporte Técnico
- Email: support@coinbalance.com
- Issues: https://github.com/coinbalance/coinbalance/issues
- Docs: https://docs.coinbalance.com

---

**Última atualização**: 27 de Outubro de 2025  
**Versão**: 2.1.0  
**Status**: Produção ✅
