# 🚀 Instruções de Setup - Frontend CoinBalance

## Como Executar o Projeto

### 1. Instalar Node.js

Se ainda não tem o Node.js instalado:

```bash
# Verificar se tem Node.js
node --version

# Se não tiver, instalar:
# macOS (usando Homebrew)
brew install node@18

# Linux (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Windows
# Baixar de: https://nodejs.org/
```

### 2. Instalar Dependências

```bash
cd frontend
npm install
```

Isso vai instalar todas as dependências listadas no `package.json`.

### 3. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env.local

# Editar .env.local se necessário
# O padrão já aponta para http://localhost:8000
```

### 4. Executar em Modo Desenvolvimento

```bash
npm run dev
```

Abra [http://localhost:3000](http://localhost:3000) no navegador.

### 5. Build para Produção

```bash
# Build
npm run build

# Executar build
npm start
```

## 📦 Scripts Disponíveis

- `npm run dev` - Inicia servidor de desenvolvimento
- `npm run build` - Cria build de produção
- `npm start` - Executa build de produção
- `npm run lint` - Executa ESLint
- `npm test` - Executa testes unitários
- `npm run test:e2e` - Executa testes E2E

## 🔧 Estrutura do Código

```
src/
├── app/                 # Páginas Next.js (App Router)
├── components/          # Componentes React
│   ├── ui/             # Componentes UI base
│   ├── layout/         # Layouts
│   └── ...             # Componentes específicos
├── lib/                # Bibliotecas e utilitários
│   ├── api/           # Cliente API
│   ├── hooks/         # Hooks customizados
│   └── utils.ts       # Funções utilitárias
├── services/          # Serviços de negócio
└── types/             # Tipos TypeScript
```

## ⚠️ Troubleshooting

### Porta 3000 em uso

```bash
# Usar porta diferente
npm run dev -- -p 3001
```

### Erros de instalação

```bash
# Limpar cache e reinstalar
rm -rf node_modules package-lock.json
npm install
```

### API não conecta

Verifique se:
1. Backend está rodando em `http://localhost:8000`
2. Arquivo `.env.local` está configurado corretamente
3. Não há firewall bloqueando

## 📚 Próximos Passos

1. Ver documentação completa em `/docs/frontend/`
2. Implementar páginas de Dashboard, Carteiras, Transações
3. Adicionar testes
4. Configurar CI/CD

## 🆘 Precisa de Ajuda?

- Ver: `/docs/frontend/TROUBLESHOOTING.md`
- Documentação: `/docs/frontend/README.md`
- Issues: GitHub Issues
