"""
Container de Injeção de Dependências

Gerencia a criação e ciclo de vida das dependências da aplicação.
"""

from typing import Dict, Any, Callable
import inspect

from src.infrastructure.config.settings import settings


class Container:
    """
    Container simples de Dependency Injection.

    Gerencia:
    - Singletons (instância única)
    - Factories (nova instância a cada chamada)
    - Resolução automática de dependências
    """

    def __init__(self):
        self._singletons: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._config = settings

    def register_singleton(self, name: str, instance: Any) -> None:
        """Registra uma instância singleton"""
        self._singletons[name] = instance

    def register_factory(self, name: str, factory: Callable) -> None:
        """Registra uma factory"""
        self._factories[name] = factory

    def get(self, name: str) -> Any:
        """Obtém uma dependência"""
        # Verificar singletons
        if name in self._singletons:
            return self._singletons[name]

        # Verificar factories
        if name in self._factories:
            factory = self._factories[name]
            return self._resolve_factory(factory)

        raise ValueError(f"Dependency '{name}' not registered")

    def _resolve_factory(self, factory: Callable) -> Any:
        """Resolve dependências de uma factory e a executa"""
        sig = inspect.signature(factory)
        kwargs = {}

        for param_name, param in sig.parameters.items():
            if param_name in self._singletons:
                kwargs[param_name] = self._singletons[param_name]
            elif param_name in self._factories:
                kwargs[param_name] = self.get(param_name)

        return factory(**kwargs)

    @property
    def config(self):
        """Retorna configurações"""
        return self._config


# Função para configurar container
def configure_container() -> Container:
    """
    Configura e retorna o container com todas as dependências.
    """
    container = Container()

    # ========== INFRASTRUCTURE ==========

    # Database
    from src.infrastructure.persistence.database_manager import DatabaseManager

    db_manager = DatabaseManager()
    container.register_singleton("db_manager", db_manager)

    # ========== REPOSITORIES ==========

    from src.infrastructure.persistence.repositories.wallet_repository_impl import (
        WalletRepositoryImpl,
    )

    def wallet_repository_factory(db_manager):
        return WalletRepositoryImpl(db_manager)

    container.register_factory("wallet_repository", wallet_repository_factory)

    # ========== USE CASES ==========

    from src.application.wallet.commands.create_wallet import CreateWalletCommandHandler
    from src.application.wallet.queries.get_wallet import GetWalletQueryHandler

    def create_wallet_handler_factory(wallet_repository):
        return CreateWalletCommandHandler(wallet_repository)

    def get_wallet_handler_factory(wallet_repository):
        return GetWalletQueryHandler(wallet_repository)

    container.register_factory("create_wallet_handler", create_wallet_handler_factory)
    container.register_factory("get_wallet_handler", get_wallet_handler_factory)

    return container


# Singleton global
_container: Container = None


def get_container() -> Container:
    """Retorna container global (singleton)"""
    global _container
    if _container is None:
        _container = configure_container()
    return _container
