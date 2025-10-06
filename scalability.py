"""
Sistema de Escalabilidade e Performance
Implementa sharding, cache, otimizações e monitoramento de performance
"""

import json
import time
import hashlib
import threading
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict
import sqlite3
from database_manager import DatabaseManager


class ShardManager:
    """Gerenciador de Sharding para escalabilidade"""
    
    def __init__(self, db_manager: DatabaseManager, num_shards: int = 4):
        self.db_manager = db_manager
        self.num_shards = num_shards
        self.shards = {}
        self.shard_locks = {}
        self._inicializar_shards()
    
    def _inicializar_shards(self):
        """Inicializa shards com bancos de dados separados"""
        for i in range(self.num_shards):
            shard_name = f"shard_{i}"
            shard_db = f"blockchain_{shard_name}.db"
            
            # Criar banco para cada shard
            conn = sqlite3.connect(shard_db)
            cursor = conn.cursor()
            
            # Tabelas específicas do shard
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blocos_shard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    indice INTEGER UNIQUE NOT NULL,
                    shard_id INTEGER NOT NULL,
                    timestamp REAL NOT NULL,
                    hash_anterior TEXT,
                    hash_atual TEXT UNIQUE NOT NULL,
                    prova INTEGER NOT NULL,
                    dados TEXT NOT NULL,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transacoes_shard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hash_transacao TEXT UNIQUE NOT NULL,
                    shard_id INTEGER NOT NULL,
                    bloco_id INTEGER,
                    remetente TEXT NOT NULL,
                    destinatario TEXT NOT NULL,
                    valor REAL NOT NULL,
                    timestamp REAL NOT NULL,
                    status TEXT DEFAULT 'pendente',
                    FOREIGN KEY (bloco_id) REFERENCES blocos_shard (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            
            self.shards[shard_name] = shard_db
            self.shard_locks[shard_name] = threading.Lock()
    
    def determinar_shard(self, endereco: str) -> str:
        """Determina qual shard deve processar um endereço"""
        hash_endereco = hashlib.sha256(endereco.encode()).hexdigest()
        shard_index = int(hash_endereco[:8], 16) % self.num_shards
        return f"shard_{shard_index}"
    
    def processar_transacao_shard(self, transacao: Dict) -> bool:
        """Processa transação no shard apropriado"""
        shard_name = self.determinar_shard(transacao['remetente'])
        
        with self.shard_locks[shard_name]:
            try:
                conn = sqlite3.connect(self.shards[shard_name])
                cursor = conn.cursor()
                
                # Inserir transação no shard
                cursor.execute('''
                    INSERT OR REPLACE INTO transacoes_shard 
                    (hash_transacao, shard_id, remetente, destinatario, valor, timestamp, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    self._gerar_hash_transacao(transacao),
                    int(shard_name.split('_')[1]),
                    transacao['remetente'],
                    transacao['destinatario'],
                    transacao['valor'],
                    transacao['timestamp'],
                    'pendente'
                ))
                
                conn.commit()
                conn.close()
                return True
                
            except Exception as e:
                print(f"Erro ao processar transação no shard {shard_name}: {e}")
                return False
    
    def obter_transacoes_shard(self, shard_name: str) -> List[Dict]:
        """Obtém transações de um shard específico"""
        with self.shard_locks[shard_name]:
            try:
                conn = sqlite3.connect(self.shards[shard_name])
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT hash_transacao, remetente, destinatario, valor, timestamp, status
                    FROM transacoes_shard ORDER BY timestamp DESC
                ''')
                
                resultados = cursor.fetchall()
                conn.close()
                
                return [
                    {
                        'hash': row[0],
                        'remetente': row[1],
                        'destinatario': row[2],
                        'valor': row[3],
                        'timestamp': row[4],
                        'status': row[5]
                    }
                    for row in resultados
                ]
                
            except Exception as e:
                print(f"Erro ao obter transações do shard {shard_name}: {e}")
                return []
    
    def _gerar_hash_transacao(self, transacao: Dict) -> str:
        """Gera hash único para transação"""
        transacao_str = json.dumps(transacao, sort_keys=True)
        return hashlib.sha256(transacao_str.encode()).hexdigest()
    
    def obter_estatisticas_shards(self) -> Dict[str, Any]:
        """Obtém estatísticas de todos os shards"""
        estatisticas = {}
        
        for shard_name in self.shards:
            with self.shard_locks[shard_name]:
                try:
                    conn = sqlite3.connect(self.shards[shard_name])
                    cursor = conn.cursor()
                    
                    # Contar transações
                    cursor.execute('SELECT COUNT(*) FROM transacoes_shard')
                    total_transacoes = cursor.fetchone()[0]
                    
                    cursor.execute('SELECT COUNT(*) FROM transacoes_shard WHERE status = "pendente"')
                    transacoes_pendentes = cursor.fetchone()[0]
                    
                    # Tamanho do banco
                    cursor.execute('SELECT COUNT(*) FROM blocos_shard')
                    total_blocos = cursor.fetchone()[0]
                    
                    conn.close()
                    
                    estatisticas[shard_name] = {
                        'total_transacoes': total_transacoes,
                        'transacoes_pendentes': transacoes_pendentes,
                        'total_blocos': total_blocos,
                        'status': 'ativo'
                    }
                    
                except Exception as e:
                    estatisticas[shard_name] = {
                        'status': 'erro',
                        'erro': str(e)
                    }
        
        return estatisticas


class CacheManager:
    """Gerenciador de cache para otimização de performance"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl  # Time to live em segundos
        self.access_times = {}
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        with self.lock:
            if key not in self.cache:
                return None
            
            # Verificar TTL
            if time.time() - self.access_times[key] > self.ttl:
                self._remove_key(key)
                return None
            
            # Atualizar tempo de acesso
            self.access_times[key] = time.time()
            return self.cache[key]
    
    def set(self, key: str, value: Any) -> bool:
        """Define valor no cache"""
        with self.lock:
            # Verificar se precisa remover itens antigos
            if len(self.cache) >= self.max_size:
                self._remove_oldest()
            
            self.cache[key] = value
            self.access_times[key] = time.time()
            return True
    
    def _remove_key(self, key: str):
        """Remove chave do cache"""
        if key in self.cache:
            del self.cache[key]
            del self.access_times[key]
    
    def _remove_oldest(self):
        """Remove item mais antigo do cache"""
        if not self.access_times:
            return
        
        oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
        self._remove_key(oldest_key)
    
    def clear(self):
        """Limpa todo o cache"""
        with self.lock:
            self.cache.clear()
            self.access_times.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas do cache"""
        with self.lock:
            return {
                'tamanho_atual': len(self.cache),
                'tamanho_maximo': self.max_size,
                'ttl': self.ttl,
                'chaves': list(self.cache.keys())
            }


class PerformanceMonitor:
    """Monitor de performance do sistema"""
    
    def __init__(self):
        self.metricas = defaultdict(list)
        self.lock = threading.Lock()
        self.inicio_monitoramento = time.time()
    
    def registrar_metrica(self, nome: str, valor: float, timestamp: float = None):
        """Registra métrica de performance"""
        if timestamp is None:
            timestamp = time.time()
        
        with self.lock:
            self.metricas[nome].append({
                'valor': valor,
                'timestamp': timestamp
            })
    
    def obter_metricas(self, nome: str, ultimos_n: int = 100) -> List[Dict]:
        """Obtém métricas específicas"""
        with self.lock:
            return self.metricas[nome][-ultimos_n:]
    
    def obter_estatisticas(self, nome: str) -> Dict[str, Any]:
        """Obtém estatísticas de uma métrica"""
        metricas = self.obter_metricas(nome)
        
        if not metricas:
            return {'erro': 'Nenhuma métrica encontrada'}
        
        valores = [m['valor'] for m in metricas]
        
        return {
            'total_registros': len(valores),
            'valor_medio': sum(valores) / len(valores),
            'valor_minimo': min(valores),
            'valor_maximo': max(valores),
            'ultimo_valor': valores[-1],
            'primeiro_registro': metricas[0]['timestamp'],
            'ultimo_registro': metricas[-1]['timestamp']
        }
    
    def obter_todas_metricas(self) -> Dict[str, Any]:
        """Obtém todas as métricas do sistema"""
        with self.lock:
            return {
                nome: self.obter_estatisticas(nome)
                for nome in self.metricas.keys()
            }
    
    def limpar_metricas_antigas(self, dias_para_manter: int = 7):
        """Remove métricas antigas"""
        tempo_limite = time.time() - (dias_para_manter * 24 * 3600)
        
        with self.lock:
            for nome in self.metricas:
                self.metricas[nome] = [
                    m for m in self.metricas[nome]
                    if m['timestamp'] > tempo_limite
                ]


class LoadBalancer:
    """Balanceador de carga para distribuir processamento"""
    
    def __init__(self, shard_manager: ShardManager):
        self.shard_manager = shard_manager
        self.carga_shards = defaultdict(int)
        self.lock = threading.Lock()
    
    def obter_shard_menos_carregado(self) -> str:
        """Obtém shard com menor carga"""
        with self.lock:
            if not self.carga_shards:
                return "shard_0"
            
            return min(self.carga_shards.keys(), key=lambda k: self.carga_shards[k])
    
    def incrementar_carga(self, shard_name: str):
        """Incrementa carga de um shard"""
        with self.lock:
            self.carga_shards[shard_name] += 1
    
    def decrementar_carga(self, shard_name: str):
        """Decrementa carga de um shard"""
        with self.lock:
            if self.carga_shards[shard_name] > 0:
                self.carga_shards[shard_name] -= 1
    
    def obter_estatisticas_carga(self) -> Dict[str, Any]:
        """Obtém estatísticas de carga"""
        with self.lock:
            if not self.carga_shards:
                return {'total_shards': 0, 'carga_media': 0}
            
            total_carga = sum(self.carga_shards.values())
            num_shards = len(self.carga_shards)
            
            return {
                'total_shards': num_shards,
                'carga_total': total_carga,
                'carga_media': total_carga / num_shards,
                'carga_por_shard': dict(self.carga_shards)
            }
