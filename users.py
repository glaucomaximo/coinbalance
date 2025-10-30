"""
Serviço de Usuários: registro e consulta.
"""
from typing import Optional
from passlib.context import CryptContext
from database_manager import DatabaseManager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    def register(self, username: str, password: str, role: str = "user") -> bool:
        ph = self.hash_password(password)
        return self.db.criar_usuario(username, ph, role)

    def get(self, username: str):
        return self.db.obter_usuario(username)

