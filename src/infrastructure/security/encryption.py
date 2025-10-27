"""
Serviço de Criptografia para Chaves Privadas
"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from typing import Optional

class EncryptionService:
    """Serviço de criptografia para dados sensíveis"""
    
    def __init__(self, master_key: Optional[str] = None):
        """
        Inicializa o serviço de criptografia
        
        Args:
            master_key: Chave mestra para criptografia. Se None, usa variável de ambiente
        """
        self.master_key = master_key or os.getenv("COINBALANCE_MASTER_KEY")
        
        if not self.master_key:
            # Usar chave padrão para desenvolvimento
            self.master_key = "dev-master-key-change-in-production-32-chars-long"
            print("⚠️  AVISO: Usando chave mestra padrão para desenvolvimento!")
            print("   Configure COINBALANCE_MASTER_KEY para produção.")
        
        # Validar comprimento da chave mestra
        if len(self.master_key.encode()) < 32:
            raise ValueError("Master key must be at least 32 bytes long for security")
        
        # Derivar chave de criptografia usando PBKDF2
        self._fernet = self._create_fernet()
    
    def _create_fernet(self) -> Fernet:
        """Cria instância Fernet com chave derivada"""
        # Usar salt único por chave para máxima segurança
        salt = os.urandom(16)  # 16 bytes de salt aleatório
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(self.master_key.encode()))
        return Fernet(key)
    
    def encrypt_private_key(self, private_key: str) -> str:
        """
        Criptografa uma chave privada
        
        Args:
            private_key: Chave privada em texto plano
            
        Returns:
            Chave privada criptografada (base64) com salt incluído
        """
        try:
            # Gerar salt único para esta chave
            salt = os.urandom(16)
            
            # Criar KDF com salt único
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            key = base64.urlsafe_b64encode(kdf.derive(self.master_key.encode()))
            fernet = Fernet(key)
            
            # Criptografar dados
            encrypted_data = fernet.encrypt(private_key.encode())
            
            # Combinar salt + dados criptografados
            combined = salt + encrypted_data
            return base64.urlsafe_b64encode(combined).decode()
            
        except Exception as e:
            raise ValueError(f"Erro ao criptografar chave privada: {e}")
    
    def decrypt_private_key(self, encrypted_private_key: str) -> str:
        """
        Descriptografa uma chave privada
        
        Args:
            encrypted_private_key: Chave privada criptografada (base64) com salt incluído
            
        Returns:
            Chave privada em texto plano
        """
        try:
            # Decodificar dados combinados
            combined = base64.urlsafe_b64decode(encrypted_private_key.encode())
            
            # Separar salt e dados criptografados
            salt = combined[:16]
            encrypted_data = combined[16:]
            
            # Criar KDF com salt extraído
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            key = base64.urlsafe_b64encode(kdf.derive(self.master_key.encode()))
            fernet = Fernet(key)
            
            # Descriptografar dados
            decrypted_data = fernet.decrypt(encrypted_data)
            return decrypted_data.decode()
            
        except Exception as e:
            raise ValueError(f"Erro ao descriptografar chave privada: {e}")
    
    def encrypt_data(self, data: str) -> str:
        """
        Criptografa dados genéricos
        
        Args:
            data: Dados em texto plano
            
        Returns:
            Dados criptografados (base64)
        """
        try:
            encrypted_data = self._fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            raise ValueError(f"Erro ao criptografar dados: {e}")
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Descriptografa dados genéricos
        
        Args:
            encrypted_data: Dados criptografados (base64)
            
        Returns:
            Dados em texto plano
        """
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self._fernet.decrypt(encrypted_bytes)
            return decrypted_data.decode()
        except Exception as e:
            raise ValueError(f"Erro ao descriptografar dados: {e}")
    
    def is_encrypted(self, data: str) -> bool:
        """
        Verifica se os dados estão criptografados
        
        Args:
            data: Dados para verificar
            
        Returns:
            True se os dados estão criptografados
        """
        try:
            # Tentar descriptografar - se funcionar, está criptografado
            self.decrypt_data(data)
            return True
        except:
            return False

# Instância global do serviço de criptografia
encryption_service = EncryptionService()
