"""
Módulo de autenticação JWT simples para FastAPI.
"""
import time
from typing import Optional, Dict, Any
from jose import jwt
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

ALGORITHM = "HS256"
# Em produção: use variável de ambiente
JWT_SECRET = "jwt_secret_aqui"

_security = HTTPBearer()


def create_access_token(subject: str, expires_in_seconds: int = 3600) -> str:
    now = int(time.time())
    payload = {"sub": subject, "iat": now, "exp": now + expires_in_seconds}
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
    return {"sub": payload.get("sub"), "exp": payload.get("exp")}
