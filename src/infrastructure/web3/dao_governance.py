"""
DAO Governance System para CoinBalance
Implementa sistema completo de governança descentralizada
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
import time
import hashlib

logger = logging.getLogger(__name__)


class ProposalType(Enum):
    """Tipos de proposta"""
    TREASURY = "treasury"  # Gestão do tesouro
    PARAMETER = "parameter"  # Mudança de parâmetros
    UPGRADE = "upgrade"  # Upgrade do sistema
    GRANT = "grant"  # Concessão de fundos
    EMERGENCY = "emergency"  # Proposta de emergência


class ProposalStatus(Enum):
    """Status da proposta"""
    DRAFT = "draft"
    ACTIVE = "active"
    SUCCEEDED = "succeeded"
    DEFEATED = "defeated"
    EXECUTED = "executed"
    EXPIRED = "expired"


class VoteType(Enum):
    """Tipos de voto"""
    FOR = "for"
    AGAINST = "against"
    ABSTAIN = "abstain"


@dataclass
class Proposal:
    """Proposta de governança"""
    proposal_id: str
    title: str
    description: str
    proposal_type: ProposalType
    proposer: str
    targets: List[str]  # Endereços de destino
    values: List[str]  # Valores em ETH
    calldatas: List[str]  # Dados de chamada
    start_block: int
    end_block: int
    status: ProposalStatus
    created_at: float
    executed_at: Optional[float] = None
    for_votes: Decimal = Decimal("0")
    against_votes: Decimal = Decimal("0")
    abstain_votes: Decimal = Decimal("0")
    quorum_votes: Decimal = Decimal("1000000")  # 1M tokens


@dataclass
class Vote:
    """Voto em uma proposta"""
    voter: str
    proposal_id: str
    vote_type: VoteType
    weight: Decimal
    timestamp: float
    reason: Optional[str] = None


@dataclass
class Delegation:
    """Delegação de votos"""
    delegator: str
    delegatee: str
    delegated_at: float
    is_active: bool = True


class DAOGovernanceManager:
    """Gerenciador de Governança DAO"""
    
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.votes: Dict[str, List[Vote]] = {}
        self.delegations: Dict[str, Delegation] = {}
        self.members: Dict[str, Dict[str, Any]] = {}
        self.treasury: Dict[str, Decimal] = {"CNB": Decimal("10000000")}  # 10M CNB
        self.parameters: Dict[str, Any] = {
            "voting_delay": 1,  # 1 bloco
            "voting_period": 17280,  # ~3 dias
            "proposal_threshold": Decimal("100000"),  # 100K tokens
            "quorum_votes": Decimal("1000000"),  # 1M tokens
            "execution_delay": 17280  # ~3 dias
        }
        logger.info("DAOGovernanceManager inicializado")
    
    def create_proposal(self, proposer: str, title: str, description: str,
                       proposal_type: ProposalType, targets: List[str],
                       values: List[str], calldatas: List[str]) -> Proposal:
        """Cria uma nova proposta"""
        try:
            # Verificar se o proposer tem tokens suficientes
            if not self._has_sufficient_tokens(proposer):
                raise ValueError("Tokens insuficientes para criar proposta")
            
            proposal_id = self._generate_proposal_id()
            
            proposal = Proposal(
                proposal_id=proposal_id,
                title=title,
                description=description,
                proposal_type=proposal_type,
                proposer=proposer,
                targets=targets,
                values=values,
                calldatas=calldatas,
                start_block=self._get_current_block() + self.parameters["voting_delay"],
                end_block=self._get_current_block() + self.parameters["voting_delay"] + self.parameters["voting_period"],
                status=ProposalStatus.DRAFT,
                created_at=time.time(),
                quorum_votes=self.parameters["quorum_votes"]
            )
            
            self.proposals[proposal_id] = proposal
            self.votes[proposal_id] = []
            
            logger.info(f"Proposta criada: {title} ({proposal_id})")
            return proposal
            
        except Exception as e:
            logger.error(f"Erro ao criar proposta: {e}")
            raise
    
    def activate_proposal(self, proposal_id: str) -> bool:
        """Ativa uma proposta para votação"""
        try:
            if proposal_id not in self.proposals:
                raise ValueError("Proposta não encontrada")
            
            proposal = self.proposals[proposal_id]
            
            if proposal.status != ProposalStatus.DRAFT:
                raise ValueError("Proposta já foi ativada")
            
            if self._get_current_block() < proposal.start_block:
                raise ValueError("Ainda não é hora de ativar a proposta")
            
            proposal.status = ProposalStatus.ACTIVE
            
            logger.info(f"Proposta ativada: {proposal_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao ativar proposta: {e}")
            return False
    
    def cast_vote(self, voter: str, proposal_id: str, vote_type: VoteType,
                  reason: Optional[str] = None) -> Vote:
        """Vota em uma proposta"""
        try:
            if proposal_id not in self.proposals:
                raise ValueError("Proposta não encontrada")
            
            proposal = self.proposals[proposal_id]
            
            if proposal.status != ProposalStatus.ACTIVE:
                raise ValueError("Proposta não está ativa para votação")
            
            if self._get_current_block() > proposal.end_block:
                raise ValueError("Período de votação expirado")
            
            # Verificar se já votou
            existing_votes = self.votes.get(proposal_id, [])
            for vote in existing_votes:
                if vote.voter == voter:
                    raise ValueError("Usuário já votou nesta proposta")
            
            # Calcular peso do voto
            vote_weight = self._calculate_vote_weight(voter)
            
            if vote_weight <= 0:
                raise ValueError("Usuário não tem direito de voto")
            
            # Criar voto
            vote = Vote(
                voter=voter,
                proposal_id=proposal_id,
                vote_type=vote_type,
                weight=vote_weight,
                timestamp=time.time(),
                reason=reason
            )
            
            self.votes[proposal_id].append(vote)
            
            # Atualizar contadores
            if vote_type == VoteType.FOR:
                proposal.for_votes += vote_weight
            elif vote_type == VoteType.AGAINST:
                proposal.against_votes += vote_weight
            elif vote_type == VoteType.ABSTAIN:
                proposal.abstain_votes += vote_weight
            
            logger.info(f"Voto registrado: {voter} votou {vote_type.value} em {proposal_id}")
            return vote
            
        except Exception as e:
            logger.error(f"Erro ao votar: {e}")
            raise
    
    def execute_proposal(self, proposal_id: str, executor: str) -> Dict[str, Any]:
        """Executa uma proposta aprovada"""
        try:
            if proposal_id not in self.proposals:
                raise ValueError("Proposta não encontrada")
            
            proposal = self.proposals[proposal_id]
            
            if proposal.status != ProposalStatus.SUCCEEDED:
                raise ValueError("Proposta não foi aprovada")
            
            if self._get_current_block() < proposal.end_block + self.parameters["execution_delay"]:
                raise ValueError("Ainda não é hora de executar a proposta")
            
            # Executar ações da proposta
            execution_results = []
            
            for i, (target, value, calldata) in enumerate(zip(proposal.targets, proposal.values, proposal.calldatas)):
                result = self._execute_call(target, value, calldata)
                execution_results.append({
                    "target": target,
                    "value": value,
                    "success": result["success"],
                    "data": result.get("data")
                })
            
            # Marcar como executada
            proposal.status = ProposalStatus.EXECUTED
            proposal.executed_at = time.time()
            
            logger.info(f"Proposta executada: {proposal_id}")
            
            return {
                "success": True,
                "proposal_id": proposal_id,
                "executed_at": proposal.executed_at,
                "results": execution_results
            }
            
        except Exception as e:
            logger.error(f"Erro ao executar proposta: {e}")
            raise
    
    def delegate_votes(self, delegator: str, delegatee: str) -> Delegation:
        """Delega votos para outro usuário"""
        try:
            if delegator == delegatee:
                raise ValueError("Não é possível delegar para si mesmo")
            
            # Verificar se o delegator tem tokens
            if not self._has_sufficient_tokens(delegator):
                raise ValueError("Delegator não tem tokens suficientes")
            
            delegation = Delegation(
                delegator=delegator,
                delegatee=delegatee,
                delegated_at=time.time()
            )
            
            delegation_key = f"{delegator}:{delegatee}"
            self.delegations[delegation_key] = delegation
            
            logger.info(f"Votos delegados: {delegator} -> {delegatee}")
            return delegation
            
        except Exception as e:
            logger.error(f"Erro ao delegar votos: {e}")
            raise
    
    def get_proposal_state(self, proposal_id: str) -> Dict[str, Any]:
        """Obtém estado de uma proposta"""
        if proposal_id not in self.proposals:
            raise ValueError("Proposta não encontrada")
        
        proposal = self.proposals[proposal_id]
        votes = self.votes.get(proposal_id, [])
        
        return {
            "proposal": {
                "id": proposal.proposal_id,
                "title": proposal.title,
                "description": proposal.description,
                "type": proposal.proposal_type.value,
                "status": proposal.status.value,
                "proposer": proposal.proposer,
                "start_block": proposal.start_block,
                "end_block": proposal.end_block,
                "for_votes": str(proposal.for_votes),
                "against_votes": str(proposal.against_votes),
                "abstain_votes": str(proposal.abstain_votes),
                "quorum_votes": str(proposal.quorum_votes)
            },
            "votes": [
                {
                    "voter": vote.voter,
                    "vote_type": vote.vote_type.value,
                    "weight": str(vote.weight),
                    "timestamp": vote.timestamp,
                    "reason": vote.reason
                }
                for vote in votes
            ],
            "current_block": self._get_current_block(),
            "can_vote": self._can_vote(proposal),
            "can_execute": self._can_execute(proposal)
        }
    
    def get_treasury_balance(self) -> Dict[str, str]:
        """Obtém saldo do tesouro"""
        return {token: str(balance) for token, balance in self.treasury.items()}
    
    def get_governance_parameters(self) -> Dict[str, Any]:
        """Obtém parâmetros de governança"""
        return self.parameters.copy()
    
    def get_member_stats(self, member: str) -> Dict[str, Any]:
        """Obtém estatísticas de um membro"""
        token_balance = self._get_token_balance(member)
        voting_power = self._calculate_vote_weight(member)
        
        # Contar propostas criadas
        proposals_created = len([
            p for p in self.proposals.values() 
            if p.proposer == member
        ])
        
        # Contar votos dados
        votes_cast = len([
            v for votes in self.votes.values() 
            for v in votes if v.voter == member
        ])
        
        return {
            "member": member,
            "token_balance": str(token_balance),
            "voting_power": str(voting_power),
            "proposals_created": proposals_created,
            "votes_cast": votes_cast,
            "delegations_received": len([
                d for d in self.delegations.values() 
                if d.delegatee == member and d.is_active
            ])
        }
    
    def _has_sufficient_tokens(self, address: str) -> bool:
        """Verifica se tem tokens suficientes"""
        balance = self._get_token_balance(address)
        return balance >= self.parameters["proposal_threshold"]
    
    def _get_token_balance(self, address: str) -> Decimal:
        """Obtém saldo de tokens (simulado)"""
        # Simular saldo baseado no endereço
        return Decimal("500000")  # 500K tokens
    
    def _calculate_vote_weight(self, voter: str) -> Decimal:
        """Calcula peso do voto"""
        balance = self._get_token_balance(voter)
        
        # Verificar delegações recebidas
        delegated_votes = Decimal("0")
        for delegation in self.delegations.values():
            if delegation.delegatee == voter and delegation.is_active:
                delegated_votes += self._get_token_balance(delegation.delegator)
        
        return balance + delegated_votes
    
    def _get_current_block(self) -> int:
        """Obtém bloco atual (simulado)"""
        return int(time.time() / 12)  # ~12 segundos por bloco
    
    def _can_vote(self, proposal: Proposal) -> bool:
        """Verifica se pode votar"""
        current_block = self._get_current_block()
        return (proposal.status == ProposalStatus.ACTIVE and 
                current_block >= proposal.start_block and 
                current_block <= proposal.end_block)
    
    def _can_execute(self, proposal: Proposal) -> bool:
        """Verifica se pode executar"""
        current_block = self._get_current_block()
        return (proposal.status == ProposalStatus.SUCCEEDED and 
                current_block >= proposal.end_block + self.parameters["execution_delay"])
    
    def _execute_call(self, target: str, value: str, calldata: str) -> Dict[str, Any]:
        """Executa uma chamada (simulado)"""
        # Simular execução
        return {
            "success": True,
            "data": "0x" + hashlib.sha256(f"{target}{value}{calldata}".encode()).hexdigest()[:64]
        }
    
    def _generate_proposal_id(self) -> str:
        """Gera ID único para proposta"""
        data = f"proposal_{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]


# Instância global
dao_governance_manager = DAOGovernanceManager()
