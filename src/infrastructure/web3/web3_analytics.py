"""
Web3 Analytics Dashboard para CoinBalance
Implementa analytics avançados para Web3
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
import time
import statistics
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Tipos de métricas"""
    VOLUME = "volume"
    TRANSACTIONS = "transactions"
    USERS = "users"
    FEES = "fees"
    LIQUIDITY = "liquidity"
    PRICE = "price"
    MARKET_CAP = "market_cap"


class TimeRange(Enum):
    """Intervalos de tempo"""
    HOUR = "1h"
    DAY = "24h"
    WEEK = "7d"
    MONTH = "30d"
    YEAR = "365d"


@dataclass
class MetricData:
    """Dados de métrica"""
    timestamp: float
    value: Decimal
    metadata: Dict[str, Any] = None


@dataclass
class AnalyticsReport:
    """Relatório de analytics"""
    report_id: str
    title: str
    metric_type: MetricType
    time_range: TimeRange
    data_points: List[MetricData]
    generated_at: float
    summary: Dict[str, Any] = None


@dataclass
class UserActivity:
    """Atividade do usuário"""
    user_address: str
    activity_type: str
    timestamp: float
    value: Decimal
    metadata: Dict[str, Any] = None


class Web3AnalyticsManager:
    """Gerenciador de Analytics Web3"""
    
    def __init__(self):
        self.metrics: Dict[str, List[MetricData]] = {}
        self.user_activities: List[UserActivity] = []
        self.reports: Dict[str, AnalyticsReport] = {}
        self.price_data: Dict[str, List[MetricData]] = {}
        self.volume_data: Dict[str, List[MetricData]] = {}
        self._initialize_sample_data()
        logger.info("Web3AnalyticsManager inicializado")
    
    def _initialize_sample_data(self):
        """Inicializa dados de exemplo"""
        # Gerar dados de preço simulados
        base_price = Decimal("0.50")
        for i in range(100):
            timestamp = time.time() - (i * 3600)  # Últimas 100 horas
            price_change = Decimal(str(statistics.NormalDist(0, 0.05).samples(1)[0]))
            price = base_price * (Decimal("1") + price_change)
            
            self.price_data.setdefault("CNB", []).append(
                MetricData(timestamp=timestamp, value=price)
            )
        
        # Gerar dados de volume simulados
        for i in range(100):
            timestamp = time.time() - (i * 3600)
            volume = Decimal(str(statistics.NormalDist(1000000, 200000).samples(1)[0]))
            
            self.volume_data.setdefault("CNB", []).append(
                MetricData(timestamp=timestamp, value=volume)
            )
    
    def track_transaction(self, tx_hash: str, user_address: str, amount: Decimal,
                        token: str, tx_type: str, fee: Decimal = Decimal("0")) -> None:
        """Rastreia uma transação"""
        try:
            activity = UserActivity(
                user_address=user_address,
                activity_type=tx_type,
                timestamp=time.time(),
                value=amount,
                metadata={
                    "tx_hash": tx_hash,
                    "token": token,
                    "fee": str(fee)
                }
            )
            
            self.user_activities.append(activity)
            
            # Atualizar métricas
            self._update_volume_metric(token, amount)
            self._update_transaction_metric()
            self._update_fee_metric(fee)
            
            logger.info(f"Transação rastreada: {tx_hash}")
            
        except Exception as e:
            logger.error(f"Erro ao rastrear transação: {e}")
    
    def track_user_activity(self, user_address: str, activity_type: str,
                           value: Decimal, metadata: Dict[str, Any] = None) -> None:
        """Rastreia atividade do usuário"""
        try:
            activity = UserActivity(
                user_address=user_address,
                activity_type=activity_type,
                timestamp=time.time(),
                value=value,
                metadata=metadata or {}
            )
            
            self.user_activities.append(activity)
            
            logger.info(f"Atividade rastreada: {user_address} - {activity_type}")
            
        except Exception as e:
            logger.error(f"Erro ao rastrear atividade: {e}")
    
    def get_price_chart(self, token: str, time_range: TimeRange) -> Dict[str, Any]:
        """Obtém gráfico de preços"""
        try:
            if token not in self.price_data:
                raise ValueError("Token não encontrado")
            
            data_points = self.price_data[token]
            filtered_data = self._filter_by_time_range(data_points, time_range)
            
            # Calcular estatísticas
            prices = [point.value for point in filtered_data]
            if not prices:
                return {"error": "Nenhum dado disponível"}
            
            current_price = prices[-1]
            price_change_24h = ((current_price - prices[0]) / prices[0] * 100) if len(prices) > 1 else Decimal("0")
            
            return {
                "token": token,
                "time_range": time_range.value,
                "current_price": str(current_price),
                "price_change_24h": str(price_change_24h),
                "price_change_percentage": str(price_change_24h),
                "data_points": [
                    {
                        "timestamp": point.timestamp,
                        "price": str(point.value)
                    }
                    for point in filtered_data
                ],
                "high_24h": str(max(prices)),
                "low_24h": str(min(prices)),
                "volume_24h": self._get_volume_24h(token)
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter gráfico de preços: {e}")
            raise
    
    def get_volume_chart(self, token: str, time_range: TimeRange) -> Dict[str, Any]:
        """Obtém gráfico de volume"""
        try:
            if token not in self.volume_data:
                raise ValueError("Token não encontrado")
            
            data_points = self.volume_data[token]
            filtered_data = self._filter_by_time_range(data_points, time_range)
            
            volumes = [point.value for point in filtered_data]
            total_volume = sum(volumes)
            avg_volume = total_volume / len(volumes) if volumes else Decimal("0")
            
            return {
                "token": token,
                "time_range": time_range.value,
                "total_volume": str(total_volume),
                "average_volume": str(avg_volume),
                "data_points": [
                    {
                        "timestamp": point.timestamp,
                        "volume": str(point.value)
                    }
                    for point in filtered_data
                ]
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter gráfico de volume: {e}")
            raise
    
    def get_user_analytics(self, user_address: str) -> Dict[str, Any]:
        """Obtém analytics de um usuário"""
        try:
            user_activities = [
                activity for activity in self.user_activities
                if activity.user_address == user_address
            ]
            
            if not user_activities:
                return {"error": "Usuário não encontrado"}
            
            # Calcular estatísticas
            total_transactions = len(user_activities)
            total_volume = sum(activity.value for activity in user_activities)
            
            # Agrupar por tipo de atividade
            activity_types = {}
            for activity in user_activities:
                activity_type = activity.activity_type
                if activity_type not in activity_types:
                    activity_types[activity_type] = {
                        "count": 0,
                        "total_value": Decimal("0")
                    }
                activity_types[activity_type]["count"] += 1
                activity_types[activity_type]["total_value"] += activity.value
            
            # Atividade recente
            recent_activities = sorted(
                user_activities, 
                key=lambda x: x.timestamp, 
                reverse=True
            )[:10]
            
            return {
                "user_address": user_address,
                "total_transactions": total_transactions,
                "total_volume": str(total_volume),
                "activity_types": {
                    activity_type: {
                        "count": data["count"],
                        "total_value": str(data["total_value"])
                    }
                    for activity_type, data in activity_types.items()
                },
                "recent_activities": [
                    {
                        "type": activity.activity_type,
                        "value": str(activity.value),
                        "timestamp": activity.timestamp,
                        "metadata": activity.metadata
                    }
                    for activity in recent_activities
                ],
                "first_activity": min(activity.timestamp for activity in user_activities),
                "last_activity": max(activity.timestamp for activity in user_activities)
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter analytics do usuário: {e}")
            raise
    
    def get_market_overview(self) -> Dict[str, Any]:
        """Obtém visão geral do mercado"""
        try:
            # Calcular métricas gerais
            total_users = len(set(activity.user_address for activity in self.user_activities))
            total_transactions = len(self.user_activities)
            total_volume = sum(activity.value for activity in self.user_activities)
            
            # Top tokens por volume
            token_volumes = {}
            for activity in self.user_activities:
                token = activity.metadata.get("token", "CNB")
                if token not in token_volumes:
                    token_volumes[token] = Decimal("0")
                token_volumes[token] += activity.value
            
            top_tokens = sorted(
                token_volumes.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            # Atividade por hora (últimas 24h)
            hourly_activity = {}
            current_time = time.time()
            for i in range(24):
                hour_start = current_time - (i * 3600)
                hour_end = hour_start + 3600
                
                hour_activities = [
                    activity for activity in self.user_activities
                    if hour_start <= activity.timestamp < hour_end
                ]
                
                hourly_activity[f"hour_{i}"] = {
                    "transactions": len(hour_activities),
                    "volume": str(sum(activity.value for activity in hour_activities))
                }
            
            return {
                "total_users": total_users,
                "total_transactions": total_transactions,
                "total_volume": str(total_volume),
                "top_tokens": [
                    {
                        "token": token,
                        "volume": str(volume)
                    }
                    for token, volume in top_tokens
                ],
                "hourly_activity": hourly_activity,
                "market_cap": self._calculate_market_cap(),
                "tvl": self._calculate_tvl()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter visão geral do mercado: {e}")
            raise
    
    def generate_report(self, metric_type: MetricType, time_range: TimeRange,
                       title: str = None) -> AnalyticsReport:
        """Gera relatório de analytics"""
        try:
            report_id = self._generate_report_id()
            
            # Coletar dados baseado no tipo de métrica
            data_points = []
            
            if metric_type == MetricType.PRICE:
                data_points = self.price_data.get("CNB", [])
            elif metric_type == MetricType.VOLUME:
                data_points = self.volume_data.get("CNB", [])
            elif metric_type == MetricType.TRANSACTIONS:
                data_points = self._generate_transaction_metrics(time_range)
            elif metric_type == MetricType.USERS:
                data_points = self._generate_user_metrics(time_range)
            
            # Filtrar por intervalo de tempo
            filtered_data = self._filter_by_time_range(data_points, time_range)
            
            # Gerar resumo
            summary = self._generate_summary(filtered_data, metric_type)
            
            report = AnalyticsReport(
                report_id=report_id,
                title=title or f"{metric_type.value.title()} Report",
                metric_type=metric_type,
                time_range=time_range,
                data_points=filtered_data,
                generated_at=time.time(),
                summary=summary
            )
            
            self.reports[report_id] = report
            
            logger.info(f"Relatório gerado: {report_id}")
            return report
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            raise
    
    def _filter_by_time_range(self, data_points: List[MetricData], time_range: TimeRange) -> List[MetricData]:
        """Filtra dados por intervalo de tempo"""
        current_time = time.time()
        
        if time_range == TimeRange.HOUR:
            cutoff = current_time - 3600
        elif time_range == TimeRange.DAY:
            cutoff = current_time - (24 * 3600)
        elif time_range == TimeRange.WEEK:
            cutoff = current_time - (7 * 24 * 3600)
        elif time_range == TimeRange.MONTH:
            cutoff = current_time - (30 * 24 * 3600)
        elif time_range == TimeRange.YEAR:
            cutoff = current_time - (365 * 24 * 3600)
        else:
            cutoff = 0
        
        return [point for point in data_points if point.timestamp >= cutoff]
    
    def _update_volume_metric(self, token: str, amount: Decimal):
        """Atualiza métrica de volume"""
        self.volume_data.setdefault(token, []).append(
            MetricData(timestamp=time.time(), value=amount)
        )
    
    def _update_transaction_metric(self):
        """Atualiza métrica de transações"""
        self.metrics.setdefault("transactions", []).append(
            MetricData(timestamp=time.time(), value=Decimal("1"))
        )
    
    def _update_fee_metric(self, fee: Decimal):
        """Atualiza métrica de taxas"""
        self.metrics.setdefault("fees", []).append(
            MetricData(timestamp=time.time(), value=fee)
        )
    
    def _get_volume_24h(self, token: str) -> str:
        """Obtém volume das últimas 24h"""
        if token not in self.volume_data:
            return "0"
        
        cutoff = time.time() - (24 * 3600)
        recent_volumes = [
            point.value for point in self.volume_data[token]
            if point.timestamp >= cutoff
        ]
        
        return str(sum(recent_volumes))
    
    def _calculate_market_cap(self) -> str:
        """Calcula market cap (simulado)"""
        # Simular market cap baseado no preço atual
        current_price = self.price_data.get("CNB", [{}])[-1].value if self.price_data.get("CNB") else Decimal("0.50")
        total_supply = Decimal("1000000000")  # 1B tokens
        return str(current_price * total_supply)
    
    def _calculate_tvl(self) -> str:
        """Calcula TVL (simulado)"""
        # Simular TVL baseado no volume total
        total_volume = sum(activity.value for activity in self.user_activities)
        return str(total_volume * Decimal("0.1"))  # 10% do volume como TVL
    
    def _generate_transaction_metrics(self, time_range: TimeRange) -> List[MetricData]:
        """Gera métricas de transações"""
        # Simular dados de transações
        data_points = []
        current_time = time.time()
        
        for i in range(100):
            timestamp = current_time - (i * 3600)
            tx_count = int(statistics.NormalDist(100, 20).samples(1)[0])
            data_points.append(
                MetricData(timestamp=timestamp, value=Decimal(str(tx_count)))
            )
        
        return data_points
    
    def _generate_user_metrics(self, time_range: TimeRange) -> List[MetricData]:
        """Gera métricas de usuários"""
        # Simular dados de usuários
        data_points = []
        current_time = time.time()
        
        for i in range(100):
            timestamp = current_time - (i * 3600)
            user_count = int(statistics.NormalDist(50, 10).samples(1)[0])
            data_points.append(
                MetricData(timestamp=timestamp, value=Decimal(str(user_count)))
            )
        
        return data_points
    
    def _generate_summary(self, data_points: List[MetricData], metric_type: MetricType) -> Dict[str, Any]:
        """Gera resumo dos dados"""
        if not data_points:
            return {"error": "Nenhum dado disponível"}
        
        values = [point.value for point in data_points]
        
        return {
            "count": len(data_points),
            "min": str(min(values)),
            "max": str(max(values)),
            "average": str(sum(values) / len(values)),
            "total": str(sum(values)),
            "first_timestamp": data_points[0].timestamp,
            "last_timestamp": data_points[-1].timestamp
        }
    
    def _generate_report_id(self) -> str:
        """Gera ID único para relatório"""
        import hashlib
        data = f"report_{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def get_defi_metrics(self) -> Dict[str, Any]:
        """
        Retorna métricas gerais de DeFi.
        
        Returns:
            Dicionário com métricas DeFi simuladas
        """
        try:
            logger.info("Obtendo métricas DeFi")
            
            # Simular métricas DeFi
            defi_metrics = {
                "tvl_total": round(150000000000.0, 2),  # $150B TVL total
                "lending_volume_24h": round(5000000000.0, 2),  # $5B empréstimos 24h
                "borrowing_volume_24h": round(3000000000.0, 2),  # $3B empréstimos 24h
                "dex_volume_24h": round(8000000000.0, 2),  # $8B volume DEX 24h
                "yield_farming_tvl": round(25000000000.0, 2),  # $25B yield farming
                "stablecoin_supply": round(120000000000.0, 2),  # $120B stablecoins
                "defi_users_24h": 450000,  # 450k usuários ativos
                "protocols_count": 850,  # 850 protocolos DeFi
                "top_protocols": [
                    {"name": "Uniswap", "tvl": 4500000000.0, "volume_24h": 1200000000.0},
                    {"name": "Aave", "tvl": 3800000000.0, "volume_24h": 800000000.0},
                    {"name": "Compound", "tvl": 2200000000.0, "volume_24h": 400000000.0},
                    {"name": "MakerDAO", "tvl": 1800000000.0, "volume_24h": 200000000.0},
                    {"name": "Curve", "tvl": 1500000000.0, "volume_24h": 300000000.0}
                ],
                "yield_rates": {
                    "eth_staking": 4.2,
                    "usdc_lending": 3.8,
                    "usdt_lending": 3.5,
                    "dai_lending": 4.1,
                    "wbtc_lending": 2.9
                },
                "risk_metrics": {
                    "average_collateral_ratio": 1.45,
                    "liquidations_24h": 1250,
                    "total_liquidated_24h": 45000000.0,
                    "impermanent_loss_risk": "medium"
                },
                "innovation_metrics": {
                    "new_protocols_30d": 12,
                    "new_features_30d": 45,
                    "cross_chain_bridges": 8,
                    "layer2_adoption": 0.35
                },
                "timestamp": time.time()
            }
            
            return defi_metrics
            
        except Exception as e:
            logger.error(f"Erro ao obter métricas DeFi: {e}")
            return {
                "error": str(e),
                "tvl_total": 0.0,
                "timestamp": time.time()
            }


# Instância global
web3_analytics_manager = Web3AnalyticsManager()
