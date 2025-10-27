"""
Handler para comando de criação de transferência
"""

from typing import Protocol

from ..commands.create_transfer import CreateTransferCommand
from src.domain.transaction.entities.transaction import Transaction
from src.domain.transaction.repositories.transaction_repository import TransactionRepository
from src.domain.wallet.repositories.wallet_repository import WalletRepository
from src.domain.shared.exceptions import DomainException, InsufficientFundsError


class CreateTransferHandler(Protocol):
    """
    Interface para handler de criação de transferência.
    """
    
    async def execute(self, command: CreateTransferCommand) -> Transaction:
        """
        Executa o comando de criação de transferência.
        
        Args:
            command: Comando de criação
            
        Returns:
            Transação criada
            
        Raises:
            DomainException: Se houver erro no domínio
        """
        ...


class CreateTransferHandlerImpl:
    """
    Implementação do handler para criação de transferência.
    """
    
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        wallet_repository: WalletRepository
    ):
        self.transaction_repository = transaction_repository
        self.wallet_repository = wallet_repository
    
    async def execute(self, command: CreateTransferCommand) -> Transaction:
        """
        Executa o comando de criação de transferência.
        
        Args:
            command: Comando de criação
            
        Returns:
            Transação criada
            
        Raises:
            DomainException: Se houver erro no domínio
        """
        try:
            # Verificar se a carteira de origem existe
            from_wallet = await self.wallet_repository.find_by_address(command.from_address)
            if not from_wallet:
                raise DomainException(f"Wallet {command.from_address} not found")
            
            # Verificar se a carteira de destino existe
            to_wallet = await self.wallet_repository.find_by_address(command.to_address)
            if not to_wallet:
                raise DomainException(f"Wallet {command.to_address} not found")
            
            # Verificar saldo suficiente
            total_amount = command.amount + command.fee
            if from_wallet.balance.value < total_amount:
                raise InsufficientFundsError(
                    f"Insufficient funds. Required: {total_amount}, Available: {from_wallet.balance.value}"
                )
            
            # Criar transação
            transaction = Transaction.create_transfer(
                from_address=command.from_address,
                to_address=command.to_address,
                amount=command.amount,
                fee=command.fee,
                memo=command.memo,
                metadata=command.metadata
            )
            
            # Salvar transação
            await self.transaction_repository.save(transaction)
            
            # Processar eventos de domínio
            await self._process_domain_events(transaction)
            
            return transaction
            
        except Exception as e:
            if isinstance(e, DomainException):
                raise
            raise DomainException(f"Error creating transfer: {str(e)}")
    
    async def _process_domain_events(self, transaction: Transaction) -> None:
        """
        Processa eventos de domínio da transação.
        
        Args:
            transaction: Transação com eventos pendentes
        """
        events = transaction.get_events()
        
        for event in events:
            # Aqui seria implementado o dispatcher de eventos
            # Por enquanto, apenas limpar os eventos
            pass
        
        transaction.clear_events()
