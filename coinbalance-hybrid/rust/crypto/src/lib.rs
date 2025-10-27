use serde::{Deserialize, Serialize};
use sha2::{Sha256, Sha512, Digest};
use sha3::{Keccak256, Keccak512};
use ecdsa::{Signature, SigningKey, VerifyingKey, signature::Signer, signature::Verifier};
use secp256k1::{Secp256k1, PublicKey, SecretKey, Message, ecdsa};
use ed25519_dalek::{SigningKey as Ed25519SigningKey, VerifyingKey as Ed25519VerifyingKey, Signature as Ed25519Signature, Signer, Verifier as Ed25519Verifier};
use aes_gcm::{Aes256Gcm, Key, Nonce, aead::{Aead, NewAead}};
use argon2::{Argon2, PasswordHash, PasswordHasher, PasswordVerifier, password_hash::{rand_core::OsRng, SaltString}};
use std::collections::HashMap;
use thiserror::Error;

/// Erros de criptografia
#[derive(Error, Debug)]
pub enum CryptoError {
    #[error("Chave inválida")]
    InvalidKey,
    #[error("Assinatura inválida")]
    InvalidSignature,
    #[error("Cifração falhou")]
    EncryptionFailed,
    #[error("Decifração falhou")]
    DecryptionFailed,
    #[error("Hash inválido")]
    InvalidHash,
    #[error("Formato inválido")]
    InvalidFormat,
}

/// Tipos de algoritmo de hash
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum HashAlgorithm {
    Sha256,
    Sha512,
    Keccak256,
    Keccak512,
}

/// Tipos de algoritmo de assinatura
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SignatureAlgorithm {
    ECDSA,
    Ed25519,
}

/// Estrutura de chave CNB
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CNBKeyPair {
    pub public_key: String,
    pub private_key: String,
    pub address: String,
    pub algorithm: SignatureAlgorithm,
}

/// Estrutura de hash
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HashResult {
    pub hash: String,
    pub algorithm: HashAlgorithm,
    pub length: usize,
}

/// Sistema de criptografia CNB
pub struct CNBCrypto {
    secp: Secp256k1<secp256k1::All>,
    aes_key: Option<Aes256Gcm>,
}

impl CNBCrypto {
    pub fn new() -> Self {
        Self {
            secp: Secp256k1::new(),
            aes_key: None,
        }
    }

    /// Gera par de chaves CNB
    pub fn generate_keypair(&self, algorithm: SignatureAlgorithm) -> Result<CNBKeyPair, CryptoError> {
        match algorithm {
            SignatureAlgorithm::ECDSA => self.generate_ecdsa_keypair(),
            SignatureAlgorithm::Ed25519 => self.generate_ed25519_keypair(),
        }
    }

    /// Gera par de chaves ECDSA
    fn generate_ecdsa_keypair(&self) -> Result<CNBKeyPair, CryptoError> {
        let (secret_key, public_key) = self.secp.generate_keypair(&mut rand::thread_rng());
        
        let public_key_hex = hex::encode(public_key.serialize());
        let secret_key_hex = hex::encode(secret_key.secret_bytes());
        let address = self.public_key_to_address(&public_key)?;

        Ok(CNBKeyPair {
            public_key: public_key_hex,
            private_key: secret_key_hex,
            address,
            algorithm: SignatureAlgorithm::ECDSA,
        })
    }

    /// Gera par de chaves Ed25519
    fn generate_ed25519_keypair(&self) -> Result<CNBKeyPair, CryptoError> {
        let signing_key = Ed25519SigningKey::generate(&mut rand::thread_rng());
        let verifying_key = signing_key.verifying_key();
        
        let public_key_hex = hex::encode(verifying_key.to_bytes());
        let secret_key_hex = hex::encode(signing_key.to_bytes());
        let address = self.ed25519_public_key_to_address(&verifying_key)?;

        Ok(CNBKeyPair {
            public_key: public_key_hex,
            private_key: secret_key_hex,
            address,
            algorithm: SignatureAlgorithm::Ed25519,
        })
    }

    /// Converte chave pública para endereço CNB
    fn public_key_to_address(&self, public_key: &PublicKey) -> Result<String, CryptoError> {
        let pub_key_bytes = public_key.serialize();
        let mut hasher = Sha256::new();
        hasher.update(&pub_key_bytes);
        let hash = hasher.finalize();
        Ok(format!("CNB_{}", hex::encode(&hash[..20])))
    }

    /// Converte chave pública Ed25519 para endereço CNB
    fn ed25519_public_key_to_address(&self, public_key: &Ed25519VerifyingKey) -> Result<String, CryptoError> {
        let pub_key_bytes = public_key.to_bytes();
        let mut hasher = Sha256::new();
        hasher.update(&pub_key_bytes);
        let hash = hasher.finalize();
        Ok(format!("CNB_{}", hex::encode(&hash[..20])))
    }

