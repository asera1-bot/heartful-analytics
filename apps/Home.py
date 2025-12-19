import streamlit as st
import pandas as pd
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from db_config import get_engine

st.set_page_config(page_title="Home", layout="wide")
st.title("Heartful Analytics")

@st.cache_data(ttl=60)
def load_monthly():
    engine = get_engine("REAL")
    return pd.read_sql("SELECT COUNT(*) as n FROM v_harvest_monthly", engine)

def sample_monthly():
    return pd.DataFrame({
        "month": ["2025-10", "2025-11", "2025-12"],
        "company": ["東レ", "昭和女子大学", "未定"],
        "total_kg": [120.5, 98.2, 30.0],
    })

try:
    df = load_monthly()
    st.success("Real data mode (v_harvest_monthly)")
except Exception as e:
    df = sample_monthly()
    st.warning("Sample mode (DB未準備/エラー)")
    st.caption(f"{type(e).__name__}: {e}")

st.dataframe(df, use_container_width=True)
st.caption(f"shape={df.shape}")
