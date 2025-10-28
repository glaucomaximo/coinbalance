"""
Sistema de Autenticação e Autorização para FastAPI
=================================================

Integração completa do sistema de autenticação com FastAPI,
incluindo middleware, dependências e decorators.
"""

import os
import sys
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps
import logging

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.infrastructure.security.auth_manager import (
    auth_manager, UserRole, Permission, get_auth_manager
)

logger = logging.getLogger(__name__)

# Configurar HTTPBearer
security = HTTPBearer()

@dataclass
class AuthenticatedUser:
    """Usuário autenticado."""
    id: str
    username: str
    email: str
    role: UserRole
    permissions: List[Permission]
    token: str

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> AuthenticatedUser:
    """
    Dependência para obter usuário atual autenticado.
    
    Args:
        credentials: Credenciais de autorização
        
    Returns:
        Usuário autenticado
        
    Raises:
        HTTPException: Se token inválido ou usuário não encontrado
    """
    try:
        token = credentials.credentials
        
        # Validar token JWT
        payload = auth_manager.validate_jwt_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Buscar usuário no banco
        user = auth_manager.get_user_by_id(payload["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar se usuário está ativo
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário inativo",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return AuthenticatedUser(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            permissions=list(user.permissions),
            token=token
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na autenticação: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro de autenticação",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_permission(permission: Permission):
    """
    Decorator para requerer permissão específica.
    
    Args:
        permission: Permissão requerida
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Encontrar usuário atual nos argumentos
            current_user = None
            for arg in args:
                if isinstance(arg, AuthenticatedUser):
                    current_user = arg
                    break
            
            if not current_user:
                for key, value in kwargs.items():
                    if isinstance(value, AuthenticatedUser):
                        current_user = value
                        break
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuário não autenticado"
                )
            
            # Verificar permissão
            if permission not in current_user.permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permissão '{permission.value}' requerida"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def require_role(role: UserRole):
    """
    Decorator para requerer role específica.
    
    Args:
        role: Role requerida
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Encontrar usuário atual nos argumentos
            current_user = None
            for arg in args:
                if isinstance(arg, AuthenticatedUser):
                    current_user = arg
                    break
            
            if not current_user:
                for key, value in kwargs.items():
                    if isinstance(value, AuthenticatedUser):
                        current_user = value
                        break
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuário não autenticado"
                )
            
            # Verificar role
            if current_user.role != role and current_user.role != UserRole.SUPER_ADMIN:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Role '{role.value}' requerida"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def require_scope(scope: str):
    """
    Dependência para requerer escopo específico.
    
    Args:
        scope: Escopo requerido (formato: "resource:action")
        
    Returns:
        Dependência FastAPI
    """
    async def scope_dependency(current_user: AuthenticatedUser = Depends(get_current_user)):
        try:
            resource, action = scope.split(":")
            
            # Mapear escopo para permissão
            permission_map = {
                "users:create": Permission.CREATE_USER,
                "users:delete": Permission.DELETE_USER,
                "users:modify": Permission.MODIFY_USER,
                "users:view": Permission.VIEW_USERS,
                "system:config": Permission.SYSTEM_CONFIG,
                "system:restart": Permission.SYSTEM_RESTART,
                "system:shutdown": Permission.SYSTEM_SHUTDOWN,
                "blockchain:mining": Permission.MINING_CONTROL,
                "blockchain:consensus": Permission.CONSENSUS_MANAGE,
                "blockchain:reset": Permission.BLOCKCHAIN_RESET,
                "economy:treasury": Permission.TREASURY_MANAGE,
                "economy:proposals": Permission.PROPOSALS_MANAGE,
                "economy:defi": Permission.DEFI_CONTROL,
                "fractal:manage": Permission.FRACTAL_MANAGE,
                "fractal:scaling": Permission.SCALING_CONTROL,
                "monitoring:advanced": Permission.MONITORING_ADVANCED,
                "security:override": Permission.SECURITY_OVERRIDE,
                "audit:logs": Permission.AUDIT_LOGS,
                "emergency:access": Permission.EMERGENCY_ACCESS
            }
            
            required_permission = permission_map.get(scope)
            if not required_permission:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Escopo inválido: {scope}"
                )
            
            # Verificar permissão
            if required_permission not in current_user.permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Escopo '{scope}' requerido"
                )
            
            return current_user
            
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Formato de escopo inválido: {scope}"
            )
    
    return scope_dependency

class RateLimiter:
    """Rate limiter simples em memória."""
    
    def __init__(self):
        self.requests = {}
        
    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        """
        Verifica se requisição é permitida.
        
        Args:
            key: Chave única (IP, user_id, etc.)
            limit: Limite de requisições
            window: Janela de tempo em segundos
            
        Returns:
            True se permitido, False caso contrário
        """
        import time
        
        now = time.time()
        
        # Limpar requisições antigas
        if key in self.requests:
            self.requests[key] = [
                req_time for req_time in self.requests[key] 
                if now - req_time < window
            ]
        else:
            self.requests[key] = []
        
        # Verificar limite
        if len(self.requests[key]) >= limit:
            return False
        
        # Adicionar requisição atual
        self.requests[key].append(now)
        return True

# Instância global do rate limiter
rate_limiter = RateLimiter()

def rate_limit_middleware(request: Request, call_next):
    """
    Middleware de rate limiting.
    
    Args:
        request: Requisição HTTP
        call_next: Próximo middleware/handler
        
    Returns:
        Resposta HTTP
    """
    try:
        # Obter IP do cliente
        client_ip = request.client.host
        
        # Verificar rate limit
        if not rate_limiter.is_allowed(
            key=client_ip,
            limit=auth_manager.config.rate_limit_requests,
            window=auth_manager.config.rate_limit_window
        ):
            return HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit excedido"
            )
        
        return call_next(request)
        
    except Exception as e:
        logger.error(f"Erro no rate limiting: {e}")
        return call_next(request)

# Funções de conveniência para uso em routers
def require_admin():
    """Requer role de admin."""
    return require_role(UserRole.ADMIN)

def require_moderator():
    """Requer role de moderador."""
    return require_role(UserRole.MODERATOR)

def require_operator():
    """Requer role de operador."""
    return require_role(UserRole.OPERATOR)

def require_super_admin():
    """Requer role de super admin."""
    return require_role(UserRole.SUPER_ADMIN)

# Escopos comuns
def require_user_management():
    """Requer permissão de gerenciamento de usuários."""
    return require_scope("users:create")

def require_system_config():
    """Requer permissão de configuração do sistema."""
    return require_scope("system:config")

def require_monitoring():
    """Requer permissão de monitoramento."""
    return require_scope("monitoring:advanced")

def require_fractal_management():
    """Requer permissão de gerenciamento fractal."""
    return require_scope("fractal:manage")

def require_audit_access():
    """Requer permissão de acesso a auditoria."""
    return require_scope("audit:logs")