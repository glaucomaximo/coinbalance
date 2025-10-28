"""
Advanced Web3 Router - Roteador Web3 Avançado
Implementação da Fase 2 do roadmap CoinBalance
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List, Optional
import logging
from pydantic import BaseModel
from decimal import Decimal

from src.infrastructure.web3.advanced_nft_marketplace import (
    nft_marketplace, 
    NFTStandard, 
    NFTStatus, 
    ListingType,
    NFTMetadata
)
from src.infrastructure.web3.advanced_defi_protocols import (
    defi_protocols,
    ProtocolType,
    PoolType
)
from src.infrastructure.web3.advanced_dao_governance import (
    dao_governance,
    ProposalType,
    ProposalStatus,
    VotingPower
)
from src.infrastructure.web3.advanced_cross_chain_bridge import (
    cross_chain_bridge,
    ChainType,
    BridgeStatus,
    BridgeType
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/web3-advanced", tags=["Web3 Advanced"])


# Schemas Pydantic para NFT Marketplace
class NFTMetadataRequest(BaseModel):
    name: str
    description: str
    image: str
    attributes: List[Dict[str, Any]] = []
    external_url: Optional[str] = None
    animation_url: Optional[str] = None


class CreateCollectionRequest(BaseModel):
    name: str
    description: str
    symbol: str
    creator: str
    total_supply: int
    royalty_percentage: float = 0.0


class MintNFTRequest(BaseModel):
    collection_id: str
    token_id: str
    owner: str
    creator: str
    metadata: NFTMetadataRequest
    standard: str = "ERC721"


class ListNFTRequest(BaseModel):
    nft_id: str
    seller: str
    listing_type: str
    price: float
    currency: str = "CNB"
    end_time: Optional[float] = None
    rental_duration: Optional[int] = None


# Schemas Pydantic para DeFi Protocols
class AddLiquidityRequest(BaseModel):
    pool_id: str
    user: str
    amounts: List[float]
    tokens: List[str]


class SwapRequest(BaseModel):
    pool_id: str
    user: str
    token_in: str
    token_out: str
    amount_in: float
    min_amount_out: float = 0.0


class SupplyRequest(BaseModel):
    pool_id: str
    user: str
    amount: float


class BorrowRequest(BaseModel):
    pool_id: str
    user: str
    amount: float
    collateral_pools: List[str]


# Schemas Pydantic para DAO Governance
class CreateProposalRequest(BaseModel):
    proposer: str
    title: str
    description: str
    proposal_type: str
    targets: List[str]
    values: List[float]
    calldatas: List[str]
    reason: Optional[str] = None


class VoteRequest(BaseModel):
    proposal_id: str
    voter: str
    support: int  # 0 = Against, 1 = For, 2 = Abstain
    reason: Optional[str] = None


class DelegateRequest(BaseModel):
    delegator: str
    delegatee: str
    amount: Optional[float] = None


# Schemas Pydantic para Cross-Chain Bridge
class BridgeRequest(BaseModel):
    from_chain: str
    to_chain: str
    token_symbol: str
    amount: float
    recipient: str
    sender: str
    bridge_type: str = "lock_mint"


# ========== NFT MARKETPLACE ENDPOINTS ==========

@router.post("/nft/collections")
async def create_collection(request: CreateCollectionRequest):
    """Cria uma nova coleção de NFTs"""
    try:
        collection = await nft_marketplace.create_collection(
            name=request.name,
            description=request.description,
            symbol=request.symbol,
            creator=request.creator,
            total_supply=request.total_supply,
            royalty_percentage=request.royalty_percentage
        )
        
        return {
            "status": "success",
            "collection": {
                "id": collection.id,
                "name": collection.name,
                "symbol": collection.symbol,
                "contract_address": collection.contract_address,
                "creator": collection.creator,
                "total_supply": collection.total_supply,
                "royalty_percentage": collection.royalty_percentage
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao criar coleção: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/nft/mint")
async def mint_nft(request: MintNFTRequest):
    """Mint um novo NFT"""
    try:
        metadata = NFTMetadata(
            name=request.metadata.name,
            description=request.metadata.description,
            image=request.metadata.image,
            attributes=request.metadata.attributes,
            external_url=request.metadata.external_url,
            animation_url=request.metadata.animation_url
        )
        
        standard = NFTStandard(request.standard)
        
        nft = await nft_marketplace.mint_nft(
            collection_id=request.collection_id,
            token_id=request.token_id,
            owner=request.owner,
            creator=request.creator,
            metadata=metadata,
            standard=standard
        )
        
        return {
            "status": "success",
            "nft": {
                "id": nft.id,
                "token_id": nft.token_id,
                "contract_address": nft.contract_address,
                "owner": nft.owner,
                "creator": nft.creator,
                "metadata": {
                    "name": nft.metadata.name,
                    "description": nft.metadata.description,
                    "image": nft.metadata.image
                },
                "status": nft.status.value
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao mintar NFT: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/nft/list")
async def list_nft(request: ListNFTRequest):
    """Lista um NFT para venda"""
    try:
        listing_type = ListingType(request.listing_type)
        
        listing = await nft_marketplace.list_nft(
            nft_id=request.nft_id,
            seller=request.seller,
            listing_type=listing_type,
            price=Decimal(str(request.price)),
            currency=request.currency,
            end_time=request.end_time,
            rental_duration=request.rental_duration
        )
        
        return {
            "status": "success",
            "listing": {
                "id": listing.id,
                "nft_id": listing.nft_id,
                "seller": listing.seller,
                "listing_type": listing.listing_type.value,
                "price": float(listing.price),
                "currency": listing.currency,
                "is_active": listing.is_active
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar NFT: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/nft/marketplace/stats")
async def get_nft_marketplace_stats():
    """Obtém estatísticas do marketplace NFT"""
    try:
        stats = nft_marketplace.get_marketplace_stats()
        return {
            "status": "success",
            "stats": stats
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas NFT: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== DEFI PROTOCOLS ENDPOINTS ==========

@router.post("/defi/liquidity/add")
async def add_liquidity(request: AddLiquidityRequest):
    """Adiciona liquidez a um pool"""
    try:
        amounts = [Decimal(str(amount)) for amount in request.amounts]
        
        result = await defi_protocols.add_liquidity(
            pool_id=request.pool_id,
            user=request.user,
            amounts=amounts,
            tokens=request.tokens
        )
        
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Erro ao adicionar liquidez: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/defi/swap")
async def swap_tokens(request: SwapRequest):
    """Realiza swap de tokens"""
    try:
        result = await defi_protocols.swap_tokens(
            pool_id=request.pool_id,
            user=request.user,
            token_in=request.token_in,
            token_out=request.token_out,
            amount_in=Decimal(str(request.amount_in)),
            min_amount_out=Decimal(str(request.min_amount_out))
        )
        
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Erro ao fazer swap: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/defi/lending/supply")
async def supply_to_lending(request: SupplyRequest):
    """Fornece tokens para pool de empréstimo"""
    try:
        result = await defi_protocols.supply_to_lending(
            pool_id=request.pool_id,
            user=request.user,
            amount=Decimal(str(request.amount))
        )
        
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Erro ao fornecer tokens: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/defi/lending/borrow")
async def borrow_from_lending(request: BorrowRequest):
    """Empresta tokens de pool de empréstimo"""
    try:
        result = await defi_protocols.borrow_from_lending(
            pool_id=request.pool_id,
            user=request.user,
            amount=Decimal(str(request.amount)),
            collateral_pools=request.collateral_pools
        )
        
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Erro ao emprestar tokens: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/defi/protocols/stats")
async def get_defi_protocols_stats():
    """Obtém estatísticas dos protocolos DeFi"""
    try:
        stats = defi_protocols.get_protocol_stats()
        return {
            "status": "success",
            "stats": stats
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas DeFi: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== DAO GOVERNANCE ENDPOINTS ==========

@router.post("/dao/proposals")
async def create_proposal(request: CreateProposalRequest):
    """Cria uma nova proposta DAO"""
    try:
        proposal_type = ProposalType(request.proposal_type)
        values = [Decimal(str(v)) for v in request.values]
        
        proposal = await dao_governance.create_proposal(
            proposer=request.proposer,
            title=request.title,
            description=request.description,
            proposal_type=proposal_type,
            targets=request.targets,
            values=values,
            calldatas=request.calldatas,
            reason=request.reason
        )
        
        return {
            "status": "success",
            "proposal": {
                "id": proposal.id,
                "title": proposal.title,
                "proposer": proposal.proposer,
                "type": proposal.proposal_type.value,
                "status": proposal.status.value
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao criar proposta: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/dao/vote")
async def cast_vote(request: VoteRequest):
    """Vota em uma proposta"""
    try:
        vote = await dao_governance.cast_vote(
            proposal_id=request.proposal_id,
            voter=request.voter,
            support=request.support,
            reason=request.reason
        )
        
        return {
            "status": "success",
            "vote": {
                "voter": vote.voter,
                "proposal_id": vote.proposal_id,
                "support": vote.support,
                "voting_power": float(vote.voting_power)
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao votar: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/dao/delegate")
async def delegate_votes(request: DelegateRequest):
    """Delega votos para outro membro"""
    try:
        amount = Decimal(str(request.amount)) if request.amount else None
        
        delegation = await dao_governance.delegate_votes(
            delegator=request.delegator,
            delegatee=request.delegatee,
            amount=amount
        )
        
        return {
            "status": "success",
            "delegation": {
                "delegator": delegation.delegator,
                "delegatee": delegation.delegatee,
                "amount": float(delegation.amount)
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao delegar votos: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/dao/governance/stats")
async def get_dao_governance_stats():
    """Obtém estatísticas da governança DAO"""
    try:
        stats = dao_governance.get_governance_stats()
        return {
            "status": "success",
            "stats": stats
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas DAO: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== CROSS-CHAIN BRIDGE ENDPOINTS ==========

@router.post("/bridge/initiate")
async def initiate_bridge(request: BridgeRequest):
    """Inicia uma transação de bridge"""
    try:
        from_chain = ChainType(request.from_chain)
        to_chain = ChainType(request.to_chain)
        bridge_type = BridgeType(request.bridge_type)
        
        transaction = await cross_chain_bridge.initiate_bridge(
            from_chain=from_chain,
            to_chain=to_chain,
            token_symbol=request.token_symbol,
            amount=Decimal(str(request.amount)),
            recipient=request.recipient,
            sender=request.sender,
            bridge_type=bridge_type
        )
        
        return {
            "status": "success",
            "transaction": {
                "id": transaction.id,
                "tx_hash": transaction.tx_hash,
                "from_chain": transaction.from_chain.value,
                "to_chain": transaction.to_chain.value,
                "amount": float(transaction.amount),
                "fee": float(transaction.fee),
                "status": transaction.status.value
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao iniciar bridge: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/bridge/transactions/{tx_id}")
async def get_bridge_transaction(tx_id: str):
    """Obtém detalhes de uma transação de bridge"""
    try:
        details = cross_chain_bridge.get_transaction_details(tx_id)
        
        if not details:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        return {
            "status": "success",
            "transaction": details
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter transação bridge: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bridge/stats")
async def get_bridge_stats():
    """Obtém estatísticas do bridge"""
    try:
        stats = cross_chain_bridge.get_bridge_stats()
        return {
            "status": "success",
            "stats": stats
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas bridge: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== ENDPOINTS DE CONTROLE GERAL ==========

@router.post("/start-all")
async def start_all_web3_advanced(background_tasks: BackgroundTasks):
    """Inicia todos os sistemas Web3 avançados"""
    try:
        # Iniciar todos os sistemas em background
        background_tasks.add_task(nft_marketplace.start_marketplace)
        background_tasks.add_task(defi_protocols.start_protocols)
        background_tasks.add_task(dao_governance.start_governance)
        background_tasks.add_task(cross_chain_bridge.start_bridge)
        
        return {
            "status": "success",
            "message": "Todos os sistemas Web3 avançados foram iniciados",
            "systems": [
                "NFT Marketplace",
                "DeFi Protocols", 
                "DAO Governance",
                "Cross-Chain Bridge"
            ]
        }
        
    except Exception as e:
        logger.error(f"Erro ao iniciar sistemas Web3: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop-all")
async def stop_all_web3_advanced():
    """Para todos os sistemas Web3 avançados"""
    try:
        await nft_marketplace.stop_marketplace()
        await defi_protocols.stop_protocols()
        await dao_governance.stop_governance()
        await cross_chain_bridge.stop_bridge()
        
        return {
            "status": "success",
            "message": "Todos os sistemas Web3 avançados foram parados"
        }
        
    except Exception as e:
        logger.error(f"Erro ao parar sistemas Web3: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_web3_advanced_status():
    """Obtém status de todos os sistemas Web3 avançados"""
    try:
        return {
            "status": "success",
            "systems": {
                "nft_marketplace": {
                    "active": nft_marketplace.is_active,
                    "stats": nft_marketplace.get_marketplace_stats()
                },
                "defi_protocols": {
                    "active": defi_protocols.is_active,
                    "stats": defi_protocols.get_protocol_stats()
                },
                "dao_governance": {
                    "active": dao_governance.is_active,
                    "stats": dao_governance.get_governance_stats()
                },
                "cross_chain_bridge": {
                    "active": cross_chain_bridge.is_active,
                    "stats": cross_chain_bridge.get_bridge_stats()
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter status Web3: {e}")
        raise HTTPException(status_code=500, detail=str(e))
