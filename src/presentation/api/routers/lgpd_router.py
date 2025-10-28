"""
Router para Conformidade com LGPD (Lei Geral de Proteção de Dados)
================================================================

Este router implementa todos os endpoints necessários para conformidade
com a Lei Geral de Proteção de Dados brasileira (Lei nº 13.709/2018).

Funcionalidades:
- Direitos dos titulares de dados
- Solicitações de acesso, retificação, exclusão
- Portabilidade de dados
- Oposição ao tratamento
- Auditoria de conformidade
"""

import logging
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from datetime import datetime

from src.infrastructure.security.auth_manager import auth_manager
from src.infrastructure.security.auth import (
    get_current_user, AuthenticatedUser, require_scope
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/lgpd", tags=["Conformidade LGPD"])

# ========== SCHEMAS ==========

class LGPDDataSubjectRequest(BaseModel):
    """Solicitação de titular de dados conforme LGPD"""
    request_type: str = Field(..., description="Tipo de solicitação: access, rectification, deletion, portability, opposition")
    details: Dict[str, Any] = Field(default_factory=dict, description="Detalhes específicos da solicitação")
    legal_basis: Optional[str] = Field(None, description="Base legal para oposição (se aplicável)")
    opposition_reason: Optional[str] = Field(None, description="Motivo da oposição (se aplicável)")

class LGPDDataAccessRequest(BaseModel):
    """Solicitação específica de acesso aos dados"""
    data_categories: Optional[List[str]] = Field(None, description="Categorias de dados solicitadas")
    include_processing_purposes: bool = Field(True, description="Incluir finalidades de tratamento")
    include_retention_period: bool = Field(True, description="Incluir prazo de retenção")

class LGPDDataRectificationRequest(BaseModel):
    """Solicitação específica de retificação dos dados"""
    fields_to_update: Dict[str, Any] = Field(..., description="Campos a serem corrigidos")
    verification_required: bool = Field(True, description="Verificação de identidade necessária")

class LGPDDataDeletionRequest(BaseModel):
    """Solicitação específica de exclusão dos dados"""
    legal_obligations: Optional[List[str]] = Field(None, description="Obrigações legais que impedem exclusão")
    anonymization_preferred: bool = Field(True, description="Prefere anonimização ao invés de exclusão completa")

class LGPDDataPortabilityRequest(BaseModel):
    """Solicitação específica de portabilidade dos dados"""
    export_format: str = Field(default="JSON", description="Formato de exportação: JSON, CSV, XML")
    include_metadata: bool = Field(True, description="Incluir metadados de tratamento")

class LGPDComplianceReport(BaseModel):
    """Relatório de conformidade LGPD"""
    user_id: str
    compliance_score: float
    violations: List[str]
    recommendations: List[str]
    last_audit: datetime
    next_audit_due: datetime

class LGPDResponse(BaseModel):
    """Resposta padrão para solicitações LGPD"""
    success: bool
    request_id: str
    message: str
    data: Optional[Dict[str, Any]] = None
    compliance_status: str = "compliant"
    processing_time_days: int = 15

# ========== ENDPOINTS ==========

@router.post("/data-subject-request", response_model=LGPDResponse)
async def handle_data_subject_request(
    request: LGPDDataSubjectRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Processa solicitações de titulares de dados conforme LGPD.
    
    Tipos de solicitação suportados:
    - access: Acesso aos dados pessoais (art. 9º)
    - rectification: Retificação de dados (art. 9º)
    - deletion: Exclusão de dados (art. 16)
    - portability: Portabilidade de dados (art. 18)
    - opposition: Oposição ao tratamento (art. 18)
    """
    try:
        logger.info(f"Solicitação LGPD {request.request_type} recebida de: {current_user.username}")
        
        # Processar solicitação usando o AuthManager
        result = auth_manager.handle_lgpd_data_subject_request(
            user_id=current_user.id,
            request_type=request.request_type,
            details=request.details
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        return LGPDResponse(
            success=result["success"],
            request_id=result["request_id"],
            message=result["message"],
            data=result.get("data"),
            compliance_status="compliant"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar solicitação LGPD: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/access-data", response_model=LGPDResponse)
async def request_data_access(
    request: LGPDDataAccessRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Solicita acesso aos dados pessoais conforme art. 9º da LGPD.
    
    O titular tem direito de obter informações sobre:
    - Confirmação da existência de tratamento
    - Acesso aos dados pessoais
    - Informações sobre tratamento
    - Finalidades do tratamento
    - Prazo de retenção
    """
    try:
        logger.info(f"Solicitação de acesso aos dados de: {current_user.username}")
        
        details = {
            "data_categories": request.data_categories,
            "include_processing_purposes": request.include_processing_purposes,
            "include_retention_period": request.include_retention_period,
            "legal_basis": "consent"  # Assumir consentimento para acesso
        }
        
        result = auth_manager.handle_lgpd_data_subject_request(
            user_id=current_user.id,
            request_type="access",
            details=details
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        return LGPDResponse(
            success=result["success"],
            request_id=result["request_id"],
            message=result["message"],
            data=result.get("data"),
            compliance_status="compliant"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar solicitação de acesso: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/rectify-data", response_model=LGPDResponse)
async def request_data_rectification(
    request: LGPDDataRectificationRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Solicita retificação de dados pessoais conforme art. 9º da LGPD.
    
    O titular tem direito de obter a correção de dados:
    - Incompletos
    - Inexatos
    - Desatualizados
    """
    try:
        logger.info(f"Solicitação de retificação de dados de: {current_user.username}")
        
        details = {
            "fields_to_update": request.fields_to_update,
            "verification_required": request.verification_required,
            "legal_basis": "consent"
        }
        
        result = auth_manager.handle_lgpd_data_subject_request(
            user_id=current_user.id,
            request_type="rectification",
            details=details
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        return LGPDResponse(
            success=result["success"],
            request_id=result["request_id"],
            message=result["message"],
            data=result.get("data"),
            compliance_status="compliant"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar solicitação de retificação: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/delete-data", response_model=LGPDResponse)
async def request_data_deletion(
    request: LGPDDataDeletionRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Solicita exclusão de dados pessoais conforme art. 16 da LGPD.
    
    O titular tem direito de obter a exclusão de dados:
    - Desnecessários
    - Excessivos
    - Tratados em desconformidade com a LGPD
    - Quando revogado o consentimento
    """
    try:
        logger.info(f"Solicitação de exclusão de dados de: {current_user.username}")
        
        details = {
            "legal_obligations": request.legal_obligations,
            "anonymization_preferred": request.anonymization_preferred,
            "legal_basis": "consent"
        }
        
        result = auth_manager.handle_lgpd_data_subject_request(
            user_id=current_user.id,
            request_type="deletion",
            details=details
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        return LGPDResponse(
            success=result["success"],
            request_id=result["request_id"],
            message=result["message"],
            data=result.get("data"),
            compliance_status="compliant"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar solicitação de exclusão: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/portability", response_model=LGPDResponse)
async def request_data_portability(
    request: LGPDDataPortabilityRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Solicita portabilidade de dados conforme art. 18 da LGPD.
    
    O titular tem direito de obter a portabilidade de dados:
    - Dados pessoais fornecidos pelo titular
    - Em formato estruturado e de uso comum
    - Para outro fornecedor de serviço
    """
    try:
        logger.info(f"Solicitação de portabilidade de dados de: {current_user.username}")
        
        details = {
            "export_format": request.export_format,
            "include_metadata": request.include_metadata,
            "legal_basis": "consent"
        }
        
        result = auth_manager.handle_lgpd_data_subject_request(
            user_id=current_user.id,
            request_type="portability",
            details=details
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        return LGPDResponse(
            success=result["success"],
            request_id=result["request_id"],
            message=result["message"],
            data=result.get("data"),
            compliance_status="compliant"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar solicitação de portabilidade: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/oppose-treatment", response_model=LGPDResponse)
async def oppose_data_treatment(
    request: LGPDDataSubjectRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Solicita oposição ao tratamento de dados conforme art. 18 da LGPD.
    
    O titular tem direito de se opor ao tratamento quando:
    - Baseado em legítimo interesse
    - Para fins de marketing direto
    - Para fins de pesquisa científica
    """
    try:
        logger.info(f"Solicitação de oposição ao tratamento de: {current_user.username}")
        
        details = {
            "legal_basis": request.legal_basis,
            "opposition_reason": request.opposition_reason,
            **request.details
        }
        
        result = auth_manager.handle_lgpd_data_subject_request(
            user_id=current_user.id,
            request_type="opposition",
            details=details
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        return LGPDResponse(
            success=result["success"],
            request_id=result["request_id"],
            message=result["message"],
            data=result.get("data"),
            compliance_status="compliant"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar solicitação de oposição: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/compliance-status", response_model=LGPDComplianceReport)
async def get_compliance_status(
    current_user: AuthenticatedUser = Depends(require_scope("audit:logs"))
):
    """
    Obtém status de conformidade LGPD do usuário.
    
    Retorna informações sobre:
    - Score de conformidade
    - Violações detectadas
    - Recomendações de melhoria
    - Próxima auditoria
    """
    try:
        logger.info(f"Verificando status de conformidade LGPD de: {current_user.username}")
        
        # Obter logs de auditoria LGPD
        audit_logs = auth_manager.get_audit_logs(
            limit=100,
            user_id=current_user.id
        )
        
        # Filtrar logs LGPD
        lgpd_logs = [
            log for log in audit_logs 
            if "lgpd" in log.get("action", "").lower()
        ]
        
        # Calcular score de conformidade
        total_logs = len(lgpd_logs)
        compliant_logs = len([
            log for log in lgpd_logs 
            if log.get("success", False)
        ])
        
        compliance_score = (compliant_logs / total_logs * 100) if total_logs > 0 else 100
        
        # Identificar violações
        violations = []
        for log in lgpd_logs:
            details = log.get("details", {})
            if details.get("compliance_violations"):
                violations.extend(details["compliance_violations"])
        
        # Gerar recomendações
        recommendations = []
        if compliance_score < 90:
            recommendations.append("Revisar políticas de tratamento de dados pessoais")
        if violations:
            recommendations.append("Implementar controles adicionais de conformidade")
        if not lgpd_logs:
            recommendations.append("Realizar auditoria inicial de conformidade LGPD")
        
        return LGPDComplianceReport(
            user_id=current_user.id,
            compliance_score=compliance_score,
            violations=list(set(violations)),  # Remover duplicatas
            recommendations=recommendations,
            last_audit=datetime.fromtimestamp(lgpd_logs[-1]["timestamp"]) if lgpd_logs else datetime.now(),
            next_audit_due=datetime.now()  # Simplificado para exemplo
        )
        
    except Exception as e:
        logger.error(f"Erro ao obter status de conformidade: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/privacy-policy")
async def get_privacy_policy():
    """
    Retorna a política de privacidade conforme LGPD.
    
    Inclui informações sobre:
    - Finalidades do tratamento
    - Base legal
    - Prazo de retenção
    - Direitos dos titulares
    - Contato do controlador
    """
    return {
        "title": "Política de Privacidade - CoinBalance",
        "version": "1.0",
        "last_updated": "2024-12-19",
        "controller": {
            "name": "CoinBalance",
            "contact": "privacy@coinbalance.com",
            "dpo": "dpo@coinbalance.com"
        },
        "data_processing": {
            "purposes": [
                "Autenticação e autorização de usuários",
                "Prestação de serviços de carteira digital",
                "Processamento de transações blockchain",
                "Segurança e prevenção de fraudes",
                "Cumprimento de obrigações legais"
            ],
            "legal_basis": [
                "Consentimento do titular",
                "Execução de contrato",
                "Obrigação legal",
                "Interesse legítimo"
            ],
            "data_categories": [
                "Dados de identificação",
                "Dados de contato",
                "Dados de transação",
                "Dados de uso do serviço"
            ],
            "retention_period": "5 anos após término do relacionamento"
        },
        "data_subject_rights": [
            "Confirmação e acesso aos dados",
            "Correção de dados incompletos ou inexatos",
            "Anonimização, bloqueio ou eliminação",
            "Portabilidade dos dados",
            "Eliminação dos dados tratados com consentimento",
            "Informação sobre compartilhamento",
            "Informação sobre possibilidade de não fornecer consentimento"
        ],
        "data_sharing": {
            "third_parties": "Não compartilhamos dados pessoais com terceiros",
            "international_transfer": "Não realizamos transferência internacional de dados",
            "law_enforcement": "Compartilhamento apenas quando exigido por lei"
        },
        "security_measures": [
            "Criptografia de dados em trânsito e em repouso",
            "Controle de acesso baseado em roles",
            "Auditoria e logging de atividades",
            "Backup e recuperação de dados",
            "Monitoramento de segurança 24/7"
        ],
        "contact": {
            "dpo": "dpo@coinbalance.com",
            "privacy": "privacy@coinbalance.com",
            "phone": "+55 11 99999-9999",
            "address": "São Paulo, SP, Brasil"
        }
    }

@router.get("/data-processing-record")
async def get_data_processing_record(
    current_user: AuthenticatedUser = Depends(require_scope("audit:logs"))
):
    """
    Retorna o registro de atividades de tratamento conforme art. 50 da LGPD.
    
    Inclui informações sobre:
    - Finalidades do tratamento
    - Categorias de dados
    - Categorias de titulares
    - Destinatários
    - Transferências internacionais
    - Medidas de segurança
    """
    try:
        logger.info(f"Gerando registro de atividades de tratamento para: {current_user.username}")
        
        # Obter logs de auditoria relacionados a dados pessoais
        audit_logs = auth_manager.get_audit_logs(
            limit=1000,
            user_id=current_user.id
        )
        
        # Processar logs para gerar registro
        processing_activities = []
        for log in audit_logs:
            if any(keyword in log.get("action", "").lower() for keyword in ["data", "personal", "user", "profile"]):
                processing_activities.append({
                    "timestamp": log["timestamp"],
                    "activity": log["action"],
                    "purpose": log.get("details", {}).get("data_purpose", "Not specified"),
                    "legal_basis": log.get("details", {}).get("legal_basis", "Not specified"),
                    "success": log.get("success", False)
                })
        
        return {
            "record_id": f"DPR_{current_user.id}_{int(datetime.now().timestamp())}",
            "generated_at": datetime.now().isoformat(),
            "controller": "CoinBalance",
            "data_protection_officer": "dpo@coinbalance.com",
            "processing_activities": processing_activities,
            "data_categories": [
                "Dados de identificação pessoal",
                "Dados de contato",
                "Dados de transação financeira",
                "Dados de uso do serviço"
            ],
            "data_subjects": [
                "Usuários da plataforma",
                "Titulares de carteiras digitais",
                "Participantes de transações"
            ],
            "recipients": [
                "Usuários autorizados",
                "Sistemas de auditoria",
                "Autoridades competentes (quando exigido)"
            ],
            "international_transfers": "Não aplicável",
            "security_measures": [
                "Criptografia AES-256",
                "Controle de acesso RBAC",
                "Auditoria completa",
                "Backup criptografado"
            ],
            "retention_periods": {
                "user_data": "5 anos",
                "transaction_data": "10 anos",
                "audit_logs": "7 anos"
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar registro de atividades: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
