#!/usr/bin/env python
"""
Testes de Carga e Performance para CoinBalance Enterprise
=========================================================

Script para realizar testes de carga, stress e performance
do sistema CoinBalance Enterprise, incluindo análise de métricas
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
    """Testador de carga para CoinBalance Enterprise"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[LoadTestResult] = []
        
    async def test_endpoint(self, client: httpx.AsyncClient, 
                          endpoint: str, method: str = "GET") -> LoadTestResult:
        """Testa um endpoint específico"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            response = await client.request(method, url, timeout=30)
            response_time = time.time() - start_time
            
            return LoadTestResult(
                endpoint=endpoint,
                method=method,
                response_time=response_time,
                status_code=response.status_code,
                success=200 <= response.status_code < 300,
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

    async def run_load_test(self, endpoints: List[str], 
                           concurrent_users: int = 10, 
                           duration_seconds: int = 60) -> Dict[str, Any]:
        """Executa teste de carga"""
        print(f"🚀 Iniciando teste de carga com {concurrent_users} usuários por {duration_seconds}s")
        
        async with httpx.AsyncClient() as client:
            tasks = []
            for _ in range(concurrent_users):
                task = asyncio.create_task(
                    self._user_simulation(client, endpoints, duration_seconds)
                )
                tasks.append(task)
            
            await asyncio.gather(*tasks)
        
        return self._analyze_results()

    async def _user_simulation(self, client: httpx.AsyncClient, 
                             endpoints: List[str], duration_seconds: int):
        """Simula um usuário fazendo requisições"""
        end_time = time.time() + duration_seconds
        
        while time.time() < end_time:
            endpoint = np.random.choice(endpoints)
            result = await self.test_endpoint(client, endpoint)
            self.results.append(result)
            await asyncio.sleep(0.1)  # Pequena pausa entre requisições

    def _analyze_results(self) -> Dict[str, Any]:
        """Analisa os resultados do teste"""
        if not self.results:
            return {"error": "Nenhum resultado encontrado"}
        
        successful_results = [r for r in self.results if r.success]
        failed_results = [r for r in self.results if not r.success]
        
        response_times = [r.response_time for r in successful_results]
        
        analysis = {
            "total_requests": len(self.results),
            "successful_requests": len(successful_results),
            "failed_requests": len(failed_results),
            "success_rate": len(successful_results) / len(self.results) * 100,
            "avg_response_time": statistics.mean(response_times) if response_times else 0,
            "min_response_time": min(response_times) if response_times else 0,
            "max_response_time": max(response_times) if response_times else 0,
            "median_response_time": statistics.median(response_times) if response_times else 0,
            "requests_per_second": len(self.results) / (max(r.timestamp for r in self.results) - min(r.timestamp for r in self.results)) if self.results else 0,
            "errors": [r.error for r in failed_results if r.error]
        }
        
        return analysis

    def generate_report(self, analysis: Dict[str, Any]) -> str:
        """Gera relatório de performance"""
        report = f"""
📊 RELATÓRIO DE PERFORMANCE - COINBALANCE ENTERPRISE
====================================================

📈 MÉTRICAS GERAIS:
- Total de Requisições: {analysis['total_requests']}
- Requisições Bem-sucedidas: {analysis['successful_requests']}
- Requisições Falhadas: {analysis['failed_requests']}
- Taxa de Sucesso: {analysis['success_rate']:.2f}%

⏱️ TEMPOS DE RESPOSTA:
- Tempo Médio: {analysis['avg_response_time']:.3f}s
- Tempo Mínimo: {analysis['min_response_time']:.3f}s
- Tempo Máximo: {analysis['max_response_time']:.3f}s
- Tempo Mediano: {analysis['median_response_time']:.3f}s

🚀 PERFORMANCE:
- Requisições por Segundo: {analysis['requests_per_second']:.2f} req/s

❌ ERROS:
"""
        
        if analysis['errors']:
            for error in set(analysis['errors']):
                count = analysis['errors'].count(error)
                report += f"- {error}: {count} ocorrências\n"
        else:
            report += "- Nenhum erro encontrado ✅\n"
        
        return report

async def main():
    """Função principal para executar testes"""
    tester = CoinBalanceLoadTester()
    
    # Endpoints para testar
    endpoints = [
        "/api/v1/health",
        "/api/v1/health/live",
        "/api/v1/health/ready",
        "/api/v1/wallet/balance",
        "/api/v1/blockchain-performance/statistics"
    ]
    
    print("Iniciando testes de performance do CoinBalance Enterprise...")
    
    # Teste de carga básico
    analysis = await tester.run_load_test(
        endpoints=endpoints,
        concurrent_users=5,
        duration_seconds=30
    )
    
    # Gerar relatório
    report = tester.generate_report(analysis)
    print(report)
    
    # Salvar relatório
    with open("performance_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("Relatório salvo em performance_report.txt")

if __name__ == "__main__":
    asyncio.run(main())
