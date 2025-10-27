"""
Exceções de domínio
"""


class DomainException(Exception):
    """Exceção base para erros de domínio"""

    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code or self.__class__.__name__
        super().__init__(self.message)


class ValidationError(DomainException):
    """Erro de validação de regras de negócio"""

    pass


class EntityNotFoundError(DomainException):
    """Entidade não encontrada"""

    pass


class InvalidOperationError(DomainException):
    """Operação inválida no contexto atual"""

    pass


class InsufficientFundsError(DomainException):
    """Saldo insuficiente"""

    pass


class DuplicateEntityError(DomainException):
    """Entidade duplicada"""

    pass


class AuthenticationError(DomainException):
    """Erro de autenticação"""

    pass


class AuthorizationError(DomainException):
    """Erro de autorização"""

    pass
