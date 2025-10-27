use serde::{Deserialize, Serialize};
use sha2::{Sha256, Digest};
use std::collections::HashMap;
use chrono::{DateTime, Utc};
use thiserror::Error;

/// Erros de validação de transação
#[derive(Error, Debug)]
pub enum ValidationError {
    #[error("Assinatura inválida")]
    InvalidSignature,
    #[error("Saldo insuficiente")]
    InsufficientBalance,
    #[error("Transação duplicada")]
    DuplicateTransaction,
    #[error("Formato inválido")]
    InvalidFormat,
    #[error("Timestamp inválido")]
    InvalidTimestamp,
    #[error("Valor inválido")]
    InvalidAmount,
}

/// Estrutura de transação CNB
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Transaction {
    pub id: String,
    pub from: String,
    pub to: String,
    pub amount: f64,
    pub fee: f64,
    pub timestamp: DateTime<Utc>,
    pub signature: String,
    pub nonce: u64,
    pub data: Option<String>,
}

/// Estrutura de bloco
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Block {
    pub index: u64,
    pub timestamp: DateTime<Utc>,
    pub previous_hash: String,
    pub hash: String,
    pub nonce: u64,
    pub transactions: Vec<Transaction>,
    pub merkle_root: String,
}

/// Validador de transações CNB
pub struct TransactionValidator {
    seen_transactions: HashMap<String, bool>,
}

impl TransactionValidator {
    pub fn new() -> Self {
        Self {
            seen_transactions: HashMap::new(),
        }
    }

    /// Valida uma transação CNB
    pub fn validate_transaction(&mut self, tx: &Transaction) -> Result<bool, ValidationError> {
        // Verificar se já foi processada
        if self.seen_transactions.contains_key(&tx.id) {
            return Err(ValidationError::DuplicateTransaction);
        }

        // Validar formato
        self.validate_format(tx)?;

        // Validar timestamp
        self.validate_timestamp(tx)?;

        // Validar valor
        self.validate_amount(tx)?;

        // Marcar como processada
        self.seen_transactions.insert(tx.id.clone(), true);

        Ok(true)
    }

    /// Valida formato da transação
    fn validate_format(&self, tx: &Transaction) -> Result<(), ValidationError> {
        if tx.from.is_empty() || tx.to.is_empty() {
            return Err(ValidationError::InvalidFormat);
        }

        if tx.id.is_empty() || tx.signature.is_empty() {
            return Err(ValidationError::InvalidFormat);
        }

        Ok(())
    }

    /// Valida timestamp da transação
    fn validate_timestamp(&self, tx: &Transaction) -> Result<(), ValidationError> {
        let now = Utc::now();
        let tx_time = tx.timestamp;
        
        // Transação não pode ser do futuro
        if tx_time > now {
            return Err(ValidationError::InvalidTimestamp);
        }

        // Transação não pode ser muito antiga (24 horas)
        let max_age = chrono::Duration::hours(24);
        if now - tx_time > max_age {
            return Err(ValidationError::InvalidTimestamp);
        }

        Ok(())
    }

    /// Valida valor da transação
    fn validate_amount(&self, tx: &Transaction) -> Result<(), ValidationError> {
        if tx.amount <= 0.0 {
            return Err(ValidationError::InvalidAmount);
        }

        if tx.fee < 0.0 {
            return Err(ValidationError::InvalidAmount);
        }

        // Valor máximo por transação (1 milhão CNB)
        if tx.amount > 1_000_000.0 {
            return Err(ValidationError::InvalidAmount);
        }

        Ok(())
    }

    /// Calcula hash de dados
    pub fn calculate_hash(&self, data: &[u8]) -> String {
        let mut hasher = Sha256::new();
        hasher.update(data);
        format!("{:x}", hasher.finalize())
    }

    /// Valida um bloco completo
    pub fn validate_block(&mut self, block: &Block) -> Result<bool, ValidationError> {
        // Validar hash do bloco
        self.validate_block_hash(block)?;

        // Validar Merkle root
        self.validate_merkle_root(block)?;

        // Validar todas as transações
        for tx in &block.transactions {
            self.validate_transaction(tx)?;
        }

        Ok(true)
    }

