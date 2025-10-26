use serde::{Deserialize, Serialize};
use sha2::{Sha256, Digest};
use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH};
use chrono::{DateTime, Utc};
use thiserror::Error;

/// Erros de consenso
#[derive(Error, Debug)]
pub enum ConsensusError {
    #[error("Bloco inválido")]
    InvalidBlock,
    #[error("Prova de stake inválida")]
    InvalidProofOfStake,
    #[error("Validador não encontrado")]
    ValidatorNotFound,
    #[error("Stake insuficiente")]
    InsufficientStake,
    #[error("Timestamp inválido")]
    InvalidTimestamp,
    #[error("Hash inválido")]
    InvalidHash,
}

/// Estrutura de validador
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Validator {
    pub address: String,
    pub stake: f64,
    pub reputation: f64,
    pub last_block_time: Option<DateTime<Utc>>,
    pub total_blocks: u64,
    pub is_active: bool,
}

/// Estrutura de bloco para consenso
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConsensusBlock {
    pub index: u64,
    pub timestamp: DateTime<Utc>,
    pub previous_hash: String,
    pub hash: String,
    pub validator: String,
    pub stake_proof: String,
    pub transactions_count: usize,
    pub difficulty: u64,
}

/// Estrutura de prova de stake
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProofOfStake {
    pub validator: String,
    pub stake_amount: f64,
    pub timestamp: DateTime<Utc>,
    pub signature: String,
    pub nonce: u64,
}

/// Sistema de consenso Proof of Stake Consciente
pub struct ConsciousProofOfStake {
    validators: HashMap<String, Validator>,
    total_stake: f64,
    min_stake: f64,
    block_time: u64, // segundos
    difficulty_adjustment: u64,
}

impl ConsciousProofOfStake {
    pub fn new(min_stake: f64, block_time: u64) -> Self {
        Self {
            validators: HashMap::new(),
            total_stake: 0.0,
            min_stake,
            block_time,
            difficulty_adjustment: 2016, // Ajustar a cada 2016 blocos
        }
    }

    /// Registra um validador
    pub fn register_validator(&mut self, address: String, stake: f64) -> Result<(), ConsensusError> {
        if stake < self.min_stake {
            return Err(ConsensusError::InsufficientStake);
        }

        let validator = Validator {
            address: address.clone(),
            stake,
            reputation: 1.0,
            last_block_time: None,
            total_blocks: 0,
            is_active: true,
        };

        self.validators.insert(address, validator);
        self.total_stake += stake;
        Ok(())
    }

    /// Remove um validador
    pub fn unregister_validator(&mut self, address: &str) -> Result<(), ConsensusError> {
        if let Some(validator) = self.validators.remove(address) {
            self.total_stake -= validator.stake;
            Ok(())
        } else {
            Err(ConsensusError::ValidatorNotFound)
        }
    }

    /// Atualiza stake de um validador
    pub fn update_stake(&mut self, address: &str, new_stake: f64) -> Result<(), ConsensusError> {
        if let Some(validator) = self.validators.get_mut(address) {
            let old_stake = validator.stake;
            validator.stake = new_stake;
            self.total_stake = self.total_stake - old_stake + new_stake;
            Ok(())
        } else {
            Err(ConsensusError::ValidatorNotFound)
        }
    }

    /// Seleciona o próximo validador baseado em stake e reputação
    pub fn select_validator(&self) -> Result<String, ConsensusError> {
        if self.validators.is_empty() {
            return Err(ConsensusError::ValidatorNotFound);
        }

        // Calcular pesos baseados em stake e reputação
        let mut weighted_validators = Vec::new();
        for validator in self.validators.values() {
            if validator.is_active {
                let weight = validator.stake * validator.reputation;
                weighted_validators.push((validator.address.clone(), weight));
            }
        }

        if weighted_validators.is_empty() {
            return Err(ConsensusError::ValidatorNotFound);
        }

        // Seleção probabilística baseada no peso
        let total_weight: f64 = weighted_validators.iter().map(|(_, weight)| weight).sum();
        let mut rng = rand::thread_rng();
        let random_value: f64 = rng.gen::<f64>() * total_weight;

        let mut current_weight = 0.0;
        for (address, weight) in weighted_validators {
            current_weight += weight;
            if random_value <= current_weight {
                return Ok(address);
            }
        }

        // Fallback para o primeiro validador
        Ok(weighted_validators[0].0.clone())
    }

