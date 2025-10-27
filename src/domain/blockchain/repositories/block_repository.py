"""
Repositório para Block - Interface do domínio
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.block import Block


class BlockRepository(ABC):
    """Interface para repositório de blocos"""
    
    @abstractmethod
    async def save(self, block: Block) -> None:
        """Salva ou atualiza um bloco"""
        pass
    
    @abstractmethod
    async def find_by_height(self, height: int) -> Optional[Block]:
        """Busca bloco por altura"""
        pass
    
    @abstractmethod
    async def find_by_hash(self, block_hash: str) -> Optional[Block]:
        """Busca bloco por hash"""
        pass
    
    @abstractmethod
    async def find_latest(self) -> Optional[Block]:
        """Busca o último bloco"""
        pass
    
    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Block]:
        """Lista todos os blocos"""
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """Conta total de blocos"""
        pass
    
    @abstractmethod
    async def exists(self, height: int) -> bool:
        """Verifica se bloco existe"""
        pass
