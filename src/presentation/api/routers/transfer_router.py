"""
Router para Transferências entre Carteiras
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional

from src.application.transaction.commands.create_transfer_command import (
    CreateTransferCommand,
    CreateTransferCommandHandler,
    CreateTransferResult
)
from src.domain.shared.exceptions import DomainException

router = APIRouter(prefix="/transferencias", tags=["Transferências"])

class TransferRequest(BaseModel):
    """Request para transferência entre carteiras"""
    from_address: str = Field(..., description="Endereço da carteira de origem")
    to_address: str = Field(..., description="Endereço da carteira de destino")
    amount: Decimal = Field(..., gt=0, description="Valor a ser transferido")
    reason: str = Field(..., min_length=1, max_length=200, description="Motivo da transferência")
    fee: Optional[Decimal] = Field(None, description="Taxa personalizada (opcional)")

class TransferResponse(BaseModel):
    """Response da transferência"""
    success: bool
    transaction_id: str
    from_address: str
    to_address: str
    amount: float
    fee: float
    total_amount: float
    reason: str
    status: str
    created_at: float

@router.post(
    "/",
    response_model=TransferResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar Transferência",
    description="Cria uma nova transferência entre carteiras"
)
async def create_transfer(request: TransferRequest) -> TransferResponse:
    """
    Cria uma nova transferência entre carteiras.
    
    - **from_address**: Endereço da carteira de origem
    - **to_address**: Endereço da carteira de destino
    - **amount**: Valor a ser transferido em CNB
    - **reason**: Motivo da transferência
    - **fee**: Taxa personalizada (opcional)
    """
    try:
        from src.infrastructure.persistence.repositories.wallet_repository_impl import WalletRepositoryImpl
        from src.infrastructure.persistence.database_manager import DatabaseManager
        from src.domain.shared.domain_events.dispatcher import EventDispatcher
        
        # Configurar dependências
        db_manager = DatabaseManager()
        wallet_repository = WalletRepositoryImpl(db_manager)
        event_dispatcher = EventDispatcher()
        
        # Criar handler
        handler = CreateTransferCommandHandler(
            wallet_repository=wallet_repository,
            transaction_repository=None,  # Por enquanto não usamos
            event_dispatcher=event_dispatcher
        )
        
        # Criar comando
        command = CreateTransferCommand(
            from_address=request.from_address,
            to_address=request.to_address,
            amount=request.amount,
            reason=request.reason,
            fee=request.fee
        )
        
        # Executar comando
        result = await handler.execute(command)
        
        # Retornar resultado
        return TransferResponse(
            success=True,
            transaction_id=result.transaction_id,
            from_address=result.from_address,
            to_address=result.to_address,
            amount=float(result.amount),
            fee=float(result.fee),
            total_amount=float(result.total_amount),
            reason=result.reason,
            status=result.status,
            created_at=result.created_at
        )
        
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e), "code": "TRANSFER_FAILED"}
        )

@router.get(
    "/health",
    summary="Health Check",
    description="Verifica se o serviço de transferências está funcionando"
)
async def health_check() -> dict:
    """Verifica se o serviço de transferências está funcionando"""
    return {
        "service": "transferencias",
        "status": "healthy",
        "version": "1.0.0"
    }
