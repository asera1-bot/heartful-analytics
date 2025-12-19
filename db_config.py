from __future__ import annotations

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

PROJECT_ROOT = Path(__file__).resolve().parent

DB_DIR = PROJECT_ROOT / "data" / "db"
REAL_DB = DB_DIR / "harvests_real.db"
STAGE_DB = DB_DIR / "harvests_stage.db"

def resolve_db_path(target: str = "REAL") -> Path:
    t = (target or "REAL").upper()
    if t in ("REAL", "PROD", "MAIN"):
        return REAL_DB
    if t in ("STAGE", "STAGING", "DEV"):
        return STAGE_DB
    raise ValueError(f"Unknown DB target: {target}")

def get_engine(target: str = "REAL") -> Engine:
    db_path = resolve_db_path(target)
    if not db_path.exists():
        raise FileNotFoundError(f"DBファイルが見つかりません: {db_path}")
    return create_engine(f"sqlite:///{db_path}", future=True)

def env_target() -> str:
    return os.getenv("HEARTFUL_DB_TARGET", "REAL").upper()

def get_engine_from_env() -> Engine:
    """環境変数 HERTFUL_DB_TARGET で切り替え（任意）。"""
    return get_engine(env_target())
