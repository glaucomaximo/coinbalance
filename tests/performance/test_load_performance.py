#!/usr/bin/env python
"""
Testes de Carga e Performance para CoinBalance
===============================================

Script para realizar testes de carga, stress e performance
do sistema CoinBalance, incluindo análise de métricas
e geração de relatórios detalhados.
"""

import asyncio
import httpx
import time
import statistics
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import numpy as np

@dataclass
class LoadTestResult:
    """Resultado de um teste de carga"""
    endpoint: str
    method: str
    response_time: float
    status_code: int
    success: bool
    timestamp: float
    error: str = None

class CoinBalanceLoadTester:
    """Testador de carga para CoinBalance"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[LoadTestResult] = []
        
    async def test_endpoint(self, session: aiohttp.ClientSession, 
                          endpoint: str, method: str = "GET") -> LoadTestResult:
        """Testa um endpoint específico"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            async with session.request(method, url, timeout=30) as response:
                response_time = time.time() - start_time
                content = await response.text()
                
                return LoadTestResult(
                    endpoint=endpoint,
                    method=method,
                    response_time=response_time,
                    status_code=response.status,
                    success=200 <= response.status < 300,
                    timestamp=start_time
                )
                
        except Exception as e:
            response_time = time.time() - start_time
            return LoadTestResult(
                endpoint=endpoint,
                method=method,
                response_time=response_time,
                status_code=0,
                success=False,
                timestamp=start_time,
                error=str(e)
            )
    
    async def run_concurrent_tests(self, endpoint: str, concurrent_users: int, 
                                 duration_seconds: int) -> List[LoadTestResult]:
        """Executa testes concorrentes por um período de tempo"""
        print(f"🚀 Testando {endpoint} com {concurrent_users} usuários por {duration_seconds}s...")
        
        results = []
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            while time.time() - start_time < duration_seconds:
                # Criar tarefas concorrentes
                tasks = []
                for _ in range(concurrent_users):
                    task = self.test_endpoint(session, endpoint)
                    tasks.append(task)
                
                # Executar todas as tarefas
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Processar resultados
                for result in batch_results:
                    if isinstance(result, LoadTestResult):
                        results.append(result)
                    elif isinstance(result, Exception):
                        results.append(LoadTestResult(
                            endpoint=endpoint,
                            method="GET",
                            response_time=0,
                            status_code=0,
                            success=False,
                            timestamp=time.time(),
                            error=str(result)
                        ))
                
                # Pequena pausa entre batches
                await asyncio.sleep(0.1)
        
        return results
    
    def analyze_results(self, results: List[LoadTestResult]) -> Dict[str, Any]:
        """Analisa resultados dos testes"""
        if not results:
            return {}
        
        response_times = [r.response_time for r in results if r.success]
        success_count = sum(1 for r in results if r.success)
        total_count = len(results)
        
        if not response_times:
            return {
                "total_requests": total_count,
                "successful_requests": success_count,
                "failed_requests": total_count - success_count,
                "success_rate": 0,
                "avg_response_time": 0,
                "min_response_time": 0,
                "max_response_time": 0,
                "p95_response_time": 0,
                "p99_response_time": 0,
                "requests_per_second": 0
            }
        
        return {
            "total_requests": total_count,
            "successful_requests": success_count,
            "failed_requests": total_count - success_count,
            "success_rate": (success_count / total_count) * 100,
            "avg_response_time": statistics.mean(response_times),
            "min_response_time": min(response_times),
            "max_response_time": max(response_times),
            "p95_response_time": np.percentile(response_times, 95),
            "p99_response_time": np.percentile(response_times, 99),
            "requests_per_second": total_count / (max(r.timestamp for r in results) - min(r.timestamp for r in results)) if results else 0
        }
    
    def generate_charts(self, results: List[LoadTestResult], output_dir: str = "load_test_charts"):
        """Gera gráficos dos resultados"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Gráfico de tempo de resposta ao longo do tempo
        timestamps = [r.timestamp for r in results]
        response_times = [r.response_time for r in results]
        
        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, response_times, alpha=0.7)
        plt.title("Response Time Over Time")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Response Time (seconds)")
        plt.grid(True)
        plt.savefig(f"{output_dir}/response_time_over_time.png")
        plt.close()
        
        # Histograma de tempos de resposta
        plt.figure(figsize=(10, 6))
        plt.hist(response_times, bins=50, alpha=0.7)
        plt.title("Response Time Distribution")
        plt.xlabel("Response Time (seconds)")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.savefig(f"{output_dir}/response_time_distribution.png")
        plt.close()
        
        # Gráfico de taxa de sucesso
        success_rates = []
        window_size = 100
        for i in range(0, len(results), window_size):
            window = results[i:i+window_size]
            success_rate = sum(1 for r in window if r.success) / len(window) * 100
            success_rates.append(success_rate)
        
        plt.figure(figsize=(12, 6))
        plt.plot(success_rates)
        plt.title("Success Rate Over Time")
        plt.xlabel("Time Window")
        plt.ylabel("Success Rate (%)")
        plt.grid(True)
        plt.savefig(f"{output_dir}/success_rate_over_time.png")
        plt.close()
        
        print(f"📊 Gráficos salvos em: {output_dir}/")
    
    async def run_comprehensive_load_tests(self):
        """Executa testes de carga abrangentes"""
        print("🔥 Iniciando testes de carga e performance...")
        print("="*80)
        
        test_scenarios = [
            {
                "name": "Root Endpoint - Light Load",
                "endpoint": "/",
                "concurrent_users": 10,
                "duration": 30
            },
            {
                "name": "Root Endpoint - Medium Load",
                "endpoint": "/",
                "concurrent_users": 50,
                "duration": 60
            },
            {
                "name": "Root Endpoint - Heavy Load",
                "endpoint": "/",
                "concurrent_users": 100,
                "duration": 120
            },
            {
                "name": "Health Check - Light Load",
                "endpoint": "/health",
                "concurrent_users": 20,
                "duration": 30
            },
            {
                "name": "Health Check - Medium Load",
                "endpoint": "/health",
                "concurrent_users": 100,
                "duration": 60
            },
            {
                "name": "Monitoring Dashboard - Light Load",
                "endpoint": "/api/v1/monitoring/dashboard",
                "concurrent_users": 5,
                "duration": 30
            },
            {
                "name": "Holistic Health - Light Load",
                "endpoint": "/api/v1/holistic/ecosystem/health",
                "concurrent_users": 10,
                "duration": 30
            }
        ]
        
        all_results = {}
        
        for scenario in test_scenarios:
            print(f"\n🧪 {scenario['name']}")
            print("-" * 50)
            
            results = await self.run_concurrent_tests(
                scenario["endpoint"],
                scenario["concurrent_users"],
                scenario["duration"]
            )
            
            analysis = self.analyze_results(results)
            all_results[scenario["name"]] = analysis
            
            # Imprimir resultados
            print(f"   Total de requisições: {analysis['total_requests']}")
            print(f"   Requisições bem-sucedidas: {analysis['successful_requests']}")
            print(f"   Taxa de sucesso: {analysis['success_rate']:.1f}%")
            print(f"   Tempo médio de resposta: {analysis['avg_response_time']:.3f}s")
            print(f"   P95 tempo de resposta: {analysis['p95_response_time']:.3f}s")
            print(f"   P99 tempo de resposta: {analysis['p99_response_time']:.3f}s")
            print(f"   Requisições por segundo: {analysis['requests_per_second']:.1f}")
            
            # Gerar gráficos para este cenário
            self.generate_charts(results, f"load_test_charts/{scenario['name'].replace(' ', '_').lower()}")
        
        return all_results
    
    async def run_stress_test(self):
        """Executa teste de stress"""
        print("\n💥 Iniciando teste de stress...")
        print("="*50)
        
        # Teste de stress gradual
        stress_levels = [
            {"users": 50, "duration": 30},
            {"users": 100, "duration": 30},
            {"users": 200, "duration": 30},
            {"users": 500, "duration": 30},
            {"users": 1000, "duration": 30}
        ]
        
        stress_results = {}
        
        for level in stress_levels:
            print(f"\n🔥 Stress Level: {level['users']} usuários por {level['duration']}s")
            
            results = await self.run_concurrent_tests(
                "/",
                level["users"],
                level["duration"]
            )
            
            analysis = self.analyze_results(results)
            stress_results[f"{level['users']}_users"] = analysis
            
            print(f"   Taxa de sucesso: {analysis['success_rate']:.1f}%")
            print(f"   Tempo médio de resposta: {analysis['avg_response_time']:.3f}s")
            print(f"   Requisições por segundo: {analysis['requests_per_second']:.1f}")
            
            # Se a taxa de sucesso cair abaixo de 95%, parar o teste
            if analysis['success_rate'] < 95:
                print("   ⚠️  Taxa de sucesso abaixo de 95% - parando teste de stress")
                break
        
        return stress_results
    
    async def run_endpoint_comparison(self):
        """Compara performance de diferentes endpoints"""
        print("\n📊 Comparando performance de endpoints...")
        print("="*50)
        
        endpoints = [
            "/",
            "/health",
            "/health/simple",
            "/metrics",
            "/info",
            "/api/v1/monitoring/dashboard",
            "/api/v1/holistic/ecosystem/health"
        ]
        
        comparison_results = {}
        
        for endpoint in endpoints:
            print(f"\n🔍 Testando {endpoint}")
            
            results = await self.run_concurrent_tests(endpoint, 20, 30)
            analysis = self.analyze_results(results)
            comparison_results[endpoint] = analysis
            
            print(f"   Taxa de sucesso: {analysis['success_rate']:.1f}%")
            print(f"   Tempo médio de resposta: {analysis['avg_response_time']:.3f}s")
            print(f"   P95 tempo de resposta: {analysis['p95_response_time']:.3f}s")
        
        return comparison_results
    
    def generate_report(self, load_results: Dict, stress_results: Dict, 
                       comparison_results: Dict) -> Dict[str, Any]:
        """Gera relatório completo dos testes"""
        report = {
            "test_summary": {
                "load_tests": len(load_results),
                "stress_tests": len(stress_results),
                "endpoint_comparisons": len(comparison_results),
                "total_endpoints_tested": len(comparison_results)
            },
            "load_test_results": load_results,
            "stress_test_results": stress_results,
            "endpoint_comparison": comparison_results,
            "recommendations": []
        }
        
        # Gerar recomendações
        recommendations = []
        
        # Analisar resultados de carga
        for test_name, results in load_results.items():
            if results['success_rate'] < 99:
                recommendations.append(f"Melhorar taxa de sucesso para {test_name}: {results['success_rate']:.1f}%")
            
            if results['avg_response_time'] > 1.0:
                recommendations.append(f"Otimizar tempo de resposta para {test_name}: {results['avg_response_time']:.3f}s")
        
        # Analisar resultados de stress
        for test_name, results in stress_results.items():
            if results['success_rate'] < 95:
                recommendations.append(f"Melhorar resiliência para {test_name}: {results['success_rate']:.1f}%")
        
        # Analisar comparação de endpoints
        slowest_endpoint = max(comparison_results.items(), key=lambda x: x[1]['avg_response_time'])
        if slowest_endpoint[1]['avg_response_time'] > 0.5:
            recommendations.append(f"Otimizar endpoint mais lento: {slowest_endpoint[0]} ({slowest_endpoint[1]['avg_response_time']:.3f}s)")
        
        report["recommendations"] = recommendations
        
        return report
    
    async def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 Iniciando testes de carga e performance do CoinBalance...")
        print("="*80)
        
        start_time = time.time()
        
        # Executar testes de carga
        load_results = await self.run_comprehensive_load_tests()
        
        # Executar testes de stress
        stress_results = await self.run_stress_test()
        
        # Executar comparação de endpoints
        comparison_results = await self.run_endpoint_comparison()
        
        total_time = time.time() - start_time
        
        # Gerar relatório
        report = self.generate_report(load_results, stress_results, comparison_results)
        
        print(f"\n⏱️  Tempo total de execução: {total_time:.2f}s")
        
        # Imprimir resumo
        print("\n📋 RESUMO DOS TESTES")
        print("="*50)
        print(f"Testes de carga executados: {report['test_summary']['load_tests']}")
        print(f"Testes de stress executados: {report['test_summary']['stress_tests']}")
        print(f"Endpoints comparados: {report['test_summary']['endpoint_comparisons']}")
        
        if report["recommendations"]:
            print(f"\n💡 RECOMENDAÇÕES:")
            for rec in report["recommendations"]:
                print(f"   • {rec}")
        
        # Salvar relatório
        with open("load_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Relatório salvo em: load_test_report.json")
        print(f"📊 Gráficos salvos em: load_test_charts/")
        
        return report

async def main():
    """Função principal"""
    tester = CoinBalanceLoadTester()
    report = await tester.run_all_tests()
    
    # Retornar código de saída baseado nos resultados
    if not report["recommendations"]:
        print("\n🎉 Todos os testes passaram sem recomendações!")
        return 0
    else:
        print(f"\n⚠️  {len(report['recommendations'])} recomendações geradas!")
        return 1

if __name__ == "__main__":
    exit(asyncio.run(main()))
