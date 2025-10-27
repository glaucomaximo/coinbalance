"""
Router adicional para endpoints de Wallet (listagem e operações)
"""

from fastapi import APIRouter, HTTPException, status

from src.presentation.schemas.wallet_schema import (
    GetWalletResponse,
    WalletListResponse,
    WalletOperationRequest,
)
from src.presentation.api.dependencies import (
    GetWalletHandlerDep,
)
from src.domain.shared.exceptions import (
    DomainException,
    EntityNotFoundError,
)

router = APIRouter(
    prefix="/carteiras",
    tags=["Carteiras"],
    responses={
        404: {"description": "Carteira não encontrada"},
        400: {"description": "Requisição inválida"},
    },
)


@router.get(
    "/",
    response_model=WalletListResponse,
    summary="Listar Carteiras",
    description="Lista todas as carteiras cadastradas no sistema",
)
async def list_wallets(handler: GetWalletHandlerDep) -> WalletListResponse:
    """
    Lista todas as carteiras cadastradas.
    """
    try:
        from src.infrastructure.persistence.repositories.wallet_repository_impl import WalletRepositoryImpl
        
        from src.infrastructure.persistence.database_manager import DatabaseManager
        
        db_manager = DatabaseManager()
        repository = WalletRepositoryImpl(db_manager)
        wallets = await repository.find_all()
        
        wallet_responses = []
        for wallet in wallets:
            wallet_responses.append(GetWalletResponse(
                address=str(wallet.address),
                name=wallet.name,
                public_key=str(wallet.public_key),
                balance_cnb=wallet.balance.to_cnb(),
                balance_satoshi=wallet.balance.to_satoshi(),
                created_at=wallet.created_at.value,
                updated_at=wallet.updated_at.value,
                is_active=wallet.is_active,
                metadata=wallet.metadata
            ))
        
        return WalletListResponse(
            wallets=wallet_responses,
            total=len(wallet_responses)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error", "message": str(e)},
        )


@router.post(
    "/{address}/credit",
    response_model=GetWalletResponse,
    summary="Creditar Carteira",
    description="Adiciona saldo a uma carteira",
)
async def credit_wallet(
    address: str, 
    request: WalletOperationRequest
) -> GetWalletResponse:
    """
    Credita saldo a uma carteira.
    
    - **address**: Endereço da carteira
    - **amount**: Valor a ser creditado
    - **reason**: Motivo do crédito
    """
    try:
        from src.infrastructure.persistence.repositories.wallet_repository_impl import WalletRepositoryImpl
        from src.domain.shared.value_objects.wallet_address import WalletAddress
        from src.domain.shared.value_objects.money import Money
        from decimal import Decimal
        
        from src.infrastructure.persistence.database_manager import DatabaseManager
        
        db_manager = DatabaseManager()
        repository = WalletRepositoryImpl(db_manager)
        wallet_address = WalletAddress(address)
        
        # Buscar carteira
        wallet = await repository.find_by_address(wallet_address)
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Wallet with address '{address}' not found", "code": "WALLET_NOT_FOUND"}
            )
        
        # Creditar saldo
        wallet.credit(Money(Decimal(str(request.amount))), request.reason)
        
        # Salvar carteira atualizada
        await repository.save(wallet)
        
        # Retornar carteira atualizada
        return GetWalletResponse(
            address=str(wallet.address),
            name=wallet.name,
            public_key=str(wallet.public_key),
            balance_cnb=wallet.balance.to_cnb(),
            balance_satoshi=wallet.balance.to_satoshi(),
            created_at=wallet.created_at.value,
            updated_at=wallet.updated_at.value,
            is_active=wallet.is_active,
            metadata=wallet.metadata
        )
        
    except HTTPException:
        raise
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e), "code": e.code},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error", "message": str(e)},
        )


@router.post(
    "/{address}/debit",
    response_model=GetWalletResponse,
    summary="Debitar Carteira",
    description="Remove saldo de uma carteira",
)
async def debit_wallet(
    address: str, 
    request: WalletOperationRequest
) -> GetWalletResponse:
    """
    Debita saldo de uma carteira.
    
    - **address**: Endereço da carteira
    - **amount**: Valor a ser debitado
    - **reason**: Motivo do débito
    """
    try:
        from src.infrastructure.persistence.repositories.wallet_repository_impl import WalletRepositoryImpl
        from src.domain.shared.value_objects.wallet_address import WalletAddress
        from src.domain.shared.value_objects.money import Money
        from decimal import Decimal
        
        from src.infrastructure.persistence.database_manager import DatabaseManager
        
        db_manager = DatabaseManager()
        repository = WalletRepositoryImpl(db_manager)
        wallet_address = WalletAddress(address)
        
        # Buscar carteira
        wallet = await repository.find_by_address(wallet_address)
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Wallet with address '{address}' not found", "code": "WALLET_NOT_FOUND"}
            )
        
        # Debitar saldo
        wallet.debit(Money(Decimal(str(request.amount))), request.reason)
        
        # Salvar carteira atualizada
        await repository.save(wallet)
        
        # Retornar carteira atualizada
        return GetWalletResponse(
            address=str(wallet.address),
            name=wallet.name,
            public_key=str(wallet.public_key),
            balance_cnb=wallet.balance.to_cnb(),
            balance_satoshi=wallet.balance.to_satoshi(),
            created_at=wallet.created_at.value,
            updated_at=wallet.updated_at.value,
            is_active=wallet.is_active,
            metadata=wallet.metadata
        )
        
    except HTTPException:
        raise
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e), "code": e.code},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error", "message": str(e)},
        )
