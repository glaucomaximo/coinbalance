"""
Sistema de Otimização de Banco de Dados - CoinBalance
Implementa índices, cache e otimizações de performance
"""

import sqlite3
import time
import json
import threading
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class DatabaseOptimizer:
    """Otimizador de performance do banco de dados"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.cache = {}
        self.cache_ttl = 300  # 5 minutos
        self.cache_timestamps = {}
        self.lock = threading.Lock()
        
    def criar_indices(self):
        """Cria índices para otimizar consultas frequentes"""
        with self.db_manager.lock:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            try:
                # Índices para tabela de blocos
                indices_blocos = [
                    "CREATE INDEX IF NOT EXISTS idx_blocos_indice ON blocos(indice)",
                    "CREATE INDEX IF NOT EXISTS idx_blocos_timestamp ON blocos(timestamp)",
                    "CREATE INDEX IF NOT EXISTS idx_blocos_hash_atual ON blocos(hash_atual)",
                    "CREATE INDEX IF NOT EXISTS idx_blocos_hash_anterior ON blocos(hash_anterior)"
                ]
                
                # Índices para tabela de transações
                indices_transacoes = [
                    "CREATE INDEX IF NOT EXISTS idx_transacoes_hash ON transacoes(hash_transacao)",
                    "CREATE INDEX IF NOT EXISTS idx_transacoes_remetente ON transacoes(remetente)",
                    "CREATE INDEX IF NOT EXISTS idx_transacoes_destinatario ON transacoes(destinatario)",
                    "CREATE INDEX IF NOT EXISTS idx_transacoes_bloco_id ON transacoes(bloco_id)",
                    "CREATE INDEX IF NOT EXISTS idx_transacoes_timestamp ON transacoes(timestamp)",
                    "CREATE INDEX IF NOT EXISTS idx_transacoes_valor ON transacoes(valor)"
                ]
                
                # Índices para tabela de carteiras (ajustados ao schema real)
                indices_carteiras = [
                    "CREATE INDEX IF NOT EXISTS idx_carteiras_endereco ON carteiras(endereco)",
                    "CREATE INDEX IF NOT EXISTS idx_carteiras_chave_publica ON carteiras(chave_publica)",
                    "CREATE INDEX IF NOT EXISTS idx_carteiras_saldo ON carteiras(saldo)"
                ]
                
                # Índices para tabela de nós (ajustados ao schema real)
                indices_nos = [
                    "CREATE INDEX IF NOT EXISTS idx_nos_endereco ON nos_rede(endereco)",
                    "CREATE INDEX IF NOT EXISTS idx_nos_ultima_sincronizacao ON nos_rede(ultima_sincronizacao)"
                ]
                
                # Executar todos os índices
                all_indices = indices_blocos + indices_transacoes + indices_carteiras + indices_nos
                
                for index_sql in all_indices:
                    cursor.execute(index_sql)
                    logger.info(f"Índice criado: {index_sql.split('idx_')[1].split(' ON ')[0]}")
                
                conn.commit()
                logger.info("✅ Todos os índices foram criados com sucesso!")
                
            except Exception as e:
                logger.error(f"Erro ao criar índices: {e}")
                conn.rollback()
            finally:
                conn.close()
    
    def analisar_performance(self) -> Dict[str, Any]:
        """Analisa performance do banco de dados"""
        with self.db_manager.lock:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            try:
                # Estatísticas gerais
                cursor.execute("SELECT COUNT(*) FROM blocos")
                total_blocos = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM transacoes")
                total_transacoes = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM carteiras")
                total_carteiras = cursor.fetchone()[0]
                
                # Tamanho do banco
                cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
                db_size = cursor.fetchone()[0]
                
                # Análise de índices
                cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'")
                indices = cursor.fetchall()
                
                # Consultas mais lentas (simulação)
                start_time = time.time()
                cursor.execute("SELECT * FROM blocos ORDER BY timestamp DESC LIMIT 10")
                cursor.fetchall()
                query_time = time.time() - start_time
                
                return {
                    "total_blocos": total_blocos,
                    "total_transacoes": total_transacoes,
                    "total_carteiras": total_carteiras,
                    "db_size_bytes": db_size,
                    "db_size_mb": round(db_size / (1024 * 1024), 2),
                    "indices_count": len(indices),
                    "indices": [idx[0] for idx in indices],
                    "query_time_ms": round(query_time * 1000, 2),
                    "timestamp": time.time()
                }
                
            except Exception as e:
                logger.error(f"Erro ao analisar performance: {e}")
                return {"error": str(e)}
            finally:
                conn.close()
    
    def obter_blocos_otimizado(self, limite: int = 10, offset: int = 0) -> List[Dict]:
        """Obtém blocos com otimização de cache"""
        cache_key = f"blocos_{limite}_{offset}"
        
        # Verificar cache
        if self._verificar_cache(cache_key):
            logger.debug(f"Cache hit para {cache_key}")
            return self.cache[cache_key]
        
        # Consulta otimizada
        with self.db_manager.lock:
            conn = sqlite3.connect(self.db_manager.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    SELECT id, indice, timestamp, hash_anterior, hash_atual, prova, dados, criado_em
                    FROM blocos 
                    ORDER BY indice DESC 
                    LIMIT ? OFFSET ?
                """, (limite, offset))
                
                blocos = [dict(row) for row in cursor.fetchall()]
                
                # Armazenar no cache
                self._armazenar_cache(cache_key, blocos)
                
                return blocos
                
            except Exception as e:
                logger.error(f"Erro ao obter blocos: {e}")
                return []
            finally:
                conn.close()
    
    def obter_transacoes_otimizado(self, remetente: str = None, destinatario: str = None, 
                                  limite: int = 50, offset: int = 0) -> List[Dict]:
        """Obtém transações com otimização de cache e filtros"""
        cache_key = f"transacoes_{remetente}_{destinatario}_{limite}_{offset}"
        
        # Verificar cache
        if self._verificar_cache(cache_key):
            logger.debug(f"Cache hit para {cache_key}")
            return self.cache[cache_key]
        
        # Construir query dinamicamente
        where_conditions = []
        params = []
        
        if remetente:
            where_conditions.append("remetente = ?")
            params.append(remetente)
        
        if destinatario:
            where_conditions.append("destinatario = ?")
            params.append(destinatario)
        
        where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        params.extend([limite, offset])
        
        with self.db_manager.lock:
            conn = sqlite3.connect(self.db_manager.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            try:
                query = f"""
                    SELECT id, hash_transacao, bloco_id, remetente, destinatario, 
                           valor, taxa, timestamp, status
                    FROM transacoes 
                    {where_clause}
                    ORDER BY timestamp DESC 
                    LIMIT ? OFFSET ?
                """
                
                cursor.execute(query, params)
                transacoes = [dict(row) for row in cursor.fetchall()]
                
                # Armazenar no cache
                self._armazenar_cache(cache_key, transacoes)
                
                return transacoes
                
            except Exception as e:
                logger.error(f"Erro ao obter transações: {e}")
                return []
            finally:
                conn.close()
    
    def obter_estatisticas_carteira_otimizado(self, endereco: str) -> Dict[str, Any]:
        """Obtém estatísticas de carteira com cache"""
        cache_key = f"carteira_stats_{endereco}"
        
        # Verificar cache
        if self._verificar_cache(cache_key):
            logger.debug(f"Cache hit para {cache_key}")
            return self.cache[cache_key]
        
        with self.db_manager.lock:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            try:
                # Transações enviadas
                cursor.execute("""
                    SELECT COUNT(*), COALESCE(SUM(valor), 0), COALESCE(SUM(taxa), 0)
                    FROM transacoes 
                    WHERE remetente = ?
                """, (endereco,))
                enviadas = cursor.fetchone()
                
                # Transações recebidas
                cursor.execute("""
                    SELECT COUNT(*), COALESCE(SUM(valor), 0)
                    FROM transacoes 
                    WHERE destinatario = ?
                """, (endereco,))
                recebidas = cursor.fetchone()
                
                # Saldo atual (ajustado para coluna `saldo`)
                cursor.execute("SELECT saldo FROM carteiras WHERE endereco = ?", (endereco,))
                saldo = cursor.fetchone()
                
                stats = {
                    "endereco": endereco,
                    "saldo_atual": saldo[0] if saldo else 0,
                    "transacoes_enviadas": enviadas[0],
                    "total_enviado": enviadas[1],
                    "total_taxas_pagas": enviadas[2],
                    "transacoes_recebidas": recebidas[0],
                    "total_recebido": recebidas[1],
                    "timestamp": time.time()
                }
                
                # Armazenar no cache
                self._armazenar_cache(cache_key, stats)
                
                return stats
                
            except Exception as e:
                logger.error(f"Erro ao obter estatísticas da carteira: {e}")
                return {"error": str(e)}
            finally:
                conn.close()
    
    def _verificar_cache(self, key: str) -> bool:
        """Verifica se item está no cache e não expirou"""
        with self.lock:
            if key in self.cache:
                if time.time() - self.cache_timestamps[key] < self.cache_ttl:
                    return True
                else:
                    # Remover item expirado
                    del self.cache[key]
                    del self.cache_timestamps[key]
            return False
    
    def _armazenar_cache(self, key: str, data: Any):
        """Armazena item no cache"""
        with self.lock:
            self.cache[key] = data
            self.cache_timestamps[key] = time.time()
            
            # Limitar tamanho do cache (máximo 100 itens)
            if len(self.cache) > 100:
                # Remover item mais antigo
                oldest_key = min(self.cache_timestamps.keys(), 
                               key=lambda k: self.cache_timestamps[k])
                del self.cache[oldest_key]
                del self.cache_timestamps[oldest_key]
    
    def limpar_cache(self):
        """Limpa todo o cache"""
        with self.lock:
            self.cache.clear()
            self.cache_timestamps.clear()
            logger.info("Cache limpo com sucesso!")
    
    def obter_estatisticas_cache(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache"""
        with self.lock:
            return {
                "itens_em_cache": len(self.cache),
                "ttl_segundos": self.cache_ttl,
                "chaves": list(self.cache.keys()),
                "timestamp": time.time()
            }
    
    def otimizar_banco(self):
        """Executa otimizações gerais no banco"""
        with self.db_manager.lock:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            try:
                # ANALYZE para atualizar estatísticas
                cursor.execute("ANALYZE")
                
                # VACUUM para compactar banco
                cursor.execute("VACUUM")
                
                # Configurações de performance
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA cache_size=10000")
                cursor.execute("PRAGMA temp_store=MEMORY")
                
                conn.commit()
                logger.info("✅ Banco de dados otimizado com sucesso!")
                
            except Exception as e:
                logger.error(f"Erro ao otimizar banco: {e}")
                conn.rollback()
            finally:
                conn.close()
