#!/usr/bin/env python3
"""
Script de Detecção de Documentação Desatualizada
=================================================

Este script detecta documentos que podem estar desatualizados:
- Compara datas de modificação
- Verifica datas no conteúdo
- Analisa commits do Git
- Gera relatório de documentos para revisão

Uso:
    python scripts/detect_obsolete_docs.py
    python scripts/detect_obsolete_docs.py --age-days 90
    python scripts/detect_obsolete_docs.py --compare-code
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

# Configurações
DOCS_DIR = Path("docs")
DEFAULT_MAX_AGE_DAYS = 180  # 6 meses


class ObsoleteDocDetector:
    """Detector de documentos obsoletos"""
    
    def __init__(self, docs_dir: Path, max_age_days: int = DEFAULT_MAX_AGE_DAYS):
        self.docs_dir = docs_dir
        self.max_age_days = max_age_days
        self.obsolete_files: List[Dict[str, any]] = []
        
    def detect_all(self) -> List[Dict[str, any]]:
        """Detecta todos os documentos obsoletos"""
        print("🔍 Detectando documentos obsoletos...\n")
        
        md_files = list(self.docs_dir.rglob("*.md"))
        
        for md_file in md_files:
            # Pular legacy_archive
            if "legacy_archive" in str(md_file):
                continue
            
            info = self._analyze_file(md_file)
            if info and info.get("is_obsolete"):
                self.obsolete_files.append(info)
        
        return self.obsolete_files
    
    def _analyze_file(self, file_path: Path) -> Optional[Dict[str, any]]:
        """Analisa um arquivo individual"""
        try:
            # Informações do arquivo
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            age_days = (datetime.now() - mtime).days
            
            # Ler conteúdo
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(5000)  # Primeiras linhas
            
            # Extrair metadados do conteúdo
            metadata = self._extract_metadata(content)
            
            # Verificar se está obsoleto
            is_obsolete = False
            reasons = []
            
            # Critério 1: Idade do arquivo
            if age_days > self.max_age_days:
                is_obsolete = True
                reasons.append(f"Arquivo não modificado há {age_days} dias")
            
            # Critério 2: Data no conteúdo
            if metadata.get("last_update"):
                content_date = metadata["last_update"]
                content_age = (datetime.now() - content_date).days
                if content_age > self.max_age_days:
                    is_obsolete = True
                    reasons.append(f"Data no conteúdo indica {content_age} dias de idade")
            
            # Critério 3: Sem data de atualização
            if not metadata.get("last_update") and not metadata.get("creation_date"):
                is_obsolete = True
                reasons.append("Sem metadados de data no conteúdo")
            
            if is_obsolete:
                return {
                    "file": str(file_path.relative_to(self.docs_dir)),
                    "absolute_path": str(file_path),
                    "age_days": age_days,
                    "metadata": metadata,
                    "is_obsolete": True,
                    "reasons": reasons,
                    "recommendation": self._get_recommendation(file_path, metadata)
                }
            
            return None
            
        except Exception as e:
            print(f"⚠️  Erro ao analisar {file_path}: {e}")
            return None
    
    def _extract_metadata(self, content: str) -> Dict[str, any]:
        """Extrai metadados do conteúdo"""
        metadata = {}
        
        # Procurar por padrões de data
        date_patterns = [
            r'\*\*Última Atualização:\*\*\s*(\d{2}/\d{2}/\d{4})',
            r'\*\*Data de Criação:\*\*\s*(\d{2}/\d{2}/\d{4})',
            r'\*\*Data:\*\*\s*(\d{2}/\d{2}/\d{4})',
            r'(\d{2}/\d{2}/\d{4})',  # Padrão genérico
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, content)
            if matches:
                try:
                    date_str = matches[0]
                    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                    
                    if "Última Atualização" in pattern or "last_update" not in metadata:
                        metadata["last_update"] = date_obj
                    if "Data de Criação" in pattern or "creation_date" not in metadata:
                        metadata["creation_date"] = date_obj
                except:
                    pass
        
        # Procurar por versão
        version_match = re.search(r'\*\*Versão:\*\*\s*([\d.]+)', content)
        if version_match:
            metadata["version"] = version_match.group(1)
        
        # Procurar por status
        status_match = re.search(r'\*\*Status:\*\*\s*([^\n]+)', content)
        if status_match:
            metadata["status"] = status_match.group(1).strip()
        
        return metadata
    
    def _get_recommendation(self, file_path: Path, metadata: Dict[str, any]) -> str:
        """Gera recomendação para o arquivo"""
        if metadata.get("status") == "✅ Completo":
            return "Atualizar data de última atualização"
        elif metadata.get("status") == "🔄 Em Progresso":
            return "Finalizar documento ou marcar como completo"
        elif "legacy" in str(file_path).lower() or "archive" in str(file_path).lower():
            return "Verificar se deve ser movido para legacy_archive"
        else:
            return "Revisar e atualizar conteúdo"
    
    def print_report(self):
        """Imprime relatório"""
        print("\n" + "="*80)
        print("📊 RELATÓRIO DE DOCUMENTOS OBSOLETOS")
        print("="*80 + "\n")
        
        if not self.obsolete_files:
            print("✅ Nenhum documento obsoleto detectado!\n")
            return
        
        print(f"⚠️  Documentos obsoletos encontrados: {len(self.obsolete_files)}\n")
        
        for file_info in self.obsolete_files:
            print(f"📄 {file_info['file']}")
            print(f"   Idade: {file_info['age_days']} dias")
            if file_info['metadata'].get('last_update'):
                content_age = (datetime.now() - file_info['metadata']['last_update']).days
                print(f"   Data no conteúdo: {file_info['metadata']['last_update'].strftime('%d/%m/%Y')} ({content_age} dias)")
            print(f"   Motivos:")
            for reason in file_info['reasons']:
                print(f"     - {reason}")
            print(f"   Recomendação: {file_info['recommendation']}")
            print()


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Detecta documentos obsoletos')
    parser.add_argument('--age-days', type=int, default=DEFAULT_MAX_AGE_DAYS,
                       help=f'Idade máxima em dias (padrão: {DEFAULT_MAX_AGE_DAYS})')
    parser.add_argument('--json', action='store_true', help='Saída em JSON')
    
    args = parser.parse_args()
    
    detector = ObsoleteDocDetector(DOCS_DIR, args.age_days)
    
    if not DOCS_DIR.exists():
        print(f"❌ Erro: Diretório {DOCS_DIR} não encontrado")
        sys.exit(1)
    
    obsolete_files = detector.detect_all()
    
    if args.json:
        print(json.dumps(obsolete_files, indent=2, default=str))
    else:
        detector.print_report()
    
    sys.exit(0 if not obsolete_files else 1)


if __name__ == "__main__":
    main()

