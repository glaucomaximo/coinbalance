"""
Handler para comando de registro de validador
"""

from typing import Protocol

from ..commands.register_validator import RegisterValidatorCommand
from ..dto.consensus_dto import ValidatorDTO, StakeReceiptDTO
from src.domain.consensus.entities.validator import Validator
from src.domain.consensus.services.consensus_service import ConsensusService
from src.domain.consensus.repositories.validator_repository import ValidatorRepository
from src.domain.shared.exceptions import DomainException


class RegisterValidatorHandler(Protocol):
    """
    Interface para handler de registro de validador.
    """
    
    async def handle(self, command: RegisterValidatorCommand) -> StakeReceiptDTO:
        """
        Executa o comando de registro de validador.
        
        Args:
            command: Comando de registro
            
        Returns:
            Recibo da operação
            
        Raises:
            DomainException: Se houver erro no domínio
        """
        ...


class RegisterValidatorHandlerImpl:
    """
    Implementação do handler para registro de validador.
    """
    
    def __init__(
        self,
        validator_repository: ValidatorRepository,
        consensus_service: ConsensusService
    ):
        self.validator_repository = validator_repository
        self.consensus_service = consensus_service
    
    async def handle(self, command: RegisterValidatorCommand) -> StakeReceiptDTO:
        """
        Executa o comando de registro de validador.
        
        Args:
            command: Comando de registro
            
        Returns:
            Recibo da operação
            
        Raises:
            DomainException: Se houver erro no domínio
        """
        try:
            # Verificar se já existe validador para este endereço
            existing_validator = await self.validator_repository.find_by_wallet_address(
                command.wallet_address
            )
            
            if existing_validator:
                raise DomainException(
                    f"Já existe validador para o endereço {command.wallet_address}"
                )
            
            # Criar novo validador
            validator = Validator.create(
                wallet_address=command.wallet_address,
                stake_amount=command.stake_amount,
                metadata=command.metadata
            )
            
            # Salvar no repositório
            await self.validator_repository.save(validator)
            
            # Registrar no serviço de consenso
            self.consensus_service.register_validator(validator)
            
            # Processar eventos de domínio
            await self._process_domain_events(validator)
            
            # Retornar recibo
            return StakeReceiptDTO(
                validator_id=validator.id,
                operation_type="register",
                amount_cnb=command.stake_amount.to_cnb(),
                new_total_stake_cnb=validator.stake_amount.to_cnb(),
                timestamp=validator.created_at
            )
            
        except Exception as e:
            if isinstance(e, DomainException):
                raise
            raise DomainException(f"Erro ao registrar validador: {str(e)}")
    
    async def _process_domain_events(self, validator: Validator) -> None:
        """
        Processa eventos de domínio do validador.
        
        Args:
            validator: Validador com eventos pendentes
        """
        events = validator.get_events()
        
        for event in events:
            # Aqui seria implementado o dispatcher de eventos
            # Por enquanto, apenas limpar os eventos
            pass
        
        validator.clear_events()
