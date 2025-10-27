"""
Router para Histórico de Transações
"""
from fastapi import APIRouter, HTTPException, status, Query, Path
from typing import List, Optional
from decimal import Decimal

from src.domain.transaction.services.transaction_history_service import (
    TransactionHistoryService,
    TransactionRecord,
    TransactionType,
    TransactionStatus
)
from src.infrastructure.persistence.database_manager import DatabaseManager

router = APIRouter(prefix="/historico", tags=["Histórico de Transações"])

# Schemas de resposta
class TransactionHistoryResponse:
    """Response para histórico de transações"""
    def __init__(self, record: TransactionRecord):
        self.id = record.id
        self.type = record.type.value
        self.status = record.status.value
        self.from_address = record.from_address
        self.to_address = record.to_address
        self.amount = float(record.amount)
        self.fee = float(record.fee)
        self.total_amount = float(record.total_amount)
        self.reason = record.reason
        self.description = record.description
        self.metadata = record.metadata
        self.created_at = record.created_at
        self.updated_at = record.updated_at
        self.block_height = record.block_height
        self.transaction_hash = record.transaction_hash
        self.confirmations = record.confirmations

class TransactionStatsResponse:
    """Response para estatísticas de transações"""
    def __init__(self, stats: dict):
        self.total_transactions = stats["total_transactions"]
        self.transfers = stats["transfers"]
        self.credits = stats["credits"]
        self.debits = stats["debits"]
        self.total_amount = stats["total_amount"]
        self.total_fees = stats["total_fees"]
        self.avg_amount = stats["avg_amount"]
        self.period_days = stats["period_days"]

@router.get(
    "/carteira/{wallet_address}",
    response_model=List[dict],
    summary="Histórico de Carteira",
    description="Obtém o histórico de transações de uma carteira específica"
)
async def get_wallet_history(
    wallet_address: str = Path(..., description="Endereço da carteira"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de transações"),
    offset: int = Query(0, ge=0, description="Número de transações para pular"),
    transaction_type: Optional[str] = Query(None, description="Tipo de transação (transfer, credit, debit)"),
    status: Optional[str] = Query(None, description="Status da transação (pending, completed, failed, cancelled)")
):
    """
    Obtém o histórico de transações de uma carteira específica.
    
    - **wallet_address**: Endereço da carteira
    - **limit**: Número máximo de transações (1-100)
    - **offset**: Número de transações para pular
    - **transaction_type**: Filtrar por tipo de transação
    - **status**: Filtrar por status da transação
    """
    try:
        # Configurar serviço
        db_manager = DatabaseManager()
        history_service = TransactionHistoryService(db_manager)
        
        # Converter filtros
        tx_type = None
        if transaction_type:
            try:
                tx_type = TransactionType(transaction_type)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"error": f"Invalid transaction type: {transaction_type}", "code": "INVALID_TYPE"}
                )
        
        tx_status = None
        if status:
            try:
                tx_status = TransactionStatus(status)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"error": f"Invalid transaction status: {status}", "code": "INVALID_STATUS"}
                )
        
        # Obter histórico
        records = history_service.get_wallet_history(
            wallet_address=wallet_address,
            limit=limit,
            offset=offset,
            transaction_type=tx_type,
            status=tx_status
        )
        
        # Converter para response
        response = []
        for record in records:
            response.append({
                "id": record.id,
                "type": record.type.value,
                "status": record.status.value,
                "from_address": record.from_address,
                "to_address": record.to_address,
                "amount": float(record.amount),
                "fee": float(record.fee),
                "total_amount": float(record.total_amount),
                "reason": record.reason,
                "description": record.description,
                "metadata": record.metadata,
                "created_at": record.created_at,
                "updated_at": record.updated_at,
                "block_height": record.block_height,
                "transaction_hash": record.transaction_hash,
                "confirmations": record.confirmations
            })
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"Internal server error: {str(e)}", "code": "INTERNAL_ERROR"}
        )

