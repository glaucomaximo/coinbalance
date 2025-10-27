#!/usr/bin/env python3
"""
🔧 SCRIPT DE VALIDAÇÃO DE MUDANÇAS - CoinBalance
Valida mudanças antes de commit/PR seguindo protocolo de manutenção
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime


class ChangeValidator:
    """Validador de mudanças seguindo protocolo de manutenção"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.changes: List[str] = []
        
    def validate_all(self) -> bool:
        """Executa todas as validações de mudança"""
        print("🔧 Validação de Mudanças - CoinBalance")
        print("=" * 50)
        
        # Fase 1: Preparação e Análise
        self.check_documentation_consultation()
        self.check_current_state()
        self.analyze_impact()
        
        # Fase 2: Verificação de Qualidade
        self.check_code_formatting()
        self.check_linting()
        self.check_type_checking()
        self.check_security()
        
        # Fase 3: Verificação Arquitetural
        self.check_architecture_compliance()
        self.check_ddd_patterns()
        self.check_solid_principles()
        
        # Fase 4: Verificação de Testes
        self.check_tests()
        self.check_coverage()
        
        # Fase 5: Verificação de Documentação
        self.check_documentation_updates()
        
        self.print_report()
        return len(self.errors) == 0
    
    def check_documentation_consultation(self):
        """Verifica se documentação foi consultada"""
        print("\n📚 Verificando consulta de documentação...")
        
        required_docs = [
            "README.md",
            "docs/RESUMO_REFATORACAO_DDD.md",
            "CONTRIBUTING.md",
            "docs/ARQUITETURA_DETALHADA.md",
            "docs/DECISOES_ARQUITETURAIS.md"
        ]
        
        for doc in required_docs:
            doc_path = self.project_root / doc
            if doc_path.exists():
                # Verificar se foi modificado recentemente (últimas 24h)
                mod_time = doc_path.stat().st_mtime
                now = datetime.now().timestamp()
                if now - mod_time < 86400:  # 24 horas
                    print(f"  ✅ {doc} - consultado recentemente")
                else:
                    self.warnings.append(f"{doc} não foi consultado recentemente")
            else:
                self.errors.append(f"Documentação obrigatória não encontrada: {doc}")
    
    def check_current_state(self):
        """Verifica estado atual do projeto"""
        print("\n🔍 Verificando estado atual...")
        
        # Verificar git status
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                changes = result.stdout.strip().split('\n') if result.stdout.strip() else []
                if changes:
                    print(f"  ✅ {len(changes)} mudanças detectadas")
                    self.changes = changes
                else:
                    print("  ✅ Nenhuma mudança pendente")
            else:
                self.warnings.append("Não foi possível verificar status do git")
                
        except FileNotFoundError:
            self.warnings.append("Git não encontrado - pulando verificação de status")
    
    def analyze_impact(self):
        """Analisa impacto das mudanças"""
        print("\n📊 Analisando impacto das mudanças...")
        
        if not self.changes:
            print("  ✅ Nenhuma mudança para analisar")
            return
        
        # Analisar arquivos modificados
        domain_changes = []
        app_changes = []
        infra_changes = []
        pres_changes = []
        
        for change in self.changes:
            file_path = change.split()[-1] if change.split() else ""
            
            if "src/domain" in file_path:
                domain_changes.append(file_path)
            elif "src/application" in file_path:
                app_changes.append(file_path)
            elif "src/infrastructure" in file_path:
                infra_changes.append(file_path)
            elif "src/presentation" in file_path:
                pres_changes.append(file_path)
        
        # Relatório de impacto
        if domain_changes:
            print(f"  ⚠️ Mudanças no DOMÍNIO: {len(domain_changes)} arquivos")
            print("    Impacto: ALTO - pode afetar regras de negócio")
            
        if app_changes:
            print(f"  ⚠️ Mudanças na APLICAÇÃO: {len(app_changes)} arquivos")
            print("    Impacto: MÉDIO - pode afetar casos de uso")
            
        if infra_changes:
            print(f"  ℹ️ Mudanças na INFRAESTRUTURA: {len(infra_changes)} arquivos")
            print("    Impacto: BAIXO - implementações técnicas")
            
        if pres_changes:
            print(f"  ℹ️ Mudanças na APRESENTAÇÃO: {len(pres_changes)} arquivos")
            print("    Impacto: BAIXO - interface com usuários")
    
    def check_code_formatting(self):
        """Verifica formatação de código"""
        print("\n🎨 Verificando formatação de código...")
        
        try:
            # Black
            result = subprocess.run(
                ["black", "--check", "--diff", "."],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                print("  ✅ Black - formatação OK")
            else:
                self.errors.append("Black - código não formatado")
                print("  ❌ Black - código precisa ser formatado")
                
        except FileNotFoundError:
            self.warnings.append("Black não encontrado")
        
        try:
            # isort
            result = subprocess.run(
                ["isort", "--check-only", "--diff", "."],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                print("  ✅ isort - imports organizados")
            else:
                self.errors.append("isort - imports não organizados")
                print("  ❌ isort - imports precisam ser organizados")
                
        except FileNotFoundError:
            self.warnings.append("isort não encontrado")
    
    def check_linting(self):
        """Verifica linting"""
        print("\n🔍 Verificando linting...")
        
        try:
            result = subprocess.run(
                ["flake8", "."],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                print("  ✅ Flake8 - linting OK")
            else:
                self.errors.append("Flake8 - problemas de linting encontrados")
                print("  ❌ Flake8 - problemas de linting")
                
        except FileNotFoundError:
            self.warnings.append("Flake8 não encontrado")
    
    def check_type_checking(self):
        """Verifica type checking"""
        print("\n🔬 Verificando type checking...")
        
        try:
            result = subprocess.run(
                ["mypy", "src/"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                print("  ✅ MyPy - type checking OK")
            else:
                self.errors.append("MyPy - problemas de tipos encontrados")
                print("  ❌ MyPy - problemas de tipos")
                
        except FileNotFoundError:
            self.warnings.append("MyPy não encontrado")
    
    def check_security(self):
        """Verifica segurança"""
        print("\n🔒 Verificando segurança...")
        
        try:
            result = subprocess.run(
                ["bandit", "-r", "src/", "-f", "json", "-o", "bandit-report.json"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            # Bandit retorna 1 mesmo com warnings, então verificamos o arquivo
            report_path = self.project_root / "bandit-report.json"
            if report_path.exists():
                with open(report_path, 'r') as f:
                    report = json.load(f)
                
                high_severity = [r for r in report.get('results', []) if r.get('issue_severity') == 'HIGH']
                medium_severity = [r for r in report.get('results', []) if r.get('issue_severity') == 'MEDIUM']
                
                if high_severity:
                    self.errors.append(f"Bandit - {len(high_severity)} vulnerabilidades críticas encontradas")
                    print(f"  ❌ Bandit - {len(high_severity)} vulnerabilidades críticas")
                elif medium_severity:
                    self.warnings.append(f"Bandit - {len(medium_severity)} vulnerabilidades médias encontradas")
                    print(f"  ⚠️ Bandit - {len(medium_severity)} vulnerabilidades médias")
                else:
                    print("  ✅ Bandit - sem vulnerabilidades críticas")
            else:
                print("  ✅ Bandit - verificação concluída")
                
        except FileNotFoundError:
            self.warnings.append("Bandit não encontrado")
    
    def check_architecture_compliance(self):
        """Verifica conformidade arquitetural"""
        print("\n🏗️ Verificando conformidade arquitetural...")
        
        try:
            result = subprocess.run(
                ["python", "scripts/check_architecture.py"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                print("  ✅ Arquitetura - conformidade OK")
            else:
                self.errors.append("Arquitetura - problemas de conformidade encontrados")
                print("  ❌ Arquitetura - problemas de conformidade")
                
        except FileNotFoundError:
            self.warnings.append("Script de verificação arquitetural não encontrado")
    
    def check_ddd_patterns(self):
        """Verifica padrões DDD"""
        print("\n💎 Verificando padrões DDD...")
        
        # Verificar se Value Objects são imutáveis
        domain_path = self.project_root / "src" / "domain"
        if domain_path.exists():
            vo_files = list(domain_path.rglob("*value_objects*.py"))
            for vo_file in vo_files:
                try:
                    with open(vo_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if "@dataclass(frozen=True)" in content:
                        print(f"  ✅ {vo_file.name} - Value Object imutável")
                    else:
                        self.warnings.append(f"{vo_file.name} - Value Object pode não ser imutável")
                        
                except Exception as e:
                    self.warnings.append(f"Erro ao verificar {vo_file}: {e}")
    
    def check_solid_principles(self):
        """Verifica princípios SOLID"""
        print("\n🔧 Verificando princípios SOLID...")
        
        # Verificação básica de responsabilidade única
        src_path = self.project_root / "src"
        if src_path.exists():
            py_files = list(src_path.rglob("*.py"))
            large_files = []
            
            for py_file in py_files:
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    if len(lines) > 200:  # Arquivos muito grandes
                        large_files.append(py_file)
                        
                except Exception:
                    continue
            
            if large_files:
                self.warnings.append(f"{len(large_files)} arquivos muito grandes (>200 linhas)")
                print(f"  ⚠️ {len(large_files)} arquivos muito grandes")
            else:
                print("  ✅ Arquivos com tamanho adequado")
    
    def check_tests(self):
        """Verifica testes"""
        print("\n🧪 Verificando testes...")
        
        tests_path = self.project_root / "tests"
        if not tests_path.exists():
            self.errors.append("Diretório de testes não encontrado")
            return
        
        # Verificar se existem testes para arquivos modificados
        if self.changes:
            modified_files = [change.split()[-1] for change in self.changes if change.split()]
            test_files = list(tests_path.rglob("test_*.py"))
            
            missing_tests = []
            for mod_file in modified_files:
                if mod_file.startswith("src/"):
                    # Procurar teste correspondente
                    test_name = f"test_{Path(mod_file).stem}.py"
                    test_found = any(test_name in str(test_file) for test_file in test_files)
                    
                    if not test_found:
                        missing_tests.append(mod_file)
            
            if missing_tests:
                self.warnings.append(f"Testes podem estar faltando para: {len(missing_tests)} arquivos")
                print(f"  ⚠️ {len(missing_tests)} arquivos podem precisar de testes")
            else:
                print("  ✅ Testes adequados para mudanças")
    
    def check_coverage(self):
        """Verifica cobertura de testes"""
        print("\n📊 Verificando cobertura de testes...")
        
        try:
            # Executar testes com cobertura
            result = subprocess.run(
                ["coverage", "run", "-m", "pytest", "tests/"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                # Verificar cobertura
                cov_result = subprocess.run(
                    ["coverage", "report", "--fail-under=80"],
                    capture_output=True,
                    text=True,
                    cwd=self.project_root
                )
                
                if cov_result.returncode == 0:
                    print("  ✅ Cobertura de testes ≥80%")
                else:
                    self.errors.append("Cobertura de testes <80%")
                    print("  ❌ Cobertura de testes insuficiente")
            else:
                self.errors.append("Testes falharam")
                print("  ❌ Testes falharam")
                
        except FileNotFoundError:
            self.warnings.append("Coverage não encontrado")
    
    def check_documentation_updates(self):
        """Verifica atualizações de documentação"""
        print("\n📚 Verificando atualizações de documentação...")
        
        # Verificar se mudanças significativas requerem atualização de documentação
        significant_changes = [
            change for change in self.changes 
            if any(keyword in change.lower() for keyword in [
                "api", "endpoint", "schema", "model", "entity", "value_object"
            ])
        ]
        
        if significant_changes:
            self.warnings.append("Mudanças significativas podem requerer atualização de documentação")
            print("  ⚠️ Mudanças significativas detectadas - verificar documentação")
        else:
            print("  ✅ Mudanças não requerem atualização de documentação")
    
    def print_report(self):
        """Imprime relatório final"""
        print("\n" + "=" * 50)
        print("📊 RELATÓRIO DE VALIDAÇÃO DE MUDANÇAS")
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
            print("\n🎉 PERFEITO! Mudanças validadas com sucesso!")
        elif not self.errors:
            print(f"\n✅ MUDANÇAS APROVADAS! ({len(self.warnings)} avisos)")
        else:
            print(f"\n❌ MUDANÇAS REJEITADAS! ({len(self.errors)} erros, {len(self.warnings)} avisos)")
        
        print("\n" + "=" * 50)
        
        # Recomendações
        if self.errors:
            print("\n🔧 AÇÕES NECESSÁRIAS:")
            print("  1. Corrigir erros listados acima")
            print("  2. Executar novamente a validação")
            print("  3. Consultar documentação se necessário")
        
        if self.warnings:
            print("\n💡 RECOMENDAÇÕES:")
            print("  1. Revisar avisos listados acima")
            print("  2. Considerar melhorias sugeridas")
            print("  3. Atualizar documentação se necessário")


def main():
    """Função principal"""
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = "."
    
    validator = ChangeValidator(project_root)
    success = validator.validate_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
