"""
Sistema de Rate Limiting Avançado para CoinBalance
"""
import time
import asyncio
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class RateLimitScope(Enum):
    """Escopo do rate limiting"""
    IP = "ip"
    USER = "user"
    GLOBAL = "global"

@dataclass
class RateLimitConfig:
    """Configuração de rate limiting para um endpoint"""
    requests_per_minute: int
    requests_per_hour: int
    requests_per_day: int
    burst_limit: int = 50  # Limite de rajada aumentado para testes
    scope: RateLimitScope = RateLimitScope.IP
    
    def __post_init__(self):
        """Validação da configuração"""
        if self.requests_per_minute <= 0:
            raise ValueError("requests_per_minute must be positive")
        if self.requests_per_hour <= 0:
            raise ValueError("requests_per_hour must be positive")
        if self.requests_per_day <= 0:
            raise ValueError("requests_per_day must be positive")

@dataclass
class RateLimitEntry:
    """Entrada de rate limiting"""
    requests: list[float] = field(default_factory=list)
    last_reset: float = field(default_factory=time.time)
    
    def add_request(self) -> None:
        """Adiciona uma requisição"""
        current_time = time.time()
        self.requests.append(current_time)
        
        # Limpar requisições antigas (mais de 24 horas)
        cutoff_time = current_time - 86400  # 24 horas
        self.requests = [req for req in self.requests if req > cutoff_time]
    
    def get_request_count(self, window_seconds: int) -> int:
        """Retorna o número de requisições em uma janela de tempo"""
        current_time = time.time()
        cutoff_time = current_time - window_seconds
        return len([req for req in self.requests if req > cutoff_time])
    
    def is_rate_limited(self, config: RateLimitConfig) -> Tuple[bool, str, int]:
        """
        Verifica se está limitado pelo rate limit
        
        Returns:
            Tuple[bool, str, int]: (is_limited, reason, retry_after)
        """
        current_time = time.time()
        
        # Verificar limite por minuto
        minute_count = self.get_request_count(60)
        if minute_count >= config.requests_per_minute:
            return True, "Rate limit exceeded: too many requests per minute", 60
        
        # Verificar limite por hora
        hour_count = self.get_request_count(3600)
        if hour_count >= config.requests_per_hour:
            return True, "Rate limit exceeded: too many requests per hour", 3600
        
        # Verificar limite por dia
        day_count = self.get_request_count(86400)
        if day_count >= config.requests_per_day:
            return True, "Rate limit exceeded: too many requests per day", 86400
        
        # Verificar limite de rajada (últimos 10 segundos)
        burst_count = self.get_request_count(10)
        if burst_count >= config.burst_limit:
            return True, "Rate limit exceeded: burst limit", 10
        
        return False, "", 0

