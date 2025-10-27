"""
Configurações centralizadas seguindo 12-Factor App
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from pathlib import Path


class Settings(BaseSettings):
    """
    Configurações centralizadas da aplicação.

    Segue os princípios do 12-Factor App:
    - Config armazenada no ambiente
    - Separação estrita de config por ambiente
    - Sem hardcoding de valores
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    # ========== APP ==========
    APP_NAME: str = "CoinBalance"
    APP_VERSION: str = "2.1.0"
    APP_DESCRIPTION: str = (
        "A Economia da Consciência - Blockchain com DeFi e Governança"
    )
    ENVIRONMENT: str = "development"  # development, staging, production
    DEBUG: bool = False

    # ========== API ==========
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 1
    API_RELOAD: bool = True
    API_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000", "http://localhost:8001"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # ========== DATABASE ==========
    DATABASE_URL: str = "sqlite:///blockchain.db"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # ========== SECURITY ==========
    SECRET_KEY: str = "dev-secret-key-change-in-production-32-chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Crypto
    ENCRYPTION_KEY: Optional[str] = "dev-encryption-key-32-chars-long"
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_DIGITS: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True

    # ========== RATE LIMITING ==========
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # segundos
    RATE_LIMIT_BURST: int = 20

    # Rate limiting por endpoint
    RATE_LIMIT_WALLET_CREATE: int = 5
    RATE_LIMIT_TRANSACTION_CREATE: int = 50
    RATE_LIMIT_MINING: int = 10

    # ========== BLOCKCHAIN ==========
    MINING_DIFFICULTY: int = 4  # Número de zeros no início do hash
    BLOCK_REWARD: float = 50.0
    HALVING_INTERVAL: int = 210000  # Blocos
    MAX_TRANSACTIONS_PER_BLOCK: int = 1000
    MIN_TRANSACTION_FEE: float = 0.00000001  # 1 satoshi

    # Consensus
    CONSENSUS_ALGORITHM: str = "proof_of_work"  # proof_of_work, proof_of_stake
    BLOCK_TIME_TARGET: int = 600  # 10 minutos em segundos

    # ========== TOKENOMICS ==========
    TOTAL_SUPPLY: float = 21000000.0  # CNB
    INITIAL_SUPPLY: float = 0.0
    STAKING_ENABLED: bool = True
    STAKING_MIN_AMOUNT: float = 100.0
    STAKING_ANNUAL_RATE: float = 0.05  # 5%
    LENDING_ENABLED: bool = True
    LENDING_MAX_LTV: float = 0.75  # 75% Loan-to-Value

    # ========== MONITORING ==========
    ENABLE_METRICS: bool = True
    ENABLE_HEALTH_CHECKS: bool = True
    ENABLE_TRACING: bool = False

    # Logging
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FORMAT: str = "json"  # json, text
    LOG_FILE: Optional[str] = "logs/coinbalance.log"
    LOG_MAX_SIZE: int = 10485760  # 10 MB
    LOG_BACKUP_COUNT: int = 5

    # Metrics
    METRICS_PORT: int = 9090
    METRICS_PATH: str = "/metrics"

    # ========== CACHE ==========
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 300  # 5 minutos
    CACHE_MAX_SIZE: int = 1000

    # Redis (opcional)
    REDIS_ENABLED: bool = False
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    # ========== EXTERNAL SERVICES ==========
    # Email
    EMAIL_ENABLED: bool = False
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: Optional[str] = None

    # Notifications
    NOTIFICATION_ENABLED: bool = False
    WEBHOOK_URL: Optional[str] = None

    # ========== TESTING ==========
    TESTING: bool = False
    TEST_DATABASE_URL: str = "sqlite:///:memory:"

    # ========== FEATURES FLAGS ==========
    FEATURE_DEFI: bool = True
    FEATURE_GOVERNANCE: bool = True
    FEATURE_NFT: bool = False
    FEATURE_SMART_CONTRACTS: bool = True

    # ========== PATHS ==========
    @property
    def base_dir(self) -> Path:
        """Diretório base do projeto"""
        return Path(__file__).parent.parent.parent.parent

    @property
    def logs_dir(self) -> Path:
        """Diretório de logs"""
        return self.base_dir / "logs"

    @property
    def data_dir(self) -> Path:
        """Diretório de dados"""
        return self.base_dir / "data"

    # ========== COMPUTED PROPERTIES ==========
    @property
    def is_development(self) -> bool:
        """Verifica se está em desenvolvimento"""
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        """Verifica se está em produção"""
        return self.ENVIRONMENT == "production"

    @property
    def is_staging(self) -> bool:
        """Verifica se está em staging"""
        return self.ENVIRONMENT == "staging"

    @property
    def docs_enabled(self) -> bool:
        """Verifica se documentação deve estar habilitada"""
        return not self.is_production

    # ========== VALIDATION ==========
    def model_post_init(self, __context) -> None:
        """Validações pós-inicialização"""
        # Criar diretórios necessários
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Validar configurações críticas em produção
        if self.is_production:
            if self.SECRET_KEY == "dev-secret-key-change-in-production":
                raise ValueError("SECRET_KEY must be changed in production!")

            if self.DEBUG:
                raise ValueError("DEBUG must be False in production!")

            if "*" in self.CORS_ORIGINS:
                raise ValueError("CORS_ORIGINS cannot be '*' in production!")

    # ========== HELPER METHODS ==========
    def get_database_url(self, for_testing: bool = False) -> str:
        """Retorna URL do banco de dados"""
        if for_testing or self.TESTING:
            return self.TEST_DATABASE_URL
        return self.DATABASE_URL

    def to_dict(self) -> dict:
        """Exporta configurações como dicionário (sem senhas)"""
        data = self.model_dump()

        # Remover informações sensíveis
        sensitive_keys = [
            "SECRET_KEY",
            "ENCRYPTION_KEY",
            "REDIS_PASSWORD",
            "SMTP_PASSWORD",
            "DATABASE_URL",
        ]

        for key in sensitive_keys:
            if key in data:
                data[key] = "***HIDDEN***"

        return data


# Instância global de configurações
settings = Settings()


# Configurações específicas por ambiente
def get_settings_for_environment(env: str) -> Settings:
    """Factory para criar Settings baseado no ambiente"""
    if env == "production":
        return Settings(
            ENVIRONMENT="production",
            DEBUG=False,
            API_RELOAD=False,
            DATABASE_ECHO=False,
            LOG_LEVEL="WARNING",
            CORS_ORIGINS=["https://coinbalance.io"],
        )
    elif env == "staging":
        return Settings(
            ENVIRONMENT="staging",
            DEBUG=False,
            API_RELOAD=False,
            LOG_LEVEL="INFO",
            CORS_ORIGINS=["https://staging.coinbalance.io"],
        )
    else:  # development
        return Settings(
            ENVIRONMENT="development",
            DEBUG=True,
            API_RELOAD=True,
            DATABASE_ECHO=True,
            LOG_LEVEL="DEBUG",
        )
