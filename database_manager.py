"""
Gerenciador de Banco de Dados para Blockchain
Implementa persistência segura e backup automático
"""

import sqlite3
import json
import os
import shutil
from datetime import datetime
from typing import List, Dict, Any, Optional
import threading


class DatabaseManager:
    """Gerencia persistência de dados da blockchain"""
    
    def __init__(self, db_path: str = "blockchain.db"):
        self.db_path = db_path
        self.backup_dir = "backups"
        self.lock = threading.Lock()
        self._inicializar_banco()
    
    def _inicializar_banco(self):
        """Inicializa banco de dados com tabelas necessárias"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabela de blocos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blocos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    indice INTEGER UNIQUE NOT NULL,
                    timestamp REAL NOT NULL,
                    hash_anterior TEXT,
                    hash_atual TEXT UNIQUE NOT NULL,
                    prova INTEGER NOT NULL,
                    dados TEXT NOT NULL,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de transações
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hash_transacao TEXT UNIQUE NOT NULL,
                    bloco_id INTEGER,
                    remetente TEXT NOT NULL,
                    destinatario TEXT NOT NULL,
                    valor REAL NOT NULL,
                    taxa REAL DEFAULT 0.0,
                    assinatura TEXT NOT NULL,
                    chave_publica TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    dados_extra TEXT,
                    status TEXT DEFAULT 'pendente',
                    FOREIGN KEY (bloco_id) REFERENCES blocos (id)
                )
            ''')

            # Migração leve: garantir coluna 'taxa' em bases existentes
            cursor.execute("PRAGMA table_info(transacoes)")
            cols = [row[1] for row in cursor.fetchall()]
            if 'taxa' not in cols:
                try:
                    cursor.execute("ALTER TABLE transacoes ADD COLUMN taxa REAL DEFAULT 0.0")
                except Exception:
                    pass
            
            # Tabela de carteiras
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS carteiras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    endereco TEXT UNIQUE NOT NULL,
                    saldo REAL DEFAULT 0.0,
                    chave_publica TEXT NOT NULL,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de nós da rede
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS nos_rede (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    endereco TEXT UNIQUE NOT NULL,
                    ultima_sincronizacao TIMESTAMP,
                    status TEXT DEFAULT 'ativo',
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tabela de usuários (autenticação)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT DEFAULT 'user',
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Índices para performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_blocos_indice ON blocos(indice)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_transacoes_hash ON transacoes(hash_transacao)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_transacoes_remetente ON transacoes(remetente)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_carteiras_endereco ON carteiras(endereco)')
            
            conn.commit()
            conn.close()
    
    def salvar_bloco(self, bloco: Dict[str, Any]) -> bool:
        """Salva bloco no banco de dados"""
        try:
            with self.lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO blocos 
                    (indice, timestamp, hash_anterior, hash_atual, prova, dados)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    bloco['indice'],
                    bloco.get('carimbo_temporal', bloco.get('timestamp')),
                    bloco.get('fragmento_anterior'),
                    bloco.get('hash_atual'),
                    bloco['prova'],
                    json.dumps(bloco)
                ))
                
                conn.commit()
                conn.close()
                return True
        except Exception as e:
            print(f"Erro ao salvar bloco: {e}")
            return False
    
    def salvar_transacao(self, transacao: Dict[str, Any], bloco_id: int = None) -> bool:
        """Salva transação no banco de dados"""
        try:
            with self.lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Gerar hash da transação
                hash_transacao = self._gerar_hash_transacao(transacao)
                
                cursor.execute('''
                    INSERT OR REPLACE INTO transacoes 
                    (hash_transacao, bloco_id, remetente, destinatario, valor, taxa,
                     assinatura, chave_publica, timestamp, dados_extra, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    hash_transacao,
                    bloco_id,
                    transacao['remetente'],
                    transacao['destinatario'],
                    transacao['valor'],
                    float(transacao.get('taxa', 0.0)),
                    transacao.get('assinatura', ''),
                    transacao.get('chave_publica', ''),
                    transacao['timestamp'],
                    json.dumps(transacao.get('dados_extra', {})),
                    'confirmada' if bloco_id else 'pendente'
                ))
                
                conn.commit()
                conn.close()
                return True
        except Exception as e:
            print(f"Erro ao salvar transação: {e}")
            return False
    
    def obter_bloco(self, indice: int) -> Optional[Dict]:
        """Obtém bloco por índice"""
        try:
            with self.lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('SELECT dados FROM blocos WHERE indice = ?', (indice,))
                resultado = cursor.fetchone()
                
                conn.close()
                
                if resultado:
                    return json.loads(resultado[0])
                return None
        except Exception as e:
            print(f"Erro ao obter bloco: {e}")
            return None
    
    def obter_ultimo_bloco(self) -> Optional[Dict]:
        """Obtém último bloco da cadeia"""
        try:
            with self.lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT dados FROM blocos 
                    ORDER BY indice DESC LIMIT 1
                ''')
                resultado = cursor.fetchone()
                
                conn.close()
                
                if resultado:
                    return json.loads(resultado[0])
                return None
        except Exception as e:
            print(f"Erro ao obter último bloco: {e}")
            return None
    
    def obter_todos_blocos(self) -> List[Dict]:
        """Obtém todos os blocos da cadeia"""
        try:
            with self.lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('SELECT dados FROM blocos ORDER BY indice')
                resultados = cursor.fetchall()
                
                conn.close()
                
                return [json.loads(resultado[0]) for resultado in resultados]
        except Exception as e:
            print(f"Erro ao obter blocos: {e}")
            return []
    
    def atualizar_saldo_carteira(self, endereco: str, novo_saldo: float) -> bool:
        """Atualiza saldo de uma carteira"""
        try:
            with self.lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO carteiras 
                    (endereco, saldo, chave_publica, atualizado_em)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ''', (endereco, novo_saldo, ''))
                
                conn.commit()
                conn.close()
                return True
        except Exception as e:
            print(f"Erro ao atualizar saldo: {e}")
            return False
    
    def obter_saldo_carteira(self, endereco: str) -> float:
        """Obtém saldo de uma carteira"""
        try:
            with self.lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('SELECT saldo FROM carteiras WHERE endereco = ?', (endereco,))
                resultado = cursor.fetchone()
                
                conn.close()
                
                return resultado[0] if resultado else 0.0
        except Exception as e:
            print(f"Erro ao obter saldo: {e}")
            return 0.0
    
    def _gerar_hash_transacao(self, transacao: Dict) -> str:
        """Gera hash único para transação"""
        import hashlib
        transacao_str = json.dumps(transacao, sort_keys=True)
        return hashlib.sha256(transacao_str.encode()).hexdigest()
    
    def criar_backup(self) -> str:
        """Cria backup do banco de dados"""
        try:
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"blockchain_backup_{timestamp}.db")
            
            shutil.copy2(self.db_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
            return ""
    
    def restaurar_backup(self, backup_path: str) -> bool:
        """Restaura backup do banco de dados"""
        try:
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, self.db_path)
                return True
            return False
        except Exception as e:
            print(f"Erro ao restaurar backup: {e}")
            return False
    
    def limpar_backups_antigos(self, dias_para_manter: int = 30):
        """Remove backups antigos"""
        try:
            if not os.path.exists(self.backup_dir):
                return
            
            import time
            tempo_limite = time.time() - (dias_para_manter * 24 * 60 * 60)
            
            for arquivo in os.listdir(self.backup_dir):
                caminho_arquivo = os.path.join(self.backup_dir, arquivo)
                if os.path.isfile(caminho_arquivo) and os.path.getmtime(caminho_arquivo) < tempo_limite:
                    os.remove(caminho_arquivo)
        except Exception as e:
            print(f"Erro ao limpar backups: {e}")

    # ===== Usuários =====
    def criar_usuario(self, username: str, password_hash: str, role: str = 'user') -> bool:
        try:
            with self.lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO usuarios (username, password_hash, role)
                    VALUES (?, ?, ?)
                    """,
                    (username, password_hash, role),
                )
                conn.commit()
                conn.close()
                return True
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return False

    def obter_usuario(self, username: str) -> Optional[Dict[str, Any]]:
        try:
            with self.lock:
                conn = sqlite3.connect(self.db_path)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT id, username, password_hash, role, criado_em FROM usuarios WHERE username = ?", (username,))
                row = cursor.fetchone()
                conn.close()
                return dict(row) if row else None
        except Exception as e:
            print(f"Erro ao obter usuário: {e}")
            return None
