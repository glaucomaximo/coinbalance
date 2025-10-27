"""
Sistema de Otimização Genética de Fractais.

Este módulo implementa um sistema de algoritmos genéticos que:
- Evolui fractais através de seleção natural
- Otimiza parâmetros baseado em fitness
- Implementa crossover e mutação inteligentes
- Aplica seleção consciente baseada em consciência
- Gera fractais superiores através de evolução
"""

import random
import threading
import time
import json
import hashlib
from typing import Dict, Any, Optional, List, Tuple, Union
from decimal import Decimal
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import logging
import copy
import statistics

logger = logging.getLogger(__name__)


class OptimizationObjective(Enum):
    """Objetivos de otimização."""
    PERFORMANCE = "performance"
    EFFICIENCY = "efficiency"
    CONSCIOUSNESS = "consciousness"
    SCALABILITY = "scalability"
    RELIABILITY = "reliability"
    COMPOSITE = "composite"


class SelectionMethod(Enum):
    """Métodos de seleção genética."""
    ROULETTE_WHEEL = "roulette_wheel"
    TOURNAMENT = "tournament"
    RANK_SELECTION = "rank_selection"
    CONSCIOUSNESS_SELECTION = "consciousness_selection"


@dataclass
class FractalGene:
    """Gene de um fractal."""
    gene_id: str
    parameter_name: str
    value: Any
    min_value: Any = None
    max_value: Any = None
    mutation_rate: float = 0.1
    consciousness_level: Decimal = Decimal('0.5')
    
    def mutate(self, mutation_strength: float = 0.1) -> 'FractalGene':
        """Aplica mutação ao gene."""
        try:
            new_gene = copy.deepcopy(self)
            
            if isinstance(self.value, (int, float)):
                # Mutação numérica
                if self.min_value is not None and self.max_value is not None:
                    range_size = self.max_value - self.min_value
                    mutation_amount = range_size * mutation_strength * random.uniform(-1, 1)
                    new_value = self.value + mutation_amount
                    new_value = max(self.min_value, min(self.max_value, new_value))
                    new_gene.value = new_value
                else:
                    # Mutação sem limites
                    mutation_amount = abs(self.value) * mutation_strength * random.uniform(-1, 1)
                    new_gene.value = self.value + mutation_amount
            
            elif isinstance(self.value, bool):
                # Mutação booleana
                if random.random() < mutation_strength:
                    new_gene.value = not self.value
            
            elif isinstance(self.value, str):
                # Mutação de string (substituir caractere)
                if random.random() < mutation_strength and len(self.value) > 0:
                    chars = list(self.value)
                    pos = random.randint(0, len(chars) - 1)
                    chars[pos] = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                    new_gene.value = ''.join(chars)
            
            elif isinstance(self.value, list):
                # Mutação de lista
                if random.random() < mutation_strength and len(self.value) > 0:
                    new_list = self.value.copy()
                    if random.random() < 0.5:
                        # Adicionar elemento
                        if len(new_list) < 10:  # Limite máximo
                            new_list.append(random.randint(0, 100))
                    else:
                        # Remover elemento
                        if len(new_list) > 1:
                            new_list.pop(random.randint(0, len(new_list) - 1))
                    new_gene.value = new_list
            
            # Aumentar consciência com mutação
            new_gene.consciousness_level = min(
                Decimal('1.0'),
                self.consciousness_level + Decimal('0.01')
            )
            
            return new_gene
            
        except Exception as e:
            logger.error(f"Erro na mutação do gene {self.gene_id}: {e}")
            return self


