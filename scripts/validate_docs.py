#!/usr/bin/env python3
"""
Script de Validação de Documentação
====================================

Este script valida a documentação técnica do projeto CoinBalance:
- Verifica links quebrados
- Valida estrutura de documentos
- Detecta documentos desatualizados
- Verifica conformidade com padrões

Uso:
    python scripts/validate_docs.py
    python scripts/validate_docs.py --check-links
    python scripts/validate_docs.py --check-obsolete
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import json

# Configurações
DOCS_DIR = Path("docs")
MAX_AGE_DAYS = 180  # 6 meses
REQUIRED_METADATA = ["Versão", "Data de Criação", "Última Atualização", "Status"]


class DocValidator:
    """Validador de documentação"""
    
    def __init__(self, docs_dir: Path):
        self.docs_dir = docs_dir
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        
    def validate_all(self) -> Dict[str, any]:
        """Executa todas as validações"""
        print("🔍 Iniciando validação de documentação...\n")
        
        # Encontrar todos os arquivos Markdown
        md_files = list(self.docs_dir.rglob("*.md"))
        
        results = {
            "total_files": len(md_files),
            "files_with_errors": [],
            "files_with_warnings": [],
            "obsolete_files": [],
            "files_without_metadata": [],
            "broken_links": []
        }
        
        for md_file in md_files:
            # Pular arquivos em legacy_archive
            if "legacy_archive" in str(md_file):
                continue
                
            print(f"📄 Validando: {md_file.relative_to(self.docs_dir)}")
            
            # Validar metadados
            has_metadata = self._validate_metadata(md_file)
            if not has_metadata:
                results["files_without_metadata"].append(str(md_file.relative_to(self.docs_dir)))
            
            # Validar estrutura
            self._validate_structure(md_file)
            
            # Verificar idade
            is_obsolete = self._check_obsolete(md_file)
            if is_obsolete:
                results["obsolete_files"].append(str(md_file.relative_to(self.docs_dir)))
        
        # Validar links
        broken_links = self._validate_links()
        results["broken_links"] = broken_links
        
        # Compilar resultados
        results["files_with_errors"] = list(set(self.errors))
        results["files_with_warnings"] = list(set(self.warnings))
        
        return results
    
    def _validate_metadata(self, file_path: Path) -> bool:
        """Valida se o arquivo tem metadados obrigatórios"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(2000)  # Ler primeiras linhas
                
            missing_metadata = []
            for metadata in REQUIRED_METADATA:
                if metadata not in content:
                    missing_metadata.append(metadata)
            
            if missing_metadata:
                self.warnings.append(
                    f"{file_path.name}: Metadados faltando: {', '.join(missing_metadata)}"
                )
                return False
                
            return True
        except Exception as e:
            self.errors.append(f"{file_path.name}: Erro ao ler arquivo: {e}")
            return False
    
    def _validate_structure(self, file_path: Path) -> bool:
        """Valida estrutura básica do documento"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Verificar se tem título H1
            has_h1 = any(line.startswith('# ') for line in lines[:10])
            if not has_h1:
                self.warnings.append(f"{file_path.name}: Sem título H1")
            
            # Verificar se tem sumário executivo
            has_summary = any('sumário' in line.lower() or 'sumario' in line.lower() 
                            for line in lines[:20])
            if not has_summary:
                self.warnings.append(f"{file_path.name}: Sem sumário executivo")
            
            return True
        except Exception as e:
            self.errors.append(f"{file_path.name}: Erro ao validar estrutura: {e}")
            return False
    
    def _check_obsolete(self, file_path: Path) -> bool:
        """Verifica se arquivo está obsoleto"""
        try:
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            age_days = (datetime.now() - mtime).days
            
            if age_days > MAX_AGE_DAYS:
                # Verificar se tem data de atualização no conteúdo
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(2000)
                    
                # Procurar por data de atualização
                date_pattern = r'\d{2}/\d{2}/\d{4}'
                dates = re.findall(date_pattern, content)
                
                if dates:
                    # Tentar encontrar a data mais recente
                    latest_date = None
                    for date_str in dates:
                        try:
                            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                            if latest_date is None or date_obj > latest_date:
                                latest_date = date_obj
                        except:
                            pass
                    
                    if latest_date:
                        content_age = (datetime.now() - latest_date).days
                        if content_age > MAX_AGE_DAYS:
                            self.warnings.append(
                                f"{file_path.name}: Possível documento obsoleto "
                                f"(última atualização há {content_age} dias)"
                            )
                            return True
                else:
                    # Sem data no conteúdo, usar mtime
                    self.warnings.append(
                        f"{file_path.name}: Sem data de atualização no conteúdo "
                        f"(arquivo modificado há {age_days} dias)"
                    )
                    return True
                    
            return False
        except Exception as e:
            self.errors.append(f"{file_path.name}: Erro ao verificar obsoleto: {e}")
            return False
    
    def _validate_links(self) -> List[Dict[str, str]]:
        """Valida links internos"""
        broken_links = []
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        md_files = list(self.docs_dir.rglob("*.md"))
        
        for md_file in md_files:
            if "legacy_archive" in str(md_file):
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                links = re.findall(link_pattern, content)
                
                for link_text, link_path in links:
                    # Pular links externos
                    if link_path.startswith('http'):
                        continue
                    
                    # Resolver caminho relativo
                    if link_path.startswith('/'):
                        target_path = self.docs_dir / link_path[1:]
                    else:
                        target_path = md_file.parent / link_path
                    
                    # Verificar se arquivo existe
                    if not target_path.exists():
                        # Tentar com .md
                        if not target_path.suffix:
                            target_path = target_path.with_suffix('.md')
                        
                        if not target_path.exists():
                            broken_links.append({
                                "file": str(md_file.relative_to(self.docs_dir)),
                                "link": link_text,
                                "path": link_path
                            })
            except Exception as e:
                self.errors.append(f"{md_file.name}: Erro ao validar links: {e}")
        
        return broken_links
    
    def print_report(self, results: Dict[str, any]):
        """Imprime relatório de validação"""
        print("\n" + "="*80)
        print("📊 RELATÓRIO DE VALIDAÇÃO")
        print("="*80 + "\n")
        
        print(f"📁 Total de arquivos: {results['total_files']}")
        print(f"🔴 Arquivos com erros: {len(results['files_with_errors'])}")
        print(f"🟡 Arquivos com avisos: {len(results['files_with_warnings'])}")
        print(f"⚠️  Arquivos obsoletos: {len(results['obsolete_files'])}")
        print(f"📄 Arquivos sem metadados: {len(results['files_without_metadata'])}")
        print(f"🔗 Links quebrados: {len(results['broken_links'])}\n")
        
        # Detalhes de erros
        if results['files_with_errors']:
            print("🔴 ERROS:")
            for error in results['files_with_errors'][:10]:
                print(f"  - {error}")
            if len(results['files_with_errors']) > 10:
                print(f"  ... e mais {len(results['files_with_errors']) - 10} erros")
            print()
        
        # Detalhes de avisos
        if results['files_with_warnings']:
            print("🟡 AVISOS:")
            for warning in results['files_with_warnings'][:10]:
                print(f"  - {warning}")
            if len(results['files_with_warnings']) > 10:
                print(f"  ... e mais {len(results['files_with_warnings']) - 10} avisos")
            print()
        
        # Links quebrados
        if results['broken_links']:
            print("🔗 LINKS QUEBRADOS:")
            for link in results['broken_links'][:10]:
                print(f"  - {link['file']}: [{link['link']}]({link['path']})")
            if len(results['broken_links']) > 10:
                print(f"  ... e mais {len(results['broken_links']) - 10} links quebrados")
            print()
        
        # Resumo final
        if not results['files_with_errors'] and not results['broken_links']:
            print("✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
            print("   Todos os documentos estão em conformidade.\n")
        else:
            print("⚠️  VALIDAÇÃO CONCLUÍDA COM PROBLEMAS")
            print("   Revise os erros e avisos acima.\n")


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Valida documentação do projeto')
    parser.add_argument('--check-links', action='store_true', help='Verificar apenas links')
    parser.add_argument('--check-obsolete', action='store_true', help='Verificar apenas obsoletos')
    parser.add_argument('--json', action='store_true', help='Saída em JSON')
    
    args = parser.parse_args()
    
    validator = DocValidator(DOCS_DIR)
    
    if not DOCS_DIR.exists():
        print(f"❌ Erro: Diretório {DOCS_DIR} não encontrado")
        sys.exit(1)
    
    if args.check_links:
        broken_links = validator._validate_links()
        if args.json:
            print(json.dumps({"broken_links": broken_links}, indent=2))
        else:
            print(f"\n🔗 Links quebrados encontrados: {len(broken_links)}")
            for link in broken_links:
                print(f"  - {link['file']}: [{link['link']}]({link['path']})")
    elif args.check_obsolete:
        md_files = list(DOCS_DIR.rglob("*.md"))
        obsolete = []
        for md_file in md_files:
            if "legacy_archive" not in str(md_file):
                if validator._check_obsolete(md_file):
                    obsolete.append(str(md_file.relative_to(DOCS_DIR)))
        if args.json:
            print(json.dumps({"obsolete_files": obsolete}, indent=2))
        else:
            print(f"\n⚠️  Arquivos obsoletos: {len(obsolete)}")
            for file in obsolete:
                print(f"  - {file}")
    else:
        results = validator.validate_all()
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            validator.print_report(results)
    
    # Exit code baseado em erros
    if validator.errors:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

