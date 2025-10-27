"""
Router para endpoints de Sistema (Faucet, Minting, etc.)
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from decimal import Decimal

from src.presentation.schemas.wallet_schema import GetWalletResponse
from src.domain.shared.value_objects.wallet_address import WalletAddress
from src.domain.shared.value_objects.money import Money
from src.domain.shared.exceptions import DomainException
from src.infrastructure.security.auth import get_current_user, AuthenticatedUser, require_scope


router = APIRouter(
    prefix="/sistema",
    tags=["Sistema"],
    responses={
        404: {"description": "Carteira não encontrada"},
        400: {"description": "Requisição inválida"},
        401: {"description": "Não autorizado"},
        403: {"description": "Permissão negada"},
    },
)


@router.post(
    "/faucet/{address}",
    response_model=GetWalletResponse,
    summary="Adicionar Saldo (Faucet)",
    description="Adiciona saldo a uma carteira para testes (apenas desenvolvimento)"
)
async def add_balance_faucet(
    address: str,
    amount: float = 100.0,
    current_user: AuthenticatedUser = Depends(require_scope("admin:faucet"))
) -> GetWalletResponse:
    """
    Adiciona saldo a uma carteira usando o sistema de faucet.
    
    - **address**: Endereço da carteira
    - **amount**: Quantidade a ser adicionada (padrão: 100 CNB)
    """
    try:
        from src.infrastructure.persistence.repositories.wallet.wallet_repository_impl import SQLiteWalletRepository
        
        repository = SQLiteWalletRepository()
        wallet_address = WalletAddress(address)
        
        # Buscar carteira
        wallet = await repository.find_by_address(wallet_address)
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Wallet not found", "code": "WALLET_NOT_FOUND"}
            )
        
        # Adicionar saldo
        wallet.credit(Money(Decimal(str(amount))), "Faucet credit")
        
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


@router.post(
    "/mint/{address}",
    response_model=GetWalletResponse,
    summary="Mint CNB",
    description="Cria novos CNB para uma carteira (apenas desenvolvimento)"
)
async def mint_cnb(
    address: str,
    amount: float = 1000.0,
    current_user: AuthenticatedUser = Depends(require_scope("admin:mint"))
) -> GetWalletResponse:
    """
    Cria novos CNB para uma carteira (minting).
    
    - **address**: Endereço da carteira
    - **amount**: Quantidade a ser criada (padrão: 1000 CNB)
    """
    try:
        from src.infrastructure.persistence.repositories.wallet.wallet_repository_impl import SQLiteWalletRepository
        
        repository = SQLiteWalletRepository()
        wallet_address = WalletAddress(address)
        
        # Buscar carteira
        wallet = await repository.find_by_address(wallet_address)
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Wallet not found", "code": "WALLET_NOT_FOUND"}
            )
        
        # Adicionar saldo via minting
        wallet.credit(Money(Decimal(str(amount))), "CNB Minting")
        
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
