"""
Router para Blockchain e Mineração
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from decimal import Decimal

from src.domain.blockchain.entities.blockchain import Blockchain
from src.domain.blockchain.entities.block import Block
from src.domain.blockchain.services.mining_service import MiningService
from src.infrastructure.persistence.database_manager import DatabaseManager
from src.infrastructure.persistence.repositories.block_repository_impl import SQLiteBlockRepository

router = APIRouter(prefix="/blockchain", tags=["Blockchain"])

# Instância global da blockchain (em produção, seria injetada via DI)
_blockchain_instance: Optional[Blockchain] = None
_mining_service_instance: Optional[MiningService] = None

def get_blockchain() -> Blockchain:
    """Dependency para obter instância da blockchain"""
    global _blockchain_instance
    if _blockchain_instance is None:
        _blockchain_instance = Blockchain.create()
    return _blockchain_instance

def get_mining_service(blockchain: Blockchain = Depends(get_blockchain)) -> MiningService:
    """Dependency para obter serviço de mineração"""
    global _mining_service_instance
    if _mining_service_instance is None:
        _mining_service_instance = MiningService(blockchain)
    return _mining_service_instance

class BlockResponse(BaseModel):
    """Response para informações de bloco"""
    height: int
    hash: str
    previous_hash: Optional[str]
    timestamp: float
    nonce: int
    difficulty: int
    mining_time: float
    miner_address: Optional[str]
    block_reward: Decimal
    total_fees: Decimal
    transactions_count: int

class BlockchainStatsResponse(BaseModel):
    """Response para estatísticas da blockchain"""
    name: str
    version: str
    total_blocks: int
    total_transactions: int
    current_difficulty: int
    average_block_time: float
    total_mining_time: float
    current_block_reward: float
    total_supply: float
    chain_valid: bool
    latest_block_height: int

class MiningStatsResponse(BaseModel):
    """Response para estatísticas de mineração"""
    blocks_mined: int
    total_mining_time: float
    average_mining_time: float
    current_difficulty: int
    current_reward: Decimal
    estimated_hash_rate: float
    pool_size: int
    estimated_mining_time: float

class MineBlockRequest(BaseModel):
    """Request para mineração de bloco"""
    miner_address: str = Field(..., description="Endereço do minerador")
    max_transactions: Optional[int] = Field(None, description="Máximo de transações por bloco")

@router.get(
    "/stats",
    response_model=BlockchainStatsResponse,
    summary="Estatísticas da Blockchain",
    description="Retorna estatísticas completas da blockchain"
)
async def get_blockchain_stats(blockchain: Blockchain = Depends(get_blockchain)):
    """Retorna estatísticas da blockchain"""
    stats = blockchain.get_chain_stats()
    
    # Converter Decimal para float para serialização JSON
    stats["current_block_reward"] = float(stats["current_block_reward"])
    stats["total_supply"] = float(stats["total_supply"])
    
    return BlockchainStatsResponse(**stats)

@router.get(
    "/blocks",
    response_model=List[BlockResponse],
    summary="Listar Blocos",
    description="Lista todos os blocos da blockchain"
)
async def get_blocks(
    skip: int = 0,
    limit: int = 100,
    blockchain: Blockchain = Depends(get_blockchain)
):
    """Lista blocos da blockchain"""
    blocks = blockchain.blocks[skip:skip+limit]
    
    return [
        BlockResponse(
            height=block.height,
            hash=block.hash.value,
            previous_hash=block.previous_hash.value if block.previous_hash else None,
            timestamp=block.timestamp.value,
            nonce=block.nonce,
            difficulty=block.difficulty,
            mining_time=block.mining_time,
            miner_address=block.miner_address,
            block_reward=block.block_reward,
            total_fees=block.total_fees,
            transactions_count=len(block.transactions)
        )
        for block in blocks
    ]

@router.get(
    "/blocks/{height}",
    response_model=BlockResponse,
    summary="Obter Bloco por Altura",
    description="Retorna informações de um bloco específico"
)
async def get_block_by_height(
    height: int,
    blockchain: Blockchain = Depends(get_blockchain)
):
    """Retorna bloco por altura"""
    block = blockchain.get_block_by_height(height)
    
    if not block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Block at height {height} not found"
        )
    
    return BlockResponse(
        height=block.height,
        hash=block.hash.value,
        previous_hash=block.previous_hash.value if block.previous_hash else None,
        timestamp=block.timestamp.value,
        nonce=block.nonce,
        difficulty=block.difficulty,
        mining_time=block.mining_time,
        miner_address=block.miner_address,
        block_reward=block.block_reward,
        total_fees=block.total_fees,
        transactions_count=len(block.transactions)
    )

@router.get(
    "/blocks/hash/{block_hash}",
    response_model=BlockResponse,
    summary="Obter Bloco por Hash",
    description="Retorna informações de um bloco específico pelo hash"
)
async def get_block_by_hash(
    block_hash: str,
    blockchain: Blockchain = Depends(get_blockchain)
):
    """Retorna bloco por hash"""
    block = blockchain.get_block_by_hash(block_hash)
    
    if not block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Block with hash {block_hash} not found"
        )
    
    return BlockResponse(
        height=block.height,
        hash=block.hash.value,
        previous_hash=block.previous_hash.value if block.previous_hash else None,
        timestamp=block.timestamp.value,
        nonce=block.nonce,
        difficulty=block.difficulty,
        mining_time=block.mining_time,
        miner_address=block.miner_address,
        block_reward=block.block_reward,
        total_fees=block.total_fees,
        transactions_count=len(block.transactions)
    )

@router.get(
    "/latest",
    response_model=BlockResponse,
    summary="Último Bloco",
    description="Retorna o último bloco da blockchain"
)
async def get_latest_block(blockchain: Blockchain = Depends(get_blockchain)):
    """Retorna o último bloco"""
    block = blockchain.get_latest_block()
    
    if not block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No blocks found"
        )
    
    return BlockResponse(
        height=block.height,
        hash=block.hash.value,
        previous_hash=block.previous_hash.value if block.previous_hash else None,
        timestamp=block.timestamp.value,
        nonce=block.nonce,
        difficulty=block.difficulty,
        mining_time=block.mining_time,
        miner_address=block.miner_address,
        block_reward=block.block_reward,
        total_fees=block.total_fees,
        transactions_count=len(block.transactions)
    )

@router.get(
    "/mining/stats",
    response_model=MiningStatsResponse,
    summary="Estatísticas de Mineração",
    description="Retorna estatísticas de mineração"
)
async def get_mining_stats(mining_service: MiningService = Depends(get_mining_service)):
    """Retorna estatísticas de mineração"""
    stats = mining_service.get_mining_stats()
    return MiningStatsResponse(**stats)

@router.post(
    "/mining/mine",
    response_model=BlockResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Mineração de Bloco",
    description="Mina um novo bloco"
)
async def mine_block(
    request: MineBlockRequest,
    mining_service: MiningService = Depends(get_mining_service)
):
    """Mina um novo bloco"""
    try:
        mined_block = mining_service.mine_block(
            miner_address=request.miner_address,
            max_transactions=request.max_transactions
        )
        
        if not mined_block:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to mine block - no transactions available"
            )
        
        return BlockResponse(
            height=mined_block.height,
            hash=mined_block.hash.value,
            previous_hash=mined_block.previous_hash.value if mined_block.previous_hash else None,
            timestamp=mined_block.timestamp.value,
            nonce=mined_block.nonce,
            difficulty=mined_block.difficulty,
            mining_time=mined_block.mining_time,
            miner_address=mined_block.miner_address,
            block_reward=mined_block.block_reward,
            total_fees=mined_block.total_fees,
            transactions_count=len(mined_block.transactions)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Mining failed: {str(e)}"
        )

@router.get(
    "/mining/pool",
    summary="Pool de Transações",
    description="Retorna transações no pool de mineração"
)
async def get_mining_pool(mining_service: MiningService = Depends(get_mining_service)):
    """Retorna pool de transações"""
    pool = mining_service.get_transaction_pool()
    
    return {
        "pool_size": len(pool),
        "transactions": [
            {
                "id": tx.id.value,
                "from_address": tx.from_address.value if tx.from_address else None,
                "to_address": tx.to_address.value,
                "amount": float(tx.amount.value),
                "fee": float(tx.fee.value),
                "status": tx.status.value,
                "created_at": tx.created_at.value
            }
            for tx in pool
        ]
    }

@router.get(
    "/validate",
    summary="Validar Blockchain",
    description="Valida a integridade da blockchain"
)
async def validate_blockchain(blockchain: Blockchain = Depends(get_blockchain)):
    """Valida a integridade da blockchain"""
    is_valid = blockchain.is_chain_valid()
    
    return {
        "valid": is_valid,
        "total_blocks": len(blockchain.blocks),
        "message": "Blockchain is valid" if is_valid else "Blockchain validation failed"
    }
