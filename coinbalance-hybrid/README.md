# 🪙 Coinbalance - A Economia da Consciência (Híbrido Python-Rust)

[![CI/CD](https://github.com/glaucomaximo/coinbalance/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/glaucomaximo/coinbalance/actions/workflows/ci-cd.yml)
[![Security](https://img.shields.io/badge/security-audited-green.svg)](https://github.com/glaucomaximo/coinbalance/security)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Rust](https://img.shields.io/badge/rust-1.70+-orange.svg)](https://rust-lang.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)

A primeira plataforma de investimento consciente baseada no framework proprietário **Coinbalance**, que integra inteligência artificial simbólica, neuroeconomia e blockchain para criar um novo paradigma econômico: **"A Economia da Consciência"**. A plataforma utiliza a moeda digital **Coinbalance (CNB)** como veículo de investimento e troca de valor.

## 🏗️ **Arquitetura Híbrida**

Este projeto implementa uma arquitetura híbrida **Python-Rust** que combina:

- **🐍 Python**: Interface, API, lógica de negócio, integração
- **🦀 Rust**: Validação de transações, criptografia, consenso, performance crítica

### **Componentes Rust (Performance Crítica)**
- **Validador de Transações**: Validação segura e rápida de transações CNB
- **Sistema de Criptografia**: ECDSA, Ed25519, AES-256-GCM, Argon2
- **Consenso Proof of Stake**: Algoritmo de consenso consciente
- **Cálculos de Hash**: SHA-256, SHA-512, Keccak256, Keccak512

### **Componentes Python (Interface e Lógica)**
- **API REST**: FastAPI para endpoints HTTP
- **Framework Coinbalance**: IA simbólica e neuroeconomia
- **Interface Web**: Interface responsiva para dispositivos móveis
- **Integração**: Ponte Python-Rust para comunicação

## 🚀 **Instalação e Execução**

### **Pré-requisitos**
- **Python 3.11+**
- **Rust 1.70+**
- **Git**

### **Instalação Rápida**
```bash
# Clonar repositório
git clone https://github.com/glaucomaximo/coinbalance.git
cd coinbalance

# Executar build automático
python scripts/build.py

# Iniciar aplicação
python launch.py
```

### **Instalação Manual**
```bash
# 1. Instalar dependências Python
pip install -r requirements.txt

# 2. Compilar componentes Rust
cd rust
cargo build --release
cd ..

# 3. Copiar bibliotecas
cp rust/target/release/libcoinbalance_core.* integration/

# 4. Executar aplicação
python launch.py
```

## 🛠️ **Desenvolvimento**

### **Estrutura do Projeto**
```
coinbalance-hybrid/
├── python/                 # Componentes Python
│   ├── main.py            # Ponto de entrada
│   ├── api_moderna.py     # API FastAPI
│   ├── coinbalance_framework.py  # Framework proprietário
│   └── ...
├── rust/                  # Componentes Rust
│   ├── validator/         # Validação de transações
│   ├── crypto/            # Sistema de criptografia
│   ├── consensus/         # Algoritmo de consenso
│   └── Cargo.toml         # Configuração Rust
├── integration/           # Ponte Python-Rust
│   ├── coinbalance_rust.py
│   └── libcoinbalance_core.*
├── scripts/               # Scripts de build
│   └── build.py
├── docs/                  # Documentação
├── examples/              # Exemplos de uso
└── requirements.txt       # Dependências Python
```

### **Comandos de Desenvolvimento**
```bash
# Build completo
python scripts/build.py

# Build em modo debug
python scripts/build.py --debug

# Apenas compilar Rust
python scripts/build.py --rust-only

# Limpar arquivos de build
python scripts/build.py --clean

# Executar testes
python scripts/build.py --test
```

## 🧠 **Framework Coinbalance**

### **IA Simbólica**
- Análise de projetos conscientes
- Recomendações personalizadas
- Detecção de padrões de consciência
- Sistema de pontuação ética

### **Neuroeconomia Aplicada**
- Detecção de vieses cognitivos
- Análise emocional de investimentos
- Modelagem de decisões conscientes
- Otimização de portfólio ético

### **Blockchain Consciente**
- Validação ética de transações
- Transparência total
- Sistema de reputação baseado em impacto
- Governança descentralizada

## 💰 **Moeda CNB**

### **Características**
- **Nome**: Coinbalance
- **Símbolo**: CNB
- **Supply**: 100 milhões de tokens
- **Algoritmo**: Proof of Stake Consciente
- **Blockchain**: Ethereum ERC-20 (migração futura)

### **Tokenomics**
- **40%** - Venda pública
- **30%** - Equipe e fundadores
- **20%** - Reserva estratégica
- **10%** - Parcerias e desenvolvimento

### **Utility**
- Pagamentos na plataforma
- Staking com 12% APY
- Governança descentralizada
- Acesso a funcionalidades premium

## 📱 **Interface Mobile**

### **Funcionalidades**
- Carteira CNB completa
- Staking e recompensas
- Investimentos conscientes
- Análise com IA simbólica
- Notificações push

### **Tecnologias**
- Interface web responsiva
- PWA (Progressive Web App)
- React Native (futuro)
- Flutter (futuro)

## 🔧 **API Endpoints**

### **Carteira**
```http
GET    /carteiras                    # Listar carteiras
POST   /carteiras/criar              # Criar carteira
GET    /carteiras/{id}               # Obter carteira
POST   /carteiras/{id}/enviar        # Enviar CNB
```

### **Transações**
```http
GET    /transacoes                   # Listar transações
POST   /transacoes/nova              # Nova transação
GET    /transacoes/{id}              # Obter transação
```

### **Staking**
```http
POST   /defi/stake                   # Fazer stake
POST   /defi/unstake                 # Retirar stake
GET    /defi/recompensas             # Ver recompensas
```

### **Investimentos**
```http
GET    /investimentos                # Listar projetos
POST   /investimentos/analisar       # Analisar projeto
POST   /investimentos/investir       # Fazer investimento
```

## 🧪 **Testes**

### **Executar Testes**
```bash
# Testes Python
pytest python/tests/

# Testes Rust
cd rust && cargo test

# Testes de integração
python integration/coinbalance_rust.py
```

### **Cobertura de Testes**
```bash
# Cobertura Python
pytest --cov=python python/tests/

# Cobertura Rust
cd rust && cargo tarpaulin
```

## 📊 **Performance**

### **Benchmarks Rust vs Python**
| Operação | Python | Rust | Melhoria |
|----------|--------|------|----------|
| Validação de transação | 10ms | 1ms | 10x |
| Cálculo de hash | 5ms | 0.5ms | 10x |
| Assinatura digital | 15ms | 2ms | 7.5x |
| Verificação de assinatura | 12ms | 1.5ms | 8x |

### **Uso de Memória**
- **Python**: ~50MB base
- **Rust**: ~5MB para componentes críticos
- **Total**: ~55MB (vs ~200MB apenas Python)

## 🔒 **Segurança**

### **Rust (Memory Safety)**
- Zero buffer overflows
- Prevenção de race conditions
- Type safety em tempo de compilação
- Gerenciamento seguro de memória

### **Python (Flexibilidade)**
- Validação de entrada robusta
- Sanitização de dados
- Rate limiting
- Autenticação JWT

## 🚀 **Deploy**

### **Docker**
```bash
# Build da imagem
docker build -t coinbalance-hybrid .

# Executar container
docker run -p 8000:8000 coinbalance-hybrid
```

### **Docker Compose**
```bash
# Iniciar todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### **Produção**
```bash
# Build para produção
python scripts/build.py --release

# Executar com Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## 📈 **Roadmap**

### **Fase 1: MVP (Atual)**
- ✅ Framework híbrido Python-Rust
- ✅ Validação de transações
- ✅ Sistema de criptografia
- ✅ Interface web responsiva
- ✅ Moeda CNB básica

### **Fase 2: Expansão (Q2 2024)**
- 🔄 PWA completo
- 🔄 App mobile nativo
- 🔄 Integração com exchanges
- 🔄 Sistema de governança

### **Fase 3: Escala (Q3 2024)**
- ⏳ Blockchain própria
- ⏳ DeFi avançado
- ⏳ IA simbólica completa
- ⏳ Parcerias estratégicas

## 🤝 **Contribuição**

### **Como Contribuir**
1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### **Padrões de Código**
- **Python**: Black, Flake8, MyPy
- **Rust**: rustfmt, clippy
- **Commits**: Conventional Commits
- **Documentação**: Markdown, docstrings

## 📄 **Licença**

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.

## 📞 **Suporte**

- **Email**: dev@coinbalance.com.br
- **Discord**: https://discord.gg/coinbalance
- **GitHub Issues**: [Abrir issue](https://github.com/glaucomaximo/coinbalance/issues)
- **Documentação**: [docs.coinbalance.com.br](https://docs.coinbalance.com.br)

## 🎯 **Visão**

**Coinbalance** representa uma revolução na forma como pensamos sobre investimentos e economia. Ao combinar tecnologia de ponta (Rust) com flexibilidade (Python) e consciência (Framework proprietário), criamos uma plataforma que não apenas gera retorno financeiro, mas também impacto positivo na sociedade e no planeta.

*"A Economia da Consciência"* - **Coinbalance (CNB)** 🪙

---

**Desenvolvido com ❤️ pela equipe Coinbalance**