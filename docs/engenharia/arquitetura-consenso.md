"""
ARQUITETURA DE CONSENSO CNB - Sistema Híbrido PoW/PoS

Este documento explica como o sistema de consenso CNB funciona,
resolvendo o conflito entre Proof of Work e Proof of Stake.

## DECISÃO ARQUITETURAL

O CNB usa um sistema HÍBRIDO que combina:
- **Proof of Work (PoW)**: Para mineração de blocos e criação de CNB
- **Proof of Stake (PoS)**: Para validação de transações e governança

## COMO FUNCIONA

### 1. MINERAÇÃO (PoW)
- Miners competem para encontrar o nonce correto
- Recompensas são distribuídas para miners
- Dificuldade é ajustada dinamicamente
- Tempo de bloco: 5 segundos

### 2. VALIDAÇÃO (PoS)
- Validators com stake mínimo validam transações
- Validators recebem parte das recompensas (15%)
- Sistema de slashing para validators maliciosos
- Governança participativa via propostas

### 3. DISTRIBUIÇÃO DE RECOMPENSAS
- 85% para miners (PoW)
- 15% para validators (PoS)
- Taxas são "queimadas" (reduzem supply)

## VANTAGENS DO SISTEMA HÍBRIDO

1. **Segurança**: PoW protege contra ataques de 51%
2. **Eficiência**: PoS valida transações rapidamente
3. **Descentralização**: Qualquer um pode minerar ou validar
4. **Sustentabilidade**: Menos consumo de energia que PoW puro
5. **Governança**: Stakeholders participam das decisões

## IMPLEMENTAÇÃO

### Arquivos Principais:
- `src/domain/blockchain/`: Implementa PoW (mineração)
- `src/domain/consensus/`: Implementa PoS (validação)
- `src/infrastructure/config/blockchain_config.py`: Configurações unificadas

### Fluxo de Funcionamento:
1. Miner cria bloco usando PoW
2. Validators verificam transações usando PoS
3. Bloco é adicionado à blockchain
4. Recompensas são distribuídas
5. Sistema de governança pode propor mudanças

## CONFIGURAÇÕES

- Tempo de bloco: 5 segundos
- Stake mínimo para validação: 1000 CNB
- Taxa de recompensa para validators: 15%
- Halving: A cada 10 anos
- Inflação anual: 2% (primeiros 10 anos)

Este sistema híbrido oferece o melhor dos dois mundos:
a segurança do PoW e a eficiência do PoS.
