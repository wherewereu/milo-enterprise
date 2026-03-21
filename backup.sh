#!/bin/bash
BACKUP_DATE=$(date +%Y-%m-%d)
BACKUP_DIR=~/Library/Mobile\ Documents/com~apple~CloudDocs/MiloBackup/$BACKUP_DATE
mkdir -p "$BACKUP_DIR"
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/"
cp ~/.openclaw/amazon-cookies.json "$BACKUP_DIR/" 2>/dev/null || true
cp ~/.openclaw/linkedin-cookies.json "$BACKUP_DIR/" 2>/dev/null || true
cp ~/.openclaw/agent-bot-tokens.json "$BACKUP_DIR/" 2>/dev/null || true
cp ~/.openclaw/discord-post.py "$BACKUP_DIR/" 2>/dev/null || true
cp ~/.openclaw/refresh-amazon-cookies.sh "$BACKUP_DIR/" 2>/dev/null || true
cp ~/.openclaw/refresh-linkedin-cookies.sh "$BACKUP_DIR/" 2>/dev/null || true
cp -r ~/.openclaw/workspace/ "$BACKUP_DIR/workspace/"
cp -r ~/.openclaw/skills/ "$BACKUP_DIR/skills/" --ignore-failed-read 2>/dev/null || rsync -a --exclude='.git' ~/.openclaw/skills/ "$BACKUP_DIR/skills/"
# Keep last 4 backups only
ls -dt ~/Library/Mobile\ Documents/com~apple~CloudDocs/MiloBackup/*/ | tail -n +5 | xargs rm -rf 2>/dev/null || true
echo "Backup complete: $BACKUP_DATE"
