"""
Serviço de Governança Participativa - Economia da Consciência
"""

from decimal import Decimal
from typing import List, Dict, Optional
from dataclasses import dataclass

from ..entities.governance_proposal import (
    GovernanceProposal, 
    ProposalType, 
    ProposalStatus, 
    VoteChoice
)
from ...shared.value_objects.money import Money
from ...shared.value_objects.wallet_address import WalletAddress
from ...shared.value_objects.timestamp import Timestamp


@dataclass(frozen=True)
class GovernanceMetrics:
    """Métricas de governança participativa"""
    
    total_proposals: int
    active_proposals: int
    passed_proposals: int
    rejected_proposals: int
    executed_proposals: int
    total_participants: int
    average_participation_rate: Decimal
    treasury_balance: Money
    community_engagement_score: Decimal  # 0-100


class GovernanceService:
    """
    Serviço de Governança Participativa.
    
    Responsabilidades:
    - Gerenciar propostas de governança
    - Facilitar votação participativa
    - Executar decisões da comunidade
    - Promover democracia descentralizada
    """
    
    def __init__(self):
        self.proposals: List[GovernanceProposal] = []
        self.treasury_balance = Money(Decimal("1000000"))  # 1M CNB inicial
        self.total_participants = 0
        self.community_engagement_score = Decimal("0")
    
    def create_proposal(
        self,
        proposal_id: str,
        title: str,
        description: str,
        proposal_type: ProposalType,
        detailed_description: str,
        implementation_plan: str,
        expected_outcomes: List[str],
        risks_and_mitigations: str,
        voting_duration_days: int,
        quorum_threshold: Decimal,
        approval_threshold: Decimal,
        proposer_address: WalletAddress,
        treasury_impact: Money = Money(Decimal("0")),
        protocol_changes: Optional[Dict[str, str]] = None
    ) -> GovernanceProposal:
        """Cria uma nova proposta de governança"""
        current_time = Timestamp.now()
        voting_start = Timestamp(current_time.value + 86400)  # 24h para revisão
        voting_end = Timestamp(voting_start.value + (voting_duration_days * 86400))
        
        proposal = GovernanceProposal.create_proposal(
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
            protocol_changes=protocol_changes
        )
        
        self.proposals.append(proposal)
        return proposal
    
    def activate_proposal(self, proposal_id: str) -> bool:
        """Ativa uma proposta para votação"""
        proposal = self._find_proposal_by_id(proposal_id)
        if not proposal:
            return False
        
        try:
            proposal.activate_voting()
            return True
        except ValueError:
            return False
    
    def vote_on_proposal(
        self,
        proposal_id: str,
        voter_address: WalletAddress,
        vote_choice: VoteChoice,
        voting_power: Decimal
    ) -> bool:
        """Vota em uma proposta"""
        proposal = self._find_proposal_by_id(proposal_id)
        if not proposal:
            return False
        
        try:
            proposal.vote(voter_address, vote_choice, voting_power)
            
            # Atualizar contador de participantes únicos
            if str(voter_address) not in [str(p.proposer_address) for p in self.proposals]:
                self.total_participants += 1
            
            return True
        except ValueError:
            return False
    
    def finalize_proposal(self, proposal_id: str) -> bool:
        """Finaliza a votação de uma proposta"""
        proposal = self._find_proposal_by_id(proposal_id)
        if not proposal:
            return False
        
        try:
            proposal.finalize_voting()
            return True
        except ValueError:
            return False
    
    def execute_proposal(self, proposal_id: str, execution_result: str) -> bool:
        """Executa uma proposta aprovada"""
        proposal = self._find_proposal_by_id(proposal_id)
        if not proposal:
            return False
        
        try:
            proposal.execute_proposal(execution_result)
            
            # Atualizar tesouro se necessário
            if proposal.treasury_impact.to_cnb() != 0:
                self.treasury_balance += proposal.treasury_impact
            
            return True
        except ValueError:
            return False
    
    def get_active_proposals(self) -> List[GovernanceProposal]:
        """Retorna propostas ativas"""
        return [p for p in self.proposals if p.status == ProposalStatus.ACTIVE]
    
    def get_proposals_by_type(self, proposal_type: ProposalType) -> List[GovernanceProposal]:
        """Retorna propostas por tipo"""
        return [p for p in self.proposals if p.proposal_type == proposal_type]
    
    def get_proposals_by_status(self, status: ProposalStatus) -> List[GovernanceProposal]:
        """Retorna propostas por status"""
        return [p for p in self.proposals if p.status == status]
    
    def get_proposal_by_id(self, proposal_id: str) -> Optional[GovernanceProposal]:
        """Busca proposta por ID"""
        return self._find_proposal_by_id(proposal_id)
    
    def get_user_voting_history(self, user_address: WalletAddress) -> List[Dict]:
        """Retorna histórico de votação de um usuário"""
        user_votes = []
        
        for proposal in self.proposals:
            voter_addr_str = str(user_address)
            if voter_addr_str in proposal.voters:
                vote_choice = proposal.voters[voter_addr_str]
                voting_power = proposal.voting_power[voter_addr_str]
                
                user_votes.append({
                    "proposal_id": proposal.proposal_id,
                    "title": proposal.title,
                    "proposal_type": proposal.proposal_type.value,
                    "vote_choice": vote_choice.value,
                    "voting_power": float(voting_power),
                    "status": proposal.status.value,
                    "voting_summary": proposal.get_voting_summary()
                })
        
        return user_votes
    
    def get_governance_metrics(self) -> GovernanceMetrics:
        """Retorna métricas de governança"""
        total_proposals = len(self.proposals)
        active_proposals = len(self.get_active_proposals())
        passed_proposals = len(self.get_proposals_by_status(ProposalStatus.PASSED))
        rejected_proposals = len(self.get_proposals_by_status(ProposalStatus.REJECTED))
        executed_proposals = len(self.get_proposals_by_status(ProposalStatus.EXECUTED))
        
        # Calcular taxa média de participação
        if total_proposals > 0:
            total_participation = sum(
                p._calculate_participation_rate() for p in self.proposals
                if p.status in [ProposalStatus.PASSED, ProposalStatus.REJECTED]
            )
            average_participation_rate = total_participation / total_proposals
        else:
            average_participation_rate = Decimal("0")
        
        # Calcular score de engajamento da comunidade
        engagement_factors = [
            min(self.total_participants / Decimal("100"), Decimal("30")),  # Participantes
            min(average_participation_rate, Decimal("40")),  # Taxa de participação
            min(executed_proposals * Decimal("2"), Decimal("30"))  # Propostas executadas
        ]
        community_engagement_score = sum(engagement_factors)
        
        return GovernanceMetrics(
            total_proposals=total_proposals,
            active_proposals=active_proposals,
            passed_proposals=passed_proposals,
            rejected_proposals=rejected_proposals,
            executed_proposals=executed_proposals,
            total_participants=self.total_participants,
            average_participation_rate=average_participation_rate,
            treasury_balance=self.treasury_balance,
            community_engagement_score=community_engagement_score
        )
    
    def get_treasury_balance(self) -> Money:
        """Retorna saldo do tesouro"""
        return self.treasury_balance
    
    def allocate_treasury_funds(self, amount: Money, purpose: str) -> bool:
        """Aloca fundos do tesouro"""
        if amount.to_cnb() > self.treasury_balance.to_cnb():
            return False
        
        self.treasury_balance -= amount
        # TODO: Registrar alocação no histórico
        return True
    
    def get_proposal_statistics(self) -> Dict[str, float]:
        """Retorna estatísticas das propostas"""
        metrics = self.get_governance_metrics()
        
        return {
            "total_proposals": metrics.total_proposals,
            "active_proposals": metrics.active_proposals,
            "passed_proposals": metrics.passed_proposals,
            "rejected_proposals": metrics.rejected_proposals,
            "executed_proposals": metrics.executed_proposals,
            "total_participants": metrics.total_participants,
            "average_participation_rate": float(metrics.average_participation_rate),
            "treasury_balance_cnb": float(metrics.treasury_balance.to_cnb()),
            "community_engagement_score": float(metrics.community_engagement_score),
            "proposals_by_type": {
                proposal_type.value: len(self.get_proposals_by_type(proposal_type))
                for proposal_type in ProposalType
            },
            "proposals_by_status": {
                status.value: len(self.get_proposals_by_status(status))
                for status in ProposalStatus
            }
        }
    
    def get_community_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Retorna ranking de participantes mais ativos"""
        participant_stats = {}
        
        for proposal in self.proposals:
            # Contar proposições
            proposer_addr = str(proposal.proposer_address)
            if proposer_addr not in participant_stats:
                participant_stats[proposer_addr] = {
                    "address": proposer_addr,
                    "proposals_created": 0,
                    "votes_cast": 0,
                    "total_voting_power": Decimal("0"),
                    "engagement_score": Decimal("0")
                }
            
            participant_stats[proposer_addr]["proposals_created"] += 1
            
            # Contar votos
            for voter_addr, vote_choice in proposal.voters.items():
                if voter_addr not in participant_stats:
                    participant_stats[voter_addr] = {
                        "address": voter_addr,
                        "proposals_created": 0,
                        "votes_cast": 0,
                        "total_voting_power": Decimal("0"),
                        "engagement_score": Decimal("0")
                    }
                
                participant_stats[voter_addr]["votes_cast"] += 1
                participant_stats[voter_addr]["total_voting_power"] += proposal.voting_power[voter_addr]
        
        # Calcular score de engajamento
        for addr, stats in participant_stats.items():
            proposal_score = stats["proposals_created"] * Decimal("10")
            vote_score = stats["votes_cast"] * Decimal("2")
            power_score = min(stats["total_voting_power"] / Decimal("1000"), Decimal("20"))
            
            stats["engagement_score"] = proposal_score + vote_score + power_score
        
        # Ordenar por score de engajamento
        sorted_participants = sorted(
            participant_stats.values(),
            key=lambda x: x["engagement_score"],
            reverse=True
        )
        
        return [
            {
                "address": participant["address"],
                "proposals_created": participant["proposals_created"],
                "votes_cast": participant["votes_cast"],
                "total_voting_power": float(participant["total_voting_power"]),
                "engagement_score": float(participant["engagement_score"])
            }
            for participant in sorted_participants[:limit]
        ]
    
    def _find_proposal_by_id(self, proposal_id: str) -> Optional[GovernanceProposal]:
        """Busca proposta por ID"""
        for proposal in self.proposals:
            if proposal.proposal_id == proposal_id:
                return proposal
        return None
