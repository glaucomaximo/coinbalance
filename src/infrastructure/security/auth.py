"""
Sistema de Autenticação JWT para CoinBalance
DEPRECATED: Use secure_auth.py instead
"""

# Importar o novo sistema seguro
from .secure_auth import (
    auth_service,
    Token,
    TokenData,
    UserCredentials,
    AuthenticatedUser,
    security,
    create_access_token,
    create_refresh_token,
    get_current_user,
    require_scope,
    AuthenticationService
)

# Manter compatibilidade com código existente
__all__ = [
    'auth_service',
    'Token',
    'TokenData', 
    'UserCredentials',
    'AuthenticatedUser',
    'security',
    'create_access_token',
    'create_refresh_token',
    'get_current_user',
    'require_scope',
    'AuthenticationService'
]