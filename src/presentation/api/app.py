"""
Nova Aplicação FastAPI com Arquitetura DDD
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time
import logging

from src.infrastructure.config.settings import settings
from src.infrastructure.monitoring.security_monitor import security_monitor
from src.presentation.api.routers import wallet_router, health_router
from src.presentation.api.routers.wallet_additional import router as wallet_additional_router
from src.presentation.api.routers.web3_router import router as web3_router
from src.presentation.api.routers.holistic_router import router as holistic_router
from src.presentation.api.routers.consensus.consensus_router import router as consensus_router
from src.presentation.api.routers.transaction_router import router as transaction_router
from src.presentation.api.routers.system_router import router as system_router
from src.presentation.api.routers.auth_router import router as auth_router
from src.presentation.api.routers.transfer_router import router as transfer_router
from src.presentation.api.routers.security_router import router as security_router
from src.presentation.api.routers.transaction_history_router import router as history_router
from src.presentation.api.routers.monitoring_dashboard_router import router as dashboard_router
from src.presentation.api.routers.blockchain_router import router as blockchain_router
from src.presentation.api.routers.consciousness_economy_router import router as consciousness_economy_router
from src.presentation.api.routers.monitoring_router import router as monitoring_router
from src.presentation.api.routers.fractal_router import router as fractal_router
from src.presentation.api.routers.improvement_router import router as improvement_router
from src.presentation.api.routers.web3_advanced_router import router as web3_advanced_router
from src.presentation.api.routers.ai_advanced_router import router as ai_advanced_router
from src.presentation.api.routers.lgpd_router import router as lgpd_router
from src.presentation.api.routers.blockchain_performance_router import router as blockchain_performance_router
from src.domain.shared.exceptions import DomainException
from src.infrastructure.security.validation_middleware import validation_middleware

from src.infrastructure.logging.structured_logging import logging_manager, get_logger


# ========== LIFESPAN EVENTS ==========

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
    logger = get_logger(__name__)
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"📍 Environment: {settings.ENVIRONMENT}")
    logger.info("🏗️  Architecture: DDD + Clean Architecture + CQRS")
    logger.info(f"🔧 Debug mode: {settings.DEBUG}")

    # Configurar logging estruturado
    logging_manager.configure(
        log_level=settings.LOG_LEVEL,
        log_format=settings.LOG_FORMAT,
        log_file=settings.LOG_FILE,
        enable_console=True,
        enable_file=bool(settings.LOG_FILE)
    )
    
    # Obter logger estruturado
    logger = get_logger(__name__)
    logger.info("✅ Structured logging configured")
    
    # Inicializar container DI
    from src.infrastructure.di.container import get_container
    get_container()
    logger.info("✅ Dependency Injection Container initialized")

    # Inicializar database e cache
    try:
        from src.infrastructure.persistence.database_manager import DatabaseManager
        db_manager = DatabaseManager()
        await db_manager.initialize()
        logger.info("✅ Database initialized")
        
        # Inicializar cache se disponível
        try:
            from src.infrastructure.cache.cache_manager import CacheManager
            cache_manager = CacheManager()
            await cache_manager.initialize()
            logger.info("✅ Cache initialized")
        except ImportError:
            logger.info("ℹ️ Cache not available")
            
    except Exception as e:
        logger.error(f"❌ Error initializing infrastructure: {e}")
        raise
    logger.info("✅ Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down application...")
    # Fechar conexões e limpar recursos
    try:
        # Fechar conexões de database
        from src.infrastructure.persistence.database_manager import DatabaseManager
        db_manager = DatabaseManager()
        await db_manager.close()
        logger.info("✅ Database connections closed")
        
        # Limpar cache se disponível
        try:
            from src.infrastructure.cache.cache_manager import CacheManager
            cache_manager = CacheManager()
            await cache_manager.close()
            logger.info("✅ Cache cleaned")
        except ImportError:
            pass
            
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")
    logger.info("✅ Application shutdown complete")


# ========== CRIAR APLICAÇÃO ==========


def create_app() -> FastAPI:
    """
    Factory para criar aplicação FastAPI.

    Implementa configurações seguindo 12-Factor App e Clean Architecture.
    """
    
    # Configurar logger
    logger = get_logger(__name__)

    # Criar app
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url="/docs" if settings.docs_enabled else None,
        redoc_url="/redoc" if settings.docs_enabled else None,
        openapi_url="/openapi.json" if settings.docs_enabled else None,
        lifespan=lifespan,
    )

    # ========== MIDDLEWARES ==========

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    # Middleware de validação rigorosa
    app.middleware("http")(validation_middleware)
    
    # Rate Limiting Avançado
    # Habilitar rate limiting para produção
    # app.middleware("http")(rate_limit_middleware)  # TODO: Implementar rate limiting

    # Security Monitoring Middleware
    @app.middleware("http")
    async def security_monitoring_middleware(request: Request, call_next):
        """Middleware para monitoramento de segurança"""
        start_time = time.time()
        
        # Extrair informações da requisição
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        try:
            # Processar requisição
            response = await call_next(request)
            
            # Monitorar respostas de erro
            if response.status_code == 401:
                security_monitor.log_auth_failure(
                    wallet_address="unknown",
                    source_ip=client_ip,
                    user_agent=user_agent
                )
            elif response.status_code == 429:
                security_monitor.log_rate_limit_exceeded(
                    endpoint=str(request.url.path),
                    source_ip=client_ip,
                    user_agent=user_agent
                )
            elif response.status_code >= 500:
                security_monitor.log_suspicious_activity(
                    activity_type="SERVER_ERROR",
                    description=f"Erro interno do servidor: {response.status_code}",
                    source_ip=client_ip,
                    severity="MEDIUM"
                )
            
            return response
            
        except Exception as e:
            # Monitorar exceções
            security_monitor.log_suspicious_activity(
                activity_type="EXCEPTION",
                description=f"Exceção não tratada: {str(e)}",
                source_ip=client_ip,
                severity="HIGH"
            )
            raise

    # Logging Middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Middleware para logging de requisições"""
        start_time = time.time()

        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            logger.info(
                f"{request.method} {request.url.path} - "
                f"{response.status_code} - {process_time:.4f}s"
            )

            # Adicionar header de tempo de processamento
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"{request.method} {request.url.path} - "
                f"ERROR - {process_time:.4f}s - {str(e)}",
                exc_info=True,
            )
            raise

    # ========== EXCEPTION HANDLERS ==========

    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        """Handler para exceções de domínio"""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": exc.message,
                "code": exc.code,
                "timestamp": time.time(),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """Handler para erros de validação Pydantic"""
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "success": False,
                "error": "Validation error",
                "code": "VALIDATION_ERROR",
                "details": [
                    {
                        "field": str(error["loc"]),
                        "message": error["msg"],
                        "type": error["type"]
                    }
                    for error in exc.errors()
                ],
                "timestamp": time.time(),
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handler para exceções gerais"""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": "Internal server error",
                "code": "INTERNAL_ERROR",
                "message": str(exc) if settings.DEBUG else "An error occurred",
                "timestamp": time.time(),
            },
        )

    # ========== REGISTRAR ROUTERS ==========

    # Health & Info (sem prefix)
    app.include_router(health_router.router)

    # Authentication endpoints
    app.include_router(auth_router, prefix="/api/v1")

    # Transfer endpoints
    app.include_router(transfer_router, prefix="/api/v1")

    # Transaction History endpoints
    app.include_router(history_router, prefix="/api/v1")

    # Monitoring Dashboard endpoints
    app.include_router(dashboard_router, prefix="/api/v1")

    # Blockchain endpoints
    app.include_router(blockchain_router, prefix="/api/v1")
    app.include_router(consciousness_economy_router, prefix="/api/v1")

    # Monitoring endpoints
    app.include_router(monitoring_router, prefix="/api/v1")

    # Fractal Architecture endpoints
    app.include_router(fractal_router, prefix="/api/v1")

    # Security endpoints
    app.include_router(security_router, prefix="/api/v1")

    # Wallet endpoints
    app.include_router(wallet_router.router, prefix="/api/v1")
    app.include_router(wallet_additional_router, prefix="/api/v1")

    # Consensus endpoints
    app.include_router(consensus_router, prefix="/api/v1")

    # Transaction endpoints
    app.include_router(transaction_router, prefix="/api/v1")

    # System endpoints (faucet, minting, etc.)
    app.include_router(system_router, prefix="/api/v1")
    app.include_router(web3_router, prefix="/api/v1")
    
    # Holistic Integration endpoints
    app.include_router(holistic_router, prefix="/api/v1")
    
    # Improvement endpoints
    app.include_router(improvement_router)
    
    # Web3 Advanced endpoints
    app.include_router(web3_advanced_router)
    
    # AI Advanced endpoints
    app.include_router(ai_advanced_router)
    
    # LGPD Compliance endpoints
    app.include_router(lgpd_router, prefix="/api/v1")
    app.include_router(blockchain_performance_router, prefix="/api/v1")

    # Additional routers can be added here as needed
    # Example: app.include_router(new_router, prefix="/api/v1")

    logger.info("✅ All routers registered")

    return app


# ========== INSTÂNCIA DA APLICAÇÃO ==========

app = create_app()


# ========== METADATA ==========


@app.get("/version", tags=["Metadata"])
async def version():
    """Retorna versão da aplicação"""
    return {
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "architecture": "DDD + Clean Architecture + Hexagonal + CQRS",
    }
