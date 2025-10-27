#!/usr/bin/env python3
"""
🔍 VERIFICADOR ARQUITETURAL - CoinBalance DDD
Verifica conformidade com padrões Domain-Driven Design e Clean Architecture
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple
import importlib.util


class ArchitectureChecker:
    """Verificador de conformidade arquitetural"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.src_root = self.project_root / "src"
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def check_all(self) -> bool:
        """Executa todas as verificações arquiteturais"""
        print("🏗️ Verificação Arquitetural - CoinBalance DDD")
        print("=" * 50)
        
        checks = [
            self.check_ddd_structure,
            self.check_domain_layer_isolation,
            self.check_application_layer_isolation,
            self.check_infrastructure_layer_isolation,
            self.check_presentation_layer_isolation,
            self.check_dependency_flow,
            self.check_cqrs_pattern,
            self.check_repository_pattern,
            self.check_value_objects,
            self.check_domain_events
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                self.errors.append(f"Erro na verificação {check.__name__}: {e}")
        
        self.print_report()
        return len(self.errors) == 0
    
    def check_ddd_structure(self):
        """Verifica estrutura básica DDD"""
        print("\n📁 Verificando estrutura DDD...")
        
        required_dirs = [
            "src/domain",
            "src/application", 
            "src/infrastructure",
            "src/presentation"
        ]
        
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                self.errors.append(f"Diretório obrigatório não encontrado: {dir_path}")
            else:
                print(f"  ✅ {dir_path}")
    
    def check_domain_layer_isolation(self):
        """Verifica isolamento da camada de domínio"""
        print("\n💎 Verificando isolamento da camada de domínio...")
        
        domain_path = self.src_root / "domain"
        if not domain_path.exists():
            self.errors.append("Camada de domínio não encontrada")
            return
        
        # Verificar imports proibidos na camada de domínio
        forbidden_imports = [
            "fastapi", "flask", "django", "sqlalchemy", "psycopg2",
            "requests", "httpx", "redis", "celery", "pandas", "numpy"
        ]
        
        for py_file in domain_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                for forbidden in forbidden_imports:
                    if forbidden in content:
                        self.errors.append(
                            f"Import proibido em {py_file.relative_to(self.project_root)}: {forbidden}"
                        )
                    else:
                        print(f"  ✅ {py_file.relative_to(self.project_root)} - sem imports proibidos")
                        
            except Exception as e:
                self.warnings.append(f"Erro ao verificar {py_file}: {e}")
    
    def check_application_layer_isolation(self):
        """Verifica isolamento da camada de aplicação"""
        print("\n🎯 Verificando isolamento da camada de aplicação...")
        
        app_path = self.src_root / "application"
        if not app_path.exists():
            self.errors.append("Camada de aplicação não encontrada")
            return
        
        # Verificar se usa apenas interfaces do domínio
        for py_file in app_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Deve importar do domínio, não da infraestrutura
                if "from infrastructure" in content or "import infrastructure" in content:
                    self.errors.append(
                        f"Camada de aplicação não deve importar infraestrutura: {py_file.relative_to(self.project_root)}"
                    )
                else:
                    print(f"  ✅ {py_file.relative_to(self.project_root)} - isolamento OK")
                    
            except Exception as e:
                self.warnings.append(f"Erro ao verificar {py_file}: {e}")
    
    def check_infrastructure_layer_isolation(self):
        """Verifica isolamento da camada de infraestrutura"""
        print("\n🔧 Verificando isolamento da camada de infraestrutura...")
        
        infra_path = self.src_root / "infrastructure"
        if not infra_path.exists():
            self.errors.append("Camada de infraestrutura não encontrada")
            return
        
        # Verificar se implementa interfaces do domínio
        repository_impls = list(infra_path.rglob("*repository*impl*.py"))
        if not repository_impls:
            self.warnings.append("Nenhuma implementação de repositório encontrada")
        else:
            for impl in repository_impls:
                print(f"  ✅ {impl.relative_to(self.project_root)} - implementação encontrada")
    
    def check_presentation_layer_isolation(self):
        """Verifica isolamento da camada de apresentação"""
        print("\n🌐 Verificando isolamento da camada de apresentação...")
        
        pres_path = self.src_root / "presentation"
        if not pres_path.exists():
            self.errors.append("Camada de apresentação não encontrada")
            return
        
        # Verificar se usa apenas casos de uso
        for py_file in pres_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Deve importar da aplicação, não do domínio diretamente
                if "from domain" in content and "from application" not in content:
                    self.warnings.append(
                        f"Camada de apresentação deveria usar casos de uso: {py_file.relative_to(self.project_root)}"
                    )
                else:
                    print(f"  ✅ {py_file.relative_to(self.project_root)} - isolamento OK")
                    
            except Exception as e:
                self.warnings.append(f"Erro ao verificar {py_file}: {e}")
    
    def check_dependency_flow(self):
        """Verifica fluxo de dependências (inward)"""
        print("\n🔄 Verificando fluxo de dependências...")
        
        # Domain não deve depender de nada
        domain_path = self.src_root / "domain"
        if domain_path.exists():
            print("  ✅ Domain - sem dependências externas")
        
        # Application pode depender apenas de Domain
        app_path = self.src_root / "application"
        if app_path.exists():
            print("  ✅ Application - depende apenas de Domain")
        
        # Infrastructure pode depender de Domain e Application
        infra_path = self.src_root / "infrastructure"
        if infra_path.exists():
            print("  ✅ Infrastructure - pode depender de Domain e Application")
        
        # Presentation pode depender de todas as camadas internas
        pres_path = self.src_root / "presentation"
        if pres_path.exists():
            print("  ✅ Presentation - pode depender de todas as camadas internas")
    
    def check_cqrs_pattern(self):
        """Verifica implementação do padrão CQRS"""
        print("\n📊 Verificando padrão CQRS...")
        
        app_path = self.src_root / "application"
        if not app_path.exists():
            self.errors.append("Camada de aplicação não encontrada para verificar CQRS")
            return
        
        # Verificar se existem commands e queries separados
        commands_path = app_path / "wallet" / "commands"
        queries_path = app_path / "wallet" / "queries"
        
        if commands_path.exists():
            command_files = list(commands_path.glob("*.py"))
            if command_files:
                print(f"  ✅ Commands encontrados: {len(command_files)} arquivos")
            else:
                self.warnings.append("Diretório de commands vazio")
        else:
            self.warnings.append("Diretório de commands não encontrado")
        
        if queries_path.exists():
            query_files = list(queries_path.glob("*.py"))
            if query_files:
                print(f"  ✅ Queries encontrados: {len(query_files)} arquivos")
            else:
                self.warnings.append("Diretório de queries vazio")
        else:
            self.warnings.append("Diretório de queries não encontrado")
    
    def check_repository_pattern(self):
        """Verifica implementação do padrão Repository"""
        print("\n🗄️ Verificando padrão Repository...")
        
        # Verificar interface no domínio
        domain_repo_path = self.src_root / "domain" / "wallet" / "repositories"
        if domain_repo_path.exists():
            repo_files = list(domain_repo_path.glob("*.py"))
            if repo_files:
                print(f"  ✅ Interfaces de repositório no domínio: {len(repo_files)} arquivos")
            else:
                self.errors.append("Nenhuma interface de repositório encontrada no domínio")
        else:
            self.errors.append("Diretório de repositórios do domínio não encontrado")
        
        # Verificar implementação na infraestrutura
        infra_repo_path = self.src_root / "infrastructure" / "persistence" / "repositories"
        if infra_repo_path.exists():
            impl_files = list(infra_repo_path.glob("*impl*.py"))
            if impl_files:
                print(f"  ✅ Implementações de repositório na infraestrutura: {len(impl_files)} arquivos")
            else:
                self.warnings.append("Nenhuma implementação de repositório encontrada na infraestrutura")
        else:
            self.warnings.append("Diretório de repositórios da infraestrutura não encontrado")
    
    def check_value_objects(self):
        """Verifica implementação de Value Objects"""
        print("\n💎 Verificando Value Objects...")
        
        domain_path = self.src_root / "domain"
        if not domain_path.exists():
            self.errors.append("Camada de domínio não encontrada para verificar Value Objects")
            return
        
        # Verificar Value Objects compartilhados
        shared_vo_path = domain_path / "shared" / "value_objects"
        if shared_vo_path.exists():
            vo_files = list(shared_vo_path.glob("*.py"))
            if vo_files:
                print(f"  ✅ Value Objects compartilhados: {len(vo_files)} arquivos")
                for vo_file in vo_files:
                    print(f"    - {vo_file.stem}")
            else:
                self.warnings.append("Nenhum Value Object compartilhado encontrado")
        else:
            self.warnings.append("Diretório de Value Objects compartilhados não encontrado")
        
        # Verificar Value Objects específicos do domínio
        wallet_vo_path = domain_path / "wallet" / "value_objects"
        if wallet_vo_path.exists():
            wallet_vo_files = list(wallet_vo_path.glob("*.py"))
            if wallet_vo_files:
                print(f"  ✅ Value Objects do Wallet: {len(wallet_vo_files)} arquivos")
                for vo_file in wallet_vo_files:
                    print(f"    - {vo_file.stem}")
            else:
                self.warnings.append("Nenhum Value Object do Wallet encontrado")
        else:
            self.warnings.append("Diretório de Value Objects do Wallet não encontrado")
    
    def check_domain_events(self):
        """Verifica implementação de Domain Events"""
        print("\n📢 Verificando Domain Events...")
        
        domain_path = self.src_root / "domain"
        if not domain_path.exists():
            self.errors.append("Camada de domínio não encontrada para verificar Domain Events")
            return
        
        # Verificar sistema de eventos compartilhado
        shared_events_path = domain_path / "shared" / "domain_events"
        if shared_events_path.exists():
            event_files = list(shared_events_path.glob("*.py"))
            if event_files:
                print(f"  ✅ Sistema de eventos compartilhado: {len(event_files)} arquivos")
                for event_file in event_files:
                    print(f"    - {event_file.stem}")
            else:
                self.warnings.append("Nenhum arquivo de sistema de eventos encontrado")
        else:
            self.warnings.append("Diretório de sistema de eventos não encontrado")
        
        # Verificar eventos específicos do domínio
        wallet_events_path = domain_path / "wallet" / "events"
        if wallet_events_path.exists():
            wallet_event_files = list(wallet_events_path.glob("*.py"))
            if wallet_event_files:
                print(f"  ✅ Eventos do Wallet: {len(wallet_event_files)} arquivos")
                for event_file in wallet_event_files:
                    print(f"    - {event_file.stem}")
            else:
                self.warnings.append("Nenhum evento do Wallet encontrado")
        else:
            self.warnings.append("Diretório de eventos do Wallet não encontrado")
    
    def print_report(self):
        """Imprime relatório final"""
        print("\n" + "=" * 50)
        print("📊 RELATÓRIO DE VERIFICAÇÃO ARQUITETURAL")
        print("=" * 50)
        
        if self.errors:
            print(f"\n❌ ERROS ENCONTRADOS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n⚠️ AVISOS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if not self.errors and not self.warnings:
            print("\n🎉 PERFEITO! Arquitetura 100% conforme!")
        elif not self.errors:
            print(f"\n✅ ARQUITETURA CONFORME! ({len(self.warnings)} avisos)")
        else:
            print(f"\n❌ ARQUITETURA NÃO CONFORME! ({len(self.errors)} erros, {len(self.warnings)} avisos)")
        
        print("\n" + "=" * 50)


def main():
    """Função principal"""
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = "."
    
    checker = ArchitectureChecker(project_root)
    success = checker.check_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
