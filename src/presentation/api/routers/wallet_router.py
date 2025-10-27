"""
Router para endpoints de Wallet
"""

from fastapi import APIRouter, HTTPException, status

from src.presentation.schemas.wallet_schema import (
    CreateWalletRequest,
    CreateWalletResponse,
    GetWalletResponse,
    WalletListResponse,
    WalletOperationRequest,
)
from src.presentation.api.dependencies import (
    CreateWalletHandlerDep,
    GetWalletHandlerDep,
)
from src.application.wallet.commands.create_wallet import CreateWalletCommand
from src.application.wallet.queries.get_wallet import GetWalletQuery
from src.domain.shared.exceptions import (
    DomainException,
    EntityNotFoundError,
    DuplicateEntityError,
)


router = APIRouter(
    prefix="/carteiras",
    tags=["Carteiras"],
    responses={
        404: {"description": "Carteira não encontrada"},
        400: {"description": "Requisição inválida"},
    },
)


@router.post(
    "/",
    response_model=CreateWalletResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar Nova Carteira",
    description="Cria uma nova carteira digital com chaves criptográficas seguras",
)
async def create_wallet(
    request: CreateWalletRequest, handler: CreateWalletHandlerDep
) -> CreateWalletResponse:
    """
    Cria uma nova carteira digital.

    - **name**: Nome da carteira (obrigatório)
    - **password**: Senha para criptografar chave privada (opcional)
    - **metadata**: Metadados adicionais (opcional)
    """
    try:
        # Criar command
        command = CreateWalletCommand(
            name=request.name, password=request.password, metadata=request.metadata
        )

        # Executar use case
        result = await handler.execute(command)

        # Retornar response
        return CreateWalletResponse(
            address=result.address,
            name=result.name,
            public_key=result.public_key,
            balance=result.balance,
            created_at=result.created_at,
        )

    except DuplicateEntityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": str(e), "code": e.code},
        )
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


@router.get(
    "/{address}",
    response_model=GetWalletResponse,
    summary="Obter Carteira por Endereço",
    description="Busca uma carteira pelo seu endereço único",
)
async def get_wallet(address: str, handler: GetWalletHandlerDep) -> GetWalletResponse:
    """
    Obtém informações detalhadas de uma carteira.

    - **address**: Endereço único da carteira
    """
    try:
        # Criar query
        query = GetWalletQuery(address=address)

        # Executar use case
        result = await handler.execute(query)

        # Retornar response
        return GetWalletResponse(
            address=result.address,
            name=result.name,
            public_key=result.public_key,
            balance_cnb=result.balance_cnb,
            balance_satoshi=result.balance_satoshi,
            created_at=result.created_at,
            updated_at=result.updated_at,
            is_active=result.is_active,
            metadata=result.metadata,
        )

    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": str(e), "code": e.code},
        )
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
