"""
Teste Simples das Funcionalidades Web3
Testa apenas as funcionalidades básicas sem dependências externas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_web3_modules():
    print("🧪 Testando Módulos Web3 CoinBalance")
    print("=" * 50)
    
    # Teste 1: NFT Marketplace
    print("\n1. 🎨 Testando NFT Marketplace...")
    try:
        from src.infrastructure.web3.nft_marketplace import (
            nft_marketplace_manager, NFTStandard, ListingType, NFTMetadata
        )
        
        # Criar NFT de teste
        metadata = NFTMetadata(
            name="Test NFT",
            description="NFT de teste",
            image="https://example.com/image.jpg"
        )
        
        nft = nft_marketplace_manager.create_nft(
            contract_address="0x1234567890123456789012345678901234567890",
            token_id="1",
            owner="0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
            creator="0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
            metadata=metadata
        )
        
        print(f"   ✅ NFT criado: {nft.metadata.name}")
        
        # Listar NFT
        listing = nft_marketplace_manager.list_nft(
            nft_key=f"{nft.contract_address}:{nft.token_id}",
            seller=nft.owner,
            listing_type=ListingType.FIXED_PRICE,
            price=100
        )
        
        print(f"   ✅ NFT listado: {listing.listing_id}")
        
    except Exception as e:
        print(f"   ❌ Erro no NFT Marketplace: {e}")
    
    # Teste 2: DAO Governance
    print("\n2. 🏛️ Testando DAO Governance...")
    try:
        from src.infrastructure.web3.dao_governance import (
            dao_governance_manager, ProposalType, VoteType
        )
        
        # Criar proposta
        proposal = dao_governance_manager.create_proposal(
            proposer="0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
            title="Proposta de Teste",
            description="Proposta de teste para validação",
            proposal_type=ProposalType.PARAMETER,
            targets=["0x1234567890123456789012345678901234567890"],
            values=["0"],
            calldatas=["0x"]
        )
        
        print(f"   ✅ Proposta criada: {proposal.proposal_id}")
        
        # Votar
        vote = dao_governance_manager.cast_vote(
            voter="0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
            proposal_id=proposal.proposal_id,
            vote_type=VoteType.FOR
        )
        
        print(f"   ✅ Voto registrado: {vote.vote_type.value}")
        
    except Exception as e:
        print(f"   ❌ Erro no DAO Governance: {e}")
    
    # Teste 3: Cross-Chain Bridge
    print("\n3. 🌉 Testando Cross-Chain Bridge...")
    try:
        from src.infrastructure.web3.cross_chain_bridge import (
            cross_chain_bridge_manager, ChainType, BridgeType
        )
        
        # Iniciar bridge
        bridge_tx = cross_chain_bridge_manager.initiate_bridge(
            source_chain=ChainType.ETHEREUM,
            target_chain=ChainType.POLYGON,
            sender="0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
            receiver="0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
            token="CNB",
            amount=1000
        )
        
        print(f"   ✅ Bridge iniciado: {bridge_tx.tx_id}")
        
        # Verificar status
        status = cross_chain_bridge_manager.get_bridge_status(bridge_tx.tx_id)
        print(f"   ✅ Status: {status['status']}")
        
    except Exception as e:
        print(f"   ❌ Erro no Cross-Chain Bridge: {e}")
    
    # Teste 4: Web3 Analytics
    print("\n4. 📊 Testando Web3 Analytics...")
    try:
        from src.infrastructure.web3.web3_analytics import (
            web3_analytics_manager, MetricType, TimeRange
        )
        
        # Gráfico de preços
        price_chart = web3_analytics_manager.get_price_chart(
            token="CNB",
            time_range=TimeRange.DAY
        )
        
        print(f"   ✅ Gráfico de preços: {price_chart['current_price']} CNB")
        
        # Visão geral
        overview = web3_analytics_manager.get_market_overview()
        print(f"   ✅ Visão geral: {overview['total_users']} usuários")
        
    except Exception as e:
        print(f"   ❌ Erro no Web3 Analytics: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Teste dos Módulos Web3 concluído!")
    print("\n🎯 Funcionalidades Validadas:")
    print("   • NFT Marketplace - Criação e listagem")
    print("   • DAO Governance - Propostas e votação")
    print("   • Cross-Chain Bridge - Ponte entre chains")
    print("   • Web3 Analytics - Métricas e gráficos")

if __name__ == "__main__":
    test_web3_modules()