    /// Valida prova de stake
    pub fn validate_proof_of_stake(&self, proof: &ProofOfStake) -> Result<bool, ConsensusError> {
        // Verificar se o validador existe
        let validator = self.validators.get(&proof.validator)
            .ok_or(ConsensusError::ValidatorNotFound)?;

        // Verificar se o validador está ativo
        if !validator.is_active {
            return Err(ConsensusError::ValidatorNotFound);
        }

        // Verificar se o stake é suficiente
        if proof.stake_amount < self.min_stake {
            return Err(ConsensusError::InsufficientStake);
        }

        // Verificar se o stake corresponde ao registrado
        if (proof.stake_amount - validator.stake).abs() > 0.001 {
            return Err(ConsensusError::InvalidProofOfStake);
        }

        // Verificar timestamp (não muito antigo)
        let now = Utc::now();
        let max_age = chrono::Duration::seconds(self.block_time as i64 * 2);
        if now - proof.timestamp > max_age {
            return Err(ConsensusError::InvalidTimestamp);
        }

        // Verificar assinatura (simplificado)
        let expected_signature = self.calculate_stake_signature(proof);
        if proof.signature != expected_signature {
            return Err(ConsensusError::InvalidProofOfStake);
        }

        Ok(true)
    }

    /// Calcula assinatura da prova de stake
    fn calculate_stake_signature(&self, proof: &ProofOfStake) -> String {
        let mut hasher = Sha256::new();
        hasher.update(proof.validator.as_bytes());
        hasher.update(proof.stake_amount.to_le_bytes());
        hasher.update(proof.timestamp.timestamp().to_le_bytes());
        hasher.update(proof.nonce.to_le_bytes());
        format!("{:x}", hasher.finalize())
    }

    /// Cria prova de stake para um validador
    pub fn create_proof_of_stake(&self, validator_address: &str, nonce: u64) -> Result<ProofOfStake, ConsensusError> {
        let validator = self.validators.get(validator_address)
            .ok_or(ConsensusError::ValidatorNotFound)?;

        if !validator.is_active {
            return Err(ConsensusError::ValidatorNotFound);
        }

        let mut proof = ProofOfStake {
            validator: validator_address.to_string(),
            stake_amount: validator.stake,
            timestamp: Utc::now(),
            signature: String::new(),
            nonce,
        };

        proof.signature = self.calculate_stake_signature(&proof);
        Ok(proof)
    }

    /// Valida um bloco de consenso
    pub fn validate_consensus_block(&mut self, block: &ConsensusBlock) -> Result<bool, ConsensusError> {
        // Verificar se o validador existe e está ativo
        let validator = self.validators.get(&block.validator)
            .ok_or(ConsensusError::ValidatorNotFound)?;

        if !validator.is_active {
            return Err(ConsensusError::ValidatorNotFound);
        }

        // Verificar timestamp
        let now = Utc::now();
        let time_diff = (now - block.timestamp).num_seconds().abs() as u64;
        if time_diff > self.block_time * 2 {
            return Err(ConsensusError::InvalidTimestamp);
        }

        // Verificar hash do bloco
        let calculated_hash = self.calculate_block_hash(block);
        if calculated_hash != block.hash {
            return Err(ConsensusError::InvalidHash);
        }

        // Verificar prova de stake
        let proof = ProofOfStake {
            validator: block.validator.clone(),
            stake_amount: validator.stake,
            timestamp: block.timestamp,
            signature: block.stake_proof.clone(),
            nonce: 0, // Simplificado
        };

        self.validate_proof_of_stake(&proof)?;

        // Atualizar estatísticas do validador
        if let Some(validator) = self.validators.get_mut(&block.validator) {
            validator.last_block_time = Some(block.timestamp);
            validator.total_blocks += 1;
            
            // Aumentar reputação baseado na performance
            validator.reputation = (validator.reputation + 0.01).min(2.0);
        }

        Ok(true)
    }

