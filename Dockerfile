# Dockerfile para Coinbalance - A Economia da Consciência
FROM python:3.14-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV MOEDA=CNB
ENV PLATAFORMA=Coinbalance

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libssl-dev \
    libffi-dev \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências primeiro (cache layer)
COPY requirements.txt .
COPY requirements-dev.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p /app/backups /app/logs /app/data /app/htmlcov

# Criar usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expor porta
EXPOSE 8000

# Comando de saúde (melhor prática: usar timeout mais longo para inicialização)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health/live || exit 1

# Comando para iniciar a aplicação
CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8000"]
