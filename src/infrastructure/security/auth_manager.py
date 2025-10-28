#!/usr/bin/env python3
"""
Sistema de Autenticação Completo do CoinBalance
==============================================

Sistema robusto de autenticação e autorização com:
- JWT tokens seguros
- Autorização baseada em roles
- Rate limiting
- Auditoria completa
"""

import os
import sys
import time
import hashlib
import secrets
import jwt
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
import sqlite3
from functools import wraps

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

logger = logging.getLogger(__name__)

class UserRole(Enum):
    """Roles de usuário."""
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MODERATOR = "moderator"
    OPERATOR = "operator"
    VIEWER = "viewer"

class Permission(Enum):
    """Permissões do sistema."""
    # Usuários
    CREATE_USER = "create_user"
    DELETE_USER = "delete_user"
    MODIFY_USER = "modify_user"
    VIEW_USERS = "view_users"
    
    # Sistema
    SYSTEM_CONFIG = "system_config"
    SYSTEM_RESTART = "system_restart"
    SYSTEM_SHUTDOWN = "system_shutdown"
    
    # Blockchain
    MINING_CONTROL = "mining_control"
    CONSENSUS_MANAGE = "consensus_manage"
    BLOCKCHAIN_RESET = "blockchain_reset"
    
    # Economia
    TREASURY_MANAGE = "treasury_manage"
    PROPOSALS_MANAGE = "proposals_manage"
    DEFI_CONTROL = "defi_control"
    
    # Fractais
    FRACTAL_MANAGE = "fractal_manage"
    SCALING_CONTROL = "scaling_control"
    MONITORING_ADVANCED = "monitoring_advanced"
    
    # Segurança
    SECURITY_OVERRIDE = "security_override"
    AUDIT_LOGS = "audit_logs"
    EMERGENCY_ACCESS = "emergency_access"

@dataclass
class User:
    """Usuário do sistema."""
    id: str
    username: str
    email: str
    password_hash: str
    role: UserRole
    permissions: Set[Permission] = field(default_factory=set)
    is_active: bool = True
    created_at: float = field(default_factory=time.time)
    last_login: Optional[float] = None
    login_attempts: int = 0
    locked_until: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AuthConfig:
    """Configurações de autenticação."""
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    password_min_length: int = 8
    max_login_attempts: int = 5
    lockout_duration: int = 3600  # 1 hora
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hora

