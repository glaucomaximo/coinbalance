#!/usr/bin/env python3
"""
Script para validar todas as disciplinas de engenharia de software implementadas
no projeto CoinBalance.

Este script verifica:
- Existência de documentos de disciplinas
- Conformidade com padrões internacionais
- Completude dos artefatos
- Qualidade da documentação
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class DisciplinaValidator:
    """Validador de disciplinas de engenharia de software."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.docs_dir = self.project_root / "docs"
        self.engenharia_dir = self.docs_dir / "engenharia"
        self.results = {
            "disciplinas_completas": [],
            "disciplinas_parciais": [],
            "disciplinas_faltantes": [],
            "problemas": [],
            "recomendacoes": []
        }
    
    def validate_disciplinas(self) -> Dict:
        """Valida todas as disciplinas de engenharia."""
        print("🏗️ Validação de Disciplinas de Engenharia - CoinBalance")
        print("=" * 60)
        
        # Disciplinas obrigatórias
        disciplinas = {
            "gestao-requisitos": {
                "arquivo": "gestao-requisitos.md",
                "titulo": "Gestão de Requisitos",
                "padroes": ["IEEE 830", "ISO/IEC 25010"],
                "artefatos_minimos": 5
            },
            "arquitetura-software": {
                "arquivo": "arquitetura-software.md", 
                "titulo": "Arquitetura de Software",
                "padroes": ["ISO/IEC 42010", "IEEE 1471"],
                "artefatos_minimos": 7
            },
            "gestao-configuracao": {
                "arquivo": "gestao-configuracao.md",
                "titulo": "Gestão de Configuração", 
                "padroes": ["IEEE 828", "ISO/IEC 12207"],
                "artefatos_minimos": 6
            },
            "gestao-projeto": {
                "arquivo": "gestao-projeto.md",
                "titulo": "Gestão de Projeto",
                "padroes": ["PMI PMBOK", "ISO 21500"],
                "artefatos_minimos": 7
            },
            "gestao-qualidade": {
                "arquivo": "gestao-qualidade.md",
                "titulo": "Gestão de Qualidade",
                "padroes": ["ISO/IEC 25010", "ISO 9001"],
                "artefatos_minimos": 6
            },
            "gestao-riscos": {
                "arquivo": "gestao-riscos.md",
                "titulo": "Gestão de Riscos",
                "padroes": ["ISO 31000", "PMI PMBOK"],
                "artefatos_minimos": 5
            },
            "gestao-mudancas": {
                "arquivo": "gestao-mudancas.md",
                "titulo": "Gestão de Mudanças",
                "padroes": ["ITIL", "ISO/IEC 20000"],
                "artefatos_minimos": 4
            },
            "gestao-testes": {
                "arquivo": "gestao-testes.md",
                "titulo": "Gestão de Testes",
                "padroes": ["ISO/IEC 29119", "IEEE 829"],
                "artefatos_minimos": 6
            },
            "gestao-deploy": {
                "arquivo": "gestao-deploy.md",
                "titulo": "Gestão de Deploy",
                "padroes": ["DevOps", "12-Factor App"],
                "artefatos_minimos": 5
            },
            "gestao-operacoes": {
                "arquivo": "gestao-operacoes.md",
                "titulo": "Gestão de Operações",
                "padroes": ["ITIL", "ISO/IEC 20000"],
                "artefatos_minimos": 6
            }
        }
        
        print(f"\n📋 Verificando {len(disciplinas)} disciplinas...")
        
        for disciplina_id, config in disciplinas.items():
            self._validate_disciplina(disciplina_id, config)
        
        self._validate_documento_consolidado()
        self._validate_estrutura_projeto()
        self._generate_report()
        
        return self.results
    
    def _validate_disciplina(self, disciplina_id: str, config: Dict):
        """Valida uma disciplina específica."""
        arquivo_path = self.engenharia_dir / config["arquivo"]
        
        print(f"\n🔍 Verificando {config['titulo']}...")
        
        if not arquivo_path.exists():
            self.results["disciplinas_faltantes"].append({
                "id": disciplina_id,
                "titulo": config["titulo"],
                "arquivo": config["arquivo"],
                "problema": "Arquivo não encontrado"
            })
            print(f"  ❌ Arquivo não encontrado: {config['arquivo']}")
            return
        
        # Verificar conteúdo do arquivo
        try:
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Verificações básicas
            verificacoes = self._check_conteudo_disciplina(conteudo, config)
            
            if verificacoes["completa"]:
                self.results["disciplinas_completas"].append({
                    "id": disciplina_id,
                    "titulo": config["titulo"],
                    "arquivo": config["arquivo"],
                    "verificacoes": verificacoes
                })
                print(f"  ✅ {config['titulo']} - COMPLETA")
            else:
                self.results["disciplinas_parciais"].append({
                    "id": disciplina_id,
                    "titulo": config["titulo"],
                    "arquivo": config["arquivo"],
                    "verificacoes": verificacoes
                })
                print(f"  ⚠️ {config['titulo']} - PARCIAL")
                
        except Exception as e:
            self.results["problemas"].append({
                "disciplina": disciplina_id,
                "problema": f"Erro ao ler arquivo: {str(e)}"
            })
            print(f"  ❌ Erro ao ler arquivo: {str(e)}")
    
    def _check_conteudo_disciplina(self, conteudo: str, config: Dict) -> Dict:
        """Verifica o conteúdo de uma disciplina."""
        verificacoes = {
            "completa": True,
            "problemas": [],
            "artefatos_encontrados": 0,
            "padroes_encontrados": 0
        }
        
        # Verificar seções obrigatórias
        secoes_obrigatorias = [
            "VISÃO GERAL",
            "OBJETIVOS", 
            "PROCESSO",
            "ARTEFATOS",
            "COMPLIANCE"
        ]
        
        for secao in secoes_obrigatorias:
            if secao not in conteudo:
                verificacoes["problemas"].append(f"Seção '{secao}' não encontrada")
                verificacoes["completa"] = False
        
        # Verificar padrões mencionados
        for padrao in config["padroes"]:
            if padrao in conteudo:
                verificacoes["padroes_encontrados"] += 1
        
        # Verificar artefatos (contar seções específicas)
        artefatos_keywords = [
            "documento", "processo", "ferramenta", "métrica", 
            "checklist", "relatório", "template"
        ]
        
        for keyword in artefatos_keywords:
            if keyword in conteudo.lower():
                verificacoes["artefatos_encontrados"] += 1
        
        # Verificar se tem artefatos mínimos
        if verificacoes["artefatos_encontrados"] < config["artefatos_minimos"]:
            verificacoes["problemas"].append(
                f"Artefatos insuficientes: {verificacoes['artefatos_encontrados']}/"
                f"{config['artefatos_minimos']}"
            )
            verificacoes["completa"] = False
        
        return verificacoes
    
    def _validate_documento_consolidado(self):
        """Valida o documento consolidado de disciplinas."""
        print(f"\n📋 Verificando documento consolidado...")
        
        consolidado_path = self.engenharia_dir / "disciplinas-engenharia.md"
        
        if not consolidado_path.exists():
            self.results["problemas"].append({
                "tipo": "documento_consolidado",
                "problema": "Documento consolidado não encontrado"
            })
            print("  ❌ Documento consolidado não encontrado")
            return
        
        try:
            with open(consolidado_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Verificar se menciona todas as disciplinas
            disciplinas_esperadas = [
                "Gestão de Requisitos", "Arquitetura de Software",
                "Gestão de Configuração", "Gestão de Projeto",
                "Gestão de Qualidade", "Gestão de Riscos",
                "Gestão de Mudanças", "Gestão de Testes",
                "Gestão de Deploy", "Gestão de Operações"
            ]
            
            disciplinas_encontradas = 0
            for disciplina in disciplinas_esperadas:
                if disciplina in conteudo:
                    disciplinas_encontradas += 1
            
            if disciplinas_encontradas == len(disciplinas_esperadas):
                print("  ✅ Documento consolidado - COMPLETO")
            else:
                print(f"  ⚠️ Documento consolidado - PARCIAL ({disciplinas_encontradas}/{len(disciplinas_esperadas)})")
                
        except Exception as e:
            self.results["problemas"].append({
                "tipo": "documento_consolidado",
                "problema": f"Erro ao ler documento: {str(e)}"
            })
            print(f"  ❌ Erro ao ler documento consolidado: {str(e)}")
    
    def _validate_estrutura_projeto(self):
        """Valida a estrutura geral do projeto."""
        print(f"\n🏗️ Verificando estrutura do projeto...")
        
        # Verificar diretórios essenciais
        diretorios_essenciais = [
            "src", "tests", "docs", "scripts", ".github"
        ]
        
        for diretorio in diretorios_essenciais:
            path = self.project_root / diretorio
            if not path.exists():
                self.results["problemas"].append({
                    "tipo": "estrutura",
                    "problema": f"Diretório '{diretorio}' não encontrado"
                })
                print(f"  ❌ Diretório '{diretorio}' não encontrado")
            else:
                print(f"  ✅ Diretório '{diretorio}' encontrado")
        
        # Verificar arquivos de configuração
        arquivos_config = [
            "pyproject.toml", "requirements.txt", ".pre-commit-config.yaml",
            "README.md", "CONTRIBUTING.md"
        ]
        
        for arquivo in arquivos_config:
            path = self.project_root / arquivo
            if not path.exists():
                self.results["problemas"].append({
                    "tipo": "configuracao",
                    "problema": f"Arquivo '{arquivo}' não encontrado"
                })
                print(f"  ❌ Arquivo '{arquivo}' não encontrado")
            else:
                print(f"  ✅ Arquivo '{arquivo}' encontrado")
    
    def _generate_report(self):
        """Gera relatório final."""
        print(f"\n" + "=" * 60)
        print("📊 RELATÓRIO DE VALIDAÇÃO DE DISCIPLINAS")
        print("=" * 60)
        
        total_disciplinas = len(self.results["disciplinas_completas"]) + \
                          len(self.results["disciplinas_parciais"]) + \
                          len(self.results["disciplinas_faltantes"])
        
        print(f"\n📈 RESUMO GERAL:")
        print(f"  • Total de disciplinas: {total_disciplinas}")
        print(f"  • Disciplinas completas: {len(self.results['disciplinas_completas'])}")
        print(f"  • Disciplinas parciais: {len(self.results['disciplinas_parciais'])}")
        print(f"  • Disciplinas faltantes: {len(self.results['disciplinas_faltantes'])}")
        print(f"  • Problemas encontrados: {len(self.results['problemas'])}")
        
        # Calcular percentual de completude
        completude = (len(self.results["disciplinas_completas"]) / total_disciplinas) * 100
        print(f"  • Completude geral: {completude:.1f}%")
        
        if completude >= 80:
            print(f"\n🎉 EXCELENTE! Disciplinas bem implementadas!")
        elif completude >= 60:
            print(f"\n✅ BOM! Disciplinas em boa implementação!")
        elif completude >= 40:
            print(f"\n⚠️ REGULAR! Disciplinas precisam de melhorias!")
        else:
            print(f"\n❌ CRÍTICO! Disciplinas precisam ser implementadas!")
        
        # Detalhar disciplinas completas
        if self.results["disciplinas_completas"]:
            print(f"\n✅ DISCIPLINAS COMPLETAS:")
            for disciplina in self.results["disciplinas_completas"]:
                print(f"  • {disciplina['titulo']}")
        
        # Detalhar disciplinas parciais
        if self.results["disciplinas_parciais"]:
            print(f"\n⚠️ DISCIPLINAS PARCIAIS:")
            for disciplina in self.results["disciplinas_parciais"]:
                print(f"  • {disciplina['titulo']}")
                for problema in disciplina["verificacoes"]["problemas"]:
                    print(f"    - {problema}")
        
        # Detalhar disciplinas faltantes
        if self.results["disciplinas_faltantes"]:
            print(f"\n❌ DISCIPLINAS FALTANTES:")
            for disciplina in self.results["disciplinas_faltantes"]:
                print(f"  • {disciplina['titulo']}")
        
        # Detalhar problemas
        if self.results["problemas"]:
            print(f"\n🚨 PROBLEMAS ENCONTRADOS:")
            for problema in self.results["problemas"]:
                print(f"  • {problema['problema']}")
        
        # Recomendações
        print(f"\n💡 RECOMENDAÇÕES:")
        if len(self.results["disciplinas_faltantes"]) > 0:
            print(f"  1. Implementar disciplinas faltantes")
        if len(self.results["disciplinas_parciais"]) > 0:
            print(f"  2. Completar disciplinas parciais")
        if len(self.results["problemas"]) > 0:
            print(f"  3. Corrigir problemas encontrados")
        print(f"  4. Revisar periodicamente as disciplinas")
        print(f"  5. Atualizar documentação conforme necessário")
        
        print(f"\n" + "=" * 60)
        print("✅ Validação concluída!")
        print("=" * 60)

def main():
    """Função principal."""
    validator = DisciplinaValidator()
    results = validator.validate_disciplinas()
    
    # Retornar código de saída baseado nos resultados
    if len(results["disciplinas_faltantes"]) > 0 or len(results["problemas"]) > 0:
        sys.exit(1)  # Erro
    else:
        sys.exit(0)  # Sucesso

if __name__ == "__main__":
    main()
