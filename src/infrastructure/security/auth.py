"""
Sistema de Autenticação JWT para CoinBalance
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets
import hashlib

# Configurações de segurança
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Contexto de criptografia para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de segurança
security = HTTPBearer()

class Token(BaseModel):
    """Modelo para tokens de acesso"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60

class TokenData(BaseModel):
    """Dados do token"""
    wallet_address: Optional[str] = None
    scopes: list[str] = []

class UserCredentials(BaseModel):
    """Credenciais do usuário"""
    wallet_address: str = Field(..., description="Endereço da carteira")
    password: str = Field(..., min_length=8, description="Senha da carteira")

class AuthenticatedUser(BaseModel):
    """Usuário autenticado"""
    wallet_address: str
    is_active: bool = True
    scopes: list[str] = ["wallet:read", "wallet:write"]

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera hash da senha"""
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Cria token de acesso JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: Dict[str, Any]) -> str:
    """Cria token de refresh JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """Verifica e decodifica token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        wallet_address: str = payload.get("sub")
        scopes: list[str] = payload.get("scopes", [])
        
        if wallet_address is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return TokenData(wallet_address=wallet_address, scopes=scopes)
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> AuthenticatedUser:
    """Obtém usuário atual a partir do token"""
    token_data = verify_token(credentials.credentials)
    
    # Aqui você pode buscar o usuário no banco de dados
    # Por enquanto, vamos criar um usuário mock
    return AuthenticatedUser(
        wallet_address=token_data.wallet_address,
        scopes=token_data.scopes
    )

def require_scope(required_scope: str):
    """Decorator para verificar escopo específico"""
    def scope_checker(current_user: AuthenticatedUser = Depends(get_current_user)):
        if required_scope not in current_user.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Escopo '{required_scope}' necessário"
            )
        return current_user
    return scope_checker

class AuthenticationService:
    """Serviço de autenticação"""
    
    def __init__(self):
        self.active_tokens: Dict[str, datetime] = {}
    
    async def authenticate_wallet(self, wallet_address: str, password: str) -> Optional[Token]:
        """Autentica carteira com senha"""
        # Aqui você deve verificar a senha no banco de dados
        # Por enquanto, vamos simular a autenticação
        
        # Simular verificação de senha (em produção, buscar no banco)
        if len(password) < 8:  # Validação básica
            return None
        
        # Criar tokens
        token_data = {
            "sub": wallet_address,
            "scopes": ["wallet:read", "wallet:write"],
            "iat": datetime.utcnow()
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        # Armazenar token ativo
        self.active_tokens[access_token] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    async def refresh_access_token(self, refresh_token: str) -> Optional[Token]:
        """Renova token de acesso usando refresh token"""
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            wallet_address = payload.get("sub")
            
            if wallet_address is None:
                return None
            
            # Criar novo token de acesso
            token_data = {
                "sub": wallet_address,
                "scopes": payload.get("scopes", ["wallet:read", "wallet:write"]),
                "iat": datetime.utcnow()
            }
            
            access_token = create_access_token(token_data)
            
            return Token(
                access_token=access_token,
                refresh_token=refresh_token,  # Manter o mesmo refresh token
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
        
        except JWTError:
            return None
    
    def revoke_token(self, token: str) -> bool:
        """Revoga token (logout)"""
        if token in self.active_tokens:
            del self.active_tokens[token]
            return True
        return False

# Instância global do serviço de autenticação
auth_service = AuthenticationService()
