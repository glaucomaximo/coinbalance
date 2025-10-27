#!/usr/bin/env python3
"""
Coinbalance - A Economia da Consciência
Ponto de entrada principal da aplicação
Framework proprietário para investimento consciente
Suporte completo a transações fracionadas com precisão decimal
"""

import os
import sys
import argparse
import uvicorn
from pathlib import Path

# Adicionar diretório atual ao path
sys.path.append(str(Path(__file__).parent))

def main():
    """Função principal para inicializar a Coinbalance"""
    
    parser = argparse.ArgumentParser(
        description="Coinbalance - A Economia da Consciência (v2.1.0)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py                    # Iniciar em modo desenvolvimento
  python main.py --production       # Iniciar em modo produção
  python main.py --port 9000        # Usar porta personalizada
  python main.py --workers 4        # Usar múltiplos workers

Funcionalidades:
  💰 Transações fracionadas com precisão decimal (8 casas)
  🔄 Múltiplas unidades: CNB, Satoshi, mCNB
  💸 Microtransações de 1 satoshi (0.00000001 CNB)
  🧠 Framework Coinbalance com IA simbólica
  🏦 DeFi consciente com staking e empréstimos
  🏛️ Governança descentralizada
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
    
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Arquivo de configuração (padrão: config.yaml)'
    )
    
    args = parser.parse_args()
    
    # Configurar variáveis de ambiente
    os.environ.setdefault('PYTHONPATH', str(Path(__file__).parent))
    
    # Configurações baseadas no modo
    if args.production:
        reload = False
        workers = args.workers
        log_level = 'warning'
    else:
        reload = args.reload or True
        workers = 1
        log_level = args.log_level
    
    print("🪙 Iniciando Coinbalance - A Economia da Consciência...")
    print(f"📍 Host: {args.host}")
    print(f"🔌 Porta: {args.port}")
    print(f"👥 Workers: {workers}")
    print(f"🔄 Reload: {reload}")
    print(f"📊 Log Level: {log_level}")
    print(f"⚙️  Config: {args.config}")
    print(f"🧠 Framework: Coinbalance")
    print(f"💰 Moeda: CNB")
    print("-" * 50)
    
    try:
        # Inicializar aplicação
        uvicorn.run(
            "api_moderna:app",
            host=args.host,
            port=args.port,
            workers=workers,
            reload=reload,
            log_level=log_level,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Coinbalance interrompida pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar Coinbalance: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
