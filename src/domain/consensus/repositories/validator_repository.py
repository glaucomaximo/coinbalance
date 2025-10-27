"""
Interface do repositório para validadores
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.validator import Validator
from ..value_objects.validator_id import ValidatorId
from ...shared.value_objects.wallet_address import WalletAddress


class ValidatorRepository(ABC):
    """
    Interface do repositório para validadores.
    
    Define os contratos para persistência de validadores
    seguindo o padrão Repository do DDD.
    """
    
    @abstractmethod
    async def save(self, validator: Validator) -> None:
        """
        Salva um validador no repositório.
        
        Args:
            validator: Validador a ser salvo
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, validator_id: ValidatorId) -> Optional[Validator]:
        """
        Busca um validador por ID.
        
        Args:
            validator_id: ID do validador
            
        Returns:
            Validador encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_wallet_address(self, wallet_address: WalletAddress) -> Optional[Validator]:
        """
        Busca um validador por endereço de carteira.
        
        Args:
            wallet_address: Endereço da carteira
            
        Returns:
            Validador encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_all_active(self) -> List[Validator]:
        """
        Busca todos os validadores ativos.
        
        Returns:
            Lista de validadores ativos
        """
        pass
    
    @abstractmethod
    async def find_all(self) -> List[Validator]:
        """
        Busca todos os validadores.
        
        Returns:
            Lista de todos os validadores
        """
        pass
    
    @abstractmethod
    async def delete(self, validator_id: ValidatorId) -> None:
        """
        Remove um validador do repositório.
        
        Args:
            validator_id: ID do validador a ser removido
        """
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """
        Conta o número total de validadores.
        
        Returns:
            Número de validadores
        """
        pass
    
    @abstractmethod
    async def count_active(self) -> int:
        """
        Conta o número de validadores ativos.
        
        Returns:
            Número de validadores ativos
        """
        pass
