"""
Autonomous Economy System - Sistema de Economia Autônoma
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
import math
import numpy as np
import random

logger = logging.getLogger(__name__)


class EconomyPhase(Enum):
    """Fases da economia"""
    GROWTH = "growth"
    STABILITY = "stability"
    DECLINE = "decline"
    RECOVERY = "recovery"
    TRANSFORMATION = "transformation"


class EconomicIndicator(Enum):
    """Indicadores econômicos"""
    GDP = "gdp"
    INFLATION = "inflation"
    UNEMPLOYMENT = "unemployment"
    INTEREST_RATE = "interest_rate"
    MONEY_SUPPLY = "money_supply"
    MARKET_CAP = "market_cap"
    TRADING_VOLUME = "trading_volume"
    USER_ACTIVITY = "user_activity"


class PolicyType(Enum):
    """Tipos de políticas econômicas"""
    MONETARY = "monetary"
    FISCAL = "fiscal"
    REGULATORY = "regulatory"
    INCENTIVE = "incentive"
    EMERGENCY = "emergency"


@dataclass
class EconomicIndicatorData:
    """Dados de indicador econômico"""
    name: EconomicIndicator
    value: Decimal
    target_value: Decimal
    weight: Decimal
    trend: str  # "increasing", "decreasing", "stable"
    impact: str  # "positive", "negative", "neutral"
    timestamp: float = field(default_factory=time.time)


@dataclass
class EconomicPolicy:
    """Política econômica"""
    id: str
    policy_type: PolicyType
    name: str
    description: str
    target_indicators: List[EconomicIndicator]
    parameters: Dict[str, Any]
    effectiveness: Decimal
    duration: int  # em segundos
    created_at: float = field(default_factory=time.time)
    is_active: bool = True


@dataclass
class EconomicCycle:
    """Ciclo econômico"""
    id: str
    phase: EconomyPhase
    start_time: float
    duration: int
    indicators: Dict[EconomicIndicator, Decimal]
    policies_applied: List[str]
    performance_score: Decimal
    is_active: bool = True


class AutonomousEconomySystem:
    """Sistema de Economia Autônoma"""
    
    def __init__(self):
        self.current_phase = EconomyPhase.GROWTH
        self.economic_indicators: Dict[EconomicIndicator, EconomicIndicatorData] = {}
        self.active_policies: Dict[str, EconomicPolicy] = {}
        self.economic_cycles: List[EconomicCycle] = []
        self.decision_history: List[Dict[str, Any]] = []
        self.is_active = False
        
        # Inicializar indicadores econômicos
        self._initialize_economic_indicators()
        
        # Inicializar políticas padrão
        self._initialize_default_policies()
    
    def _initialize_economic_indicators(self):
        """Inicializa indicadores econômicos"""
        self.economic_indicators = {
            EconomicIndicator.GDP: EconomicIndicatorData(
                name=EconomicIndicator.GDP,
                value=Decimal('1000000000'),  # 1B CNB
                target_value=Decimal('2000000000'),  # 2B CNB
                weight=Decimal('0.3'),
                trend="increasing",
                impact="positive"
            ),
            EconomicIndicator.INFLATION: EconomicIndicatorData(
                name=EconomicIndicator.INFLATION,
                value=Decimal('0.02'),  # 2%
                target_value=Decimal('0.03'),  # 3%
                weight=Decimal('0.2'),
                trend="stable",
                impact="neutral"
            ),
            EconomicIndicator.UNEMPLOYMENT: EconomicIndicatorData(
                name=EconomicIndicator.UNEMPLOYMENT,
                value=Decimal('0.05'),  # 5%
                target_value=Decimal('0.03'),  # 3%
                weight=Decimal('0.15'),
                trend="decreasing",
                impact="positive"
            ),
            EconomicIndicator.INTEREST_RATE: EconomicIndicatorData(
                name=EconomicIndicator.INTEREST_RATE,
                value=Decimal('0.05'),  # 5%
                target_value=Decimal('0.04'),  # 4%
                weight=Decimal('0.15'),
                trend="stable",
                impact="neutral"
            ),
            EconomicIndicator.MONEY_SUPPLY: EconomicIndicatorData(
                name=EconomicIndicator.MONEY_SUPPLY,
                value=Decimal('1000000000'),  # 1B CNB
                target_value=Decimal('1500000000'),  # 1.5B CNB
                weight=Decimal('0.1'),
                trend="increasing",
                impact="positive"
            ),
            EconomicIndicator.MARKET_CAP: EconomicIndicatorData(
                name=EconomicIndicator.MARKET_CAP,
                value=Decimal('2000000000'),  # 2B CNB
                target_value=Decimal('5000000000'),  # 5B CNB
                weight=Decimal('0.05'),
                trend="increasing",
                impact="positive"
            ),
            EconomicIndicator.TRADING_VOLUME: EconomicIndicatorData(
                name=EconomicIndicator.TRADING_VOLUME,
                value=Decimal('10000000'),  # 10M CNB/dia
                target_value=Decimal('50000000'),  # 50M CNB/dia
                weight=Decimal('0.03'),
                trend="increasing",
                impact="positive"
            ),
            EconomicIndicator.USER_ACTIVITY: EconomicIndicatorData(
                name=EconomicIndicator.USER_ACTIVITY,
                value=Decimal('1000'),  # 1000 usuários ativos
                target_value=Decimal('10000'),  # 10000 usuários ativos
                weight=Decimal('0.02'),
                trend="increasing",
                impact="positive"
            )
        }
    
    def _initialize_default_policies(self):
        """Inicializa políticas econômicas padrão"""
        # Política Monetária - Controle de Inflação
        inflation_policy = EconomicPolicy(
            id="monetary_inflation_control",
            policy_type=PolicyType.MONETARY,
            name="Controle de Inflação",
            description="Ajusta taxa de juros para controlar inflação",
            target_indicators=[EconomicIndicator.INFLATION],
            parameters={
                "interest_rate_adjustment": Decimal('0.01'),
                "trigger_threshold": Decimal('0.05'),
                "max_adjustment": Decimal('0.02')
            },
            effectiveness=Decimal('0.8'),
            duration=86400  # 24 horas
        )
        
        # Política Fiscal - Incentivo ao Crescimento
        growth_policy = EconomicPolicy(
            id="fiscal_growth_incentive",
            policy_type=PolicyType.FISCAL,
            name="Incentivo ao Crescimento",
            description="Reduz impostos e aumenta gastos para estimular crescimento",
            target_indicators=[EconomicIndicator.GDP, EconomicIndicator.UNEMPLOYMENT],
            parameters={
                "tax_reduction": Decimal('0.05'),
                "spending_increase": Decimal('0.1'),
                "duration_months": 6
            },
            effectiveness=Decimal('0.7'),
            duration=15552000  # 6 meses
        )
        
        # Política Regulatória - Estabilidade do Mercado
        stability_policy = EconomicPolicy(
            id="regulatory_market_stability",
            policy_type=PolicyType.REGULATORY,
            name="Estabilidade do Mercado",
            description="Implementa regulamentações para estabilizar o mercado",
            target_indicators=[EconomicIndicator.MARKET_CAP, EconomicIndicator.TRADING_VOLUME],
            parameters={
                "volatility_threshold": Decimal('0.1'),
                "circuit_breaker": True,
                "margin_requirements": Decimal('0.1')
            },
            effectiveness=Decimal('0.9'),
            duration=2592000  # 30 dias
        )
        
        self.active_policies = {
            inflation_policy.id: inflation_policy,
            growth_policy.id: growth_policy,
            stability_policy.id: stability_policy
        }
    
    async def start_autonomous_economy(self):
        """Inicia o sistema de economia autônoma"""
        self.is_active = True
        logger.info("🏛️ Sistema de Economia Autônoma iniciado")
        
        # Iniciar monitoramento econômico
        asyncio.create_task(self._monitor_economic_indicators())
        
        # Iniciar análise de políticas
        asyncio.create_task(self._analyze_and_adjust_policies())
        
        # Iniciar ciclos econômicos
        asyncio.create_task(self._manage_economic_cycles())
        
        # Iniciar decisões autônomas
        asyncio.create_task(self._make_economic_decisions())
    
    async def stop_autonomous_economy(self):
        """Para o sistema de economia autônoma"""
        self.is_active = False
        logger.info("🛑 Sistema de Economia Autônoma parado")
    
    async def _monitor_economic_indicators(self):
        """Monitora indicadores econômicos"""
        while self.is_active:
            try:
                # Atualizar indicadores baseados em dados reais
                await self._update_economic_indicators()
                
                # Calcular tendências
                await self._calculate_trends()
                
                # Detectar anomalias
                await self._detect_anomalies()
                
                await asyncio.sleep(300)  # Monitorar a cada 5 minutos
                
            except Exception as e:
                logger.error(f"Erro no monitoramento econômico: {e}")
                await asyncio.sleep(300)
    
    async def _update_economic_indicators(self):
        """Atualiza indicadores econômicos"""
        # Simular atualização baseada em dados de mercado
        for indicator_name, indicator in self.economic_indicators.items():
            # Simular crescimento/declínio baseado na fase atual
            growth_factor = self._get_growth_factor_for_phase()
            
            # Aplicar crescimento com alguma volatilidade
            volatility = Decimal('0.01')  # 1% de volatilidade
            change = growth_factor + Decimal(str(np.random.normal(0, float(volatility))))
            
            # Atualizar valor
            new_value = indicator.value * (Decimal('1') + change)
            indicator.value = max(new_value, Decimal('0.01'))  # Manter positivo
            
            # Atualizar timestamp
            indicator.timestamp = time.time()
            
            logger.debug(f"📊 {indicator_name.value}: {indicator.value} (mudança: {change:.2%})")
    
    def _get_growth_factor_for_phase(self) -> Decimal:
        """Obtém fator de crescimento baseado na fase atual"""
        if self.current_phase == EconomyPhase.GROWTH:
            return Decimal('0.001')  # 0.1% crescimento
        elif self.current_phase == EconomyPhase.STABILITY:
            return Decimal('0.0001')  # 0.01% crescimento
        elif self.current_phase == EconomyPhase.DECLINE:
            return Decimal('-0.0005')  # -0.05% declínio
        elif self.current_phase == EconomyPhase.RECOVERY:
            return Decimal('0.002')  # 0.2% recuperação
        else:  # TRANSFORMATION
            return Decimal('0.003')  # 0.3% transformação
    
    async def _calculate_trends(self):
        """Calcula tendências dos indicadores"""
        for indicator in self.economic_indicators.values():
            # Simplificado - determinar tendência baseada no valor atual vs target
            if indicator.value > indicator.target_value * Decimal('1.1'):
                indicator.trend = "increasing"
                indicator.impact = "positive"
            elif indicator.value < indicator.target_value * Decimal('0.9'):
                indicator.trend = "decreasing"
                indicator.impact = "negative"
            else:
                indicator.trend = "stable"
                indicator.impact = "neutral"
    
    async def _detect_anomalies(self):
        """Detecta anomalias econômicas"""
        anomalies = []
        
        for indicator_name, indicator in self.economic_indicators.items():
            # Detectar valores extremos
            if indicator.value > indicator.target_value * Decimal('2'):
                anomalies.append({
                    "type": "extreme_high",
                    "indicator": indicator_name.value,
                    "value": float(indicator.value),
                    "threshold": float(indicator.target_value * Decimal('2'))
                })
            elif indicator.value < indicator.target_value * Decimal('0.5'):
                anomalies.append({
                    "type": "extreme_low",
                    "indicator": indicator_name.value,
                    "value": float(indicator.value),
                    "threshold": float(indicator.target_value * Decimal('0.5'))
                })
        
        if anomalies:
            logger.warning(f"⚠️ Anomalias detectadas: {len(anomalies)}")
            await self._handle_anomalies(anomalies)
    
    async def _handle_anomalies(self, anomalies: List[Dict[str, Any]]):
        """Trata anomalias econômicas"""
        for anomaly in anomalies:
            if anomaly["type"] == "extreme_high":
                # Implementar política de contenção
                await self._implement_containment_policy(anomaly)
            elif anomaly["type"] == "extreme_low":
                # Implementar política de estímulo
                await self._implement_stimulus_policy(anomaly)
    
    async def _implement_containment_policy(self, anomaly: Dict[str, Any]):
        """Implementa política de contenção"""
        policy_id = f"containment_{anomaly['indicator']}_{int(time.time())}"
        
        policy = EconomicPolicy(
            id=policy_id,
            policy_type=PolicyType.EMERGENCY,
            name=f"Contenção - {anomaly['indicator']}",
            description=f"Política de emergência para conter {anomaly['indicator']}",
            target_indicators=[EconomicIndicator(anomaly['indicator'])],
            parameters={
                "reduction_factor": Decimal('0.1'),
                "duration_hours": 24,
                "monitoring_frequency": 300
            },
            effectiveness=Decimal('0.9'),
            duration=86400  # 24 horas
        )
        
        self.active_policies[policy_id] = policy
        
        logger.info(f"🚨 Política de contenção implementada: {anomaly['indicator']}")
    
    async def _implement_stimulus_policy(self, anomaly: Dict[str, Any]):
        """Implementa política de estímulo"""
        policy_id = f"stimulus_{anomaly['indicator']}_{int(time.time())}"
        
        policy = EconomicPolicy(
            id=policy_id,
            policy_type=PolicyType.EMERGENCY,
            name=f"Estímulo - {anomaly['indicator']}",
            description=f"Política de emergência para estimular {anomaly['indicator']}",
            target_indicators=[EconomicIndicator(anomaly['indicator'])],
            parameters={
                "stimulus_factor": Decimal('0.2'),
                "duration_hours": 48,
                "monitoring_frequency": 300
            },
            effectiveness=Decimal('0.8'),
            duration=172800  # 48 horas
        )
        
        self.active_policies[policy_id] = policy
        
        logger.info(f"🚀 Política de estímulo implementada: {anomaly['indicator']}")
    
    async def _analyze_and_adjust_policies(self):
        """Analisa e ajusta políticas econômicas"""
        while self.is_active:
            try:
                # Analisar efetividade das políticas ativas
                for policy_id, policy in list(self.active_policies.items()):
                    if time.time() - policy.created_at > policy.duration:
                        # Política expirada
                        del self.active_policies[policy_id]
                        logger.info(f"⏰ Política expirada: {policy.name}")
                        continue
                    
                    # Avaliar efetividade
                    effectiveness = await self._evaluate_policy_effectiveness(policy)
                    
                    if effectiveness < Decimal('0.3'):
                        # Política inefetiva - ajustar ou remover
                        await self._adjust_policy(policy)
                
                # Criar novas políticas se necessário
                await self._create_new_policies()
                
                await asyncio.sleep(1800)  # Analisar a cada 30 minutos
                
            except Exception as e:
                logger.error(f"Erro na análise de políticas: {e}")
                await asyncio.sleep(1800)
    
    async def _evaluate_policy_effectiveness(self, policy: EconomicPolicy) -> Decimal:
        """Avalia efetividade de uma política"""
        # Simplificado - calcular baseado nos indicadores alvo
        total_improvement = Decimal('0')
        
        for target_indicator in policy.target_indicators:
            if target_indicator in self.economic_indicators:
                indicator = self.economic_indicators[target_indicator]
                
                # Calcular melhoria em relação ao target
                if indicator.value < indicator.target_value:
                    improvement = indicator.value / indicator.target_value
                else:
                    improvement = indicator.target_value / indicator.value
                
                total_improvement += improvement
        
        # Média ponderada
        avg_improvement = total_improvement / len(policy.target_indicators)
        
        return avg_improvement
    
    async def _adjust_policy(self, policy: EconomicPolicy):
        """Ajusta uma política inefetiva"""
        logger.info(f"🔧 Ajustando política: {policy.name}")
        
        # Aumentar intensidade dos parâmetros
        for param_name, param_value in policy.parameters.items():
            if isinstance(param_value, Decimal):
                if "reduction" in param_name.lower():
                    policy.parameters[param_name] = param_value * Decimal('1.5')
                elif "stimulus" in param_name.lower() or "increase" in param_name.lower():
                    policy.parameters[param_name] = param_value * Decimal('1.5')
        
        # Reduzir efetividade esperada
        policy.effectiveness *= Decimal('0.9')
    
    async def _create_new_policies(self):
        """Cria novas políticas baseadas nas condições atuais"""
        # Analisar indicadores que precisam de atenção
        problematic_indicators = []
        
        for indicator_name, indicator in self.economic_indicators.items():
            if indicator.value < indicator.target_value * Decimal('0.8'):
                problematic_indicators.append(indicator_name)
        
        # Criar políticas para indicadores problemáticos
        for indicator in problematic_indicators:
            policy_id = f"auto_policy_{indicator.value}_{int(time.time())}"
            
            policy = EconomicPolicy(
                id=policy_id,
                policy_type=PolicyType.INCENTIVE,
                name=f"Auto-Política - {indicator.value}",
                description=f"Política automática para melhorar {indicator.value}",
                target_indicators=[indicator],
                parameters={
                    "incentive_rate": Decimal('0.1'),
                    "duration_days": 7,
                    "monitoring_frequency": 600
                },
                effectiveness=Decimal('0.6'),
                duration=604800  # 7 dias
            )
            
            self.active_policies[policy_id] = policy
            
            logger.info(f"🆕 Nova política criada: {policy.name}")
    
    async def _manage_economic_cycles(self):
        """Gerencia ciclos econômicos"""
        while self.is_active:
            try:
                # Determinar fase atual baseada nos indicadores
                new_phase = await self._determine_economic_phase()
                
                if new_phase != self.current_phase:
                    await self._transition_to_phase(new_phase)
                
                await asyncio.sleep(3600)  # Verificar a cada hora
                
            except Exception as e:
                logger.error(f"Erro no gerenciamento de ciclos: {e}")
                await asyncio.sleep(3600)
    
    async def _determine_economic_phase(self) -> EconomyPhase:
        """Determina a fase econômica atual"""
        # Calcular score geral da economia
        total_score = Decimal('0')
        total_weight = Decimal('0')
        
        for indicator in self.economic_indicators.values():
            # Calcular score do indicador (0-1)
            if indicator.value <= Decimal('0'):
                score = Decimal('0')
            else:
                score = min(indicator.value / indicator.target_value, Decimal('2'))
            
            total_score += score * indicator.weight
            total_weight += indicator.weight
        
        avg_score = total_score / total_weight
        
        # Determinar fase baseada no score
        if avg_score > Decimal('1.2'):
            return EconomyPhase.GROWTH
        elif avg_score > Decimal('0.8'):
            return EconomyPhase.STABILITY
        elif avg_score > Decimal('0.6'):
            return EconomyPhase.DECLINE
        elif avg_score > Decimal('0.4'):
            return EconomyPhase.RECOVERY
        else:
            return EconomyPhase.TRANSFORMATION
    
    async def _transition_to_phase(self, new_phase: EconomyPhase):
        """Transição para nova fase econômica"""
        old_phase = self.current_phase
        self.current_phase = new_phase
        
        # Criar novo ciclo econômico
        cycle_id = f"cycle_{int(time.time())}"
        
        cycle = EconomicCycle(
            id=cycle_id,
            phase=new_phase,
            start_time=time.time(),
            duration=86400 * 30,  # 30 dias
            indicators={indicator.name: indicator.value for indicator in self.economic_indicators.values()},
            policies_applied=list(self.active_policies.keys()),
            performance_score=Decimal('0.5')  # Será calculado posteriormente
        )
        
        self.economic_cycles.append(cycle)
        
        # Manter apenas últimos 10 ciclos
        if len(self.economic_cycles) > 10:
            self.economic_cycles = self.economic_cycles[-10:]
        
        logger.info(f"🔄 Transição econômica: {old_phase.value} -> {new_phase.value}")
        
        # Aplicar políticas específicas da nova fase
        await self._apply_phase_specific_policies(new_phase)
    
    async def _apply_phase_specific_policies(self, phase: EconomyPhase):
        """Aplica políticas específicas da fase"""
        if phase == EconomyPhase.GROWTH:
            # Políticas de crescimento sustentável
            await self._create_growth_policies()
        elif phase == EconomyPhase.DECLINE:
            # Políticas de contenção
            await self._create_decline_policies()
        elif phase == EconomyPhase.RECOVERY:
            # Políticas de estímulo
            await self._create_recovery_policies()
        elif phase == EconomyPhase.TRANSFORMATION:
            # Políticas de transformação
            await self._create_transformation_policies()
    
    async def _create_growth_policies(self):
        """Cria políticas de crescimento"""
        policy_id = f"growth_policy_{int(time.time())}"
        
        policy = EconomicPolicy(
            id=policy_id,
            policy_type=PolicyType.FISCAL,
            name="Política de Crescimento Sustentável",
            description="Mantém crescimento equilibrado",
            target_indicators=[EconomicIndicator.GDP, EconomicIndicator.UNEMPLOYMENT],
            parameters={
                "growth_target": Decimal('0.05'),
                "sustainability_factor": Decimal('0.8'),
                "monitoring_frequency": 1800
            },
            effectiveness=Decimal('0.8'),
            duration=2592000  # 30 dias
        )
        
        self.active_policies[policy_id] = policy
        
        logger.info("🌱 Política de crescimento sustentável aplicada")
    
    async def _create_decline_policies(self):
        """Cria políticas de contenção de declínio"""
        policy_id = f"decline_policy_{int(time.time())}"
        
        policy = EconomicPolicy(
            id=policy_id,
            policy_type=PolicyType.EMERGENCY,
            name="Política de Contenção de Declínio",
            description="Contém declínio e prepara recuperação",
            target_indicators=[EconomicIndicator.GDP, EconomicIndicator.UNEMPLOYMENT],
            parameters={
                "decline_limit": Decimal('0.1'),
                "recovery_preparation": True,
                "monitoring_frequency": 900
            },
            effectiveness=Decimal('0.9'),
            duration=1209600  # 14 dias
        )
        
        self.active_policies[policy_id] = policy
        
        logger.info("🛡️ Política de contenção de declínio aplicada")
    
    async def _create_recovery_policies(self):
        """Cria políticas de recuperação"""
        policy_id = f"recovery_policy_{int(time.time())}"
        
        policy = EconomicPolicy(
            id=policy_id,
            policy_type=PolicyType.FISCAL,
            name="Política de Recuperação Econômica",
            description="Estimula recuperação econômica",
            target_indicators=[EconomicIndicator.GDP, EconomicIndicator.UNEMPLOYMENT, EconomicIndicator.MARKET_CAP],
            parameters={
                "stimulus_rate": Decimal('0.15'),
                "recovery_target": Decimal('0.1'),
                "monitoring_frequency": 1200
            },
            effectiveness=Decimal('0.85'),
            duration=1814400  # 21 dias
        )
        
        self.active_policies[policy_id] = policy
        
        logger.info("🚀 Política de recuperação econômica aplicada")
    
    async def _create_transformation_policies(self):
        """Cria políticas de transformação"""
        policy_id = f"transformation_policy_{int(time.time())}"
        
        policy = EconomicPolicy(
            id=policy_id,
            policy_type=PolicyType.REGULATORY,
            name="Política de Transformação Econômica",
            description="Transforma estrutura econômica",
            target_indicators=list(EconomicIndicator),
            parameters={
                "transformation_rate": Decimal('0.2'),
                "structural_changes": True,
                "monitoring_frequency": 600
            },
            effectiveness=Decimal('0.7'),
            duration=2592000  # 30 dias
        )
        
        self.active_policies[policy_id] = policy
        
        logger.info("🔄 Política de transformação econômica aplicada")
    
    async def _make_economic_decisions(self):
        """Faz decisões econômicas autônomas"""
        while self.is_active:
            try:
                # Analisar situação econômica
                economic_health = await self._assess_economic_health()
                
                # Tomar decisões baseadas na saúde econômica
                if economic_health < Decimal('0.3'):
                    await self._make_crisis_decisions()
                elif economic_health < Decimal('0.6'):
                    await self._make_stabilization_decisions()
                else:
                    await self._make_growth_decisions()
                
                await asyncio.sleep(1800)  # Decidir a cada 30 minutos
                
            except Exception as e:
                logger.error(f"Erro nas decisões econômicas: {e}")
                await asyncio.sleep(1800)
    
    async def _assess_economic_health(self) -> Decimal:
        """Avalia saúde econômica geral"""
        total_score = Decimal('0')
        total_weight = Decimal('0')
        
        for indicator in self.economic_indicators.values():
            # Calcular score de saúde (0-1)
            if indicator.value <= Decimal('0'):
                health_score = Decimal('0')
            else:
                health_score = min(indicator.value / indicator.target_value, Decimal('1'))
            
            total_score += health_score * indicator.weight
            total_weight += indicator.weight
        
        return total_score / total_weight
    
    async def _make_crisis_decisions(self):
        """Faz decisões de crise"""
        logger.info("🚨 Tomando decisões de crise econômica")
        
        # Implementar medidas de emergência
        emergency_policy = EconomicPolicy(
            id=f"emergency_crisis_{int(time.time())}",
            policy_type=PolicyType.EMERGENCY,
            name="Medidas de Emergência",
            description="Medidas de emergência para crise econômica",
            target_indicators=list(EconomicIndicator),
            parameters={
                "emergency_funding": Decimal('0.2'),
                "regulatory_relief": True,
                "monitoring_frequency": 300
            },
            effectiveness=Decimal('0.95'),
            duration=86400  # 24 horas
        )
        
        self.active_policies[emergency_policy.id] = emergency_policy
        
        # Registrar decisão
        self.decision_history.append({
            "timestamp": time.time(),
            "type": "crisis_decision",
            "action": "emergency_measures",
            "reasoning": "Saúde econômica crítica detectada",
            "confidence": float(emergency_policy.effectiveness)
        })
    
    async def _make_stabilization_decisions(self):
        """Faz decisões de estabilização"""
        logger.info("⚖️ Tomando decisões de estabilização econômica")
        
        # Implementar medidas de estabilização
        stabilization_policy = EconomicPolicy(
            id=f"stabilization_{int(time.time())}",
            policy_type=PolicyType.MONETARY,
            name="Medidas de Estabilização",
            description="Medidas para estabilizar economia",
            target_indicators=[EconomicIndicator.INFLATION, EconomicIndicator.INTEREST_RATE],
            parameters={
                "interest_rate_adjustment": Decimal('0.01'),
                "monetary_supply_control": True,
                "monitoring_frequency": 600
            },
            effectiveness=Decimal('0.8'),
            duration=172800  # 48 horas
        )
        
        self.active_policies[stabilization_policy.id] = stabilization_policy
        
        # Registrar decisão
        self.decision_history.append({
            "timestamp": time.time(),
            "type": "stabilization_decision",
            "action": "stabilization_measures",
            "reasoning": "Economia instável - medidas de estabilização necessárias",
            "confidence": float(stabilization_policy.effectiveness)
        })
    
    async def _make_growth_decisions(self):
        """Faz decisões de crescimento"""
        logger.info("📈 Tomando decisões de crescimento econômico")
        
        # Implementar medidas de crescimento
        growth_policy = EconomicPolicy(
            id=f"growth_{int(time.time())}",
            policy_type=PolicyType.FISCAL,
            name="Medidas de Crescimento",
            description="Medidas para estimular crescimento",
            target_indicators=[EconomicIndicator.GDP, EconomicIndicator.UNEMPLOYMENT],
            parameters={
                "growth_incentive": Decimal('0.1'),
                "job_creation": True,
                "monitoring_frequency": 1200
            },
            effectiveness=Decimal('0.75'),
            duration=2592000  # 30 dias
        )
        
        self.active_policies[growth_policy.id] = growth_policy
        
        # Registrar decisão
        self.decision_history.append({
            "timestamp": time.time(),
            "type": "growth_decision",
            "action": "growth_measures",
            "reasoning": "Economia saudável - oportunidades de crescimento",
            "confidence": float(growth_policy.effectiveness)
        })
    
    def get_economy_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas da economia"""
        economic_health = sum(
            min(indicator.value / indicator.target_value, Decimal('1')) * indicator.weight
            for indicator in self.economic_indicators.values()
        ) / sum(indicator.weight for indicator in self.economic_indicators.values())
        
        return {
            "system_status": "active" if self.is_active else "stopped",
            "current_phase": self.current_phase.value,
            "economic_health": float(economic_health),
            "indicators": {
                indicator_name.value: {
                    "value": float(indicator.value),
                    "target": float(indicator.target_value),
                    "trend": indicator.trend,
                    "impact": indicator.impact,
                    "weight": float(indicator.weight)
                }
                for indicator_name, indicator in self.economic_indicators.items()
            },
            "policies": {
                "active": len(self.active_policies),
                "total_created": len(self.decision_history),
                "by_type": {
                    policy_type.value: len([p for p in self.active_policies.values() if p.policy_type == policy_type])
                    for policy_type in PolicyType
                }
            },
            "cycles": {
                "current_cycle": self.economic_cycles[-1].id if self.economic_cycles else None,
                "total_cycles": len(self.economic_cycles),
                "phase_history": [cycle.phase.value for cycle in self.economic_cycles[-5:]]
            },
            "decisions": {
                "total": len(self.decision_history),
                "recent": self.decision_history[-5:] if self.decision_history else []
            }
        }


# Instância global do sistema de economia autônoma
autonomous_economy = AutonomousEconomySystem()
