#!/usr/bin/env python3
"""
🪙 CoinBalance - A Economia da Consciência
Versão 2.1.0 DDD - Arquitetura de Classe Mundial

Entry point principal da aplicação CoinBalance com arquitetura DDD.
"""

import sys
import os
import argparse
import uvicorn
from pathlib import Path

def main():
    """
    Função principal para inicializar a aplicação CoinBalance.
    """
    parser = argparse.ArgumentParser(
        description="🪙 CoinBalance v2.1.0 DDD - A Economia da Consciência",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
╔═══════════════════════════════════════════════════════════════╗
║            🏗️  NOVA ARQUITETURA DDD 2.1.0                    ║
╠═══════════════════════════════════════════════════════════════╣
║  ✅ Domain-Driven Design (DDD)                                ║
║  ✅ Clean Architecture (Uncle Bob)                            ║
║  ✅ Hexagonal Architecture (Ports & Adapters)                 ║
║  ✅ CQRS (Command Query Responsibility Segregation)           ║
║  ✅ SOLID Principles                                          ║
║  ✅ 12-Factor App                                             ║
║  ✅ Event-Driven Architecture                                 ║
╚═══════════════════════════════════════════════════════════════╝

Exemplos de uso:
  python main.py                      # Modo desenvolvimento
  python main.py --production         # Modo produção
  python main.py --port 9000          # Porta customizada
  python main.py --workers 4          # Múltiplos workers

Funcionalidades:
  💰 Transações fracionadas (precisão 8 casas decimais)
  🔄 Múltiplas unidades: CNB, Satoshi, mCNB
  💸 Microtransações (1 satoshi = 0.00000001 CNB)
  🧠 Framework Coinbalance com IA
  🏦 DeFi consciente (staking, lending)
  🏛️  Governança descentralizada

Documentação:
  📖 docs/RESUMO_REFATORACAO_DDD.md
  🔍 docs/ANALISE_E_CORRECAO_ARQUITETURA.md
  🚀 docs/PROXIMOS_PASSOS.md
        """
    )
    
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host para bind da aplicação (padrão: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Porta para bind da aplicação (padrão: 8000)'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=1,
        help='Número de workers (padrão: 1)'
    )
    
    parser.add_argument(
        '--production',
        action='store_true',
        help='Executar em modo produção'
    )
    
    parser.add_argument(
        '--reload',
        action='store_true',
        help='Habilitar reload automático (desenvolvimento)'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        default='info',
        help='Nível de log (padrão: info)'
    )
    
    args = parser.parse_args()
    
    # Configurar variáveis de ambiente
    os.environ.setdefault('PYTHONPATH', str(Path(__file__).parent))
    
    # Configurações baseadas no modo
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
              Versao 2.1.0 DDD - Arquitetura
===============================================================
  Host: {args.host}
  Porta: {args.port}
  Workers: {workers}
  Reload: {reload}
  Log Level: {log_level}
  Environment: {env}
===============================================================
  Architecture: DDD + Clean + Hexagonal + CQRS
  Framework: Coinbalance
  Moeda: CNB (Coinbalance)
  Docs: docs/RESUMO_REFATORACAO_DDD.md
===============================================================
    """)
    
    try:
        # Inicializar aplicação
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
        print("\n🛑 CoinBalance interrompida pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar CoinBalance: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()