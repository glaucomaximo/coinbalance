# 🤝 Guia de Contribuição - CoinBalance
## Como Contribuir para a Economia da Consciência

---

## 🌟 **BEM-VINDO CONTRIBUIDOR!**

Obrigado por considerar contribuir para o **CoinBalance**! Este projeto representa uma revolução na tecnologia blockchain, combinando IA consciente, Web3 completo e arquitetura fractal. Sua contribuição ajudará a construir o futuro da economia digital consciente.

---

## 🚀 **PRIMEIROS PASSOS**

### **1. Configuração do Ambiente**

#### **Pré-requisitos**
- Python 3.11+
- Git
- SQLite3
- Docker (opcional)

#### **Fork e Clone**
```bash
# Fork o repositório no GitHub primeiro
git clone https://github.com/SEU-USUARIO/coinbalance.git
cd coinbalance

# Adicionar upstream
git remote add upstream https://github.com/coinbalance/coinbalance.git

# Instalar dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### **Configuração do Ambiente**
```bash
# Copiar arquivo de ambiente
cp .env.example .env

# Configurar variáveis (editar .env)
JWT_SECRET_KEY="dev-secret-key-change-in-production"
COINBALANCE_MASTER_KEY="dev-master-key-change-in-production"
DEBUG=true
```

### **2. Executar o Sistema**
```bash
# Executar em modo desenvolvimento
python main.py

# Verificar se está funcionando
curl http://localhost:8000/health
```

---

## 🔧 **PROCESSO DE CONTRIBUIÇÃO**

### **1. Criar Branch**
```bash
# Sempre criar branch a partir de main
git checkout main
git pull upstream main
git checkout -b feature/nova-funcionalidade
# ou
git checkout -b fix/correcao-bug
# ou
git checkout -b docs/atualizacao-documentacao
```

### **2. Desenvolver**
- Implemente sua funcionalidade
- Siga os padrões de código
- Adicione testes
- Atualize documentação

### **3. Testar**
```bash
# Executar todos os testes
python -m pytest

# Testes específicos
python -m pytest tests/unit/
python -m pytest tests/integration/

# Com cobertura
python -m pytest --cov=src --cov-report=html

# Linting
flake8 src/
black --check src/
isort --check-only src/

# Type checking
mypy src/
```

### **4. Commit**
```bash
# Adicionar arquivos
git add .

# Commit com mensagem descritiva
git commit -m "feat(wallet): adiciona funcionalidade de backup automático

- Implementa backup automático de carteiras
- Adiciona validação de integridade
- Inclui testes unitários e de integração
- Atualiza documentação da API

Closes #123"
```

### **5. Push e Pull Request**
```bash
# Push para seu fork
git push origin feature/nova-funcionalidade

# Criar Pull Request no GitHub
# Usar template apropriado
# Aguardar review
```

---

## 📝 **PADRÕES DE CÓDIGO**

### **Python Style Guide**

#### **PEP 8 Compliance**
```python
# ✅ Bom
def create_wallet(name: str, user_id: str) -> Wallet:
    """Cria uma nova carteira para o usuário."""
    wallet = Wallet(
        id=generate_id(),
        name=name,
        user_id=user_id,
        created_at=time.time()
    )
    return wallet_repository.save(wallet)

# ❌ Ruim
def create_wallet(name,user_id):
    wallet=Wallet(id=generate_id(),name=name,user_id=user_id,created_at=time.time())
    return wallet_repository.save(wallet)
```

#### **Type Hints Obrigatórios**
```python
# ✅ Sempre usar type hints
def transfer_tokens(
    from_wallet_id: str,
    to_address: str,
    amount: Decimal,
    currency: str = "CNB"
) -> Transaction:
    """Transfere tokens entre carteiras."""
    pass

# ❌ Sem type hints
def transfer_tokens(from_wallet_id, to_address, amount, currency="CNB"):
    pass
