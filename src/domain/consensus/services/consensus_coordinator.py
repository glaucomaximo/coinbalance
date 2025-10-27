"""
Serviço de Coordenação de Consenso - Integra PoW e PoS
"""

from typing import List, Optional, Dict, Any
from decimal import Decimal
import time

from ..blockchain.entities.blockchain import Blockchain
from ..blockchain.entities.block import Block
from ..consensus.services.consensus_service import ConsensusService
from ..consensus.entities.validator import Validator
from ..transaction.entities.transaction import Transaction
from ..shared.value_objects.timestamp import Timestamp
from ...shared.config.blockchain_config import BlockchainConfig


class ConsensusCoordinator:
    """
    Coordenador do sistema de consenso híbrido PoW/PoS.
    
    Responsabilidades:
    - Coordenar mineração (PoW) e validação (PoS)
    - Distribuir recompensas entre miners e validators
    - Gerenciar ciclo de vida dos blocos
    - Manter sincronização entre sistemas
    """
    
    def __init__(self, blockchain: Blockchain, consensus_service: ConsensusService):
        self.blockchain = blockchain
        self.consensus_service = consensus_service
        self.mining_stats: Dict[str, Any] = {
            "blocks_mined": 0,
            "blocks_validated": 0,
            "total_rewards_distributed": Decimal("0"),
            "miner_rewards": Decimal("0"),
            "validator_rewards": Decimal("0")
        }
    
    def mine_and_validate_block(
        self, 
        transactions: List[Transaction], 
        miner_address: str
    ) -> Optional[Block]:
        """
        Processo completo: mineração (PoW) + validação (PoS).
        
        Args:
            transactions: Lista de transações para incluir no bloco
            miner_address: Endereço do miner
            
        Returns:
            Bloco minerado e validado, ou None se falhar
        """
        try:
            # 1. MINERAÇÃO (PoW)
            mined_block = self.blockchain.mine_block(transactions, miner_address)
            if not mined_block:
                return None
            
            # 2. VALIDAÇÃO (PoS)
            validation_result = self._validate_block_with_pos(mined_block)
            if not validation_result["is_valid"]:
                return None
            
            # 3. ADICIONAR À BLOCKCHAIN
            if self.blockchain.add_block(mined_block):
                # 4. DISTRIBUIR RECOMPENSAS
                self._distribute_rewards(mined_block, validation_result["validator"])
                
                # 5. ATUALIZAR ESTATÍSTICAS
                self._update_stats(mined_block, validation_result["validator"])
                
                return mined_block
            
            return None
            
        except Exception as e:
            print(f"Erro no processo de mineração/validação: {e}")
            return None
    
    def _validate_block_with_pos(self, block: Block) -> Dict[str, Any]:
        """
        Valida bloco usando sistema PoS.
        
        Args:
            block: Bloco a ser validado
            
        Returns:
            Resultado da validação com informações do validator
        """
        # Selecionar validator para esta rodada
        validator = self.consensus_service.select_validator_for_round(block.height)
        if not validator:
            return {"is_valid": False, "validator": None, "reason": "No validators available"}
        
        # Preparar dados do bloco para validação
        block_data = {
            "hash": block.hash.value,
            "previous_hash": block.previous_hash.value if block.previous_hash else None,
            "transactions": [tx.to_dict() for tx in block.transactions],
            "timestamp": block.timestamp.value,
            "height": block.height,
            "nonce": block.nonce,
            "difficulty": block.difficulty
        }
        
        # Validar usando PoS
        is_valid = self.consensus_service.validate_block(validator, block_data)
        
        return {
            "is_valid": is_valid,
            "validator": validator,
            "reason": "Validation successful" if is_valid else "Validation failed"
        }
    
    def _distribute_rewards(self, block: Block, validator: Optional[Validator]) -> None:
        """
        Distribui recompensas entre miner e validator.
        
        Args:
            block: Bloco minerado
            validator: Validator que validou o bloco
        """
        # Calcular recompensas usando política monetária unificada
        total_reward = BlockchainConfig.calculate_block_reward(block.height)
        validator_reward = BlockchainConfig.calculate_staking_reward(block.height)
        miner_reward = total_reward - validator_reward
        
        # Adicionar taxas das transações ao miner
        total_fees = block.get_total_transaction_fees()
        miner_reward += total_fees
        
        # Registrar recompensas (em implementação real, seria transferido para carteiras)
        self.mining_stats["miner_rewards"] += miner_reward
        if validator:
            self.mining_stats["validator_rewards"] += validator_reward
        
        self.mining_stats["total_rewards_distributed"] += total_reward + total_fees
    
    def _update_stats(self, block: Block, validator: Optional[Validator]) -> None:
        """Atualiza estatísticas do sistema."""
        self.mining_stats["blocks_mined"] += 1
        if validator:
            self.mining_stats["blocks_validated"] += 1
    
    def get_consensus_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do sistema de consenso híbrido.
        
        Returns:
            Estatísticas consolidadas
        """
        blockchain_stats = self.blockchain.get_chain_stats()
        
        return {
            "consensus_type": "Hybrid PoW/PoS",
            "blockchain_stats": blockchain_stats,
            "mining_stats": {
                "blocks_mined": self.mining_stats["blocks_mined"],
                "blocks_validated": self.mining_stats["blocks_validated"],
                "total_rewards_distributed": float(self.mining_stats["total_rewards_distributed"]),
                "miner_rewards": float(self.mining_stats["miner_rewards"]),
                "validator_rewards": float(self.mining_stats["validator_rewards"]),
                "miner_reward_percentage": float(
                    (self.mining_stats["miner_rewards"] / self.mining_stats["total_rewards_distributed"]) * 100
                ) if self.mining_stats["total_rewards_distributed"] > 0 else 0,
                "validator_reward_percentage": float(
                    (self.mining_stats["validator_rewards"] / self.mining_stats["total_rewards_distributed"]) * 100
                ) if self.mining_stats["total_rewards_distributed"] > 0 else 0
            },
            "active_validators": len(self.consensus_service.active_validators),
            "block_time_seconds": BlockchainConfig.BLOCK_TIME_SECONDS,
            "current_difficulty": self.blockchain.difficulty,
            "current_block_reward": float(BlockchainConfig.calculate_block_reward(len(self.blockchain.blocks)))
        }
    
    def register_validator(self, validator: Validator) -> bool:
        """
        Registra um novo validator no sistema.
        
        Args:
            validator: Validator a ser registrado
            
        Returns:
            True se registrado com sucesso
        """
        try:
            self.consensus_service.register_validator(validator)
            return True
        except Exception:
            return False
    
    def get_next_block_info(self) -> Dict[str, Any]:
        """
        Retorna informações sobre o próximo bloco a ser minerado.
        
        Returns:
            Informações do próximo bloco
        """
        current_height = len(self.blockchain.blocks)
        next_height = current_height + 1
        
        return {
            "next_height": next_height,
            "current_difficulty": self.blockchain.difficulty,
            "expected_reward": float(BlockchainConfig.calculate_block_reward(next_height)),
            "expected_miner_reward": float(
                BlockchainConfig.calculate_block_reward(next_height) * Decimal("0.85")
            ),
            "expected_validator_reward": float(
                BlockchainConfig.calculate_staking_reward(next_height)
            ),
            "target_block_time": BlockchainConfig.BLOCK_TIME_SECONDS,
            "active_validators": len(self.consensus_service.active_validators)
        }
