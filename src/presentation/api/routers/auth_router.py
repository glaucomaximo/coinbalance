"""
Router de Autenticação e Autorização
====================================

Endpoints para autenticação, autorização e gerenciamento de usuários.
"""

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
import logging

from src.infrastructure.security.auth_manager import (
    auth_manager, UserRole, Permission, get_auth_manager
)
from src.infrastructure.security.auth import (
    get_current_user, AuthenticatedUser, require_scope
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação e Autorização"],
    responses={
        401: {"description": "Não autorizado"},
        403: {"description": "Permissão negada"},
        429: {"description": "Rate limit excedido"},
        500: {"description": "Erro interno do servidor"},
    },
)

# ========== SCHEMAS ==========

class LoginRequest(BaseModel):
    """Request de login."""
    username: str
    password: str

class LoginResponse(BaseModel):
    """Response de login."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]

class CreateUserRequest(BaseModel):
    """Request para criar usuário."""
    username: str
    email: EmailStr
    password: str
    role: str
    metadata: Optional[Dict[str, Any]] = None

class CreateUserResponse(BaseModel):
    """Response de criação de usuário."""
    user_id: str
    username: str
    email: str
    role: str
    created_at: float

class UserResponse(BaseModel):
    """Response de usuário."""
    id: str
    username: str
    email: str
    role: str
    is_active: bool
    created_at: float
    last_login: Optional[float]
    permissions: List[str]

class ChangePasswordRequest(BaseModel):
    """Request para alterar senha."""
    current_password: str
    new_password: str

class AuditLogResponse(BaseModel):
    """Response de log de auditoria."""
    id: str
    timestamp: float
    user_id: str
    action: str
    resource: str
    details: Dict[str, Any]
    ip_address: str
    success: bool

# ========== ENDPOINTS DE AUTENTICAÇÃO ==========

@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    http_request: Request
):
    """
    Autentica usuário e retorna token JWT.
    
    Args:
        request: Dados de login
        http_request: Requisição HTTP para obter IP
        
    Returns:
        Token JWT e informações do usuário
        
    Raises:
        HTTPException: Se credenciais inválidas
    """
    try:
        logger.info(f"Tentativa de login para usuário: {request.username}")
        
        # Obter IP do cliente
        client_ip = http_request.client.host
        
        # Autenticar usuário
        token = auth_manager.authenticate(
            username=request.username,
            password=request.password,
            ip_address=client_ip
        )
        
        logger.info(f"Resultado da autenticação: {'Sucesso' if token else 'Falha'}")
        
        if not token:
            logger.warning(f"Login falhou para usuário: {request.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Obter informações do usuário
        payload = auth_manager.validate_jwt_token(token)
        user = auth_manager.get_user_by_id(payload["user_id"])
        
        logger.info(f"Login bem-sucedido para usuário: {request.username}")
        
        return LoginResponse(
            access_token=token,
            expires_in=auth_manager.config.jwt_expiration_hours * 3600,
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.value,
                "permissions": [p.value for p in user.permissions]
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/logout")
async def logout(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Encerra sessão do usuário.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        Confirmação de logout
    """
    try:
        auth_manager.logout(current_user.token, current_user.id)
        
        return {
            "message": "Logout realizado com sucesso",
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Erro no logout: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retorna informações do usuário atual.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        Informações do usuário
    """
    try:
        user = auth_manager.get_user_by_id(current_user.id)
        
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role.value,
            is_active=user.is_active,
            created_at=user.created_at,
            last_login=user.last_login,
            permissions=[p.value for p in user.permissions]
        )
        
    except Exception as e:
        logger.error(f"Erro ao obter informações do usuário: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# ========== ENDPOINTS DE GERENCIAMENTO DE USUÁRIOS ==========

@router.post("/users", response_model=CreateUserResponse)
async def create_user(
    request: CreateUserRequest,
    current_user: AuthenticatedUser = Depends(require_scope("users:create"))
):
    """
    Cria um novo usuário.
    
    Args:
        request: Dados do usuário
        current_user: Usuário autenticado com permissão
        
    Returns:
        Informações do usuário criado
        
    Raises:
        HTTPException: Se não tiver permissão ou erro na criação
    """
    try:
        logger.info(f"Criando usuário: {request.username}")
        
        # Validar role
        try:
            role = UserRole(request.role)
        except ValueError:
            logger.error(f"Role inválida: {request.role}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role inválida: {request.role}"
            )
        
        logger.info(f"Role válida: {role.value}")
        
        # Criar usuário
        user = auth_manager.create_user(
            username=request.username,
            email=request.email,
            password=request.password,
            role=role,
            creator_id=current_user.id
        )
        
        logger.info(f"Resultado da criação: {'Sucesso' if user else 'Falha'}")
        
        if not user:
            logger.error("Falha ao criar usuário")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Falha ao criar usuário"
            )
        
        logger.info(f"Usuário criado com sucesso: {user.id}")
        
        return CreateUserResponse(
            user_id=user.id,
            username=user.username,
            email=user.email,
            role=user.role.value,
            created_at=user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/users", response_model=List[UserResponse])
async def list_users(
    current_user: AuthenticatedUser = Depends(require_scope("users:view"))
):
    """
    Lista todos os usuários.
    
    Args:
        current_user: Usuário autenticado com permissão
        
    Returns:
        Lista de usuários
    """
    try:
        users = auth_manager.list_users()
        
        return [
            UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                role=user.role.value,
                is_active=user.is_active,
                created_at=user.created_at,
                last_login=user.last_login,
                permissions=[p.value for p in user.permissions]
            )
            for user in users
        ]
        
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Altera senha do usuário atual.
    
    Args:
        request: Dados para alteração de senha
        current_user: Usuário autenticado
        
    Returns:
        Confirmação de alteração
    """
    try:
        # Verificar senha atual
        user = auth_manager.get_user_by_id(current_user.id)
        if not auth_manager.verify_password(request.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha atual incorreta"
            )
        
        # Validar nova senha
        if len(request.new_password) < auth_manager.config.password_min_length:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Nova senha deve ter pelo menos {auth_manager.config.password_min_length} caracteres"
            )
        
        # Alterar senha
        new_password_hash = auth_manager.hash_password(request.new_password)
        success = auth_manager.update_user(user.id, password_hash=new_password_hash)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Falha ao alterar senha"
            )
        
        return {
            "message": "Senha alterada com sucesso",
            "success": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao alterar senha: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# ========== ENDPOINTS DE AUDITORIA ==========

@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    limit: int = 100,
    current_user: AuthenticatedUser = Depends(require_scope("audit:logs"))
):
    """
    Retorna logs de auditoria.
    
    Args:
        limit: Limite de logs a retornar
        current_user: Usuário autenticado com permissão
        
    Returns:
        Lista de logs de auditoria
    """
    try:
        logs = auth_manager.get_audit_logs(limit=limit)
        
        return [
            AuditLogResponse(
                id=log.id,
                timestamp=log.timestamp,
                user_id=log.user_id,
                action=log.action,
                resource=log.resource,
                details=log.details,
                ip_address=log.ip_address,
                success=log.success
            )
            for log in logs
        ]
        
    except Exception as e:
        logger.error(f"Erro ao obter logs de auditoria: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# ========== ENDPOINTS DE SISTEMA ==========

@router.post("/init-super-admin")
async def init_super_admin():
    """
    Inicializa super admin padrão.
    
    Returns:
        Confirmação de inicialização
    """
    try:
        success = auth_manager.create_super_admin()
        
        if success:
            return {
                "message": "Super admin inicializado com sucesso",
                "success": True,
                "credentials": {
                    "username": "admin",
                    "password": "admin123",
                    "note": "Altere a senha após o primeiro login"
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Falha ao inicializar super admin"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao inicializar super admin: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )