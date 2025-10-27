# 🤝 Guia de Contribuição - CoinBalance

<div align="center">

![Contributing](https://img.shields.io/badge/Contributing-Welcome-FF6B6B?style=for-the-badge)
![Community](https://img.shields.io/badge/Community-Driven-4ECDC4?style=for-the-badge)
![Open Source](https://img.shields.io/badge/Open%20Source-MIT-00D4AA?style=for-the-badge)

**Contribua para a Revolução da Blockchain Consciente**

</div>

---

## 🌟 **Bem-vindo Contribuidor!**

Obrigado por considerar contribuir para o **CoinBalance**! Este projeto representa uma revolução na tecnologia blockchain através da implementação de uma arquitetura fractal consciente. Sua contribuição é fundamental para o sucesso desta iniciativa.

### 🎯 **Como Contribuir**

Existem várias maneiras de contribuir para o projeto:

- 🐛 **Reportar Bugs**: Encontrou um bug? Reporte-o!
- 💡 **Sugerir Melhorias**: Tem uma ideia? Compartilhe!
- 🔧 **Corrigir Bugs**: Corrija bugs existentes
- ✨ **Implementar Features**: Adicione novas funcionalidades
- 📚 **Melhorar Documentação**: Ajude a melhorar a documentação
- 🧪 **Escrever Testes**: Adicione ou melhore testes
- 🌍 **Tradução**: Ajude com traduções

---

## 🚀 **Início Rápido**

### **1. Fork e Clone**

```bash
# Fork o repositório no GitHub
# Depois clone seu fork
git clone https://github.com/SEU_USUARIO/coinbalance.git
cd coinbalance

# Adicionar upstream
git remote add upstream https://github.com/coinbalance/coinbalance.git
```

### **2. Configurar Ambiente**

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Instalar pre-commit hooks
pre-commit install
```

### **3. Criar Branch**

```bash
# Atualizar main
git checkout main
git pull upstream main

# Criar nova branch
git checkout -b feature/nova-funcionalidade
# ou
git checkout -b bugfix/correcao-bug
# ou
git checkout -b docs/melhoria-documentacao
```

---

## 📋 **Processo de Contribuição**

### **1. Antes de Começar**

- ✅ Verifique se já existe uma issue relacionada
- ✅ Se não existir, crie uma issue descrevendo sua proposta
- ✅ Aguarde feedback da equipe antes de começar
- ✅ Certifique-se de que está seguindo o roadmap do projeto

### **2. Durante o Desenvolvimento**

- ✅ Mantenha commits pequenos e focados
- ✅ Use mensagens de commit descritivas
- ✅ Siga os padrões de código do projeto
- ✅ Escreva testes para suas mudanças
- ✅ Atualize documentação quando necessário

### **3. Antes de Enviar**

- ✅ Execute todos os testes: `pytest`
- ✅ Execute linting: `flake8 src/`
- ✅ Execute formatação: `black src/`
- ✅ Verifique cobertura: `pytest --cov=src`
- ✅ Atualize CHANGELOG.md se necessário

### **4. Pull Request**

- ✅ Título descritivo e claro
- ✅ Descrição detalhada das mudanças
- ✅ Referência à issue relacionada
- ✅ Screenshots/GIFs se aplicável
- ✅ Checklist preenchido

---

## 🏗️ **Padrões de Código**

### **Python**

Seguimos as seguintes convenções:

- **PEP 8**: Style guide para código Python
- **PEP 257**: Docstring conventions
- **Type Hints**: Sempre use type hints
- **Black**: Formatação automática
- **isort**: Organização de imports
- **flake8**: Linting

### **Estrutura de Commits**

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Mudanças na documentação
- `style`: Formatação, ponto e vírgula, etc.
- `refactor`: Refatoração de código
- `test`: Adição ou correção de testes
- `chore`: Mudanças em build, dependências, etc.

**Exemplos:**
```
feat(fractal): adicionar sistema de cache inteligente
fix(api): corrigir validação de JWT tokens
docs(readme): atualizar instruções de instalação
test(consensus): adicionar testes para validação de blocos
```

### **Estrutura de Arquivos**

```
src/
├── domain/           # Camada de domínio (DDD)
├── application/      # Camada de aplicação (Use Cases)
├── infrastructure/   # Camada de infraestrutura
└── presentation/    # Camada de apresentação (API)

tests/
├── unit/            # Testes unitários
├── integration/     # Testes de integração
├── e2e/            # Testes end-to-end
└── performance/    # Testes de performance
```

---

## 🧪 **Testes**

### **Executar Testes**

```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Com cobertura
pytest --cov=src --cov-report=html

# Com verbose
pytest -v

# Testes de performance
pytest tests/performance/ --benchmark-only
```

### **Escrever Testes**

- ✅ Teste casos positivos e negativos
- ✅ Use fixtures apropriadas
- ✅ Mock dependências externas
- ✅ Mantenha testes isolados
- ✅ Use nomes descritivos

**Exemplo:**
```python
def test_create_wallet_success():
    """Testa criação bem-sucedida de carteira."""
    # Arrange
    wallet_data = {"name": "Test Wallet", "description": "Test"}
    
    # Act
    result = wallet_service.create_wallet(wallet_data)
    
    # Assert
    assert result.name == "Test Wallet"
    assert result.is_active is True
    assert result.balance.total == 0.0
```

---

## 📚 **Documentação**

### **Padrões de Documentação**

- ✅ Use docstrings em todas as funções públicas
- ✅ Inclua exemplos de uso quando apropriado
- ✅ Mantenha documentação atualizada
- ✅ Use type hints para clareza

**Exemplo:**
```python
def create_wallet(self, wallet_data: dict) -> Wallet:
    """
    Cria uma nova carteira no sistema.
    
    Args:
        wallet_data: Dados da carteira contendo nome e descrição
        
    Returns:
        Wallet: Instância da carteira criada
        
    Raises:
        ValidationError: Se os dados forem inválidos
        DuplicateWalletError: Se já existir carteira com mesmo nome
        
    Example:
        >>> wallet_data = {"name": "My Wallet", "description": "Personal"}
        >>> wallet = service.create_wallet(wallet_data)
        >>> print(wallet.name)
        My Wallet
    """
```

### **Atualizar Documentação**

- ✅ README.md para mudanças principais
- ✅ Documentação de API para endpoints
- ✅ Documentação de arquitetura para mudanças estruturais
- ✅ CHANGELOG.md para releases

---

## 🔍 **Code Review**

### **Como Revisar**

- ✅ Verifique se o código segue os padrões
- ✅ Teste as funcionalidades localmente
- ✅ Verifique se os testes cobrem as mudanças
- ✅ Confirme se a documentação está atualizada
- ✅ Seja construtivo e educacional

### **Respondendo a Reviews**

- ✅ Seja respeitoso e profissional
- ✅ Responda a todos os comentários
- ✅ Faça as mudanças solicitadas
- ✅ Explique decisões quando necessário
- ✅ Agradeça o feedback

---

## 🐛 **Reportando Bugs**

### **Template de Bug Report**

```markdown
**Descrição do Bug**
Uma descrição clara e concisa do bug.

**Passos para Reproduzir**
1. Vá para '...'
2. Clique em '...'
3. Role até '...'
4. Veja o erro

**Comportamento Esperado**
O que deveria acontecer.

**Comportamento Atual**
O que está acontecendo.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente:**
- OS: [ex: Windows 10, macOS 12, Ubuntu 20.04]
- Python: [ex: 3.11.5]
- Versão: [ex: 2.1.0]

**Contexto Adicional**
Qualquer outra informação relevante.
```

---

## 💡 **Sugerindo Melhorias**

### **Template de Feature Request**

```markdown
**É sua feature request relacionada a um problema?**
Uma descrição clara e concisa do problema.

**Descreva a solução que você gostaria**
Uma descrição clara e concisa do que você quer que aconteça.

**Descreva alternativas que você considerou**
Uma descrição clara e concisa de soluções alternativas.

**Contexto Adicional**
Qualquer outro contexto sobre a feature request.
```

---

## 🏷️ **Labels e Milestones**

### **Labels Disponíveis**

- `bug`: Algo não está funcionando
- `enhancement`: Nova feature ou melhoria
- `documentation`: Melhorias na documentação
- `good first issue`: Bom para novos contribuidores
- `help wanted`: Precisa de ajuda extra
- `priority: high`: Alta prioridade
- `priority: medium`: Prioridade média
- `priority: low`: Baixa prioridade
- `area: fractal`: Relacionado a sistemas fractais
- `area: api`: Relacionado à API
- `area: blockchain`: Relacionado à blockchain
- `area: consensus`: Relacionado ao consenso

### **Milestones**

- `v2.2.0`: Próxima versão menor
- `v2.3.0`: Versão futura
- `v3.0.0`: Próxima versão maior

---

## 🌍 **Comunidade**

### **Canais de Comunicação**

- 💬 **Discord**: [Discord Server](https://discord.gg/coinbalance)
- 🐦 **Twitter**: [@coinbalance](https://twitter.com/coinbalance)
- 📧 **Email**: community@coinbalance.com
- 📺 **YouTube**: [CoinBalance Channel](https://youtube.com/coinbalance)

### **Eventos**

- 🎯 **Sprints**: Sprints de desenvolvimento mensais
- 🎓 **Workshops**: Workshops sobre arquitetura fractal
- 🏆 **Hackathons**: Hackathons temáticos
- 📚 **Study Groups**: Grupos de estudo sobre blockchain consciente

---

## 🏆 **Reconhecimento**

### **Contribuidores**

Todos os contribuidores são reconhecidos:

- 📝 **Contributors.md**: Lista de todos os contribuidores
- 🏅 **Badges**: Badges especiais para contribuidores
- 🎉 **Releases**: Menção em releases
- 🌟 **Hall of Fame**: Contribuidores destacados

### **Tipos de Contribuição**

- 🥇 **Gold**: Contribuições significativas
- 🥈 **Silver**: Contribuições regulares
- 🥉 **Bronze**: Primeiras contribuições
- 🌟 **Special**: Contribuições especiais

---

## 📋 **Checklist para Contribuidores**

### **Antes de Contribuir**

- [ ] Li e entendi o [README](README.md)
- [ ] Li e entendi este guia de contribuição
- [ ] Verifiquei se já existe uma issue relacionada
- [ ] Configurei meu ambiente de desenvolvimento
- [ ] Executei os testes e passaram

### **Durante o Desenvolvimento**

- [ ] Segui os padrões de código do projeto
- [ ] Escrevi testes para minhas mudanças
- [ ] Atualizei documentação quando necessário
- [ ] Mantive commits pequenos e focados
- [ ] Usei mensagens de commit descritivas

### **Antes de Enviar PR**

- [ ] Todos os testes passam
- [ ] Linting passa sem erros
- [ ] Cobertura de testes mantida
- [ ] Documentação atualizada
- [ ] CHANGELOG.md atualizado
- [ ] PR tem título e descrição claros

---

## ❓ **FAQ**

### **P: Como começar a contribuir?**

R: Comece lendo este guia, configurando seu ambiente e escolhendo uma issue marcada com `good first issue`.

### **P: Preciso de permissão para contribuir?**

R: Não! Qualquer um pode contribuir. Só precisamos que você siga este guia.

### **P: Como escolher uma issue?**

R: Procure por issues marcadas com `good first issue` ou `help wanted`. Comece com algo pequeno.

### **P: E se minha PR for rejeitada?**

R: Não se preocupe! Feedback é parte do processo. Revise os comentários e melhore sua contribuição.

### **P: Posso contribuir com documentação?**

R: Sim! Documentação é muito importante. Procure por issues marcadas com `documentation`.

---

## 📄 **Licença**

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [Licença MIT](LICENSE.md).

---

## 🙏 **Agradecimentos**

Obrigado por considerar contribuir para o CoinBalance! Sua contribuição é fundamental para o sucesso deste projeto revolucionário.

---

<div align="center">

**🤝 Contribua para a Revolução da Blockchain Consciente**

![Contributing](https://img.shields.io/badge/Contributing-Welcome-FF6B6B?style=for-the-badge)
![Community](https://img.shields.io/badge/Community-Driven-4ECDC4?style=for-the-badge)
![Open Source](https://img.shields.io/badge/Open%20Source-MIT-00D4AA?style=for-the-badge)

**🌟 Juntos Construímos o Futuro da Tecnologia**

</div>