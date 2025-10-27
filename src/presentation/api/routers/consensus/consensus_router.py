"""
Router para endpoints de Consenso (Staking e Validadores)
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from src.application.consensus.commands.register_validator import RegisterValidatorCommand
from src.application.consensus.commands.register_validator_handler import RegisterValidatorHandlerImpl
from src.application.consensus.dto.consensus_dto import ValidatorDTO, ConsensusStatsDTO, StakeReceiptDTO
from src.domain.consensus.value_objects.stake_amount import StakeAmount
from src.domain.shared.value_objects.wallet_address import WalletAddress
from src.domain.shared.exceptions import DomainException


router = APIRouter(
    prefix="/consenso",
    tags=["Consenso"],
    responses={
        404: {"description": "Validador não encontrado"},
        400: {"description": "Requisição inválida"},
        409: {"description": "Conflito (ex: validador já existe)"},
    },
)


# Dependency para o handler de registro de validador
async def get_register_validator_handler() -> RegisterValidatorHandlerImpl:
    """
    Dependency para obter o handler de registro de validador.
    
    Em uma implementação real, isso seria injetado via container DI.
    """
    from src.infrastructure.persistence.repositories.consensus.validator_repository_impl import SQLiteValidatorRepository
    from src.domain.consensus.services.consensus_service import ConsensusService
    
    repository = SQLiteValidatorRepository()
    consensus_service = ConsensusService()
    
    return RegisterValidatorHandlerImpl(repository, consensus_service)


@router.post(
    "/validadores",
    response_model=StakeReceiptDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar Novo Validador",
    description="Registra um novo validador no sistema de consenso PoS"
)
async def register_validator(
    wallet_address: str,
    stake_amount_cnb: float,
    metadata: dict = None,
    handler: RegisterValidatorHandlerImpl = Depends(get_register_validator_handler)
) -> StakeReceiptDTO:
    """
    Registra um novo validador no sistema de consenso.
    
    - **wallet_address**: Endereço da carteira do validador
    - **stake_amount_cnb**: Quantidade de CNB para stake (mínimo 1000)
    - **metadata**: Metadados adicionais (opcional)
    
    Returns:
        Recibo da operação de registro
    """
    try:
        # Validar e converter parâmetros
        wallet_addr = WalletAddress(wallet_address)
        stake_amount = StakeAmount.from_cnb(stake_amount_cnb)
        
        # Criar comando
        command = RegisterValidatorCommand(
            wallet_address=wallet_addr,
            stake_amount=stake_amount,
            metadata=metadata
        )
        
        # Executar comando
        receipt = await handler.handle(command)
        
        return receipt
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Parâmetros inválidos: {str(e)}"
        )
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.get(
    "/validadores",
    response_model=List[ValidatorDTO],
    summary="Listar Validadores",
    description="Lista todos os validadores registrados no sistema"
)
async def list_validators() -> List[ValidatorDTO]:
    """
    Lista todos os validadores registrados.
    
    Returns:
        Lista de validadores
    """
    try:
        from src.infrastructure.persistence.repositories.consensus.validator_repository_impl import SQLiteValidatorRepository
        
        repository = SQLiteValidatorRepository()
        validators = await repository.find_all()
        
        # Converter para DTOs
        validator_dtos = []
        for validator in validators:
            dto = ValidatorDTO(
                id=validator.id,
                wallet_address=validator.wallet_address,
                stake_amount_cnb=validator.stake_amount.to_cnb(),
                is_active=validator.is_active,
                blocks_validated=validator.blocks_validated,
                total_rewards_cnb=validator.total_rewards,
                created_at=validator.created_at,
                updated_at=validator.updated_at,
                last_validation_at=validator.last_validation_at
            )
            validator_dtos.append(dto)
        
        return validator_dtos
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar validadores: {str(e)}"
        )


@router.get(
    "/validadores/ativos",
    response_model=List[ValidatorDTO],
    summary="Listar Validadores Ativos",
    description="Lista apenas os validadores ativos no sistema"
)
async def list_active_validators() -> List[ValidatorDTO]:
    """
    Lista apenas os validadores ativos.
    
    Returns:
        Lista de validadores ativos
    """
    try:
        from src.infrastructure.persistence.repositories.consensus.validator_repository_impl import SQLiteValidatorRepository
        
        repository = SQLiteValidatorRepository()
        validators = await repository.find_all_active()
        
        # Converter para DTOs
        validator_dtos = []
        for validator in validators:
            dto = ValidatorDTO(
                id=validator.id,
                wallet_address=validator.wallet_address,
                stake_amount_cnb=validator.stake_amount.to_cnb(),
                is_active=validator.is_active,
                blocks_validated=validator.blocks_validated,
                total_rewards_cnb=validator.total_rewards,
                created_at=validator.created_at,
                updated_at=validator.updated_at,
                last_validation_at=validator.last_validation_at
            )
            validator_dtos.append(dto)
        
        return validator_dtos
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar validadores ativos: {str(e)}"
        )


@router.get(
    "/estatisticas",
    response_model=ConsensusStatsDTO,
    summary="Estatísticas do Consenso",
    description="Retorna estatísticas do sistema de consenso"
)
async def get_consensus_stats() -> ConsensusStatsDTO:
    """
    Retorna estatísticas do sistema de consenso.
    
    Returns:
        Estatísticas do consenso
    """
    try:
        from src.domain.consensus.services.consensus_service import ConsensusService
        
        consensus_service = ConsensusService()
        stats = consensus_service.get_consensus_stats()
        
        return ConsensusStatsDTO(
            total_validators=stats["total_validators"],
            total_stake_cnb=stats["total_stake_cnb"],
            current_round=stats["current_round"],
            block_time_seconds=stats["block_time_seconds"],
            min_stake_cnb=stats["min_stake_cnb"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter estatísticas: {str(e)}"
        )
