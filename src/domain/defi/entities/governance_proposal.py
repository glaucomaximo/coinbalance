"""
Entidade GovernanceProposal - Governança Participativa
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from decimal import Decimal
from enum import Enum

from ...shared.value_objects.money import Money
from ...shared.value_objects.timestamp import Timestamp
from ...shared.value_objects.wallet_address import WalletAddress
from ...shared.domain_events.base import DomainEvent


class ProposalType(Enum):
    """Tipos de propostas de governança"""
    MONETARY_POLICY = "monetary_policy"        # Política monetária
    PROTOCOL_UPGRADE = "protocol_upgrade"      # Atualização do protocolo
    TREASURY_ALLOCATION = "treasury_allocation" # Alocação do tesouro
    PARAMETER_CHANGE = "parameter_change"     # Mudança de parâmetros
    COMMUNITY_FUNDING = "community_funding"    # Financiamento comunitário
    ESG_INITIATIVE = "esg_initiative"          # Iniciativa ESG


class ProposalStatus(Enum):
    """Status da proposta"""
    DRAFT = "draft"                    # Rascunho
    ACTIVE = "active"                  # Ativa (votação)
    PASSED = "passed"                  # Aprovada
    REJECTED = "rejected"              # Rejeitada
    EXECUTED = "executed"              # Executada
    EXPIRED = "expired"                # Expirada


class VoteChoice(Enum):
    """Opções de voto"""
    YES = "yes"                        # Sim
    NO = "no"                          # Não
    ABSTAIN = "abstain"                # Abstenção


@dataclass
class GovernanceProposal:
    """
    Entidade GovernanceProposal - Aggregate Root.
    
    Representa uma proposta de governança participativa que permite
    à comunidade decidir sobre o futuro da plataforma CNB.
    
    Características Disruptivas:
    - Governança verdadeiramente descentralizada
    - Votação ponderada por stake CNB
    - Transparência total via blockchain
    - Execução automática de propostas aprovadas
    - Incentivos para participação ativa
    """
    
    # Identity
    proposal_id: str
    title: str
    description: str
    proposal_type: ProposalType
    
    # Content
    detailed_description: str
    implementation_plan: str
    expected_outcomes: List[str]
    risks_and_mitigations: str
    
    # Voting Parameters
    voting_start: Timestamp
    voting_end: Timestamp
    quorum_threshold: Decimal  # % mínimo de participação
    approval_threshold: Decimal  # % mínimo para aprovação
    
    # Participants
    proposer_address: WalletAddress
    
    # Financial Impact
    treasury_impact: Money = Money(Decimal("0"))
    protocol_changes: Dict[str, str] = field(default_factory=dict)
    
    # Current State
    status: ProposalStatus = ProposalStatus.DRAFT
    total_votes: int = 0
    yes_votes: int = 0
    no_votes: int = 0
    abstain_votes: int = 0
    total_voting_power: Decimal = Decimal("0")
    
    # Voting Data
    voters: Dict[str, VoteChoice] = field(default_factory=dict)  # address -> vote
    voting_power: Dict[str, Decimal] = field(default_factory=dict)  # address -> power
    
    # Execution
    execution_timestamp: Optional[Timestamp] = None
    execution_result: Optional[str] = None
    
    # Domain Events
    _events: List[DomainEvent] = field(default_factory=list, init=False, repr=False)
    
    def __post_init__(self):
        """Validação após inicialização"""
        self._validate()
    
    def _validate(self):
        """Valida invariantes do domínio"""
        if self.voting_start.value >= self.voting_end.value:
            raise ValueError("Voting start must be before voting end")
        if self.quorum_threshold <= 0 or self.quorum_threshold > 100:
            raise ValueError("Quorum threshold must be between 0 and 100")
        if self.approval_threshold <= 0 or self.approval_threshold > 100:
            raise ValueError("Approval threshold must be between 0 and 100")
    
    @classmethod
    def create_proposal(
        cls,
        proposal_id: str,
        title: str,
        description: str,
        proposal_type: ProposalType,
        detailed_description: str,
        implementation_plan: str,
        expected_outcomes: List[str],
        risks_and_mitigations: str,
        voting_start: Timestamp,
        voting_end: Timestamp,
        quorum_threshold: Decimal,
        approval_threshold: Decimal,
        proposer_address: WalletAddress,
        treasury_impact: Money = Money(Decimal("0")),
        protocol_changes: Optional[Dict[str, str]] = None
    ) -> "GovernanceProposal":
        """Factory method para criar uma nova proposta"""
        proposal = cls(
            proposal_id=proposal_id,
            title=title,
            description=description,
            proposal_type=proposal_type,
            detailed_description=detailed_description,
            implementation_plan=implementation_plan,
            expected_outcomes=expected_outcomes,
            risks_and_mitigations=risks_and_mitigations,
            voting_start=voting_start,
            voting_end=voting_end,
            quorum_threshold=quorum_threshold,
            approval_threshold=approval_threshold,
            proposer_address=proposer_address,
            treasury_impact=treasury_impact,
            protocol_changes=protocol_changes or {}
        )
        
        # TODO: Dispatch ProposalCreatedEvent
        return proposal
    
    def activate_voting(self) -> None:
        """Ativa a votação da proposta"""
        if self.status != ProposalStatus.DRAFT:
            raise ValueError("Only draft proposals can be activated")
        
        current_time = Timestamp.now()
        if current_time.value < self.voting_start.value:
            raise ValueError("Voting period has not started yet")
        
        self.status = ProposalStatus.ACTIVE
        # TODO: Dispatch ProposalActivatedEvent
    
    def vote(
        self, 
        voter_address: WalletAddress, 
        vote_choice: VoteChoice, 
        voting_power: Decimal
    ) -> None:
        """Registra um voto na proposta"""
        if self.status != ProposalStatus.ACTIVE:
            raise ValueError("Proposal must be active to receive votes")
        
        current_time = Timestamp.now()
        if current_time.value < self.voting_start.value or current_time.value > self.voting_end.value:
            raise ValueError("Voting period is not active")
        
        voter_addr_str = str(voter_address)
        
        # Remover voto anterior se existir
        if voter_addr_str in self.voters:
            self._remove_vote(voter_addr_str)
        
        # Registrar novo voto
        self.voters[voter_addr_str] = vote_choice
        self.voting_power[voter_addr_str] = voting_power
        
        # Atualizar contadores
        self.total_votes += 1
        self.total_voting_power += voting_power
        
        if vote_choice == VoteChoice.YES:
            self.yes_votes += 1
        elif vote_choice == VoteChoice.NO:
            self.no_votes += 1
        else:  # ABSTAIN
            self.abstain_votes += 1
        
        # TODO: Dispatch VoteCastEvent
    
    def _remove_vote(self, voter_addr_str: str) -> None:
        """Remove um voto existente"""
        if voter_addr_str not in self.voters:
            return
        
        vote_choice = self.voters[voter_addr_str]
        voting_power = self.voting_power[voter_addr_str]
        
        # Atualizar contadores
        self.total_votes -= 1
        self.total_voting_power -= voting_power
        
        if vote_choice == VoteChoice.YES:
            self.yes_votes -= 1
        elif vote_choice == VoteChoice.NO:
            self.no_votes -= 1
        else:  # ABSTAIN
            self.abstain_votes -= 1
        
        # Remover voto
        del self.voters[voter_addr_str]
        del self.voting_power[voter_addr_str]
    
    def finalize_voting(self) -> None:
        """Finaliza a votação e determina o resultado"""
        if self.status != ProposalStatus.ACTIVE:
            raise ValueError("Only active proposals can be finalized")
        
        current_time = Timestamp.now()
        if current_time.value < self.voting_end.value:
            raise ValueError("Voting period has not ended yet")
        
        # Calcular resultados
        participation_rate = self._calculate_participation_rate()
        approval_rate = self._calculate_approval_rate()
        
        # Verificar quorum
        if participation_rate < self.quorum_threshold:
            self.status = ProposalStatus.REJECTED
            # TODO: Dispatch ProposalRejectedEvent (quorum not met)
            return
        
        # Verificar aprovação
        if approval_rate >= self.approval_threshold:
            self.status = ProposalStatus.PASSED
            # TODO: Dispatch ProposalPassedEvent
        else:
            self.status = ProposalStatus.REJECTED
            # TODO: Dispatch ProposalRejectedEvent
    
    def execute_proposal(self, execution_result: str) -> None:
        """Executa a proposta aprovada"""
        if self.status != ProposalStatus.PASSED:
            raise ValueError("Only passed proposals can be executed")
        
        self.status = ProposalStatus.EXECUTED
        self.execution_timestamp = Timestamp.now()
        self.execution_result = execution_result
        
        # TODO: Dispatch ProposalExecutedEvent
    
    def _calculate_participation_rate(self) -> Decimal:
        """Calcula taxa de participação"""
        # Assumindo que há um total de CNB em circulação para calcular participação
        # Em uma implementação real, isso viria de um serviço de supply
        total_cnb_supply = Decimal("21000000")  # Supply total CNB
        if total_cnb_supply == 0:
            return Decimal("0")
        
        return (self.total_voting_power / total_cnb_supply) * Decimal("100")
    
    def _calculate_approval_rate(self) -> Decimal:
        """Calcula taxa de aprovação"""
        if self.total_votes == 0:
            return Decimal("0")
        
        return (Decimal(str(self.yes_votes)) / Decimal(str(self.total_votes))) * Decimal("100")
    
    def get_voting_summary(self) -> Dict[str, float]:
        """Retorna resumo da votação"""
        participation_rate = self._calculate_participation_rate()
        approval_rate = self._calculate_approval_rate()
        
        return {
            "total_votes": self.total_votes,
            "yes_votes": self.yes_votes,
            "no_votes": self.no_votes,
            "abstain_votes": self.abstain_votes,
            "total_voting_power": float(self.total_voting_power),
            "participation_rate": float(participation_rate),
            "approval_rate": float(approval_rate),
            "quorum_threshold": float(self.quorum_threshold),
            "approval_threshold": float(self.approval_threshold),
            "meets_quorum": participation_rate >= self.quorum_threshold,
            "meets_approval": approval_rate >= self.approval_threshold
        }
    
    def is_voting_active(self) -> bool:
        """Verifica se a votação está ativa"""
        if self.status != ProposalStatus.ACTIVE:
            return False
        
        current_time = Timestamp.now()
        return self.voting_start.value <= current_time.value <= self.voting_end.value
    
    def get_events(self) -> List[DomainEvent]:
        """Retorna eventos de domínio"""
        return self._events.copy()
    
    def clear_events(self) -> None:
        """Limpa eventos de domínio"""
        self._events.clear()
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            "proposal_id": self.proposal_id,
            "title": self.title,
            "description": self.description,
            "proposal_type": self.proposal_type.value,
            "status": self.status.value,
            "voting_start": self.voting_start.value,
            "voting_end": self.voting_end.value,
            "quorum_threshold": float(self.quorum_threshold),
            "approval_threshold": float(self.approval_threshold),
            "treasury_impact": float(self.treasury_impact.to_cnb()),
            "proposer_address": str(self.proposer_address),
            "voting_summary": self.get_voting_summary(),
            "is_voting_active": self.is_voting_active()
        }
