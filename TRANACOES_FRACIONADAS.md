# 💰 Sistema de Transações Fracionadas CNB

## 📋 Visão Geral

O sistema Coinbalance agora suporta **transações fracionadas** com precisão decimal de **8 casas decimais**, permitindo negociação de valores extremamente pequenos e conversão entre diferentes unidades.

## 🔢 Unidades Disponíveis

### 1. **CNB (Coinbalance)**
- **Unidade principal** da moeda
- **Precisão**: 8 casas decimais
- **Símbolo**: CNB
- **Exemplo**: 1.12345678 CNB

### 2. **Satoshi**
- **Menor unidade** possível
- **Precisão**: 0 casas decimais (números inteiros)
- **Símbolo**: sat
- **Conversão**: 1 CNB = 100,000,000 satoshis
- **Exemplo**: 112345678 sat

### 3. **mCNB (Micro CNB)**
- **Unidade intermediária**
- **Precisão**: 6 casas decimais
- **Símbolo**: mCNB
- **Conversão**: 1 CNB = 1,000,000 mCNB
- **Exemplo**: 1123456.78 mCNB

## 🚀 Funcionalidades Implementadas

### 1. **Transações com Precisão Decimal**

```python
# Exemplo de transação com 8 casas decimais
transacao = {
    "remetente": "CNB_abc123...",
    "destinatario": "CNB_def456...",
    "valor": 0.12345678,  # 8 casas decimais
    "unidade": "cnb"
}
```

### 2. **Conversão de Unidades**

```python
# Converter 1.5 CNB para satoshis
POST /conversao/unidades
{
    "valor": 1.5,
    "unidade_origem": "cnb",
    "unidade_destino": "satoshi"
}

# Resultado: 150000000 sat
```

### 3. **Transações Fracionadas**

```python
# Transação em satoshis
POST /transacoes/fracionada
{
    "remetente": "CNB_abc123...",
    "destinatario": "CNB_def456...",
    "valor": 1000000,  # 1 milhão de satoshis
    "unidade": "satoshi"
}
```

### 4. **Cálculo Automático de Taxas**

```python
# Calcular taxa para transação
GET /transacoes/calcular-taxa?valor=0.001&unidade=cnb

# Resultado:
{
    "valor_original": "0.001 CNB",
    "valor_cnb": "0.00100000 CNB",
    "taxa_cnb": "0.00000001 CNB",
    "taxa_satoshi": "1 sat",
    "total_necessario": "0.00100001 CNB"
}
```

## 📊 Endpoints da API

### **Transações**

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/transacoes/criar` | POST | Criar transação com suporte a unidades |
| `/transacoes/fracionada` | POST | Criar transação fracionada |
| `/transacoes/calcular-taxa` | GET | Calcular taxa de transação |

### **Conversão**

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/conversao/unidades` | POST | Converter entre unidades |
| `/conversao/info` | GET | Informações sobre unidades |

### **Carteiras**

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/carteiras/{endereco}/saldo/detalhado` | GET | Saldo em todas as unidades |

## 🔧 Exemplos de Uso

### **1. Transação Mínima (1 Satoshi)**

```bash
curl -X POST "http://localhost:8000/transacoes/fracionada" \
  -H "Content-Type: application/json" \
  -d '{
    "remetente": "CNB_abc123...",
    "destinatario": "CNB_def456...",
    "valor": 0.00000001,
    "unidade": "cnb"
  }'
```

### **2. Conversão de Unidades**

```bash
curl -X POST "http://localhost:8000/conversao/unidades" \
  -H "Content-Type: application/json" \
  -d '{
    "valor": 1.5,
    "unidade_origem": "cnb",
    "unidade_destino": "satoshi"
  }'
```

### **3. Saldo Detalhado**

```bash
curl -X GET "http://localhost:8000/carteiras/CNB_abc123.../saldo/detalhado"
```

## ⚙️ Configurações Técnicas

### **Precisão Decimal**
- **Precisão**: 8 casas decimais
- **Valor mínimo**: 0.00000001 CNB (1 satoshi)
- **Valor máximo**: 100,000,000 CNB
- **Biblioteca**: Python `decimal.Decimal`

### **Validação**
- **Estrutura**: Campos obrigatórios validados
- **Assinatura**: Verificação criptográfica
- **Saldo**: Verificação de saldo suficiente
- **Gastos duplos**: Prevenção automática
- **Valores**: Validação de limites

### **Taxas**
- **Taxa base**: 0.1% do valor da transação
- **Taxa mínima**: 0.00000001 CNB (1 satoshi)
- **Cálculo**: Automático com precisão decimal

## 🧪 Testando o Sistema

### **1. Executar Demonstração**

```bash
python demo_transacoes_fracionadas.py
```

### **2. Testar Conversões**

```python
# Converter 1 CNB para satoshis
valor_satoshi = converter_para_unidades(1.0, "satoshi")
# Resultado: 100000000.0

# Converter 100000000 satoshis para CNB
valor_cnb = converter_de_unidades(100000000, "satoshi")
# Resultado: 1.0
```

### **3. Validar Precisão**

```python
# Teste de precisão
valor_original = 0.12345678
valor_convertido = converter_de_unidades(
    converter_para_unidades(valor_original, "satoshi"), 
    "satoshi"
)
# Deve ser igual ao valor original
```

## 🔒 Segurança

### **Validações Implementadas**
- ✅ Verificação de estrutura da transação
- ✅ Validação de assinatura digital
- ✅ Verificação de saldo suficiente
- ✅ Prevenção de gastos duplos
- ✅ Validação de limites de valor
- ✅ Cálculo preciso de taxas

### **Precisão Garantida**
- ✅ Uso de `decimal.Decimal` para cálculos
- ✅ Arredondamento consistente
- ✅ Validação de valores mínimos/máximos
- ✅ Prevenção de overflow/underflow

## 📈 Benefícios

### **Para Usuários**
- 💰 **Microtransações**: Enviar valores mínimos (1 satoshi)
- 🔄 **Flexibilidade**: Usar a unidade mais conveniente
- 📊 **Transparência**: Ver valores em todas as unidades
- ⚡ **Precisão**: Cálculos exatos sem perda de precisão

### **Para Desenvolvedores**
- 🛠️ **API Completa**: Endpoints para todas as operações
- 📝 **Documentação**: Swagger/OpenAPI automático
- 🧪 **Testes**: Scripts de demonstração incluídos
- 🔧 **Configurável**: Parâmetros ajustáveis

## 🚀 Próximos Passos

1. **Interface Web**: Criar interface para transações fracionadas
2. **Mobile App**: Suporte nativo em aplicativo móvel
3. **Exchange Integration**: Integração com exchanges
4. **Advanced Features**: Ordens limitadas, stop-loss, etc.

## 📞 Suporte

Para dúvidas ou problemas:
- 📧 Email: support@coinbalance.com.br
- 💬 Discord: https://discord.gg/coinbalance
- 📖 Documentação: `/docs` na API

---

**Coinbalance - A Economia da Consciência** 💚