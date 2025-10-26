#!/usr/bin/env python3
"""
Script para executar Coinbalance em dispositivos móveis
Oferece diferentes opções de execução mobile
"""

import os
import sys
import subprocess
import webbrowser
import argparse
from pathlib import Path


def print_banner():
    """Exibe banner do Coinbalance"""
    print("🪙" + "="*50)
    print("   COINBALANCE - A ECONOMIA DA CONSCIÊNCIA")
    print("   Execução Mobile - Dispositivos Móveis")
    print("="*52)
    print()


def check_dependencies():
    """Verifica dependências necessárias"""
    print("🔍 Verificando dependências...")
    
    # Verificar Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ necessário")
        return False
    
    # Verificar FastAPI
    try:
        import fastapi
        print("✅ FastAPI disponível")
    except ImportError:
        print("❌ FastAPI não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"])
    
    # Verificar outras dependências
    dependencies = ["uvicorn", "cryptography", "requests"]
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} disponível")
        except ImportError:
            print(f"❌ {dep} não encontrado. Instalando...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep])
    
    return True


def start_web_server(port=8000, host="0.0.0.0"):
    """Inicia servidor web para acesso mobile"""
    print(f"🚀 Iniciando servidor web na porta {port}...")
    print(f"📱 Acesse no mobile: http://{host}:{port}")
    print("🛑 Pressione Ctrl+C para parar")
    print()
    
    try:
        # Iniciar servidor FastAPI
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "api_moderna:app", 
            "--host", host, 
            "--port", str(port),
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Servidor interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")


def open_mobile_interface():
    """Abre interface mobile no navegador"""
    mobile_file = Path(__file__).parent / "mobile_interface.html"
    
    if not mobile_file.exists():
        print("❌ Arquivo mobile_interface.html não encontrado")
        return False
    
    print("📱 Abrindo interface mobile...")
    webbrowser.open(f"file://{mobile_file.absolute()}")
    return True


def create_mobile_config():
    """Cria configuração otimizada para mobile"""
    config = {
        "mobile": {
            "enabled": True,
            "responsive": True,
            "touch_optimized": True,
            "offline_support": True
        },
        "ui": {
            "theme": "coinbalance",
            "colors": {
                "primary": "#FFD700",
                "secondary": "#4169E1",
                "accent": "#32CD32"
            },
            "fonts": {
                "primary": "Inter",
                "secondary": "Source Sans Pro"
            }
        },
        "features": {
            "wallet": True,
            "staking": True,
            "investments": True,
            "notifications": True,
            "offline_mode": True
        }
    }
    
    import json
    config_file = Path(__file__).parent / "mobile_config.json"
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Configuração mobile criada: {config_file}")
    return True


def show_mobile_instructions():
    """Exibe instruções para uso mobile"""
    print("📱 INSTRUÇÕES PARA USO MOBILE")
    print("="*40)
    print()
    print("1. 🌐 INTERFACE WEB RESPONSIVA:")
    print("   - Abra mobile_interface.html no navegador")
    print("   - Funciona em qualquer dispositivo")
    print("   - Interface otimizada para touch")
    print()
    print("2. 🚀 SERVIDOR LOCAL:")
    print("   - Execute: python run_mobile.py --server")
    print("   - Acesse: http://SEU_IP:8000")
    print("   - Compartilhe com outros dispositivos")
    print()
    print("3. 📱 PWA (Progressive Web App):")
    print("   - Adicione à tela inicial do mobile")
    print("   - Funciona offline")
    print("   - Notificações push")
    print()
    print("4. 🔧 DESENVOLVIMENTO:")
    print("   - React Native para app nativo")
    print("   - Flutter para multiplataforma")
    print("   - Ionic para híbrido")
    print()


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="Coinbalance Mobile - Execução em dispositivos móveis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python run_mobile.py                    # Mostrar opções
  python run_mobile.py --server           # Iniciar servidor web
  python run_mobile.py --interface       # Abrir interface mobile
  python run_mobile.py --config          # Criar configuração mobile
  python run_mobile.py --instructions    # Mostrar instruções
        """
    )
    
    parser.add_argument(
        '--server',
        action='store_true',
        help='Iniciar servidor web para acesso mobile'
    )
    
    parser.add_argument(
        '--interface',
        action='store_true',
        help='Abrir interface mobile no navegador'
    )
    
    parser.add_argument(
        '--config',
        action='store_true',
        help='Criar configuração mobile'
    )
    
    parser.add_argument(
        '--instructions',
        action='store_true',
        help='Mostrar instruções de uso mobile'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Porta do servidor (padrão: 8000)'
    )
    
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host do servidor (padrão: 0.0.0.0)'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    # Verificar dependências
    if not check_dependencies():
        print("❌ Dependências não atendidas")
        sys.exit(1)
    
    # Executar ação solicitada
    if args.server:
        start_web_server(args.port, args.host)
    elif args.interface:
        open_mobile_interface()
    elif args.config:
        create_mobile_config()
    elif args.instructions:
        show_mobile_instructions()
    else:
        # Mostrar menu interativo
        print("📱 OPÇÕES DE EXECUÇÃO MOBILE")
        print("="*35)
        print()
        print("1. 🌐 Abrir interface web responsiva")
        print("2. 🚀 Iniciar servidor web")
        print("3. ⚙️  Criar configuração mobile")
        print("4. 📖 Mostrar instruções")
        print("5. ❌ Sair")
        print()
        
        try:
            choice = input("Escolha uma opção (1-5): ").strip()
            
            if choice == "1":
                open_mobile_interface()
            elif choice == "2":
                start_web_server(args.port, args.host)
            elif choice == "3":
                create_mobile_config()
            elif choice == "4":
                show_mobile_instructions()
            elif choice == "5":
                print("👋 Até logo!")
                sys.exit(0)
            else:
                print("❌ Opção inválida")
                sys.exit(1)
                
        except KeyboardInterrupt:
            print("\n👋 Até logo!")
            sys.exit(0)


if __name__ == "__main__":
    main()