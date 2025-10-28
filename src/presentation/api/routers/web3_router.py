"""
Router Web3 API para CoinBalance
Endpoints para integração Web3: Smart Contracts, Wallet Connect, DeFi
"""

import logging
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status, Depends
from src.infrastructure.security.auth import get_current_user, AuthenticatedUser, require_scope
from src.infrastructure.web3.nft_marketplace import (
    nft_marketplace_manager, NFTStandard, ListingType
)
from src.infrastructure.web3.dao_governance import (
    dao_governance_manager, ProposalType, VoteType
)
from src.infrastructure.web3.cross_chain_bridge import (
    cross_chain_bridge_manager, ChainType, BridgeType
)
from src.infrastructure.web3.web3_analytics import (
    web3_analytics_manager, MetricType, TimeRange
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/web3",
    tags=["Web3 Integration"],
    responses={
        400: {"description": "Bad Request"},
        401: {"description": "Não autorizado"},
        500: {"description": "Erro interno do servidor"},
    },
)

# ========== SCHEMAS ==========

class CreateContractRequest(BaseModel):
    contract_type: str = Field(..., description="Tipo do contrato")
    custom_params: Optional[Dict[str, Any]] = Field(None, description="Parâmetros customizados")

class ContractResponse(BaseModel):
    address: str
    name: str
    contract_type: str
    status: str
    deployer: str
    deployed_at: float

class WalletConnectRequest(BaseModel):
    wallet_type: str = Field(..., description="Tipo da carteira")
    chain_id: int = Field(1, description="ID da blockchain")

class WalletSessionResponse(BaseModel):
    session_id: str
    address: str
    chain_id: int
    status: str
    wallet_type: str

class SignMessageRequest(BaseModel):
    session_id: str = Field(..., description="ID da sessão")
    message: str = Field(..., description="Mensagem para assinar")

class TransactionRequest(BaseModel):
    session_id: str = Field(..., description="ID da sessão")
    to: str = Field(..., description="Endereço de destino")
    value: str = Field(..., description="Valor em wei")
    data: str = Field("0x", description="Dados da transação")

class DeFiSwapRequest(BaseModel):
    pool_address: str = Field(..., description="Endereço do pool")
    token_in: str = Field(..., description="Token de entrada")
    amount_in: str = Field(..., description="Quantidade de entrada")
    user_address: str = Field(..., description="Endereço do usuário")

class DeFiLiquidityRequest(BaseModel):
    pool_address: str = Field(..., description="Endereço do pool")
    amount_a: str = Field(..., description="Quantidade do token A")
    amount_b: str = Field(..., description="Quantidade do token B")
    user_address: str = Field(..., description="Endereço do usuário")

# ========== SMART CONTRACTS ENDPOINTS ==========

@router.post("/contracts", response_model=ContractResponse)
async def create_smart_contract(
    request: CreateContractRequest,
    current_user: AuthenticatedUser = Depends(require_scope("fractal_manage"))
):
    """
    Cria um novo contrato inteligente.
    
    Args:
        request: Dados do contrato
        current_user: Usuário autenticado
        
    Returns:
        Informações do contrato criado
    """
    try:
        logger.info(f"Criando contrato {request.contract_type} para usuário {current_user.username}")
        
        # Validar tipo de contrato
        try:
            contract_type = ContractType(request.contract_type.upper())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de contrato inválido: {request.contract_type}"
            )
        
        # Criar contrato
        contract = web3_contract_manager.create_contract(
            contract_type=contract_type,
            deployer=current_user.id,
            custom_params=request.custom_params
        )
        
        logger.info(f"Contrato criado: {contract.address}")
        
        return ContractResponse(
            address=contract.address,
            name=contract.name,
            contract_type=contract.contract_type.value,
            status=contract.status.value,
            deployer=contract.deployer,
            deployed_at=contract.deployed_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar contrato: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/contracts/{contract_address}/deploy")
async def deploy_contract(
    contract_address: str,
    current_user: AuthenticatedUser = Depends(require_scope("fractal_manage"))
):
    """
    Deploya um contrato inteligente.
    
    Args:
        contract_address: Endereço do contrato
        current_user: Usuário autenticado
        
    Returns:
        Status do deploy
    """
    try:
        logger.info(f"Deployando contrato {contract_address}")
        
        success = web3_contract_manager.deploy_contract(contract_address)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Falha ao fazer deploy do contrato"
            )
        
        logger.info(f"Contrato deployado com sucesso: {contract_address}")
        
        return {"message": "Contrato deployado com sucesso", "success": True}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao fazer deploy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/contracts", response_model=List[ContractResponse])
