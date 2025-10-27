"""
Sistema de Logs Estruturados (JSON) para CoinBalance
"""
import json
import logging
import time
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import Request
from contextvars import ContextVar

# Context variables para rastreamento de requisições
request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar('user_id', default=None)
wallet_address_var: ContextVar[Optional[str]] = ContextVar('wallet_address', default=None)

class StructuredFormatter(logging.Formatter):
    """Formatter para logs estruturados em JSON"""
    
    def __init__(self):
        super().__init__()
    
    def format(self, record: logging.LogRecord) -> str:
        """Formata o log em JSON estruturado"""
        try:
            # Dados básicos do log
            log_data = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
            }
            
            # Adicionar request_id se disponível
            request_id = request_id_var.get()
            if request_id:
                log_data["request_id"] = request_id
            
            # Adicionar user_id se disponível
            user_id = user_id_var.get()
            if user_id:
                log_data["user_id"] = user_id
            
            # Adicionar wallet_address se disponível
            wallet_address = wallet_address_var.get()
            if wallet_address:
                log_data["wallet_address"] = wallet_address
            
            # Adicionar dados extras se existirem
            if hasattr(record, 'extra_data'):
                log_data.update(record.extra_data)
            
            # Adicionar exceção se existir
            if record.exc_info:
                log_data["exception"] = {
                    "type": record.exc_info[0].__name__,
                    "message": str(record.exc_info[1]),
                    "traceback": self.formatException(record.exc_info)
                }
            
            # Adicionar dados de performance se disponíveis
            if hasattr(record, 'duration'):
                log_data["duration_ms"] = record.duration
            
            if hasattr(record, 'memory_usage'):
                log_data["memory_usage_mb"] = record.memory_usage
            
            return json.dumps(log_data, ensure_ascii=False, default=str)
            
        except Exception as e:
            # Fallback para formato simples em caso de erro
            return f"ERROR formatting log: {e} | {record.getMessage()}"

class StructuredLogger:
    """Logger estruturado para CoinBalance"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Remover handlers existentes
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Adicionar handler com formatter estruturado
        handler = logging.StreamHandler()
        handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(handler)
    
    def _log_with_context(self, level: int, message: str, extra_data: Optional[Dict[str, Any]] = None, **kwargs):
        """Log com contexto estruturado"""
        if extra_data is None:
            extra_data = {}
        
        # Adicionar dados extras ao record
        extra_data.update(kwargs)
        
        # Criar record com dados extras
        record = self.logger.makeRecord(
            self.logger.name, level, "", 0, message, (), None
        )
        record.extra_data = extra_data
        
        self.logger.handle(record)
    
    def info(self, message: str, **kwargs):
        """Log de informação"""
        self._log_with_context(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log de aviso"""
        self._log_with_context(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log de erro"""
        self._log_with_context(logging.ERROR, message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log de debug"""
        self._log_with_context(logging.DEBUG, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log crítico"""
        self._log_with_context(logging.CRITICAL, message, **kwargs)

# Loggers estruturados para diferentes módulos
def get_structured_logger(name: str) -> StructuredLogger:
    """Obtém um logger estruturado"""
    return StructuredLogger(name)

# Loggers específicos
api_logger = get_structured_logger("coinbalance.api")
auth_logger = get_structured_logger("coinbalance.auth")
wallet_logger = get_structured_logger("coinbalance.wallet")
transfer_logger = get_structured_logger("coinbalance.transfer")
security_logger = get_structured_logger("coinbalance.security")
performance_logger = get_structured_logger("coinbalance.performance")

class RequestContextMiddleware:
    """Middleware para adicionar contexto às requisições"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Gerar request_id único
            request_id = str(uuid.uuid4())
            request_id_var.set(request_id)
            
            # Extrair informações da requisição
            request = Request(scope, receive)
            
            # Log da requisição
            api_logger.info(
                "Request started",
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                client_ip=request.client.host if request.client else "unknown",
                user_agent=request.headers.get("user-agent", "unknown")
            )
            
            # Processar requisição
            start_time = time.time()
            
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    # Calcular duração
                    duration = (time.time() - start_time) * 1000  # em ms
                    
                    # Log da resposta
                    api_logger.info(
                        "Request completed",
                        request_id=request_id,
                        status_code=message["status"],
                        duration_ms=duration,
                        method=request.method,
                        url=str(request.url)
                    )
                
                await send(message)
            
            await self.app(scope, receive, send_wrapper)
            
            # Limpar contexto
            request_id_var.set(None)
        else:
            await self.app(scope, receive, send)

# Funções utilitárias para logging estruturado
def log_wallet_operation(operation: str, wallet_address: str, amount: Optional[float] = None, **kwargs):
    """Log de operação de carteira"""
    wallet_logger.info(
        f"Wallet {operation}",
        operation=operation,
        wallet_address=wallet_address,
        amount=amount,
        **kwargs
    )

def log_transfer_operation(from_address: str, to_address: str, amount: float, fee: float, **kwargs):
    """Log de operação de transferência"""
    transfer_logger.info(
        "Transfer operation",
        from_address=from_address,
        to_address=to_address,
        amount=amount,
        fee=fee,
        total_amount=amount + fee,
        **kwargs
    )

def log_auth_event(event: str, user_id: Optional[str] = None, ip: Optional[str] = None, **kwargs):
    """Log de evento de autenticação"""
    auth_logger.info(
        f"Auth {event}",
        event=event,
        user_id=user_id,
        client_ip=ip,
        **kwargs
    )

def log_security_event(event: str, severity: str = "medium", **kwargs):
    """Log de evento de segurança"""
    security_logger.warning(
        f"Security {event}",
        event=event,
        severity=severity,
        **kwargs
    )

def log_performance_metric(metric: str, value: float, unit: str = "ms", **kwargs):
    """Log de métrica de performance"""
    performance_logger.info(
        f"Performance {metric}",
        metric=metric,
        value=value,
        unit=unit,
        **kwargs
    )

# Configuração global de logging estruturado
def setup_structured_logging():
    """Configura logging estruturado globalmente"""
    # Configurar root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remover handlers existentes
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Adicionar handler estruturado
    handler = logging.StreamHandler()
    handler.setFormatter(StructuredFormatter())
    root_logger.addHandler(handler)
    
    # Configurar loggers específicos
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
