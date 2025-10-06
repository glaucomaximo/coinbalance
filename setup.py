#!/usr/bin/env python3
"""
Script de configuração e instalação da CryptoChain
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Exibe banner da CryptoChain"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🚀 CRYPTOCHAIN SETUP 🚀                    ║
    ║              Blockchain Moderna com DeFi                      ║
    ║                                                              ║
    ║  ✨ Características:                                         ║
    ║     🔐 Criptografia ECDSA                                    ║
    ║     💰 DeFi Completo (Staking, Empréstimos)                  ║
    ║     🏛️  Governança Descentralizada                           ║
    ║     ⚡ Escalabilidade com Sharding                           ║
    ║     🐳 Docker & CI/CD                                        ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ é necessário")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")

def check_dependencies():
    """Verifica dependências do sistema"""
    print("🔍 Verificando dependências do sistema...")
    
    # Verificar se pip está disponível
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip disponível")
    except subprocess.CalledProcessError:
        print("❌ pip não encontrado")
        sys.exit(1)
    
    # Verificar se git está disponível
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ git disponível")
    except subprocess.CalledProcessError:
        print("⚠️  git não encontrado (opcional)")

def install_python_dependencies():
    """Instala dependências Python"""
    print("📦 Instalando dependências Python...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✅ Dependências Python instaladas")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        sys.exit(1)

def create_directories():
    """Cria diretórios necessários"""
    print("📁 Criando diretórios...")
    
    directories = [
        "data",
        "backups", 
        "logs",
        "ssl",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Diretório {directory}/ criado")

def setup_environment():
    """Configura variáveis de ambiente"""
    print("⚙️  Configurando ambiente...")
    
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# CryptoChain Environment Variables
DATABASE_URL=sqlite:///data/blockchain.db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here
NETWORK_ID=cryptochain_mainnet
PORT=8000
LOG_LEVEL=info
DEBUG=false
"""
        env_file.write_text(env_content)
        print("✅ Arquivo .env criado")
    else:
        print("✅ Arquivo .env já existe")

def run_tests():
    """Executa testes básicos"""
    print("🧪 Executando testes...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v"
        ], check=True)
        print("✅ Todos os testes passaram")
    except subprocess.CalledProcessError:
        print("⚠️  Alguns testes falharam (continuando...)")

def show_next_steps():
    """Mostra próximos passos"""
    next_steps = """
    🎉 INSTALAÇÃO CONCLUÍDA! 🎉
    
    📋 Próximos passos:
    
    1. 🚀 Iniciar a aplicação:
       python main.py
    
    2. 🌐 Acessar a API:
       http://localhost:8000
    
    3. 📚 Documentação:
       http://localhost:8000/docs
    
    4. 🐳 Usar Docker (opcional):
       docker-compose up -d
    
    5. 🧪 Executar testes:
       pytest tests/ -v
    
    📞 Suporte:
    - Discord: discord.gg/cryptochain
    - Email: support@cryptochain.com
    - GitHub: github.com/seu-usuario/cryptochain
    
    ⭐ Se este projeto foi útil, considere dar uma estrela! ⭐
    """
    print(next_steps)

def main():
    """Função principal do setup"""
    print_banner()
    
    print("🔧 Iniciando configuração da CryptoChain...")
    print("-" * 60)
    
    # Verificações
    check_python_version()
    check_dependencies()
    
    # Instalação
    install_python_dependencies()
    create_directories()
    setup_environment()
    
    # Testes
    run_tests()
    
    # Próximos passos
    show_next_steps()

if __name__ == "__main__":
    main()