@dataclass
class FractalGenome:
    """Genoma de um fractal."""
    genome_id: str
    fractal_id: str
    genes: Dict[str, FractalGene]
    fitness_score: float = 0.0
    consciousness_level: Decimal = Decimal('0.5')
    generation: int = 0
    parent_genomes: List[str] = field(default_factory=list)
    creation_time: float = field(default_factory=time.time)
    
    def get_genome_hash(self) -> str:
        """Calcula hash do genoma."""
        genome_data = {
            'genes': {gene_id: gene.value for gene_id, gene in self.genes.items()},
            'generation': self.generation
        }
        return hashlib.md5(json.dumps(genome_data, sort_keys=True).encode()).hexdigest()[:16]
    
    def calculate_fitness(self, objective: OptimizationObjective, 
                        performance_metrics: Dict[str, float]) -> float:
        """Calcula fitness do genoma."""
        try:
            if objective == OptimizationObjective.PERFORMANCE:
                # Fitness baseado em performance
                cpu_efficiency = 1.0 - performance_metrics.get('cpu_usage', 0.5)
                memory_efficiency = 1.0 - performance_metrics.get('memory_usage', 0.5)
                response_time_score = max(0.0, 1.0 - (performance_metrics.get('response_time', 100) / 1000))
                
                fitness = (cpu_efficiency + memory_efficiency + response_time_score) / 3
                
            elif objective == OptimizationObjective.CONSCIOUSNESS:
                # Fitness baseado em consciência
                consciousness_score = float(self.consciousness_level)
                gene_consciousness = sum(float(gene.consciousness_level) for gene in self.genes.values()) / len(self.genes)
                
                fitness = (consciousness_score + gene_consciousness) / 2
                
            elif objective == OptimizationObjective.EFFICIENCY:
                # Fitness baseado em eficiência
                throughput = performance_metrics.get('throughput', 1000) / 10000  # Normalizar
                error_rate = 1.0 - performance_metrics.get('error_rate', 0.1)
                resource_usage = 1.0 - (performance_metrics.get('cpu_usage', 0.5) + 
                                      performance_metrics.get('memory_usage', 0.5)) / 2
                
                fitness = (throughput + error_rate + resource_usage) / 3
                
            elif objective == OptimizationObjective.SCALABILITY:
                # Fitness baseado em escalabilidade
                load_handling = performance_metrics.get('load_capacity', 0.5)
                scaling_efficiency = performance_metrics.get('scaling_efficiency', 0.5)
                resource_scalability = 1.0 - performance_metrics.get('resource_waste', 0.3)
                
                fitness = (load_handling + scaling_efficiency + resource_scalability) / 3
                
            elif objective == OptimizationObjective.RELIABILITY:
                # Fitness baseado em confiabilidade
                uptime = performance_metrics.get('uptime', 0.9)
                error_tolerance = 1.0 - performance_metrics.get('error_rate', 0.1)
                recovery_time = max(0.0, 1.0 - (performance_metrics.get('recovery_time', 60) / 300))
                
                fitness = (uptime + error_tolerance + recovery_time) / 3
                
            else:  # COMPOSITE
                # Fitness composto considerando múltiplos objetivos
                objectives = [
                    OptimizationObjective.PERFORMANCE,
                    OptimizationObjective.CONSCIOUSNESS,
                    OptimizationObjective.EFFICIENCY,
                    OptimizationObjective.SCALABILITY,
                    OptimizationObjective.RELIABILITY
                ]
                
                fitness_scores = []
                for obj in objectives:
                    score = self.calculate_fitness(obj, performance_metrics)
                    fitness_scores.append(score)
                
                fitness = statistics.mean(fitness_scores)
            
            # Ajustar pela consciência do genoma
            consciousness_factor = float(self.consciousness_level)
            final_fitness = fitness * (0.7 + 0.3 * consciousness_factor)
            
            self.fitness_score = min(final_fitness, 1.0)
            return self.fitness_score
            
        except Exception as e:
            logger.error(f"Erro no cálculo de fitness: {e}")
            return 0.0
    
    def crossover(self, other: 'FractalGenome', crossover_rate: float = 0.8) -> Tuple['FractalGenome', 'FractalGenome']:
        """Realiza crossover com outro genoma."""
        try:
            if random.random() > crossover_rate:
                return copy.deepcopy(self), copy.deepcopy(other)
            
            # Criar novos genomas
            child1_genes = {}
            child2_genes = {}
            
            for gene_id in self.genes:
                if gene_id in other.genes:
                    # Crossover de genes
                    if random.random() < 0.5:
                        child1_genes[gene_id] = copy.deepcopy(self.genes[gene_id])
                        child2_genes[gene_id] = copy.deepcopy(other.genes[gene_id])
                    else:
                        child1_genes[gene_id] = copy.deepcopy(other.genes[gene_id])
                        child2_genes[gene_id] = copy.deepcopy(self.genes[gene_id])
                else:
                    # Gene único, copiar para ambos
                    child1_genes[gene_id] = copy.deepcopy(self.genes[gene_id])
                    child2_genes[gene_id] = copy.deepcopy(self.genes[gene_id])
            
            # Criar novos genomas
            child1_id = f"genome_{int(time.time() * 1000)}_1"
            child2_id = f"genome_{int(time.time() * 1000)}_2"
            
            child1 = FractalGenome(
                genome_id=child1_id,
                fractal_id=self.fractal_id,
                genes=child1_genes,
                generation=max(self.generation, other.generation) + 1,
                parent_genomes=[self.genome_id, other.genome_id],
                consciousness_level=(self.consciousness_level + other.consciousness_level) / 2
            )
            
            child2 = FractalGenome(
                genome_id=child2_id,
                fractal_id=self.fractal_id,
                genes=child2_genes,
                generation=max(self.generation, other.generation) + 1,
                parent_genomes=[self.genome_id, other.genome_id],
                consciousness_level=(self.consciousness_level + other.consciousness_level) / 2
            )
            
            return child1, child2
            
        except Exception as e:
            logger.error(f"Erro no crossover: {e}")
            return copy.deepcopy(self), copy.deepcopy(other)


