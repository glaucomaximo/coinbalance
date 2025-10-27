"""
Schemas para endpoints de Transações
"""

from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class CreateTransferRequest(BaseModel):
    """Request para criar transferência"""
    
    from_address: str = Field(..., description="Endereço da carteira de origem")
    to_address: str = Field(..., description="Endereço da carteira de destino")
    amount: Decimal = Field(..., gt=0, description="Valor a ser transferido em CNB")
    fee: Decimal = Field(default=Decimal("0.001"), ge=0, description="Taxa da transação em CNB")
    memo: Optional[str] = Field(None, max_length=255, description="Memo opcional")
    metadata: Optional[dict] = Field(default_factory=dict, description="Metadados adicionais")
    
    class Config:
        json_schema_extra = {
            "example": {
                "from_address": "abc123def456...",
                "to_address": "xyz789uvw012...",
                "amount": "10.5",
                "fee": "0.001",
                "memo": "Pagamento de serviços",
                "metadata": {"category": "payment"}
            }
        }


class CreateStakeRequest(BaseModel):
    """Request para criar staking"""
    
    wallet_address: str = Field(..., description="Endereço da carteira")
    amount: Decimal = Field(..., gt=0, description="Valor para stake em CNB")
    fee: Decimal = Field(default=Decimal("0.001"), ge=0, description="Taxa da transação em CNB")
    metadata: Optional[dict] = Field(default_factory=dict, description="Metadados adicionais")
    
    class Config:
        json_schema_extra = {
            "example": {
                "wallet_address": "abc123def456...",
                "amount": "1000.0",
                "fee": "0.001",
                "metadata": {"validator_type": "full_node"}
            }
        }


class TransactionResponse(BaseModel):
    """Response de transação"""
    
    id: str
    from_address: Optional[str]
    to_address: str
    amount_cnb: Decimal
    fee_cnb: Decimal
    transaction_type: str
    status: str
    created_at: float
    confirmed_at: Optional[float]
    block_height: Optional[int]
    transaction_hash: Optional[str]
    memo: Optional[str]
    metadata: dict
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "tx_abc123def456...",
                "from_address": "abc123def456...",
                "to_address": "xyz789uvw012...",
                "amount_cnb": "10.5",
                "fee_cnb": "0.001",
                "transaction_type": "transfer",
                "status": "pending",
                "created_at": 1698412800.0,
                "confirmed_at": None,
                "block_height": None,
                "transaction_hash": None,
                "memo": "Pagamento de serviços",
                "metadata": {"category": "payment"}
            }
        }


class TransactionListResponse(BaseModel):
    """Response de lista de transações"""
    
    transactions: list[TransactionResponse]
    total: int
    limit: int
    offset: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "transactions": [
                    {
                        "id": "tx_abc123def456...",
                        "from_address": "abc123def456...",
                        "to_address": "xyz789uvw012...",
                        "amount_cnb": "10.5",
                        "fee_cnb": "0.001",
                        "transaction_type": "transfer",
                        "status": "confirmed",
                        "created_at": 1698412800.0,
                        "confirmed_at": 1698412900.0,
                        "block_height": 12345,
                        "transaction_hash": "0xabc123...",
                        "memo": "Pagamento de serviços",
                        "metadata": {"category": "payment"}
                    }
                ],
                "total": 1,
                "limit": 50,
                "offset": 0
            }
        }


class TransactionStatsResponse(BaseModel):
    """Response de estatísticas de transações"""
    
    total_transactions: int
    total_volume_cnb: Decimal
    total_fees_cnb: Decimal
    pending_transactions: int
    confirmed_transactions: int
    failed_transactions: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_transactions": 1500,
                "total_volume_cnb": "50000.0",
                "total_fees_cnb": "15.0",
                "pending_transactions": 5,
                "confirmed_transactions": 1490,
                "failed_transactions": 5
            }
        }
