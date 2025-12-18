import streamlit as st
import pandas as pd
from sqlalchemy import text
from datetime import datetime

from db_config import get_engine

st.set_page_config(page_title="Heartful Analytics", layout="wide")
st.title("はーとふる農園ダッシュボード(Stage)")

engine = get_engine()

@st.cache_data(ttl=60)
def load_counts():
    q = """
    select 'raw_csv' as tbl, count(*) as rows from raw_csv
    union all select 'env_header', count(*) from env_header
    union all select 'env_rows', count(*) from env_rows
    union all select 'staging', count(*) from staging_monthly
    union all select 'harvest', count(*) from harvest_monthly
    """
    return pd.read_sql(q, engine)

@st.cache_data(ttl=60)
def load_harvest_summary():
    q = """
    select month, sum(total_kg) as total_kg
    from harvest_monthly
    group by month
    order by month
    """
    return pd.read_sql(q, engine)

col1, col2 = st.columns([1,2], gap="large")

with col1:
    st.subheader("テーブル件数")
    st.dataframe(load_counts(), use_container_width=True, hide_index=True)

with col2:
    st.subheader("月次合計（全ファーム）")
    df = load_harvest_summary()
    if not df.empty:
        st.bar_chart(df, x="month", y="total_kg")
    else:
        st.info("harvest_monhtly が空です。")

def sample_harvest_df() -> pd.DataFrame:
    return pd.DataFrame({
        "harvest_date": pd.to_datetime(["2025-12-01", "2025-12-02", "2025-12-03"]),
        "company": ["東レ", "昭和女子大学", "未定"},
        "farm": ["A1", "B2", "C1"],
        "crop": ["べビーリーフ", "イチゴ", "べビーリーフ"],
        "kg": [12.4, 8.1, 15.0],
    })

def load_harvest_df():
    """本物→ダメならサンプル。状態も返す。"""
    try:
        engine = get_engien()
        df = pd.read_sql("SELECT * FROM harvest_fact LIMIT 200", engine)
        return df, "real", None
    except Exception as e:
        retun sample_harvest_df(), "sample", e

df, mode, err = load_harvset_df()

if mode == "real":
    st.success("Real data mode (DBから読み込み)")
else:
    st.warning("Sample mode（DB未準備/エラーのためサンプルで準備)")
    st.caption(f"原因: {type(err).__name__}: {err}")

st.dataframe(df)
