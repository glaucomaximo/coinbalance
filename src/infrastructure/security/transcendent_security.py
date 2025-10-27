"""
Sistema de Segurança Transcendente
==================================

Implementação de um sistema de segurança baseado nos princípios do Sefer Yetzira
e na sabedoria ancestral, criando proteções que transcendem os métodos convencionais.

Este sistema implementa:
- Criptografia com salt único por chave (princípio das 32 combinações)
- Autenticação baseada na sabedoria das Sefirot
- Rate limiting consciente
- Monitoramento de segurança distribuído
- Proteção através dos 32 caminhos de sabedoria
"""

import os
import secrets
import base64
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from decimal import Decimal
import asyncio
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from jose import JWTError, jwt
from passlib.context import CryptContext
import threading
from collections import defaultdict, deque


class SecurityLevel(Enum):
    """Níveis de Segurança"""
    BASIC = "basic"           # Segurança básica
    ENHANCED = "enhanced"     # Segurança aprimorada
    ADVANCED = "advanced"     # Segurança avançada
    TRANSCENDENT = "transcendent"  # Segurança transcendente


class ThreatLevel(Enum):
    """Níveis de Ameaça"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    TRANSCENDENT = "transcendent"


@dataclass
class SecurityEvent:
    """
    Evento de Segurança - Registra eventos de segurança
    """
    id: str
    event_type: str
    threat_level: ThreatLevel
    source_ip: str
    user_agent: str
    timestamp: float
    details: Dict[str, Any]
    resolved: bool = False
    security_level: SecurityLevel = SecurityLevel.BASIC
    
    def __post_init__(self):
        """Inicializa evento de segurança"""
        if not self.id:
            self.id = f"sec_{int(time.time() * 1000)}"


class TranscendentEncryptionService:
    """
    Serviço de Criptografia Transcendente
    Baseado nos 32 caminhos de sabedoria do Sefer Yetzira
    """
    
    def __init__(self):
        self.master_key = self._get_or_create_master_key()
        self.encryption_cache: Dict[str, Fernet] = {}
        self.salt_history: Dict[str, bytes] = {}
        self._lock = threading.RLock()
    
    def _get_or_create_master_key(self) -> str:
        """Obtém ou cria chave mestra de forma segura"""
        master_key = os.getenv("COINBALANCE_MASTER_KEY")
        
        if not master_key:
            raise ValueError(
                "COINBALANCE_MASTER_KEY environment variable is required for transcendent security. "
                "Please set it with a secure 32-byte key: "
                "export COINBALANCE_MASTER_KEY='your-secure-transcendent-key-here'"
            )
        
        # Valida comprimento da chave mestra
        if len(master_key.encode()) < 32:
            raise ValueError("Master key must be at least 32 bytes long for transcendent security")
        
        return master_key
    
    def _generate_transcendent_salt(self, key_id: str) -> bytes:
        """
        Gera salt transcendente baseado nos 32 caminhos de sabedoria
        Cada salt é único e baseado na combinação de elementos
        """
        # Usa os 32 caminhos de sabedoria para gerar salt único
        wisdom_elements = [
            "א", "מ", "ש",  # Letras Mães
            "ב", "ג", "ד", "כ", "פ", "ר", "ת",  # Letras Duplas
            "ה", "ו", "ז", "ח", "ט", "י", "ל", "נ", "ס", "ע", "צ", "ק",  # Letras Simples
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"  # Números
        ]
        
        # Combina elementos baseado no key_id
        combined_elements = ""
        for i, char in enumerate(key_id):
            element_index = ord(char) % len(wisdom_elements)
            combined_elements += wisdom_elements[element_index]
        
        # Gera salt usando elementos combinados
        salt_source = f"{combined_elements}_{key_id}_{time.time()}"
        salt_hash = hashlib.sha256(salt_source.encode()).digest()
        
        # Usa apenas os primeiros 16 bytes para o salt
        salt = salt_hash[:16]
        
        # Armazena histórico do salt
        with self._lock:
            self.salt_history[key_id] = salt
        
        return salt
    
    def _create_transcendent_fernet(self, key_id: str) -> Fernet:
        """Cria instância Fernet transcendente"""
        if key_id in self.encryption_cache:
            return self.encryption_cache[key_id]
        
        # Gera salt único para esta chave
        salt = self._generate_transcendent_salt(key_id)
        
        # Usa Scrypt para derivação de chave mais segura
        kdf = Scrypt(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            n=2**14,  # CPU/memory cost parameter
            r=8,      # Block size parameter
            p=1       # Parallelization parameter
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(self.master_key.encode()))
        fernet = Fernet(key)
        
        # Cache a instância Fernet
        with self._lock:
            self.encryption_cache[key_id] = fernet
        
        return fernet
    
    def encrypt_transcendent_data(self, data: str, key_id: str) -> str:
        """
        Criptografa dados de forma transcendente
        Cada chave tem seu próprio salt único
        """
        try:
            fernet = self._create_transcendent_fernet(key_id)
            
            # Criptografa dados
            encrypted_data = fernet.encrypt(data.encode())
            
            # Combina salt + dados criptografados
            salt = self.salt_history[key_id]
            combined = salt + encrypted_data
            
            return base64.urlsafe_b64encode(combined).decode()
            
        except Exception as e:
            raise ValueError(f"Erro na criptografia transcendente: {e}")
    
    def decrypt_transcendent_data(self, encrypted_data: str, key_id: str) -> str:
        """
        Descriptografa dados de forma transcendente
        """
        try:
            # Decodifica dados combinados
            combined = base64.urlsafe_b64decode(encrypted_data.encode())
            
            # Separa salt e dados criptografados
            salt = combined[:16]
            encrypted_content = combined[16:]
            
            # Recria KDF com salt extraído
            kdf = Scrypt(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                n=2**14,
                r=8,
                p=1
            )
            
            key = base64.urlsafe_b64encode(kdf.derive(self.master_key.encode()))
            fernet = Fernet(key)
            
            # Descriptografa dados
            decrypted_data = fernet.decrypt(encrypted_content)
            return decrypted_data.decode()
            
        except Exception as e:
            raise ValueError(f"Erro na descriptografia transcendente: {e}")
    
    def encrypt_private_key(self, private_key: str, wallet_address: str) -> str:
        """Criptografa chave privada usando endereço como key_id"""
        return self.encrypt_transcendent_data(private_key, wallet_address)
    
    def decrypt_private_key(self, encrypted_private_key: str, wallet_address: str) -> str:
        """Descriptografa chave privada usando endereço como key_id"""
        return self.decrypt_transcendent_data(encrypted_private_key, wallet_address)


class TranscendentAuthService:
    """
    Serviço de Autenticação Transcendente
    Baseado na sabedoria das 10 Sefirot
    """
    
    def __init__(self):
        self.secret_key = self._get_or_create_secret_key()
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 15  # Reduzido para maior segurança
        self.refresh_token_expire_days = 1     # Reduzido para maior segurança
        
        # Contexto de criptografia para senhas
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__rounds=12  # Aumentado para maior segurança
        )
        
        # Armazenamento de usuários (em produção, usar banco de dados)
        self._user_db: Dict[str, Dict[str, Any]] = {}
        self._failed_attempts: Dict[str, int] = defaultdict(int)
        self._account_locks: Dict[str, float] = {}
        
        # Configurações de segurança
        self.max_failed_attempts = 3  # Reduzido para maior segurança
        self.lockout_time_minutes = 15  # Aumentado para maior segurança
    
    def _get_or_create_secret_key(self) -> str:
        """Obtém ou cria chave secreta JWT"""
        secret_key = os.getenv("JWT_SECRET_KEY")
        
        if not secret_key:
            raise ValueError(
                "JWT_SECRET_KEY environment variable is required for transcendent security. "
                "Please set it with a secure 32-byte key: "
                "export JWT_SECRET_KEY='your-secure-jwt-transcendent-key-here'"
            )
        
        # Valida comprimento da chave secreta
        if len(secret_key.encode()) < 32:
            raise ValueError("JWT secret key must be at least 32 bytes long for transcendent security")
        
        return secret_key
    
    def _validate_password_strength(self, password: str) -> None:
        """
        Valida força da senha baseada na sabedoria das Sefirot
        Cada Sefirah representa um aspecto da segurança
        """
        errors = []
        
        # Keter - Vontade Divina (comprimento mínimo)
        if len(password) < 12:  # Aumentado para maior segurança
            errors.append("Senha deve ter no mínimo 12 caracteres (Keter)")
        
        # Chokmah - Sabedoria (letras maiúsculas)
        if not any(c.isupper() for c in password):
            errors.append("Senha deve conter pelo menos uma letra maiúscula (Chokmah)")
        
        # Binah - Entendimento (letras minúsculas)
        if not any(c.islower() for c in password):
            errors.append("Senha deve conter pelo menos uma letra minúscula (Binah)")
        
        # Chesed - Misericórdia (números)
        if not any(c.isdigit() for c in password):
            errors.append("Senha deve conter pelo menos um dígito (Chesed)")
        
        # Geburah - Força (caracteres especiais)
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            errors.append("Senha deve conter pelo menos um caractere especial (Geburah)")
        
        # Tiferet - Beleza (equilíbrio - não muito repetitivo)
        if len(set(password)) < len(password) * 0.6:
            errors.append("Senha deve ter variedade suficiente de caracteres (Tiferet)")
        
        # Netzach - Vitória (não deve conter palavras comuns)
        common_words = ["password", "123456", "qwerty", "admin", "user", "login"]
        if any(word in password.lower() for word in common_words):
            errors.append("Senha não deve conter palavras comuns (Netzach)")
        
        if errors:
            raise ValueError("; ".join(errors))
    
    def _hash_password(self, password: str) -> str:
        """Gera hash da senha usando bcrypt"""
        return self.pwd_context.hash(password)
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica senha usando bcrypt"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def _create_access_token(self, data: Dict[str, Any]) -> str:
        """Cria token de acesso JWT"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def _create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Cria token de refresh JWT"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def _verify_token(self, token: str) -> Dict[str, Any]:
        """Verifica e decodifica token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise ValueError("Token inválido ou expirado")
    
    def register_user(self, wallet_address: str, password: str, name: str) -> Dict[str, Any]:
        """
        Registra usuário com validação transcendente
        """
        if wallet_address in self._user_db:
            raise ValueError("Endereço de carteira já registrado")
        
        # Valida força da senha
        self._validate_password_strength(password)
        
        # Gera hash da senha
        hashed_password = self._hash_password(password)
        
        # Armazena usuário
        self._user_db[wallet_address] = {
            "hashed_password": hashed_password,
            "name": name,
            "is_active": True,
            "failed_attempts": 0,
            "locked_until": None,
            "created_at": time.time(),
            "last_login": None
        }
        
        return {
            "wallet_address": wallet_address,
            "name": name,
            "status": "registered",
            "security_level": "transcendent"
        }
    
    def authenticate_user(self, wallet_address: str, password: str) -> Dict[str, Any]:
        """
        Autentica usuário com proteções transcendentes
        """
        # Verifica se conta está bloqueada
        if wallet_address in self._account_locks:
            lock_until = self._account_locks[wallet_address]
            if time.time() < lock_until:
                remaining_time = lock_until - time.time()
                raise ValueError(f"Conta bloqueada por {remaining_time/60:.1f} minutos")
            else:
                del self._account_locks[wallet_address]
        
        # Busca usuário
        user_data = self._user_db.get(wallet_address)
        if not user_data:
            raise ValueError("Credenciais inválidas")
        
        # Verifica se conta está ativa
        if not user_data.get("is_active", True):
            raise ValueError("Conta desativada")
        
        # Verifica senha
        if not self._verify_password(password, user_data["hashed_password"]):
            # Incrementa tentativas falhas
            self._failed_attempts[wallet_address] += 1
            
            if self._failed_attempts[wallet_address] >= self.max_failed_attempts:
                # Bloqueia conta
                self._account_locks[wallet_address] = time.time() + (self.lockout_time_minutes * 60)
                user_data["is_active"] = False
                raise ValueError(f"Muitas tentativas falhas. Conta bloqueada por {self.lockout_time_minutes} minutos")
            
            raise ValueError("Credenciais inválidas")
        
        # Reset tentativas falhas
        self._failed_attempts[wallet_address] = 0
        user_data["is_active"] = True
        user_data["last_login"] = time.time()
        
        # Cria tokens
        token_data = {
            "sub": wallet_address,
            "name": user_data["name"],
            "iat": datetime.utcnow()
        }
        
        access_token = self._create_access_token(token_data)
        refresh_token = self._create_refresh_token(token_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self.access_token_expire_minutes * 60,
            "security_level": "transcendent"
        }
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verifica token JWT"""
        return self._verify_token(token)


