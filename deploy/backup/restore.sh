#!/bin/sh
# Restore a backup produced by backup.sh into a target database.
# Usage: restore.sh <dump_file> [target_db_name]
#
# Run this ONCE after setting up a new server to verify backups are
# actually restorable (see docs/deployment.md "Restore Drill"), and again
# any time you need to recover from a failure.

set -e

DUMP_FILE="$1"
TARGET_DB="${2:-${POSTGRES_DB}_restore_test}"

if [ -z "$DUMP_FILE" ]; then
    echo "Usage: restore.sh <dump_file> [target_db_name]" >&2
    exit 1
fi

export PGPASSWORD="$POSTGRES_PASSWORD"
HOST="${PGHOST:-db}"

echo "[$(date -Iseconds)] Creating target database '$TARGET_DB' if needed..."
psql -h "$HOST" -U "$POSTGRES_USER" -d postgres -tc \
    "SELECT 1 FROM pg_database WHERE datname = '$TARGET_DB'" | grep -q 1 || \
    psql -h "$HOST" -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE \"$TARGET_DB\""

echo "[$(date -Iseconds)] Restoring $DUMP_FILE into $TARGET_DB..."
pg_restore -h "$HOST" -U "$POSTGRES_USER" -d "$TARGET_DB" --clean --if-exists "$DUMP_FILE"

echo "[$(date -Iseconds)] Restore complete. Verify row counts before trusting this backup, e.g.:"
echo "  psql -h $HOST -U $POSTGRES_USER -d $TARGET_DB -c \"SELECT count(*) FROM patients_patient;\""
