from pathlib import Path
from sqlalchemy import create_engine

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