class AuthManager:
    """Gerenciador de autenticação."""
    
    def __init__(self, db_path: str = "auth.db"):
        self.db_path = db_path
        self.config = self._load_config()
        self.init_database()
        self.setup_default_permissions()
        
    def _load_config(self) -> AuthConfig:
        """Carrega configurações de autenticação."""
        jwt_secret = os.getenv('JWT_SECRET_KEY')
        if not jwt_secret:
            # Gerar chave segura para desenvolvimento
            import secrets
            jwt_secret = secrets.token_urlsafe(32)
            logger.warning("⚠️ Gerando chave JWT temporária para desenvolvimento!")
            logger.warning("   Configure JWT_SECRET_KEY para produção.")
        
        return AuthConfig(
            jwt_secret_key=jwt_secret,
            jwt_expiration_hours=int(os.getenv('JWT_EXPIRATION_HOURS', '24')),
            password_min_length=int(os.getenv('PASSWORD_MIN_LENGTH', '8')),
            max_login_attempts=int(os.getenv('MAX_LOGIN_ATTEMPTS', '5')),
            lockout_duration=int(os.getenv('LOCKOUT_DURATION', '3600')),
            rate_limit_requests=int(os.getenv('RATE_LIMIT_REQUESTS', '100')),
            rate_limit_window=int(os.getenv('RATE_LIMIT_WINDOW', '3600'))
        )
        
    def init_database(self):
        """Inicializa o banco de dados."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                permissions TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at REAL NOT NULL,
                last_login REAL,
                login_attempts INTEGER DEFAULT 0,
                locked_until REAL,
                metadata TEXT
            )
        """)
        
        # Tabela de tokens
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tokens (
                token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_at REAL NOT NULL,
                expires_at REAL NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                is_revoked BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Tabela de logs de auditoria
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id TEXT PRIMARY KEY,
                timestamp REAL NOT NULL,
                user_id TEXT,
                action TEXT NOT NULL,
                resource TEXT NOT NULL,
                details TEXT,
                ip_address TEXT,
                user_agent TEXT,
                success BOOLEAN NOT NULL
            )
        """)
        
        # Índices
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tokens_user ON tokens(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp)")
        
        conn.commit()
        conn.close()
        
    def setup_default_permissions(self):
        """Configura permissões padrão por role."""
        self.role_permissions = {
            UserRole.SUPER_ADMIN: set(Permission),
            UserRole.ADMIN: {
                Permission.CREATE_USER,
                Permission.MODIFY_USER,
                Permission.VIEW_USERS,
                Permission.SYSTEM_CONFIG,
                Permission.TREASURY_MANAGE,
                Permission.PROPOSALS_MANAGE,
                Permission.FRACTAL_MANAGE,
                Permission.MONITORING_ADVANCED,
                Permission.AUDIT_LOGS
            },
            UserRole.MODERATOR: {
                Permission.VIEW_USERS,
                Permission.PROPOSALS_MANAGE,
                Permission.MONITORING_ADVANCED,
                Permission.AUDIT_LOGS
            },
            UserRole.OPERATOR: {
                Permission.VIEW_USERS,
                Permission.MONITORING_ADVANCED
            },
            UserRole.VIEWER: {
                Permission.VIEW_USERS,
                Permission.MONITORING_ADVANCED
            }
        }
        
    def hash_password(self, password: str) -> str:
        """Hash da senha com salt."""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{password_hash.hex()}"
        
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verifica senha."""
        try:
            salt, hash_hex = password_hash.split(':')
            password_hash_check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return password_hash_check.hex() == hash_hex
        except:
            return False
            
    def create_user(self, username: str, email: str, password: str, role: UserRole, 
                   creator_id: str = None, ip_address: str = "127.0.0.1") -> Optional[User]:
        """Cria um novo usuário."""
        try:
            # Verificar se usuário já existe
            if self.get_user_by_username(username):
                logger.warning(f"Usuário {username} já existe")
                return None
                
            if self.get_user_by_email(email):
                logger.warning(f"Email {email} já existe")
                return None
                
            # Validar senha
            if len(password) < self.config.password_min_length:
                logger.warning(f"Senha muito curta (mínimo {self.config.password_min_length} caracteres)")
                return None
                
            # Criar usuário
            user_id = secrets.token_urlsafe(16)
            password_hash = self.hash_password(password)
            permissions = self.role_permissions.get(role, set())
            
            user = User(
                id=user_id,
                username=username,
                email=email,
                password_hash=password_hash,
                role=role,
                permissions=permissions
            )
            
            # Salvar no banco
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO users (id, username, email, password_hash, role, permissions, 
                                 is_active, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user.id,
                user.username,
                user.email,
                user.password_hash,
                user.role.value,
                json.dumps([p.value for p in user.permissions]),
                user.is_active,
                user.created_at,
                json.dumps(user.metadata)
            ))
            
            conn.commit()
            conn.close()
            
            # Log de auditoria
            self.log_audit(
                user_id=creator_id or "system",
                action="create_user",
                resource=f"user:{user_id}",
                details={"username": username, "role": role.value},
                ip_address=ip_address,
                success=True
            )
            
            logger.info(f"Usuário {username} criado com sucesso")
            return user
            
        except Exception as e:
            logger.error(f"Erro ao criar usuário {username}: {e}")
            return None
            
    def authenticate(self, username: str, password: str, ip_address: str = "127.0.0.1") -> Optional[str]:
        """Autentica usuário e retorna token JWT."""
        try:
            user = self.get_user_by_username(username)
            if not user:
                logger.warning(f"Tentativa de login com usuário inexistente: {username}")
                return None
                
            # Verificar se usuário está bloqueado
            if user.locked_until and time.time() < user.locked_until:
                logger.warning(f"Usuário {username} está bloqueado")
                return None
                
            # Verificar se usuário está ativo
            if not user.is_active:
                logger.warning(f"Usuário {username} está inativo")
                return None
                
            # Verificar senha
            if not self.verify_password(password, user.password_hash):
                # Incrementar tentativas de login
                self.increment_login_attempts(user.id)
                logger.warning(f"Senha incorreta para usuário {username}")
                return None
                
            # Login bem-sucedido
            self.reset_login_attempts(user.id)
            self.update_last_login(user.id)
            
            # Criar token JWT
            token = self.create_jwt_token(user)
            
            # Salvar token no banco
            self.save_token(token, user.id, ip_address)
            
            # Log de auditoria
            self.log_audit(
                user_id=user.id,
                action="login",
                resource="system",
                details={"username": username},
                ip_address=ip_address,
                success=True
            )
            
            logger.info(f"Login bem-sucedido para usuário {username}")
            return token
            
        except Exception as e:
            logger.error(f"Erro na autenticação de {username}: {e}")
            return None
            
    def create_jwt_token(self, user: User) -> str:
        """Cria token JWT."""
        now = datetime.utcnow()
        payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role.value,
            "permissions": [p.value for p in user.permissions],
            "iat": now,
            "exp": now + timedelta(hours=self.config.jwt_expiration_hours),
            "iss": "coinbalance",
            "sub": user.id
        }
        
        return jwt.encode(payload, self.config.jwt_secret_key, algorithm=self.config.jwt_algorithm)
        
    def validate_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Valida token JWT."""
        try:
            payload = jwt.decode(token, self.config.jwt_secret_key, algorithms=[self.config.jwt_algorithm])
            
            # Verificar se token não foi revogado
            if self.is_token_revoked(token):
                return None
                
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token JWT expirado")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Token JWT inválido")
            return None
            
    def save_token(self, token: str, user_id: str, ip_address: str):
        """Salva token no banco."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Decodificar token para obter expiração
            payload = jwt.decode(token, self.config.jwt_secret_key, algorithms=[self.config.jwt_algorithm], options={"verify_exp": False})
            expires_at = payload['exp']
            
            cursor.execute("""
                INSERT INTO tokens (token, user_id, created_at, expires_at, ip_address)
                VALUES (?, ?, ?, ?, ?)
            """, (token, user_id, time.time(), expires_at, ip_address))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Erro ao salvar token: {e}")
            
    def is_token_revoked(self, token: str) -> bool:
        """Verifica se token foi revogado."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT is_revoked FROM tokens 
                WHERE token = ? AND expires_at > ?
            """, (token, time.time()))
            
            row = cursor.fetchone()
            conn.close()
            
            return row and row[0] if row else False
            
        except Exception as e:
            logger.error(f"Erro ao verificar token revogado: {e}")
            return True  # Em caso de erro, considerar revogado
            
    def revoke_token(self, token: str):
        """Revoga token."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE tokens SET is_revoked = TRUE WHERE token = ?", (token,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Erro ao revogar token: {e}")
            
    def logout(self, token: str, user_id: str = None):
        """Encerra sessão."""
        self.revoke_token(token)
        
        if user_id:
            self.log_audit(
                user_id=user_id,
                action="logout",
                resource="system",
                details={},
                ip_address="127.0.0.1",
                success=True
            )
            
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Busca usuário por username."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return self._row_to_user(row)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar usuário {username}: {e}")
            return None
            
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return self._row_to_user(row)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar usuário por email {email}: {e}")
            return None
            
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Busca usuário por ID."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return self._row_to_user(row)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar usuário {user_id}: {e}")
            return None
            
    def list_users(self) -> List[User]:
        """Lista todos os usuários."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
            rows = cursor.fetchall()
            conn.close()
            
            return [self._row_to_user(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Erro ao listar usuários: {e}")
            return []
            
    def _row_to_user(self, row) -> User:
        """Converte linha do banco em objeto User."""
        permissions_data = json.loads(row[5] or "[]")
        permissions = {Permission(p) for p in permissions_data}
        
        return User(
            id=row[0],
            username=row[1],
            email=row[2],
            password_hash=row[3],
            role=UserRole(row[4]),
            permissions=permissions,
            is_active=bool(row[6]),
            created_at=row[7],
            last_login=row[8],
            login_attempts=row[9] or 0,
            locked_until=row[10],
            metadata=json.loads(row[11] or "{}")
        )
        
    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """Verifica se usuário tem permissão."""
        try:
            user = self.get_user_by_id(user_id)
            if not user or not user.is_active:
                return False
                
            return permission in user.permissions
            
        except Exception as e:
            logger.error(f"Erro ao verificar permissão: {e}")
            return False
            
    def increment_login_attempts(self, user_id: str):
        """Incrementa tentativas de login."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE users 
                SET login_attempts = login_attempts + 1,
                    locked_until = CASE 
                        WHEN login_attempts >= ? THEN ? 
                        ELSE locked_until 
                    END
                WHERE id = ?
            """, (self.config.max_login_attempts - 1, time.time() + self.config.lockout_duration, user_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Erro ao incrementar tentativas de login: {e}")
            
    def reset_login_attempts(self, user_id: str):
        """Reseta tentativas de login."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE users 
                SET login_attempts = 0, locked_until = NULL
                WHERE id = ?
            """, (user_id,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Erro ao resetar tentativas de login: {e}")
            
    def update_last_login(self, user_id: str):
        """Atualiza último login."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (time.time(), user_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Erro ao atualizar último login: {e}")
            
    def update_user(self, user_id: str, **kwargs) -> bool:
        """Atualiza dados do usuário."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Construir query dinamicamente
            fields = []
            values = []
            
            for key, value in kwargs.items():
                if key == 'password_hash':
                    fields.append('password_hash = ?')
                    values.append(value)
                elif key == 'metadata':
                    fields.append('metadata = ?')
                    values.append(json.dumps(value))
                elif key in ['is_active', 'role']:
                    fields.append(f'{key} = ?')
                    values.append(value)
            
            if not fields:
                return False
            
            values.append(user_id)
            query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
            
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao atualizar usuário {user_id}: {e}")
            return False
            
    def get_audit_logs(self, limit: int = 100, user_id: str = None) -> List[Dict[str, Any]]:
        """Retorna logs de auditoria."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute("""
                    SELECT * FROM audit_logs 
                    WHERE user_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (user_id, limit))
            else:
                cursor.execute("""
                    SELECT * FROM audit_logs 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            logs = []
            for row in rows:
                logs.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'user_id': row[2],
                    'action': row[3],
                    'resource': row[4],
                    'details': json.loads(row[5] or "{}"),
                    'ip_address': row[6],
                    'user_agent': row[7],
                    'success': bool(row[8])
                })
            
            return logs
            
        except Exception as e:
            logger.error(f"Erro ao obter logs de auditoria: {e}")
            return []
            
    def log_audit(self, user_id: str, action: str, resource: str, details: Dict[str, Any],
                  ip_address: str = "127.0.0.1", user_agent: str = "", success: bool = True):
        """
        Registra log de auditoria com análise de conformidade.
        
        EVOLUÇÃO: Adiciona verificação de conformidade e análise de risco.
        """
        try:
            log_id = secrets.token_urlsafe(16)
            
            # EVOLUÇÃO: Análise de conformidade
            compliance_violations = self._check_compliance_violations(action, details, user_id)
            risk_score = self._calculate_risk_score(action, details, success)
            
            # Adicionar informações de conformidade aos detalhes
            enhanced_details = {
                **details,
                "compliance_violations": compliance_violations,
                "risk_score": risk_score,
                "compliance_checked": True
            }
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO audit_logs 
                (id, timestamp, user_id, action, resource, details, ip_address, user_agent, success)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                log_id,
                time.time(),
                user_id,
                action,
                resource,
                json.dumps(enhanced_details),
                ip_address,
                user_agent,
                success
            ))
            
            conn.commit()
            conn.close()
            
            # EVOLUÇÃO: Alertar sobre violações críticas
            if compliance_violations:
                self._handle_compliance_violations(log_id, compliance_violations, user_id)
            
            # EVOLUÇÃO: Alertar sobre alto risco
            if risk_score > 0.8:
                self._handle_high_risk_event(log_id, risk_score, action, user_id)
            
        except Exception as e:
            logger.error(f"Erro ao registrar log de auditoria: {e}")
    
    def _check_compliance_violations(self, action: str, details: Dict[str, Any], user_id: str) -> List[str]:
        """
        Verifica violações de conformidade incluindo LGPD.
        
        EVOLUÇÃO: Implementação real de verificação de conformidade com LGPD.
        """
        violations = []
        
        try:
            # Verificar AML/KYC para transações grandes
            if action == "transaction" and details.get("amount", 0) > 10000:
                if not details.get("kyc_verified", False):
                    violations.append("AML_KYC: Transação acima de $10,000 sem verificação KYC")
            
            # Verificar GDPR para acesso a dados pessoais
            if action == "access_personal_data" and not details.get("gdpr_consent", False):
                violations.append("GDPR: Acesso a dados pessoais sem consentimento")
            
            # EVOLUÇÃO: Verificar LGPD para dados pessoais brasileiros
            violations.extend(self._check_lgpd_compliance(action, details, user_id))
            
            # Verificar SOX para ações administrativas com impacto financeiro
            if action in ["admin_action", "financial_operation"] and details.get("financial_impact", False):
                if not details.get("sox_approved", False):
                    violations.append("SOX: Ação com impacto financeiro sem aprovação")
            
            # Verificar controle de acesso para ações administrativas
            if action == "admin_action" and not details.get("admin_authorized", False):
                violations.append("ACCESS_CONTROL: Ação administrativa não autorizada")
            
        except Exception as e:
            logger.error(f"Erro na verificação de conformidade: {e}")
        
        return violations
    
    def _check_lgpd_compliance(self, action: str, details: Dict[str, Any], user_id: str) -> List[str]:
        """
        Verifica conformidade específica com a LGPD (Lei Geral de Proteção de Dados).
        
        EVOLUÇÃO: Implementação específica para LGPD brasileira.
        """
        violations = []
        
        try:
            # Verificar se há dados pessoais brasileiros
            has_brazilian_data = details.get("country", "").upper() == "BR" or details.get("locale", "").upper() == "PT-BR"
            
            if has_brazilian_data or self._is_brazilian_user(user_id):
                
                # 1. Verificar base legal para tratamento de dados
                if action in ["collect_personal_data", "process_personal_data", "store_personal_data"]:
                    legal_basis = details.get("legal_basis")
                    valid_bases = ["consent", "contract", "legal_obligation", "legitimate_interest", "public_interest", "health_protection"]
                    
                    if not legal_basis or legal_basis not in valid_bases:
                        violations.append("LGPD: Base legal inválida ou ausente para tratamento de dados pessoais")
                
                # 2. Verificar consentimento específico e inequívoco
                if action == "collect_personal_data" and details.get("legal_basis") == "consent":
                    if not details.get("lgpd_consent", False):
                        violations.append("LGPD: Consentimento específico e inequívoco não obtido")
                    
                    # Verificar se consentimento foi livre (não condicionado)
                    if details.get("consent_conditioned", False):
                        violations.append("LGPD: Consentimento condicionado não é válido")
                
                # 3. Verificar finalidade específica e informada
                if action in ["collect_personal_data", "process_personal_data"]:
                    purpose = details.get("data_purpose")
                    if not purpose or len(purpose.strip()) < 10:
                        violations.append("LGPD: Finalidade do tratamento não especificada adequadamente")
                
                # 4. Verificar dados sensíveis (art. 5º, II)
                if details.get("sensitive_data", False):
                    if not details.get("sensitive_data_consent", False):
                        violations.append("LGPD: Consentimento específico ausente para dados sensíveis")
                    
                    # Verificar se há necessidade específica para dados sensíveis
                    if not details.get("sensitive_data_necessity", False):
                        violations.append("LGPD: Necessidade específica não justificada para dados sensíveis")
                
                # 5. Verificar dados de menores de idade (art. 14)
                if details.get("minor_data", False):
                    if not details.get("parental_consent", False):
                        violations.append("LGPD: Consentimento dos pais/responsáveis ausente para dados de menores")
                
                # 6. Verificar princípio da minimização (art. 6º, III)
                if action == "collect_personal_data":
                    data_types = details.get("data_types", [])
                    if len(data_types) > 5:  # Limite arbitrário para exemplo
                        violations.append("LGPD: Possível violação do princípio da minimização - muitos tipos de dados coletados")
                
                # 7. Verificar prazo de retenção (art. 16)
                if action == "store_personal_data":
                    retention_period = details.get("retention_period_days")
                    if not retention_period or retention_period > 2555:  # ~7 anos
                        violations.append("LGPD: Prazo de retenção não especificado ou excessivo")
                
                # 8. Verificar segurança dos dados (art. 46)
                if action in ["store_personal_data", "process_personal_data"]:
                    security_measures = details.get("security_measures", [])
                    required_measures = ["encryption", "access_control", "audit_log"]
                    
                    missing_measures = [measure for measure in required_measures if measure not in security_measures]
                    if missing_measures:
                        violations.append(f"LGPD: Medidas de segurança ausentes: {', '.join(missing_measures)}")
                
                # 9. Verificar transferência internacional (art. 33)
                if details.get("international_transfer", False):
                    if not details.get("adequacy_decision", False) and not details.get("appropriate_guarantees", False):
                        violations.append("LGPD: Transferência internacional sem adequação ou garantias apropriadas")
                
                # 10. Verificar registro de atividades (art. 50)
                if action in ["collect_personal_data", "process_personal_data", "delete_personal_data"]:
                    if not details.get("activity_logged", False):
                        violations.append("LGPD: Atividade de tratamento não registrada conforme art. 50")
            
        except Exception as e:
            logger.error(f"Erro na verificação de conformidade LGPD: {e}")
        
        return violations
    
    def _is_brazilian_user(self, user_id: str) -> bool:
        """
        Verifica se o usuário é brasileiro baseado em dados do sistema.
        
        EVOLUÇÃO: Detecção de usuários brasileiros para aplicação da LGPD.
        """
        try:
            # Em uma implementação real, isso consultaria o banco de dados
            # Por enquanto, simular baseado em padrões comuns de ID brasileiro
            
            # Verificar se há dados do usuário no banco
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT country, locale FROM users WHERE id = ?
            """, (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                country, locale = result
                return (country and country.upper() == "BR") or (locale and "BR" in locale.upper())
            
            # Fallback: verificar padrões comuns de usuários brasileiros
            # (CPF, telefone brasileiro, etc.)
            return False
            
        except Exception as e:
            logger.error(f"Erro ao verificar nacionalidade do usuário: {e}")
            return False
    
    def _calculate_risk_score(self, action: str, details: Dict[str, Any], success: bool) -> float:
        """
        Calcula score de risco do evento.
        
        EVOLUÇÃO: Implementação real de análise de risco.
        """
        try:
            risk_score = 0.0
            
            # Base score baseado no sucesso
            if not success:
                risk_score += 0.3
            
            # Ajustar baseado na ação
            high_risk_actions = ["admin_action", "financial_operation", "security_change", "user_creation"]
            if action in high_risk_actions:
                risk_score += 0.2
            
            # Ajustar baseado nos detalhes
            if details.get("amount", 0) > 50000:
                risk_score += 0.2
            
            if details.get("sensitive_data", False):
                risk_score += 0.1
            
            if details.get("external_access", False):
                risk_score += 0.1
            
            # Limitar entre 0 e 1
            return min(1.0, max(0.0, risk_score))
            
        except Exception as e:
            logger.error(f"Erro no cálculo de risco: {e}")
            return 0.5
    
    def _handle_compliance_violations(self, log_id: str, violations: List[str], user_id: str):
        """Trata violações de conformidade."""
        try:
            logger.warning(f"Violações de conformidade detectadas no log {log_id}: {violations}")
            
            # Em produção, aqui seria enviado alerta para equipe de conformidade
            # e/ou sistema de monitoramento
            
        except Exception as e:
            logger.error(f"Erro ao tratar violações de conformidade: {e}")
    
    def _handle_high_risk_event(self, log_id: str, risk_score: float, action: str, user_id: str):
        """Trata eventos de alto risco."""
        try:
            logger.critical(f"Evento de alto risco detectado: Log {log_id}, Score {risk_score}, Ação {action}")
            
            # Em produção, aqui seria enviado alerta imediato para equipe de segurança
            
        except Exception as e:
            logger.error(f"Erro ao tratar evento de alto risco: {e}")
    
    def handle_lgpd_data_subject_request(self, user_id: str, request_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa solicitações de titulares de dados conforme LGPD.
        
        EVOLUÇÃO: Implementação dos direitos dos titulares da LGPD.
        """
        try:
            # Verificar se o usuário é brasileiro
            if not self._is_brazilian_user(user_id):
                return {"error": "LGPD aplicável apenas a usuários brasileiros"}
            
            request_id = secrets.token_urlsafe(16)
            
            # Registrar solicitação
            self.log_audit(
                user_id=user_id,
                action=f"lgpd_{request_type}_request",
                resource="personal_data",
                details={
                    **details,
                    "request_id": request_id,
                    "lgpd_compliant": True,
                    "request_timestamp": time.time()
                },
                success=True
            )
            
            # Processar solicitação baseada no tipo
            if request_type == "access":
                return self._process_lgpd_access_request(user_id, request_id, details)
            elif request_type == "rectification":
                return self._process_lgpd_rectification_request(user_id, request_id, details)
            elif request_type == "deletion":
                return self._process_lgpd_deletion_request(user_id, request_id, details)
            elif request_type == "portability":
                return self._process_lgpd_portability_request(user_id, request_id, details)
            elif request_type == "opposition":
                return self._process_lgpd_opposition_request(user_id, request_id, details)
            else:
                return {"error": f"Tipo de solicitação LGPD não suportado: {request_type}"}
                
        except Exception as e:
            logger.error(f"Erro ao processar solicitação LGPD: {e}")
            return {"error": str(e)}
    
    def _process_lgpd_access_request(self, user_id: str, request_id: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Processa solicitação de acesso aos dados (art. 9º da LGPD)"""
        try:
            # Em implementação real, consultaria todos os dados do usuário
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, username, email, created_at, last_login, country, locale
                FROM users WHERE id = ?
            """, (user_id,))
            
            user_data = cursor.fetchone()
            conn.close()
            
            if not user_data:
                return {"error": "Usuário não encontrado"}
            
            # Preparar dados para retorno (sem informações sensíveis)
            response_data = {
                "user_id": user_data[0],
                "username": user_data[1],
                "email": user_data[2],
                "created_at": user_data[3],
                "last_login": user_data[4],
                "country": user_data[5],
                "locale": user_data[6],
                "data_categories": ["identification", "contact", "usage"],
                "processing_purposes": ["authentication", "service_provision", "security"],
                "retention_period": "5 years",
                "data_sharing": "No third-party sharing"
            }
            
            # Log da resposta
            self.log_audit(
                user_id=user_id,
                action="lgpd_access_response",
                resource="personal_data",
                details={
                    "request_id": request_id,
                    "data_provided": True,
                    "lgpd_compliant": True
                },
                success=True
            )
            
            return {
                "success": True,
                "request_id": request_id,
                "data": response_data,
                "message": "Dados pessoais fornecidos conforme art. 9º da LGPD"
            }
            
        except Exception as e:
            logger.error(f"Erro no processamento de acesso LGPD: {e}")
            return {"error": str(e)}
    
    def _process_lgpd_rectification_request(self, user_id: str, request_id: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Processa solicitação de retificação dos dados (art. 9º da LGPD)"""
        try:
            # Verificar dados a serem corrigidos
            fields_to_update = details.get("fields_to_update", {})
            
            if not fields_to_update:
                return {"error": "Nenhum campo especificado para correção"}
            
            # Validar campos permitidos
            allowed_fields = ["username", "email", "country", "locale"]
            invalid_fields = [field for field in fields_to_update.keys() if field not in allowed_fields]
            
            if invalid_fields:
                return {"error": f"Campos não permitidos para correção: {invalid_fields}"}
            
            # Atualizar dados no banco
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for field, new_value in fields_to_update.items():
                cursor.execute(f"""
                    UPDATE users SET {field} = ? WHERE id = ?
                """, (new_value, user_id))
            
            conn.commit()
            conn.close()
            
            # Log da correção
            self.log_audit(
                user_id=user_id,
                action="lgpd_rectification_completed",
                resource="personal_data",
                details={
                    "request_id": request_id,
                    "fields_updated": list(fields_to_update.keys()),
                    "lgpd_compliant": True
                },
                success=True
            )
            
            return {
                "success": True,
                "request_id": request_id,
                "updated_fields": list(fields_to_update.keys()),
                "message": "Dados corrigidos conforme art. 9º da LGPD"
            }
            
        except Exception as e:
            logger.error(f"Erro no processamento de retificação LGPD: {e}")
            return {"error": str(e)}
    
    def _process_lgpd_deletion_request(self, user_id: str, request_id: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Processa solicitação de exclusão dos dados (art. 16 da LGPD)"""
        try:
            # Verificar se há impedimentos legais para exclusão
            legal_obligations = details.get("legal_obligations", [])
            
            if legal_obligations:
                return {
                    "success": False,
                    "request_id": request_id,
                    "reason": "Impedimentos legais para exclusão",
                    "obligations": legal_obligations,
                    "message": "Exclusão parcial aplicada conforme art. 16 da LGPD"
                }
            
            # Anonimizar dados pessoais (não excluir completamente por questões de auditoria)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Anonimizar dados pessoais mantendo ID para auditoria
            cursor.execute("""
                UPDATE users SET 
                    username = 'ANONYMIZED_' || id,
                    email = 'anonymized_' || id || '@deleted.local',
                    country = NULL,
                    locale = NULL
                WHERE id = ?
            """, (user_id,))
            
            conn.commit()
            conn.close()
            
            # Log da exclusão
            self.log_audit(
                user_id=user_id,
                action="lgpd_deletion_completed",
                resource="personal_data",
                details={
                    "request_id": request_id,
                    "anonymization_applied": True,
                    "lgpd_compliant": True
                },
                success=True
            )
            
            return {
                "success": True,
                "request_id": request_id,
                "anonymization_applied": True,
                "message": "Dados anonimizados conforme art. 16 da LGPD"
            }
            
        except Exception as e:
            logger.error(f"Erro no processamento de exclusão LGPD: {e}")
            return {"error": str(e)}
    
    def _process_lgpd_portability_request(self, user_id: str, request_id: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Processa solicitação de portabilidade dos dados (art. 18 da LGPD)"""
        try:
            # Obter dados do usuário em formato estruturado
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, username, email, created_at, last_login, country, locale
                FROM users WHERE id = ?
            """, (user_id,))
            
            user_data = cursor.fetchone()
            conn.close()
            
            if not user_data:
                return {"error": "Usuário não encontrado"}
            
            # Preparar dados em formato portável (JSON estruturado)
            portable_data = {
                "user_profile": {
                    "id": user_data[0],
                    "username": user_data[1],
                    "email": user_data[2],
                    "created_at": user_data[3],
                    "last_login": user_data[4],
                    "country": user_data[5],
                    "locale": user_data[6]
                },
                "data_categories": ["identification", "contact", "usage"],
                "export_format": "JSON",
                "export_timestamp": time.time(),
                "lgpd_compliant": True
            }
            
            # Log da portabilidade
            self.log_audit(
                user_id=user_id,
                action="lgpd_portability_completed",
                resource="personal_data",
                details={
                    "request_id": request_id,
                    "data_exported": True,
                    "format": "JSON",
                    "lgpd_compliant": True
                },
                success=True
            )
            
            return {
                "success": True,
                "request_id": request_id,
                "portable_data": portable_data,
                "message": "Dados exportados conforme art. 18 da LGPD"
            }
            
        except Exception as e:
            logger.error(f"Erro no processamento de portabilidade LGPD: {e}")
            return {"error": str(e)}
    
    def _process_lgpd_opposition_request(self, user_id: str, request_id: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Processa solicitação de oposição ao tratamento (art. 18 da LGPD)"""
        try:
            # Verificar base legal do tratamento
            legal_basis = details.get("legal_basis")
            
            if legal_basis in ["legal_obligation", "public_interest"]:
                return {
                    "success": False,
                    "request_id": request_id,
                    "reason": "Oposição não aplicável devido à base legal",
                    "legal_basis": legal_basis,
                    "message": "Tratamento mantido conforme art. 18 da LGPD"
                }
            
            # Registrar oposição no sistema
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Criar tabela de oposições se não existir
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lgpd_oppositions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    legal_basis TEXT,
                    opposition_reason TEXT,
                    created_at REAL,
                    status TEXT DEFAULT 'active'
                )
            """)
            
            # Registrar oposição
            cursor.execute("""
                INSERT INTO lgpd_oppositions 
                (id, user_id, legal_basis, opposition_reason, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                request_id,
                user_id,
                legal_basis,
                details.get("opposition_reason", "User request"),
                time.time()
            ))
            
            conn.commit()
            conn.close()
            
            # Log da oposição
            self.log_audit(
                user_id=user_id,
                action="lgpd_opposition_registered",
                resource="personal_data",
                details={
                    "request_id": request_id,
                    "legal_basis": legal_basis,
                    "opposition_reason": details.get("opposition_reason"),
                    "lgpd_compliant": True
                },
                success=True
            )
            
            return {
                "success": True,
                "request_id": request_id,
                "opposition_registered": True,
                "message": "Oposição registrada conforme art. 18 da LGPD"
            }
            
        except Exception as e:
            logger.error(f"Erro no processamento de oposição LGPD: {e}")
            return {"error": str(e)}
            
    def create_super_admin(self) -> bool:
        """Cria super admin padrão."""
        try:
            # Verificar se já existe super admin
            existing = self.get_user_by_username("admin")
            if existing:
                logger.info("Super admin já existe")
                return True
                
            # Criar super admin com senha forte
            user = self.create_user(
                username="admin",
                email="admin@coinbalance.com",
                password=secrets.token_urlsafe(16),  # Senha forte gerada
                role=UserRole.SUPER_ADMIN,
                creator_id="system"
            )
            
            if user:
                logger.info("Super admin criado com sucesso")
                return True
            else:
                logger.error("Falha ao criar super admin")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao criar super admin: {e}")
            return False

# Instância global do gerenciador de autenticação
auth_manager = AuthManager()

def get_auth_manager() -> AuthManager:
    """Retorna instância do gerenciador de autenticação."""
    return auth_manager
