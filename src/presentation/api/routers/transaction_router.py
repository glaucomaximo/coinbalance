"""
Router para endpoints de Transações
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from decimal import Decimal

from src.presentation.schemas.transaction_schema import (
    CreateTransferRequest,
    CreateStakeRequest,
    TransactionResponse,
    TransactionListResponse,
    TransactionStatsResponse,
)
from src.application.transaction.commands.create_transfer import CreateTransferCommand
from src.application.transaction.commands.create_transfer_handler import CreateTransferHandlerImpl
from src.application.transaction.queries.get_transaction import (
    GetTransactionQuery,
    GetTransactionsByAddressQuery,
    GetTransactionStatsQuery,
)
from src.domain.shared.exceptions import (
    DomainException,
    EntityNotFoundError,
    InsufficientFundsError,
)
from src.domain.shared.value_objects.wallet_address import WalletAddress
from src.domain.shared.value_objects.money import Money


router = APIRouter(
    prefix="/transacoes",
    tags=["Transações"],
    responses={
        404: {"description": "Transação não encontrada"},
        400: {"description": "Requisição inválida"},
        409: {"description": "Conflito (ex: saldo insuficiente)"},
    },
)


# Dependency para o handler de criação de transferência
async def get_create_transfer_handler() -> CreateTransferHandlerImpl:
    """
    Dependency para obter o handler de criação de transferência.
    
    Em uma implementação real, isso seria injetado via container DI.
    """
    from src.infrastructure.persistence.repositories.transaction.transaction_repository_impl import SQLiteTransactionRepository
    from src.infrastructure.persistence.repositories.wallet.wallet_repository_impl import SQLiteWalletRepository
    
    transaction_repository = SQLiteTransactionRepository()
    wallet_repository = SQLiteWalletRepository()
    
    return CreateTransferHandlerImpl(transaction_repository, wallet_repository)


@router.post(
    "/transferencia",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar Transferência",
    description="Cria uma nova transação de transferência entre carteiras"
)
async def create_transfer(
    request: CreateTransferRequest,
    handler: CreateTransferHandlerImpl = Depends(get_create_transfer_handler)
) -> TransactionResponse:
    """
    Cria uma nova transferência entre carteiras.
    
    - **from_address**: Endereço da carteira de origem
    - **to_address**: Endereço da carteira de destino
    - **amount**: Valor a ser transferido em CNB
    - **fee**: Taxa da transação (padrão: 0.001 CNB)
    - **memo**: Memo opcional
    - **metadata**: Metadados adicionais
    """
    try:
        # Criar comando
        command = CreateTransferCommand(
            from_address=WalletAddress(request.from_address),
            to_address=WalletAddress(request.to_address),
            amount=Money(request.amount),
            fee=Money(request.fee),
            memo=request.memo,
            metadata=request.metadata
        )
        
        # Executar comando
        transaction = await handler.execute(command)
        
        # Retornar response
        return TransactionResponse(
            id=str(transaction.id),
            from_address=str(transaction.from_address) if transaction.from_address else None,
            to_address=str(transaction.to_address),
            amount_cnb=transaction.amount.to_cnb(),
            fee_cnb=transaction.fee.to_cnb(),
            transaction_type=transaction.transaction_type.value,
            status=transaction.status.value,
            created_at=transaction.created_at.value,
            confirmed_at=transaction.confirmed_at.value if transaction.confirmed_at else None,
            block_height=transaction.block_height,
            transaction_hash=transaction.transaction_hash,
            memo=transaction.memo,
            metadata=transaction.metadata
        )
        
    except InsufficientFundsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": str(e), "code": "INSUFFICIENT_FUNDS"}
        )
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e), "code": "DOMAIN_ERROR"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error", "message": str(e)}
        )


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
    summary="Obter Transação por ID",
    description="Busca uma transação pelo seu ID único"
)
async def get_transaction(transaction_id: str) -> TransactionResponse:
    """
    Obtém informações detalhadas de uma transação.
    
    - **transaction_id**: ID único da transação
    """
    try:
        from src.infrastructure.persistence.repositories.transaction.transaction_repository_impl import SQLiteTransactionRepository
        from src.domain.transaction.value_objects.transaction_id import TransactionId
        
        repository = SQLiteTransactionRepository()
        transaction = await repository.find_by_id(TransactionId(transaction_id))
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Transaction not found", "code": "TRANSACTION_NOT_FOUND"}
            )
        
        return TransactionResponse(
            id=str(transaction.id),
            from_address=str(transaction.from_address) if transaction.from_address else None,
            to_address=str(transaction.to_address),
            amount_cnb=transaction.amount.to_cnb(),
            fee_cnb=transaction.fee.to_cnb(),
            transaction_type=transaction.transaction_type.value,
            status=transaction.status.value,
            created_at=transaction.created_at.value,
            confirmed_at=transaction.confirmed_at.value if transaction.confirmed_at else None,
            block_height=transaction.block_height,
            transaction_hash=transaction.transaction_hash,
            memo=transaction.memo,
            metadata=transaction.metadata
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error", "message": str(e)}
        )


@router.get(
    "/endereco/{address}",
    response_model=TransactionListResponse,
    summary="Listar Transações por Endereço",
    description="Lista transações relacionadas a um endereço específico"
)
async def get_transactions_by_address(
    address: str,
    limit: int = Query(50, ge=1, le=100, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação")
) -> TransactionListResponse:
    """
    Lista transações de um endereço específico.
    
    - **address**: Endereço da carteira
    - **limit**: Limite de resultados (1-100)
    - **offset**: Offset para paginação
    """
    try:
        from src.infrastructure.persistence.repositories.transaction.transaction_repository_impl import SQLiteTransactionRepository
        
        repository = SQLiteTransactionRepository()
        transactions = await repository.find_by_address(
            WalletAddress(address), limit, offset
        )
        total = await repository.count_by_address(WalletAddress(address))
        
        transaction_responses = []
        for transaction in transactions:
            transaction_responses.append(TransactionResponse(
                id=str(transaction.id),
                from_address=str(transaction.from_address) if transaction.from_address else None,
                to_address=str(transaction.to_address),
                amount_cnb=transaction.amount.to_cnb(),
                fee_cnb=transaction.fee.to_cnb(),
                transaction_type=transaction.transaction_type.value,
                status=transaction.status.value,
                created_at=transaction.created_at.value,
                confirmed_at=transaction.confirmed_at.value if transaction.confirmed_at else None,
                block_height=transaction.block_height,
                transaction_hash=transaction.transaction_hash,
                memo=transaction.memo,
                metadata=transaction.metadata
            ))
        
        return TransactionListResponse(
            transactions=transaction_responses,
            total=total,
            limit=limit,
            offset=offset
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error", "message": str(e)}
        )


@router.get(
    "/pendentes",
    response_model=TransactionListResponse,
    summary="Listar Transações Pendentes",
    description="Lista todas as transações pendentes no sistema"
)
async def get_pending_transactions(
    limit: int = Query(100, ge=1, le=500, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação")
) -> TransactionListResponse:
    """
    Lista todas as transações pendentes.
    
    - **limit**: Limite de resultados (1-500)
    - **offset**: Offset para paginação
    """
    try:
        from src.infrastructure.persistence.repositories.transaction.transaction_repository_impl import SQLiteTransactionRepository
        
        repository = SQLiteTransactionRepository()
        transactions = await repository.find_pending_transactions()
        
        # Aplicar paginação
        paginated_transactions = transactions[offset:offset + limit]
        
        transaction_responses = []
        for transaction in paginated_transactions:
            transaction_responses.append(TransactionResponse(
                id=str(transaction.id),
                from_address=str(transaction.from_address) if transaction.from_address else None,
                to_address=str(transaction.to_address),
                amount_cnb=transaction.amount.to_cnb(),
                fee_cnb=transaction.fee.to_cnb(),
                transaction_type=transaction.transaction_type.value,
                status=transaction.status.value,
                created_at=transaction.created_at.value,
                confirmed_at=transaction.confirmed_at.value if transaction.confirmed_at else None,
                block_height=transaction.block_height,
                transaction_hash=transaction.transaction_hash,
                memo=transaction.memo,
                metadata=transaction.metadata
            ))
        
        return TransactionListResponse(
            transactions=transaction_responses,
            total=len(transactions),
            limit=limit,
            offset=offset
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error", "message": str(e)}
        )


@router.get(
    "/estatisticas",
    response_model=TransactionStatsResponse,
    summary="Estatísticas de Transações",
    description="Retorna estatísticas gerais das transações"
)
async def get_transaction_stats() -> TransactionStatsResponse:
    """
    Retorna estatísticas das transações.
    """
    try:
        from src.infrastructure.persistence.repositories.transaction.transaction_repository_impl import SQLiteTransactionRepository
        
        repository = SQLiteTransactionRepository()
        stats = await repository.get_transaction_stats()
        
        return TransactionStatsResponse(
            total_transactions=stats.get("total_transactions", 0),
            total_volume_cnb=stats.get("total_volume_cnb", Decimal("0")),
            total_fees_cnb=stats.get("total_fees_cnb", Decimal("0")),
            pending_transactions=stats.get("pending_transactions", 0),
            confirmed_transactions=stats.get("confirmed_transactions", 0),
            failed_transactions=stats.get("failed_transactions", 0)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error", "message": str(e)}
        )
