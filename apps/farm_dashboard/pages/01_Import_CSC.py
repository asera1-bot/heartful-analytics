import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st
import yaml

def find_project_root(start: Path) -> Path:
    for p in [start] + list(start.parents):
        if (p / "config" / "app.yaml").exists():
            return p
    raise FileNotFoundError("config/app.yaml not found")

ROOT = find_project_root(Path(__file__).resolve())
CFG = yaml.safe_load((ROOT / "config" / "app.yaml").read_text(encoding="utf-8"))
DB = (ROOT / CFG["db_path"]).resolve()

st.set_page_config(page_title="CSVを取り込み", layout="wide")
st.title("収量CSV取り込み（継続運用）")

# Debug
with st.expander("Debug（環境確認）", expanded=False):
    st.write("ROOT:", str(ROOT))
    st.write("DB:", str(DB))
    st.write("DB exists:", DB.exists())
    st.write("DB parent exists:", DB.parent.exists())

# DBフォルダだけは必ず作る（ファイルが無いなら作成される）
DB.parent.mkdir(parents=True, exist_ok=True)

# SQLite接続（失敗理由を画面に出す）
try:
    conn = sqlite3.connect(str(DB))
except Exception as e:
    st.error(f"SQLite connect failed: {e}")
    st.stop()

# テンプレ
TEMPLATE = pd.DataFrame(
    {
        "farm": ["愛川c1"],
        "month": ["2025-10"],
        "total_kg": [123.4],
    }
)

with st.expander("CSVテンプレートを確認", expanded=False):
    st.dataframe(TEMPLATE, use_container_width=True, hide_index=True)

st.caption("CSV列: farm, month, total_kg(UTF-8推奨)")
file = st.file_uploader("CSVファイルを選択", type=["csv"])
if not file:
    st.stop()

# 読み込み(file)
def read_csv_flexible(file):
    for enc in ("utf-8-sig", "utf-8", "cp932"):
        try:
            file.seek(0) # 重要:毎回先頭に戻す
            return pd.read_csv(file, encoding=enc)
        except UnicodeDecodeError:
            continue
        except pd.errors.EmptyDataError:
            continue
    raise ValueError("CSVの文字コードを判別できません（UTF-8　/　CP932非対応 or 空ファイル）")
    
df = read_csv_flexible(file)    

st.write("読み込めた列名:", list(df.columns))
st.dataframe(df.head(5), use_container_width=True)

# 列名マッピング（実CSV　→　内部仕様）
colmap = {
    "企業名": "farm",
    "収穫日": "date",
    "収穫量（ｇ）": "total_g",
}

df = df.rename(columns=colmap)

required_src = {"farm", "month", "total_kg"}
missing_src = required_src - set(df.columns)
if missing:
    st.error(f"CSVに必須列が不足: {sorted(missing_src)}")
    st.stop()

# 変換処理(日時→月次、g→kg)
df["farm"] = df["farm"].astype(str).str.strip()
df["month"] = pd.to_datetime(df["date"], errors="coerce").dt.to_period("M").astype(str)
df["total_kg"] = pd.to_numeric(df["total_g"], errors="coerce") / 1000.0

df = df[["farm", "month", "total_kg"]]
df = df.groupby(["farm", "month"], as_index=False)["total_kg"].sum()

# 変換後チェック
required = {"farm", "month", "total_kg"}
missing = required - set(df.columns)
if missing:
    st.error(f"変換後に必須列が不足: {sorted(missing)}")
    st.stop()

st.subheader("取り込みプレビュー")
st.dataframe(df, use_container_width=True, hide_index=True)

# 取り込み
# ここでは[harvest_monthly] [mv_harvest_monthly] をテーブルとして運用する想定
# 無ければ作る
def ensure_tables(c: sqlite3.Connection) -> None:
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS harvest_monthly (
            farm TEXT NOT NULL,
            month TEXT NOT NULL,
            total_kg REAL NOT NULL,
            PRIMARY KEY (farm, month)
        );
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS mv_harvest_monthly (
            month TEXT NOT NULL,
            farm TEXT NOT NULL,
            total_kg REAL NOT NULL,
            PRIMARY KEY (farm, month)
        );
        """
    )

def refresh_mv(c: sqlite3.Connection) -> None:
    c.execute("DELETE FROM mv_harvest_monthly;")
    c.execute(
        """
        INSERT INTO mv_harvest_monthly (month, farm, total_kg)
        SELECT month, farm, SUM(total_kg)
        FROM harvest_monthly
        GROUP BY month, farm;
        """
    )

if st.button("取り込む(UPSERT)", type="primary"):
    try:
        ensure_tables(conn)

        rows = df.to_records(index=False)
        conn.executemany(
            """
            INSERT INTO harvest_monthly (farm, month, total_kg)
            VALUES (?, ?, ?)
            ON CONFLICT(farm, month) DO UPDATE SET
                total_kg = excluded.total_kg;
            """,
            rows,
        )

        refresh_mv(conn)
        conn.commit()
        st.success(f"取り込み完了: {len(df)}行")
    except Exception as e:
        conn.rollback()
        st.error(f"取り込み失敗: {e}")
        st.stop()
