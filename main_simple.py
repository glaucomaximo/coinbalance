#!/usr/bin/env python3
"""
CoinBalance - A Economia da Consciencia
Versao 3.0.0 Enterprise - Arquitetura de Classe Mundial

Entry point principal da aplicacao CoinBalance com arquitetura Enterprise.
"""

import sys
import os
import argparse
import uvicorn
from pathlib import Path

def main():
    """
    Funcao principal para inicializar a aplicacao CoinBalance.
    """
    parser = argparse.ArgumentParser(
        description="CoinBalance v3.0.0 Enterprise - A Economia da Consciencia",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Arquitetura Enterprise 3.0.0:
- Domain-Driven Design (DDD)
- Clean Architecture (Uncle Bob)
- Hexagonal Architecture (Ports & Adapters)
- CQRS (Command Query Responsibility Segregation)
- SOLID Principles
- 12-Factor App
- Event-Driven Architecture
- Enterprise Patterns

Exemplos de uso:
  python main.py                      # Modo desenvolvimento
  python main.py --production         # Modo produção
  python main.py --port 9000          # Porta customizada
  python main.py --workers 4          # Múltiplos workers

Funcionalidades Enterprise:
- Transações fracionadas (precisão 8 casas decimais)
- Múltiplas unidades: CNB, Satoshi, mCNB
- Microtransações (1 satoshi = 0.00000001 CNB)
- Framework Coinbalance com IA Avançada
- DeFi consciente (staking, lending)
- Governança descentralizada
- Blockchain Enterprise com mineração paralela
- Web3 completo (NFTs, DeFi, DAO, Cross-Chain)
- Monitoramento em tempo real
- Segurança enterprise-grade

Documentação:
- docs/DOCUMENTACAO_TECNICA_ENTERPRISE.md
- docs/GUIA_DEPLOY_OTIMIZADO.md
- docs/reports/RELATORIO_FINAL_REVISAO_COMPLETA_DOCUMENTACAO_ATUALIZADA.md
        """
    )
    
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host para bind da aplicacao (padrao: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Porta para bind da aplicacao (padrao: 8000)'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=1,
        help='Numero de workers (padrao: 1)'
    )
    
    parser.add_argument(
        '--production',
        action='store_true',
        help='Executar em modo producao'
    )
    
    parser.add_argument(
        '--reload',
        action='store_true',
        help='Habilitar reload automatico (desenvolvimento)'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        default='info',
        help='Nivel de log (padrao: info)'
    )
    
    args = parser.parse_args()
    
    # Configurar variaveis de ambiente
    os.environ.setdefault('PYTHONPATH', str(Path(__file__).parent))
    
    # Configuracoes baseadas no modo
    if args.production:
        reload = False
        workers = args.workers
        log_level = 'warning'
        env = 'production'
    else:
        reload = args.reload or True
        workers = 1
        log_level = args.log_level
        env = 'development'
    
    print(f"""
===============================================================
       CoinBalance - A Economia da Consciencia
              Versao 3.0.0 Enterprise - Arquitetura
===============================================================
  Host: {args.host}
  Porta: {args.port}
  Workers: {workers}
  Reload: {reload}
  Log Level: {log_level}
  Environment: {env}
===============================================================
  Architecture: Enterprise + DDD + Clean + Hexagonal + CQRS
  Framework: Coinbalance Enterprise
  Moeda: CNB (Coinbalance)
  Docs: docs/DOCUMENTACAO_TECNICA_ENTERPRISE.md
===============================================================
    """)
    
    try:
        # Inicializar aplicacao
        uvicorn.run(
            "src.presentation.api.app:app",
            host=args.host,
            port=args.port,
            workers=workers,
            reload=reload,
            log_level=log_level,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\nCoinBalance interrompida pelo usuario")
    except Exception as e:
        print(f"Erro ao iniciar CoinBalance: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
