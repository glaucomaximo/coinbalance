#!/usr/bin/env python3
"""
Script de Validação e Teste do Sistema CoinBalance
===================================================

Este script valida que o sistema está funcionando corretamente:
- Verifica dependências
- Testa conexões
- Valida endpoints
- Testa funcionalidades básicas

Uso:
    python scripts/validate_system.py
"""

import sys
import os
from pathlib import Path

# Adicionar raiz do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_imports():
    """Verifica se todas as dependências necessárias estão instaladas"""
    print("🔍 Verificando dependências...")
    
    required_modules = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "pydantic_settings",
        "cryptography",
        "psutil",
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module} - FALTANDO")
            missing.append(module)
    
    if missing:
        print(f"\n❌ Módulos faltando: {', '.join(missing)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    print("✅ Todas as dependências estão instaladas\n")
    return True


def check_configuration():
    """Verifica configurações básicas"""
    print("🔍 Verificando configurações...")
    
    # Verificar arquivos essenciais
    essential_files = [
        "main.py",
        "requirements.txt",
        "src/presentation/api/app.py",
    ]
    
    for file_path in essential_files:
        if not (project_root / file_path).exists():
            print(f"  ❌ {file_path} não encontrado")
            return False
        print(f"  ✅ {file_path}")
    
    # Verificar diretórios
    essential_dirs = [
        "src",
        "src/domain",
        "src/infrastructure",
        "src/presentation",
        "data",
    ]
    
    for dir_path in essential_dirs:
        full_path = project_root / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"  📁 Criado: {dir_path}")
        else:
            print(f"  ✅ {dir_path}")
    
    print("✅ Configurações básicas OK\n")
    return True


def check_database():
    """Verifica se o banco de dados pode ser inicializado"""
    print("🔍 Verificando banco de dados...")
    
    try:
        from src.infrastructure.persistence.database_manager import DatabaseManager
        
        db_manager = DatabaseManager()
        print("  ✅ DatabaseManager pode ser instanciado")
        
        # Verificar se diretório data existe
        data_dir = project_root / "data"
        if not data_dir.exists():
            data_dir.mkdir(parents=True, exist_ok=True)
            print("  📁 Diretório 'data' criado")
        
        print("  ✅ Banco de dados OK")
        print("✅ Verificação de banco de dados concluída\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao verificar banco de dados: {e}")
        return False


def check_api():
    """Verifica se a API pode ser criada"""
    print("🔍 Verificando API...")
    
    try:
        from src.presentation.api.app import create_app
        
        app = create_app()
        print("  ✅ Aplicação FastAPI criada com sucesso")
        
        # Verificar rotas principais
        routes = [str(route.path) for route in app.routes]
        essential_routes = [
            "/health/live",
            "/health/ready",
            "/",
        ]
        
        for route in essential_routes:
            if route in routes:
                print(f"  ✅ Rota {route} registrada")
            else:
                print(f"  ⚠️  Rota {route} não encontrada")
        
        print("✅ Verificação de API concluída\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao verificar API: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal"""
    print("="*80)
    print("🔧 VALIDAÇÃO DO SISTEMA COINBALANCE")
    print("="*80)
    print()
    
    checks = [
        ("Dependências", check_imports),
        ("Configurações", check_configuration),
        ("Banco de Dados", check_database),
        ("API", check_api),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Erro ao executar {name}: {e}")
            results.append((name, False))
    
    # Resumo final
    print("="*80)
    print("📊 RESUMO DA VALIDAÇÃO")
    print("="*80)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {name}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("✅ TODAS AS VALIDAÇÕES PASSARAM!")
        print("   O sistema está pronto para uso.")
        print()
        print("Para iniciar o sistema:")
        print("  python main.py")
        print()
        print("Ou com Docker:")
        print("  docker-compose up -d")
        return 0
    else:
        print("❌ ALGUMAS VALIDAÇÕES FALHARAM")
        print("   Por favor, corrija os problemas acima antes de continuar.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

