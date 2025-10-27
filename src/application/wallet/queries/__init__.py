"""
Queries do domínio Wallet (Read Operations - CQRS)
"""

from .get_wallet import GetWalletQuery, GetWalletQueryHandler

__all__ = ["GetWalletQuery", "GetWalletQueryHandler"]
