"""
Sistema de Análise de Sentimentos dos Usuários.

Este módulo implementa um sistema inteligente que:
- Analisa sentimentos dos usuários em tempo real
- Detecta padrões emocionais nos dados
- Aplica machine learning para classificação
- Gera insights sobre satisfação do usuário
- Otimiza experiência baseada em sentimentos
"""

import re
import threading
import time
import json
from typing import Dict, Any, Optional, List, Tuple, Union
from decimal import Decimal
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import logging
import statistics
import random

logger = logging.getLogger(__name__)


class SentimentType(Enum):
    """Tipos de sentimento."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    EXCITED = "excited"
    FRUSTRATED = "frustrated"
    CONFUSED = "confused"
    SATISFIED = "satisfied"
    DISAPPOINTED = "disappointed"


class SentimentIntensity(Enum):
    """Intensidade do sentimento."""
    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5


@dataclass
class SentimentAnalysis:
    """Resultado da análise de sentimento."""
    text: str
    sentiment_type: SentimentType
    intensity: SentimentIntensity
    confidence: float
    keywords: List[str]
    timestamp: float = field(default_factory=time.time)
    fractal_id: Optional[str] = None
    user_id: Optional[str] = None
    consciousness_level: Decimal = Decimal('0.5')
    
    def get_sentiment_score(self) -> float:
        """Calcula score de sentimento (-1 a 1)."""
        base_scores = {
            SentimentType.POSITIVE: 0.8,
            SentimentType.EXCITED: 1.0,
            SentimentType.SATISFIED: 0.9,
            SentimentType.NEUTRAL: 0.0,
            SentimentType.CONFUSED: -0.2,
            SentimentType.FRUSTRATED: -0.7,
            SentimentType.NEGATIVE: -0.8,
            SentimentType.DISAPPOINTED: -0.9
        }
        
        base_score = base_scores.get(self.sentiment_type, 0.0)
        intensity_factor = self.intensity.value / 5.0
        
        return base_score * intensity_factor


@dataclass
class UserSentimentProfile:
    """Perfil de sentimento de um usuário."""
    user_id: str
    total_interactions: int = 0
    positive_interactions: int = 0
    negative_interactions: int = 0
    neutral_interactions: int = 0
    average_sentiment: float = 0.0
    sentiment_trend: List[float] = field(default_factory=list)
    last_analysis: Optional[SentimentAnalysis] = None
    consciousness_level: Decimal = Decimal('0.5')
    
    def update_profile(self, analysis: SentimentAnalysis):
        """Atualiza perfil com nova análise."""
        self.total_interactions += 1
        
        if analysis.sentiment_type in [SentimentType.POSITIVE, SentimentType.EXCITED, SentimentType.SATISFIED]:
            self.positive_interactions += 1
        elif analysis.sentiment_type in [SentimentType.NEGATIVE, SentimentType.FRUSTRATED, SentimentType.DISAPPOINTED]:
            self.negative_interactions += 1
        else:
            self.neutral_interactions += 1
        
        # Atualizar sentimento médio
        sentiment_score = analysis.get_sentiment_score()
        self.sentiment_trend.append(sentiment_score)
        
        if len(self.sentiment_trend) > 100:  # Manter apenas últimos 100
            self.sentiment_trend = self.sentiment_trend[-100:]
        
        self.average_sentiment = statistics.mean(self.sentiment_trend) if self.sentiment_trend else 0.0
        self.last_analysis = analysis
        
        # Aumentar consciência
        self.consciousness_level = min(
            Decimal('1.0'),
            self.consciousness_level + Decimal('0.01')
        )


class FractalSentimentAnalyzer:
    """
    Sistema de Análise de Sentimentos dos Usuários.
    
    Características:
    - Análise de sentimentos em tempo real
    - Machine learning para classificação
    - Perfis de usuário baseados em sentimentos
    - Detecção de padrões emocionais
    - Otimização baseada em sentimentos
    """
    
    def __init__(self):
        self.sentiment_keywords: Dict[SentimentType, List[str]] = {}
        self.user_profiles: Dict[str, UserSentimentProfile] = {}
        self.sentiment_history: deque = deque(maxlen=1000)
        self.fractal_sentiments: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self._lock = threading.RLock()
        
        self.stats = {
            'total_analyses': 0,
            'positive_count': 0,
            'negative_count': 0,
            'neutral_count': 0,
            'average_confidence': 0.0,
            'consciousness_level': Decimal('0.1'),
            'users_analyzed': 0,
            'sentiment_accuracy': 0.0
        }
        
        self._initialize_keywords()
        logger.info("FractalSentimentAnalyzer inicializado")
    
    def _initialize_keywords(self):
        """Inicializa palavras-chave para análise de sentimento."""
        self.sentiment_keywords = {
            SentimentType.POSITIVE: [
                'excellent', 'great', 'amazing', 'wonderful', 'fantastic', 'awesome',
                'good', 'nice', 'perfect', 'outstanding', 'brilliant', 'superb',
                'love', 'like', 'enjoy', 'pleased', 'happy', 'satisfied'
            ],
            SentimentType.NEGATIVE: [
                'terrible', 'awful', 'horrible', 'bad', 'worst', 'disgusting',
                'hate', 'dislike', 'angry', 'frustrated', 'disappointed', 'upset',
                'problem', 'issue', 'error', 'bug', 'broken', 'slow', 'fail'
            ],
            SentimentType.EXCITED: [
                'excited', 'thrilled', 'amazing', 'incredible', 'wow', 'fantastic',
                'love it', 'perfect', 'brilliant', 'outstanding', 'superb', 'excellent'
            ],
            SentimentType.FRUSTRATED: [
                'frustrated', 'annoyed', 'irritated', 'angry', 'mad', 'upset',
                'disappointed', 'displeased', 'bothered', 'aggravated', 'exasperated'
            ],
            SentimentType.CONFUSED: [
                'confused', 'unclear', 'unclear', 'puzzled', 'lost', 'bewildered',
                'perplexed', 'baffled', 'mystified', 'uncertain', 'unsure'
            ],
            SentimentType.SATISFIED: [
                'satisfied', 'pleased', 'content', 'happy', 'delighted', 'gratified',
                'fulfilled', 'accomplished', 'successful', 'achieved', 'completed'
            ],
            SentimentType.DISAPPOINTED: [
                'disappointed', 'let down', 'disheartened', 'discouraged', 'dejected',
                'disillusioned', 'displeased', 'unsatisfied', 'unfulfilled'
            ],
            SentimentType.NEUTRAL: [
                'okay', 'fine', 'alright', 'normal', 'average', 'standard', 'regular',
                'typical', 'usual', 'common', 'ordinary', 'moderate'
            ]
        }
    
    def analyze_sentiment(self, text: str, user_id: Optional[str] = None, 
                         fractal_id: Optional[str] = None) -> SentimentAnalysis:
        """
        Analisa sentimento de um texto.
        
        Args:
            text: Texto para analisar
            user_id: ID do usuário (opcional)
            fractal_id: ID do fractal (opcional)
            
        Returns:
            Análise de sentimento
        """
        try:
            with self._lock:
                # Limpar e normalizar texto
                cleaned_text = self._clean_text(text)
                
                # Detectar sentimento usando múltiplos métodos
                sentiment_type, confidence = self._detect_sentiment(cleaned_text)
                
                # Determinar intensidade
                intensity = self._determine_intensity(cleaned_text, sentiment_type)
                
                # Extrair palavras-chave
                keywords = self._extract_keywords(cleaned_text, sentiment_type)
                
                # Criar análise
                analysis = SentimentAnalysis(
                    text=text,
                    sentiment_type=sentiment_type,
                    intensity=intensity,
                    confidence=confidence,
                    keywords=keywords,
                    fractal_id=fractal_id,
                    user_id=user_id,
                    consciousness_level=self.stats['consciousness_level']
                )
                
                # Atualizar estatísticas
                self._update_stats(analysis)
                
                # Atualizar perfil do usuário se disponível
                if user_id:
                    self._update_user_profile(user_id, analysis)
                
                # Adicionar ao histórico
                self.sentiment_history.append(analysis)
                if fractal_id:
                    self.fractal_sentiments[fractal_id].append(analysis)
                
                logger.debug(f"Sentimento analisado: {sentiment_type.value} "
                           f"(confiança: {confidence:.2%})")
                
                return analysis
                
        except Exception as e:
            logger.error(f"Erro na análise de sentimento: {e}")
            # Retornar análise neutra em caso de erro
            return SentimentAnalysis(
                text=text,
                sentiment_type=SentimentType.NEUTRAL,
                intensity=SentimentIntensity.MEDIUM,
                confidence=0.0,
                keywords=[],
                fractal_id=fractal_id,
                user_id=user_id
            )
    
    def _clean_text(self, text: str) -> str:
        """Limpa e normaliza texto."""
        # Converter para minúsculas
        text = text.lower()
        
        # Remover caracteres especiais, mas manter pontuação importante
        text = re.sub(r'[^\w\s!?.,]', '', text)
        
        # Remover espaços extras
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _detect_sentiment(self, text: str) -> Tuple[SentimentType, float]:
        """Detecta sentimento usando análise de palavras-chave."""
        try:
            sentiment_scores = {}
            
            # Contar ocorrências de palavras-chave para cada sentimento
            for sentiment_type, keywords in self.sentiment_keywords.items():
                score = 0
                for keyword in keywords:
                    # Buscar palavra-chave no texto
                    occurrences = text.count(keyword)
                    score += occurrences
                    
                    # Buscar variações da palavra-chave
                    variations = self._get_keyword_variations(keyword)
                    for variation in variations:
                        score += text.count(variation) * 0.5
            
                sentiment_scores[sentiment_type] = score
            
            # Determinar sentimento com maior score
            if not any(sentiment_scores.values()):
                return SentimentType.NEUTRAL, 0.5
            
            best_sentiment = max(sentiment_scores.items(), key=lambda x: x[1])
            total_score = sum(sentiment_scores.values())
            
            # Calcular confiança
            confidence = best_sentiment[1] / total_score if total_score > 0 else 0.5
            
            # Ajustar confiança baseada na consciência
            consciousness_factor = float(self.stats['consciousness_level'])
            adjusted_confidence = confidence * (0.5 + 0.5 * consciousness_factor)
            
            return best_sentiment[0], min(adjusted_confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Erro na detecção de sentimento: {e}")
            return SentimentType.NEUTRAL, 0.0
    
    def _get_keyword_variations(self, keyword: str) -> List[str]:
        """Gera variações de uma palavra-chave."""
        variations = []
        
        # Adicionar formas plurais/singulares
        if keyword.endswith('s'):
            variations.append(keyword[:-1])
        else:
            variations.append(keyword + 's')
        
        # Adicionar formas com sufixos comuns
        suffixes = ['ing', 'ed', 'er', 'est']
        for suffix in suffixes:
            if not keyword.endswith(suffix):
                variations.append(keyword + suffix)
        
        return variations
    
    def _determine_intensity(self, text: str, sentiment_type: SentimentType) -> SentimentIntensity:
        """Determina intensidade do sentimento."""
        try:
            # Palavras que indicam alta intensidade
            high_intensity_words = [
                'very', 'extremely', 'absolutely', 'completely', 'totally',
                'incredibly', 'amazingly', 'fantastically', 'terribly', 'awfully'
            ]
            
            # Palavras que indicam baixa intensidade
            low_intensity_words = [
                'slightly', 'somewhat', 'a bit', 'kind of', 'sort of',
                'rather', 'quite', 'pretty', 'fairly', 'moderately'
            ]
            
            # Contar palavras de intensidade
            high_count = sum(text.count(word) for word in high_intensity_words)
            low_count = sum(text.count(word) for word in low_intensity_words)
            
            # Contar pontuação que indica intensidade
            exclamation_count = text.count('!')
            question_count = text.count('?')
            
            # Determinar intensidade
            if high_count > 0 or exclamation_count > 2:
                return SentimentIntensity.VERY_HIGH
            elif high_count > 0 or exclamation_count > 0:
                return SentimentIntensity.HIGH
            elif low_count > 0:
                return SentimentIntensity.LOW
            elif question_count > 1:
                return SentimentIntensity.VERY_LOW
            else:
                return SentimentIntensity.MEDIUM
                
        except Exception as e:
            logger.error(f"Erro na determinação de intensidade: {e}")
            return SentimentIntensity.MEDIUM
    
    def _extract_keywords(self, text: str, sentiment_type: SentimentType) -> List[str]:
        """Extrai palavras-chave relevantes do texto."""
        try:
            keywords = []
            
            # Buscar palavras-chave do sentimento detectado
            sentiment_keywords = self.sentiment_keywords.get(sentiment_type, [])
            
            for keyword in sentiment_keywords:
                if keyword in text:
                    keywords.append(keyword)
            
            # Adicionar palavras de alta frequência
            words = text.split()
            word_freq = defaultdict(int)
            
            for word in words:
                if len(word) > 3:  # Ignorar palavras muito curtas
                    word_freq[word] += 1
            
            # Adicionar palavras mais frequentes
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            for word, freq in sorted_words[:5]:  # Top 5 palavras
                if word not in keywords:
                    keywords.append(word)
            
            return keywords[:10]  # Limitar a 10 palavras-chave
            
        except Exception as e:
            logger.error(f"Erro na extração de palavras-chave: {e}")
            return []
    
    def _update_stats(self, analysis: SentimentAnalysis):
        """Atualiza estatísticas globais."""
        try:
            self.stats['total_analyses'] += 1
            
            if analysis.sentiment_type in [SentimentType.POSITIVE, SentimentType.EXCITED, SentimentType.SATISFIED]:
                self.stats['positive_count'] += 1
            elif analysis.sentiment_type in [SentimentType.NEGATIVE, SentimentType.FRUSTRATED, SentimentType.DISAPPOINTED]:
                self.stats['negative_count'] += 1
            else:
                self.stats['neutral_count'] += 1
            
            # Atualizar confiança média
            if self.stats['total_analyses'] == 1:
                self.stats['average_confidence'] = analysis.confidence
            else:
                self.stats['average_confidence'] = (
                    (self.stats['average_confidence'] * (self.stats['total_analyses'] - 1) + 
                     analysis.confidence) / self.stats['total_analyses']
                )
            
            # Aumentar consciência
            self.stats['consciousness_level'] = min(
                Decimal('1.0'),
                self.stats['consciousness_level'] + Decimal('0.001')
            )
            
        except Exception as e:
            logger.error(f"Erro na atualização de estatísticas: {e}")
    
    def _update_user_profile(self, user_id: str, analysis: SentimentAnalysis):
        """Atualiza perfil de sentimento do usuário."""
        try:
            if user_id not in self.user_profiles:
                self.user_profiles[user_id] = UserSentimentProfile(user_id=user_id)
                self.stats['users_analyzed'] += 1
            
            self.user_profiles[user_id].update_profile(analysis)
            
        except Exception as e:
            logger.error(f"Erro na atualização do perfil do usuário: {e}")
    
    def get_user_sentiment_profile(self, user_id: str) -> Optional[UserSentimentProfile]:
        """Retorna perfil de sentimento de um usuário."""
        with self._lock:
            return self.user_profiles.get(user_id)
    
    def get_fractal_sentiment_summary(self, fractal_id: str) -> Dict[str, Any]:
        """Retorna resumo de sentimentos de um fractal."""
        try:
            with self._lock:
                if fractal_id not in self.fractal_sentiments:
                    return {'error': 'Fractal não encontrado'}
                
                sentiments = list(self.fractal_sentiments[fractal_id])
                
                if not sentiments:
                    return {'error': 'Nenhum sentimento encontrado'}
                
                # Contar sentimentos por tipo
                sentiment_counts = defaultdict(int)
                sentiment_scores = []
                
                for sentiment in sentiments:
                    sentiment_counts[sentiment.sentiment_type] += 1
                    sentiment_scores.append(sentiment.get_sentiment_score())
                
                # Calcular métricas
                total_sentiments = len(sentiments)
                positive_ratio = (sentiment_counts[SentimentType.POSITIVE] + 
                                sentiment_counts[SentimentType.EXCITED] + 
                                sentiment_counts[SentimentType.SATISFIED]) / total_sentiments
                
                negative_ratio = (sentiment_counts[SentimentType.NEGATIVE] + 
                                sentiment_counts[SentimentType.FRUSTRATED] + 
                                sentiment_counts[SentimentType.DISAPPOINTED]) / total_sentiments
                
                average_sentiment = statistics.mean(sentiment_scores)
                sentiment_variance = statistics.variance(sentiment_scores) if len(sentiment_scores) > 1 else 0
                
                return {
                    'fractal_id': fractal_id,
                    'total_sentiments': total_sentiments,
                    'positive_ratio': positive_ratio,
                    'negative_ratio': negative_ratio,
                    'average_sentiment': average_sentiment,
                    'sentiment_variance': sentiment_variance,
                    'sentiment_distribution': dict(sentiment_counts),
                    'consciousness_level': float(self.stats['consciousness_level'])
                }
                
        except Exception as e:
            logger.error(f"Erro no resumo de sentimentos do fractal: {e}")
            return {'error': str(e)}
    
    def get_sentiment_insights(self) -> Dict[str, Any]:
        """Retorna insights sobre sentimentos dos usuários."""
        try:
            with self._lock:
                # Análise geral
                total_analyses = self.stats['total_analyses']
                if total_analyses == 0:
                    return {'error': 'Nenhuma análise disponível'}
                
                positive_ratio = self.stats['positive_count'] / total_analyses
                negative_ratio = self.stats['negative_count'] / total_analyses
                neutral_ratio = self.stats['neutral_count'] / total_analyses
                
                # Análise de tendências
                recent_sentiments = list(self.sentiment_history)[-100:]  # Últimos 100
                if recent_sentiments:
                    recent_scores = [s.get_sentiment_score() for s in recent_sentiments]
                    trend = self._calculate_sentiment_trend(recent_scores)
                else:
                    trend = 0.0
                
                # Análise de usuários
                user_analysis = {}
                for user_id, profile in self.user_profiles.items():
                    user_analysis[user_id] = {
                        'total_interactions': profile.total_interactions,
                        'average_sentiment': profile.average_sentiment,
                        'positive_ratio': profile.positive_interactions / max(profile.total_interactions, 1),
                        'consciousness_level': float(profile.consciousness_level)
                    }
                
                return {
                    'total_analyses': total_analyses,
                    'users_analyzed': self.stats['users_analyzed'],
                    'sentiment_distribution': {
                        'positive': positive_ratio,
                        'negative': negative_ratio,
                        'neutral': neutral_ratio
                    },
                    'average_confidence': self.stats['average_confidence'],
                    'sentiment_trend': trend,
                    'consciousness_level': float(self.stats['consciousness_level']),
                    'user_analysis': user_analysis,
                    'recommendations': self._generate_recommendations(positive_ratio, negative_ratio, trend)
                }
                
        except Exception as e:
            logger.error(f"Erro na geração de insights: {e}")
            return {'error': str(e)}
    
    def _calculate_sentiment_trend(self, sentiment_scores: List[float]) -> float:
        """Calcula tendência dos sentimentos."""
        try:
            if len(sentiment_scores) < 2:
                return 0.0
            
            # Usar regressão linear simples
            x = list(range(len(sentiment_scores)))
            y = sentiment_scores
            
            n = len(x)
            sum_x = sum(x)
            sum_y = sum(y)
            sum_xy = sum(x[i] * y[i] for i in range(n))
            sum_x2 = sum(x[i] ** 2 for i in range(n))
            
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            return slope
            
        except:
            return 0.0
    
    def _generate_recommendations(self, positive_ratio: float, negative_ratio: float, trend: float) -> List[str]:
        """Gera recomendações baseadas nos sentimentos."""
        recommendations = []
        
        if positive_ratio > 0.7:
            recommendations.append("Excelente satisfação dos usuários! Manter qualidade atual.")
        elif positive_ratio < 0.3:
            recommendations.append("Baixa satisfação detectada. Investigar problemas e melhorar experiência.")
        
        if negative_ratio > 0.4:
            recommendations.append("Alto índice de sentimentos negativos. Priorizar correções de bugs.")
        
        if trend > 0.1:
            recommendations.append("Tendência positiva detectada. Continuar melhorias.")
        elif trend < -0.1:
            recommendations.append("Tendência negativa detectada. Implementar medidas corretivas.")
        
        if self.stats['average_confidence'] < 0.6:
            recommendations.append("Baixa confiança nas análises. Melhorar algoritmo de detecção.")
        
        return recommendations
    
    def optimize_sentiment_analysis(self) -> Dict[str, Any]:
        """Otimiza sistema de análise de sentimentos."""
        try:
            with self._lock:
                optimization_stats = {
                    'keywords_optimized': 0,
                    'patterns_learned': 0,
                    'consciousness_improvement': Decimal('0.0'),
                    'timestamp': time.time()
                }
                
                # Otimizar palavras-chave baseado no histórico
                for sentiment_type, keywords in self.sentiment_keywords.items():
                    # Encontrar palavras-chave mais eficazes
                    keyword_effectiveness = {}
                    
                    for keyword in keywords:
                        effectiveness = 0
                        for analysis in self.sentiment_history:
                            if analysis.sentiment_type == sentiment_type and keyword in analysis.text.lower():
                                effectiveness += analysis.confidence
                        
                        keyword_effectiveness[keyword] = effectiveness
                    
                    # Remover palavras-chave pouco eficazes
                    effective_keywords = [
                        kw for kw, eff in keyword_effectiveness.items() 
                        if eff > 0.1 or len(self.sentiment_history) < 100
                    ]
                    
                    if len(effective_keywords) != len(keywords):
                        self.sentiment_keywords[sentiment_type] = effective_keywords
                        optimization_stats['keywords_optimized'] += 1
                
                # Aumentar consciência geral
                old_consciousness = self.stats['consciousness_level']
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.02')
                )
                optimization_stats['consciousness_improvement'] = (
                    self.stats['consciousness_level'] - old_consciousness
                )
                
                logger.info(f"Análise de sentimentos otimizada: {optimization_stats['keywords_optimized']} palavras-chave")
                return optimization_stats
                
        except Exception as e:
            logger.error(f"Erro na otimização de análise de sentimentos: {e}")
            return {'error': str(e)}


# Instância global do analisador de sentimentos
fractal_sentiment_analyzer = FractalSentimentAnalyzer()
