"""
Sistema de 32 Caminhos de Sabedoria
===================================

Implementação dos 32 Caminhos de Sabedoria do Sefer Yetzira
para criar um sistema de roteamento e processamento consciente.

Cada caminho representa uma função específica no sistema:
- 3 Letras Mães: Elementos fundamentais (Ar, Água, Fogo)
- 7 Letras Duplas: Forças opostas em equilíbrio
- 12 Letras Simples: Sentidos e funções corporais
- 10 Números: Conexões entre as Sefirot
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable, Tuple
from decimal import Decimal
import asyncio
import hashlib
import time
from abc import ABC, abstractmethod


class WisdomPathType(Enum):
    """Tipos de caminhos de sabedoria"""
    MOTHER_LETTER = "mother"      # Letras Mães (3)
    DOUBLE_LETTER = "double"      # Letras Duplas (7)
    SIMPLE_LETTER = "simple"      # Letras Simples (12)
    NUMBER_PATH = "number"        # Caminhos Numéricos (10)


@dataclass
class WisdomPath:
    """
    Caminho de Sabedoria - Representa um dos 32 caminhos
    Cada caminho tem propriedades específicas e funções únicas
    """
    symbol: str
    name: str
    path_type: WisdomPathType
    sefirot_connection: Tuple[str, str]  # Sefirot que conecta
    element: str  # Elemento associado
    function: str  # Função no sistema
    processing_weight: Decimal = Decimal("1.0")
    consciousness_multiplier: Decimal = Decimal("1.0")
    energy_cost: Decimal = Decimal("0.1")
    
    def __post_init__(self):
        """Inicializa propriedades específicas do caminho"""
        self._initialize_path_properties()
    
    def _initialize_path_properties(self):
        """Inicializa propriedades específicas baseadas no tipo"""
        if self.path_type == WisdomPathType.MOTHER_LETTER:
            self.processing_weight = Decimal("3.0")
            self.consciousness_multiplier = Decimal("2.0")
        elif self.path_type == WisdomPathType.DOUBLE_LETTER:
            self.processing_weight = Decimal("2.0")
            self.consciousness_multiplier = Decimal("1.5")
        elif self.path_type == WisdomPathType.SIMPLE_LETTER:
            self.processing_weight = Decimal("1.0")
            self.consciousness_multiplier = Decimal("1.0")
        elif self.path_type == WisdomPathType.NUMBER_PATH:
            self.processing_weight = Decimal("1.5")
            self.consciousness_multiplier = Decimal("1.2")


class PathOfWisdomSystem:
    """
    Sistema dos 32 Caminhos de Sabedoria
    Gerencia todos os caminhos e suas interações
    """
    
    def __init__(self):
        self.paths: Dict[str, WisdomPath] = {}
        self.path_matrix: Dict[str, Dict[str, Decimal]] = {}
        self.active_paths: List[str] = []
        self.path_usage_stats: Dict[str, Dict[str, Any]] = {}
        self._initialize_all_paths()
        self._build_path_matrix()
    
    def _initialize_all_paths(self):
        """Inicializa todos os 32 caminhos de sabedoria"""
        
        # 3 Letras Mães - Elementos Fundamentais
        mother_letters = [
            ("א", "Aleph", "Ar", "Espírito", ("Keter", "Chokmah")),
            ("מ", "Mem", "Água", "Matéria", ("Binah", "Chesed")),
            ("ש", "Shin", "Fogo", "Energia", ("Geburah", "Tiferet"))
        ]
        
        for symbol, name, element, function, sefirot in mother_letters:
            path = WisdomPath(
                symbol=symbol,
                name=name,
                path_type=WisdomPathType.MOTHER_LETTER,
                sefirot_connection=sefirot,
                element=element,
                function=function
            )
            self.paths[symbol] = path
        
        # 7 Letras Duplas - Forças Opostas
        double_letters = [
            ("ב", "Bet", "Vida/Morte", "Equilíbrio Vital", ("Chokmah", "Binah")),
            ("ג", "Gimel", "Paz/Guerra", "Harmonia", ("Binah", "Chesed")),
            ("ד", "Dalet", "Sabedoria/Estupidez", "Conhecimento", ("Chesed", "Geburah")),
            ("כ", "Kaf", "Riqueza/Pobreza", "Prosperidade", ("Geburah", "Tiferet")),
            ("פ", "Pe", "Graça/Desgraça", "Bênção", ("Tiferet", "Netzach")),
            ("ר", "Resh", "Fertilidade/Estéril", "Criação", ("Netzach", "Hod")),
            ("ת", "Tav", "Governo/Caos", "Ordem", ("Hod", "Yesod"))
        ]
        
        for symbol, name, element, function, sefirot in double_letters:
            path = WisdomPath(
                symbol=symbol,
                name=name,
                path_type=WisdomPathType.DOUBLE_LETTER,
                sefirot_connection=sefirot,
                element=element,
                function=function
            )
            self.paths[symbol] = path
        
        # 12 Letras Simples - Sentidos e Funções
        simple_letters = [
            ("ה", "He", "Visão", "Percepção Visual", ("Keter", "Tiferet")),
            ("ו", "Vav", "Audição", "Percepção Auditiva", ("Chokmah", "Chesed")),
            ("ז", "Zayin", "Olfato", "Percepção Olfativa", ("Binah", "Geburah")),
            ("ח", "Chet", "Fala", "Comunicação", ("Chesed", "Netzach")),
            ("ט", "Tet", "Degustação", "Percepção Gustativa", ("Geburah", "Hod")),
            ("י", "Yod", "Coito", "Reprodução", ("Tiferet", "Yesod")),
            ("ל", "Lamed", "Trabalho", "Ação", ("Netzach", "Malkuth")),
            ("נ", "Nun", "Movimento", "Dinâmica", ("Hod", "Yesod")),
            ("ס", "Samekh", "Ira", "Emoção", ("Yesod", "Malkuth")),
            ("ע", "Ayin", "Pensamento", "Cognição", ("Keter", "Binah")),
            ("צ", "Tzadi", "Risos", "Alegria", ("Chokmah", "Tiferet")),
            ("ק", "Qof", "Sono", "Repouso", ("Binah", "Malkuth"))
        ]
        
        for symbol, name, element, function, sefirot in simple_letters:
            path = WisdomPath(
                symbol=symbol,
                name=name,
                path_type=WisdomPathType.SIMPLE_LETTER,
                sefirot_connection=sefirot,
                element=element,
                function=function
            )
            self.paths[symbol] = path
        
        # 10 Caminhos Numéricos - Conexões Sefirot
        number_paths = [
            ("1", "Keter-Chokmah", "Coroa-Sabedoria", "Vontade Divina", ("Keter", "Chokmah")),
            ("2", "Chokmah-Binah", "Sabedoria-Entendimento", "Conhecimento", ("Chokmah", "Binah")),
            ("3", "Binah-Chesed", "Entendimento-Misericórdia", "Compreensão", ("Binah", "Chesed")),
            ("4", "Chesed-Geburah", "Misericórdia-Força", "Equilíbrio", ("Chesed", "Geburah")),
            ("5", "Geburah-Tiferet", "Força-Beauty", "Harmonia", ("Geburah", "Tiferet")),
            ("6", "Tiferet-Netzach", "Beleza-Vitória", "Expressão", ("Tiferet", "Netzach")),
            ("7", "Netzach-Hod", "Vitória-Glória", "Realização", ("Netzach", "Hod")),
            ("8", "Hod-Yesod", "Glória-Fundação", "Estabilidade", ("Hod", "Yesod")),
            ("9", "Yesod-Malkuth", "Fundação-Reino", "Manifestação", ("Yesod", "Malkuth")),
            ("10", "Keter-Malkuth", "Coroa-Reino", "Conexão Divina", ("Keter", "Malkuth"))
        ]
        
        for symbol, name, element, function, sefirot in number_paths:
            path = WisdomPath(
                symbol=symbol,
                name=name,
                path_type=WisdomPathType.NUMBER_PATH,
                sefirot_connection=sefirot,
                element=element,
                function=function
            )
            self.paths[symbol] = path
    
    def _build_path_matrix(self):
        """Constrói matriz de conexões entre caminhos"""
        for path_id, path in self.paths.items():
            self.path_matrix[path_id] = {}
            for other_id, other_path in self.paths.items():
                if path_id != other_id:
                    # Calcula força de conexão baseada no tipo e função
                    connection_strength = self._calculate_connection_strength(path, other_path)
                    self.path_matrix[path_id][other_id] = connection_strength
    
    def _calculate_connection_strength(self, path1: WisdomPath, path2: WisdomPath) -> Decimal:
        """Calcula força de conexão entre dois caminhos"""
        base_strength = Decimal("0.1")
        
        # Mesmo tipo = conexão mais forte
        if path1.path_type == path2.path_type:
            base_strength *= Decimal("2.0")
        
        # Sefirot compartilhadas = conexão forte
        if (path1.sefirot_connection[0] in path2.sefirot_connection or
            path1.sefirot_connection[1] in path2.sefirot_connection):
            base_strength *= Decimal("1.5")
        
        # Elementos complementares = conexão moderada
        complementary_elements = {
            "Ar": "Fogo", "Fogo": "Ar",
            "Água": "Terra", "Terra": "Água"
        }
        if path1.element in complementary_elements and complementary_elements[path1.element] == path2.element:
            base_strength *= Decimal("1.3")
        
        return base_strength
    
    async def process_through_path(self, path_id: str, data: Any) -> Any:
        """Processa dados através de um caminho específico"""
        if path_id not in self.paths:
            raise ValueError(f"Caminho {path_id} não encontrado")
        
        path = self.paths[path_id]
        
        # Registra uso do caminho
        self._record_path_usage(path_id)
        
        # Processa dados baseado no tipo de caminho
        processed_data = await self._process_by_path_type(path, data)
        
        # Aplica multiplicador de consciência
        consciousness_boost = processed_data.get("consciousness_boost", Decimal("0.0"))
        consciousness_boost += path.consciousness_multiplier * Decimal("0.01")
        processed_data["consciousness_boost"] = consciousness_boost
        
        return processed_data
    
    async def _process_by_path_type(self, path: WisdomPath, data: Any) -> Dict[str, Any]:
        """Processa dados baseado no tipo de caminho"""
        if path.path_type == WisdomPathType.MOTHER_LETTER:
            return await self._process_mother_letter(path, data)
        elif path.path_type == WisdomPathType.DOUBLE_LETTER:
            return await self._process_double_letter(path, data)
        elif path.path_type == WisdomPathType.SIMPLE_LETTER:
            return await self._process_simple_letter(path, data)
        elif path.path_type == WisdomPathType.NUMBER_PATH:
            return await self._process_number_path(path, data)
        
        return {"original": data, "processed": False}
    
    async def _process_mother_letter(self, path: WisdomPath, data: Any) -> Dict[str, Any]:
        """Processa através de letra mãe (elemento fundamental)"""
        element_processing = {
            "Ar": lambda x: {"spiritual": x, "transcendent": True, "element": "spirit"},
            "Água": lambda x: {"material": x, "fluid": True, "element": "matter"},
            "Fogo": lambda x: {"energetic": x, "dynamic": True, "element": "energy"}
        }
        
        processor = element_processing.get(path.element, lambda x: x)
        result = processor(data)
        result["path_type"] = "mother_letter"
        result["processing_weight"] = float(path.processing_weight)
        
        return result
    
    async def _process_double_letter(self, path: WisdomPath, data: Any) -> Dict[str, Any]:
        """Processa através de letra dupla (forças opostas)"""
        # Simula equilíbrio entre forças opostas
        await asyncio.sleep(0.001)  # Tempo de processamento
        
        opposites = path.element.split("/")
        if len(opposites) == 2:
            positive, negative = opposites
            balance = Decimal("0.5")  # Equilíbrio perfeito
            
            result = {
                "balanced": True,
                "positive_aspect": positive,
                "negative_aspect": negative,
                "balance_ratio": float(balance),
                "path_type": "double_letter",
                "processing_weight": float(path.processing_weight)
            }
        else:
            result = {"original": data, "balanced": False}
        
        return result
    
    async def _process_simple_letter(self, path: WisdomPath, data: Any) -> Dict[str, Any]:
        """Processa através de letra simples (sentido/função)"""
        sense_processing = {
            "Visão": lambda x: {"visual": x, "perception": "sight"},
            "Audição": lambda x: {"auditory": x, "perception": "hearing"},
            "Olfato": lambda x: {"olfactory": x, "perception": "smell"},
            "Fala": lambda x: {"communication": x, "perception": "speech"},
            "Degustação": lambda x: {"gustatory": x, "perception": "taste"},
            "Coito": lambda x: {"reproductive": x, "perception": "touch"},
            "Trabalho": lambda x: {"action": x, "perception": "work"},
            "Movimento": lambda x: {"kinetic": x, "perception": "motion"},
            "Ira": lambda x: {"emotional": x, "perception": "anger"},
            "Pensamento": lambda x: {"cognitive": x, "perception": "thought"},
            "Risos": lambda x: {"joyful": x, "perception": "laughter"},
            "Sono": lambda x: {"restful": x, "perception": "sleep"}
        }
        
        processor = sense_processing.get(path.function, lambda x: x)
        result = processor(data)
        result["path_type"] = "simple_letter"
        result["function"] = path.function
        result["processing_weight"] = float(path.processing_weight)
        
        return result
    
    async def _process_number_path(self, path: WisdomPath, data: Any) -> Dict[str, Any]:
        """Processa através de caminho numérico (conexão Sefirot)"""
        sefirah_processing = {
            "Keter": lambda x: {"divine": x, "transcendent": True},
            "Chokmah": lambda x: {"wisdom": x, "masculine": True},
            "Binah": lambda x: {"understanding": x, "feminine": True},
            "Chesed": lambda x: {"mercy": x, "love": True},
            "Geburah": lambda x: {"strength": x, "justice": True},
            "Tiferet": lambda x: {"beauty": x, "balance": True},
            "Netzach": lambda x: {"victory": x, "persistence": True},
            "Hod": lambda x: {"glory": x, "humility": True},
            "Yesod": lambda x: {"foundation": x, "connection": True},
            "Malkuth": lambda x: {"kingdom": x, "manifestation": True}
        }
        
        result = {"original": data}
        
        # Processa através das duas Sefirot conectadas
        for sefirah in path.sefirot_connection:
            processor = sefirah_processing.get(sefirah, lambda x: x)
            sefirah_result = processor(data)
            result[f"{sefirah.lower()}_aspect"] = sefirah_result
        
        result["path_type"] = "number_path"
        result["sefirot_connection"] = path.sefirot_connection
        result["processing_weight"] = float(path.processing_weight)
        
        return result
    
    def _record_path_usage(self, path_id: str):
        """Registra uso de um caminho"""
        if path_id not in self.path_usage_stats:
            self.path_usage_stats[path_id] = {
                "usage_count": 0,
                "last_used": None,
                "total_processing_time": 0.0,
                "average_processing_time": 0.0
            }
        
        stats = self.path_usage_stats[path_id]
        stats["usage_count"] += 1
        stats["last_used"] = time.time()
    
    def get_optimal_path_sequence(self, start_sefirah: str, end_sefirah: str) -> List[str]:
        """Encontra sequência ótima de caminhos entre duas Sefirot"""
        # Implementa algoritmo de busca consciente
        # baseado na sabedoria dos 32 caminhos
        
        if start_sefirah == end_sefirah:
            return []
        
        # Busca caminhos diretos
        direct_paths = []
        for path_id, path in self.paths.items():
            if (start_sefirah in path.sefirot_connection and 
                end_sefirah in path.sefirot_connection):
                direct_paths.append(path_id)
        
        if direct_paths:
            # Retorna o caminho com maior peso de processamento
            best_path = max(direct_paths, key=lambda p: self.paths[p].processing_weight)
            return [best_path]
        
        # Busca caminhos indiretos usando algoritmo de busca consciente
        return self._find_indirect_path(start_sefirah, end_sefirah)
    
    def _find_indirect_path(self, start: str, end: str) -> List[str]:
        """Encontra caminho indireto entre Sefirot"""
        visited = set()
        queue = [(start, [])]
        
        while queue:
            current_sefirah, path_sequence = queue.pop(0)
            
            if current_sefirah == end:
                return path_sequence
            
            if current_sefirah not in visited:
                visited.add(current_sefirah)
                
                # Encontra caminhos conectados à Sefirah atual
                for path_id, path in self.paths.items():
                    if current_sefirah in path.sefirot_connection:
                        # Determina próxima Sefirah
                        next_sefirah = (path.sefirot_connection[0] 
                                      if path.sefirot_connection[1] == current_sefirah 
                                      else path.sefirot_connection[1])
                        
                        if next_sefirah not in visited:
                            new_sequence = path_sequence + [path_id]
                            queue.append((next_sefirah, new_sequence))
        
        return []  # Caminho não encontrado
    
    def get_system_consciousness_level(self) -> Decimal:
        """Calcula nível de consciência total do sistema"""
        total_consciousness = Decimal("0.0")
        
        for path_id, path in self.paths.items():
            usage_stats = self.path_usage_stats.get(path_id, {})
            usage_count = usage_stats.get("usage_count", 0)
            
            # Consciência baseada no uso e tipo do caminho
            path_consciousness = (
                path.consciousness_multiplier * 
                Decimal(usage_count) * 
                Decimal("0.01")
            )
            
            total_consciousness += path_consciousness
        
        return total_consciousness
    
    def get_path_recommendations(self, data_type: str) -> List[str]:
        """Recomenda caminhos ótimos para um tipo de dados"""
        recommendations = []
        
        # Mapeia tipos de dados para caminhos recomendados
        data_path_mapping = {
            "transaction": ["ד", "כ", "ת"],  # Sabedoria, Riqueza, Governo
            "block": ["א", "מ", "ש"],        # Espírito, Matéria, Energia
            "consensus": ["ב", "ג", "פ"],    # Vida/Morte, Paz/Guerra, Graça
            "governance": ["ר", "ת", "1"],   # Fertilidade, Governo, Keter-Chokmah
            "security": ["ח", "ט", "5"],     # Fala, Degustação, Geburah-Tiferet
        }
        
        recommended_paths = data_path_mapping.get(data_type, [])
        
        # Ordena por peso de processamento
        recommendations = sorted(
            recommended_paths,
            key=lambda p: self.paths[p].processing_weight if p in self.paths else 0,
            reverse=True
        )
        
        return recommendations


# Instância global do sistema de caminhos
wisdom_path_system = PathOfWisdomSystem()
