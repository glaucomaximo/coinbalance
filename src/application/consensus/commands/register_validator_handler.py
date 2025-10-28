"""
Handler para comando de registro de validador
"""

from typing import Protocol
import time
import logging

from ..commands.register_validator import RegisterValidatorCommand
from ..dto.consensus_dto import ValidatorDTO, StakeReceiptDTO
from src.domain.consensus.entities.validator import Validator
from src.domain.consensus.services.consensus_service import ConsensusService
from src.domain.consensus.repositories.validator_repository import ValidatorRepository
from src.domain.shared.exceptions import DomainException
from src.application.common.interfaces.use_case import UseCase

logger = logging.getLogger(__name__)


class RegisterValidatorHandler(UseCase[RegisterValidatorCommand, StakeReceiptDTO]):
    """
    Interface para handler de registro de validador.
    """
    
    async def execute(self, command: RegisterValidatorCommand) -> StakeReceiptDTO:
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


class RegisterValidatorHandlerImpl(RegisterValidatorHandler):
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
    
    async def execute(self, command: RegisterValidatorCommand) -> StakeReceiptDTO:
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
            logger.info(f"Iniciando registro de validador para endereço: {command.wallet_address}")
            
            # Verificar se já existe validador para este endereço
            existing_validator = await self.validator_repository.find_by_wallet_address(
                command.wallet_address
            )
            
            if existing_validator:
                raise DomainException(
                    f"Já existe validador para o endereço {command.wallet_address}"
                )
            
            # Validar stake mínimo
            if command.stake_amount.value <= 0:
                raise DomainException("Stake deve ser maior que zero")
            
            # Criar novo validador
            validator = Validator.create(
                wallet_address=command.wallet_address,
                stake_amount=command.stake_amount,
                metadata=command.metadata or {}
            )
            
            logger.info(f"Validador criado com ID: {validator.id}")
            
            # Salvar no repositório
            await self.validator_repository.save(validator)
            
            # Registrar no serviço de consenso
            self.consensus_service.register_validator(validator)
            
            # Processar eventos de domínio
            await self._process_domain_events(validator)
            
            # Retornar recibo
            receipt = StakeReceiptDTO(
                validator_id=validator.id,
                operation_type="register",
                amount_cnb=float(command.stake_amount.value),
                new_total_stake_cnb=float(validator.stake_amount.value),
                timestamp=time.time()
            )
            
            logger.info(f"Validador registrado com sucesso: {validator.id}")
            return receipt
            
        except DomainException:
            raise
        except Exception as e:
            logger.error(f"Erro ao registrar validador: {e}")
            raise DomainException(f"Erro ao registrar validador: {str(e)}")
    
    async def _process_domain_events(self, validator: Validator) -> None:
        """
        Processa eventos de domínio do validador.
        
        Args:
            validator: Validador com eventos pendentes
        """
        try:
            events = validator.get_events()
            
            for event in events:
                logger.info(f"Processando evento de domínio: {event.__class__.__name__}")
                # Aqui seria implementado o dispatcher de eventos
                # Por enquanto, apenas logar o evento
                
            validator.clear_events()
            
        except Exception as e:
            logger.error(f"Erro ao processar eventos de domínio: {e}")
            # Não re-raise para não interromper o fluxo principal
