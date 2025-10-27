"""
Sistema de Compressão de Dados Fractal.

Este módulo implementa um sistema inteligente de compressão que:
- Adapta algoritmos baseado no tipo de dados
- Usa padrões fractais para compressão
- Aplica compressão consciente baseada em contexto
- Otimiza automaticamente para diferentes cenários
"""

import zlib
import gzip
import bz2
import lzma
import time
import threading
from typing import Dict, Any, Optional, List, Tuple, Union
from decimal import Decimal
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import logging
import struct

logger = logging.getLogger(__name__)


class CompressionAlgorithm(Enum):
    """Algoritmos de compressão disponíveis."""
    ZLIB = "zlib"
    GZIP = "gzip"
    BZ2 = "bz2"
    LZMA = "lzma"
    FRACTAL_PATTERN = "fractal_pattern"
    ADAPTIVE = "adaptive"


class DataType(Enum):
    """Tipos de dados para otimização de compressão."""
    TEXT = "text"
    JSON = "json"
    BINARY = "binary"
    NUMERIC = "numeric"
    FRACTAL_DATA = "fractal_data"
    BLOCKCHAIN_DATA = "blockchain_data"
    UNKNOWN = "unknown"


@dataclass
class CompressionResult:
    """Resultado da compressão."""
    original_size: int
    compressed_size: int
    compression_ratio: float
    algorithm_used: CompressionAlgorithm
    compression_time: float
    consciousness_level: Decimal = Decimal('0.5')
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_efficiency_score(self) -> Decimal:
        """Calcula score de eficiência da compressão."""
        if self.original_size == 0:
            return Decimal('0.0')
        
        ratio = Decimal(str(self.compression_ratio))
        time_factor = Decimal('1.0') - min(Decimal(str(self.compression_time)) / Decimal('1.0'), Decimal('1.0'))
        consciousness_factor = self.consciousness_level
        
        efficiency = ratio * time_factor * consciousness_factor
        return min(efficiency, Decimal('1.0'))


@dataclass
class FractalPattern:
    """Padrão fractal para compressão."""
    pattern_id: str
    pattern_data: bytes
    frequency: int
    consciousness_level: Decimal
    compression_strength: Decimal
    last_used: float = field(default_factory=time.time)


