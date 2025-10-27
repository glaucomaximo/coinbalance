"""
Schemas comuns para toda a API
"""

from pydantic import BaseModel
from typing import Any, Optional


class ErrorResponse(BaseModel):
    """Resposta padrão de erro"""

    success: bool = False
    error: str
    code: Optional[str] = None
    details: Optional[dict] = None
    timestamp: float

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Resource not found",
                "code": "NOT_FOUND",
                "timestamp": 1698412800.0,
            }
        }


class SuccessResponse(BaseModel):
    """Resposta padrão de sucesso"""

    success: bool = True
    message: str
    data: Optional[Any] = None
    timestamp: float

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {},
                "timestamp": 1698412800.0,
            }
        }
