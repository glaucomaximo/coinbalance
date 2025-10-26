"""
Sistema de Rate Limiting - CoinBalance
Implementa limitação de taxa para prevenir abuso e ataques
"""

import time
import asyncio
from typing import Dict, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
import logging
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

class RateLimitType(Enum):
    """Tipos de rate limiting"""
    GLOBAL = "global"
    PER_IP = "per_ip"
    PER_USER = "per_user"
    PER_ENDPOINT = "per_endpoint"

@dataclass
class RateLimitConfig:
    """Configuração de rate limiting"""
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    requests_per_day: int = 10000
    burst_limit: int = 10
    window_size: int = 60  # segundos

class RateLimiter:
    """Implementa rate limiting com múltiplas estratégias"""
    
    def __init__(self):
        self.rate_limits = defaultdict(lambda: defaultdict(deque))
        self.blocked_ips = set()
        self.suspicious_ips = set()
        self.config = RateLimitConfig()
        
        # Configurações específicas por endpoint
        self.endpoint_configs = {
            "/carteiras/criar": RateLimitConfig(5, 50, 500, 2),
            "/transacoes/criar": RateLimitConfig(30, 500, 5000, 5),
            "/defi/stake": RateLimitConfig(10, 100, 1000, 3),
            "/defi/borrow": RateLimitConfig(5, 50, 500, 2),
            "/": RateLimitConfig(120, 2000, 20000, 20)
        }
    
    def is_allowed(self, 
                   identifier: str, 
                   endpoint: str = "/",
                   rate_type: RateLimitType = RateLimitType.PER_IP) -> Tuple[bool, Dict]:
        """Verifica se requisição é permitida"""
        
        # Verificar se IP está bloqueado
        if identifier in self.blocked_ips:
            return False, {
                "error": "IP bloqueado permanentemente",
                "retry_after": None,
                "reason": "blocked"
            }
        
        # Obter configuração do endpoint
        config = self.endpoint_configs.get(endpoint, self.config)
        
        # Verificar diferentes tipos de rate limiting
        if rate_type == RateLimitType.PER_IP:
            return self._check_ip_rate_limit(identifier, config)
        elif rate_type == RateLimitType.PER_USER:
            return self._check_user_rate_limit(identifier, config)
        elif rate_type == RateLimitType.PER_ENDPOINT:
            return self._check_endpoint_rate_limit(identifier, endpoint, config)
        else:
            return self._check_global_rate_limit(identifier, config)
    
    def _check_ip_rate_limit(self, ip: str, config: RateLimitConfig) -> Tuple[bool, Dict]:
        """Verifica rate limiting por IP"""
        current_time = time.time()
        
        # Limpar requisições antigas
        self._clean_old_requests(ip, current_time, config.window_size)
        
        # Verificar limites
        requests = self.rate_limits["ip"][ip]
        
        # Verificar burst limit (últimos 10 segundos)
        recent_requests = [req_time for req_time in requests if current_time - req_time < 10]
        if len(recent_requests) >= config.burst_limit:
            self._mark_suspicious(ip)
            return False, {
                "error": "Muitas requisições em pouco tempo",
                "retry_after": 10,
                "reason": "burst_limit"
            }
        
        # Verificar limite por minuto
        minute_requests = [req_time for req_time in requests if current_time - req_time < 60]
        if len(minute_requests) >= config.requests_per_minute:
            return False, {
                "error": "Limite de requisições por minuto excedido",
                "retry_after": 60 - (current_time - minute_requests[0]),
                "reason": "minute_limit"
            }
        
        # Verificar limite por hora
        hour_requests = [req_time for req_time in requests if current_time - req_time < 3600]
        if len(hour_requests) >= config.requests_per_hour:
            return False, {
                "error": "Limite de requisições por hora excedido",
                "retry_after": 3600 - (current_time - hour_requests[0]),
                "reason": "hour_limit"
            }
        
        # Verificar limite por dia
        day_requests = [req_time for req_time in requests if current_time - req_time < 86400]
        if len(day_requests) >= config.requests_per_day:
            return False, {
                "error": "Limite de requisições por dia excedido",
                "retry_after": 86400 - (current_time - day_requests[0]),
                "reason": "day_limit"
            }
        
        # Adicionar requisição atual
        requests.append(current_time)
        
        return True, {
            "remaining": config.requests_per_minute - len(minute_requests) - 1,
            "reset_time": current_time + 60
        }
    
    def _check_user_rate_limit(self, user_id: str, config: RateLimitConfig) -> Tuple[bool, Dict]:
        """Verifica rate limiting por usuário"""
        # Implementação similar ao IP, mas por usuário
        return self._check_generic_rate_limit("user", user_id, config)
    
    def _check_endpoint_rate_limit(self, identifier: str, endpoint: str, config: RateLimitConfig) -> Tuple[bool, Dict]:
        """Verifica rate limiting por endpoint"""
        key = f"{identifier}:{endpoint}"
        return self._check_generic_rate_limit("endpoint", key, config)
    
    def _check_global_rate_limit(self, identifier: str, config: RateLimitConfig) -> Tuple[bool, Dict]:
        """Verifica rate limiting global"""
        return self._check_generic_rate_limit("global", identifier, config)
    
    def _check_generic_rate_limit(self, rate_type: str, identifier: str, config: RateLimitConfig) -> Tuple[bool, Dict]:
        """Implementação genérica de rate limiting"""
        current_time = time.time()
        
        # Limpar requisições antigas
        self._clean_old_requests(f"{rate_type}:{identifier}", current_time, config.window_size)
        
        # Verificar limites
        requests = self.rate_limits[rate_type][identifier]
        
        # Verificar burst limit
        recent_requests = [req_time for req_time in requests if current_time - req_time < 10]
        if len(recent_requests) >= config.burst_limit:
            return False, {
                "error": "Muitas requisições em pouco tempo",
                "retry_after": 10,
                "reason": "burst_limit"
            }
        
        # Verificar limite por minuto
        minute_requests = [req_time for req_time in requests if current_time - req_time < 60]
        if len(minute_requests) >= config.requests_per_minute:
            return False, {
                "error": "Limite de requisições por minuto excedido",
                "retry_after": 60 - (current_time - minute_requests[0]),
                "reason": "minute_limit"
            }
        
        # Adicionar requisição atual
        requests.append(current_time)
        
        return True, {
            "remaining": config.requests_per_minute - len(minute_requests) - 1,
            "reset_time": current_time + 60
        }
    
    def _clean_old_requests(self, key: str, current_time: float, window_size: int):
        """Remove requisições antigas"""
        if key in self.rate_limits:
            # Manter apenas requisições dentro da janela
            cutoff_time = current_time - window_size
            self.rate_limits[key] = deque([
                req_time for req_time in self.rate_limits[key] 
                if req_time > cutoff_time
            ])
    
    def _mark_suspicious(self, ip: str):
        """Marca IP como suspeito"""
        self.suspicious_ips.add(ip)
        logger.warning(f"IP suspeito detectado: {ip}")
        
        # Se muito suspeito, bloquear temporariamente
        if ip in self.suspicious_ips and len(self.suspicious_ips) > 5:
            self.blocked_ips.add(ip)
            logger.critical(f"IP bloqueado: {ip}")
    
    def block_ip(self, ip: str, reason: str = "Manual block"):
        """Bloqueia IP permanentemente"""
        self.blocked_ips.add(ip)
        logger.critical(f"IP bloqueado manualmente: {ip} - {reason}")
    
    def unblock_ip(self, ip: str):
        """Desbloqueia IP"""
        self.blocked_ips.discard(ip)
        self.suspicious_ips.discard(ip)
        logger.info(f"IP desbloqueado: {ip}")
    
    def get_rate_limit_stats(self) -> Dict:
        """Retorna estatísticas de rate limiting"""
        return {
            "blocked_ips": len(self.blocked_ips),
            "suspicious_ips": len(self.suspicious_ips),
            "active_limits": {
                rate_type: len(identifiers) 
                for rate_type, identifiers in self.rate_limits.items()
            },
            "config": {
                "default": {
                    "requests_per_minute": self.config.requests_per_minute,
                    "burst_limit": self.config.burst_limit
                },
                "endpoints": {
                    endpoint: {
                        "requests_per_minute": config.requests_per_minute,
                        "burst_limit": config.burst_limit
                    }
                    for endpoint, config in self.endpoint_configs.items()
                }
            }
        }

# Instância global do rate limiter
rate_limiter = RateLimiter()

# Middleware para FastAPI
async def rate_limit_middleware(request, call_next):
    """Middleware de rate limiting para FastAPI"""
    client_ip = request.client.host if request.client else "unknown"
    endpoint = request.url.path
    
    # Verificar rate limiting
    allowed, info = rate_limiter.is_allowed(
        identifier=client_ip,
        endpoint=endpoint,
        rate_type=RateLimitType.PER_IP
    )
    
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={
                "error": True,
                "message": info["error"],
                "retry_after": info.get("retry_after"),
                "reason": info.get("reason")
            },
            headers={
                "Retry-After": str(int(info.get("retry_after", 60)))
            }
        )
    
    # Adicionar headers de rate limiting
    response = await call_next(request)
    response.headers["X-RateLimit-Remaining"] = str(info.get("remaining", 0))
    response.headers["X-RateLimit-Reset"] = str(int(info.get("reset_time", 0)))
    
    return response