```

#### **Docstrings Padronizadas**
```python
def analyze_market_opportunity(
    crypto_spec: CryptoSpecification
) -> MarketAnalysis:
    """
    Analisa oportunidade de mercado para uma criptomoeda.
    
    Args:
        crypto_spec: Especificação da criptomoeda a ser analisada
        
    Returns:
        Análise de mercado com score de oportunidade
        
    Raises:
        ValidationError: Se a especificação for inválida
        AnalysisError: Se houver erro na análise
        
    Example:
        >>> spec = CryptoSpecification(name="TestCoin", symbol="TEST")
        >>> analysis = analyze_market_opportunity(spec)
        >>> print(analysis.opportunity_score)
        0.85
    """
    pass
```

### **Conventional Commits**

#### **Formato**
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### **Tipos Válidos**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Mudanças na documentação
- `style`: Formatação, sem mudança de código
- `refactor`: Refatoração de código
- `test`: Adição ou correção de testes
- `chore`: Mudanças em build, dependências, etc.

#### **Exemplos**
```bash
# ✅ Bons commits
feat(wallet): adiciona funcionalidade de backup automático
fix(api): corrige validação de endereços de carteira
docs(api): atualiza documentação dos endpoints de wallet
test(wallet): adiciona testes para criação de carteira
refactor(domain): simplifica lógica de validação de transações

# ❌ Commits ruins
fix bug
update
changes
wip
```

---

## 🤖 **CONTRIBUIÇÕES PARA IA AVANÇADA**

### **Áreas de Contribuição**

#### **Machine Learning**
- **Novos Modelos**: Implementar novos algoritmos de ML
- **Otimização**: Melhorar performance dos modelos existentes
- **Precisão**: Aumentar precisão das predições
- **Dados**: Melhorar coleta e qualidade dos dados

#### **Economia Autônoma**
- **Indicadores**: Adicionar novos indicadores econômicos
- **Políticas**: Implementar novas políticas econômicas
- **Decisões**: Melhorar algoritmo de decisões
- **Fases**: Otimizar transições entre fases econômicas

#### **Predições de Mercado**
- **Timeframes**: Adicionar novos timeframes
- **Indicadores**: Implementar novos indicadores técnicos
- **Padrões**: Detectar novos padrões de mercado
- **Validação**: Melhorar sistema de validação

#### **Criação de Tokens**
- **Tipos**: Adicionar novos tipos de tokens
- **Templates**: Criar novos templates inteligentes
- **Oportunidades**: Melhorar detecção de oportunidades
- **Otimização**: Implementar novas estratégias de otimização

### **Diretrizes Específicas**

#### **Para Modelos de ML**
```python
# Estrutura esperada para novos modelos
class NovoModeloML:
    def __init__(self):
        self.name = "Novo Modelo"
        self.model_type = MLModelType.NOVO_MODELO
        self.accuracy = 0.0
    
    async def train(self, data: List[MarketData]) -> float:
        # Implementar treinamento
        pass
    
    async def predict(self, data: MarketData) -> Prediction:
        # Implementar predição
        pass
```

#### **Para Indicadores Econômicos**
```python
# Estrutura esperada para novos indicadores
class NovoIndicador(EconomicIndicator):
    def __init__(self):
        self.name = "Novo Indicador"
        self.weight = 0.1
        self.target_value = 0.0
    
    async def calculate(self, data: Dict[str, Any]) -> EconomicIndicatorData:
        # Implementar cálculo
        pass
```

#### **Para Tipos de Tokens**
```python
# Estrutura esperada para novos tipos de tokens
class NovoTipoToken(TokenType):
    def __init__(self):
        self.name = "novo_tipo"
        self.display_name = "Novo Tipo"
        self.features = ["feature1", "feature2"]
        self.standards = [TokenStandard.ERC20]
```

### **Testes para IA**

#### **Testes de ML**
```python
# Exemplo de teste para modelo de ML
async def test_novo_modelo_ml():
    modelo = NovoModeloML()
    dados_teste = [MarketData(...) for _ in range(100)]
    
    precisao = await modelo.train(dados_teste)
    assert precisao > 0.8
    
    predicao = await modelo.predict(dados_teste[0])
    assert predicao.confidence > 0.7
```

#### **Testes de Economia**
```python
# Exemplo de teste para economia autônoma
async def test_novo_indicador():
    indicador = NovoIndicador()
    dados = {"valor": 100.0, "timestamp": time.time()}
    
    resultado = await indicador.calculate(dados)
    assert resultado.value == 100.0
    assert resultado.trend in ["increasing", "decreasing", "stable"]
```

### **Documentação para IA**

#### **Documentar Modelos**
```markdown
## Novo Modelo ML

### Descrição
Breve descrição do modelo e seu propósito.

### Algoritmo
Explicação do algoritmo utilizado.

### Parâmetros
- `param1`: Descrição do parâmetro
- `param2`: Descrição do parâmetro

### Performance
- Precisão esperada: > 80%
- Tempo de treinamento: < 5 minutos
- Tempo de predição: < 1 segundo

### Exemplo de Uso
```python
# Código de exemplo
```

### Referências
Links para papers ou documentação relevante.
```

#### **Documentar APIs**
```markdown
## Endpoint: POST /api/v1/ai-advanced/novo-endpoint

### Descrição
Breve descrição do endpoint.

### Parâmetros
- `param1` (string): Descrição
- `param2` (number): Descrição

### Resposta
```json
{
  "status": "success",
  "data": {...}
}
```

### Exemplo
```bash
curl -X POST "http://localhost:8000/api/v1/ai-advanced/novo-endpoint" \
  -H "Content-Type: application/json" \
  -d '{"param1": "valor", "param2": 123}'
```
```

---

## 🧪 **TESTES**

### **Estrutura de Testes**
```
tests/
├── unit/                    # Testes unitários
│   ├── domain/             # Testes de domínio
│   ├── application/        # Testes de aplicação
│   └── infrastructure/     # Testes de infraestrutura
├── integration/            # Testes de integração
│   ├── api/               # Testes de API
│   └── database/          # Testes de banco
├── e2e/                   # Testes end-to-end
├── performance/           # Testes de performance
└── fixtures/              # Fixtures compartilhadas
```

### **Escrevendo Testes**

#### **Testes Unitários**
```python
# tests/unit/domain/wallet/test_wallet.py
import pytest
from decimal import Decimal
from src.domain.wallet.entities.wallet import Wallet
from src.domain.wallet.value_objects.address import Address
from src.domain.wallet.value_objects.balance import Balance

class TestWallet:
    def test_create_wallet_success(self):
        """Testa criação bem-sucedida de carteira."""
        # Arrange
        address = Address("0x1234567890abcdef")
        balance = Balance(Decimal("100.0"))
        
        # Act
        wallet = Wallet(
            id="wallet_123",
            address=address,
            balance=balance
        )
        
        # Assert
        assert wallet.id == "wallet_123"
        assert wallet.address.value == "0x1234567890abcdef"
        assert wallet.balance.amount == Decimal("100.0")
    
    def test_credit_wallet_increases_balance(self):
        """Testa que crédito aumenta saldo da carteira."""
        # Arrange
        wallet = self._create_test_wallet()
        initial_balance = wallet.balance.amount
        
        # Act
        wallet.credit(Decimal("50.0"))
        
        # Assert
        assert wallet.balance.amount == initial_balance + Decimal("50.0")
    
    def test_debit_insufficient_balance_raises_error(self):
        """Testa que débito com saldo insuficiente gera erro."""
        # Arrange
        wallet = self._create_test_wallet()
        
        # Act & Assert
        with pytest.raises(InsufficientBalanceError):
            wallet.debit(Decimal("200.0"))
    
    def _create_test_wallet(self) -> Wallet:
        """Cria carteira de teste."""
        return Wallet(
            id="wallet_test",
            address=Address("0x1234567890abcdef"),
            balance=Balance(Decimal("100.0"))
        )
```

#### **Testes de Integração**
```python
# tests/integration/api/test_wallet_api.py
import pytest
from fastapi.testclient import TestClient
from src.presentation.api.app import app

client = TestClient(app)

class TestWalletAPI:
    def test_create_wallet_success(self):
        """Testa criação de carteira via API."""
        # Act
        response = client.post(
            "/api/v1/wallet/create",
            json={"name": "Test Wallet"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "wallet" in data
        assert "id" in data["wallet"]
        assert "address" in data["wallet"]
    
    def test_get_wallet_not_found(self):
        """Testa obtenção de carteira inexistente."""
        # Act
        response = client.get("/api/v1/wallet/nonexistent")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
```

### **Executando Testes**
```bash
# Todos os testes
python -m pytest

# Testes específicos
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/e2e/

# Com cobertura
python -m pytest --cov=src --cov-report=html --cov-report=term

# Testes de performance
python -m pytest tests/performance/ -v

# Testes em paralelo
python -m pytest -n auto
```

---

## 📚 **DOCUMENTAÇÃO**

### **Atualizando Documentação**

#### **README.md**
- Atualize seção relevante
- Adicione exemplos de uso
- Mantenha instruções de instalação atualizadas

#### **Documentação Técnica**
- Atualize `DOCUMENTACAO_TECNICA_COMPLETA.md`
- Adicione novos endpoints na seção de APIs
- Documente novas funcionalidades

#### **Docstrings**
- Sempre adicione docstrings em funções públicas
- Use formato Google Style
- Inclua exemplos quando apropriado

#### **Exemplos de Código**
```python
def create_nft(
    name: str,
    description: str,
    image_url: str,
    attributes: Dict[str, Any]
) -> NFT:
    """
    Cria um novo NFT no marketplace.
    
    Args:
        name: Nome do NFT
        description: Descrição do NFT
        image_url: URL da imagem do NFT
        attributes: Atributos personalizados do NFT
        
    Returns:
        NFT criado com ID único
        
    Raises:
        ValidationError: Se os dados forem inválidos
        InsufficientFundsError: Se não houver fundos para taxa
        
    Example:
        >>> nft = create_nft(
        ...     name="Meu NFT",
        ...     description="Um NFT único",
        ...     image_url="https://example.com/image.jpg",
        ...     attributes={"rarity": "rare", "color": "blue"}
        ... )
        >>> print(nft.id)
        nft_1234567890abcdef
    """
    pass
```

---

## 🐛 **REPORTANDO BUGS**

### **Antes de Reportar**
1. Verifique se o bug já foi reportado
2. Teste com a versão mais recente
3. Verifique se não é um comportamento esperado

### **Template de Bug Report**
```markdown
## 🐛 Bug Report

### Descrição
Descrição clara e concisa do bug.

### Passos para Reproduzir
1. Vá para '...'
2. Clique em '...'
3. Role até '...'
4. Veja o erro

### Comportamento Esperado
O que deveria acontecer.

### Comportamento Atual
O que está acontecendo.

### Screenshots
Se aplicável, adicione screenshots.

### Ambiente
- OS: [e.g. Windows 10, macOS 12, Ubuntu 20.04]
- Python: [e.g. 3.11.0]
- CoinBalance: [e.g. 2.1.0]
- Browser: [e.g. Chrome 90, Firefox 88]

### Logs
```
Cole logs relevantes aqui
```

### Informações Adicionais
Qualquer outra informação relevante.
```

---

## 💡 **SUGERINDO FEATURES**

### **Template de Feature Request**
```markdown
## 💡 Feature Request

### Descrição
Descrição clara e concisa da funcionalidade desejada.

### Problema que Resolve
Qual problema esta funcionalidade resolveria?

### Solução Proposta
Descrição detalhada da solução proposta.

### Alternativas Consideradas
Outras soluções que você considerou.

### Impacto
- Usuários afetados: [e.g. Todos os usuários, apenas desenvolvedores]
- Complexidade: [e.g. Baixa, Média, Alta]
- Prioridade: [e.g. Baixa, Média, Alta]

### Exemplos de Uso
Como esta funcionalidade seria usada?

### Informações Adicionais
Qualquer outra informação relevante.
```

---

## 🔍 **REVIEW PROCESS**

### **Critérios de Review**

#### **Código**
- ✅ Segue padrões de código estabelecidos
- ✅ Tem testes adequados
- ✅ Documentação atualizada
- ✅ Performance considerada
- ✅ Segurança verificada

#### **Funcionalidade**
- ✅ Resolve o problema proposto
- ✅ Não quebra funcionalidades existentes
- ✅ API consistente
- ✅ Tratamento de erros adequado
- ✅ Validação de dados

#### **Testes**
- ✅ Cobertura adequada (>80%)
- ✅ Testes unitários
- ✅ Testes de integração (se aplicável)
- ✅ Testes de edge cases
- ✅ Performance tests (se aplicável)

### **Processo de Review**
1. **Automated Checks**: CI/CD pipeline executa
2. **Code Review**: Pelo menos 2 revisores
3. **Testing**: Testes manuais se necessário
4. **Approval**: Aprovação dos mantenedores
5. **Merge**: Merge para branch principal

---

## 🏆 **RECONHECIMENTO**

### **Tipos de Contribuição**
- **🐛 Bug Fixes**: Correções de bugs
- **✨ Features**: Novas funcionalidades
- **📚 Documentation**: Melhorias na documentação
- **🧪 Tests**: Adição de testes
- **🎨 UI/UX**: Melhorias na interface
- **⚡ Performance**: Otimizações de performance
- **🔒 Security**: Melhorias de segurança

### **Sistema de Reconhecimento**
- **Contributors**: Listados no README
- **Hall of Fame**: Contribuidores destacados
- **Badges**: Badges especiais no GitHub
- **Mentions**: Menções em releases
- **Community**: Reconhecimento na comunidade

---

## 📞 **COMUNIDADE E SUPORTE**

### **Canais de Comunicação**
- **GitHub Issues**: Para bugs e feature requests
- **GitHub Discussions**: Para discussões gerais
- **Discord**: Comunidade ativa de desenvolvedores
- **Email**: dev@coinbalance.com
- **Twitter**: @CoinBalance

### **Recursos da Comunidade**
- **Contributing Guide**: Este documento
- **Code of Conduct**: Código de conduta
- **Roadmap**: Roadmap público do projeto
- **Wiki**: Wiki com informações detalhadas
- **Video Tutorials**: Tutoriais em vídeo

### **Eventos e Meetups**
- **Monthly Meetups**: Encontros mensais online
- **Hackathons**: Hackathons regulares
- **Conferences**: Apresentações em conferências
- **Workshops**: Workshops técnicos
- **AMA Sessions**: Sessões de perguntas e respostas

---

## 🎯 **ÁREAS DE CONTRIBUIÇÃO**

### **Desenvolvimento**
- **Backend**: APIs, serviços, integrações
- **Frontend**: Interface web, dashboards
- **Mobile**: Aplicativos móveis
- **Blockchain**: Smart contracts, protocolos
- **IA**: Machine learning, algoritmos

### **Documentação**
- **Técnica**: Documentação de APIs, arquitetura
- **Usuário**: Manuais, tutoriais, guias
- **Marketing**: Conteúdo, blog posts
- **Tradução**: Tradução para outros idiomas
- **Vídeos**: Tutoriais em vídeo

### **Qualidade**
- **Testes**: Testes unitários, integração, E2E
- **QA**: Testes manuais, validação
- **Performance**: Otimização, profiling
- **Segurança**: Auditoria, análise de segurança
- **Acessibilidade**: Melhorias de acessibilidade

### **Comunidade**
- **Moderação**: Moderação de fóruns, Discord
- **Suporte**: Suporte a usuários
- **Eventos**: Organização de eventos
- **Mentoria**: Mentoria de novos contribuidores
- **Outreach**: Divulgação do projeto

---

## 🚀 **PRÓXIMOS PASSOS**

### **Para Novos Contribuidores**
1. **Leia a documentação**: Comece com o README e documentação técnica
2. **Explore o código**: Familiarize-se com a arquitetura
3. **Execute o sistema**: Configure e execute localmente
4. **Escolha uma issue**: Comece com issues marcadas como "good first issue"
5. **Participe da comunidade**: Junte-se ao Discord e GitHub Discussions

### **Para Contribuidores Experientes**
1. **Mentore novos contribuidores**: Ajude outros a começar
2. **Revise PRs**: Ajude com code reviews
3. **Proponha melhorias**: Sugira melhorias arquiteturais
4. **Mantenha documentação**: Mantenha docs atualizadas
5. **Organize eventos**: Ajude a organizar meetups e workshops

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

## 📄 **LICENÇA**

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [Licença MIT](LICENSE.md).

---

**🎉 Obrigado por contribuir para o CoinBalance!**

Sua contribuição ajuda a construir o futuro da economia digital consciente. Juntos, estamos criando uma tecnologia que transcende as limitações tradicionais e abre novas possibilidades para a humanidade.

**Junte-se à revolução! 🧠✨**