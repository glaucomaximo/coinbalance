#!/usr/bin/env python
"""
Testes de Integração para CoinBalance
=====================================

Testes abrangentes para todos os endpoints e funcionalidades
do sistema CoinBalance, incluindo os novos sistemas de monitoramento
holístico e Web3-IA.
"""

import asyncio
import json
import time
from typing import Dict, Any, List
import requests
from dataclasses import dataclass

@dataclass
class TestResult:
    """Resultado de um teste"""
    name: str
    success: bool
    response_time: float
    status_code: int
    error: str = None
    data: Dict[str, Any] = None

class CoinBalanceIntegrationTests:
    """Testes de integração para CoinBalance"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[TestResult] = []
        self.session = requests.Session()
        
    def test_endpoint(self, name: str, method: str, endpoint: str, 
                     expected_status: int = 200, **kwargs) -> TestResult:
        """Testa um endpoint específico"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            response = self.session.request(method, url, timeout=30, **kwargs)
            response_time = time.time() - start_time
            
            success = response.status_code == expected_status
            
            result = TestResult(
                name=name,
                success=success,
                response_time=response_time,
                status_code=response.status_code,
                data=response.json() if response.headers.get('content-type', '').startswith('application/json') else None
            )
            
            if not success:
                result.error = f"Expected {expected_status}, got {response.status_code}"
                
        except Exception as e:
            response_time = time.time() - start_time
            result = TestResult(
                name=name,
                success=False,
                response_time=response_time,
                status_code=0,
                error=str(e)
            )
        
        self.results.append(result)
        return result
    
    def run_basic_tests(self):
        """Executa testes básicos"""
        print("🧪 Executando testes básicos...")
        
        # Teste do endpoint raiz
        self.test_endpoint("Root Endpoint", "GET", "/")
        
        # Teste do health check
        self.test_endpoint("Health Check", "GET", "/health")
        
        # Teste do liveness probe
        self.test_endpoint("Liveness Probe", "GET", "/health/live")
        
        # Teste do readiness probe
        self.test_endpoint("Readiness Probe", "GET", "/health/ready")
        
        # Teste das métricas
        self.test_endpoint("Metrics", "GET", "/metrics")
        
        # Teste das informações da API
        self.test_endpoint("API Info", "GET", "/info")
    
    def run_monitoring_tests(self):
        """Executa testes de monitoramento"""
        print("📊 Executando testes de monitoramento...")
        
        # Teste do dashboard de monitoramento
        self.test_endpoint("Monitoring Dashboard", "GET", "/api/v1/monitoring/dashboard")
        
        # Teste do sistema de consciência
        self.test_endpoint("Consciousness System", "GET", "/api/v1/monitoring/consciousness")
        
        # Teste do sistema de segurança
        self.test_endpoint("Security System", "GET", "/api/v1/security/health")
        
        # Teste do sistema de performance
        self.test_endpoint("Performance System", "GET", "/api/v1/monitoring/performance")
    
    def run_holistic_tests(self):
        """Executa testes do sistema holístico"""
        print("🌐 Executando testes do sistema holístico...")
        
        # Teste da saúde do ecossistema
        self.test_endpoint("Ecosystem Health", "GET", "/api/v1/holistic/ecosystem/health")
        
        # Teste dos alertas ativos
        self.test_endpoint("Active Alerts", "GET", "/api/v1/holistic/alerts/active")
        
        # Teste das recomendações
        self.test_endpoint("Recommendations", "GET", "/api/v1/holistic/recommendations")
        
        # Teste da saúde de componentes
        self.test_endpoint("Component Health", "GET", "/api/v1/holistic/components/health")
    
    def run_web3_tests(self):
        """Executa testes Web3"""
        print("🔗 Executando testes Web3...")
        
        # Teste das métricas DeFi
        self.test_endpoint("DeFi Metrics", "GET", "/api/v1/web3/analytics/defi")
        
        # Teste do marketplace NFT
        self.test_endpoint("NFT Marketplace", "GET", "/api/v1/web3/nft/marketplace")
        
        # Teste da governança DAO
        self.test_endpoint("DAO Governance", "GET", "/api/v1/web3/dao/governance")
        
        # Teste da ponte cross-chain
        self.test_endpoint("Cross-Chain Bridge", "GET", "/api/v1/web3/bridge/status")
    
    def run_ai_crypto_tests(self):
        """Executa testes de IA e criptomoedas"""
        print("🤖 Executando testes de IA e criptomoedas...")
        
        # Teste da saúde do ecossistema IA
        self.test_endpoint("AI Ecosystem Health", "GET", "/api/v1/ai-crypto/ecosystem-health")
        
        # Teste das decisões autônomas
        self.test_endpoint("Autonomous Decisions", "GET", "/api/v1/ai-crypto/decisions")
        
        # Teste da criação de criptomoedas
        self.test_endpoint("Crypto Creation", "GET", "/api/v1/ai-crypto/crypto-creation")
        
        # Teste da evolução de tokens
        self.test_endpoint("Token Evolution", "GET", "/api/v1/ai-crypto/token-evolution")
    
    def run_fractal_tests(self):
        """Executa testes fractais"""
        print("🌀 Executando testes fractais...")
        
        # Teste da saúde fractal-Web3
        self.test_endpoint("Fractal-Web3 Health", "GET", "/api/v1/fractal-web3/health")
        
        # Teste dos contratos conscientes
        self.test_endpoint("Conscious Contracts", "GET", "/api/v1/fractal-web3/conscious-contracts")
        
        # Teste da integração fractal
        self.test_endpoint("Fractal Integration", "GET", "/api/v1/fractal-web3/integration")
    
    def run_performance_tests(self):
        """Executa testes de performance"""
        print("⚡ Executando testes de performance...")
        
        # Teste de carga no endpoint raiz
        start_time = time.time()
        for i in range(10):
            self.test_endpoint(f"Load Test {i+1}", "GET", "/")
        load_time = time.time() - start_time
        
        print(f"   ⏱️  10 requisições em {load_time:.2f}s (média: {load_time/10:.3f}s)")
        
        # Teste de carga no health check
        start_time = time.time()
        for i in range(5):
            self.test_endpoint(f"Health Load Test {i+1}", "GET", "/health")
        health_load_time = time.time() - start_time
        
        print(f"   ⏱️  5 health checks em {health_load_time:.2f}s (média: {health_load_time/5:.3f}s)")
    
    def generate_report(self) -> Dict[str, Any]:
        """Gera relatório dos testes"""
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - successful_tests
        
        avg_response_time = sum(r.response_time for r in self.results) / total_tests if total_tests > 0 else 0
        
        # Agrupar por categoria
        categories = {
            "Basic": [r for r in self.results if "Root" in r.name or "Health" in r.name or "Metrics" in r.name or "Info" in r.name],
            "Monitoring": [r for r in self.results if "Monitoring" in r.name or "Consciousness" in r.name or "Security" in r.name or "Performance" in r.name],
            "Holistic": [r for r in self.results if "Ecosystem" in r.name or "Alerts" in r.name or "Recommendations" in r.name or "Component" in r.name],
            "Web3": [r for r in self.results if "DeFi" in r.name or "NFT" in r.name or "DAO" in r.name or "Bridge" in r.name],
            "AI-Crypto": [r for r in self.results if "AI" in r.name or "Autonomous" in r.name or "Crypto" in r.name or "Token" in r.name],
            "Fractal": [r for r in self.results if "Fractal" in r.name or "Conscious" in r.name or "Integration" in r.name],
            "Performance": [r for r in self.results if "Load Test" in r.name]
        }
        
        # Converter TestResult para dict para serialização JSON
        failed_tests_serializable = [
            {
                "name": r.name,
                "success": r.success,
                "response_time": r.response_time,
                "status_code": r.status_code,
                "error": r.error
            }
            for r in self.results if not r.success
        ]
        
        slowest_tests_serializable = [
            {
                "name": r.name,
                "success": r.success,
                "response_time": r.response_time,
                "status_code": r.status_code,
                "error": r.error
            }
            for r in sorted(self.results, key=lambda x: x.response_time, reverse=True)[:5]
        ]
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
                "average_response_time": avg_response_time
            },
            "categories": {},
            "failed_tests": failed_tests_serializable,
            "slowest_tests": slowest_tests_serializable
        }
        
        for category, tests in categories.items():
            if tests:
                category_success = sum(1 for t in tests if t.success)
                report["categories"][category] = {
                    "total": len(tests),
                    "successful": category_success,
                    "failed": len(tests) - category_success,
                    "success_rate": (category_success / len(tests) * 100) if tests else 0
                }
        
        return report
    
    def print_results(self):
        """Imprime resultados dos testes"""
        print("\n" + "="*80)
        print("📋 RELATÓRIO DE TESTES DE INTEGRAÇÃO")
        print("="*80)
        
        report = self.generate_report()
        
        # Resumo geral
        print(f"\n📊 RESUMO GERAL:")
        print(f"   Total de testes: {report['summary']['total_tests']}")
        print(f"   Testes bem-sucedidos: {report['summary']['successful_tests']}")
        print(f"   Testes falharam: {report['summary']['failed_tests']}")
        print(f"   Taxa de sucesso: {report['summary']['success_rate']:.1f}%")
        print(f"   Tempo médio de resposta: {report['summary']['average_response_time']:.3f}s")
        
        # Por categoria
        print(f"\n📂 RESULTADOS POR CATEGORIA:")
        for category, stats in report["categories"].items():
            print(f"   {category}: {stats['successful']}/{stats['total']} ({stats['success_rate']:.1f}%)")
        
        # Testes mais lentos
        print(f"\n🐌 TESTES MAIS LENTOS:")
        for test in report["slowest_tests"]:
            status = "✅" if test.success else "❌"
            print(f"   {status} {test.name}: {test.response_time:.3f}s")
        
        # Testes que falharam
        if report["failed_tests"]:
            print(f"\n❌ TESTES QUE FALHARAM:")
            for test in report["failed_tests"]:
                print(f"   • {test.name}: {test.error}")
        
        print("\n" + "="*80)
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 Iniciando testes de integração do CoinBalance...")
        print("="*80)
        
        start_time = time.time()
        
        # Executar todos os testes
        self.run_basic_tests()
        self.run_monitoring_tests()
        self.run_holistic_tests()
        self.run_web3_tests()
        self.run_ai_crypto_tests()
        self.run_fractal_tests()
        self.run_performance_tests()
        
        total_time = time.time() - start_time
        
        print(f"\n⏱️  Tempo total de execução: {total_time:.2f}s")
        
        # Imprimir resultados
        self.print_results()
        
        return self.generate_report()

def main():
    """Função principal"""
    tester = CoinBalanceIntegrationTests()
    report = tester.run_all_tests()
    
    # Salvar relatório em arquivo
    with open("integration_test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Relatório salvo em: integration_test_report.json")
    
    # Retornar código de saída baseado no sucesso
    if report["summary"]["failed_tests"] == 0:
        print("\n🎉 Todos os testes passaram!")
        return 0
    else:
        print(f"\n⚠️  {report['summary']['failed_tests']} testes falharam!")
        return 1

if __name__ == "__main__":
    exit(main())
