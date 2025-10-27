"""
Dependency Injection para FastAPI endpoints
"""

from typing import Annotated
from fastapi import Depends

from src.infrastructure.di.container import get_container
from src.application.wallet.commands.create_wallet import CreateWalletCommandHandler
from src.application.wallet.queries.get_wallet import GetWalletQueryHandler


# ========== CONTAINER ==========


def get_di_container():
    """Retorna o container DI"""
    return get_container()


# ========== WALLET USE CASES ==========


def get_create_wallet_handler(
    container=Depends(get_di_container),
) -> CreateWalletCommandHandler:
    """Dependency para criar carteira"""
    return container.get("create_wallet_handler")


def get_get_wallet_handler(
    container=Depends(get_di_container),
) -> GetWalletQueryHandler:
    """Dependency para buscar carteira"""
    return container.get("get_wallet_handler")


# Type aliases para uso nos endpoints
CreateWalletHandlerDep = Annotated[
    CreateWalletCommandHandler, Depends(get_create_wallet_handler)
]
GetWalletHandlerDep = Annotated[GetWalletQueryHandler, Depends(get_get_wallet_handler)]
