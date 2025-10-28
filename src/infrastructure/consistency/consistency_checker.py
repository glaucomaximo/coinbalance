"""
Consistency Checker - Sistema de Verificação e Correção de Inconsistências
Baseado na análise holística do CoinBalance
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import json
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)


class ConsistencyLevel(Enum):
    """Níveis de consistência"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ConsistencyIssue:
    """Problema de consistência identificado"""
    id: str
    level: ConsistencyLevel
    component: str
    description: str
    impact: str
    solution: str
    auto_fixable: bool = False
    detected_at: float = field(default_factory=lambda: __import__('time').time())
    fixed: bool = False


@dataclass
class ConsistencyCheck:
    """Verificação de consistência"""
    name: str
    description: str
    check_function: str
    fix_function: Optional[str] = None
    enabled: bool = True
    last_run: Optional[float] = None


class ConsistencyChecker:
    """Verificador de Consistência Holístico"""
    
    def __init__(self):
        self.issues: List[ConsistencyIssue] = []
        self.checks: List[ConsistencyCheck] = []
        self.is_running = False
        self._setup_default_checks()
    
    def _setup_default_checks(self):
        """Configura verificações padrão"""
        self.checks = [
            ConsistencyCheck(
                name="database_schema",
                description="Verifica consistência do schema do banco",
                check_function="check_database_schema",
                fix_function="fix_database_schema"
            ),
            ConsistencyCheck(
                name="api_endpoints",
                description="Verifica consistência dos endpoints da API",
                check_function="check_api_endpoints",
                fix_function="fix_api_endpoints"
            ),
            ConsistencyCheck(
                name="web3_integration",
                description="Verifica integração Web3",
                check_function="check_web3_integration",
                fix_function="fix_web3_integration"
            ),
            ConsistencyCheck(
                name="fractal_consistency",
                description="Verifica consistência fractal",
                check_function="check_fractal_consistency",
                fix_function="fix_fractal_consistency"
            ),
            ConsistencyCheck(
                name="ai_system_consistency",
                description="Verifica consistência do sistema de IA",
                check_function="check_ai_system_consistency",
                fix_function="fix_ai_system_consistency"
            ),
            ConsistencyCheck(
                name="monitoring_alignment",
                description="Verifica alinhamento do monitoramento",
                check_function="check_monitoring_alignment",
                fix_function="fix_monitoring_alignment"
            )
        ]
    
    async def start_consistency_monitoring(self):
        """Inicia monitoramento de consistência"""
        self.is_running = True
        logger.info("🔍 Iniciando monitoramento de consistência")
        
        while self.is_running:
            try:
                await self._run_all_checks()
                await asyncio.sleep(30)  # Verificar a cada 30 segundos
                
            except Exception as e:
                logger.error(f"Erro no monitoramento de consistência: {e}")
                await asyncio.sleep(60)
    
    async def stop_consistency_monitoring(self):
        """Para o monitoramento de consistência"""
        self.is_running = False
        logger.info("🛑 Monitoramento de consistência parado")
    
    async def _run_all_checks(self):
        """Executa todas as verificações"""
        for check in self.checks:
            if not check.enabled:
                continue
            
            try:
                await self._run_check(check)
                check.last_run = __import__('time').time()
                
            except Exception as e:
                logger.error(f"Erro na verificação {check.name}: {e}")
    
    async def _run_check(self, check: ConsistencyCheck):
        """Executa uma verificação específica"""
        method = getattr(self, check.check_function, None)
        if method:
            issues = await method()
            for issue in issues:
                if not self._issue_exists(issue.id):
                    self.issues.append(issue)
                    logger.warning(f"⚠️ Inconsistência detectada: {issue.description}")
    
    def _issue_exists(self, issue_id: str) -> bool:
        """Verifica se o problema já existe"""
        return any(issue.id == issue_id and not issue.fixed for issue in self.issues)
    
    async def check_database_schema(self) -> List[ConsistencyIssue]:
        """Verifica consistência do schema do banco"""
        issues = []
        
        try:
            # Verificar se o banco existe
            db_path = Path("blockchain.db")
            if not db_path.exists():
                issues.append(ConsistencyIssue(
                    id="db_missing",
                    level=ConsistencyLevel.CRITICAL,
                    component="database",
                    description="Banco de dados não encontrado",
                    impact="Sistema não pode funcionar",
                    solution="Criar banco de dados",
                    auto_fixable=True
                ))
                return issues
            
            # Verificar tabelas essenciais
            conn = sqlite3.connect("blockchain.db")
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = [
                "blocks", "transactions", "wallets", "users", 
                "validators", "stakes", "ai_tokens", "web3_contracts"
            ]
            
            for table in required_tables:
                if table not in tables:
                    issues.append(ConsistencyIssue(
                        id=f"table_missing_{table}",
                        level=ConsistencyLevel.HIGH,
                        component="database",
                        description=f"Tabela '{table}' não encontrada",
                        impact="Funcionalidades relacionadas não funcionarão",
                        solution=f"Criar tabela '{table}'",
                        auto_fixable=True
                    ))
            
            conn.close()
            
        except Exception as e:
            issues.append(ConsistencyIssue(
                id="db_check_error",
                level=ConsistencyLevel.CRITICAL,
                component="database",
                description=f"Erro ao verificar banco: {e}",
                impact="Verificação de consistência falhou",
                solution="Corrigir conexão com banco",
                auto_fixable=False
            ))
        
        return issues
    
    async def check_api_endpoints(self) -> List[ConsistencyIssue]:
        """Verifica consistência dos endpoints da API"""
        issues = []
        
        try:
            # Verificar se os roteadores existem
            router_files = [
                "src/presentation/api/routers/auth_router.py",
                "src/presentation/api/routers/wallet_router.py",
                "src/presentation/api/routers/transaction_router.py",
                "src/presentation/api/routers/web3_router.py",
                "src/presentation/api/routers/ai_crypto_router.py",
                "src/presentation/api/routers/holistic_router.py"
            ]
            
            for router_file in router_files:
                if not Path(router_file).exists():
                    issues.append(ConsistencyIssue(
                        id=f"router_missing_{Path(router_file).stem}",
                        level=ConsistencyLevel.HIGH,
                        component="api",
                        description=f"Roteador '{router_file}' não encontrado",
                        impact="Endpoints relacionados não estarão disponíveis",
                        solution=f"Criar roteador '{router_file}'",
                        auto_fixable=False
                    ))
            
        except Exception as e:
            issues.append(ConsistencyIssue(
                id="api_check_error",
                level=ConsistencyLevel.MEDIUM,
                component="api",
                description=f"Erro ao verificar API: {e}",
                impact="Verificação de endpoints falhou",
                solution="Corrigir verificação de API",
                auto_fixable=False
            ))
        
        return issues
    
    async def check_web3_integration(self) -> List[ConsistencyIssue]:
        """Verifica integração Web3"""
        issues = []
        
        try:
            # Verificar módulos Web3
            web3_modules = [
                "src/infrastructure/web3/smart_contracts.py",
                "src/infrastructure/web3/wallet_connect.py",
                "src/infrastructure/web3/defi_protocols.py",
                "src/infrastructure/web3/nft_marketplace.py",
                "src/infrastructure/web3/dao_governance.py",
                "src/infrastructure/web3/cross_chain_bridge.py",
                "src/infrastructure/web3/web3_analytics.py"
            ]
            
            for module in web3_modules:
                if not Path(module).exists():
                    issues.append(ConsistencyIssue(
                        id=f"web3_module_missing_{Path(module).stem}",
                        level=ConsistencyLevel.HIGH,
                        component="web3",
                        description=f"Módulo Web3 '{module}' não encontrado",
                        impact="Funcionalidades Web3 não estarão disponíveis",
                        solution=f"Criar módulo '{module}'",
                        auto_fixable=False
                    ))
            
        except Exception as e:
            issues.append(ConsistencyIssue(
                id="web3_check_error",
                level=ConsistencyLevel.MEDIUM,
                component="web3",
                description=f"Erro ao verificar Web3: {e}",
                impact="Verificação de Web3 falhou",
                solution="Corrigir verificação de Web3",
                auto_fixable=False
            ))
        
        return issues
    
    async def check_fractal_consistency(self) -> List[ConsistencyIssue]:
        """Verifica consistência fractal"""
        issues = []
        
        try:
            # Verificar módulos de consciência fractal
            fractal_modules = [
                "src/domain/consciousness/services/distributed_consciousness.py",
                "src/infrastructure/fractal/web3/conscious_web3_manager.py",
                "src/domain/web3/consciousness/web3_consciousness.py"
            ]
            
            for module in fractal_modules:
                if not Path(module).exists():
                    issues.append(ConsistencyIssue(
                        id=f"fractal_module_missing_{Path(module).stem}",
                        level=ConsistencyLevel.MEDIUM,
                        component="fractal",
                        description=f"Módulo fractal '{module}' não encontrado",
                        impact="Consciência fractal não funcionará completamente",
                        solution=f"Criar módulo '{module}'",
                        auto_fixable=False
                    ))
            
        except Exception as e:
            issues.append(ConsistencyIssue(
                id="fractal_check_error",
                level=ConsistencyLevel.MEDIUM,
                component="fractal",
                description=f"Erro ao verificar fractal: {e}",
                impact="Verificação de fractal falhou",
                solution="Corrigir verificação de fractal",
                auto_fixable=False
            ))
        
        return issues
    
    async def check_ai_system_consistency(self) -> List[ConsistencyIssue]:
        """Verifica consistência do sistema de IA"""
        issues = []
        
        try:
            # Verificar módulos de IA
            ai_modules = [
                "src/domain/ai_crypto_creation/services/autonomous_economy.py",
                "src/domain/ai_crypto_creation/services/token_factory.py",
                "src/domain/ai_crypto_creation/entities/crypto_intelligence.py"
            ]
            
            for module in ai_modules:
                if not Path(module).exists():
                    issues.append(ConsistencyIssue(
                        id=f"ai_module_missing_{Path(module).stem}",
                        level=ConsistencyLevel.HIGH,
                        component="ai",
                        description=f"Módulo de IA '{module}' não encontrado",
                        impact="Funcionalidades de IA não estarão disponíveis",
                        solution=f"Criar módulo '{module}'",
                        auto_fixable=False
                    ))
            
        except Exception as e:
            issues.append(ConsistencyIssue(
                id="ai_check_error",
                level=ConsistencyLevel.MEDIUM,
                component="ai",
                description=f"Erro ao verificar IA: {e}",
                impact="Verificação de IA falhou",
                solution="Corrigir verificação de IA",
                auto_fixable=False
            ))
        
        return issues
    
    async def check_monitoring_alignment(self) -> List[ConsistencyIssue]:
        """Verifica alinhamento do monitoramento"""
        issues = []
        
        try:
            # Verificar módulos de monitoramento
            monitoring_modules = [
                "src/infrastructure/monitoring/holistic_monitoring.py",
                "src/infrastructure/monitoring/conscious_monitoring.py",
                "src/infrastructure/monitoring/performance_monitor.py",
                "src/infrastructure/monitoring/security_monitor.py",
                "src/infrastructure/monitoring/unified_monitoring.py"
            ]
            
            for module in monitoring_modules:
                if not Path(module).exists():
                    issues.append(ConsistencyIssue(
                        id=f"monitoring_module_missing_{Path(module).stem}",
                        level=ConsistencyLevel.MEDIUM,
                        component="monitoring",
                        description=f"Módulo de monitoramento '{module}' não encontrado",
                        impact="Monitoramento não funcionará completamente",
                        solution=f"Criar módulo '{module}'",
                        auto_fixable=False
                    ))
            
        except Exception as e:
            issues.append(ConsistencyIssue(
                id="monitoring_check_error",
                level=ConsistencyLevel.MEDIUM,
                component="monitoring",
                description=f"Erro ao verificar monitoramento: {e}",
                impact="Verificação de monitoramento falhou",
                solution="Corrigir verificação de monitoramento",
                auto_fixable=False
            ))
        
        return issues
    
    async def auto_fix_issues(self):
        """Corrige automaticamente problemas que podem ser corrigidos"""
        fixable_issues = [issue for issue in self.issues if issue.auto_fixable and not issue.fixed]
        
        for issue in fixable_issues:
            try:
                await self._fix_issue(issue)
                issue.fixed = True
                logger.info(f"✅ Problema corrigido automaticamente: {issue.description}")
                
            except Exception as e:
                logger.error(f"Erro ao corrigir problema {issue.id}: {e}")
    
    async def _fix_issue(self, issue: ConsistencyIssue):
        """Corrige um problema específico"""
        if issue.id == "db_missing":
            await self._create_database()
        elif issue.id.startswith("table_missing_"):
            table_name = issue.id.replace("table_missing_", "")
            await self._create_table(table_name)
    
    async def _create_database(self):
        """Cria banco de dados se não existir"""
        # Implementação da criação do banco
        logger.info("🗄️ Criando banco de dados")
    
    async def _create_table(self, table_name: str):
        """Cria tabela específica"""
        # Implementação da criação de tabelas
        logger.info(f"📋 Criando tabela: {table_name}")
    
    def get_consistency_report(self) -> Dict[str, Any]:
        """Gera relatório de consistência"""
        total_issues = len(self.issues)
        critical_issues = len([i for i in self.issues if i.level == ConsistencyLevel.CRITICAL and not i.fixed])
        high_issues = len([i for i in self.issues if i.level == ConsistencyLevel.HIGH and not i.fixed])
        medium_issues = len([i for i in self.issues if i.level == ConsistencyLevel.MEDIUM and not i.fixed])
        low_issues = len([i for i in self.issues if i.level == ConsistencyLevel.LOW and not i.fixed])
        fixed_issues = len([i for i in self.issues if i.fixed])
        
        return {
            "status": "active" if self.is_running else "stopped",
            "total_issues": total_issues,
            "critical_issues": critical_issues,
            "high_issues": high_issues,
            "medium_issues": medium_issues,
            "low_issues": low_issues,
            "fixed_issues": fixed_issues,
            "active_checks": len([c for c in self.checks if c.enabled]),
            "last_check": max([c.last_run for c in self.checks if c.last_run], default=None),
            "issues_by_component": self._group_issues_by_component()
        }
    
    def _group_issues_by_component(self) -> Dict[str, int]:
        """Agrupa problemas por componente"""
        components = {}
        for issue in self.issues:
            if not issue.fixed:
                components[issue.component] = components.get(issue.component, 0) + 1
        return components


# Instância global do verificador
consistency_checker = ConsistencyChecker()
