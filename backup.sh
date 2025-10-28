#!/bin/bash
# CoinBalance Web3 Backup Script

set -e

BACKUP_DIR="/app/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="coinbalance_backup_${TIMESTAMP}.sql"

echo "💾 Iniciando backup do banco de dados..."

# Criar backup do PostgreSQL
docker-compose -f docker-compose.production.yml exec -T postgres \
    pg_dump -U coinbalance coinbalance_prod > "${BACKUP_DIR}/${BACKUP_FILE}"

# Comprimir backup
gzip "${BACKUP_DIR}/${BACKUP_FILE}"

# Remover backups antigos (manter apenas últimos 7 dias)
find "${BACKUP_DIR}" -name "coinbalance_backup_*.sql.gz" -mtime +7 -delete

echo "✅ Backup concluído: ${BACKUP_FILE}.gz"
