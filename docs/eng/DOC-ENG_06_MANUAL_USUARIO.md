# 📘 DOC-ENG_06_MANUAL_USUARIO
## Manual do Usuário - CoinBalance Enterprise v3.0.0

**Versão:** 1.0  
**Data de Criação:** 29 de outubro de 2025  
**Última Atualização:** 29 de outubro de 2025  
**Autor:** Engenharia de Documentação Sênior  
**Status:** ✅ **COMPLETO**

---

## 📋 Sumário Executivo

Este manual fornece instruções completas para usuários finais do sistema CoinBalance Enterprise, incluindo instalação, configuração inicial, uso das funcionalidades principais e resolução de problemas.

---

## 🚀 Instalação

### **Pré-requisitos**

- **Python**: 3.11 ou superior
- **Sistema Operacional**: Windows, Linux ou macOS
- **Memória**: Mínimo 2GB RAM
- **Disco**: Mínimo 500MB de espaço livre

### **Instalação Local**

#### **Windows**

```powershell
# 1. Baixar e instalar Python 3.11+
# https://www.python.org/downloads/

# 2. Clonar repositório
git clone https://github.com/coinbalance/coinbalance.git
cd coinbalance

# 3. Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Executar
python main.py
```

#### **Linux/macOS**

```bash
# 1. Instalar Python 3.11+
sudo apt-get install python3.11 python3.11-venv  # Ubuntu/Debian
brew install python@3.11  # macOS

# 2. Clonar repositório
git clone https://github.com/coinbalance/coinbalance.git
cd coinbalance

# 3. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Executar
python main.py
```

### **Instalação com Docker**

```bash
# 1. Clonar repositório
git clone https://github.com/coinbalance/coinbalance.git
cd coinbalance

# 2. Executar com Docker Compose
docker-compose up -d

# 3. Verificar status
docker-compose ps
```

---

## ⚙️ Configuração Inicial

### **Criar Arquivo .env**

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar configurações
nano .env  # ou use seu editor preferido
```

### **Configurações Principais**

```env
# .env
DEBUG=false
LOG_LEVEL=INFO
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///blockchain.db
CORS_ORIGINS=["http://localhost:3000"]
```

### **Inicializar Banco de Dados**

O banco de dados é criado automaticamente na primeira execução. Se necessário, pode ser inicializado manualmente:

```bash
python scripts/init_database.py
```

---

## 📱 Funcionalidades Principais

### **1. Criar Carteira**

#### **Via API REST**

```bash
curl -X POST http://localhost:8000/api/v1/wallets \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Minha Carteira"}'
```

**Resposta:**

```json
{
  "success": true,
  "data": {
    "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "name": "Minha Carteira",
    "balance_cnb": 0.0,
    "created_at": 1698624000.0
  }
}
```

#### **Pontos Importantes**

- ✅ Guarde o endereço da carteira
- ✅ Guarde a chave privada em local seguro
- ✅ Não compartilhe sua chave privada

---

### **2. Consultar Saldo**

```bash
curl -X GET http://localhost:8000/api/v1/wallets/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Resposta:**

```json
{
  "success": true,
  "data": {
    "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "balance_cnb": 1000.0,
    "balance_satoshi": 100000000
  }
}
```

---

### **3. Criar Transação**

```bash
curl -X POST http://localhost:8000/api/v1/transactions \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "from_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "to_address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
    "amount_cnb": 10.5
  }'
```

**Resposta:**

```json
{
  "success": true,
  "data": {
    "id": "tx_abc123...",
    "status": "pending",
    "amount_cnb": 10.5
  }
}
```

---

### **4. Consultar Histórico de Transações**

```bash
curl -X GET "http://localhost:8000/api/v1/transactions?from_address=1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa&page=1&limit=20" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### **5. Consultar Blockchain**

#### **Estatísticas da Blockchain**

```bash
curl -X GET http://localhost:8000/api/v1/blockchain \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Resposta:**

```json
{
  "success": true,
  "data": {
    "height": 12345,
    "total_blocks": 12345,
    "total_transactions": 98765,
    "total_supply": 21000000.0,
    "difficulty": 5
  }
}
```

#### **Consultar Bloco Específico**

```bash
curl -X GET http://localhost:8000/api/v1/blockchain/blocks/12345 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🔧 Guias de Uso

### **Guia 1: Primeira Transação**

1. **Criar duas carteiras**
   ```bash
   # Carteira 1
   curl -X POST http://localhost:8000/api/v1/wallets \
     -H "Authorization: Bearer TOKEN" \
     -d '{"name": "Carteira A"}'
   
   # Carteira 2
   curl -X POST http://localhost:8000/api/v1/wallets \
     -H "Authorization: Bearer TOKEN" \
     -d '{"name": "Carteira B"}'
   ```

2. **Fazer transferência**
   ```bash
   curl -X POST http://localhost:8000/api/v1/transactions \
     -H "Authorization: Bearer TOKEN" \
     -d '{
       "from_address": "ENDEREÇO_A",
       "to_address": "ENDEREÇO_B",
       "amount_cnb": 10.0
     }'
   ```

3. **Verificar saldos**
   ```bash
   # Saldo da carteira A
   curl -X GET http://localhost:8000/api/v1/wallets/ENDEREÇO_A \
     -H "Authorization: Bearer TOKEN"
   
   # Saldo da carteira B
   curl -X GET http://localhost:8000/api/v1/wallets/ENDEREÇO_B \
     -H "Authorization: Bearer TOKEN"
   ```

### **Guia 2: Mineração de Blocos**

```bash
# Minerar um novo bloco
curl -X POST http://localhost:8000/api/v1/blockchain/mine \
  -H "Authorization: Bearer TOKEN" \
  -d '{"miner_address": "SEU_ENDEREÇO"}'
```

---

## 🔍 Troubleshooting

### **Problema: Erro de Conexão**

**Sintomas:**
```
Connection refused
```

**Soluções:**
1. Verificar se o servidor está rodando:
   ```bash
   curl http://localhost:8000/health
   ```

2. Verificar porta:
   ```bash
   # Padrão: porta 8000
   # Verificar se está em uso
   netstat -an | grep 8000  # Linux/Mac
   netstat -an | findstr 8000  # Windows
   ```

3. Verificar logs:
   ```bash
   tail -f logs/coinbalance.log
   ```

---

### **Problema: Erro de Autenticação**

**Sintomas:**
```
401 Unauthorized
```

**Soluções:**
1. Verificar token:
   ```bash
   # Obter novo token
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -d '{"username": "usuario", "password": "senha"}'
   ```

2. Verificar formato do header:
   ```bash
   # Correto
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   
   # Incorreto
   Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

---

### **Problema: Saldo Insuficiente**

**Sintomas:**
```
400 Bad Request - Insufficient balance
```

**Soluções:**
1. Verificar saldo atual:
   ```bash
   curl -X GET http://localhost:8000/api/v1/wallets/ENDEREÇO \
     -H "Authorization: Bearer TOKEN"
   ```

2. Adicionar fundos (se sistema de faucet disponível):
   ```bash
   curl -X POST http://localhost:8000/api/v1/system/faucet \
     -H "Authorization: Bearer TOKEN" \
     -d '{"address": "SEU_ENDEREÇO", "amount": 100.0}'
   ```

---

### **Problema: Transação Pendente**

**Sintomas:**
```
Status: pending (não confirma)
```

**Soluções:**
1. Minerar um bloco para confirmar transações pendentes:
   ```bash
   curl -X POST http://localhost:8000/api/v1/blockchain/mine \
     -H "Authorization: Bearer TOKEN" \
     -d '{"miner_address": "ENDEREÇO"}'
   ```

2. Verificar status da transação:
   ```bash
   curl -X GET http://localhost:8000/api/v1/transactions/TX_ID \
     -H "Authorization: Bearer TOKEN"
   ```

---

### **Problema: Banco de Dados Corrompido**

**Sintomas:**
```
Database error ou Integrity error
```

**Soluções:**
1. Verificar integridade:
   ```bash
   sqlite3 blockchain.db "PRAGMA integrity_check;"
   ```

2. Restaurar backup:
   ```bash
   cp backups/blockchain_<timestamp>.db blockchain.db
   ```

3. Reiniciar aplicação:
   ```bash
   docker-compose restart backend
   # ou
   python main.py
   ```

---

## ❓ FAQ (Perguntas Frequentes)

### **P: Como obter CNB para testar?**

**R:** Use o sistema de faucet (se disponível):
```bash
curl -X POST http://localhost:8000/api/v1/system/faucet \
  -H "Authorization: Bearer TOKEN" \
  -d '{"address": "SEU_ENDEREÇO", "amount": 1000.0}'
```

---

### **P: Qual é o valor mínimo de transação?**

**R:** Não há valor mínimo obrigatório, mas transações muito pequenas podem não ser economicamente viáveis devido às taxas.

---

### **P: Como faço backup da minha carteira?**

**R:** Guarde:
- Endereço da carteira
- Chave privada (em local seguro)
- Seed phrase (se disponível)

---

### **P: Posso recuperar uma carteira perdida?**

**R:** Sim, se você tiver a chave privada ou seed phrase. Sem essas informações, a carteira não pode ser recuperada.

---

### **P: Como funciona a mineração?**

**R:** A mineração usa Proof of Work (PoW). Minere blocos para:
- Confirmar transações pendentes
- Ganhar recompensa de mineração
- Manter a blockchain segura

---

## 📞 Suporte

### **Documentação Adicional**

- [Documentação Técnica Completa](../DOCUMENTACAO_TECNICA_ENTERPRISE.md)
- [Referência de API](../eng/DOC-ENG_03_API_REFERENCE.md)
- [Guia de Deploy](../GUIA_DEPLOY_OTIMIZADO.md)

### **Canais de Suporte**

- **GitHub Issues**: Para reportar bugs
- **Documentação**: Para consultas técnicas
- **Email**: contato@coinbalance.com (se disponível)

---

## ✅ Histórico de Versões

| Versão | Data | Alterações | Autor |
|--------|------|------------|-------|
| 1.0 | 29/10/2025 | Criação do manual do usuário | Eng. Documentação Sênior |

---

**Status:** ✅ **FASE 4 PARCIAL - MANUAL DO USUARIO COMPLETO**