@router.get(
    "/transacao/{transaction_id}",
    response_model=dict,
    summary="Detalhes da Transação",
    description="Obtém detalhes de uma transação específica"
)
async def get_transaction_details(
    transaction_id: str = Path(..., description="ID da transação")
):
    """
    Obtém detalhes de uma transação específica.
    
    - **transaction_id**: ID único da transação
    """
    try:
        # Configurar serviço
        db_manager = DatabaseManager()
        history_service = TransactionHistoryService(db_manager)
        
        # Obter transação
        record = history_service.get_transaction_by_id(transaction_id)
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Transaction not found: {transaction_id}", "code": "TRANSACTION_NOT_FOUND"}
            )
        
        # Converter para response
        return {
            "id": record.id,
            "type": record.type.value,
            "status": record.status.value,
            "from_address": record.from_address,
            "to_address": record.to_address,
            "amount": float(record.amount),
            "fee": float(record.fee),
            "total_amount": float(record.total_amount),
            "reason": record.reason,
            "description": record.description,
            "metadata": record.metadata,
            "created_at": record.created_at,
            "updated_at": record.updated_at,
            "block_height": record.block_height,
            "transaction_hash": record.transaction_hash,
            "confirmations": record.confirmations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"Internal server error: {str(e)}", "code": "INTERNAL_ERROR"}
        )

@router.get(
    "/recentes",
    response_model=List[dict],
    summary="Transações Recentes",
    description="Obtém as transações mais recentes do sistema"
)
async def get_recent_transactions(
    limit: int = Query(20, ge=1, le=100, description="Número máximo de transações"),
    transaction_type: Optional[str] = Query(None, description="Tipo de transação (transfer, credit, debit)")
):
    """
    Obtém as transações mais recentes do sistema.
    
    - **limit**: Número máximo de transações (1-100)
    - **transaction_type**: Filtrar por tipo de transação
    """
    try:
        # Configurar serviço
        db_manager = DatabaseManager()
        history_service = TransactionHistoryService(db_manager)
        
        # Converter filtro
        tx_type = None
        if transaction_type:
            try:
                tx_type = TransactionType(transaction_type)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"error": f"Invalid transaction type: {transaction_type}", "code": "INVALID_TYPE"}
                )
        
        # Obter transações recentes
        records = history_service.get_recent_transactions(
            limit=limit,
            transaction_type=tx_type
        )
        
        # Converter para response
        response = []
        for record in records:
            response.append({
                "id": record.id,
                "type": record.type.value,
                "status": record.status.value,
                "from_address": record.from_address,
                "to_address": record.to_address,
                "amount": float(record.amount),
                "fee": float(record.fee),
                "total_amount": float(record.total_amount),
                "reason": record.reason,
                "description": record.description,
                "metadata": record.metadata,
                "created_at": record.created_at,
                "updated_at": record.updated_at,
                "block_height": record.block_height,
                "transaction_hash": record.transaction_hash,
                "confirmations": record.confirmations
            })
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"Internal server error: {str(e)}", "code": "INTERNAL_ERROR"}
        )

@router.get(
    "/estatisticas",
    response_model=dict,
    summary="Estatísticas de Transações",
    description="Obtém estatísticas de transações do sistema"
)
async def get_transaction_stats(
    wallet_address: Optional[str] = Query(None, description="Endereço da carteira (opcional)"),
    days: int = Query(30, ge=1, le=365, description="Período em dias (1-365)")
):
    """
    Obtém estatísticas de transações do sistema.
    
    - **wallet_address**: Endereço da carteira (opcional)
    - **days**: Período em dias para análise
    """
    try:
        # Configurar serviço
        db_manager = DatabaseManager()
        history_service = TransactionHistoryService(db_manager)
        
        # Obter estatísticas
        stats = history_service.get_transaction_stats(
            wallet_address=wallet_address,
            days=days
        )
        
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"Internal server error: {str(e)}", "code": "INTERNAL_ERROR"}
        )

@router.get(
    "/health",
    summary="Health Check",
    description="Verifica se o serviço de histórico está funcionando"
)
async def health_check() -> dict:
    """Verifica se o serviço de histórico está funcionando"""
    return {
        "service": "transaction_history",
        "status": "healthy",
        "version": "1.0.0"
    }
