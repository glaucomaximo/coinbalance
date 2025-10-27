#!/usr/bin/env python3
"""
Ponte de integração Python-Rust para Coinbalance
Integra componentes críticos em Rust com interface Python
"""

import ctypes
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoinbalanceRustBridge:
    """Ponte principal para integração Python-Rust"""
    
    def __init__(self, lib_path: Optional[str] = None):
        """
        Inicializa a ponte com a biblioteca Rust
        
        Args:
            lib_path: Caminho para a biblioteca Rust compilada
        """
        self.lib_path = lib_path or self._find_lib_path()
        self.lib = None
        self._load_library()
        self._setup_functions()
    
    def _find_lib_path(self) -> str:
        """Encontra o caminho da biblioteca Rust compilada"""
        # Procurar em diferentes locais
        possible_paths = [
            "./target/release/libcoinbalance_core.so",
            "./target/debug/libcoinbalance_core.so",
            "../rust/target/release/libcoinbalance_core.so",
            "../rust/target/debug/libcoinbalance_core.so",
            "/usr/local/lib/libcoinbalance_core.so",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Se não encontrar, tentar compilar
        logger.warning("Biblioteca Rust não encontrada. Tentando compilar...")
        self._compile_rust_lib()
        
        # Tentar novamente após compilação
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        raise FileNotFoundError("Biblioteca Rust não encontrada e não foi possível compilar")
    
    def _compile_rust_lib(self):
        """Compila a biblioteca Rust"""
        try:
            import subprocess
            rust_dir = Path(__file__).parent.parent / "rust"
            if rust_dir.exists():
                result = subprocess.run(
                    ["cargo", "build", "--release"],
                    cwd=rust_dir,
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    logger.error(f"Erro ao compilar Rust: {result.stderr}")
                else:
                    logger.info("Biblioteca Rust compilada com sucesso")
            else:
                logger.error("Diretório Rust não encontrado")
        except Exception as e:
            logger.error(f"Erro ao compilar Rust: {e}")
    
    def _load_library(self):
        """Carrega a biblioteca Rust"""
        try:
            self.lib = ctypes.CDLL(self.lib_path)
            logger.info(f"Biblioteca Rust carregada: {self.lib_path}")
        except Exception as e:
            logger.error(f"Erro ao carregar biblioteca Rust: {e}")
            raise
    
    def _setup_functions(self):
        """Configura as funções da biblioteca Rust"""
        # Configurar tipos de retorno
        self.lib.validate_transaction.restype = ctypes.c_bool
        self.lib.validate_transaction.argtypes = [ctypes.c_char_p]
        
        self.lib.calculate_hash.restype = ctypes.c_char_p
        self.lib.calculate_hash.argtypes = [ctypes.c_char_p, ctypes.c_int]
        
        self.lib.generate_keypair.restype = ctypes.c_char_p
        self.lib.generate_keypair.argtypes = [ctypes.c_int]
        
        self.lib.sign_data.restype = ctypes.c_char_p
        self.lib.sign_data.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        
        self.lib.verify_signature.restype = ctypes.c_bool
        self.lib.verify_signature.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        
        self.lib.create_proof_of_stake.restype = ctypes.c_char_p
        self.lib.create_proof_of_stake.argtypes = [ctypes.c_char_p, ctypes.c_ulonglong]
        
        self.lib.validate_proof_of_stake.restype = ctypes.c_bool
        self.lib.validate_proof_of_stake.argtypes = [ctypes.c_char_p]
    
    # ==================== VALIDAÇÃO DE TRANSAÇÕES ====================
    
    def validate_transaction(self, transaction_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Valida uma transação usando Rust
        
        Args:
            transaction_data: Dados da transação
            
        Returns:
            Tuple[bool, str]: (válida, mensagem)
        """
        try:
            json_data = json.dumps(transaction_data).encode('utf-8')
            result = self.lib.validate_transaction(json_data)
            return result, "Transação válida" if result else "Transação inválida"
        except Exception as e:
            logger.error(f"Erro ao validar transação: {e}")
            return False, f"Erro: {e}"
    
    def validate_block(self, block_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Valida um bloco usando Rust
        
        Args:
            block_data: Dados do bloco
            
        Returns:
            Tuple[bool, str]: (válido, mensagem)
        """
        try:
            json_data = json.dumps(block_data).encode('utf-8')
            result = self.lib.validate_block(json_data)
            return result, "Bloco válido" if result else "Bloco inválido"
        except Exception as e:
            logger.error(f"Erro ao validar bloco: {e}")
            return False, f"Erro: {e}"
    
    # ==================== CRIPTOGRAFIA ====================
    
    def calculate_hash(self, data: str, algorithm: int = 0) -> str:
        """
        Calcula hash de dados usando Rust
        
        Args:
            data: Dados para hash
            algorithm: Algoritmo (0=SHA256, 1=SHA512, 2=Keccak256, 3=Keccak512)
            
        Returns:
            str: Hash calculado
        """
        try:
            data_bytes = data.encode('utf-8')
            result = self.lib.calculate_hash(data_bytes, algorithm)
            return result.decode('utf-8')
        except Exception as e:
            logger.error(f"Erro ao calcular hash: {e}")
            return ""
    
    def generate_keypair(self, algorithm: int = 0) -> Dict[str, str]:
        """
        Gera par de chaves usando Rust
        
        Args:
            algorithm: Algoritmo (0=ECDSA, 1=Ed25519)
            
        Returns:
            Dict[str, str]: Par de chaves
        """
        try:
            result = self.lib.generate_keypair(algorithm)
            keypair_data = json.loads(result.decode('utf-8'))
            return keypair_data
        except Exception as e:
            logger.error(f"Erro ao gerar par de chaves: {e}")
            return {}
    
    def sign_data(self, data: str, private_key: str, algorithm: int = 0) -> str:
        """
        Assina dados usando Rust
        
        Args:
            data: Dados para assinar
            algorithm: Algoritmo (0=ECDSA, 1=Ed25519)
            
        Returns:
            str: Assinatura
        """
        try:
            data_bytes = data.encode('utf-8')
            private_key_bytes = private_key.encode('utf-8')
            result = self.lib.sign_data(data_bytes, private_key_bytes, algorithm)
            return result.decode('utf-8')
        except Exception as e:
            logger.error(f"Erro ao assinar dados: {e}")
            return ""
    
    def verify_signature(self, data: str, signature: str, public_key: str, algorithm: int = 0) -> bool:
        """
        Verifica assinatura usando Rust
        
        Args:
            data: Dados originais
            signature: Assinatura
            public_key: Chave pública
            algorithm: Algoritmo (0=ECDSA, 1=Ed25519)
            
        Returns:
            bool: Assinatura válida
        """
        try:
            data_bytes = data.encode('utf-8')
            signature_bytes = signature.encode('utf-8')
            public_key_bytes = public_key.encode('utf-8')
            result = self.lib.verify_signature(data_bytes, signature_bytes, public_key_bytes, algorithm)
            return result
        except Exception as e:
            logger.error(f"Erro ao verificar assinatura: {e}")
            return False
    
    # ==================== CONSENSO ====================
    
    def create_proof_of_stake(self, validator_address: str, nonce: int) -> Dict[str, Any]:
        """
        Cria prova de stake usando Rust
        
        Args:
            validator_address: Endereço do validador
            nonce: Nonce da prova
            
        Returns:
            Dict[str, Any]: Prova de stake
        """
        try:
            address_bytes = validator_address.encode('utf-8')
            result = self.lib.create_proof_of_stake(address_bytes, nonce)
            proof_data = json.loads(result.decode('utf-8'))
            return proof_data
        except Exception as e:
            logger.error(f"Erro ao criar prova de stake: {e}")
            return {}
    
    def validate_proof_of_stake(self, proof_data: Dict[str, Any]) -> bool:
        """
        Valida prova de stake usando Rust
        
        Args:
            proof_data: Dados da prova
            
        Returns:
            bool: Prova válida
        """
        try:
            json_data = json.dumps(proof_data).encode('utf-8')
            result = self.lib.validate_proof_of_stake(json_data)
            return result
        except Exception as e:
            logger.error(f"Erro ao validar prova de stake: {e}")
            return False
    
    # ==================== UTILITÁRIOS ====================
    
    def get_library_info(self) -> Dict[str, Any]:
        """Retorna informações da biblioteca Rust"""
        return {
            "library_path": self.lib_path,
            "loaded": self.lib is not None,
            "version": "1.0.0",
            "components": [
                "Transaction Validator",
                "Cryptography Engine",
                "Consensus Algorithm",
                "Hash Calculator"
            ]
        }
    
    def test_integration(self) -> Dict[str, Any]:
        """Testa a integração Python-Rust"""
        results = {
            "hash_calculation": False,
            "keypair_generation": False,
            "signature_verification": False,
            "transaction_validation": False,
            "proof_of_stake": False
        }
        
        try:
            # Teste de hash
            test_data = "Hello, Coinbalance!"
            hash_result = self.calculate_hash(test_data)
            results["hash_calculation"] = len(hash_result) > 0
            
            # Teste de geração de chaves
            keypair = self.generate_keypair()
            results["keypair_generation"] = len(keypair) > 0
            
            # Teste de assinatura
            if keypair:
                signature = self.sign_data(test_data, keypair.get("private_key", ""))
                if signature:
                    is_valid = self.verify_signature(test_data, signature, keypair.get("public_key", ""))
                    results["signature_verification"] = is_valid
            
            # Teste de validação de transação
            test_tx = {
                "id": "test_tx_1",
                "from": "CNB_test123",
                "to": "CNB_test456",
                "amount": 100.0,
                "fee": 0.1,
                "timestamp": "2024-01-01T00:00:00Z",
                "signature": "test_signature",
                "nonce": 1
            }
            is_valid, _ = self.validate_transaction(test_tx)
            results["transaction_validation"] = is_valid
            
            # Teste de prova de stake
            proof = self.create_proof_of_stake("CNB_validator123", 12345)
            if proof:
                is_valid = self.validate_proof_of_stake(proof)
                results["proof_of_stake"] = is_valid
            
        except Exception as e:
            logger.error(f"Erro no teste de integração: {e}")
        
        return results

# ==================== FUNÇÕES DE CONVENIÊNCIA ====================

def create_rust_bridge() -> CoinbalanceRustBridge:
    """Cria uma instância da ponte Rust"""
    return CoinbalanceRustBridge()

def quick_hash(data: str) -> str:
    """Calcula hash rapidamente"""
    bridge = create_rust_bridge()
    return bridge.calculate_hash(data)

def quick_validate_transaction(transaction_data: Dict[str, Any]) -> bool:
    """Valida transação rapidamente"""
    bridge = create_rust_bridge()
    is_valid, _ = bridge.validate_transaction(transaction_data)
    return is_valid

def quick_generate_keypair() -> Dict[str, str]:
    """Gera par de chaves rapidamente"""
    bridge = create_rust_bridge()
    return bridge.generate_keypair()

# ==================== EXEMPLO DE USO ====================

if __name__ == "__main__":
    print("🦀 Testando integração Python-Rust...")
    
    try:
        # Criar ponte
        bridge = create_rust_bridge()
        
        # Mostrar informações
        info = bridge.get_library_info()
        print(f"📚 Biblioteca: {info['library_path']}")
        print(f"✅ Carregada: {info['loaded']}")
        
        # Testar integração
        results = bridge.test_integration()
        print("\n🧪 Resultados dos testes:")
        for test, passed in results.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {test}")
        
        # Exemplo de uso
        print("\n💡 Exemplo de uso:")
        
        # Gerar par de chaves
        keypair = bridge.generate_keypair()
        print(f"🔑 Chaves geradas: {len(keypair)} campos")
        
        # Calcular hash
        data = "Dados para hash"
        hash_result = bridge.calculate_hash(data)
        print(f"🔐 Hash calculado: {hash_result[:16]}...")
        
        print("\n🎉 Integração Python-Rust funcionando!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)