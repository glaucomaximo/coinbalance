"""
DTOs (Data Transfer Objects) do domínio Wallet
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class WalletDTO:
    """DTO padrão para carteira"""

    address: str
    name: str
    public_key: str
    balance_cnb: float
    balance_satoshi: int
    created_at: float
    updated_at: float
    is_active: bool
    metadata: Optional[dict] = None


@dataclass
class BalanceDTO:
    """DTO para saldo"""

    cnb: float
    satoshi: int
    mcnb: float
    formatted: str
