"""
Sistema de Logging Estruturado para CoinBalance
===============================================

Implementa logging estruturado com diferentes formatos,
níveis de severidade e integração com monitoramento.
"""

import logging
import json
import sys
import traceback
from typing import Any, Dict, Optional, Union
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from contextvars import ContextVar

# Context variables para rastreamento de requisições
request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar('user_id', default=None)
session_id_var: ContextVar[Optional[str]] = ContextVar('session_id', default=None)

class LogLevel(Enum):
    """Níveis de log"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogCategory(Enum):
    """Categorias de log"""
    AUTHENTICATION = "auth"
    BUSINESS_LOGIC = "business"
    INFRASTRUCTURE = "infrastructure"
    SECURITY = "security"
    PERFORMANCE = "performance"
    EXTERNAL_API = "external_api"
    DATABASE = "database"
    CACHE = "cache"
    BLOCKCHAIN = "blockchain"
    TRANSACTION = "transaction"
    WALLET = "wallet"
    MONITORING = "monitoring"

@dataclass
class LogEntry:
    """Entrada de log estruturada"""
    timestamp: datetime
    level: str
    category: str
    message: str
    module: str
    function: str
    line_number: int
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None
    exception_info: Optional[str] = None
    duration_ms: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data

class StructuredFormatter(logging.Formatter):
    """Formatador estruturado para logs"""
    
    def __init__(self, format_type: str = "json"):
        self.format_type = format_type
        super().__init__()
    
    def format(self, record: logging.LogRecord) -> str:
        """Formata registro de log"""
        # Obter informações do contexto
        request_id = request_id_var.get()
        user_id = user_id_var.get()
        session_id = session_id_var.get()
        
        # Criar entrada estruturada
        log_entry = LogEntry(
            timestamp=datetime.fromtimestamp(record.created),
            level=record.levelname,
            category=getattr(record, 'category', 'general'),
            message=record.getMessage(),
            module=record.module,
            function=record.funcName,
            line_number=record.lineno,
            request_id=request_id,
            user_id=user_id,
            session_id=session_id,
            extra_data=getattr(record, 'extra_data', None),
            exception_info=self._format_exception(record),
            duration_ms=getattr(record, 'duration_ms', None)
        )
        
        if self.format_type == "json":
            return json.dumps(log_entry.to_dict(), ensure_ascii=False)
        else:
            return self._format_text(log_entry)
    
    def _format_exception(self, record: logging.LogRecord) -> Optional[str]:
        """Formata informações de exceção"""
        if record.exc_info:
            return ''.join(traceback.format_exception(*record.exc_info))
        return None
    
    def _format_text(self, log_entry: LogEntry) -> str:
        """Formata como texto legível"""
        timestamp = log_entry.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        # Informações básicas
        parts = [
            f"[{timestamp}]",
            f"{log_entry.level:8}",
            f"{log_entry.category:12}",
            f"{log_entry.module}:{log_entry.function}:{log_entry.line_number}",
            log_entry.message
        ]
        
        # Adicionar contexto se disponível
        context_parts = []
        if log_entry.request_id:
            context_parts.append(f"req_id={log_entry.request_id}")
        if log_entry.user_id:
            context_parts.append(f"user_id={log_entry.user_id}")
        if log_entry.session_id:
            context_parts.append(f"session_id={log_entry.session_id}")
        
        if context_parts:
            parts.append(f"[{' '.join(context_parts)}]")
        
        # Adicionar dados extras
        if log_entry.extra_data:
            parts.append(f"extra={json.dumps(log_entry.extra_data)}")
        
        # Adicionar duração se disponível
        if log_entry.duration_ms:
            parts.append(f"duration={log_entry.duration_ms}ms")
        
        return " ".join(parts)

class ContextualLogger:
    """Logger contextual com informações de requisição"""
    
    def __init__(self, name: str, category: LogCategory = LogCategory.BUSINESS_LOGIC):
        self.logger = logging.getLogger(name)
        self.category = category
    
    def _log(self, level: LogLevel, message: str, extra_data: Optional[Dict[str, Any]] = None, 
             exc_info: bool = False, duration_ms: Optional[float] = None):
        """Log interno com contexto"""
        extra = {
            'category': self.category.value,
            'extra_data': extra_data,
            'duration_ms': duration_ms
        }
        
        self.logger.log(
            getattr(logging, level.value),
            message,
            extra=extra,
            exc_info=exc_info
        )
    
    def debug(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log de debug"""
        self._log(LogLevel.DEBUG, message, extra_data)
    
    def info(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log de informação"""
        self._log(LogLevel.INFO, message, extra_data)
    
    def warning(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log de aviso"""
        self._log(LogLevel.WARNING, message, extra_data)
    
    def error(self, message: str, extra_data: Optional[Dict[str, Any]] = None, 
              exc_info: bool = False):
        """Log de erro"""
        self._log(LogLevel.ERROR, message, extra_data, exc_info)
    
    def critical(self, message: str, extra_data: Optional[Dict[str, Any]] = None, 
                 exc_info: bool = False):
        """Log crítico"""
        self._log(LogLevel.CRITICAL, message, extra_data, exc_info)
    
    def performance(self, message: str, duration_ms: float, extra_data: Optional[Dict[str, Any]] = None):
        """Log de performance"""
        self._log(LogLevel.INFO, message, extra_data, duration_ms=duration_ms)

class LoggingManager:
    """Gerenciador centralizado de logging"""
    
    def __init__(self):
        self._loggers: Dict[str, ContextualLogger] = {}
        self._handlers: Dict[str, logging.Handler] = {}
        self._configured = False
    
    def configure(self, 
                 log_level: str = "INFO",
                 log_format: str = "json",
                 log_file: Optional[str] = None,
                 enable_console: bool = True,
                 enable_file: bool = True):
        """Configura sistema de logging"""
        
        if self._configured:
            return
        
        # Configurar nível de log
        level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Configurar formatador
        formatter = StructuredFormatter(log_format)
        
        # Handler para console
        if enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(level)
            logging.getLogger().addHandler(console_handler)
            self._handlers['console'] = console_handler
        
        # Handler para arquivo
        if enable_file and log_file:
            # Criar diretório de logs se necessário
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(level)
            logging.getLogger().addHandler(file_handler)
            self._handlers['file'] = file_handler
        
        # Configurar logger raiz
        logging.getLogger().setLevel(level)
        
        # Configurar loggers específicos
        self._configure_specific_loggers()
        
        self._configured = True
    
    def _configure_specific_loggers(self):
        """Configura loggers específicos"""
        # Logger para SQLAlchemy (menos verboso)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
        logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
        
        # Logger para requests (menos verboso)
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        
        # Logger para asyncio (menos verboso)
        logging.getLogger('asyncio').setLevel(logging.WARNING)
    
    def get_logger(self, name: str, category: LogCategory = LogCategory.BUSINESS_LOGIC) -> ContextualLogger:
        """Obtém logger contextual"""
        if name not in self._loggers:
            self._loggers[name] = ContextualLogger(name, category)
        return self._loggers[name]
    
    def set_request_context(self, request_id: str, user_id: Optional[str] = None, 
                           session_id: Optional[str] = None):
        """Define contexto da requisição"""
        request_id_var.set(request_id)
        if user_id:
            user_id_var.set(user_id)
        if session_id:
            session_id_var.set(session_id)
    
    def clear_request_context(self):
        """Limpa contexto da requisição"""
        request_id_var.set(None)
        user_id_var.set(None)
        session_id_var.set(None)
    
    def get_log_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de logging"""
        stats = {
            "configured": self._configured,
            "handlers": list(self._handlers.keys()),
            "loggers": list(self._loggers.keys()),
            "context": {
                "request_id": request_id_var.get(),
                "user_id": user_id_var.get(),
                "session_id": session_id_var.get()
            }
        }
        return stats

# Instância global do gerenciador
logging_manager = LoggingManager()

# Função de conveniência para obter logger
def get_logger(name: str, category: LogCategory = LogCategory.BUSINESS_LOGIC) -> ContextualLogger:
    """Obtém logger contextual"""
    return logging_manager.get_logger(name, category)

# Decorator para logging de performance
def log_performance(logger: ContextualLogger, operation: str):
    """Decorator para log de performance"""
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                logger.performance(f"{operation} completed", duration_ms)
                return result
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                logger.error(f"{operation} failed", {"duration_ms": duration_ms}, exc_info=True)
                raise
        
        def sync_wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                logger.performance(f"{operation} completed", duration_ms)
                return result
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                logger.error(f"{operation} failed", {"duration_ms": duration_ms}, exc_info=True)
                raise
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

# Loggers específicos por categoria
auth_logger = get_logger("auth", LogCategory.AUTHENTICATION)
business_logger = get_logger("business", LogCategory.BUSINESS_LOGIC)
infra_logger = get_logger("infrastructure", LogCategory.INFRASTRUCTURE)
security_logger = get_logger("security", LogCategory.SECURITY)
perf_logger = get_logger("performance", LogCategory.PERFORMANCE)
db_logger = get_logger("database", LogCategory.DATABASE)
blockchain_logger = get_logger("blockchain", LogCategory.BLOCKCHAIN)
transaction_logger = get_logger("transaction", LogCategory.TRANSACTION)
wallet_logger = get_logger("wallet", LogCategory.WALLET)
monitoring_logger = get_logger("monitoring", LogCategory.MONITORING)
