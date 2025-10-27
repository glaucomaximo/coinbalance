//! Coinbalance Core - A Economia da Consciência
//! Biblioteca principal que integra todos os componentes Rust

pub mod validator;
pub mod crypto;
pub mod consensus;

// Re-exportar componentes principais
pub use validator::*;
pub use crypto::*;
pub use consensus::*;

/// Versão da biblioteca
pub const VERSION: &str = "1.0.0";

/// Informações da biblioteca
pub fn get_library_info() -> String {
    serde_json::json!({
        "name": "coinbalance_core",
        "version": VERSION,
        "description": "A Economia da Consciência - Core Rust Components",
        "components": [
            "Transaction Validator",
            "Cryptography Engine", 
            "Consensus Algorithm"
        ]
    }).to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_library_info() {
        let info = get_library_info();
        assert!(info.contains("coinbalance_core"));
        assert!(info.contains(VERSION));
    }
}