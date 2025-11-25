import argparse
import sqlite3
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "db" / "harvests.db"

CREATE_MV_SQL = """
CREATE TABLE IF NOT EXISTS mv_farm_month_totals (
  month    TEXT NOT NULL,
  farm     TEXT NOT NULL,
  total_kg REAL NOT NULL,
  PRIMARY KEY (month, farm)
);
"""

FULL_REFRESH_SQL = """
INSERT INTO mv_farm_month_totals(month, farm, total_kg)
SELECT month, farm, SUM(total_kg)
FROM harvest_monthly
GROUP BY month, farm
ON CONFLICT(month, farm) DO UPDATE SET
  total_kg = excluded.total_kg;
"""

DELTA_SQL = """
INSERT INTO mv_farm_month_totals(month, farm, total_kg)
VALUES (?, ?, ?)
ON CONFLICT(month, farm) DO UPDATE SET
  total_kg = total_kg + ?;
"""

def assert_source_tables(conn: sqlite3.Connection):
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='harvest_monthly'"
    )
    if cur.fetchone() is None:
        raise RuntimeError(
            "'harvest_monthly' が見つかりません。\n"
            f"DB: {DB_PATH}\n"
            "sqlite3 で `.tables` を実行して DB パスが正しいか確認してください。"
        )

def ensure_db_exists():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"DB not found: {DB_PATH.resolve()} "
            "(パスを確認してください。'db/harvests.db')"
        )

def ensure_schema(conn: sqlite3.Connection):
    conn.execute(CREATE_MV_SQL)

def run_full(conn: sqlite3.Connection):
    ensure_schema(conn)
    conn.execute(FULL_REFRESH_SQL)
    conn.commit()

def run_delta(conn: sqlite3.Connection, month: str, farm: str, kg: float):
    ensure_schema(conn)
    conn.execute(DELTA_SQL, (month, farm, kg, kg))
    conn.commit()

def show_mv(conn: sqlite3.Connection, limit: int = 20):
    df = pd.read_sql(
        """
        SELECT month, farm, total_kg
        FROM mv_farm_month_totals
        ORDER BY month, farm
        LIMIT ?;
        """,
        conn,
        params=(limit,),
    )
    print(df.to_string(index=False))

def main():
    parser = argparse.ArgumentParser(description="Refresh or delta-update mv_farm_month_totals")
    parser.add_argument("--mode", choices=["full", "delta"], default="delta")
    parser.add_argument("--month", default="2025-10")
    parser.add_argument("--farm", default="FarmA")
    parser.add_argument("--kg", type=float, default=5.0)
    parser.add_argument("--show", action="store_true", help="print top rows after update")
    args = parser.parse_args()

    ensure_db_exists()

    with sqlite3.connect(str(DB_PATH)) as conn:
        assert_source_tables(conn)
        if args.mode == "full":
            run_full(conn)
            print("[OK] Full refresh done.")
        else:
            run_delta(conn, args.month, args.farm, args.kg)
            print(f"[OK] Delta applied: ({args.month}, {args.farm}, +{args.kg})")

        if args.show:
            show_mv(conn)

if __name__ == "__main__":
    main()

