"""
Value Objects para tipos de transação
"""

from enum import Enum


class TransactionType(Enum):
    """Tipos de transação suportados"""
    
    GENESIS = "genesis"
    TRANSFER = "transfer"
    MINING_REWARD = "mining_reward"
    CONTRACT_CALL = "contract_call"
    FEE = "fee"
    REWARD = "reward"
