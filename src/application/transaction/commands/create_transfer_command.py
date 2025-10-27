"""
Comando para criar transferência entre carteiras
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from src.domain.shared.value_objects.money import Money
from src.domain.shared.value_objects.wallet_address import WalletAddress
from src.domain.shared.exceptions import DomainException
from src.application.common.interfaces.use_case import UseCase

@dataclass
class CreateTransferCommand:
    """Comando para criar transferência entre carteiras"""
    
    from_address: str
    to_address: str
    amount: Decimal
    reason: str
    fee: Optional[Decimal] = None
    
    def __post_init__(self):
        """Validação pós-inicialização"""
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        
        if not self.reason or len(self.reason.strip()) == 0:
            raise ValueError("Reason is required")
        
        if len(self.reason) > 200:
            raise ValueError("Reason too long (max 200 characters)")

@dataclass
class CreateTransferResult:
    """Resultado da criação de transferência"""
    
    transaction_id: str
    from_address: str
    to_address: str
    amount: Decimal
    fee: Decimal
    total_amount: Decimal
    reason: str
    status: str
    created_at: float

class CreateTransferCommandHandler(UseCase[CreateTransferCommand, CreateTransferResult]):
    """Handler para criar transferência entre carteiras"""
    
    def __init__(
        self,
        wallet_repository,
        transaction_repository,
        event_dispatcher
    ):
        self.wallet_repository = wallet_repository
        self.transaction_repository = transaction_repository
        self.event_dispatcher = event_dispatcher
    
    async def execute(self, command: CreateTransferCommand) -> CreateTransferResult:
        """
        Executa a criação de transferência entre carteiras
        
        Args:
            command: Comando de transferência
            
        Returns:
            Resultado da transferência
            
        Raises:
            ValueError: Se os dados são inválidos
            RuntimeError: Se a transferência falha
        """
        try:
            # Validar endereços
            from_wallet_address = WalletAddress(command.from_address)
            to_wallet_address = WalletAddress(command.to_address)
            
            # Buscar carteiras
            from_wallet = await self.wallet_repository.find_by_address(from_wallet_address)
            to_wallet = await self.wallet_repository.find_by_address(to_wallet_address)
            
            if not from_wallet:
                raise DomainException(f"Source wallet not found: {command.from_address}", "SOURCE_WALLET_NOT_FOUND")
            
            if not to_wallet:
                raise DomainException(f"Destination wallet not found: {command.to_address}", "DESTINATION_WALLET_NOT_FOUND")
            
            # Verificar se não é a mesma carteira
            if from_wallet.address == to_wallet.address:
                raise DomainException("Cannot transfer to the same wallet", "SAME_WALLET_TRANSFER")
            
            # Verificar se carteiras estão ativas
            if not from_wallet.is_active:
                raise DomainException("Source wallet is not active", "SOURCE_WALLET_INACTIVE")
            
            if not to_wallet.is_active:
                raise DomainException("Destination wallet is not active", "DESTINATION_WALLET_INACTIVE")
            
            # Calcular taxa (se não fornecida)
            fee = command.fee or self._calculate_fee(command.amount)
            total_amount = command.amount + fee
            
            # Verificar saldo suficiente
            if not from_wallet.has_sufficient_balance(Money(total_amount)):
                raise DomainException("Insufficient balance for transfer", "INSUFFICIENT_BALANCE")
            
            # Criar valor monetário
            transfer_amount = Money(command.amount)
            fee_amount = Money(fee)
            
            # Executar transferência
            from_wallet.debit(Money(total_amount), f"Transfer to {command.to_address}")
            to_wallet.credit(transfer_amount, f"Transfer from {command.from_address}")
            
            # Salvar carteiras atualizadas
            await self.wallet_repository.save(from_wallet)
            await self.wallet_repository.save(to_wallet)
            
            # Criar registro de transação
            transaction_id = f"tx_{from_wallet_address.value[:8]}_{to_wallet_address.value[:8]}_{int(from_wallet.updated_at.value)}"
            
            # Disparar eventos
            for event in from_wallet.get_events():
                await self.event_dispatcher.dispatch(event)
            for event in to_wallet.get_events():
                await self.event_dispatcher.dispatch(event)
            
            # Limpar eventos das carteiras
            from_wallet.clear_events()
            to_wallet.clear_events()
            
            return CreateTransferResult(
                transaction_id=transaction_id,
                from_address=command.from_address,
                to_address=command.to_address,
                amount=command.amount,
                fee=fee,
                total_amount=total_amount,
                reason=command.reason,
                status="completed",
                created_at=from_wallet.updated_at.value
            )
            
        except Exception as e:
            # Re-lançar DomainException sem modificação
            if isinstance(e, DomainException):
                raise e
            raise RuntimeError(f"Transfer failed: {str(e)}")
    
    def _calculate_fee(self, amount: Decimal) -> Decimal:
        """
        Calcula taxa de transferência
        
        Args:
            amount: Valor da transferência
            
        Returns:
            Taxa calculada
        """
        # Taxa fixa de 0.01 CNB ou 0.1% do valor, o que for maior
        fixed_fee = Decimal("0.01")
        percentage_fee = amount * Decimal("0.001")  # 0.1%
        
        return max(fixed_fee, percentage_fee)
