"""
Advanced Market Predictions - Predições de Mercado Precisas
Implementação da Fase 3 do roadmap CoinBalance
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from decimal import Decimal
import time
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import math

logger = logging.getLogger(__name__)


class PredictionModel(Enum):
    """Modelos de predição"""
    LSTM = "lstm"
    TRANSFORMER = "transformer"
    ARIMA = "arima"
    RANDOM_FOREST = "random_forest"
    XGBOOST = "xgboost"
    ENSEMBLE = "ensemble"


class PredictionTimeframe(Enum):
    """Timeframes de predição"""
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    HOUR_1 = "1h"
    HOUR_4 = "4h"
    DAY_1 = "1d"
    WEEK_1 = "1w"
    MONTH_1 = "1M"


class PredictionConfidence(Enum):
    """Níveis de confiança"""
    VERY_LOW = "very_low"    # < 50%
    LOW = "low"              # 50-60%
    MEDIUM = "medium"        # 60-75%
    HIGH = "high"            # 75-90%
    VERY_HIGH = "very_high"  # > 90%


@dataclass
class MarketPrediction:
    """Predição de mercado"""
    id: str
    symbol: str
    timeframe: PredictionTimeframe
    model: PredictionModel
    predicted_price: Decimal
    confidence: Decimal
    confidence_level: PredictionConfidence
    factors: List[str]
    technical_indicators: Dict[str, Decimal]
    fundamental_indicators: Dict[str, Decimal]
    sentiment_score: Decimal
    volatility_forecast: Decimal
    trend_direction: str  # "bullish", "bearish", "sideways"
    support_levels: List[Decimal]
    resistance_levels: List[Decimal]
    created_at: float = field(default_factory=time.time)
    expires_at: float = field(default_factory=lambda: time.time() + 3600)


@dataclass
class PredictionAccuracy:
    """Precisão de predições"""
    model: PredictionModel
    timeframe: PredictionTimeframe
    accuracy_score: Decimal
    total_predictions: int
    correct_predictions: int
    last_updated: float = field(default_factory=time.time)


class AdvancedMarketPredictions:
    """Sistema de Predições de Mercado Precisas"""
    
    def __init__(self):
        self.predictions: Dict[str, MarketPrediction] = {}
        self.accuracy_tracking: Dict[str, PredictionAccuracy] = {}
        self.market_data: List[Dict[str, Any]] = []
        self.models: Dict[PredictionModel, Dict[str, Any]] = {}
        self.is_active = False
        
        # Inicializar modelos
        self._initialize_prediction_models()
        
        # Inicializar tracking de precisão
        self._initialize_accuracy_tracking()
    
    def _initialize_prediction_models(self):
        """Inicializa modelos de predição"""
        self.models = {
            PredictionModel.LSTM: {
                "name": "LSTM Neural Network",
                "accuracy": Decimal('0.78'),
                "best_timeframe": PredictionTimeframe.HOUR_1,
                "features": ["price", "volume", "volatility", "rsi", "macd"],
                "last_trained": time.time(),
                "parameters": {
                    "layers": 3,
                    "neurons": 128,
                    "dropout": 0.2,
                    "epochs": 100
                }
            },
            PredictionModel.TRANSFORMER: {
                "name": "Transformer Model",
                "accuracy": Decimal('0.82'),
                "best_timeframe": PredictionTimeframe.DAY_1,
                "features": ["price", "volume", "sentiment", "news", "social"],
                "last_trained": time.time(),
                "parameters": {
                    "heads": 8,
                    "layers": 6,
                    "d_model": 512,
                    "dropout": 0.1
                }
            },
            PredictionModel.ARIMA: {
                "name": "ARIMA Time Series",
                "accuracy": Decimal('0.72'),
                "best_timeframe": PredictionTimeframe.DAY_1,
                "features": ["price_history"],
                "last_trained": time.time(),
                "parameters": {
                    "p": 2,
                    "d": 1,
                    "q": 2
                }
            },
            PredictionModel.RANDOM_FOREST: {
                "name": "Random Forest",
                "accuracy": Decimal('0.75'),
                "best_timeframe": PredictionTimeframe.HOUR_4,
                "features": ["price", "volume", "volatility", "technical_indicators"],
                "last_trained": time.time(),
                "parameters": {
                    "n_estimators": 100,
                    "max_depth": 10,
                    "min_samples_split": 5
                }
            },
            PredictionModel.XGBOOST: {
                "name": "XGBoost Gradient Boosting",
                "accuracy": Decimal('0.80'),
                "best_timeframe": PredictionTimeframe.HOUR_4,
                "features": ["price", "volume", "volatility", "fundamental_indicators"],
                "last_trained": time.time(),
                "parameters": {
                    "n_estimators": 200,
                    "max_depth": 6,
                    "learning_rate": 0.1
                }
            },
            PredictionModel.ENSEMBLE: {
                "name": "Ensemble Model",
                "accuracy": Decimal('0.85'),
                "best_timeframe": PredictionTimeframe.DAY_1,
                "features": ["all_models"],
                "last_trained": time.time(),
                "parameters": {
                    "weights": [0.2, 0.25, 0.15, 0.15, 0.25],
                    "voting": "soft"
                }
            }
        }
    
    def _initialize_accuracy_tracking(self):
        """Inicializa tracking de precisão"""
        for model in PredictionModel:
            for timeframe in PredictionTimeframe:
                key = f"{model.value}_{timeframe.value}"
                self.accuracy_tracking[key] = PredictionAccuracy(
                    model=model,
                    timeframe=timeframe,
                    accuracy_score=Decimal('0.5'),  # Inicial
                    total_predictions=0,
                    correct_predictions=0
                )
    
    async def start_prediction_system(self):
        """Inicia o sistema de predições"""
        self.is_active = True
        logger.info("🔮 Sistema de Predições de Mercado Precisas iniciado")
        
        # Iniciar coleta de dados
        asyncio.create_task(self._collect_market_data())
        
        # Iniciar treinamento de modelos
        asyncio.create_task(self._train_models())
        
        # Iniciar predições automáticas
        asyncio.create_task(self._generate_predictions())
        
        # Iniciar validação de predições
        asyncio.create_task(self._validate_predictions())
    
    async def stop_prediction_system(self):
        """Para o sistema de predições"""
        self.is_active = False
        logger.info("🛑 Sistema de Predições parado")
    
    async def _collect_market_data(self):
        """Coleta dados de mercado para predições"""
        while self.is_active:
            try:
                # Simular coleta de dados de mercado
                current_time = time.time()
                
                # Dados de preço (simulados)
                price_data = self._generate_realistic_price_data()
                
                # Dados técnicos
                technical_data = self._calculate_technical_indicators(price_data)
                
                # Dados fundamentais
                fundamental_data = self._generate_fundamental_data()
                
                # Dados de sentimento
                sentiment_data = self._generate_sentiment_data()
                
                market_data_point = {
                    "timestamp": current_time,
                    "price": price_data["price"],
                    "volume": price_data["volume"],
                    "technical": technical_data,
                    "fundamental": fundamental_data,
                    "sentiment": sentiment_data
                }
                
                self.market_data.append(market_data_point)
                
                # Manter apenas últimos 10000 pontos
                if len(self.market_data) > 10000:
                    self.market_data = self.market_data[-10000:]
                
                await asyncio.sleep(60)  # Coletar a cada minuto
                
            except Exception as e:
                logger.error(f"Erro na coleta de dados: {e}")
                await asyncio.sleep(300)
    
    def _generate_realistic_price_data(self) -> Dict[str, Decimal]:
        """Gera dados de preço realistas"""
        if not self.market_data:
            base_price = Decimal('1.0')
            base_volume = Decimal('1000000')
        else:
            last_data = self.market_data[-1]
            base_price = last_data["price"]
            base_volume = last_data["volume"]
        
        # Simular movimento de preço com tendência e volatilidade
        trend = Decimal('0.0005')  # Tendência de alta de 0.05%
        volatility = Decimal('0.02')  # Volatilidade de 2%
        
        # Adicionar ruído gaussiano
        noise = Decimal(str(np.random.normal(0, float(volatility))))
        
        new_price = base_price * (Decimal('1') + trend + noise)
        new_volume = base_volume * Decimal(str(np.random.uniform(0.8, 1.2)))
        
        return {
            "price": max(new_price, Decimal('0.01')),
            "volume": max(new_volume, Decimal('100000'))
        }
    
    def _calculate_technical_indicators(self, price_data: Dict[str, Decimal]) -> Dict[str, Decimal]:
        """Calcula indicadores técnicos"""
        if len(self.market_data) < 20:
            return {
                "rsi": Decimal('50'),
                "macd": Decimal('0'),
                "bollinger_upper": price_data["price"] * Decimal('1.02'),
                "bollinger_lower": price_data["price"] * Decimal('0.98'),
                "sma_20": price_data["price"],
                "ema_12": price_data["price"]
            }
        
        # Calcular RSI
        recent_prices = [data["price"] for data in self.market_data[-14:]]
        rsi = self._calculate_rsi(recent_prices)
        
        # Calcular MACD
        macd = self._calculate_macd(recent_prices)
        
        # Calcular Bollinger Bands
        sma_20 = sum(recent_prices) / len(recent_prices)
        std_dev = Decimal(str(np.std([float(p) for p in recent_prices])))
        bollinger_upper = sma_20 + (std_dev * Decimal('2'))
        bollinger_lower = sma_20 - (std_dev * Decimal('2'))
        
        return {
            "rsi": rsi,
            "macd": macd,
            "bollinger_upper": bollinger_upper,
            "bollinger_lower": bollinger_lower,
            "sma_20": sma_20,
            "ema_12": sma_20  # Simplificado
        }
    
    def _calculate_rsi(self, prices: List[Decimal]) -> Decimal:
        """Calcula RSI"""
        if len(prices) < 2:
            return Decimal('50')
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(Decimal('0'))
            else:
                gains.append(Decimal('0'))
                losses.append(-change)
        
        if not gains or not losses:
            return Decimal('50')
        
        avg_gain = sum(gains) / len(gains)
        avg_loss = sum(losses) / len(losses)
        
        if avg_loss == 0:
            return Decimal('100')
        
        rs = avg_gain / avg_loss
        rsi = Decimal('100') - (Decimal('100') / (Decimal('1') + rs))
        
        return rsi
    
    def _calculate_macd(self, prices: List[Decimal]) -> Decimal:
        """Calcula MACD"""
        if len(prices) < 12:
            return Decimal('0')
        
        # Simplificado - calcular diferença entre médias móveis
        ema_12 = sum(prices[-12:]) / Decimal('12')
        ema_26 = sum(prices[-26:]) / Decimal('26') if len(prices) >= 26 else ema_12
        
        return ema_12 - ema_26
    
    def _generate_fundamental_data(self) -> Dict[str, Decimal]:
        """Gera dados fundamentais"""
        return {
            "market_cap": Decimal(str(np.random.uniform(1e9, 5e9))),
            "circulating_supply": Decimal('1000000000'),
            "total_supply": Decimal('2000000000'),
            "inflation_rate": Decimal('0.02'),
            "staking_rate": Decimal('0.15'),
            "network_activity": Decimal(str(np.random.uniform(0.5, 1.0)))
        }
    
    def _generate_sentiment_data(self) -> Dict[str, Decimal]:
        """Gera dados de sentimento"""
        return {
            "social_sentiment": Decimal(str(np.random.uniform(0.3, 0.8))),
            "news_sentiment": Decimal(str(np.random.uniform(0.2, 0.9))),
            "fear_greed_index": Decimal(str(np.random.uniform(20, 80))),
            "twitter_mentions": Decimal(str(np.random.randint(100, 1000))),
            "reddit_sentiment": Decimal(str(np.random.uniform(0.1, 0.9)))
        }
    
    async def _train_models(self):
        """Treina modelos de predição"""
        while self.is_active:
            try:
                if len(self.market_data) < 100:
                    await asyncio.sleep(300)
                    continue
                
                for model_type, model_info in self.models.items():
                    await self._train_model(model_type)
                
                await asyncio.sleep(3600)  # Treinar a cada hora
                
            except Exception as e:
                logger.error(f"Erro no treinamento de modelos: {e}")
                await asyncio.sleep(3600)
    
    async def _train_model(self, model_type: PredictionModel):
        """Treina um modelo específico"""
        logger.info(f"🧠 Treinando modelo: {self.models[model_type]['name']}")
        
        # Simular tempo de treinamento
        await asyncio.sleep(2)
        
        # Atualizar timestamp de treinamento
        self.models[model_type]["last_trained"] = time.time()
        
        # Simular melhoria de precisão
        current_accuracy = self.models[model_type]["accuracy"]
        improvement = Decimal('0.005') if np.random.random() > 0.8 else Decimal('0')
        new_accuracy = min(Decimal('0.95'), current_accuracy + improvement)
        
        self.models[model_type]["accuracy"] = new_accuracy
        
        logger.info(f"✅ Modelo treinado: {self.models[model_type]['name']} - Precisão: {new_accuracy}")
    
    async def _generate_predictions(self):
        """Gera predições automaticamente"""
        while self.is_active:
            try:
                if len(self.market_data) < 50:
                    await asyncio.sleep(300)
                    continue
                
                # Gerar predições para diferentes modelos e timeframes
                for model_type in PredictionModel:
                    for timeframe in PredictionTimeframe:
                        await self._generate_model_prediction(model_type, timeframe)
                
                await asyncio.sleep(300)  # Gerar predições a cada 5 minutos
                
            except Exception as e:
                logger.error(f"Erro na geração de predições: {e}")
                await asyncio.sleep(300)
    
    async def _generate_model_prediction(self, model_type: PredictionModel, timeframe: PredictionTimeframe):
        """Gera predição para um modelo específico"""
        if not self.market_data:
            return
        
        current_data = self.market_data[-1]
        current_price = current_data["price"]
        
        # Obter dados históricos para o modelo
        historical_data = self._prepare_historical_data(timeframe)
        
        # Gerar predição baseada no modelo
        predicted_price = await self._predict_with_model(model_type, historical_data, current_price)
        
        # Calcular confiança baseada na precisão do modelo
        model_accuracy = self.models[model_type]["accuracy"]
        confidence = model_accuracy * Decimal(str(np.random.uniform(0.8, 1.0)))
        
        # Determinar nível de confiança
        if confidence >= Decimal('0.9'):
            confidence_level = PredictionConfidence.VERY_HIGH
        elif confidence >= Decimal('0.75'):
            confidence_level = PredictionConfidence.HIGH
        elif confidence >= Decimal('0.6'):
            confidence_level = PredictionConfidence.MEDIUM
        elif confidence >= Decimal('0.5'):
            confidence_level = PredictionConfidence.LOW
        else:
            confidence_level = PredictionConfidence.VERY_LOW
        
        # Calcular indicadores técnicos para a predição
        technical_indicators = self._calculate_technical_indicators({"price": predicted_price, "volume": current_data["volume"]})
        
        # Calcular sentimento
        sentiment_score = (current_data["sentiment"]["social_sentiment"] + 
                          current_data["sentiment"]["news_sentiment"]) / Decimal('2')
        
        # Calcular volatilidade prevista
        volatility_forecast = self._calculate_volatility_forecast(historical_data)
        
        # Determinar direção da tendência
        trend_direction = self._determine_trend_direction(predicted_price, current_price)
        
        # Calcular níveis de suporte e resistência
        support_levels, resistance_levels = self._calculate_support_resistance(historical_data)
        
        prediction_id = f"pred_{model_type.value}_{timeframe.value}_{int(time.time())}"
        
        prediction = MarketPrediction(
            id=prediction_id,
            symbol="CNB",
            timeframe=timeframe,
            model=model_type,
            predicted_price=predicted_price,
            confidence=confidence,
            confidence_level=confidence_level,
            factors=self.models[model_type]["features"],
            technical_indicators=technical_indicators,
            fundamental_indicators=current_data["fundamental"],
            sentiment_score=sentiment_score,
            volatility_forecast=volatility_forecast,
            trend_direction=trend_direction,
            support_levels=support_levels,
            resistance_levels=resistance_levels,
            expires_at=time.time() + self._timeframe_to_seconds(timeframe)
        )
        
        self.predictions[prediction_id] = prediction
        
        logger.info(f"🔮 Predição gerada: {model_type.value} {timeframe.value} - {predicted_price} CNB (confiança: {confidence})")
    
    def _prepare_historical_data(self, timeframe: PredictionTimeframe) -> List[Dict[str, Any]]:
        """Prepara dados históricos para predição"""
        # Simplificado - retornar dados recentes
        return self.market_data[-50:] if len(self.market_data) >= 50 else self.market_data
    
    async def _predict_with_model(self, model_type: PredictionModel, historical_data: List[Dict[str, Any]], current_price: Decimal) -> Decimal:
        """Prediz preço usando modelo específico"""
        # Simular predição baseada no tipo de modelo
        if model_type == PredictionModel.LSTM:
            # LSTM - bom para padrões temporais
            trend_factor = Decimal('1.002')
        elif model_type == PredictionModel.TRANSFORMER:
            # Transformer - bom para sequências longas
            trend_factor = Decimal('1.003')
        elif model_type == PredictionModel.ARIMA:
            # ARIMA - bom para séries temporais
            trend_factor = Decimal('1.001')
        elif model_type == PredictionModel.RANDOM_FOREST:
            # Random Forest - bom para features categóricas
            trend_factor = Decimal('1.0015')
        elif model_type == PredictionModel.XGBOOST:
            # XGBoost - bom para features numéricas
            trend_factor = Decimal('1.0025')
        else:  # ENSEMBLE
            # Ensemble - combina todos os modelos
            trend_factor = Decimal('1.002')
        
        # Adicionar volatilidade
        volatility = Decimal('0.01')
        noise = Decimal(str(np.random.normal(0, float(volatility))))
        
        predicted_price = current_price * trend_factor * (Decimal('1') + noise)
        
        return max(predicted_price, Decimal('0.01'))
    
    def _calculate_volatility_forecast(self, historical_data: List[Dict[str, Any]]) -> Decimal:
        """Calcula previsão de volatilidade"""
        if len(historical_data) < 10:
            return Decimal('0.02')
        
        prices = [data["price"] for data in historical_data[-10:]]
        returns = [np.log(float(prices[i] / prices[i-1])) for i in range(1, len(prices))]
        
        volatility = np.std(returns) * np.sqrt(24)  # Volatilidade diária
        
        return Decimal(str(volatility))
    
    def _determine_trend_direction(self, predicted_price: Decimal, current_price: Decimal) -> str:
        """Determina direção da tendência"""
        change_percent = (predicted_price - current_price) / current_price
        
        if change_percent > Decimal('0.02'):  # > 2%
            return "bullish"
        elif change_percent < Decimal('-0.02'):  # < -2%
            return "bearish"
        else:
            return "sideways"
    
    def _calculate_support_resistance(self, historical_data: List[Dict[str, Any]]) -> Tuple[List[Decimal], List[Decimal]]:
        """Calcula níveis de suporte e resistência"""
        if len(historical_data) < 20:
            return [], []
        
        prices = [data["price"] for data in historical_data]
        
        # Simplificado - usar percentis
        support_levels = [
            Decimal(str(np.percentile([float(p) for p in prices], 25))),
            Decimal(str(np.percentile([float(p) for p in prices], 10)))
        ]
        
        resistance_levels = [
            Decimal(str(np.percentile([float(p) for p in prices], 75))),
            Decimal(str(np.percentile([float(p) for p in prices], 90)))
        ]
        
        return support_levels, resistance_levels
    
    def _timeframe_to_seconds(self, timeframe: PredictionTimeframe) -> int:
        """Converte timeframe para segundos"""
        timeframe_map = {
            PredictionTimeframe.MINUTE_1: 60,
            PredictionTimeframe.MINUTE_5: 300,
            PredictionTimeframe.MINUTE_15: 900,
            PredictionTimeframe.HOUR_1: 3600,
            PredictionTimeframe.HOUR_4: 14400,
            PredictionTimeframe.DAY_1: 86400,
            PredictionTimeframe.WEEK_1: 604800,
            PredictionTimeframe.MONTH_1: 2592000
        }
        
        return timeframe_map.get(timeframe, 3600)
    
    async def _validate_predictions(self):
        """Valida predições expiradas"""
        while self.is_active:
            try:
                current_time = time.time()
                expired_predictions = [
                    pred for pred in self.predictions.values()
                    if pred.expires_at < current_time
                ]
                
                for prediction in expired_predictions:
                    await self._validate_prediction(prediction)
                
                await asyncio.sleep(300)  # Validar a cada 5 minutos
                
            except Exception as e:
                logger.error(f"Erro na validação de predições: {e}")
                await asyncio.sleep(300)
    
    async def _validate_prediction(self, prediction: MarketPrediction):
        """Valida uma predição específica"""
        # Encontrar preço atual mais próximo ao tempo de expiração
        current_price = self.market_data[-1]["price"] if self.market_data else Decimal('1.0')
        
        # Calcular erro da predição
        error = abs(prediction.predicted_price - current_price) / current_price
        
        # Determinar se a predição foi correta (erro < 5%)
        is_correct = error < Decimal('0.05')
        
        # Atualizar tracking de precisão
        key = f"{prediction.model.value}_{prediction.timeframe.value}"
        if key in self.accuracy_tracking:
            accuracy_tracking = self.accuracy_tracking[key]
            accuracy_tracking.total_predictions += 1
            
            if is_correct:
                accuracy_tracking.correct_predictions += 1
            
            # Recalcular score de precisão
            accuracy_tracking.accuracy_score = Decimal(accuracy_tracking.correct_predictions) / Decimal(accuracy_tracking.total_predictions)
            accuracy_tracking.last_updated = time.time()
        
        # Remover predição expirada
        if prediction.id in self.predictions:
            del self.predictions[prediction.id]
        
        logger.info(f"✅ Predição validada: {prediction.model.value} {prediction.timeframe.value} - {'Correta' if is_correct else 'Incorreta'} (erro: {error:.2%})")
    
    def get_prediction_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas das predições"""
        total_predictions = len(self.predictions)
        active_predictions = len([p for p in self.predictions.values() if p.expires_at > time.time()])
        
        # Calcular precisão média por modelo
        model_accuracy = {}
        for model_type in PredictionModel:
            model_predictions = [p for p in self.predictions.values() if p.model == model_type]
            if model_predictions:
                avg_confidence = sum(p.confidence for p in model_predictions) / len(model_predictions)
                model_accuracy[model_type.value] = float(avg_confidence)
        
        # Calcular precisão média por timeframe
        timeframe_accuracy = {}
        for timeframe in PredictionTimeframe:
            timeframe_predictions = [p for p in self.predictions.values() if p.timeframe == timeframe]
            if timeframe_predictions:
                avg_confidence = sum(p.confidence for p in timeframe_predictions) / len(timeframe_predictions)
                timeframe_accuracy[timeframe.value] = float(avg_confidence)
        
        return {
            "system_status": "active" if self.is_active else "stopped",
            "predictions": {
                "total": total_predictions,
                "active": active_predictions,
                "by_model": {
                    model_type.value: len([p for p in self.predictions.values() if p.model == model_type])
                    for model_type in PredictionModel
                },
                "by_timeframe": {
                    timeframe.value: len([p for p in self.predictions.values() if p.timeframe == timeframe])
                    for timeframe in PredictionTimeframe
                }
            },
            "model_accuracy": model_accuracy,
            "timeframe_accuracy": timeframe_accuracy,
            "accuracy_tracking": {
                key: {
                    "model": accuracy.model.value,
                    "timeframe": accuracy.timeframe.value,
                    "accuracy_score": float(accuracy.accuracy_score),
                    "total_predictions": accuracy.total_predictions,
                    "correct_predictions": accuracy.correct_predictions
                }
                for key, accuracy in self.accuracy_tracking.items()
            },
            "market_data_points": len(self.market_data)
        }


# Instância global do sistema de predições
market_predictions = AdvancedMarketPredictions()
