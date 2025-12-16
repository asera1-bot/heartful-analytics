#!/usr/bin/env bash
set -euo pipefail

SRC="${1:-$HOME/heartful-analytics/data/db/harvests_real.db}"
DST_DIR="${2:-/mnt/c/Users/fclsa/Backups/heartful-analytics-db}"
TS="$(date +%Y%m%d_%H%M%S)"

mkdir -p "$DST_DIR"
cp "$SRC" "$DST_DIR/harvests_real_$TS.db"
echo "[OK] backed up to $DST_DIR/harvests_real_$TS.db"

