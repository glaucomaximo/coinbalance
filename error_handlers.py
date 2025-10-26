"""
Sistema Avançado de Tratamento de Erros - CoinBalance
Implementa logging, monitoramento e tratamento robusto de erros
"""

import logging
import traceback
import time
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import json

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/coinbalance.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class CoinBalanceError(Exception):
    """Exceção base para erros do CoinBalance"""
    def __init__(self, message: str, error_code: str = "COINBALANCE_ERROR", details: Dict = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(CoinBalanceError):
    """Erro de validação"""
    def __init__(self, message: str, field: str = None):
        super().__init__(message, "VALIDATION_ERROR", {"field": field})

class SecurityError(CoinBalanceError):
    """Erro de segurança"""
    def __init__(self, message: str, threat_level: str = "MEDIUM"):
        super().__init__(message, "SECURITY_ERROR", {"threat_level": threat_level})

class BusinessLogicError(CoinBalanceError):
    """Erro de lógica de negócio"""
    def __init__(self, message: str, operation: str = None):
        super().__init__(message, "BUSINESS_LOGIC_ERROR", {"operation": operation})

class DatabaseError(CoinBalanceError):
    """Erro de banco de dados"""
    def __init__(self, message: str, query: str = None):
        super().__init__(message, "DATABASE_ERROR", {"query": query})

class ErrorHandler:
    """Gerenciador centralizado de erros"""
    
    def __init__(self):
        self.error_counts = {}
        self.error_history = []
    
    def handle_error(self, error: Exception, request: Request = None) -> JSONResponse:
        """Trata erro e retorna resposta JSON apropriada"""
        
        # Log do erro
        self._log_error(error, request)
        
        # Contar erros
        error_type = type(error).__name__
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Determinar código de status HTTP
        status_code = self._get_status_code(error)
        
        # Criar resposta de erro
        error_response = {
            "error": True,
            "error_code": getattr(error, 'error_code', 'UNKNOWN_ERROR'),
            "message": str(error),
            "timestamp": time.time(),
            "request_id": getattr(request.state, 'request_id', 'unknown') if hasattr(request, 'state') else 'unknown'
        }
        
        # Adicionar detalhes se disponíveis
        if hasattr(error, 'details'):
            error_response["details"] = error.details
        
        # Adicionar traceback em modo debug
        if logging.getLogger().level == logging.DEBUG:
            error_response["traceback"] = traceback.format_exc()
        
        return JSONResponse(
            status_code=status_code,
            content=error_response
        )
    
    def _log_error(self, error: Exception, request: Request = None):
        """Registra erro no log"""
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": time.time(),
            "traceback": traceback.format_exc()
        }
        
        if request:
            error_info.update({
                "method": request.method,
                "url": str(request.url),
                "headers": dict(request.headers),
                "client_ip": request.client.host if request.client else None
            })
        
        # Log baseado no tipo de erro
        if isinstance(error, SecurityError):
            logger.critical(f"SECURITY ERROR: {error_info}")
        elif isinstance(error, (ValidationError, BusinessLogicError)):
            logger.warning(f"BUSINESS ERROR: {error_info}")
        else:
            logger.error(f"SYSTEM ERROR: {error_info}")
        
        # Adicionar ao histórico
        self.error_history.append(error_info)
        
        # Manter apenas últimos 1000 erros
        if len(self.error_history) > 1000:
            self.error_history = self.error_history[-1000:]
    
    def _get_status_code(self, error: Exception) -> int:
        """Determina código de status HTTP baseado no tipo de erro"""
        if isinstance(error, ValidationError):
            return 400
        elif isinstance(error, SecurityError):
            return 403
        elif isinstance(error, BusinessLogicError):
            return 422
        elif isinstance(error, DatabaseError):
            return 500
        elif isinstance(error, HTTPException):
            return error.status_code
        else:
            return 500
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de erros"""
        return {
            "total_errors": sum(self.error_counts.values()),
            "error_counts": self.error_counts,
            "recent_errors": self.error_history[-10:] if self.error_history else [],
            "error_rate": self._calculate_error_rate()
        }
    
    def _calculate_error_rate(self) -> float:
        """Calcula taxa de erro por minuto"""
        if not self.error_history:
            return 0.0
        
        current_time = time.time()
        errors_last_minute = [
            error for error in self.error_history
            if current_time - error["timestamp"] < 60
        ]
        
        return len(errors_last_minute)

# Instância global do gerenciador de erros
error_handler = ErrorHandler()

# Middleware de tratamento de erros
async def error_middleware(request: Request, call_next):
    """Middleware para capturar e tratar erros"""
    request.state.request_id = f"req_{int(time.time() * 1000)}"
    
    try:
        response = await call_next(request)
        return response
    except Exception as error:
        return error_handler.handle_error(error, request)

# Handlers específicos para FastAPI
def setup_error_handlers(app):
    """Configura handlers de erro para FastAPI"""
    
    @app.exception_handler(CoinBalanceError)
    async def coinbalance_error_handler(request: Request, exc: CoinBalanceError):
        return error_handler.handle_error(exc, request)
    
    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return error_handler.handle_error(exc, request)
    
    @app.exception_handler(SecurityError)
    async def security_error_handler(request: Request, exc: SecurityError):
        return error_handler.handle_error(exc, request)
    
    @app.exception_handler(BusinessLogicError)
    async def business_logic_error_handler(request: Request, exc: BusinessLogicError):
        return error_handler.handle_error(exc, request)
    
    @app.exception_handler(DatabaseError)
    async def database_error_handler(request: Request, exc: DatabaseError):
        return error_handler.handle_error(exc, request)
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        error = ValidationError(
            message="Dados de entrada inválidos",
            details={"validation_errors": exc.errors()}
        )
        return error_handler.handle_error(error, request)
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return error_handler.handle_error(exc, request)

# Funções utilitárias para validação
def validate_wallet_address(address: str) -> bool:
    """Valida endereço de carteira"""
    if not address or not isinstance(address, str):
        raise ValidationError("Endereço de carteira inválido", "address")
    
    if not address.startswith("CRYPTO_"):
        raise ValidationError("Endereço deve começar com 'CRYPTO_'", "address")
    
    if len(address) < 20:
        raise ValidationError("Endereço muito curto", "address")
    
    return True

def validate_transaction_amount(amount: float) -> bool:
    """Valida valor de transação"""
    if not isinstance(amount, (int, float)):
        raise ValidationError("Valor deve ser numérico", "amount")
    
    if amount <= 0:
        raise ValidationError("Valor deve ser positivo", "amount")
    
    if amount > 1000000:  # Limite de 1M tokens
        raise ValidationError("Valor excede limite máximo", "amount")
    
    return True

def validate_private_key(private_key: str) -> bool:
    """Valida chave privada"""
    if not private_key or not isinstance(private_key, str):
        raise SecurityError("Chave privada inválida", "HIGH")
    
    if not private_key.startswith("-----BEGIN PRIVATE KEY-----"):
        raise SecurityError("Formato de chave privada inválido", "HIGH")
    
    return True
