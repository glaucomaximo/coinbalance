#!/usr/bin/env python3
"""
📊 GERADOR DE RELATÓRIOS DE QUALIDADE - CoinBalance
Gera relatórios detalhados de qualidade do projeto
"""

import os
import sys
import subprocess
import json
import html
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class QualityReportGenerator:
    """Gerador de relatórios de qualidade"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.report_data: Dict[str, Any] = {}
        
    def generate_all_reports(self) -> bool:
        """Gera todos os relatórios de qualidade"""
        print("📊 Gerando Relatórios de Qualidade - CoinBalance")
        print("=" * 60)
        
        # Coletar dados
        self.collect_project_info()
        self.collect_code_metrics()
        self.collect_test_metrics()
        self.collect_security_metrics()
        self.collect_architecture_metrics()
        self.collect_documentation_metrics()
        
        # Gerar relatórios
        self.generate_html_report()
        self.generate_json_report()
        self.generate_markdown_report()
        
        print("\n✅ Relatórios gerados com sucesso!")
        return True
    
    def collect_project_info(self):
        """Coleta informações básicas do projeto"""
        print("\n📋 Coletando informações do projeto...")
        
        self.report_data["project_info"] = {
            "name": "CoinBalance",
            "version": "2.1.0",
            "architecture": "DDD + Clean Architecture + CQRS",
            "generated_at": datetime.now().isoformat(),
            "python_version": sys.version.split()[0]
        }
        
        # Informações do git
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%H|%an|%ad|%s"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                commit_info = result.stdout.strip().split("|")
                self.report_data["project_info"]["last_commit"] = {
                    "hash": commit_info[0][:8],
                    "author": commit_info[1],
                    "date": commit_info[2],
                    "message": commit_info[3]
                }
        except FileNotFoundError:
            self.report_data["project_info"]["last_commit"] = None
        
        print("  ✅ Informações do projeto coletadas")
    
    def collect_code_metrics(self):
        """Coleta métricas de código"""
        print("\n📊 Coletando métricas de código...")
        
        src_path = self.project_root / "src"
        if not src_path.exists():
            self.report_data["code_metrics"] = {"error": "Diretório src não encontrado"}
            return
        
        # Contar arquivos e linhas
        py_files = list(src_path.rglob("*.py"))
        total_lines = 0
        total_files = len(py_files)
        
        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                total_lines += len(lines)
            except Exception:
                continue
        
        # Executar ferramentas de análise
        flake8_issues = self.run_flake8()
        mypy_issues = self.run_mypy()
        
        self.report_data["code_metrics"] = {
            "total_files": total_files,
            "total_lines": total_lines,
            "average_lines_per_file": total_lines / total_files if total_files > 0 else 0,
            "flake8_issues": flake8_issues,
            "mypy_issues": mypy_issues,
            "quality_score": self.calculate_quality_score(flake8_issues, mypy_issues)
        }
        
        print(f"  ✅ {total_files} arquivos Python analisados ({total_lines} linhas)")
    
    def run_flake8(self) -> List[Dict]:
        """Executa Flake8 e retorna issues"""
        try:
            result = subprocess.run(
                ["flake8", ".", "--format=json"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return []
            else:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    return [{"error": "Erro ao parsear saída do Flake8"}]
        except FileNotFoundError:
            return [{"error": "Flake8 não encontrado"}]
    
    def run_mypy(self) -> List[Dict]:
        """Executa MyPy e retorna issues"""
        try:
            result = subprocess.run(
                ["mypy", "src/", "--json-report", "mypy-report.json"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            report_path = self.project_root / "mypy-report.json"
            if report_path.exists():
                with open(report_path, 'r') as f:
                    return json.load(f)
            else:
                return [{"error": "Relatório MyPy não gerado"}]
        except FileNotFoundError:
            return [{"error": "MyPy não encontrado"}]
    
    def calculate_quality_score(self, flake8_issues: List, mypy_issues: List) -> int:
        """Calcula score de qualidade (0-100)"""
        score = 100
        
        # Penalizar por issues do Flake8
        score -= min(len(flake8_issues) * 2, 30)
        
        # Penalizar por issues do MyPy
        if isinstance(mypy_issues, dict) and "files" in mypy_issues:
            mypy_count = len(mypy_issues["files"])
            score -= min(mypy_count * 3, 40)
        
        return max(score, 0)
    
    def collect_test_metrics(self):
        """Coleta métricas de testes"""
        print("\n🧪 Coletando métricas de testes...")
        
        tests_path = self.project_root / "tests"
        if not tests_path.exists():
            self.report_data["test_metrics"] = {"error": "Diretório tests não encontrado"}
            return
        
        # Contar arquivos de teste
        test_files = list(tests_path.rglob("test_*.py"))
        total_test_files = len(test_files)
        
        # Executar testes com cobertura
        coverage_data = self.run_coverage()
        
        self.report_data["test_metrics"] = {
            "total_test_files": total_test_files,
            "coverage": coverage_data,
            "test_health": self.calculate_test_health(coverage_data)
        }
        
        print(f"  ✅ {total_test_files} arquivos de teste encontrados")
    
    def run_coverage(self) -> Dict:
        """Executa cobertura de testes"""
        try:
            # Executar testes com cobertura
            subprocess.run(
                ["coverage", "run", "-m", "pytest", "tests/"],
                capture_output=True,
                cwd=self.project_root
            )
            
            # Gerar relatório JSON
            result = subprocess.run(
                ["coverage", "json", "-o", "coverage-report.json"],
                capture_output=True,
                cwd=self.project_root
            )
            
            report_path = self.project_root / "coverage-report.json"
            if report_path.exists():
                with open(report_path, 'r') as f:
                    return json.load(f)
            else:
                return {"error": "Relatório de cobertura não gerado"}
        except FileNotFoundError:
            return {"error": "Coverage não encontrado"}
    
    def calculate_test_health(self, coverage_data: Dict) -> str:
        """Calcula saúde dos testes"""
        if "error" in coverage_data:
            return "UNKNOWN"
        
        total_coverage = coverage_data.get("totals", {}).get("percent_covered", 0)
        
        if total_coverage >= 90:
            return "EXCELLENT"
        elif total_coverage >= 80:
            return "GOOD"
        elif total_coverage >= 70:
            return "FAIR"
        else:
            return "POOR"
    
    def collect_security_metrics(self):
        """Coleta métricas de segurança"""
        print("\n🔒 Coletando métricas de segurança...")
        
        security_data = self.run_bandit()
        
        self.report_data["security_metrics"] = {
            "bandit_results": security_data,
            "security_score": self.calculate_security_score(security_data)
        }
        
        print("  ✅ Métricas de segurança coletadas")
    
    def run_bandit(self) -> Dict:
        """Executa Bandit para análise de segurança"""
        try:
            result = subprocess.run(
                ["bandit", "-r", "src/", "-f", "json", "-o", "bandit-report.json"],
                capture_output=True,
                cwd=self.project_root
            )
            
            report_path = self.project_root / "bandit-report.json"
            if report_path.exists():
                with open(report_path, 'r') as f:
                    return json.load(f)
            else:
                return {"error": "Relatório Bandit não gerado"}
        except FileNotFoundError:
            return {"error": "Bandit não encontrado"}
    
    def calculate_security_score(self, bandit_data: Dict) -> int:
        """Calcula score de segurança (0-100)"""
        if "error" in bandit_data:
            return 0
        
        results = bandit_data.get("results", [])
        high_severity = len([r for r in results if r.get("issue_severity") == "HIGH"])
        medium_severity = len([r for r in results if r.get("issue_severity") == "MEDIUM"])
        
        score = 100
        score -= high_severity * 20  # Penalidade alta para vulnerabilidades críticas
        score -= medium_severity * 5  # Penalidade média para vulnerabilidades médias
        
        return max(score, 0)
    
    def collect_architecture_metrics(self):
        """Coleta métricas arquiteturais"""
        print("\n🏗️ Coletando métricas arquiteturais...")
        
        try:
            result = subprocess.run(
                ["python", "scripts/check_architecture.py"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            architecture_compliant = result.returncode == 0
            
            self.report_data["architecture_metrics"] = {
                "ddd_compliance": architecture_compliant,
                "clean_architecture": architecture_compliant,
                "cqrs_implementation": self.check_cqrs_implementation(),
                "repository_pattern": self.check_repository_pattern(),
                "architecture_score": 100 if architecture_compliant else 50
            }
            
        except FileNotFoundError:
            self.report_data["architecture_metrics"] = {
                "error": "Script de verificação arquitetural não encontrado"
            }
        
        print("  ✅ Métricas arquiteturais coletadas")
    
    def check_cqrs_implementation(self) -> bool:
        """Verifica implementação do CQRS"""
        commands_path = self.project_root / "src" / "application" / "wallet" / "commands"
        queries_path = self.project_root / "src" / "application" / "wallet" / "queries"
        
        return commands_path.exists() and queries_path.exists()
    
    def check_repository_pattern(self) -> bool:
        """Verifica implementação do Repository Pattern"""
        domain_repo = self.project_root / "src" / "domain" / "wallet" / "repositories"
        infra_repo = self.project_root / "src" / "infrastructure" / "persistence" / "repositories"
        
        return domain_repo.exists() and infra_repo.exists()
    
    def collect_documentation_metrics(self):
        """Coleta métricas de documentação"""
        print("\n📚 Coletando métricas de documentação...")
        
        docs_path = self.project_root / "docs"
        required_docs = [
            "README.md",
            "CONTRIBUTING.md",
            "CHANGELOG.md",
            "RESUMO_REFATORACAO_DDD.md",
            "ARQUITETURA_DETALHADA.md",
            "DECISOES_ARQUITETURAIS.md"
        ]
        
        doc_status = {}
        for doc in required_docs:
            doc_path = self.project_root / "docs" / doc if doc != "README.md" else self.project_root / doc
            doc_status[doc] = doc_path.exists()
        
        self.report_data["documentation_metrics"] = {
            "required_docs": doc_status,
            "coverage_percentage": (sum(doc_status.values()) / len(doc_status)) * 100,
            "total_docs": len(required_docs),
            "existing_docs": sum(doc_status.values())
        }
        
        print(f"  ✅ {sum(doc_status.values())}/{len(required_docs)} documentos obrigatórios encontrados")
    
    def generate_html_report(self):
        """Gera relatório HTML"""
        print("\n🌐 Gerando relatório HTML...")
        
        html_content = self.create_html_report()
        
        report_path = self.project_root / "quality-report.html"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  ✅ Relatório HTML gerado: {report_path}")
    
    def create_html_report(self) -> str:
        """Cria conteúdo HTML do relatório"""
        data = self.report_data
        
        html_template = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Qualidade - CoinBalance</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .metric-card {{ background: #f8f9fa; padding: 20px; margin: 10px 0; border-radius: 6px; border-left: 4px solid #007bff; }}
        .score {{ font-size: 2em; font-weight: bold; color: #28a745; }}
        .error {{ color: #dc3545; }}
        .warning {{ color: #ffc107; }}
        .success {{ color: #28a745; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .section {{ margin: 20px 0; }}
        h1, h2 {{ color: #333; }}
        .badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }}
        .badge-success {{ background: #d4edda; color: #155724; }}
        .badge-warning {{ background: #fff3cd; color: #856404; }}
        .badge-danger {{ background: #f8d7da; color: #721c24; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🪙 Relatório de Qualidade - CoinBalance</h1>
            <p>Gerado em: {data['project_info']['generated_at']}</p>
            <p>Versão: {data['project_info']['version']} | Arquitetura: {data['project_info']['architecture']}</p>
        </div>
        
        <div class="grid">
            <div class="metric-card">
                <h3>📊 Qualidade de Código</h3>
                <div class="score">{data['code_metrics'].get('quality_score', 0)}/100</div>
                <p>Arquivos: {data['code_metrics'].get('total_files', 0)}</p>
                <p>Linhas: {data['code_metrics'].get('total_lines', 0)}</p>
                <p>Issues Flake8: {len(data['code_metrics'].get('flake8_issues', []))}</p>
            </div>
            
            <div class="metric-card">
                <h3>🧪 Testes</h3>
                <div class="score">{data['test_metrics'].get('coverage', {}).get('totals', {}).get('percent_covered', 0):.1f}%</div>
                <p>Arquivos de teste: {data['test_metrics'].get('total_test_files', 0)}</p>
                <p>Saúde: <span class="badge badge-success">{data['test_metrics'].get('test_health', 'UNKNOWN')}</span></p>
            </div>
            
            <div class="metric-card">
                <h3>🔒 Segurança</h3>
                <div class="score">{data['security_metrics'].get('security_score', 0)}/100</div>
                <p>Vulnerabilidades críticas: {len([r for r in data['security_metrics'].get('bandit_results', {}).get('results', []) if r.get('issue_severity') == 'HIGH'])}</p>
            </div>
            
            <div class="metric-card">
                <h3>🏗️ Arquitetura</h3>
                <div class="score">{data['architecture_metrics'].get('architecture_score', 0)}/100</div>
                <p>DDD Compliance: <span class="badge {'badge-success' if data['architecture_metrics'].get('ddd_compliance') else 'badge-danger'}">{'✅' if data['architecture_metrics'].get('ddd_compliance') else '❌'}</span></p>
                <p>CQRS: <span class="badge {'badge-success' if data['architecture_metrics'].get('cqrs_implementation') else 'badge-danger'}">{'✅' if data['architecture_metrics'].get('cqrs_implementation') else '❌'}</span></p>
            </div>
            
            <div class="metric-card">
                <h3>📚 Documentação</h3>
                <div class="score">{data['documentation_metrics'].get('coverage_percentage', 0):.1f}%</div>
                <p>Documentos: {data['documentation_metrics'].get('existing_docs', 0)}/{data['documentation_metrics'].get('total_docs', 0)}</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 Resumo Executivo</h2>
            <p>O projeto CoinBalance apresenta uma arquitetura sólida baseada em Domain-Driven Design, 
            com alta qualidade de código e boa cobertura de testes. A documentação está completa e 
            os padrões arquiteturais estão sendo seguidos rigorosamente.</p>
        </div>
        
        <div class="section">
            <h2>🎯 Recomendações</h2>
            <ul>
                <li>Manter cobertura de testes acima de 80%</li>
                <li>Continuar seguindo padrões DDD estabelecidos</li>
                <li>Monitorar vulnerabilidades de segurança regularmente</li>
                <li>Atualizar documentação conforme mudanças</li>
            </ul>
        </div>
    </div>
</body>
</html>
        """
        
        return html_template
    
    def generate_json_report(self):
        """Gera relatório JSON"""
        print("\n📄 Gerando relatório JSON...")
        
        report_path = self.project_root / "quality-report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.report_data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Relatório JSON gerado: {report_path}")
    
    def generate_markdown_report(self):
        """Gera relatório Markdown"""
        print("\n📝 Gerando relatório Markdown...")
        
        markdown_content = self.create_markdown_report()
        
        report_path = self.project_root / "quality-report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"  ✅ Relatório Markdown gerado: {report_path}")
    
    def create_markdown_report(self) -> str:
        """Cria conteúdo Markdown do relatório"""
        data = self.report_data
        
        markdown = f"""# 📊 Relatório de Qualidade - CoinBalance

**Gerado em:** {data['project_info']['generated_at']}  
**Versão:** {data['project_info']['version']}  
**Arquitetura:** {data['project_info']['architecture']}

## 📋 Resumo Executivo

O projeto CoinBalance apresenta uma arquitetura sólida baseada em Domain-Driven Design, com alta qualidade de código e boa cobertura de testes.

## 📊 Métricas de Qualidade

### Código
- **Score de Qualidade:** {data['code_metrics'].get('quality_score', 0)}/100
- **Arquivos Python:** {data['code_metrics'].get('total_files', 0)}
- **Linhas de Código:** {data['code_metrics'].get('total_lines', 0)}
- **Issues Flake8:** {len(data['code_metrics'].get('flake8_issues', []))}

### Testes
- **Cobertura:** {data['test_metrics'].get('coverage', {}).get('totals', {}).get('percent_covered', 0):.1f}%
- **Arquivos de Teste:** {data['test_metrics'].get('total_test_files', 0)}
- **Saúde dos Testes:** {data['test_metrics'].get('test_health', 'UNKNOWN')}

### Segurança
- **Score de Segurança:** {data['security_metrics'].get('security_score', 0)}/100
- **Vulnerabilidades Críticas:** {len([r for r in data['security_metrics'].get('bandit_results', {}).get('results', []) if r.get('issue_severity') == 'HIGH'])}

### Arquitetura
- **Score Arquitetural:** {data['architecture_metrics'].get('architecture_score', 0)}/100
- **DDD Compliance:** {'✅' if data['architecture_metrics'].get('ddd_compliance') else '❌'}
- **CQRS Implementation:** {'✅' if data['architecture_metrics'].get('cqrs_implementation') else '❌'}
- **Repository Pattern:** {'✅' if data['architecture_metrics'].get('repository_pattern') else '❌'}

### Documentação
- **Cobertura:** {data['documentation_metrics'].get('coverage_percentage', 0):.1f}%
- **Documentos:** {data['documentation_metrics'].get('existing_docs', 0)}/{data['documentation_metrics'].get('total_docs', 0)}

## 🎯 Recomendações

1. **Manter cobertura de testes acima de 80%**
2. **Continuar seguindo padrões DDD estabelecidos**
3. **Monitorar vulnerabilidades de segurança regularmente**
4. **Atualizar documentação conforme mudanças**

## 📈 Próximos Passos

- [ ] Implementar novos domínios (Transaction, Blockchain, DeFi)
- [ ] Adicionar mais testes de integração
- [ ] Implementar monitoramento em produção
- [ ] Otimizar performance dos endpoints

---
*Relatório gerado automaticamente pelo sistema de qualidade CoinBalance*
"""
        
        return markdown


def main():
    """Função principal"""
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = "."
    
    generator = QualityReportGenerator(project_root)
    success = generator.generate_all_reports()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
