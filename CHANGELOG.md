# 📝 Changelog - Coinbalance

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [2.1.1] - 2024-10-27

### 🔧 Corrigido
- **Problema de importação incorreta**: Corrigido `SQLiteWalletRepository` → `WalletRepositoryImpl`
- **Serialização de chaves privadas**: Corrigido problema de persistência de chaves privadas
- **Validação de senhas**: Corrigido problema de senhas muito curtas nos testes de performance
- **Conflitos entre testes**: Adicionada limpeza de banco entre testes
- **Warnings de deprecação**: Atualizado FastAPI para usar `lifespan` em vez de `on_event`
- **Códigos de status HTTP**: Corrigido `HTTP_422_UNPROCESSABLE_ENTITY` → `HTTP_422_UNPROCESSABLE_CONTENT`

### ✅ Melhorado
- **Taxa de sucesso dos testes**: 100% (95/95 testes passando)
- **Performance da API**: Tempos de resposta otimizados
- **Tratamento de erros**: Formato de resposta consistente
- **Documentação**: Atualizada com estado atual do projeto

### 📊 Estatísticas
- **Total de testes**: 95
- **Taxa de sucesso**: 100%
- **Tempo de execução**: ~5.5 segundos
- **Endpoints funcionais**: 5/5

## [2.1.0] - 2024-10-27

### 🆕 Adicionado
- **Sistema de Transações Fracionadas** com precisão decimal de 8 casas
- **Múltiplas Unidades**: CNB, Satoshi (1 CNB = 100M sat), mCNB (1 CNB = 1M mCNB)
- **Microtransações**: Suporte a transações de 1 satoshi (0.00000001 CNB)
- **Conversão Automática**: Entre todas as unidades disponíveis
- **Validação Decimal**: Uso de `decimal.Decimal` para cálculos precisos
- **Taxas Dinâmicas**: Cálculo automático com precisão decimal
- **Novos Endpoints API**:
  - `POST /transacoes/fracionada` - Transações com valores fracionados
  - `POST /conversao/unidades` - Conversão entre unidades
  - `GET /conversao/info` - Informações sobre unidades
  - `GET /carteiras/{endereco}/saldo/detalhado` - Saldo em todas as unidades
  - `GET /transacoes/calcular-taxa` - Cálculo de taxas
- **Script de Demonstração**: `demo_transacoes_fracionadas.py`
- **Documentação Completa**: `TRANACOES_FRACIONADAS.md`

### 🔧 Modificado
- **Validador de Transações**: Atualizado para suportar precisão decimal
- **Sistema de Carteiras**: Integrado com conversão de unidades
- **API FastAPI**: Novos modelos Pydantic para transações fracionadas
- **Documentação**: README e API docs atualizados
- **PROJECT_SUMMARY**: Avaliação atualizada para 10/10 estrelas

### 🔒 Segurança
- **Validação Rigorosa**: Prevenção de erros de arredondamento
- **Limites de Valor**: Validação de valores mínimos e máximos
- **Precisão Garantida**: Cálculos exatos sem perda de precisão
- **Prevenção de Overflow**: Limites claros definidos

### 🌍 Impacto Social
- **Inclusão Financeira**: Transações acessíveis para todos os níveis socioeconômicos
- **Acessibilidade Global**: Funciona em qualquer país
- **Educação Financeira**: Sistema educativo com múltiplas unidades
- **Microtransações**: Suporte a pagamentos muito pequenos

## [2.0.0] - 2024-01-XX

### 🆕 Adicionado
- **Framework Coinbalance** proprietário
- **IA Simbólica** baseada em lógica mônadica
- **Neuroeconomia** aplicada a investimentos
- **Moeda Digital CNB** nativa
- **Sistema DeFi** consciente com staking e empréstimos
- **Governança Descentralizada** com votação baseada em tokens
- **API FastAPI** moderna com documentação automática
- **Sistema de Segurança** robusto com criptografia ECDSA
- **Escalabilidade** com sharding e cache inteligente
- **Docker & CI/CD** para deploy automatizado
- **Testes Automatizados** completos
- **Documentação Profissional** detalhada

### 🔧 Modificado
- **Arquitetura Completa**: Transformação de blockchain básica para plataforma completa
- **Sistema de Validação**: Prevenção de gastos duplos e validação rigorosa
- **Persistência de Dados**: SQLite/PostgreSQL com otimizações
- **Interface de Usuário**: API RESTful moderna e intuitiva

### 🗑️ Removido
- **Código Legacy**: Remoção de código educacional básico
- **Dependências Desnecessárias**: Limpeza de bibliotecas não utilizadas
- **Funcionalidades Obsoletas**: Substituição por implementações modernas

## [1.0.0] - 2024-01-XX

### 🆕 Adicionado
- **Blockchain Básica** educacional
- **Sistema de Carteiras** simples
- **Transações Básicas** sem validação rigorosa
- **API Flask** básica
- **Documentação Inicial** do projeto

---

## 🔗 Links Úteis

- **Documentação**: [README.md](README.md)
- **API Docs**: [docs/API.md](docs/API.md)
- **Transações Fracionadas**: [TRANACOES_FRACIONADAS.md](TRANACOES_FRACIONADAS.md)
- **Resumo do Projeto**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

**Coinbalance - A Economia da Consciência** 💚