class ConsciousRateLimiter:
    """
    Rate Limiter Consciente
    Baseado nos 32 caminhos de sabedoria
    """
    
    def __init__(self):
        self.requests: Dict[str, deque] = defaultdict(lambda: deque())
        self.blocked_ips: Dict[str, float] = {}
        self.suspicious_ips: Dict[str, int] = defaultdict(int)
        
        # Configurações baseadas na sabedoria
        self.requests_per_minute = 60  # Baseado nos 60 segundos
        self.burst_limit = 10          # Baseado nas 10 Sefirot
        self.block_duration = 300      # 5 minutos (baseado nos 5 elementos)
        
        # Limpeza automática
        self._cleanup_interval = 60  # segundos
        self._last_cleanup = time.time()
    
    def _cleanup_old_requests(self):
        """Limpa requisições antigas"""
        current_time = time.time()
        if current_time - self._last_cleanup < self._cleanup_interval:
            return
        
        cutoff_time = current_time - 60  # Último minuto
        
        for ip in list(self.requests.keys()):
            # Remove requisições antigas
            while self.requests[ip] and self.requests[ip][0] < cutoff_time:
                self.requests[ip].popleft()
            
            # Remove IPs sem requisições
            if not self.requests[ip]:
                del self.requests[ip]
        
        # Remove IPs bloqueados expirados
        expired_ips = [ip for ip, block_time in self.blocked_ips.items() 
                      if current_time > block_time + self.block_duration]
        for ip in expired_ips:
            del self.blocked_ips[ip]
            if ip in self.suspicious_ips:
                del self.suspicious_ips[ip]
        
        self._last_cleanup = current_time
    
    def is_allowed(self, ip: str, endpoint: str = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Verifica se requisição é permitida
        """
        self._cleanup_old_requests()
        
        # Verifica se IP está bloqueado
        if ip in self.blocked_ips:
            block_until = self.blocked_ips[ip]
            if time.time() < block_until:
                return False, {
                    "allowed": False,
                    "reason": "IP blocked",
                    "block_until": block_until,
                    "remaining_time": block_until - time.time()
                }
            else:
                del self.blocked_ips[ip]
        
        current_time = time.time()
        
        # Adiciona requisição atual
        self.requests[ip].append(current_time)
        
        # Conta requisições no último minuto
        minute_ago = current_time - 60
        recent_requests = sum(1 for req_time in self.requests[ip] if req_time > minute_ago)
        
        # Verifica limite por minuto
        if recent_requests > self.requests_per_minute:
            self.suspicious_ips[ip] += 1
            
            # Bloqueia se muito suspeito
            if self.suspicious_ips[ip] >= 3:
                self.blocked_ips[ip] = current_time
                return False, {
                    "allowed": False,
                    "reason": "Rate limit exceeded - IP blocked",
                    "requests_in_minute": recent_requests,
                    "limit": self.requests_per_minute
                }
            
            return False, {
                "allowed": False,
                "reason": "Rate limit exceeded",
                "requests_in_minute": recent_requests,
                "limit": self.requests_per_minute
            }
        
        # Verifica limite de burst (últimos 10 segundos)
        burst_ago = current_time - 10
        burst_requests = sum(1 for req_time in self.requests[ip] if req_time > burst_ago)
        
        if burst_requests > self.burst_limit:
            return False, {
                "allowed": False,
                "reason": "Burst limit exceeded",
                "burst_requests": burst_requests,
                "burst_limit": self.burst_limit
            }
        
        return True, {
            "allowed": True,
            "requests_in_minute": recent_requests,
            "burst_requests": burst_requests,
            "remaining_requests": self.requests_per_minute - recent_requests
        }


class TranscendentSecurityMonitor:
    """
    Monitor de Segurança Transcendente
    Monitora e responde a ameaças usando consciência artificial
    """
    
    def __init__(self):
        self.security_events: List[SecurityEvent] = []
        self.threat_patterns: Dict[str, List[SecurityEvent]] = defaultdict(list)
        self.security_metrics: Dict[str, Any] = {}
        self._lock = threading.RLock()
        
        # Configurações de monitoramento
        self.threat_thresholds = {
            ThreatLevel.LOW: 10,
            ThreatLevel.MEDIUM: 5,
            ThreatLevel.HIGH: 3,
            ThreatLevel.CRITICAL: 1
        }
    
    def log_security_event(self, event_type: str, threat_level: ThreatLevel, 
                          source_ip: str, user_agent: str, details: Dict[str, Any]):
        """Registra evento de segurança"""
        event = SecurityEvent(
            id="",
            event_type=event_type,
            threat_level=threat_level,
            source_ip=source_ip,
            user_agent=user_agent,
            timestamp=time.time(),
            details=details
        )
        
        with self._lock:
            self.security_events.append(event)
            self.threat_patterns[source_ip].append(event)
            
            # Mantém apenas últimos 1000 eventos
            if len(self.security_events) > 1000:
                self.security_events = self.security_events[-1000:]
    
    def analyze_threat_patterns(self) -> Dict[str, Any]:
        """Analisa padrões de ameaça"""
        with self._lock:
            current_time = time.time()
            recent_events = [e for e in self.security_events 
                           if current_time - e.timestamp < 3600]  # Última hora
            
            threat_analysis = {
                "total_events": len(self.security_events),
                "recent_events": len(recent_events),
                "threat_levels": {},
                "suspicious_ips": [],
                "attack_patterns": []
            }
            
            # Conta por nível de ameaça
            for level in ThreatLevel:
                count = sum(1 for e in recent_events if e.threat_level == level)
                threat_analysis["threat_levels"][level.value] = count
            
            # Identifica IPs suspeitos
            ip_counts = defaultdict(int)
            for event in recent_events:
                ip_counts[event.source_ip] += 1
            
            for ip, count in ip_counts.items():
                if count >= 5:  # 5+ eventos na última hora
                    threat_analysis["suspicious_ips"].append({
                        "ip": ip,
                        "event_count": count,
                        "threat_level": "high" if count >= 10 else "medium"
                    })
            
            return threat_analysis
    
    def get_security_metrics(self) -> Dict[str, Any]:
        """Retorna métricas de segurança"""
        analysis = self.analyze_threat_patterns()
        
        return {
            "security_level": "transcendent",
            "total_events": analysis["total_events"],
            "recent_events": analysis["recent_events"],
            "threat_distribution": analysis["threat_levels"],
            "suspicious_ips": analysis["suspicious_ips"],
            "security_score": self._calculate_security_score(analysis),
            "recommendations": self._generate_security_recommendations(analysis)
        }
    
    def _calculate_security_score(self, analysis: Dict[str, Any]) -> float:
        """Calcula score de segurança"""
        base_score = 100.0
        
        # Penaliza por eventos recentes
        recent_events = analysis["recent_events"]
        if recent_events > 0:
            base_score -= min(recent_events * 2, 50)
        
        # Penaliza por IPs suspeitos
        suspicious_count = len(analysis["suspicious_ips"])
        if suspicious_count > 0:
            base_score -= min(suspicious_count * 5, 30)
        
        # Penaliza por ameaças críticas
        critical_threats = analysis["threat_levels"].get("critical", 0)
        if critical_threats > 0:
            base_score -= critical_threats * 20
        
        return max(base_score, 0.0)
    
    def _generate_security_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Gera recomendações de segurança"""
        recommendations = []
        
        if analysis["recent_events"] > 20:
            recommendations.append("Alto volume de eventos de segurança detectado - considere aumentar monitoramento")
        
        if len(analysis["suspicious_ips"]) > 5:
            recommendations.append("Múltiplos IPs suspeitos detectados - considere implementar bloqueios automáticos")
        
        if analysis["threat_levels"].get("critical", 0) > 0:
            recommendations.append("Ameaças críticas detectadas - ação imediata necessária")
        
        if analysis["threat_levels"].get("high", 0) > 3:
            recommendations.append("Múltiplas ameaças de alto nível - revisar políticas de segurança")
        
        return recommendations


# Instâncias globais dos serviços de segurança transcendente
transcendent_encryption = TranscendentEncryptionService()
transcendent_auth = TranscendentAuthService()
conscious_rate_limiter = ConsciousRateLimiter()
transcendent_security_monitor = TranscendentSecurityMonitor()