    /// Calcula hash de dados
    pub fn hash_data(&self, data: &[u8], algorithm: HashAlgorithm) -> HashResult {
        let hash = match algorithm {
            HashAlgorithm::Sha256 => {
                let mut hasher = Sha256::new();
                hasher.update(data);
                hasher.finalize()
            }
            HashAlgorithm::Sha512 => {
                let mut hasher = Sha512::new();
                hasher.update(data);
                hasher.finalize()
            }
            HashAlgorithm::Keccak256 => {
                let mut hasher = Keccak256::new();
                hasher.update(data);
                hasher.finalize()
            }
            HashAlgorithm::Keccak512 => {
                let mut hasher = Keccak512::new();
                hasher.update(data);
                hasher.finalize()
            }
        };

        HashResult {
            hash: hex::encode(hash),
            algorithm,
            length: hash.len(),
        }
    }

    /// Assina dados com chave privada
    pub fn sign_data(&self, data: &[u8], private_key: &str, algorithm: SignatureAlgorithm) -> Result<String, CryptoError> {
        match algorithm {
            SignatureAlgorithm::ECDSA => self.sign_ecdsa(data, private_key),
            SignatureAlgorithm::Ed25519 => self.sign_ed25519(data, private_key),
        }
    }

    /// Assina dados com ECDSA
    fn sign_ecdsa(&self, data: &[u8], private_key: &str) -> Result<String, CryptoError> {
        let secret_key_bytes = hex::decode(private_key)
            .map_err(|_| CryptoError::InvalidKey)?;
        
        let secret_key = SecretKey::from_slice(&secret_key_bytes)
            .map_err(|_| CryptoError::InvalidKey)?;

        let message = Message::from_slice(data)
            .map_err(|_| CryptoError::InvalidFormat)?;

        let signature = self.secp.sign_ecdsa(&message, &secret_key);
        Ok(hex::encode(signature.serialize_der()))
    }

    /// Assina dados com Ed25519
    fn sign_ed25519(&self, data: &[u8], private_key: &str) -> Result<String, CryptoError> {
        let secret_key_bytes = hex::decode(private_key)
            .map_err(|_| CryptoError::InvalidKey)?;
        
        let signing_key = Ed25519SigningKey::from_bytes(&secret_key_bytes)
            .map_err(|_| CryptoError::InvalidKey)?;

        let signature = signing_key.sign(data);
        Ok(hex::encode(signature.to_bytes()))
    }

    /// Verifica assinatura
    pub fn verify_signature(&self, data: &[u8], signature: &str, public_key: &str, algorithm: SignatureAlgorithm) -> Result<bool, CryptoError> {
        match algorithm {
            SignatureAlgorithm::ECDSA => self.verify_ecdsa(data, signature, public_key),
            SignatureAlgorithm::Ed25519 => self.verify_ed25519(data, signature, public_key),
        }
    }

    /// Verifica assinatura ECDSA
    fn verify_ecdsa(&self, data: &[u8], signature: &str, public_key: &str) -> Result<bool, CryptoError> {
        let public_key_bytes = hex::decode(public_key)
            .map_err(|_| CryptoError::InvalidKey)?;
        
        let public_key = PublicKey::from_slice(&public_key_bytes)
            .map_err(|_| CryptoError::InvalidKey)?;

        let signature_bytes = hex::decode(signature)
            .map_err(|_| CryptoError::InvalidSignature)?;
        
        let signature = Signature::from_der(&signature_bytes)
            .map_err(|_| CryptoError::InvalidSignature)?;

        let message = Message::from_slice(data)
            .map_err(|_| CryptoError::InvalidFormat)?;

        match public_key.verify(&message, &signature) {
            Ok(_) => Ok(true),
            Err(_) => Ok(false),
        }
    }

    /// Verifica assinatura Ed25519
    fn verify_ed25519(&self, data: &[u8], signature: &str, public_key: &str) -> Result<bool, CryptoError> {
        let public_key_bytes = hex::decode(public_key)
            .map_err(|_| CryptoError::InvalidKey)?;
        
        let public_key = Ed25519VerifyingKey::from_bytes(&public_key_bytes)
            .map_err(|_| CryptoError::InvalidKey)?;

        let signature_bytes = hex::decode(signature)
            .map_err(|_| CryptoError::InvalidSignature)?;
        
        let signature = Ed25519Signature::from_bytes(&signature_bytes)
            .map_err(|_| CryptoError::InvalidSignature)?;

        match public_key.verify(data, &signature) {
            Ok(_) => Ok(true),
            Err(_) => Ok(false),
        }
    }

