import streamlit as st
import pandas as pd
from df_config import get_engine

st.set_page_config(page_title="EDA", layout="wide")
st.title("07_EDA(目次)")

def sample_df():
    return pd.DataFrame({
        "month": ["2025-10", "2025-11", "2025-12"],
        "company": ["東レ", "昭和女子大学", "未定"],
        "total_kg": [120.5, 98.2, 30.0],
    })

@st.cache_date(ttl=60)
def load_monthly():
    try:
        engine = get_engine()
        df = pd.read_sql("SELECT * FROM v_harvest_monthly", engine)
        return df, "real", None
    except Exception as e:
        return samplt_df(), "sample", e

df, mode, err = load_monthly()

if mode == "real":
    st.success("DBから読み込み（v_harvest_monthly)")
else:
    st.warning("サンプルデータで起動（DB未準備/エラー）")
    st.caption(f"{type(err).__name__}: {err}")

st.subheader("先頭")
st.dataframe(df.head(30), use_container_width=True)

st.subheader("統計")
st.write("shape:", df.shape)
st.dataframe(df.describe(include="all"), use_container_width=True)