async def list_contracts(
    current_user: AuthenticatedUser = Depends(require_scope("fractal_manage"))
):
    """
    Lista todos os contratos inteligentes.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        Lista de contratos
    """
    try:
        contracts = web3_contract_manager.list_contracts()
        
        return [
            ContractResponse(
                address=contract.address,
                name=contract.name,
                contract_type=contract.contract_type.value,
                status=contract.status.value,
                deployer=contract.deployer,
                deployed_at=contract.deployed_at
            )
            for contract in contracts
        ]
        
    except Exception as e:
        logger.error(f"Erro ao listar contratos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# ========== WALLET CONNECT ENDPOINTS ==========

@router.post("/wallet/connect", response_model=WalletSessionResponse)
async def connect_wallet(
    request: WalletConnectRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Conecta uma carteira Web3.
    
    Args:
        request: Dados da conexão
        current_user: Usuário autenticado
        
    Returns:
        Informações da sessão
    """
    try:
        logger.info(f"Conectando carteira {request.wallet_type} para usuário {current_user.username}")
        
        # Validar tipo de carteira
        try:
            wallet_type = WalletType(request.wallet_type.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de carteira inválido: {request.wallet_type}"
            )
        
        # Conectar carteira
        result = await wallet_connect_manager.connect_wallet(
            wallet_type=wallet_type,
            chain_id=request.chain_id
        )
        
        logger.info(f"Carteira conectada: {result['address']}")
        
        return WalletSessionResponse(
            session_id=result["session_id"],
            address=result["address"],
            chain_id=result["chain_id"],
            status=result["status"],
            wallet_type=request.wallet_type
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao conectar carteira: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/wallet/sign")
async def sign_message(
    request: SignMessageRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Assina uma mensagem com a carteira conectada.
    
    Args:
        request: Dados da assinatura
        current_user: Usuário autenticado
        
    Returns:
        Assinatura da mensagem
    """
    try:
        logger.info(f"Assinando mensagem para usuário {current_user.username}")
        
        result = await wallet_connect_manager.sign_message(
            session_id=request.session_id,
            message=request.message
        )
        
        logger.info(f"Mensagem assinada: {result['signature'][:20]}...")
        
        return result
        
    except Exception as e:
        logger.error(f"Erro ao assinar mensagem: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/wallet/transaction")
async def send_transaction(
    request: TransactionRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Envia uma transação blockchain.
    
    Args:
        request: Dados da transação
        current_user: Usuário autenticado
        
    Returns:
        Hash da transação
    """
    try:
        logger.info(f"Enviando transação para usuário {current_user.username}")
        
        result = await wallet_connect_manager.send_transaction(
            session_id=request.session_id,
            to=request.to,
            value=request.value,
            data=request.data
        )
        
        logger.info(f"Transação enviada: {result['transaction_hash']}")
        
        return result
        
    except Exception as e:
        logger.error(f"Erro ao enviar transação: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# ========== DEFI ENDPOINTS ==========

@router.post("/defi/swap")
async def execute_swap(
    request: DeFiSwapRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Executa swap de tokens via DeFi.
    
    Args:
        request: Dados do swap
        current_user: Usuário autenticado
        
    Returns:
        Resultado do swap
    """
    try:
        logger.info(f"Executando swap para usuário {current_user.username}")
        
        from decimal import Decimal
        
        transaction = defi_protocol_manager.swap_tokens(
            pool_address=request.pool_address,
            token_in=request.token_in,
            amount_in=Decimal(request.amount_in),
            user_address=request.user_address
        )
        
        logger.info(f"Swap executado: {transaction.tx_hash}")
        
        return {
            "transaction_hash": transaction.tx_hash,
            "amount_in": str(transaction.amount_in),
            "amount_out": str(transaction.amount_out),
            "fee": str(transaction.fee),
            "timestamp": transaction.timestamp
        }
        
    except Exception as e:
        logger.error(f"Erro ao executar swap: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/defi/liquidity")
async def add_liquidity(
    request: DeFiLiquidityRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Adiciona liquidez ao pool DeFi.
    
    Args:
        request: Dados da liquidez
        current_user: Usuário autenticado
        
    Returns:
        Resultado da adição de liquidez
    """
    try:
        logger.info(f"Adicionando liquidez para usuário {current_user.username}")
        
        from decimal import Decimal
        
        transaction = defi_protocol_manager.add_liquidity(
            pool_address=request.pool_address,
            amount_a=Decimal(request.amount_a),
            amount_b=Decimal(request.amount_b),
            user_address=request.user_address
        )
        
        logger.info(f"Liquidez adicionada: {transaction.tx_hash}")
        
        return {
            "transaction_hash": transaction.tx_hash,
            "lp_tokens": str(transaction.amount_out),
            "timestamp": transaction.timestamp
        }
        
    except Exception as e:
        logger.error(f"Erro ao adicionar liquidez: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/defi/pools")
async def list_liquidity_pools(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Lista pools de liquidez disponíveis.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        Lista de pools
    """
    try:
        pools = []
        
        for pool_address, pool in defi_protocol_manager.liquidity_pools.items():
            pools.append({
                "address": pool.address,
                "token_a": pool.token_a.symbol,
                "token_b": pool.token_b.symbol,
                "reserve_a": str(pool.reserve_a),
                "reserve_b": str(pool.reserve_b),
                "apr": str(pool.apr),
                "fee_rate": str(pool.fee_rate)
            })
        
        return {"pools": pools}
        
    except Exception as e:
        logger.error(f"Erro ao listar pools: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/defi/positions/{user_address}")
async def get_user_positions(
    user_address: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Obtém posições DeFi do usuário.
    
    Args:
        user_address: Endereço do usuário
        current_user: Usuário autenticado
        
    Returns:
        Posições do usuário
    """
    try:
        positions = defi_protocol_manager.get_user_positions(user_address)
        
        return {"positions": positions}
        
    except Exception as e:
        logger.error(f"Erro ao obter posições: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# ========== SCHEMAS PARA NFT ==========

class CreateNFTRequest(BaseModel):
    contract_address: str
    token_id: str
    owner: str
    creator: str
    name: str
    description: str
    image_url: str

class ListNFTRequest(BaseModel):
    nft_key: str
    seller: str
    listing_type: str
    price: str
    currency: str = "CNB"

# ========== SCHEMAS PARA DAO ==========

class CreateProposalRequest(BaseModel):
    proposer: str
    title: str
    description: str
    proposal_type: str
    targets: List[str]
    values: List[str]
    calldatas: List[str]

class VoteRequest(BaseModel):
    voter: str
    proposal_id: str
    vote_type: str
    reason: Optional[str] = None

# ========== SCHEMAS PARA BRIDGE ==========

class InitiateBridgeRequest(BaseModel):
    source_chain: str
    target_chain: str
    sender: str
    receiver: str
    token: str
    amount: str

@router.post("/nft/create")
async def create_nft(
    request: CreateNFTRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Cria um novo NFT"""
    try:
        from src.infrastructure.web3.nft_marketplace import NFTMetadata
        
        metadata = NFTMetadata(
            name=request.name,
            description=request.description,
            image=request.image_url
        )
        
        nft = nft_marketplace_manager.create_nft(
            contract_address=request.contract_address,
            token_id=request.token_id,
            owner=request.owner,
            creator=request.creator,
            metadata=metadata
        )
        
        return {
            "success": True,
            "nft": {
                "token_id": nft.token_id,
                "contract_address": nft.contract_address,
                "owner": nft.owner,
                "creator": nft.creator,
                "name": nft.metadata.name
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao criar NFT: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/nft/list")
async def list_nft(
    request: ListNFTRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Lista um NFT para venda"""
    try:
        from decimal import Decimal
        
        listing = nft_marketplace_manager.list_nft(
            nft_key=request.nft_key,
            seller=request.seller,
            listing_type=ListingType(request.listing_type),
            price=Decimal(request.price),
            currency=request.currency
        )
        
        return {
            "success": True,
            "listing_id": listing.listing_id,
            "price": str(listing.price),
            "currency": listing.currency
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar NFT: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# ========== DAO GOVERNANCE ENDPOINTS ==========

@router.post("/dao/proposal")
async def create_proposal(
    request: CreateProposalRequest,
    current_user: AuthenticatedUser = Depends(require_scope("users:create"))
):
    """Cria uma proposta de governança"""
    try:
        proposal = dao_governance_manager.create_proposal(
            proposer=request.proposer,
            title=request.title,
            description=request.description,
            proposal_type=ProposalType(request.proposal_type),
            targets=request.targets,
            values=request.values,
            calldatas=request.calldatas
        )
        
        return {
            "success": True,
            "proposal_id": proposal.proposal_id,
            "title": proposal.title,
            "status": proposal.status.value
        }
        
    except Exception as e:
        logger.error(f"Erro ao criar proposta: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/dao/vote")
async def cast_vote(
    request: VoteRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Vota em uma proposta"""
    try:
        vote = dao_governance_manager.cast_vote(
            voter=request.voter,
            proposal_id=request.proposal_id,
            vote_type=VoteType(request.vote_type),
            reason=request.reason
        )
        
        return {
            "success": True,
            "vote_id": vote.bid_id,
            "vote_type": vote.vote_type.value,
            "weight": str(vote.weight)
        }
        
    except Exception as e:
        logger.error(f"Erro ao votar: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# ========== CROSS-CHAIN BRIDGE ENDPOINTS ==========

@router.post("/bridge/initiate")
async def initiate_bridge(
    request: InitiateBridgeRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Inicia uma transação de ponte"""
    try:
        from decimal import Decimal
        
        bridge_tx = cross_chain_bridge_manager.initiate_bridge(
            source_chain=ChainType(request.source_chain),
            target_chain=ChainType(request.target_chain),
            sender=request.sender,
            receiver=request.receiver,
            token=request.token,
            amount=Decimal(request.amount)
        )
        
        return {
            "success": True,
            "tx_id": bridge_tx.tx_id,
            "status": bridge_tx.status.value,
            "fee": str(bridge_tx.fee)
        }
        
    except Exception as e:
        logger.error(f"Erro ao iniciar bridge: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/bridge/status/{tx_id}")
async def get_bridge_status(
    tx_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Obtém status de uma transação de ponte"""
    try:
        status = cross_chain_bridge_manager.get_bridge_status(tx_id)
        return status
        
    except Exception as e:
        logger.error(f"Erro ao obter status do bridge: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# ========== WEB3 ANALYTICS ENDPOINTS ==========

@router.get("/analytics/price/{token}")
async def get_price_chart(
    token: str,
    time_range: str = "24h",
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Obtém gráfico de preços"""
    try:
        chart_data = web3_analytics_manager.get_price_chart(
            token=token,
            time_range=TimeRange(time_range)
        )
        return chart_data
        
    except Exception as e:
        logger.error(f"Erro ao obter gráfico de preços: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/analytics/market-overview")
async def get_market_overview(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Obtém visão geral do mercado"""
    try:
        overview = web3_analytics_manager.get_market_overview()
        return overview
        
    except Exception as e:
        logger.error(f"Erro ao obter visão geral: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/analytics/user/{user_address}")
async def get_user_analytics(
    user_address: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Obtém analytics de um usuário"""
    try:
        analytics = web3_analytics_manager.get_user_analytics(user_address)
        return analytics
        
    except Exception as e:
        logger.error(f"Erro ao obter analytics do usuário: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
