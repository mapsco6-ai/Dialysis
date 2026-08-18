#!/bin/sh
# Nightly Postgres backup with daily/weekly/monthly retention.
# Scheduled via cron inside the `backup` service (see deploy/docker-compose.yml).
#
# Retention is controlled by BACKUP_RETENTION_DAILY/WEEKLY/MONTHLY env vars
# (defaults: 14 daily, 8 weekly, 6 monthly), matching docs/deployment.md.

set -e

BACKUP_ROOT="/backups"
DAILY_DIR="$BACKUP_ROOT/daily"
WEEKLY_DIR="$BACKUP_ROOT/weekly"
MONTHLY_DIR="$BACKUP_ROOT/monthly"

RETENTION_DAILY="${BACKUP_RETENTION_DAILY:-14}"
RETENTION_WEEKLY="${BACKUP_RETENTION_WEEKLY:-8}"
RETENTION_MONTHLY="${BACKUP_RETENTION_MONTHLY:-6}"

mkdir -p "$DAILY_DIR" "$WEEKLY_DIR" "$MONTHLY_DIR"

export PGPASSWORD="$POSTGRES_PASSWORD"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
DAY_OF_WEEK="$(date +%u)"   # 1=Monday .. 7=Sunday
DAY_OF_MONTH="$(date +%d)"

DUMP_FILE="$DAILY_DIR/dialysis_${TIMESTAMP}.dump"

echo "[$(date -Iseconds)] Starting backup -> $DUMP_FILE"
pg_dump -h "${PGHOST:-db}" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc -f "$DUMP_FILE"
echo "[$(date -Iseconds)] Backup complete: $(du -h "$DUMP_FILE" | cut -f1)"

if [ "$DAY_OF_WEEK" = "7" ]; then
    cp "$DUMP_FILE" "$WEEKLY_DIR/"
fi

if [ "$DAY_OF_MONTH" = "01" ]; then
    cp "$DUMP_FILE" "$MONTHLY_DIR/"
fi

prune() {
    dir="$1"
    keep="$2"
    # shellcheck disable=SC2012
    ls -1t "$dir"/*.dump 2>/dev/null | tail -n "+$((keep + 1))" | xargs -r rm -f
}

prune "$DAILY_DIR" "$RETENTION_DAILY"
prune "$WEEKLY_DIR" "$RETENTION_WEEKLY"
prune "$MONTHLY_DIR" "$RETENTION_MONTHLY"

echo "[$(date -Iseconds)] Retention applied (daily=$RETENTION_DAILY weekly=$RETENTION_WEEKLY monthly=$RETENTION_MONTHLY)"
