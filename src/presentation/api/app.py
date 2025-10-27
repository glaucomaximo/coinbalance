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
from src.presentation.api.routers import wallet_router, health_router
from src.presentation.api.routers.wallet_additional import router as wallet_additional_router
from src.presentation.api.routers.consensus.consensus_router import router as consensus_router
from src.presentation.api.routers.transaction_router import router as transaction_router
from src.presentation.api.routers.system_router import router as system_router
from src.domain.shared.exceptions import DomainException

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ========== LIFESPAN EVENTS ==========

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"📍 Environment: {settings.ENVIRONMENT}")
    logger.info("🏗️  Architecture: DDD + Clean Architecture + CQRS")
    logger.info(f"🔧 Debug mode: {settings.DEBUG}")

    # Inicializar container DI
    from src.infrastructure.di.container import get_container
    get_container()
    logger.info("✅ Dependency Injection Container initialized")

    # TODO: Inicializar database, cache, etc
    logger.info("✅ Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down application...")
    # TODO: Fechar conexões, limpar recursos
    logger.info("✅ Application shutdown complete")


# ========== CRIAR APLICAÇÃO ==========


def create_app() -> FastAPI:
    """
    Factory para criar aplicação FastAPI.

    Implementa configurações seguindo 12-Factor App e Clean Architecture.
    """

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
                "details": exc.errors(),
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

    # Wallet endpoints
    app.include_router(wallet_router.router, prefix="/api/v1")
    app.include_router(wallet_additional_router, prefix="/api/v1")
    
    # Consensus endpoints
    app.include_router(consensus_router, prefix="/api/v1")
    
    # Transaction endpoints
    app.include_router(transaction_router, prefix="/api/v1")
    
    # System endpoints (faucet, minting, etc.)
    app.include_router(system_router, prefix="/api/v1")

    # TODO: Adicionar outros routers
    # app.include_router(blockchain_router.router, prefix="/api/v1")
    # app.include_router(defi_router.router, prefix="/api/v1")

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
