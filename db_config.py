from pathlib import Path
from sqlalchemy import create_engine, text
import pandas as pd

# プロジェクトのルートディレクトリ
BASE_DIR = Path(__file__).resolve().parent

def resolve_db_path(env: str = "real") -> Path:
    """
    利用するDBファイルの絶対パスを返す。
    env: "real" | "stage" | "dev"
    """
    db_map = {
        "real": BASE_DIR / "data" / "db" / "harvests_real.db",
        "stage": BASE_DIR / "data" / "db" / "harvests_stage.db",
        "dev": BASE_DIR / "data" / "db" / "harvests.db",
    }

    path = db_map.get(env, db_map["real"])

    if not path.exists():
        raise FileNotFoundError(f"DBファイルが見つかりません: {path}")

    return path

def get_engine(env: str = "real"):
    """
    SQLAlchemy の Engine を返す。
    """
    db_path = resolve_db_path(env)
    return create_engine(f"sqlite:///{db_path}", future=True)

def read_sql_safe(engine, sql: str, params: dict | None = None) -> pd.DataFrame:
    """SQLを安全に実行。失敗したら例外をそのまま投げる（呼び出し側でフォールバック）。"""
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params or {})