class AdvancedRateLimiter:
    """Rate limiter avançado com múltiplas configurações"""
    
    def __init__(self):
        self._entries: Dict[str, RateLimitEntry] = {}
        self._configs: Dict[str, RateLimitConfig] = {}
        self._cleanup_interval = 300  # 5 minutos
        self._last_cleanup = time.time()
        
        # Configurações padrão por endpoint
        self._setup_default_configs()
    
    def _setup_default_configs(self) -> None:
        """Configura configurações padrão"""
        # Configurações por endpoint
        self._configs = {
            # Autenticação - mais restritivo
            "/api/v1/auth/login": RateLimitConfig(
                requests_per_minute=5,
                requests_per_hour=20,
                requests_per_day=100,
                burst_limit=3,
                scope=RateLimitScope.IP
            ),
            "/api/v1/auth/refresh": RateLimitConfig(
                requests_per_minute=10,
                requests_per_hour=50,
                requests_per_day=200,
                burst_limit=5,
                scope=RateLimitScope.USER
            ),
            
            # Carteiras - moderado
            "/api/v1/carteiras/": RateLimitConfig(
                requests_per_minute=30,
                requests_per_hour=200,
                requests_per_day=1000,
                burst_limit=10,
                scope=RateLimitScope.USER
            ),
            
            # Transferências - mais restritivo
            "/api/v1/transferencias/": RateLimitConfig(
                requests_per_minute=10,
                requests_per_hour=50,
                requests_per_day=200,
                burst_limit=5,
                scope=RateLimitScope.USER
            ),
            
            # Operações de carteira - moderado
            "/api/v1/carteiras/{address}/credit": RateLimitConfig(
                requests_per_minute=20,
                requests_per_hour=100,
                requests_per_day=500,
                burst_limit=8,
                scope=RateLimitScope.USER
            ),
            "/api/v1/carteiras/{address}/debit": RateLimitConfig(
                requests_per_minute=20,
                requests_per_hour=100,
                requests_per_day=500,
                burst_limit=8,
                scope=RateLimitScope.USER
            ),
            
            # Health check - mais permissivo
            "/health": RateLimitConfig(
                requests_per_minute=60,
                requests_per_hour=1000,
                requests_per_day=10000,
                burst_limit=20,
                scope=RateLimitScope.IP
            ),
            
            # Padrão para outros endpoints
            "default": RateLimitConfig(
                requests_per_minute=60,
                requests_per_hour=500,
                requests_per_day=2000,
                burst_limit=15,
                scope=RateLimitScope.IP
            )
        }
    
    def _get_config_for_path(self, path: str) -> RateLimitConfig:
        """Obtém configuração para um caminho específico"""
        # Buscar configuração exata
        if path in self._configs:
            return self._configs[path]
        
        # Buscar por padrão (ex: /api/v1/carteiras/{address}/credit)
        for config_path, config in self._configs.items():
            if config_path != "default" and self._path_matches(path, config_path):
                return config
        
        # Retornar configuração padrão
        return self._configs["default"]
    
    def _path_matches(self, path: str, pattern: str) -> bool:
        """Verifica se um caminho corresponde a um padrão"""
        if "{" in pattern:
            # Padrão com variáveis (ex: /api/v1/carteiras/{address}/credit)
            path_parts = path.split("/")
            pattern_parts = pattern.split("/")
            
            if len(path_parts) != len(pattern_parts):
                return False
            
            for path_part, pattern_part in zip(path_parts, pattern_parts):
                if not pattern_part.startswith("{") and path_part != pattern_part:
                    return False
            
            return True
        
        return path == pattern
    
    def _get_identifier(self, request: Request, config: RateLimitConfig) -> str:
        """Obtém identificador para rate limiting"""
        if config.scope == RateLimitScope.IP:
            # Usar IP do cliente
            client_ip = request.client.host if request.client else "unknown"
            return f"ip:{client_ip}"
        
        elif config.scope == RateLimitScope.USER:
            # Tentar obter user_id do token JWT
            try:
                auth_header = request.headers.get("Authorization")
                if auth_header and auth_header.startswith("Bearer "):
                    # Em uma implementação real, você decodificaria o JWT aqui
                    # Por enquanto, usar o IP como fallback
                    client_ip = request.client.host if request.client else "unknown"
                    return f"user:{client_ip}"
            except Exception:
                pass
            
            # Fallback para IP
            client_ip = request.client.host if request.client else "unknown"
            return f"user:{client_ip}"
        
        else:  # GLOBAL
            return "global"
    
    def _cleanup_old_entries(self) -> None:
        """Remove entradas antigas para economizar memória"""
        current_time = time.time()
        if current_time - self._last_cleanup < self._cleanup_interval:
            return
        
        # Remover entradas sem atividade há mais de 1 hora
        cutoff_time = current_time - 3600
        keys_to_remove = []
        
        for key, entry in self._entries.items():
            if not entry.requests or max(entry.requests) < cutoff_time:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self._entries[key]
        
        self._last_cleanup = current_time
        logger.debug(f"Rate limiter cleanup: removed {len(keys_to_remove)} old entries")
    
    async def check_rate_limit(self, request: Request) -> Tuple[bool, str, int]:
        """
        Verifica se a requisição está dentro dos limites
        
        Returns:
            Tuple[bool, str, int]: (is_limited, reason, retry_after)
        """
        try:
            # Obter configuração para o endpoint
            config = self._get_config_for_path(request.url.path)
            
            # Obter identificador
            identifier = self._get_identifier(request, config)
            
            # Obter ou criar entrada
            if identifier not in self._entries:
                self._entries[identifier] = RateLimitEntry()
            
            entry = self._entries[identifier]
            
            # Verificar rate limit
            is_limited, reason, retry_after = entry.is_rate_limited(config)
            
            if is_limited:
                logger.warning(f"Rate limit exceeded for {identifier}: {reason}")
                return True, reason, retry_after
            
            # Adicionar requisição
            entry.add_request()
            
            # Cleanup periódico
            self._cleanup_old_entries()
            
            return False, "", 0
            
        except Exception as e:
            logger.error(f"Error in rate limiting: {e}")
            # Em caso de erro, permitir a requisição
            return False, "", 0
    
    def get_rate_limit_headers(self, request: Request) -> Dict[str, str]:
        """Retorna headers de rate limiting"""
        try:
            config = self._get_config_for_path(request.url.path)
            identifier = self._get_identifier(request, config)
            
            if identifier in self._entries:
                entry = self._entries[identifier]
                minute_count = entry.get_request_count(60)
                hour_count = entry.get_request_count(3600)
                day_count = entry.get_request_count(86400)
                
                return {
                    "X-RateLimit-Limit-Minute": str(config.requests_per_minute),
                    "X-RateLimit-Limit-Hour": str(config.requests_per_hour),
                    "X-RateLimit-Limit-Day": str(config.requests_per_day),
                    "X-RateLimit-Remaining-Minute": str(max(0, config.requests_per_minute - minute_count)),
                    "X-RateLimit-Remaining-Hour": str(max(0, config.requests_per_hour - hour_count)),
                    "X-RateLimit-Remaining-Day": str(max(0, config.requests_per_day - day_count)),
                    "X-RateLimit-Reset": str(int(time.time() + 60)),  # Próximo reset em 1 minuto
                }
            
            return {}
            
        except Exception as e:
            logger.error(f"Error generating rate limit headers: {e}")
            return {}

# Instância global do rate limiter
rate_limiter = AdvancedRateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    """Middleware de rate limiting"""
    # Verificar rate limit
    is_limited, reason, retry_after = await rate_limiter.check_rate_limit(request)
    
    if is_limited:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "success": False,
                "error": reason,
                "code": "RATE_LIMIT_EXCEEDED",
                "retry_after": retry_after,
                "timestamp": time.time()
            },
            headers={
                "Retry-After": str(retry_after),
                "X-RateLimit-Limit": "60",
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(int(time.time() + retry_after))
            }
        )
    
    # Processar requisição
    response = await call_next(request)
    
    # Adicionar headers de rate limiting
    rate_limit_headers = rate_limiter.get_rate_limit_headers(request)
    for header, value in rate_limit_headers.items():
        response.headers[header] = value
    
    return response