class FractalGeneticOptimizer:
    """
    Sistema de Otimização Genética de Fractais.
    
    Características:
    - Evolução de fractais através de algoritmos genéticos
    - Seleção consciente baseada em fitness
    - Crossover e mutação inteligentes
    - Múltiplos objetivos de otimização
    - Adaptação contínua dos parâmetros
    """
    
    def __init__(self, population_size: int = 50, elite_size: int = 10):
        self.population_size = population_size
        self.elite_size = elite_size
        self.population: List[FractalGenome] = []
        self.generation_history: deque = deque(maxlen=100)
        self.best_genomes: deque = deque(maxlen=20)
        self._lock = threading.RLock()
        
        self.stats = {
            'current_generation': 0,
            'total_generations': 0,
            'best_fitness': 0.0,
            'average_fitness': 0.0,
            'consciousness_level': Decimal('0.1'),
            'optimization_objective': OptimizationObjective.COMPOSITE,
            'selection_method': SelectionMethod.CONSCIOUSNESS_SELECTION,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'convergence_generations': 0
        }
        
        logger.info(f"FractalGeneticOptimizer inicializado (população: {population_size})")
    
    def initialize_population(self, fractal_id: str, gene_templates: Dict[str, Dict[str, Any]]):
        """Inicializa população inicial de genomas."""
        try:
            with self._lock:
                self.population.clear()
                
                for i in range(self.population_size):
                    genes = {}
                    
                    for gene_name, template in gene_templates.items():
                        gene_id = f"{fractal_id}_{gene_name}_{i}"
                        
                        # Gerar valor aleatório baseado no template
                        if template['type'] == 'int':
                            value = random.randint(template['min'], template['max'])
                        elif template['type'] == 'float':
                            value = random.uniform(template['min'], template['max'])
                        elif template['type'] == 'bool':
                            value = random.choice([True, False])
                        elif template['type'] == 'str':
                            value = random.choice(template['options'])
                        elif template['type'] == 'list':
                            value = [random.randint(0, 100) for _ in range(random.randint(1, 5))]
                        else:
                            value = template.get('default', 0)
                        
                        gene = FractalGene(
                            gene_id=gene_id,
                            parameter_name=gene_name,
                            value=value,
                            min_value=template.get('min'),
                            max_value=template.get('max'),
                            mutation_rate=template.get('mutation_rate', 0.1)
                        )
                        
                        genes[gene_name] = gene
                    
                    genome = FractalGenome(
                        genome_id=f"genome_{fractal_id}_{i}",
                        fractal_id=fractal_id,
                        genes=genes,
                        generation=0
                    )
                    
                    self.population.append(genome)
                
                self.stats['current_generation'] = 0
                logger.info(f"População inicializada com {len(self.population)} genomas")
                
        except Exception as e:
            logger.error(f"Erro na inicialização da população: {e}")
    
    def evaluate_population(self, performance_metrics: Dict[str, float]):
        """Avalia fitness de toda a população."""
        try:
            with self._lock:
                for genome in self.population:
                    genome.calculate_fitness(self.stats['optimization_objective'], performance_metrics)
                
                # Ordenar população por fitness
                self.population.sort(key=lambda x: x.fitness_score, reverse=True)
                
                # Atualizar estatísticas
                self.stats['best_fitness'] = self.population[0].fitness_score
                self.stats['average_fitness'] = sum(g.fitness_score for g in self.population) / len(self.population)
                
                # Adicionar melhor genoma ao histórico
                if not self.best_genomes or self.population[0].fitness_score > self.best_genomes[0].fitness_score:
                    self.best_genomes.appendleft(copy.deepcopy(self.population[0]))
                
                logger.debug(f"População avaliada - Melhor fitness: {self.stats['best_fitness']:.3f}")
                
        except Exception as e:
            logger.error(f"Erro na avaliação da população: {e}")
    
    def select_parents(self, num_parents: int = 2) -> List[FractalGenome]:
        """Seleciona pais para reprodução."""
        try:
            with self._lock:
                if self.stats['selection_method'] == SelectionMethod.ROULETTE_WHEEL:
                    return self._roulette_wheel_selection(num_parents)
                elif self.stats['selection_method'] == SelectionMethod.TOURNAMENT:
                    return self._tournament_selection(num_parents)
                elif self.stats['selection_method'] == SelectionMethod.RANK_SELECTION:
                    return self._rank_selection(num_parents)
                else:  # CONSCIOUSNESS_SELECTION
                    return self._consciousness_selection(num_parents)
                    
        except Exception as e:
            logger.error(f"Erro na seleção de pais: {e}")
            return self.population[:num_parents]  # Fallback
    
    def _roulette_wheel_selection(self, num_parents: int) -> List[FractalGenome]:
        """Seleção por roleta."""
        total_fitness = sum(g.fitness_score for g in self.population)
        if total_fitness == 0:
            return random.sample(self.population, min(num_parents, len(self.population)))
        
        parents = []
        for _ in range(num_parents):
            pick = random.uniform(0, total_fitness)
            current = 0
            for genome in self.population:
                current += genome.fitness_score
                if current >= pick:
                    parents.append(genome)
                    break
        
        return parents
    
    def _tournament_selection(self, num_parents: int, tournament_size: int = 3) -> List[FractalGenome]:
        """Seleção por torneio."""
        parents = []
        for _ in range(num_parents):
            tournament = random.sample(self.population, min(tournament_size, len(self.population)))
            winner = max(tournament, key=lambda x: x.fitness_score)
            parents.append(winner)
        
        return parents
    
    def _rank_selection(self, num_parents: int) -> List[FractalGenome]:
        """Seleção por ranking."""
        # Ordenar por fitness
        sorted_population = sorted(self.population, key=lambda x: x.fitness_score, reverse=True)
        
        # Calcular probabilidades baseadas no ranking
        n = len(sorted_population)
        probabilities = [(2 * (n - i + 1)) / (n * (n + 1)) for i in range(1, n + 1)]
        
        parents = []
        for _ in range(num_parents):
            pick = random.random()
            current = 0
            for i, prob in enumerate(probabilities):
                current += prob
                if current >= pick:
                    parents.append(sorted_population[i])
                    break
        
        return parents
    
    def _consciousness_selection(self, num_parents: int) -> List[FractalGenome]:
        """Seleção baseada em consciência."""
        # Combinar fitness e consciência
        scores = []
        for genome in self.population:
            fitness_score = genome.fitness_score
            consciousness_score = float(genome.consciousness_level)
            combined_score = fitness_score * 0.7 + consciousness_score * 0.3
            scores.append(combined_score)
        
        total_score = sum(scores)
        if total_score == 0:
            return random.sample(self.population, min(num_parents, len(self.population)))
        
        parents = []
        for _ in range(num_parents):
            pick = random.uniform(0, total_score)
            current = 0
            for i, score in enumerate(scores):
                current += score
                if current >= pick:
                    parents.append(self.population[i])
                    break
        
        return parents
    
    def evolve_generation(self, performance_metrics: Dict[str, float]) -> Dict[str, Any]:
        """Evolui uma geração completa."""
        try:
            with self._lock:
                # Avaliar população atual
                self.evaluate_population(performance_metrics)
                
                # Criar nova população
                new_population = []
                
                # Manter elite
                elite = self.population[:self.elite_size]
                new_population.extend(elite)
                
                # Gerar descendentes
                while len(new_population) < self.population_size:
                    parents = self.select_parents(2)
                    if len(parents) >= 2:
                        child1, child2 = parents[0].crossover(parents[1], self.stats['crossover_rate'])
                        
                        # Aplicar mutação
                        child1 = self._mutate_genome(child1)
                        child2 = self._mutate_genome(child2)
                        
                        new_population.extend([child1, child2])
                    else:
                        # Fallback: adicionar genoma aleatório
                        new_population.append(random.choice(self.population))
                
                # Limitar população
                new_population = new_population[:self.population_size]
                
                # Substituir população
                self.population = new_population
                self.stats['current_generation'] += 1
                self.stats['total_generations'] += 1
                
                # Registrar geração no histórico
                generation_stats = {
                    'generation': self.stats['current_generation'],
                    'best_fitness': self.stats['best_fitness'],
                    'average_fitness': self.stats['average_fitness'],
                    'consciousness_level': float(self.stats['consciousness_level']),
                    'timestamp': time.time()
                }
                self.generation_history.append(generation_stats)
                
                # Verificar convergência
                convergence = self._check_convergence()
                
                # Aumentar consciência
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.01')
                )
                
                logger.info(f"Geração {self.stats['current_generation']} evoluída - "
                           f"Melhor fitness: {self.stats['best_fitness']:.3f}")
                
                return {
                    'generation': self.stats['current_generation'],
                    'best_fitness': self.stats['best_fitness'],
                    'average_fitness': self.stats['average_fitness'],
                    'convergence': convergence,
                    'consciousness_level': float(self.stats['consciousness_level'])
                }
                
        except Exception as e:
            logger.error(f"Erro na evolução da geração: {e}")
            return {'error': str(e)}
    
    def _mutate_genome(self, genome: FractalGenome) -> FractalGenome:
        """Aplica mutação a um genoma."""
        try:
            mutated_genes = {}
            
            for gene_id, gene in genome.genes.items():
                if random.random() < self.stats['mutation_rate']:
                    mutated_gene = gene.mutate(self.stats['mutation_rate'])
                    mutated_genes[gene_id] = mutated_gene
                else:
                    mutated_genes[gene_id] = copy.deepcopy(gene)
            
            mutated_genome = FractalGenome(
                genome_id=f"{genome.genome_id}_mutated_{int(time.time() * 1000)}",
                fractal_id=genome.fractal_id,
                genes=mutated_genes,
                generation=genome.generation,
                parent_genomes=genome.parent_genomes.copy(),
                consciousness_level=genome.consciousness_level
            )
            
            return mutated_genome
            
        except Exception as e:
            logger.error(f"Erro na mutação do genoma: {e}")
            return genome
    
    def _check_convergence(self) -> bool:
        """Verifica se o algoritmo convergiu."""
        try:
            if len(self.generation_history) < 10:
                return False
            
            # Verificar se fitness não melhorou nas últimas 10 gerações
            recent_generations = list(self.generation_history)[-10:]
            best_fitness_values = [gen['best_fitness'] for gen in recent_generations]
            
            # Calcular variância do melhor fitness
            if len(best_fitness_values) > 1:
                variance = statistics.variance(best_fitness_values)
                if variance < 0.001:  # Convergência se variância muito baixa
                    self.stats['convergence_generations'] += 1
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erro na verificação de convergência: {e}")
            return False
    
    def get_best_genome(self) -> Optional[FractalGenome]:
        """Retorna o melhor genoma da população atual."""
        with self._lock:
            if self.population:
                return max(self.population, key=lambda x: x.fitness_score)
            return None
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de otimização."""
        with self._lock:
            # Estatísticas por geração
            generation_stats = []
            for gen in list(self.generation_history)[-20:]:  # Últimas 20 gerações
                generation_stats.append({
                    'generation': gen['generation'],
                    'best_fitness': gen['best_fitness'],
                    'average_fitness': gen['average_fitness'],
                    'consciousness_level': gen['consciousness_level']
                })
            
            # Estatísticas dos melhores genomas
            best_genomes_stats = []
            for genome in list(self.best_genomes)[:10]:  # Top 10
                best_genomes_stats.append({
                    'genome_id': genome.genome_id,
                    'fitness_score': genome.fitness_score,
                    'consciousness_level': float(genome.consciousness_level),
                    'generation': genome.generation,
                    'gene_count': len(genome.genes)
                })
            
            return {
                'current_generation': self.stats['current_generation'],
                'total_generations': self.stats['total_generations'],
                'population_size': len(self.population),
                'best_fitness': self.stats['best_fitness'],
                'average_fitness': self.stats['average_fitness'],
                'consciousness_level': float(self.stats['consciousness_level']),
                'optimization_objective': self.stats['optimization_objective'].value,
                'selection_method': self.stats['selection_method'].value,
                'mutation_rate': self.stats['mutation_rate'],
                'crossover_rate': self.stats['crossover_rate'],
                'convergence_generations': self.stats['convergence_generations'],
                'generation_history': generation_stats,
                'best_genomes': best_genomes_stats
            }
    
    def optimize_parameters(self) -> Dict[str, Any]:
        """Otimiza parâmetros do algoritmo genético."""
        try:
            with self._lock:
                optimization_stats = {
                    'parameters_adjusted': 0,
                    'consciousness_improvement': Decimal('0.0'),
                    'timestamp': time.time()
                }
                
                # Ajustar taxa de mutação baseado na convergência
                if self.stats['convergence_generations'] > 5:
                    # Aumentar mutação se convergiu muito rápido
                    self.stats['mutation_rate'] = min(0.3, self.stats['mutation_rate'] * 1.1)
                    optimization_stats['parameters_adjusted'] += 1
                elif self.stats['convergence_generations'] == 0 and self.stats['total_generations'] > 20:
                    # Diminuir mutação se não convergiu
                    self.stats['mutation_rate'] = max(0.05, self.stats['mutation_rate'] * 0.9)
                    optimization_stats['parameters_adjusted'] += 1
                
                # Ajustar taxa de crossover baseado na diversidade
                if len(self.population) > 1:
                    fitness_values = [g.fitness_score for g in self.population]
                    fitness_variance = statistics.variance(fitness_values) if len(fitness_values) > 1 else 0
                    
                    if fitness_variance < 0.01:  # Baixa diversidade
                        self.stats['crossover_rate'] = min(0.95, self.stats['crossover_rate'] * 1.05)
                        optimization_stats['parameters_adjusted'] += 1
                    elif fitness_variance > 0.1:  # Alta diversidade
                        self.stats['crossover_rate'] = max(0.5, self.stats['crossover_rate'] * 0.95)
                        optimization_stats['parameters_adjusted'] += 1
                
                # Aumentar consciência geral
                old_consciousness = self.stats['consciousness_level']
                self.stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    self.stats['consciousness_level'] + Decimal('0.02')
                )
                optimization_stats['consciousness_improvement'] = (
                    self.stats['consciousness_level'] - old_consciousness
                )
                
                logger.info(f"Parâmetros otimizados: {optimization_stats['parameters_adjusted']} ajustes")
                return optimization_stats
                
        except Exception as e:
            logger.error(f"Erro na otimização de parâmetros: {e}")
            return {'error': str(e)}


# Instância global do otimizador genético
fractal_genetic_optimizer = FractalGeneticOptimizer()
