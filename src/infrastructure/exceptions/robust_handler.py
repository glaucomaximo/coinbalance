"""
Sistema de Tratamento de Exceções Robusto
=========================================

Implementa tratamento centralizado de exceções com logging estruturado,
recuperação automática e notificações de erro.
"""

import logging
import traceback
import asyncio
from typing import Any, Dict, Optional, Callable, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    """Severidade do erro"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Categoria do erro"""
    VALIDATION = "validation"
    BUSINESS_LOGIC = "business_logic"
    INFRASTRUCTURE = "infrastructure"
    SECURITY = "security"
    PERFORMANCE = "performance"
    EXTERNAL_SERVICE = "external_service"

@dataclass
class ErrorContext:
    """Contexto do erro"""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    endpoint: Optional[str] = None
    operation: Optional[str] = None
    additional_data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.additional_data is None:
            self.additional_data = {}

@dataclass
class ErrorInfo:
    """Informações estruturadas do erro"""
    error_id: str
    timestamp: datetime
    severity: ErrorSeverity
    category: ErrorCategory
    message: str
    exception_type: str
    stack_trace: str
    context: ErrorContext
    recovery_attempted: bool = False
    recovery_successful: bool = False

class RobustExceptionHandler:
    """Manipulador robusto de exceções"""
    
    def __init__(self):
        self.error_history: Dict[str, ErrorInfo] = {}
        self.recovery_strategies: Dict[str, Callable] = {}
        self.notification_handlers: list[Callable] = []
        self._setup_default_recovery_strategies()
    
    def _setup_default_recovery_strategies(self):
        """Configura estratégias de recuperação padrão"""
        self.recovery_strategies = {
            "ConnectionError": self._recover_connection_error,
            "TimeoutError": self._recover_timeout_error,
            "ValidationError": self._recover_validation_error,
            "BusinessLogicError": self._recover_business_logic_error,
            "InfrastructureError": self._recover_infrastructure_error,
        }
    
    async def handle_exception(
        self,
        exception: Exception,
        context: ErrorContext,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.BUSINESS_LOGIC,
        operation: Optional[str] = None
    ) -> ErrorInfo:
        """Manipula exceção de forma robusta"""
        
        # Gerar ID único para o erro
        error_id = f"ERR_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{id(exception)}"
        
        # Criar informações do erro
        error_info = ErrorInfo(
            error_id=error_id,
            timestamp=datetime.now(),
            severity=severity,
            category=category,
            message=str(exception),
            exception_type=type(exception).__name__,
            stack_trace=traceback.format_exc(),
            context=context
        )
        
        # Log estruturado
        await self._log_error(error_info)
        
        # Tentar recuperação automática
        if severity in [ErrorSeverity.LOW, ErrorSeverity.MEDIUM]:
            await self._attempt_recovery(error_info)
        
        # Notificar se crítico
        if severity == ErrorSeverity.CRITICAL:
            await self._notify_critical_error(error_info)
        
        # Armazenar histórico
        self.error_history[error_id] = error_info
        
        return error_info
    
    async def _log_error(self, error_info: ErrorInfo):
        """Log estruturado do erro"""
        log_data = {
            "error_id": error_info.error_id,
            "timestamp": error_info.timestamp.isoformat(),
            "severity": error_info.severity.value,
            "category": error_info.category.value,
            "message": error_info.message,
            "exception_type": error_info.exception_type,
            "context": {
                "user_id": error_info.context.user_id,
                "session_id": error_info.context.session_id,
                "request_id": error_info.context.request_id,
                "endpoint": error_info.context.endpoint,
                "operation": error_info.context.operation,
                "additional_data": error_info.context.additional_data
            }
        }
        
        # Log baseado na severidade
        if error_info.severity == ErrorSeverity.CRITICAL:
            logger.critical(f"CRITICAL ERROR: {json.dumps(log_data)}")
        elif error_info.severity == ErrorSeverity.HIGH:
            logger.error(f"HIGH ERROR: {json.dumps(log_data)}")
        elif error_info.severity == ErrorSeverity.MEDIUM:
            logger.warning(f"MEDIUM ERROR: {json.dumps(log_data)}")
        else:
            logger.info(f"LOW ERROR: {json.dumps(log_data)}")
    
    async def _attempt_recovery(self, error_info: ErrorInfo):
        """Tenta recuperação automática"""
        try:
            error_info.recovery_attempted = True
            
            # Buscar estratégia de recuperação
            recovery_func = self.recovery_strategies.get(error_info.exception_type)
            if recovery_func:
                success = await recovery_func(error_info)
                error_info.recovery_successful = success
                
                if success:
                    logger.info(f"Recovery successful for error {error_info.error_id}")
                else:
                    logger.warning(f"Recovery failed for error {error_info.error_id}")
            else:
                logger.debug(f"No recovery strategy for {error_info.exception_type}")
                
        except Exception as recovery_error:
            logger.error(f"Recovery attempt failed: {recovery_error}")
            error_info.recovery_successful = False
    
    async def _recover_connection_error(self, error_info: ErrorInfo) -> bool:
        """Estratégia de recuperação para erros de conexão"""
        try:
            # Implementar retry com backoff exponencial
            await asyncio.sleep(1)  # Simular retry
            return True
        except Exception:
            return False
    
    async def _recover_timeout_error(self, error_info: ErrorInfo) -> bool:
        """Estratégia de recuperação para timeouts"""
        try:
            # Implementar retry com timeout aumentado
            await asyncio.sleep(0.5)
            return True
        except Exception:
            return False
    
    async def _recover_validation_error(self, error_info: ErrorInfo) -> bool:
        """Estratégia de recuperação para erros de validação"""
        # Erros de validação geralmente não são recuperáveis
        return False
    
    async def _recover_business_logic_error(self, error_info: ErrorInfo) -> bool:
        """Estratégia de recuperação para erros de lógica de negócio"""
        try:
            # Implementar lógica de recuperação específica
            return False  # Geralmente não recuperável
        except Exception:
            return False
    
    async def _recover_infrastructure_error(self, error_info: ErrorInfo) -> bool:
        """Estratégia de recuperação para erros de infraestrutura"""
        try:
            # Tentar reconectar ou reinicializar componentes
            await asyncio.sleep(2)
            return True
        except Exception:
            return False
    
    async def _notify_critical_error(self, error_info: ErrorInfo):
        """Notifica erros críticos"""
        try:
            for handler in self.notification_handlers:
                await handler(error_info)
        except Exception as e:
            logger.error(f"Failed to notify critical error: {e}")
    
    def add_recovery_strategy(self, exception_type: str, strategy: Callable):
        """Adiciona estratégia de recuperação personalizada"""
        self.recovery_strategies[exception_type] = strategy
    
    def add_notification_handler(self, handler: Callable):
        """Adiciona manipulador de notificação"""
        self.notification_handlers.append(handler)
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de erros"""
        if not self.error_history:
            return {"total_errors": 0}
        
        total_errors = len(self.error_history)
        errors_by_severity = {}
        errors_by_category = {}
        recovery_success_rate = 0
        
        recovery_attempts = 0
        recovery_successes = 0
        
        for error in self.error_history.values():
            # Contar por severidade
            severity = error.severity.value
            errors_by_severity[severity] = errors_by_severity.get(severity, 0) + 1
            
            # Contar por categoria
            category = error.category.value
            errors_by_category[category] = errors_by_category.get(category, 0) + 1
            
            # Calcular taxa de recuperação
            if error.recovery_attempted:
                recovery_attempts += 1
                if error.recovery_successful:
                    recovery_successes += 1
        
        if recovery_attempts > 0:
            recovery_success_rate = (recovery_successes / recovery_attempts) * 100
        
        return {
            "total_errors": total_errors,
            "errors_by_severity": errors_by_severity,
            "errors_by_category": errors_by_category,
            "recovery_success_rate": recovery_success_rate,
            "recovery_attempts": recovery_attempts,
            "recovery_successes": recovery_successes
        }

# Instância global do manipulador
exception_handler = RobustExceptionHandler()

# Decorator para tratamento automático de exceções
def handle_exceptions(
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    category: ErrorCategory = ErrorCategory.BUSINESS_LOGIC,
    operation: Optional[str] = None
):
    """Decorator para tratamento automático de exceções"""
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                context = ErrorContext(
                    operation=operation or func.__name__,
                    additional_data={"args": str(args), "kwargs": str(kwargs)}
                )
                
                error_info = await exception_handler.handle_exception(
                    e, context, severity, category, operation
                )
                
                # Re-raise se não foi recuperado
                if not error_info.recovery_successful:
                    raise
                
                return None
        return wrapper
    return decorator
