#!/bin/bash
set -e

BACKUP_DIR="./backups/$(date +%Y-%m-%d_%H-%M-%S)"

echo "💾 Creating backup..."
echo "==================="

mkdir -p "$BACKUP_DIR"

# Backup database
echo "📊 Backing up database..."
docker-compose exec -T bedrock-db mysqldump -u root -p"${MYSQL_ROOT_PASSWORD:-rootpassword123}" wordpress > "$BACKUP_DIR/database.sql"

# Backup WordPress uploads
echo "📁 Backing up WordPress files..."
docker-compose exec -T bedrock tar czf - /app/web/app/uploads > "$BACKUP_DIR/wp-uploads.tar.gz"

# Backup environment and configuration
echo "⚙️  Backing up configuration..."
cp .env "$BACKUP_DIR/env-backup"
cp docker-compose.yml "$BACKUP_DIR/"

# Create backup info
cat > "$BACKUP_DIR/backup-info.txt" << BACKUP_EOF
WordPress MCP Server Backup
Created: $(date)
Services: $(docker-compose ps --services | tr '\n' ' ')
BACKUP_EOF

echo "✅ Backup completed: $BACKUP_DIR"
echo ""
echo "To restore: ./restore.sh $BACKUP_DIR"
