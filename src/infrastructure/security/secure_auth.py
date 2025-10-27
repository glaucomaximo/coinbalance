"""
Sistema de Autenticação Seguro para CoinBalance
"""

import os
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configurações de segurança
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    # Usar chave padrão para desenvolvimento
    SECRET_KEY = "dev-secret-key-change-in-production-32-chars-long"
    print("⚠️  AVISO: Usando chave JWT padrão para desenvolvimento!")
    print("   Configure JWT_SECRET_KEY para produção.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Reduzido para maior segurança
REFRESH_TOKEN_EXPIRE_DAYS = 1     # Reduzido para maior segurança

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
    scopes: list[str] = []

class SecureAuthenticationService:
    """Serviço de autenticação seguro"""
    
    def __init__(self, db_path: str = "blockchain.db"):
        self.db_path = db_path
        self.active_tokens: Dict[str, datetime] = {}
        self._init_auth_tables()
    
    def _init_auth_tables(self):
        """Inicializa tabelas de autenticação"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS wallet_auth (
                    wallet_address TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    last_login REAL,
                    failed_attempts INTEGER DEFAULT 0,
                    locked_until REAL,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS auth_sessions (
                    session_id TEXT PRIMARY KEY,
                    wallet_address TEXT NOT NULL,
                    access_token TEXT NOT NULL,
                    refresh_token TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    expires_at REAL NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (wallet_address) REFERENCES wallet_auth(wallet_address)
                )
            """)
            
            conn.commit()
    
    def _generate_salt(self) -> str:
        """Gera salt único"""
        return secrets.token_hex(32)
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Gera hash seguro da senha"""
        # Combinar senha + salt
        combined = password + salt
        
        # Usar PBKDF2 com SHA-256
        hash_obj = hashlib.pbkdf2_hmac('sha256', combined.encode(), salt.encode(), 100000)
        return hash_obj.hex()
    
    def _verify_password(self, password: str, salt: str, stored_hash: str) -> bool:
        """Verifica senha"""
        computed_hash = self._hash_password(password, salt)
        return secrets.compare_digest(computed_hash, stored_hash)
    
    def register_wallet(self, wallet_address: str, password: str) -> bool:
        """
        Registra uma nova carteira com autenticação
        
        Args:
            wallet_address: Endereço da carteira
            password: Senha da carteira
            
        Returns:
            True se registrada com sucesso
        """
        try:
            # Validar senha
            if len(password) < 8:
                raise ValueError("Password must be at least 8 characters long")
            
            if not any(c.isupper() for c in password):
                raise ValueError("Password must contain at least one uppercase letter")
            
            if not any(c.islower() for c in password):
                raise ValueError("Password must contain at least one lowercase letter")
            
            if not any(c.isdigit() for c in password):
                raise ValueError("Password must contain at least one digit")
            
            # Gerar salt único
            salt = self._generate_salt()
            
            # Gerar hash da senha
            password_hash = self._hash_password(password, salt)
            
            # Salvar no banco
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO wallet_auth 
                    (wallet_address, password_hash, salt, created_at)
                    VALUES (?, ?, ?, ?)
                """, (wallet_address, password_hash, salt, datetime.utcnow().timestamp()))
                
                conn.commit()
            
            return True
            
        except Exception as e:
            print(f"Erro ao registrar carteira: {e}")
            return False
    
    def authenticate_wallet(self, wallet_address: str, password: str) -> Optional[Token]:
        """
        Autentica uma carteira
        
        Args:
            wallet_address: Endereço da carteira
            password: Senha da carteira
            
        Returns:
            Token se autenticação bem-sucedida, None caso contrário
        """
        try:
            # Buscar dados da carteira
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT password_hash, salt, failed_attempts, locked_until, is_active
                    FROM wallet_auth 
                    WHERE wallet_address = ?
                """, (wallet_address,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                password_hash, salt, failed_attempts, locked_until, is_active = row
                
                # Verificar se conta está ativa
                if not is_active:
                    return None
                
                # Verificar se conta está bloqueada
                if locked_until and datetime.utcnow().timestamp() < locked_until:
                    return None
                
                # Verificar senha
                if not self._verify_password(password, salt, password_hash):
                    # Incrementar tentativas falhadas
                    self._increment_failed_attempts(wallet_address, failed_attempts)
                    return None
                
                # Resetar tentativas falhadas
                self._reset_failed_attempts(wallet_address)
                
                # Atualizar último login
                self._update_last_login(wallet_address)
                
                # Criar tokens
                token_data = {
                    "sub": wallet_address,
                    "scopes": ["wallet:read", "wallet:write"],
                    "iat": datetime.utcnow(),
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                }
                
                access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
                
                # Refresh token
                refresh_data = {
                    "sub": wallet_address,
                    "type": "refresh",
                    "iat": datetime.utcnow(),
                    "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
                }
                
                refresh_token = jwt.encode(refresh_data, SECRET_KEY, algorithm=ALGORITHM)
                
                # Salvar sessão
                self._save_session(wallet_address, access_token, refresh_token)
                
                return Token(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
                )
                
        except Exception as e:
            print(f"Erro na autenticação: {e}")
            return None
    
    def _increment_failed_attempts(self, wallet_address: str, current_attempts: int):
        """Incrementa tentativas falhadas"""
        new_attempts = current_attempts + 1
        locked_until = None
        
        # Bloquear após 5 tentativas por 30 minutos
        if new_attempts >= 5:
            locked_until = datetime.utcnow().timestamp() + (30 * 60)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE wallet_auth 
                SET failed_attempts = ?, locked_until = ?
                WHERE wallet_address = ?
            """, (new_attempts, locked_until, wallet_address))
            conn.commit()
    
    def _reset_failed_attempts(self, wallet_address: str):
        """Reseta tentativas falhadas"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE wallet_auth 
                SET failed_attempts = 0, locked_until = NULL
                WHERE wallet_address = ?
            """, (wallet_address,))
            conn.commit()
    
    def _update_last_login(self, wallet_address: str):
        """Atualiza último login"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE wallet_auth 
                SET last_login = ?
                WHERE wallet_address = ?
            """, (datetime.utcnow().timestamp(), wallet_address))
            conn.commit()
    
    def _save_session(self, wallet_address: str, access_token: str, refresh_token: str):
        """Salva sessão no banco"""
        session_id = secrets.token_hex(16)
        created_at = datetime.utcnow().timestamp()
        expires_at = created_at + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO auth_sessions 
                (session_id, wallet_address, access_token, refresh_token, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (session_id, wallet_address, access_token, refresh_token, created_at, expires_at))
            conn.commit()
    
    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verifica token JWT"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            wallet_address = payload.get("sub")
            
            if wallet_address is None:
                return None
            
            return TokenData(
                wallet_address=wallet_address,
                scopes=payload.get("scopes", [])
            )
            
        except JWTError:
            return None
    
    def refresh_access_token(self, refresh_token: str) -> Optional[Token]:
        """Renova token de acesso"""
        try:
            # Verificar refresh token
            token_data = self.verify_token(refresh_token)
            if not token_data:
                return None
            
            # Verificar se é um refresh token válido
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != "refresh":
                return None
            
            # Criar novo access token
            new_token_data = {
                "sub": token_data.wallet_address,
                "scopes": token_data.scopes,
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            }
            
            new_access_token = jwt.encode(new_token_data, SECRET_KEY, algorithm=ALGORITHM)
            
            return Token(
                access_token=new_access_token,
                refresh_token=refresh_token,  # Refresh token permanece o mesmo
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
            
        except JWTError:
            return None
    
    def logout(self, access_token: str) -> bool:
        """Faz logout invalidando token"""
        try:
            # Marcar sessão como inativa
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE auth_sessions 
                    SET is_active = 0
                    WHERE access_token = ?
                """, (access_token,))
                conn.commit()
            
            return True
            
        except Exception:
            return False

# Instância global do serviço
auth_service = SecureAuthenticationService()

# Funções auxiliares para compatibilidade
def create_access_token(data: dict) -> str:
    """Cria token de acesso"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    """Cria refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> AuthenticatedUser:
    """Obtém usuário atual"""
    token = credentials.credentials
    token_data = auth_service.verify_token(token)
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return AuthenticatedUser(
        wallet_address=token_data.wallet_address,
        scopes=token_data.scopes
    )

def require_scope(required_scope: str):
    """Decorator para verificar escopo"""
    def scope_checker(current_user: AuthenticatedUser = Depends(get_current_user)):
        if required_scope not in current_user.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions. Required scope: {required_scope}"
            )
        return current_user
    return scope_checker

# Alias para compatibilidade
AuthenticationService = SecureAuthenticationService
