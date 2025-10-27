"""
Eventos de domínio do módulo Wallet
"""

from .wallet_created import WalletCreated
from .balance_updated import BalanceUpdated

__all__ = ["WalletCreated", "BalanceUpdated"]