    /// Calcula hash do bloco
    fn calculate_block_hash(&self, block: &ConsensusBlock) -> String {
        let mut hasher = Sha256::new();
        hasher.update(block.index.to_le_bytes());
        hasher.update(block.timestamp.timestamp().to_le_bytes());
        hasher.update(block.previous_hash.as_bytes());
        hasher.update(block.validator.as_bytes());
        hasher.update(block.stake_proof.as_bytes());
        hasher.update(block.transactions_count.to_le_bytes());
        hasher.update(block.difficulty.to_le_bytes());
        format!("{:x}", hasher.finalize())
    }

    /// Ajusta dificuldade baseada no tempo de blocos
    pub fn adjust_difficulty(&mut self, actual_block_time: u64) {
        let target_time = self.block_time;
        let adjustment_factor = target_time as f64 / actual_block_time as f64;
        
        // Ajustar dificuldade (simplificado)
        for validator in self.validators.values_mut() {
            if adjustment_factor > 1.1 {
                validator.reputation *= 0.99; // Reduzir reputação se muito rápido
            } else if adjustment_factor < 0.9 {
                validator.reputation *= 1.01; // Aumentar reputação se muito lento
            }
        }
    }

    /// Obtém estatísticas do consenso
    pub fn get_consensus_stats(&self) -> ConsensusStats {
        let active_validators = self.validators.values().filter(|v| v.is_active).count();
        let total_blocks: u64 = self.validators.values().map(|v| v.total_blocks).sum();
        let avg_reputation: f64 = self.validators.values()
            .map(|v| v.reputation)
            .sum::<f64>() / self.validators.len() as f64;

        ConsensusStats {
            total_validators: self.validators.len(),
            active_validators,
            total_stake: self.total_stake,
            total_blocks,
            average_reputation: avg_reputation,
            min_stake: self.min_stake,
        }
    }

    /// Lista validadores por reputação
    pub fn get_validators_by_reputation(&self) -> Vec<Validator> {
        let mut validators: Vec<Validator> = self.validators.values().cloned().collect();
        validators.sort_by(|a, b| b.reputation.partial_cmp(&a.reputation).unwrap());
        validators
    }
}

/// Estatísticas do consenso
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConsensusStats {
    pub total_validators: usize,
    pub active_validators: usize,
    pub total_stake: f64,
    pub total_blocks: u64,
    pub average_reputation: f64,
    pub min_stake: f64,
}

impl Default for ConsciousProofOfStake {
    fn default() -> Self {
        Self::new(1000.0, 10) // 1000 CNB mínimo, 10 segundos por bloco
    }
}

/// Função de conveniência para criar consenso
pub fn create_conscious_consensus(min_stake: f64, block_time: u64) -> ConsciousProofOfStake {
    ConsciousProofOfStake::new(min_stake, block_time)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_validator_registration() {
        let mut consensus = ConsciousProofOfStake::new(100.0, 10);
        
        let result = consensus.register_validator("CNB_test123".to_string(), 500.0);
        assert!(result.is_ok());
        
        let stats = consensus.get_consensus_stats();
        assert_eq!(stats.total_validators, 1);
        assert_eq!(stats.total_stake, 500.0);
    }

    #[test]
    fn test_insufficient_stake() {
        let mut consensus = ConsciousProofOfStake::new(100.0, 10);
        
        let result = consensus.register_validator("CNB_test123".to_string(), 50.0);
        assert!(result.is_err());
    }

    #[test]
    fn test_validator_selection() {
        let mut consensus = ConsciousProofOfStake::new(100.0, 10);
        
        consensus.register_validator("CNB_validator1".to_string(), 1000.0).unwrap();
        consensus.register_validator("CNB_validator2".to_string(), 2000.0).unwrap();
        
        let selected = consensus.select_validator();
        assert!(selected.is_ok());
    }

    #[test]
    fn test_proof_of_stake_validation() {
        let mut consensus = ConsciousProofOfStake::new(100.0, 10);
        consensus.register_validator("CNB_test123".to_string(), 500.0).unwrap();
        
        let proof = consensus.create_proof_of_stake("CNB_test123", 12345).unwrap();
        let is_valid = consensus.validate_proof_of_stake(&proof).unwrap();
        
        assert!(is_valid);
    }
}