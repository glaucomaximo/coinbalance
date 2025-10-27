"""
Configuração do Framework Coinbalance
Centraliza todas as configurações da plataforma
"""

import os
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class ConfigCoinbalance:
    """Configuração principal do Coinbalance"""
    
    # Identidade da plataforma
    nome: str = "Coinbalance"
    descricao: str = "A Economia da Consciência"
    versao: str = "2.1.0"
    moeda: str = "CNB"
    sigla: str = "CNB"
    
    # URLs e contatos
    website: str = "https://coinbalance.com.br"
    email_suporte: str = "support@coinbalance.com.br"
    email_investimentos: str = "investimentos@coinbalance.com.br"
    discord: str = "https://discord.gg/coinbalance"
    
    # Configurações de rede
    porta_padrao: int = 8000
    host_padrao: str = "0.0.0.0"
    
    # Configurações de banco de dados
    database_url: str = "sqlite:///data/coinbalance.db"
    redis_url: str = "redis://localhost:6379"
    
    # Configurações da moeda CNB
    supply_maximo: int = 100_000_000  # 100 milhões de CNB
    recompensa_bloco_inicial: float = 50.0
    taxa_transacao_base: float = 0.001
    taxa_queima: float = 0.1  # 10% das taxas são queimadas
    
    # Configurações de transações fracionadas
    precisao_decimal: int = 8  # 8 casas decimais
    valor_minimo: float = 0.00000001  # 1 satoshi
    valor_maximo: float = 100_000_000  # 100M CNB
    taxa_minima: float = 0.00000001  # 1 satoshi
    conversao_cnb_satoshi: int = 100_000_000  # 1 CNB = 100M sat
    conversao_cnb_mcnb: int = 1_000_000  # 1 CNB = 1M mCNB
    
    # Configurações de DeFi
    staking_apy: float = 0.12  # 12% APY
    lending_rate: float = 0.05  # 5% taxa de empréstimo
    yield_farming_rate: float = 0.08  # 8% yield farming
    
    # Configurações de governança
    quorum_minimo: float = 0.1  # 10% do supply
    maioria_necessaria: float = 0.51  # 51%
    tempo_votacao: int = 7 * 24 * 3600  # 7 dias em segundos
    
    # Configurações de IA Simbólica
    peso_material: float = 0.2
    peso_emocional: float = 0.2
    peso_mental: float = 0.2
    peso_espiritual: float = 0.2
    peso_transcendental: float = 0.2
    
    # Configurações de neuroeconomia
    nivel_medo_maximo: float = 0.5
    nivel_ganancia_maximo: float = 0.5
    score_racionalidade_minimo: float = 0.6
    
    # Configurações de segurança
    chave_secreta: str = os.getenv("SECRET_KEY", "coinbalance_secret_key_2025")
    jwt_secret: str = os.getenv("JWT_SECRET", "coinbalance_jwt_secret_2025")
    tempo_expiracao_token: int = 24 * 3600  # 24 horas
    
    # Configurações de monitoramento
    log_level: str = os.getenv("LOG_LEVEL", "info")
    metrics_enabled: bool = True
    prometheus_port: int = 9090
    grafana_port: int = 3000
    
    # Configurações de cache
    cache_ttl: int = 3600  # 1 hora
    cache_max_size: int = 1000
    
    # Configurações de backup
    backup_intervalo: int = 24 * 3600  # 24 horas
    backup_retention: int = 30  # 30 dias
    backup_path: str = "./backups"
    
    # Configurações de desenvolvimento
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    reload: bool = os.getenv("RELOAD", "false").lower() == "true"
    workers: int = int(os.getenv("WORKERS", "1"))
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte configuração para dicionário"""
        return {
            "identidade": {
                "nome": self.nome,
                "descricao": self.descricao,
                "versao": self.versao,
                "moeda": self.moeda,
                "sigla": self.sigla
            },
            "contatos": {
                "website": self.website,
                "email_suporte": self.email_suporte,
                "email_investimentos": self.email_investimentos,
                "discord": self.discord
            },
            "rede": {
                "porta": self.porta_padrao,
                "host": self.host_padrao
            },
            "banco_dados": {
                "database_url": self.database_url,
                "redis_url": self.redis_url
            },
            "moeda_cnb": {
                "supply_maximo": self.supply_maximo,
                "recompensa_bloco_inicial": self.recompensa_bloco_inicial,
                "taxa_transacao_base": self.taxa_transacao_base,
                "taxa_queima": self.taxa_queima
            },
            "defi": {
                "staking_apy": self.staking_apy,
                "lending_rate": self.lending_rate,
                "yield_farming_rate": self.yield_farming_rate
            },
            "governanca": {
                "quorum_minimo": self.quorum_minimo,
                "maioria_necessaria": self.maioria_necessaria,
                "tempo_votacao": self.tempo_votacao
            },
            "ia_simbolica": {
                "peso_material": self.peso_material,
                "peso_emocional": self.peso_emocional,
                "peso_mental": self.peso_mental,
                "peso_espiritual": self.peso_espiritual,
                "peso_transcendental": self.peso_transcendental
            },
            "neuroeconomia": {
                "nivel_medo_maximo": self.nivel_medo_maximo,
                "nivel_ganancia_maximo": self.nivel_ganancia_maximo,
                "score_racionalidade_minimo": self.score_racionalidade_minimo
            },
            "seguranca": {
                "chave_secreta": self.chave_secreta[:10] + "...",  # Ocultar chave
                "jwt_secret": self.jwt_secret[:10] + "...",  # Ocultar chave
                "tempo_expiracao_token": self.tempo_expiracao_token
            },
            "monitoramento": {
                "log_level": self.log_level,
                "metrics_enabled": self.metrics_enabled,
                "prometheus_port": self.prometheus_port,
                "grafana_port": self.grafana_port
            },
            "cache": {
                "cache_ttl": self.cache_ttl,
                "cache_max_size": self.cache_max_size
            },
            "backup": {
                "backup_intervalo": self.backup_intervalo,
                "backup_retention": self.backup_retention,
                "backup_path": self.backup_path
            },
            "desenvolvimento": {
                "debug": self.debug,
                "reload": self.reload,
                "workers": self.workers
            }
        }
    
    def validar_configuracao(self) -> bool:
        """Valida se a configuração está correta"""
        erros = []
        
        # Validar supply máximo
        if self.supply_maximo <= 0:
            erros.append("Supply máximo deve ser maior que zero")
        
        # Validar taxas
        if not 0 <= self.taxa_transacao_base <= 1:
            erros.append("Taxa de transação deve estar entre 0 e 1")
        
        if not 0 <= self.taxa_queima <= 1:
            erros.append("Taxa de queima deve estar entre 0 e 1")
        
        # Validar pesos de consciência
        pesos = [
            self.peso_material,
            self.peso_emocional,
            self.peso_mental,
            self.peso_espiritual,
            self.peso_transcendental
        ]
        
        if abs(sum(pesos) - 1.0) > 0.01:
            erros.append("Soma dos pesos de consciência deve ser 1.0")
        
        # Validar configurações de governança
        if not 0 <= self.quorum_minimo <= 1:
            erros.append("Quorum mínimo deve estar entre 0 e 1")
        
        if not 0 <= self.maioria_necessaria <= 1:
            erros.append("Maioria necessária deve estar entre 0 e 1")
        
        if erros:
            print("❌ Erros de configuração encontrados:")
            for erro in erros:
                print(f"  - {erro}")
            return False
        
        print("✅ Configuração validada com sucesso!")
        return True


# Instância global da configuração
config = ConfigCoinbalance()


def obter_configuracao() -> ConfigCoinbalance:
    """Obtém a configuração atual do Coinbalance"""
    return config


def atualizar_configuracao(nova_config: Dict[str, Any]) -> bool:
    """Atualiza configuração com novos valores"""
    try:
        # Atualizar valores da configuração
        for secao, valores in nova_config.items():
            for chave, valor in valores.items():
                if hasattr(config, chave):
                    setattr(config, chave, valor)
        
        # Validar nova configuração
        return config.validar_configuracao()
    
    except Exception as e:
        print(f"❌ Erro ao atualizar configuração: {e}")
        return False


def obter_info_plataforma() -> Dict[str, Any]:
    """Obtém informações da plataforma"""
    return {
        "nome": config.nome,
        "descricao": config.descricao,
        "versao": config.versao,
        "moeda": config.moeda,
        "sigla": config.sigla,
        "website": config.website,
        "framework": "Coinbalance",
        "slogan": "A Economia da Consciência"
    }


if __name__ == "__main__":
    # Testar configuração
    print("🪙 Configuração do Coinbalance")
    print("=" * 40)
    
    # Validar configuração
    if config.validar_configuracao():
        print("✅ Configuração válida!")
        
        # Mostrar informações da plataforma
        info = obter_info_plataforma()
        print(f"\n📊 Informações da Plataforma:")
        for chave, valor in info.items():
            print(f"  {chave}: {valor}")
        
        # Mostrar configuração completa
        print(f"\n⚙️ Configuração Completa:")
        config_dict = config.to_dict()
        for secao, valores in config_dict.items():
            print(f"\n{secao.upper()}:")
            for chave, valor in valores.items():
                print(f"  {chave}: {valor}")
    else:
        print("❌ Configuração inválida!")