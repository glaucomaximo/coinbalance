"""
Sistema de Distribuição Geográfica de Fractais.

Este módulo implementa um sistema inteligente que:
- Distribui fractais geograficamente para otimizar latência
- Gerencia regiões e zonas de disponibilidade
- Implementa roteamento inteligente baseado em localização
- Otimiza recursos baseado em proximidade geográfica
- Aplica políticas de conformidade regional
"""

import threading
import time
import json
import math
from typing import Dict, Any, Optional, List, Tuple, Union
from decimal import Decimal
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import logging
import random

logger = logging.getLogger(__name__)


class Region(Enum):
    """Regiões geográficas."""
    NORTH_AMERICA = "north_america"
    SOUTH_AMERICA = "south_america"
    EUROPE = "europe"
    ASIA = "asia"
    AFRICA = "africa"
    OCEANIA = "oceania"
    ANTARCTICA = "antarctica"


class AvailabilityZone(Enum):
    """Zonas de disponibilidade."""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    DISASTER_RECOVERY = "disaster_recovery"
    EDGE = "edge"


@dataclass
class GeographicLocation:
    """Localização geográfica."""
    latitude: float
    longitude: float
    region: Region
    country: str
    city: str
    timezone: str
    availability_zone: AvailabilityZone = AvailabilityZone.PRIMARY
    
    def distance_to(self, other: 'GeographicLocation') -> float:
        """Calcula distância em quilômetros usando fórmula de Haversine."""
        try:
            R = 6371  # Raio da Terra em km
            
            lat1_rad = math.radians(self.latitude)
            lat2_rad = math.radians(other.latitude)
            delta_lat = math.radians(other.latitude - self.latitude)
            delta_lon = math.radians(other.longitude - self.longitude)
            
            a = (math.sin(delta_lat / 2) ** 2 + 
                 math.cos(lat1_rad) * math.cos(lat2_rad) * 
                 math.sin(delta_lon / 2) ** 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            
            return R * c
            
        except Exception as e:
            logger.error(f"Erro no cálculo de distância: {e}")
            return 0.0
    
    def latency_estimate(self, other: 'GeographicLocation') -> float:
        """Estima latência baseada na distância."""
        distance = self.distance_to(other)
        # Estimativa: 1ms por 100km + latência base de 10ms
        return (distance / 100) + 10


@dataclass
class FractalLocation:
    """Localização de um fractal."""
    fractal_id: str
    location: GeographicLocation
    capacity: int = 1000
    current_load: int = 0
    is_active: bool = True
    last_heartbeat: float = field(default_factory=time.time)
    consciousness_level: Decimal = Decimal('0.5')
    
    def get_load_percentage(self) -> float:
        """Retorna porcentagem de carga."""
        return (self.current_load / self.capacity) * 100 if self.capacity > 0 else 0
    
    def is_healthy(self) -> bool:
        """Verifica se fractal está saudável."""
        return (self.is_active and 
                time.time() - self.last_heartbeat < 300 and  # 5 minutos
                self.get_load_percentage() < 95)


@dataclass
class RoutingRule:
    """Regra de roteamento geográfico."""
    rule_id: str
    source_region: Optional[Region]
    target_region: Optional[Region]
    priority: int
    max_latency: float = 100.0  # ms
    min_capacity: int = 100
    enabled: bool = True
    consciousness_level: Decimal = Decimal('0.5')


class GeographicFractalDistributor:
    """
    Sistema de Distribuição Geográfica de Fractais.
    
    Características:
    - Distribuição geográfica inteligente
    - Roteamento baseado em localização
    - Otimização de latência
    - Conformidade regional
    - Balanceamento geográfico
    """
    
    def __init__(self):
        self.fractal_locations: Dict[str, FractalLocation] = {}
        self.routing_rules: List[RoutingRule] = []
        self.region_stats: Dict[Region, Dict[str, Any]] = {}
        self.latency_matrix: Dict[Tuple[str, str], float] = {}
        self._lock = threading.RLock()
        
        self.stats = {
            'total_fractals': 0,
            'active_fractals': 0,
            'regions_covered': 0,
            'average_latency': 0.0,
            'consciousness_level': Decimal('0.1'),
            'routing_decisions': 0,
            'latency_optimizations': 0
        }
        
        self._initialize_regions()
        self._initialize_routing_rules()
        logger.info("GeographicFractalDistributor inicializado")
    
    def _initialize_regions(self):
        """Inicializa estatísticas das regiões."""
        for region in Region:
            self.region_stats[region] = {
                'fractal_count': 0,
                'total_capacity': 0,
                'current_load': 0,
                'average_latency': 0.0,
                'consciousness_level': Decimal('0.1'),
                'last_update': time.time()
            }
    
    def _initialize_routing_rules(self):
        """Inicializa regras de roteamento padrão."""
        # Regra de baixa latência
        self.routing_rules.append(RoutingRule(
            rule_id="low_latency",
            source_region=None,
            target_region=None,
            priority=1,
            max_latency=50.0,
            min_capacity=50,
            consciousness_level=Decimal('0.8')
        ))
        
        # Regra de alta capacidade
        self.routing_rules.append(RoutingRule(
            rule_id="high_capacity",
            source_region=None,
            target_region=None,
            priority=2,
            max_latency=200.0,
            min_capacity=500,
            consciousness_level=Decimal('0.7')
        ))
        
        # Regra de disaster recovery
        self.routing_rules.append(RoutingRule(
            rule_id="disaster_recovery",
            source_region=None,
            target_region=None,
            priority=3,
            max_latency=500.0,
            min_capacity=100,
            consciousness_level=Decimal('0.6')
        ))
    
    def register_fractal(self, fractal_id: str, location: GeographicLocation, 
                       capacity: int = 1000) -> bool:
        """Registra um fractal em uma localização geográfica."""
        try:
            with self._lock:
                fractal_location = FractalLocation(
                    fractal_id=fractal_id,
                    location=location,
                    capacity=capacity
                )
                
                self.fractal_locations[fractal_id] = fractal_location
                
                # Atualizar estatísticas da região
                region_stats = self.region_stats[location.region]
                region_stats['fractal_count'] += 1
                region_stats['total_capacity'] += capacity
                region_stats['last_update'] = time.time()
                
                # Atualizar estatísticas globais
                self.stats['total_fractals'] += 1
                self.stats['active_fractals'] += 1
                
                # Calcular regiões cobertas
                self.stats['regions_covered'] = len([
                    region for region, stats in self.region_stats.items()
                    if stats['fractal_count'] > 0
                ])
                
                logger.info(f"Fractal {fractal_id} registrado em {location.city}, {location.country}")
                return True
                
        except Exception as e:
            logger.error(f"Erro no registro do fractal {fractal_id}: {e}")
            return False
    
    def update_fractal_load(self, fractal_id: str, load: int) -> bool:
        """Atualiza carga de um fractal."""
        try:
            with self._lock:
                if fractal_id not in self.fractal_locations:
                    return False
                
                fractal_location = self.fractal_locations[fractal_id]
                old_load = fractal_location.current_load
                fractal_location.current_load = load
                fractal_location.last_heartbeat = time.time()
                
                # Atualizar estatísticas da região
                region_stats = self.region_stats[fractal_location.location.region]
                region_stats['current_load'] += (load - old_load)
                
                logger.debug(f"Carga do fractal {fractal_id} atualizada: {load}")
                return True
                
        except Exception as e:
            logger.error(f"Erro na atualização de carga do fractal {fractal_id}: {e}")
            return False
    
    def find_optimal_fractal(self, user_location: GeographicLocation, 
                           requirements: Dict[str, Any]) -> Optional[str]:
        """
        Encontra fractal ótimo baseado na localização do usuário.
        
        Args:
            user_location: Localização do usuário
            requirements: Requisitos (latência, capacidade, etc.)
            
        Returns:
            ID do fractal ótimo ou None
        """
        try:
            with self._lock:
                max_latency = requirements.get('max_latency', 100.0)
                min_capacity = requirements.get('min_capacity', 100)
                preferred_region = requirements.get('preferred_region')
                
                candidates = []
                
                for fractal_id, fractal_location in self.fractal_locations.items():
                    if not fractal_location.is_healthy():
                        continue
                    
                    # Verificar capacidade
                    if fractal_location.current_load + min_capacity > fractal_location.capacity:
                        continue
                    
                    # Calcular latência
                    latency = user_location.latency_estimate(fractal_location.location)
                    if latency > max_latency:
                        continue
                    
                    # Verificar região preferida
                    if preferred_region and fractal_location.location.region != preferred_region:
                        continue
                    
                    # Calcular score de adequação
                    capacity_score = (fractal_location.capacity - fractal_location.current_load) / fractal_location.capacity
                    latency_score = max(0.0, 1.0 - (latency / max_latency))
                    consciousness_score = float(fractal_location.consciousness_level)
                    
                    # Score composto
                    fitness_score = (capacity_score * 0.4 + latency_score * 0.4 + consciousness_score * 0.2)
                    
                    candidates.append((fractal_id, fitness_score, latency))
                
                if not candidates:
                    return None
                
                # Ordenar por score de adequação
                candidates.sort(key=lambda x: x[1], reverse=True)
                
                # Selecionar melhor candidato
                best_fractal_id = candidates[0][0]
                
                # Atualizar estatísticas
                self.stats['routing_decisions'] += 1
                
                logger.debug(f"Fractal ótimo selecionado: {best_fractal_id} "
                           f"(score: {candidates[0][1]:.3f}, latência: {candidates[0][2]:.1f}ms)")
                
                return best_fractal_id
                
        except Exception as e:
            logger.error(f"Erro na busca de fractal ótimo: {e}")
            return None
    
    def get_region_performance(self, region: Region) -> Dict[str, Any]:
        """Retorna performance de uma região."""
        try:
            with self._lock:
                region_stats = self.region_stats[region]
                
                # Encontrar fractais da região
                region_fractals = [
                    fl for fl in self.fractal_locations.values()
                    if fl.location.region == region
                ]
                
                if not region_fractals:
                    return {'error': 'Nenhum fractal encontrado na região'}
                
                # Calcular métricas
                total_capacity = sum(f.capacity for f in region_fractals)
                total_load = sum(f.current_load for f in region_fractals)
                active_fractals = sum(1 for f in region_fractals if f.is_healthy())
                
                # Calcular latência média entre fractais da região
                latencies = []
                for i, f1 in enumerate(region_fractals):
                    for f2 in region_fractals[i+1:]:
                        latency = f1.location.latency_estimate(f2.location)
                        latencies.append(latency)
                
                average_latency = statistics.mean(latencies) if latencies else 0.0
                
                return {
                    'region': region.value,
                    'fractal_count': len(region_fractals),
                    'active_fractals': active_fractals,
                    'total_capacity': total_capacity,
                    'current_load': total_load,
                    'load_percentage': (total_load / total_capacity) * 100 if total_capacity > 0 else 0,
                    'average_latency': average_latency,
                    'consciousness_level': float(region_stats['consciousness_level'])
                }
                
        except Exception as e:
            logger.error(f"Erro na obtenção de performance da região: {e}")
            return {'error': str(e)}
    
    def optimize_geographic_distribution(self) -> Dict[str, Any]:
        """Otimiza distribuição geográfica dos fractais."""
        try:
            with self._lock:
                optimization_stats = {
                    'fractals_rebalanced': 0,
                    'latency_improvements': 0,
                    'consciousness_improvement': Decimal('0.0'),
                    'timestamp': time.time()
                }
                
                # Identificar regiões sobrecarregadas
                overloaded_regions = []
                underloaded_regions = []
                
                for region, stats in self.region_stats.items():
                    if stats['fractal_count'] > 0:
                        load_percentage = (stats['current_load'] / stats['total_capacity']) * 100
                        
                        if load_percentage > 80:
                            overloaded_regions.append(region)
                        elif load_percentage < 30:
                            underloaded_regions.append(region)
                
                # Sugerir redistribuição
                redistribution_suggestions = []
                for overloaded_region in overloaded_regions:
                    for underloaded_region in underloaded_regions:
                        # Encontrar fractais que podem ser movidos
                        overloaded_fractals = [
                            fl for fl in self.fractal_locations.values()
                            if (fl.location.region == overloaded_region and 
                                fl.get_load_percentage() > 70)
                        ]
                        
                        if overloaded_fractals:
                            suggestion = {
                                'from_region': overloaded_region.value,
                                'to_region': underloaded_region.value,
                                'fractal_count': len(overloaded_fractals),
                                'expected_latency_reduction': self._estimate_latency_reduction(
                                    overloaded_region, underloaded_region
                                )
                            }
                            redistribution_suggestions.append(suggestion)
                
                optimization_stats['redistribution_suggestions'] = redistribution_suggestions
                
                # Otimizar regras de roteamento
                self._optimize_routing_rules()
                
                # Aumentar consciência
                old_consciousness = self.stats['consciousness_level']
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.02')
                )
                optimization_stats['consciousness_improvement'] = (
                    self.stats['consciousness_level'] - old_consciousness
                )
                
                logger.info(f"Distribuição geográfica otimizada: {len(redistribution_suggestions)} sugestões")
                return optimization_stats
                
        except Exception as e:
            logger.error(f"Erro na otimização da distribuição geográfica: {e}")
            return {'error': str(e)}
    
    def _estimate_latency_reduction(self, from_region: Region, to_region: Region) -> float:
        """Estima redução de latência com redistribuição."""
        try:
            # Simular redução baseada na distância entre regiões
            region_distances = {
                (Region.NORTH_AMERICA, Region.EUROPE): 50.0,
                (Region.EUROPE, Region.ASIA): 40.0,
                (Region.ASIA, Region.NORTH_AMERICA): 60.0,
                (Region.SOUTH_AMERICA, Region.NORTH_AMERICA): 20.0,
                (Region.AFRICA, Region.EUROPE): 30.0,
                (Region.OCEANIA, Region.ASIA): 25.0,
            }
            
            # Buscar distância entre regiões
            distance = region_distances.get((from_region, to_region), 0.0)
            if distance == 0.0:
                distance = region_distances.get((to_region, from_region), 0.0)
            
            return distance
            
        except:
            return 0.0
    
    def _optimize_routing_rules(self):
        """Otimiza regras de roteamento."""
        try:
            for rule in self.routing_rules:
                # Ajustar latência máxima baseada na performance atual
                if rule.max_latency > 200:
                    rule.max_latency *= 0.95  # Reduzir gradualmente
                elif rule.max_latency < 50:
                    rule.max_latency *= 1.05  # Aumentar gradualmente
                
                # Ajustar capacidade mínima
                if rule.min_capacity > 1000:
                    rule.min_capacity = int(rule.min_capacity * 0.9)
                elif rule.min_capacity < 50:
                    rule.min_capacity = int(rule.min_capacity * 1.1)
                
                # Aumentar consciência da regra
                rule.consciousness_level = min(
                    Decimal('1.0'),
                    rule.consciousness_level + Decimal('0.01')
                )
                
        except Exception as e:
            logger.error(f"Erro na otimização das regras de roteamento: {e}")
    
    def get_geographic_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas geográficas."""
        with self._lock:
            # Estatísticas por região
            region_performance = {}
            for region in Region:
                region_performance[region.value] = self.get_region_performance(region)
            
            # Estatísticas globais
            total_capacity = sum(stats['total_capacity'] for stats in self.region_stats.values())
            total_load = sum(stats['current_load'] for stats in self.region_stats.values())
            
            return {
                'total_fractals': self.stats['total_fractals'],
                'active_fractals': self.stats['active_fractals'],
                'regions_covered': self.stats['regions_covered'],
                'total_capacity': total_capacity,
                'total_load': total_load,
                'global_load_percentage': (total_load / total_capacity) * 100 if total_capacity > 0 else 0,
                'consciousness_level': float(self.stats['consciousness_level']),
                'routing_decisions': self.stats['routing_decisions'],
                'latency_optimizations': self.stats['latency_optimizations'],
                'region_performance': region_performance,
                'routing_rules': [
                    {
                        'rule_id': rule.rule_id,
                        'priority': rule.priority,
                        'max_latency': rule.max_latency,
                        'min_capacity': rule.min_capacity,
                        'enabled': rule.enabled,
                        'consciousness_level': float(rule.consciousness_level)
                    }
                    for rule in self.routing_rules
                ]
            }


# Instância global do distribuidor geográfico
geographic_fractal_distributor = GeographicFractalDistributor()