    /// Valida hash do bloco
    fn validate_block_hash(&self, block: &Block) -> Result<(), ValidationError> {
        let calculated_hash = self.calculate_block_hash(block);
        if calculated_hash != block.hash {
            return Err(ValidationError::InvalidFormat);
        }
        Ok(())
    }

    /// Calcula hash do bloco
    fn calculate_block_hash(&self, block: &Block) -> String {
        let mut hasher = Sha256::new();
        hasher.update(block.index.to_le_bytes());
        hasher.update(block.timestamp.timestamp().to_le_bytes());
        hasher.update(block.previous_hash.as_bytes());
        hasher.update(block.merkle_root.as_bytes());
        hasher.update(block.nonce.to_le_bytes());
        format!("{:x}", hasher.finalize())
    }

    /// Valida Merkle root
    fn validate_merkle_root(&self, block: &Block) -> Result<(), ValidationError> {
        let calculated_root = self.calculate_merkle_root(&block.transactions);
        if calculated_root != block.merkle_root {
            return Err(ValidationError::InvalidFormat);
        }
        Ok(())
    }

    /// Calcula Merkle root das transações
    fn calculate_merkle_root(&self, transactions: &[Transaction]) -> String {
        if transactions.is_empty() {
            return "0".to_string();
        }

        let mut hashes: Vec<String> = transactions
            .iter()
            .map(|tx| {
                let mut hasher = Sha256::new();
                hasher.update(tx.id.as_bytes());
                format!("{:x}", hasher.finalize())
            })
            .collect();

        while hashes.len() > 1 {
            let mut next_level = Vec::new();
            for chunk in hashes.chunks(2) {
                let mut hasher = Sha256::new();
                hasher.update(chunk[0].as_bytes());
                if chunk.len() > 1 {
                    hasher.update(chunk[1].as_bytes());
                } else {
                    hasher.update(chunk[0].as_bytes());
                }
                next_level.push(format!("{:x}", hasher.finalize()));
            }
            hashes = next_level;
        }

        hashes[0].clone()
    }
}

impl Default for TransactionValidator {
    fn default() -> Self {
        Self::new()
    }
}

/// Função de conveniência para validação rápida
pub fn validate_transaction_fast(tx: &Transaction) -> Result<bool, ValidationError> {
    let mut validator = TransactionValidator::new();
    validator.validate_transaction(tx)
}

/// Função de conveniência para validação de bloco
pub fn validate_block_fast(block: &Block) -> Result<bool, ValidationError> {
    let mut validator = TransactionValidator::new();
    validator.validate_block(block)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_transaction_validation() {
        let tx = Transaction {
            id: "test_tx_1".to_string(),
            from: "CNB_1234567890abcdef".to_string(),
            to: "CNB_fedcba0987654321".to_string(),
            amount: 100.0,
            fee: 0.1,
            timestamp: Utc::now(),
            signature: "test_signature".to_string(),
            nonce: 1,
            data: None,
        };

        let result = validate_transaction_fast(&tx);
        assert!(result.is_ok());
    }

    #[test]
    fn test_merkle_root_calculation() {
        let validator = TransactionValidator::new();
        let transactions = vec![
            Transaction {
                id: "tx1".to_string(),
                from: "CNB_1".to_string(),
                to: "CNB_2".to_string(),
                amount: 100.0,
                fee: 0.1,
                timestamp: Utc::now(),
                signature: "sig1".to_string(),
                nonce: 1,
                data: None,
            },
            Transaction {
                id: "tx2".to_string(),
                from: "CNB_2".to_string(),
                to: "CNB_3".to_string(),
                amount: 50.0,
                fee: 0.05,
                timestamp: Utc::now(),
                signature: "sig2".to_string(),
                nonce: 2,
                data: None,
            },
        ];

        let root = validator.calculate_merkle_root(&transactions);
        assert!(!root.is_empty());
    }
}