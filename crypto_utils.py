"""
Sistema de Criptografia Robusta para Blockchain
Implementa ECDSA, geração de chaves, assinatura digital e validação
"""

import hashlib
import json
import secrets
from typing import Tuple, Dict, Any
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64


class CryptoUtils:
    """Utilitários de criptografia para blockchain segura"""
    
    @staticmethod
    def gerar_par_chaves() -> Tuple[str, str]:
        """Gera um par de chaves privada/pública usando ECDSA"""
        private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        public_key = private_key.public_key()
        
        # Serializar chaves
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem.decode(), public_pem.decode()
    
    @staticmethod
    def assinar_transacao(transacao: Dict[str, Any], chave_privada: str) -> str:
        """Assina uma transação com a chave privada"""
        try:
            # Carregar chave privada
            private_key = serialization.load_pem_private_key(
                chave_privada.encode(),
                password=None,
                backend=default_backend()
            )
            
            # Criar hash da transação
            transacao_str = json.dumps(transacao, sort_keys=True)
            transacao_hash = hashlib.sha256(transacao_str.encode()).digest()
            
            # Assinar
            assinatura = private_key.sign(transacao_hash, ec.ECDSA(hashes.SHA256()))
            
            return base64.b64encode(assinatura).decode()
            
        except Exception as e:
            raise ValueError(f"Erro ao assinar transação: {e}")
    
    @staticmethod
    def verificar_assinatura(transacao: Dict[str, Any], assinatura: str, chave_publica: str) -> bool:
        """Verifica se a assinatura da transação é válida"""
        try:
            # Carregar chave pública
            public_key = serialization.load_pem_public_key(
                chave_publica.encode(),
                backend=default_backend()
            )
            
            # Criar hash da transação
            transacao_str = json.dumps(transacao, sort_keys=True)
            transacao_hash = hashlib.sha256(transacao_str.encode()).digest()
            
            # Verificar assinatura
            assinatura_bytes = base64.b64decode(assinatura)
            public_key.verify(assinatura_bytes, transacao_hash, ec.ECDSA(hashes.SHA256()))
            
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def gerar_hash_duplo(dados: str) -> str:
        """Gera hash duplo SHA-256 para maior segurança"""
        primeiro_hash = hashlib.sha256(dados.encode()).hexdigest()
        segundo_hash = hashlib.sha256(primeiro_hash.encode()).hexdigest()
        return segundo_hash
    
    @staticmethod
    def derivar_chave_maestra(senha: str, salt: bytes) -> bytes:
        """Deriva chave mestra usando PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(senha.encode())
    
    @staticmethod
    def gerar_salt() -> bytes:
        """Gera salt aleatório para derivação de chaves"""
        return secrets.token_bytes(32)
