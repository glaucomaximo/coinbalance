#!/usr/bin/env python
"""
Script de Configuração de Ambiente de Produção
==============================================

Este script configura o ambiente de produção do CoinBalance,
incluindo variáveis de ambiente, configurações de segurança e
validações necessárias.
"""

import os
import secrets
import string
from pathlib import Path
from typing import Dict, Any

def generate_secure_key(length: int = 64) -> str:
    """Gera uma chave segura aleatória"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_production_config() -> Dict[str, Any]:
    """Cria configuração de produção"""
    return {
        # Configurações de Segurança
        "JWT_SECRET_KEY": generate_secure_key(64),
        "COINBALANCE_MASTER_KEY": generate_secure_key(128),
        
        # Configurações do Banco de Dados
        "DATABASE_URL": "sqlite:///./coinbalance_prod.db",
        "DATABASE_POOL_SIZE": "20",
        "DATABASE_MAX_OVERFLOW": "30",
        
        # Configurações de Cache
        "REDIS_URL": "redis://localhost:6379/0",
        "CACHE_TTL": "3600",
        "CACHE_MAX_SIZE": "1000",
        
        # Configurações de Monitoramento
        "MONITORING_ENABLED": "true",
        "PERFORMANCE_MONITORING": "true",
        "SECURITY_MONITORING": "true",
        "CONSCIOUSNESS_MONITORING": "true",
        
        # Configurações de Log
        "LOG_LEVEL": "INFO",
        "LOG_FILE": "logs/coinbalance.log",
        "LOG_MAX_SIZE": "100MB",
        "LOG_BACKUP_COUNT": "5",
        
        # Configurações de API
        "API_RATE_LIMIT": "1000",
        "API_TIMEOUT": "30",
        "CORS_ORIGINS": '["https://yourdomain.com", "https://app.yourdomain.com"]',
        
        # Configurações de Web3
        "WEB3_PROVIDER_URL": "https://mainnet.infura.io/v3/your-infura-key",
        "WEB3_CHAIN_ID": "1",
        "WEB3_GAS_LIMIT": "21000",
        
        # Configurações de IA
        "AI_MODEL_PATH": "models/coinbalance-ai-v2.1.0",
        "AI_CONFIDENCE_THRESHOLD": "0.8",
        "AI_DECISION_INTERVAL": "300",
        
        # Configurações de Economia Autônoma
        "ECONOMY_AUTO_DECISIONS": "true",
        "ECONOMY_RISK_THRESHOLD": "0.7",
        "ECONOMY_GROWTH_TARGET": "0.15",
        
        # Configurações de Fractais
        "FRACTAL_AUTO_SCALING": "true",
        "FRACTAL_MIN_INSTANCES": "3",
        "FRACTAL_MAX_INSTANCES": "10",
        "FRACTAL_SCALE_THRESHOLD": "0.8",
        
        # Configurações de Notificações
        "NOTIFICATION_EMAIL": "support@yourdomain.com",
        "NOTIFICATION_WEBHOOK": "https://yourdomain.com/webhooks/alerts",
        "NOTIFICATION_SLACK_WEBHOOK": "https://hooks.slack.com/services/your/slack/webhook",
        
        # Configurações de Backup
        "BACKUP_ENABLED": "true",
        "BACKUP_INTERVAL": "3600",
        "BACKUP_RETENTION_DAYS": "30",
        "BACKUP_S3_BUCKET": "coinbalance-backups",
        
        # Configurações de Métricas
        "METRICS_ENABLED": "true",
        "METRICS_EXPORT_INTERVAL": "60",
        "METRICS_PROMETHEUS_PORT": "9090",
        
        # Configurações de Desenvolvimento (desabilitar em produção)
        "DEBUG": "false",
        "RELOAD": "false",
        "DEVELOPMENT_MODE": "false"
    }

def create_env_file(config: Dict[str, Any], filename: str = ".env.production"):
    """Cria arquivo de ambiente"""
    env_content = "# CoinBalance - Configuração de Produção\n"
    env_content += "# =====================================\n\n"
    
    for key, value in config.items():
        env_content += f"{key}={value}\n"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"✅ Arquivo {filename} criado com sucesso!")

def create_directories():
    """Cria diretórios necessários"""
    directories = [
        "logs",
        "models",
        "backups",
        "data",
        "config"
    ]
    
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
            print(f"✅ Diretório {directory}/ criado")
        except FileExistsError:
            print(f"✅ Diretório {directory}/ já existe")

def validate_config(config: Dict[str, Any]) -> bool:
    """Valida configuração"""
    required_keys = [
        "JWT_SECRET_KEY",
        "COINBALANCE_MASTER_KEY",
        "DATABASE_URL"
    ]
    
    for key in required_keys:
        if key not in config:
            print(f"❌ Chave obrigatória ausente: {key}")
            return False
    
    print("✅ Configuração validada com sucesso!")
    return True

def main():
    """Função principal"""
    print("🚀 Configurando ambiente de produção do CoinBalance...")
    print("=" * 60)
    
    # Criar diretórios
    create_directories()
    
    # Criar configuração
    config = create_production_config()
    
    # Validar configuração
    if not validate_config(config):
        print("❌ Falha na validação da configuração")
        return
    
    # Criar arquivo de ambiente
    create_env_file(config)
    
    print("\n" + "=" * 60)
    print("✅ Configuração de produção concluída!")
    print("\n📋 Próximos passos:")
    print("1. Edite o arquivo .env.production com suas configurações específicas")
    print("2. Configure suas chaves de API (Infura, Slack, etc.)")
    print("3. Ajuste as URLs de domínio para produção")
    print("4. Execute: python main.py --env production")

if __name__ == "__main__":
    main()
