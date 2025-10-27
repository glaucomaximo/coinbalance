"""
Schemas para endpoints de Wallet
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class CreateWalletRequest(BaseModel):
    """Request para criar carteira"""

    name: str = Field(..., min_length=1, max_length=100, description="Nome da carteira")
    password: Optional[str] = Field(
        None, min_length=8, description="Senha da carteira (opcional)"
    )
    metadata: Optional[dict] = Field(
        default_factory=dict, description="Metadados adicionais"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Minha Carteira",
                "password": "senha_segura_123",
                "metadata": {"tipo": "pessoal"},
            }
        }


class CreateWalletResponse(BaseModel):
    """Response de carteira criada"""

    address: str
    name: str
    public_key: str
    balance: float
    created_at: float

    class Config:
        json_schema_extra = {
            "example": {
                "address": "abc123def456...",
                "name": "Minha Carteira",
                "public_key": "04a1b2c3...",
                "balance": 0.0,
                "created_at": 1698412800.0,
            }
        }


class GetWalletResponse(BaseModel):
    """Response de consulta de carteira"""

    address: str
    name: str
    public_key: str
    balance_cnb: float
    balance_satoshi: int
    created_at: float
    updated_at: float
    is_active: bool
    metadata: dict

    class Config:
        json_schema_extra = {
            "example": {
                "address": "abc123def456...",
                "name": "Minha Carteira",
                "public_key": "04a1b2c3...",
                "balance_cnb": 100.50,
                "balance_satoshi": 10050000000,
                "created_at": 1698412800.0,
                "updated_at": 1698412900.0,
                "is_active": True,
                "metadata": {"tipo": "pessoal"},
            }
        }


class WalletBalanceResponse(BaseModel):
    """Response de saldo detalhado"""

    address: str
    balance: dict
    units: dict
    timestamp: float

    class Config:
        json_schema_extra = {
            "example": {
                "address": "abc123...",
                "balance": {
                    "cnb": "100.50000000 CNB",
                    "satoshi": "10050000000 sat",
                    "mcnb": "100500000.000000 mCNB",
                },
                "units": {"cnb": 100.5, "satoshi": 10050000000, "mcnb": 100500000.0},
                "timestamp": 1698412800.0,
            }
        }


class WalletOperationRequest(BaseModel):
    """Request para operações de carteira (crédito/débito)"""

    amount: float = Field(..., gt=0, description="Valor da operação")
    reason: str = Field(..., min_length=1, max_length=200, description="Motivo da operação")

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 100.0,
                "reason": "Transferência recebida"
            }
        }


class WalletListResponse(BaseModel):
    """Response de listagem de carteiras"""

    wallets: List[GetWalletResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "wallets": [
                    {
                        "address": "abc123def456...",
                        "name": "Minha Carteira",
                        "public_key": "04a1b2c3...",
                        "balance_cnb": 100.50,
                        "balance_satoshi": 10050000000,
                        "created_at": 1698412800.0,
                        "updated_at": 1698412900.0,
                        "is_active": True,
                        "metadata": {"tipo": "pessoal"}
                    }
                ],
                "total": 1
            }
        }