    /// Cifra dados com AES-256-GCM
    pub fn encrypt_data(&mut self, data: &[u8], password: &str) -> Result<Vec<u8>, CryptoError> {
        // Gerar chave AES a partir da senha
        let salt = SaltString::generate(&mut OsRng);
        let argon2 = Argon2::default();
        let password_hash = argon2.hash_password(password.as_bytes(), &salt)
            .map_err(|_| CryptoError::EncryptionFailed)?;

        let key = Key::from_slice(&password_hash.hash.unwrap().as_bytes()[..32]);
        let cipher = Aes256Gcm::new(key);

        // Gerar nonce aleatório
        let nonce = Nonce::from_slice(b"unique nonce"); // Em produção, usar nonce aleatório

        // Cifrar dados
        cipher.encrypt(nonce, data)
            .map_err(|_| CryptoError::EncryptionFailed)
    }

    /// Decifra dados com AES-256-GCM
    pub fn decrypt_data(&mut self, encrypted_data: &[u8], password: &str) -> Result<Vec<u8>, CryptoError> {
        // Gerar chave AES a partir da senha
        let salt = SaltString::generate(&mut OsRng);
        let argon2 = Argon2::default();
        let password_hash = argon2.hash_password(password.as_bytes(), &salt)
            .map_err(|_| CryptoError::DecryptionFailed)?;

        let key = Key::from_slice(&password_hash.hash.unwrap().as_bytes()[..32]);
        let cipher = Aes256Gcm::new(key);

        // Usar mesmo nonce (em produção, armazenar nonce separadamente)
        let nonce = Nonce::from_slice(b"unique nonce");

        // Decifrar dados
        cipher.decrypt(nonce, encrypted_data)
            .map_err(|_| CryptoError::DecryptionFailed)
    }

    /// Gera hash de senha com Argon2
    pub fn hash_password(&self, password: &str) -> Result<String, CryptoError> {
        let salt = SaltString::generate(&mut OsRng);
        let argon2 = Argon2::default();
        let password_hash = argon2.hash_password(password.as_bytes(), &salt)
            .map_err(|_| CryptoError::InvalidHash)?;

        Ok(password_hash.to_string())
    }

    /// Verifica hash de senha
    pub fn verify_password(&self, password: &str, hash: &str) -> Result<bool, CryptoError> {
        let parsed_hash = PasswordHash::new(hash)
            .map_err(|_| CryptoError::InvalidHash)?;

        let argon2 = Argon2::default();
        match argon2.verify_password(password.as_bytes(), &parsed_hash) {
            Ok(_) => Ok(true),
            Err(_) => Ok(false),
        }
    }

    /// Gera seed mnemônico (simplificado)
    pub fn generate_mnemonic(&self) -> String {
        // Em produção, usar biblioteca de mnemônico real
        let words = [
            "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
            "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid"
        ];
        
        let mut mnemonic = String::new();
        for i in 0..12 {
            let word = words[i % words.len()];
            mnemonic.push_str(word);
            if i < 11 {
                mnemonic.push(' ');
            }
        }
        mnemonic
    }
}

impl Default for CNBCrypto {
    fn default() -> Self {
        Self::new()
    }
}

/// Função de conveniência para hash rápido
pub fn quick_hash(data: &[u8]) -> String {
    let crypto = CNBCrypto::new();
    let result = crypto.hash_data(data, HashAlgorithm::Sha256);
    result.hash
}

/// Função de conveniência para geração de chaves
pub fn generate_cnb_keypair() -> Result<CNBKeyPair, CryptoError> {
    let crypto = CNBCrypto::new();
    crypto.generate_keypair(SignatureAlgorithm::ECDSA)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_keypair_generation() {
        let crypto = CNBCrypto::new();
        let keypair = crypto.generate_keypair(SignatureAlgorithm::ECDSA).unwrap();
        
        assert!(!keypair.public_key.is_empty());
        assert!(!keypair.private_key.is_empty());
        assert!(keypair.address.starts_with("CNB_"));
    }

    #[test]
    fn test_hash_calculation() {
        let crypto = CNBCrypto::new();
        let data = b"Hello, Coinbalance!";
        let result = crypto.hash_data(data, HashAlgorithm::Sha256);
        
        assert!(!result.hash.is_empty());
        assert_eq!(result.algorithm, HashAlgorithm::Sha256);
        assert_eq!(result.length, 32);
    }

    #[test]
    fn test_signature_verification() {
        let crypto = CNBCrypto::new();
        let keypair = crypto.generate_keypair(SignatureAlgorithm::ECDSA).unwrap();
        let data = b"Test data for signing";
        
        let signature = crypto.sign_data(data, &keypair.private_key, SignatureAlgorithm::ECDSA).unwrap();
        let is_valid = crypto.verify_signature(data, &signature, &keypair.public_key, SignatureAlgorithm::ECDSA).unwrap();
        
        assert!(is_valid);
    }

    #[test]
    fn test_password_hashing() {
        let crypto = CNBCrypto::new();
        let password = "test_password_123";
        
        let hash = crypto.hash_password(password).unwrap();
        let is_valid = crypto.verify_password(password, &hash).unwrap();
        
        assert!(is_valid);
    }
}