class FractalCompressor:
    """
    Sistema de Compressão de Dados Fractal Consciente.
    
    Características:
    - Compressão adaptativa baseada em consciência
    - Detecção automática de padrões fractais
    - Otimização para diferentes tipos de dados
    - Compressão hierárquica
    - Aprendizado contínuo de padrões
    """
    
    def __init__(self):
        self.compression_stats: Dict[CompressionAlgorithm, Dict[str, Any]] = {}
        self.fractal_patterns: Dict[str, FractalPattern] = {}
        self.data_type_stats: Dict[DataType, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self.consciousness_level = Decimal('0.1')
        
        self._initialize_stats()
        logger.info("FractalCompressor inicializado")
    
    def _initialize_stats(self):
        """Inicializa estatísticas de compressão."""
        for algorithm in CompressionAlgorithm:
            self.compression_stats[algorithm] = {
                'total_compressions': 0,
                'total_decompressions': 0,
                'total_time': 0.0,
                'average_ratio': 0.0,
                'success_rate': 0.0,
                'consciousness_level': Decimal('0.1')
            }
        
        for data_type in DataType:
            self.data_type_stats[data_type] = {
                'total_size': 0,
                'compressed_size': 0,
                'best_algorithm': CompressionAlgorithm.ZLIB,
                'average_ratio': 0.0,
                'consciousness_level': Decimal('0.1')
            }
    
    def detect_data_type(self, data: Union[str, bytes]) -> DataType:
        """Detecta o tipo de dados para otimização."""
        try:
            if isinstance(data, str):
                # Tentar detectar JSON
                try:
                    json.loads(data)
                    return DataType.JSON
                except:
                    pass
                
                # Verificar se é texto
                if data.isprintable():
                    return DataType.TEXT
                
                return DataType.UNKNOWN
            
            elif isinstance(data, bytes):
                # Verificar se é dados binários estruturados
                if len(data) > 4:
                    # Verificar padrões comuns de blockchain
                    if data[:4] in [b'BLK\x00', b'TXN\x00', b'FRC\x00']:
                        return DataType.BLOCKCHAIN_DATA
                    
                    # Verificar se contém padrões fractais
                    if self._has_fractal_pattern(data):
                        return DataType.FRACTAL_DATA
                
                return DataType.BINARY
            
            return DataType.UNKNOWN
            
        except Exception as e:
            logger.error(f"Erro na detecção de tipo de dados: {e}")
            return DataType.UNKNOWN
    
    def _has_fractal_pattern(self, data: bytes) -> bool:
        """Verifica se os dados contêm padrões fractais."""
        try:
            # Verificar repetições de padrões
            if len(data) < 16:
                return False
            
            # Procurar por padrões repetitivos
            for pattern_size in [4, 8, 16]:
                if len(data) >= pattern_size * 2:
                    pattern = data[:pattern_size]
                    repetitions = 0
                    
                    for i in range(pattern_size, len(data) - pattern_size + 1, pattern_size):
                        if data[i:i+pattern_size] == pattern:
                            repetitions += 1
                    
                    if repetitions >= 2:  # Padrão repetido pelo menos 2 vezes
                        return True
            
            return False
            
        except:
            return False
    
    def compress(self, data: Union[str, bytes], 
                algorithm: Optional[CompressionAlgorithm] = None,
                consciousness_threshold: Decimal = Decimal('0.5')) -> CompressionResult:
        """
        Comprime dados usando algoritmo otimizado.
        
        Args:
            data: Dados para comprimir
            algorithm: Algoritmo específico (None para automático)
            consciousness_threshold: Limiar de consciência para otimização
            
        Returns:
            Resultado da compressão
        """
        try:
            start_time = time.time()
            original_size = len(data)
            
            # Detectar tipo de dados
            data_type = self.detect_data_type(data)
            
            # Selecionar algoritmo se não especificado
            if algorithm is None:
                algorithm = self._select_optimal_algorithm(data_type, consciousness_threshold)
            
            # Converter para bytes se necessário
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            
            # Aplicar compressão
            compressed_data = self._apply_compression(data_bytes, algorithm)
            
            # Calcular métricas
            compression_time = time.time() - start_time
            compressed_size = len(compressed_data)
            compression_ratio = compressed_size / original_size if original_size > 0 else 0.0
            
            # Criar resultado
            result = CompressionResult(
                original_size=original_size,
                compressed_size=compressed_size,
                compression_ratio=compression_ratio,
                algorithm_used=algorithm,
                compression_time=compression_time,
                consciousness_level=self.consciousness_level,
                metadata={
                    'data_type': data_type.value,
                    'consciousness_threshold': float(consciousness_threshold)
                }
            )
            
            # Atualizar estatísticas
            self._update_stats(algorithm, data_type, result)
            
            # Aprender padrões fractais se aplicável
            if data_type == DataType.FRACTAL_DATA:
                self._learn_fractal_patterns(data_bytes)
            
            logger.debug(f"Dados comprimidos: {original_size} -> {compressed_size} "
                        f"({compression_ratio:.2%}) usando {algorithm.value}")
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na compressão: {e}")
            # Retornar resultado de falha
            return CompressionResult(
                original_size=len(data),
                compressed_size=len(data),
                compression_ratio=1.0,
                algorithm_used=CompressionAlgorithm.ZLIB,
                compression_time=0.0,
                consciousness_level=Decimal('0.0'),
                metadata={'error': str(e)}
            )
    
    def _select_optimal_algorithm(self, data_type: DataType, 
                                consciousness_threshold: Decimal) -> CompressionAlgorithm:
        """Seleciona algoritmo ótimo baseado no tipo de dados e consciência."""
        try:
            # Algoritmos recomendados por tipo de dados
            algorithm_map = {
                DataType.TEXT: [CompressionAlgorithm.GZIP, CompressionAlgorithm.ZLIB],
                DataType.JSON: [CompressionAlgorithm.GZIP, CompressionAlgorithm.ZLIB],
                DataType.BINARY: [CompressionAlgorithm.LZMA, CompressionAlgorithm.BZ2],
                DataType.FRACTAL_DATA: [CompressionAlgorithm.FRACTAL_PATTERN, CompressionAlgorithm.LZMA],
                DataType.BLOCKCHAIN_DATA: [CompressionAlgorithm.BZ2, CompressionAlgorithm.LZMA],
                DataType.NUMERIC: [CompressionAlgorithm.ZLIB, CompressionAlgorithm.GZIP],
                DataType.UNKNOWN: [CompressionAlgorithm.ADAPTIVE, CompressionAlgorithm.ZLIB]
            }
            
            candidates = algorithm_map.get(data_type, [CompressionAlgorithm.ZLIB])
            
            # Selecionar baseado em consciência e estatísticas
            if self.consciousness_level >= consciousness_threshold:
                # Usar algoritmo com melhor histórico
                best_algorithm = None
                best_score = Decimal('0.0')
                
                for algorithm in candidates:
                    stats = self.compression_stats[algorithm]
                    if stats['total_compressions'] > 0:
                        # Score baseado em taxa de sucesso e ratio médio
                        success_rate = Decimal(str(stats['success_rate']))
                        avg_ratio = Decimal(str(stats['average_ratio']))
                        consciousness = stats['consciousness_level']
                        
                        score = success_rate * (Decimal('1.0') - avg_ratio) * consciousness
                        
                        if score > best_score:
                            best_score = score
                            best_algorithm = algorithm
                
                if best_algorithm:
                    return best_algorithm
            
            # Fallback para primeiro candidato
            return candidates[0]
            
        except Exception as e:
            logger.error(f"Erro na seleção de algoritmo: {e}")
            return CompressionAlgorithm.ZLIB
    
    def _apply_compression(self, data: bytes, algorithm: CompressionAlgorithm) -> bytes:
        """Aplica algoritmo de compressão específico."""
        try:
            if algorithm == CompressionAlgorithm.ZLIB:
                return zlib.compress(data, level=9)
            elif algorithm == CompressionAlgorithm.GZIP:
                return gzip.compress(data, compresslevel=9)
            elif algorithm == CompressionAlgorithm.BZ2:
                return bz2.compress(data, compresslevel=9)
            elif algorithm == CompressionAlgorithm.LZMA:
                return lzma.compress(data, preset=9)
            elif algorithm == CompressionAlgorithm.FRACTAL_PATTERN:
                return self._fractal_pattern_compress(data)
            elif algorithm == CompressionAlgorithm.ADAPTIVE:
                return self._adaptive_compress(data)
            else:
                return zlib.compress(data)
                
        except Exception as e:
            logger.error(f"Erro na aplicação de compressão {algorithm.value}: {e}")
            return data
    
    def _fractal_pattern_compress(self, data: bytes) -> bytes:
        """Compressão baseada em padrões fractais."""
        try:
            compressed_parts = []
            i = 0
            
            while i < len(data):
                best_pattern = None
                best_savings = 0
                best_length = 0
                
                # Procurar padrões fractais conhecidos
                for pattern_id, pattern in self.fractal_patterns.items():
                    pattern_data = pattern.pattern_data
                    pattern_len = len(pattern_data)
                    
                    if i + pattern_len <= len(data):
                        if data[i:i+pattern_len] == pattern_data:
                            # Calcular economia
                            savings = pattern_len - 8  # 8 bytes para referência
                            if savings > best_savings:
                                best_savings = savings
                                best_pattern = pattern_id
                                best_length = pattern_len
                
                if best_pattern and best_savings > 0:
                    # Usar padrão fractal
                    compressed_parts.append(b'FRC:' + best_pattern.encode()[:4])
                    i += best_length
                else:
                    # Adicionar byte literal
                    compressed_parts.append(data[i:i+1])
                    i += 1
            
            return b''.join(compressed_parts)
            
        except Exception as e:
            logger.error(f"Erro na compressão fractal: {e}")
            return data
    
    def _adaptive_compress(self, data: bytes) -> bytes:
        """Compressão adaptativa que testa múltiplos algoritmos."""
        try:
            algorithms_to_test = [
                CompressionAlgorithm.ZLIB,
                CompressionAlgorithm.GZIP,
                CompressionAlgorithm.BZ2,
                CompressionAlgorithm.LZMA
            ]
            
            best_result = None
            best_size = len(data)
            
            for algorithm in algorithms_to_test:
                try:
                    compressed = self._apply_compression(data, algorithm)
                    if len(compressed) < best_size:
                        best_size = len(compressed)
                        best_result = compressed
                except:
                    continue
            
            return best_result if best_result else data
            
        except Exception as e:
            logger.error(f"Erro na compressão adaptativa: {e}")
            return data
    
    def decompress(self, compressed_data: bytes, 
                  algorithm: CompressionAlgorithm) -> bytes:
        """Descomprime dados usando algoritmo específico."""
        try:
            start_time = time.time()
            
            if algorithm == CompressionAlgorithm.ZLIB:
                result = zlib.decompress(compressed_data)
            elif algorithm == CompressionAlgorithm.GZIP:
                result = gzip.decompress(compressed_data)
            elif algorithm == CompressionAlgorithm.BZ2:
                result = bz2.decompress(compressed_data)
            elif algorithm == CompressionAlgorithm.LZMA:
                result = lzma.decompress(compressed_data)
            elif algorithm == CompressionAlgorithm.FRACTAL_PATTERN:
                result = self._fractal_pattern_decompress(compressed_data)
            else:
                result = zlib.decompress(compressed_data)
            
            # Atualizar estatísticas de descompressão
            with self._lock:
                stats = self.compression_stats[algorithm]
                stats['total_decompressions'] += 1
                stats['total_time'] += time.time() - start_time
            
            logger.debug(f"Dados descomprimidos usando {algorithm.value}")
            return result
            
        except Exception as e:
            logger.error(f"Erro na descompressão {algorithm.value}: {e}")
            return compressed_data
    
    def _fractal_pattern_decompress(self, compressed_data: bytes) -> bytes:
        """Descompressão baseada em padrões fractais."""
        try:
            result = []
            i = 0
            
            while i < len(compressed_data):
                if i + 4 <= len(compressed_data) and compressed_data[i:i+4] == b'FRC:':
                    # Referência a padrão fractal
                    pattern_id = compressed_data[i+4:i+8].decode('ascii', errors='ignore')
                    if pattern_id in self.fractal_patterns:
                        pattern_data = self.fractal_patterns[pattern_id].pattern_data
                        result.append(pattern_data)
                        i += 8
                    else:
                        result.append(compressed_data[i:i+1])
                        i += 1
                else:
                    result.append(compressed_data[i:i+1])
                    i += 1
            
            return b''.join(result)
            
        except Exception as e:
            logger.error(f"Erro na descompressão fractal: {e}")
            return compressed_data
    
    def _learn_fractal_patterns(self, data: bytes):
        """Aprende novos padrões fractais dos dados."""
        try:
            with self._lock:
                # Procurar padrões de diferentes tamanhos
                for pattern_size in [4, 8, 16, 32]:
                    if len(data) >= pattern_size * 3:  # Pelo menos 3 repetições
                        patterns = {}
                        
                        for i in range(len(data) - pattern_size + 1):
                            pattern = data[i:i+pattern_size]
                            pattern_key = hashlib.md5(pattern).hexdigest()[:8]
                            
                            if pattern_key not in patterns:
                                patterns[pattern_key] = {
                                    'data': pattern,
                                    'count': 0,
                                    'positions': []
                                }
                            
                            patterns[pattern_key]['count'] += 1
                            patterns[pattern_key]['positions'].append(i)
                        
                        # Adicionar padrões frequentes
                        for pattern_key, info in patterns.items():
                            if info['count'] >= 3:  # Padrão repetido pelo menos 3 vezes
                                if pattern_key not in self.fractal_patterns:
                                    self.fractal_patterns[pattern_key] = FractalPattern(
                                        pattern_id=pattern_key,
                                        pattern_data=info['data'],
                                        frequency=info['count'],
                                        consciousness_level=self.consciousness_level,
                                        compression_strength=Decimal(str(info['count'] / len(data)))
                                    )
                                
                                logger.debug(f"Padrão fractal aprendido: {pattern_key} "
                                           f"(frequência: {info['count']})")
                
                # Limitar número de padrões
                if len(self.fractal_patterns) > 1000:
                    # Remover padrões menos usados
                    sorted_patterns = sorted(
                        self.fractal_patterns.items(),
                        key=lambda x: x[1].frequency
                    )
                    
                    for pattern_id, _ in sorted_patterns[:100]:  # Remover 100 menos usados
                        del self.fractal_patterns[pattern_id]
                
        except Exception as e:
            logger.error(f"Erro no aprendizado de padrões fractais: {e}")
    
    def _update_stats(self, algorithm: CompressionAlgorithm, 
                     data_type: DataType, result: CompressionResult):
        """Atualiza estatísticas de compressão."""
        try:
            with self._lock:
                # Atualizar estatísticas do algoritmo
                stats = self.compression_stats[algorithm]
                stats['total_compressions'] += 1
                stats['total_time'] += result.compression_time
                
                # Atualizar ratio médio
                if stats['total_compressions'] == 1:
                    stats['average_ratio'] = result.compression_ratio
                else:
                    stats['average_ratio'] = (
                        (stats['average_ratio'] * (stats['total_compressions'] - 1) + 
                         result.compression_ratio) / stats['total_compressions']
                    )
                
                # Atualizar taxa de sucesso
                success = 1 if result.compression_ratio < 1.0 else 0
                if stats['total_compressions'] == 1:
                    stats['success_rate'] = success
                else:
                    stats['success_rate'] = (
                        (stats['success_rate'] * (stats['total_compressions'] - 1) + 
                         success) / stats['total_compressions']
                    )
                
                # Aumentar consciência do algoritmo
                stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    stats['consciousness_level'] + Decimal('0.01')
                )
                
                # Atualizar estatísticas do tipo de dados
                type_stats = self.data_type_stats[data_type]
                type_stats['total_size'] += result.original_size
                type_stats['compressed_size'] += result.compressed_size
                
                if type_stats['total_size'] > 0:
                    type_stats['average_ratio'] = type_stats['compressed_size'] / type_stats['total_size']
                
                # Atualizar melhor algoritmo para o tipo
                if result.compression_ratio < type_stats['average_ratio']:
                    type_stats['best_algorithm'] = algorithm
                
                # Aumentar consciência do tipo de dados
                type_stats['consciousness_level'] = min(
                    Decimal('1.0'),
                    type_stats['consciousness_level'] + Decimal('0.005')
                )
                
                # Atualizar consciência geral
                self.consciousness_level = min(
                    Decimal('1.0'),
                    self.consciousness_level + Decimal('0.001')
                )
                
        except Exception as e:
            logger.error(f"Erro na atualização de estatísticas: {e}")
    
    def get_compression_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de compressão."""
        with self._lock:
            return {
                'consciousness_level': float(self.consciousness_level),
                'algorithms': {
                    algorithm.value: {
                        'total_compressions': stats['total_compressions'],
                        'total_decompressions': stats['total_decompressions'],
                        'average_ratio': stats['average_ratio'],
                        'success_rate': stats['success_rate'],
                        'consciousness_level': float(stats['consciousness_level'])
                    }
                    for algorithm, stats in self.compression_stats.items()
                },
                'data_types': {
                    data_type.value: {
                        'total_size': stats['total_size'],
                        'compressed_size': stats['compressed_size'],
                        'average_ratio': stats['average_ratio'],
                        'best_algorithm': stats['best_algorithm'].value,
                        'consciousness_level': float(stats['consciousness_level'])
                    }
                    for data_type, stats in self.data_type_stats.items()
                },
                'fractal_patterns': {
                    'count': len(self.fractal_patterns),
                    'patterns': {
                        pattern_id: {
                            'frequency': pattern.frequency,
                            'consciousness_level': float(pattern.consciousness_level),
                            'compression_strength': float(pattern.compression_strength)
                        }
                        for pattern_id, pattern in list(self.fractal_patterns.items())[:10]  # Top 10
                    }
                }
            }
    
    def optimize_compression(self) -> Dict[str, Any]:
        """Otimiza sistema de compressão."""
        try:
            with self._lock:
                optimization_stats = {
                    'patterns_optimized': 0,
                    'algorithms_optimized': 0,
                    'consciousness_improvement': Decimal('0.0'),
                    'timestamp': time.time()
                }
                
                # Otimizar padrões fractais
                patterns_to_remove = []
                for pattern_id, pattern in self.fractal_patterns.items():
                    if pattern.frequency < 2:  # Remover padrões pouco usados
                        patterns_to_remove.append(pattern_id)
                    else:
                        # Aumentar consciência de padrões bem usados
                        pattern.consciousness_level = min(
                            Decimal('1.0'),
                            pattern.consciousness_level + Decimal('0.01')
                        )
                        optimization_stats['patterns_optimized'] += 1
                
                for pattern_id in patterns_to_remove:
                    del self.fractal_patterns[pattern_id]
                
                # Otimizar algoritmos baseado em performance
                for algorithm, stats in self.compression_stats.items():
                    if stats['total_compressions'] > 10:
                        if stats['success_rate'] > 0.8:
                            stats['consciousness_level'] = min(
                                Decimal('1.0'),
                                stats['consciousness_level'] + Decimal('0.02')
                            )
                            optimization_stats['algorithms_optimized'] += 1
                
                # Aumentar consciência geral
                old_consciousness = self.consciousness_level
                self.consciousness_level = min(
                    Decimal('1.0'),
                    self.consciousness_level + Decimal('0.05')
                )
                optimization_stats['consciousness_improvement'] = (
                    self.consciousness_level - old_consciousness
                )
                
                logger.info(f"Compressão otimizada: {optimization_stats['patterns_optimized']} "
                           f"padrões, {optimization_stats['algorithms_optimized']} algoritmos")
                
                return optimization_stats
                
        except Exception as e:
            logger.error(f"Erro na otimização de compressão: {e}")
            return {'error': str(e)}


# Instância global do compressor fractal
fractal_compressor = FractalCompressor()
