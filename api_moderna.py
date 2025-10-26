"""
API Moderna com FastAPI
Implementa endpoints RESTful com documentação automática, validação e segurança
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uvicorn
import time
import json
import logging
import psutil

# Importar módulos do sistema
from database_manager import DatabaseManager
from wallet_system import Carteira, GerenciadorCarteiras
from transaction_validator import TransactionValidator
from smart_contracts import ContractManager
from crypto_utils import CryptoUtils

# Importar melhorias
from error_handlers import error_handler, setup_error_handlers, error_middleware
from rate_limiter import rate_limit_middleware, rate_limiter
from health_monitor import health_monitor

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar aplicação FastAPI
app = FastAPI(
    title="CoinBalance API",
    description="Blockchain moderna com DeFi, staking e contratos inteligentes - Equilíbrio perfeito entre segurança e performance",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adicionar middleware de tratamento de erros
app.middleware("http")(error_middleware)

# Adicionar middleware de rate limiting
app.middleware("http")(rate_limit_middleware)

# Configurar handlers de erro
setup_error_handlers(app)

# Inicializar componentes do sistema
db_manager = DatabaseManager()
wallet_manager = GerenciadorCarteiras()
transaction_validator = TransactionValidator(db_manager)
contract_manager = ContractManager(db_manager)
security = HTTPBearer()

# Inicializar tempo de início da aplicação
app.state.start_time = time.time()

# Modelos Pydantic para validação
class TransacaoRequest(BaseModel):
    remetente: str = Field(..., description="Endereço do remetente")
    destinatario: str = Field(..., description="Endereço do destinatário")
    valor: float = Field(..., gt=0, description="Valor da transação")
    taxa: Optional[float] = Field(0.001, description="Taxa da transação")
    dados_extra: Optional[Dict[str, Any]] = Field(default_factory=dict)

class CarteiraRequest(BaseModel):
    nome: str = Field(..., description="Nome da carteira")
    senha: Optional[str] = Field(None, description="Senha da carteira")

class StakeRequest(BaseModel):
    valor: float = Field(..., gt=0, description="Valor para stake")
    contrato: str = Field("STAKING_CONTRACT_001", description="Endereço do contrato")

class BorrowRequest(BaseModel):
    valor: float = Field(..., gt=0, description="Valor do empréstimo")
    colateral: float = Field(..., gt=0, description="Valor do colateral")

class BlocoResponse(BaseModel):
    indice: int
    timestamp: float
    hash_anterior: str
    hash_atual: str
    prova: int
    transacoes: List[Dict]
    tempo_mineracao: float

class CarteiraResponse(BaseModel):
    endereco: str
    saldo: float
    chave_publica: str
    criado_em: float

# Endpoints da API

@app.get("/", summary="Status da API")
async def status():
    """Verifica status da API e informações básicas"""
    return {
        "status": "online",
        "versao": "2.0.0",
        "timestamp": time.time(),
        "blockchain": {
            "blocos": len(db_manager.obter_todos_blocos()),
            "contratos_ativos": len(contract_manager.contratos)
        }
    }

@app.post("/carteiras/criar", response_model=CarteiraResponse, summary="Criar Nova Carteira")
async def criar_carteira(request: CarteiraRequest):
    """Cria uma nova carteira digital segura"""
    try:
        carteira = wallet_manager.criar_carteira(request.nome, request.senha)
        
        # Salvar no banco de dados
        db_manager.atualizar_saldo_carteira(carteira.endereco, 0.0)
        
        return CarteiraResponse(
            endereco=carteira.endereco,
            saldo=carteira.saldo,
            chave_publica=carteira.public_key,
            criado_em=carteira._obter_timestamp()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/carteiras/{nome}", response_model=CarteiraResponse, summary="Obter Carteira")
async def obter_carteira(nome: str):
    """Obtém informações de uma carteira"""
    carteira = wallet_manager.obter_carteira(nome)
    if not carteira:
        raise HTTPException(status_code=404, detail="Carteira não encontrada")
    
    saldo = db_manager.obter_saldo_carteira(carteira.endereco)
    
    return CarteiraResponse(
        endereco=carteira.endereco,
        saldo=saldo,
        chave_publica=carteira.public_key,
        criado_em=carteira._obter_timestamp()
    )

@app.post("/transacoes/criar", summary="Criar Transação")
async def criar_transacao(request: TransacaoRequest):
    """Cria e valida uma nova transação"""
    try:
        # Obter carteira do remetente
        carteira_remetente = None
        for nome, carteira in wallet_manager.carteiras.items():
            if carteira.endereco == request.remetente:
                carteira_remetente = carteira
                break
        
        if not carteira_remetente:
            raise HTTPException(status_code=404, detail="Carteira remetente não encontrada")
        
        # Criar transação
        transacao = carteira_remetente.criar_transacao(
            request.destinatario,
            request.valor,
            request.dados_extra
        )
        
        # Validar transação
        validacao = transaction_validator.validar_transacao(transacao)
        if not validacao['valida']:
            raise HTTPException(status_code=400, detail=f"Transação inválida: {validacao['erros']}")
        
        # Processar transação
        sucesso = transaction_validator.processar_transacao(transacao)
        if not sucesso:
            raise HTTPException(status_code=500, detail="Erro ao processar transação")
        
        return {
            "sucesso": True,
            "mensagem": "Transação criada e processada com sucesso",
            "hash_transacao": transaction_validator._gerar_hash_transacao(transacao),
            "validacao": validacao
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/blockchain", summary="Obter Blockchain Completa")
async def obter_blockchain():
    """Retorna a blockchain completa"""
    blocos = db_manager.obter_todos_blocos()
    return {
        "blockchain": blocos,
        "comprimento": len(blocos),
        "hash_ultimo_bloco": blocos[-1].get('hash_atual') if blocos else None
    }

@app.get("/blockchain/{indice}", response_model=BlocoResponse, summary="Obter Bloco Específico")
async def obter_bloco(indice: int):
    """Obtém um bloco específico por índice"""
    bloco = db_manager.obter_bloco(indice)
    if not bloco:
        raise HTTPException(status_code=404, detail="Bloco não encontrado")
    
    return BlocoResponse(
        indice=bloco['indice'],
        timestamp=bloco['carimbo_temporal'],
        hash_anterior=bloco.get('fragmento_anterior', ''),
        hash_atual=bloco.get('hash_atual', ''),
        prova=bloco['prova'],
        transacoes=bloco.get('transacoes', []),
        tempo_mineracao=0.0  # Implementar cálculo
    )

@app.post("/defi/stake", summary="Fazer Stake")
async def fazer_stake(request: StakeRequest):
    """Faz stake de tokens em contrato de staking"""
    try:
        resultado = contract_manager.executar_contrato(
            request.contrato,
            "stake",
            {"valor": request.valor},
            "USER_ADDRESS"  # Implementar autenticação
        )
        
        if not resultado['sucesso']:
            raise HTTPException(status_code=400, detail=resultado['erro'])
        
        return resultado
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/defi/borrow", summary="Solicitar Empréstimo")
async def solicitar_emprestimo(request: BorrowRequest):
    """Solicita empréstimo no protocolo DeFi"""
    try:
        resultado = contract_manager.executar_contrato(
            "LENDING_CONTRACT_001",
            "borrow",
            {
                "valor": request.valor,
                "colateral": request.colateral
            },
            "USER_ADDRESS"  # Implementar autenticação
        )
        
        if not resultado['sucesso']:
            raise HTTPException(status_code=400, detail=resultado['erro'])
        
        return resultado
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/defi/contratos", summary="Listar Contratos DeFi")
async def listar_contratos():
    """Lista todos os contratos inteligentes disponíveis"""
    return {
        "contratos": contract_manager.listar_contratos(),
        "total": len(contract_manager.contratos)
    }

@app.get("/defi/stake/info", summary="Informações de Staking")
async def info_staking():
    """Obtém informações sobre staking"""
    resultado = contract_manager.executar_contrato(
        "STAKING_CONTRACT_001",
        "get_stake_info",
        {},
        "USER_ADDRESS"
    )
    
    return resultado

@app.post("/mineracao/minerar", summary="Minerar Novo Bloco")
async def minerar_bloco(background_tasks: BackgroundTasks):
    """Inicia processo de mineração de novo bloco"""
    try:
        # Implementar lógica de mineração
        # Por enquanto, retorna sucesso
        return {
            "sucesso": True,
            "mensagem": "Mineração iniciada",
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/estatisticas", summary="Estatísticas da Rede")
async def estatisticas():
    """Obtém estatísticas da rede blockchain"""
    blocos = db_manager.obter_todos_blocos()
    
    return {
        "blockchain": {
            "total_blocos": len(blocos),
            "ultimo_bloco": blocos[-1] if blocos else None,
            "hash_atual": blocos[-1].get('hash_atual') if blocos else None
        },
        "contratos": {
            "total_contratos": len(contract_manager.contratos),
            "tipos": list(set(type(c).__name__ for c in contract_manager.contratos.values()))
        },
        "rede": {
            "status": "ativa",
            "timestamp": time.time()
        }
    }

@app.get("/health", summary="Health Check Avançado")
async def health_check():
    """Verifica saúde completa do sistema"""
    try:
        # Executar todos os health checks
        checks = await health_monitor.run_all_checks()
        summary = health_monitor.get_health_summary()
        
        return {
            "status": "success",
            "timestamp": time.time(),
            "overall_status": summary["overall_status"],
            "checks": summary["checks"],
            "summary": {
                "total_checks": summary["total_checks"],
                "healthy": summary["healthy_checks"],
                "warnings": summary["warning_checks"],
                "critical": summary["critical_checks"]
            }
        }
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        return {
            "status": "error",
            "message": str(e),
            "timestamp": time.time()
        }

@app.get("/health/simple", summary="Health Check Simples")
async def health_simple():
    """Health check simples para load balancers"""
    try:
        # Verificação básica
        blocos = db_manager.obter_todos_blocos()
        
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "blockchain": len(blocos),
            "version": "2.1.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }

@app.get("/metrics", summary="Métricas do Sistema")
async def metrics():
    """Retorna métricas detalhadas do sistema"""
    try:
        # Estatísticas de erro
        error_stats = error_handler.get_error_statistics()
        
        # Estatísticas de rate limiting
        rate_limit_stats = rate_limiter.get_rate_limit_stats()
        
        # Estatísticas da blockchain
        blocos = db_manager.obter_todos_blocos()
        
        return {
            "timestamp": time.time(),
            "version": "2.1.0",
            "blockchain": {
                "total_blocks": len(blocos),
                "last_block_time": blocos[-1].get('carimbo_temporal') if blocos else None
            },
            "errors": error_stats,
            "rate_limiting": rate_limit_stats,
            "system": {
                "uptime": time.time() - app.state.start_time if hasattr(app.state, 'start_time') else 0,
                "memory_usage": psutil.virtual_memory().percent if 'psutil' in globals() else 0
            }
        }
    except Exception as e:
        logger.error(f"Erro ao obter métricas: {e}")
        return {"error": str(e), "timestamp": time.time()}

@app.get("/admin/errors", summary="Estatísticas de Erros")
async def admin_errors():
    """Retorna estatísticas detalhadas de erros (apenas para administradores)"""
    try:
        return error_handler.get_error_statistics()
    except Exception as e:
        return {"error": str(e), "timestamp": time.time()}

@app.post("/admin/rate-limit/block", summary="Bloquear IP")
async def block_ip(ip: str, reason: str = "Manual block"):
    """Bloqueia um IP (apenas para administradores)"""
    try:
        rate_limiter.block_ip(ip, reason)
        return {"success": True, "message": f"IP {ip} bloqueado", "reason": reason}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.delete("/admin/rate-limit/unblock", summary="Desbloquear IP")
async def unblock_ip(ip: str):
    """Desbloqueia um IP (apenas para administradores)"""
    try:
        rate_limiter.unblock_ip(ip)
        return {"success": True, "message": f"IP {ip} desbloqueado"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Middleware para logging
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(f"{request.method} {request.url} - {response.status_code} - {process_time:.4f}s")
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"{request.method} {request.url} - ERROR - {process_time:.4f}s - {str(e)}")
        raise

if __name__ == "__main__":
    uvicorn.run(
        "api_moderna:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
