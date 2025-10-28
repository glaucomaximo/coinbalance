"""
Sistema de Configuração de Ambiente Robusto
===========================================

Gerencia configurações de ambiente com validação rigorosa,
fallbacks seguros e detecção automática de problemas.
"""

import os
import logging
from typing import Any, Dict, Optional, List, Union
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class EnvironmentType(Enum):
    """Tipos de ambiente"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

@dataclass
class ConfigValidationError(Exception):
    """Erro de validação de configuração"""
    field: str
    message: str
    current_value: Any
    required_value: Any = None

class EnvironmentConfigManager:
    """Gerenciador robusto de configuração de ambiente"""
    
    def __init__(self):
        self._config_cache: Dict[str, Any] = {}
        self._required_vars: List[str] = []
        self._sensitive_vars: List[str] = []
        self._validation_rules: Dict[str, callable] = {}
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Configura regras de validação padrão"""
        self._required_vars = [
            "SECRET_KEY",
            "JWT_SECRET_KEY", 
            "ENCRYPTION_KEY",
            "COINBALANCE_MASTER_KEY"
        ]
        
        self._sensitive_vars = [
            "SECRET_KEY",
            "JWT_SECRET_KEY",
            "ENCRYPTION_KEY", 
            "COINBALANCE_MASTER_KEY",
            "DATABASE_URL",
            "REDIS_PASSWORD",
            "SMTP_PASSWORD"
        ]
        
        self._validation_rules = {
            "SECRET_KEY": self._validate_secret_key,
            "JWT_SECRET_KEY": self._validate_jwt_secret,
            "ENCRYPTION_KEY": self._validate_encryption_key,
            "COINBALANCE_MASTER_KEY": self._validate_master_key,
            "DATABASE_URL": self._validate_database_url,
            "API_PORT": self._validate_port,
            "LOG_LEVEL": self._validate_log_level,
            "ENVIRONMENT": self._validate_environment
        }
    
    def get_environment_type(self) -> EnvironmentType:
        """Detecta o tipo de ambiente"""
        env = os.getenv("ENVIRONMENT", "development").lower()
        
        if env == "production":
            return EnvironmentType.PRODUCTION
        elif env == "staging":
            return EnvironmentType.STAGING
        elif env == "testing":
            return EnvironmentType.TESTING
        else:
            return EnvironmentType.DEVELOPMENT
    
    def get_config(self, key: str, default: Any = None, required: bool = False) -> Any:
        """Obtém configuração com validação"""
        # Verificar cache primeiro
        if key in self._config_cache:
            return self._config_cache[key]
        
        # Obter valor do ambiente
        value = os.getenv(key, default)
        
        # Validar se é obrigatório
        if required and value is None:
            raise ConfigValidationError(
                field=key,
                message=f"Variável de ambiente obrigatória não definida: {key}",
                current_value=None
            )
        
        # Aplicar validação se existir regra
        if key in self._validation_rules and value is not None:
            try:
                value = self._validation_rules[key](value)
            except Exception as e:
                raise ConfigValidationError(
                    field=key,
                    message=f"Validação falhou para {key}: {str(e)}",
                    current_value=value
                )
        
        # Cachear valor
        self._config_cache[key] = value
        
        return value
    
    def get_all_config(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Obtém todas as configurações"""
        config = {}
        
        # Obter todas as variáveis de ambiente
        for key, value in os.environ.items():
            if not include_sensitive and key in self._sensitive_vars:
                config[key] = "***HIDDEN***"
            else:
                config[key] = value
        
        return config
    
    def validate_production_config(self) -> List[ConfigValidationError]:
        """Valida configurações para produção"""
        errors = []
        
        if self.get_environment_type() != EnvironmentType.PRODUCTION:
            return errors
        
        # Verificar variáveis obrigatórias
        for var in self._required_vars:
            try:
                value = self.get_config(var, required=True)
                if not value or value == f"dev-{var.lower()}-change-in-production":
                    errors.append(ConfigValidationError(
                        field=var,
                        message=f"Variável {var} deve ser definida para produção",
                        current_value=value
                    ))
            except ConfigValidationError as e:
                errors.append(e)
        
        # Verificar configurações específicas de produção
        debug_mode = self.get_config("DEBUG", "false").lower()
        if debug_mode == "true":
            errors.append(ConfigValidationError(
                field="DEBUG",
                message="DEBUG deve ser False em produção",
                current_value=debug_mode,
                required_value="false"
            ))
        
        cors_origins = self.get_config("CORS_ORIGINS", "")
        if "*" in cors_origins:
            errors.append(ConfigValidationError(
                field="CORS_ORIGINS",
                message="CORS_ORIGINS não pode ser '*' em produção",
                current_value=cors_origins
            ))
        
        return errors
    
    def generate_env_template(self, environment: EnvironmentType) -> str:
        """Gera template de arquivo .env para ambiente específico"""
        template = f"# Configurações para {environment.value}\n\n"
        
        if environment == EnvironmentType.PRODUCTION:
            template += "# CONFIGURAÇÕES OBRIGATÓRIAS PARA PRODUÇÃO\n"
            template += "SECRET_KEY=your-super-secure-secret-key-here-minimum-32-chars\n"
            template += "JWT_SECRET_KEY=your-jwt-secret-key-here-minimum-32-chars\n"
            template += "ENCRYPTION_KEY=your-encryption-key-here-minimum-32-chars\n"
            template += "COINBALANCE_MASTER_KEY=your-master-key-here-minimum-32-chars\n\n"
            
            template += "# CONFIGURAÇÕES DE PRODUÇÃO\n"
            template += "ENVIRONMENT=production\n"
            template += "DEBUG=false\n"
            template += "LOG_LEVEL=WARNING\n"
            template += "API_RELOAD=false\n"
            template += "DATABASE_ECHO=false\n\n"
            
            template += "# BANCO DE DADOS\n"
            template += "DATABASE_URL=postgresql://user:password@localhost:5432/coinbalance\n\n"
            
            template += "# CORS\n"
            template += "CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com\n\n"
            
        elif environment == EnvironmentType.STAGING:
            template += "# CONFIGURAÇÕES PARA STAGING\n"
            template += "ENVIRONMENT=staging\n"
            template += "DEBUG=false\n"
            template += "LOG_LEVEL=INFO\n"
            template += "API_RELOAD=false\n\n"
            
        else:  # DEVELOPMENT
            template += "# CONFIGURAÇÕES PARA DESENVOLVIMENTO\n"
            template += "ENVIRONMENT=development\n"
            template += "DEBUG=true\n"
            template += "LOG_LEVEL=DEBUG\n"
            template += "API_RELOAD=true\n"
            template += "DATABASE_ECHO=true\n\n"
        
        template += "# CONFIGURAÇÕES COMUNS\n"
        template += "API_HOST=0.0.0.0\n"
        template += "API_PORT=8000\n"
        template += "API_WORKERS=1\n\n"
        
        template += "# RATE LIMITING\n"
        template += "RATE_LIMIT_ENABLED=true\n"
        template += "RATE_LIMIT_REQUESTS=100\n"
        template += "RATE_LIMIT_PERIOD=60\n\n"
        
        template += "# MONITORAMENTO\n"
        template += "ENABLE_METRICS=true\n"
        template += "ENABLE_HEALTH_CHECKS=true\n"
        template += "METRICS_PORT=9090\n\n"
        
        return template
    
    def check_environment_health(self) -> Dict[str, Any]:
        """Verifica saúde do ambiente de configuração"""
        health = {
            "environment_type": self.get_environment_type().value,
            "total_vars": len(os.environ),
            "required_vars_defined": 0,
            "validation_errors": [],
            "warnings": [],
            "recommendations": []
        }
        
        # Verificar variáveis obrigatórias
        for var in self._required_vars:
            if os.getenv(var):
                health["required_vars_defined"] += 1
            else:
                health["validation_errors"].append(f"Variável obrigatória não definida: {var}")
        
        # Verificar configurações específicas do ambiente
        env_type = self.get_environment_type()
        
        if env_type == EnvironmentType.PRODUCTION:
            prod_errors = self.validate_production_config()
            health["validation_errors"].extend([str(e) for e in prod_errors])
            
            if health["validation_errors"]:
                health["recommendations"].append("Corrija os erros de configuração antes do deploy")
        
        elif env_type == EnvironmentType.DEVELOPMENT:
            if not os.getenv("DEBUG"):
                health["warnings"].append("DEBUG não definido - usando padrão")
            
            if not os.getenv("LOG_LEVEL"):
                health["warnings"].append("LOG_LEVEL não definido - usando padrão")
        
        # Calcular score de saúde
        total_required = len(self._required_vars)
        defined_required = health["required_vars_defined"]
        health["health_score"] = (defined_required / total_required) * 100 if total_required > 0 else 100
        
        return health
    
    # ========== VALIDADORES ==========
    
    def _validate_secret_key(self, value: str) -> str:
        """Valida chave secreta"""
        if len(value) < 32:
            raise ValueError("SECRET_KEY deve ter pelo menos 32 caracteres")
        return value
    
    def _validate_jwt_secret(self, value: str) -> str:
        """Valida chave JWT"""
        if len(value) < 32:
            raise ValueError("JWT_SECRET_KEY deve ter pelo menos 32 caracteres")
        return value
    
    def _validate_encryption_key(self, value: str) -> str:
        """Valida chave de criptografia"""
        if len(value) < 32:
            raise ValueError("ENCRYPTION_KEY deve ter pelo menos 32 caracteres")
        return value
    
    def _validate_master_key(self, value: str) -> str:
        """Valida chave mestra"""
        if len(value) < 32:
            raise ValueError("COINBALANCE_MASTER_KEY deve ter pelo menos 32 caracteres")
        return value
    
    def _validate_database_url(self, value: str) -> str:
        """Valida URL do banco de dados"""
        if not value.startswith(("sqlite://", "postgresql://", "mysql://")):
            raise ValueError("DATABASE_URL deve começar com sqlite://, postgresql:// ou mysql://")
        return value
    
    def _validate_port(self, value: Union[str, int]) -> int:
        """Valida porta"""
        try:
            port = int(value)
            if not (1 <= port <= 65535):
                raise ValueError("Porta deve estar entre 1 e 65535")
            return port
        except ValueError:
            raise ValueError("Porta deve ser um número inteiro")
    
    def _validate_log_level(self, value: str) -> str:
        """Valida nível de log"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if value.upper() not in valid_levels:
            raise ValueError(f"LOG_LEVEL deve ser um dos: {', '.join(valid_levels)}")
        return value.upper()
    
    def _validate_environment(self, value: str) -> str:
        """Valida tipo de ambiente"""
        valid_envs = ["development", "staging", "production", "testing"]
        if value.lower() not in valid_envs:
            raise ValueError(f"ENVIRONMENT deve ser um dos: {', '.join(valid_envs)}")
        return value.lower()

# Instância global do gerenciador
config_manager = EnvironmentConfigManager()
