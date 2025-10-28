"""
Handler para comando de criação de transferência
"""

from typing import Protocol
import time
import logging

from ..commands.create_transfer import CreateTransferCommand
from src.domain.transaction.entities.transaction import Transaction
from src.domain.transaction.repositories.transaction_repository import TransactionRepository
from src.domain.wallet.repositories.wallet_repository import WalletRepository
from src.domain.shared.exceptions import DomainException, InsufficientFundsError
from src.application.common.interfaces.use_case import UseCase

logger = logging.getLogger(__name__)


class CreateTransferHandler(UseCase[CreateTransferCommand, Transaction]):
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


class CreateTransferHandlerImpl(CreateTransferHandler):
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
            logger.info(f"Iniciando transferência de {command.from_address} para {command.to_address}")
            
            # Validar endereços
            if command.from_address == command.to_address:
                raise DomainException("Endereço de origem e destino não podem ser iguais")
            
            # Verificar se a carteira de origem existe
            from_wallet = await self.wallet_repository.find_by_address(command.from_address)
            if not from_wallet:
                raise DomainException(f"Carteira de origem {command.from_address} não encontrada")
            
            # Verificar se a carteira de destino existe
            to_wallet = await self.wallet_repository.find_by_address(command.to_address)
            if not to_wallet:
                raise DomainException(f"Carteira de destino {command.to_address} não encontrada")
            
            # Verificar se carteiras estão ativas
            if not from_wallet.is_active:
                raise DomainException("Carteira de origem está inativa")
            
            if not to_wallet.is_active:
                raise DomainException("Carteira de destino está inativa")
            
            # Validar valores
            if command.amount <= 0:
                raise DomainException("Valor da transferência deve ser maior que zero")
            
            if command.fee < 0:
                raise DomainException("Taxa não pode ser negativa")
            
            # Verificar saldo suficiente
            total_amount = command.amount + command.fee
            if from_wallet.balance.value < total_amount:
                raise InsufficientFundsError(
                    f"Saldo insuficiente. Necessário: {total_amount}, Disponível: {from_wallet.balance.value}"
                )
            
            logger.info(f"Saldo suficiente. Criando transação...")
            
            # Criar transação
            transaction = Transaction.create_transfer(
                from_address=command.from_address,
                to_address=command.to_address,
                amount=command.amount,
                fee=command.fee,
                memo=command.memo,
                metadata=command.metadata or {}
            )
            
            logger.info(f"Transação criada com ID: {transaction.id}")
            
            # Salvar transação
            await self.transaction_repository.save(transaction)
            
            # Processar eventos de domínio
            await self._process_domain_events(transaction)
            
            logger.info(f"Transferência criada com sucesso: {transaction.id}")
            return transaction
            
        except (DomainException, InsufficientFundsError):
            raise
        except Exception as e:
            logger.error(f"Erro ao criar transferência: {e}")
            raise DomainException(f"Erro ao criar transferência: {str(e)}")
    
    async def _process_domain_events(self, transaction: Transaction) -> None:
        """
        Processa eventos de domínio da transação.
        
        Args:
            transaction: Transação com eventos pendentes
        """
        try:
            events = transaction.get_events()
            
            for event in events:
                logger.info(f"Processando evento de domínio: {event.__class__.__name__}")
                # Aqui seria implementado o dispatcher de eventos
                # Por enquanto, apenas logar o evento
                
            transaction.clear_events()
            
        except Exception as e:
            logger.error(f"Erro ao processar eventos de domínio: {e}")
            # Não re-raise para não interromper o fluxo principal
