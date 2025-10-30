"""
Módulo de autenticação JWT simples para FastAPI.
"""
import time
from typing import Optional, Dict, Any
import os
from jose import jwt
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

ALGORITHM = "HS256"
JWT_SECRET = os.getenv("JWT_SECRET", "jwt_secret_aqui")
JWT_EXPIRES_SECONDS = int(os.getenv("JWT_EXPIRES", "3600"))

_security = HTTPBearer()


def create_access_token(subject: str, role: str = "user", expires_in_seconds: int | None = None) -> str:
    now = int(time.time())
    exp = expires_in_seconds if expires_in_seconds is not None else JWT_EXPIRES_SECONDS
    payload = {"sub": subject, "role": role, "iat": now, "exp": now + exp}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


def verify_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(credentials: HTTPAuthorizationCredentials = _security) -> Dict[str, Any]:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Credenciais ausentes")
    payload = verify_token(credentials.credentials)
    return {"sub": payload.get("sub"), "role": payload.get("role", "user"), "exp": payload.get("exp")}


def require_role(required_role: str):
    async def _dependency(user: Dict[str, Any] = _security):
        # Will be replaced by Depends(get_current_user) in route; kept here for clarity
        raise NotImplementedError
    return _dependency
