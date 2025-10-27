#!/usr/bin/env python3
"""
Script de build para projeto híbrido Python-Rust
Compila componentes Rust e configura integração
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import argparse
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CoinbalanceBuilder:
    """Builder para projeto híbrido Coinbalance"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.rust_dir = project_root / "rust"
        self.python_dir = project_root / "python"
        self.integration_dir = project_root / "integration"
        self.scripts_dir = project_root / "scripts"
        
    def check_dependencies(self) -> bool:
        """Verifica dependências necessárias"""
        logger.info("🔍 Verificando dependências...")
        
        # Verificar Rust
        try:
            result = subprocess.run(["cargo", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"✅ Rust encontrado: {result.stdout.strip()}")
            else:
                logger.error("❌ Rust não encontrado")
                return False
        except FileNotFoundError:
            logger.error("❌ Rust não encontrado. Instale em: https://rustup.rs/")
            return False
        
        # Verificar Python
        try:
            result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"✅ Python encontrado: {result.stdout.strip()}")
            else:
                logger.error("❌ Python não encontrado")
                return False
        except FileNotFoundError:
            logger.error("❌ Python não encontrado")
            return False
        
        # Verificar pip
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"✅ pip encontrado: {result.stdout.strip()}")
            else:
                logger.error("❌ pip não encontrado")
                return False
        except FileNotFoundError:
            logger.error("❌ pip não encontrado")
            return False
        
        return True
    
    def build_rust_components(self, release: bool = True) -> bool:
        """Compila componentes Rust"""
        logger.info("🦀 Compilando componentes Rust...")
        
        if not self.rust_dir.exists():
            logger.error("❌ Diretório Rust não encontrado")
            return False
        
        try:
            # Configurar variáveis de ambiente
            env = os.environ.copy()
            env["RUST_BACKTRACE"] = "1"
            
            # Comando de build
            cmd = ["cargo", "build"]
            if release:
                cmd.append("--release")
            
            # Executar build
            result = subprocess.run(
                cmd,
                cwd=self.rust_dir,
                env=env,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("✅ Componentes Rust compilados com sucesso")
                return True
            else:
                logger.error(f"❌ Erro ao compilar Rust: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao compilar Rust: {e}")
            return False
    
    def install_python_dependencies(self) -> bool:
        """Instala dependências Python"""
        logger.info("🐍 Instalando dependências Python...")
        
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            logger.warning("⚠️ Arquivo requirements.txt não encontrado")
            return True
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("✅ Dependências Python instaladas")
                return True
            else:
                logger.error(f"❌ Erro ao instalar dependências Python: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao instalar dependências Python: {e}")
            return False
    
    def copy_rust_libraries(self) -> bool:
        """Copia bibliotecas Rust compiladas"""
        logger.info("📚 Copiando bibliotecas Rust...")
        
        # Encontrar bibliotecas compiladas
        lib_patterns = [
            "target/release/libcoinbalance_core.so",
            "target/debug/libcoinbalance_core.so",
            "target/release/libcoinbalance_core.dll",
            "target/debug/libcoinbalance_core.dll",
            "target/release/libcoinbalance_core.dylib",
            "target/debug/libcoinbalance_core.dylib",
        ]
        
        lib_found = False
        for pattern in lib_patterns:
            lib_path = self.rust_dir / pattern
            if lib_path.exists():
                # Copiar para diretório de integração
                dest_path = self.integration_dir / lib_path.name
                shutil.copy2(lib_path, dest_path)
                logger.info(f"✅ Biblioteca copiada: {dest_path}")
                lib_found = True
                break
        
        if not lib_found:
            logger.error("❌ Nenhuma biblioteca Rust encontrada")
            return False
        
        return True
    
    def create_launcher_script(self) -> bool:
        """Cria script de inicialização"""
        logger.info("🚀 Criando script de inicialização...")
        
        launcher_content = '''#!/usr/bin/env python3
"""
Launcher para projeto híbrido Coinbalance
Inicializa componentes Python e Rust
"""

import sys
import os
from pathlib import Path

# Adicionar diretórios ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "python"))
sys.path.insert(0, str(project_root / "integration"))

# Importar e executar
try:
    from main import main
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    print("💡 Execute: python scripts/build.py --build")
    sys.exit(1)
'''
        
        launcher_path = self.project_root / "launch.py"
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        
        # Tornar executável
        os.chmod(launcher_path, 0o755)
        logger.info(f"✅ Script de inicialização criado: {launcher_path}")
        
        return True
    
    def run_tests(self) -> bool:
        """Executa testes de integração"""
        logger.info("🧪 Executando testes de integração...")
        
        try:
            # Testar integração Python-Rust
            test_script = self.integration_dir / "coinbalance_rust.py"
            if test_script.exists():
                result = subprocess.run(
                    [sys.executable, str(test_script)],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    logger.info("✅ Testes de integração passaram")
                    return True
                else:
                    logger.error(f"❌ Testes falharam: {result.stderr}")
                    return False
            else:
                logger.warning("⚠️ Script de teste não encontrado")
                return True
                
        except Exception as e:
            logger.error(f"❌ Erro ao executar testes: {e}")
            return False
    
    def build(self, release: bool = True, test: bool = True) -> bool:
        """Executa build completo"""
        logger.info("🏗️ Iniciando build do projeto híbrido Coinbalance...")
        
        # Verificar dependências
        if not self.check_dependencies():
            return False
        
        # Compilar Rust
        if not self.build_rust_components(release):
            return False
        
        # Instalar dependências Python
        if not self.install_python_dependencies():
            return False
        
        # Copiar bibliotecas
        if not self.copy_rust_libraries():
            return False
        
        # Criar script de inicialização
        if not self.create_launcher_script():
            return False
        
        # Executar testes
        if test and not self.run_tests():
            return False
        
        logger.info("🎉 Build concluído com sucesso!")
        logger.info("💡 Execute: python launch.py")
        
        return True
    
    def clean(self) -> bool:
        """Limpa arquivos de build"""
        logger.info("🧹 Limpando arquivos de build...")
        
        try:
            # Limpar Rust
            if self.rust_dir.exists():
                target_dir = self.rust_dir / "target"
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                    logger.info("✅ Diretório target removido")
            
            # Limpar Python
            pycache_dirs = list(self.project_root.rglob("__pycache__"))
            for pycache_dir in pycache_dirs:
                shutil.rmtree(pycache_dir)
                logger.info(f"✅ {pycache_dir} removido")
            
            # Limpar bibliotecas copiadas
            lib_files = list(self.integration_dir.glob("libcoinbalance_core.*"))
            for lib_file in lib_files:
                lib_file.unlink()
                logger.info(f"✅ {lib_file} removido")
            
            logger.info("✅ Limpeza concluída")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro na limpeza: {e}")
            return False

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="Builder para projeto híbrido Coinbalance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python build.py                    # Build completo
  python build.py --debug           # Build em modo debug
  python build.py --no-test         # Build sem testes
  python build.py --clean           # Limpar arquivos
  python build.py --rust-only       # Apenas compilar Rust
        """
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Build em modo debug (não release)'
    )
    
    parser.add_argument(
        '--no-test',
        action='store_true',
        help='Não executar testes'
    )
    
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Limpar arquivos de build'
    )
    
    parser.add_argument(
        '--rust-only',
        action='store_true',
        help='Apenas compilar componentes Rust'
    )
    
    args = parser.parse_args()
    
    # Determinar diretório do projeto
    project_root = Path(__file__).parent.parent
    
    # Criar builder
    builder = CoinbalanceBuilder(project_root)
    
    # Executar ação
    if args.clean:
        success = builder.clean()
    elif args.rust_only:
        success = builder.build_rust_components(not args.debug)
    else:
        success = builder.build(
            release=not args.debug,
            test=not args.no_test
        )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()