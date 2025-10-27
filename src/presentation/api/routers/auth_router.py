"""
Router de Autenticação para CoinBalance
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional

from src.infrastructure.security.auth import (
    auth_service, 
    Token, 
    UserCredentials, 
    get_current_user,
    AuthenticatedUser,
    security
)

router = APIRouter(prefix="/auth", tags=["Autenticação"])

class LoginRequest(BaseModel):
    """Request de login"""
    wallet_address: str = Field(..., description="Endereço da carteira")
    password: str = Field(..., min_length=8, description="Senha da carteira")

class RefreshTokenRequest(BaseModel):
    """Request de refresh token"""
    refresh_token: str = Field(..., description="Refresh token")

class LogoutRequest(BaseModel):
    """Request de logout"""
    access_token: str = Field(..., description="Access token")

@router.post(
    "/login",
    response_model=Token,
    summary="Fazer Login",
    description="Autentica uma carteira e retorna tokens de acesso"
)
async def login(request: LoginRequest) -> Token:
    """
    Autentica uma carteira usando endereço e senha.
    
    - **wallet_address**: Endereço da carteira
    - **password**: Senha da carteira (mínimo 8 caracteres)
    
    Retorna tokens de acesso e refresh.
    """
    try:
        token = await auth_service.authenticate_wallet(
            request.wallet_address, 
            request.password
        )
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return token
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@router.post(
    "/refresh",
    response_model=Token,
    summary="Renovar Token",
    description="Renova o token de acesso usando refresh token"
)
async def refresh_token(request: RefreshTokenRequest) -> Token:
    """
    Renova o token de acesso usando um refresh token válido.
    
    - **refresh_token**: Token de refresh válido
    """
    try:
        token = await auth_service.refresh_access_token(request.refresh_token)
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return token
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@router.post(
    "/logout",
    summary="Fazer Logout",
    description="Revoga o token de acesso (logout)"
)
async def logout(request: LogoutRequest) -> dict:
    """
    Faz logout revogando o token de acesso.
    
    - **access_token**: Token de acesso a ser revogado
    """
    try:
        success = auth_service.revoke_token(request.access_token)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token não encontrado ou já revogado"
            )
        
        return {
            "success": True,
            "message": "Logout realizado com sucesso"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@router.get(
    "/me",
    response_model=AuthenticatedUser,
    summary="Informações do Usuário",
    description="Retorna informações do usuário autenticado"
)
async def get_current_user_info(
    current_user: AuthenticatedUser = Depends(get_current_user)
) -> AuthenticatedUser:
    """
    Retorna informações do usuário atualmente autenticado.
    
    Requer token de acesso válido.
    """
    return current_user

@router.get(
    "/verify",
    summary="Verificar Token",
    description="Verifica se o token de acesso é válido"
)
async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Verifica se o token de acesso fornecido é válido.
    
    Retorna informações básicas sobre o token.
    """
    try:
        from src.infrastructure.security.auth import verify_token
        
        token_data = verify_token(credentials.credentials)
        
        return {
            "valid": True,
            "wallet_address": token_data.wallet_address,
            "scopes": token_data.scopes
        }
    
    except HTTPException:
        return {
            "valid": False,
            "error": "Token inválido ou expirado"
        }
