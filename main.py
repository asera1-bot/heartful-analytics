import pandas as pd
import streamlit as st
from sqlalchemy import text
from db_config import get_engine

st.set_page_config(page_title="はーとふる農園｜ダッシュボード", layout="wide")
st.title("はーとふる農園｜収量ダッシュボード（本番DB接続）")

engine = get_engine()

@st.cache_data(ttl=60)
def load_monthly():
    """本番のDBのmv_harvest_monthlyを読み込む"""
    with engine.begin() as conn:
        query = text("""
            select month, farm, total_kg
            from mv_harvest_monthly
            order by month, farm
        """)
        return pd.read_sql(query, conn)

df = load_monthly()

if df.empty:
    st.warning("データがありません。harvest_monthlyを確認してください。")
else:
    st.subheader("収量一覧")
    st.dataframe(df, use_container_width=True)

    st.subheader("月別・農園別　収量グラフ")
    st.bar_chart(df, x="month", y="total_kg", color="farm")

    summary = df.groupby("month", as_index=False)["total_kg"].sum()
    st.subheader("月別合計")
    st.line_chart(summary, x="month", y="total_kg")
