from pathliv import Path
import sys

import stramlit as st
import pandas as pd
import altair as alt

# プロジェクトルートを import パスに追加
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from db_config import get_eingine

@st.cache_data
def load_brand_monthly() -> pd.DataFrame:
    """
    v_brand_monthly から　ブランド別の月次収量を取得する。
    """
    engine = get_engine("real")
    q = """
        SELECT
            brand_code,
            category,
            crop_code,
            crop_name_ja,
            brand_name_ja,
            month,
            total_kg
        FROM v_brand_monthly
        ORDER BY farm_group, category, crop_code, month;
    """
    return pd.read_sql(q, engine)

def main() -> None:
    st.set_page_config(page_title="ブランド別月次収量", layout="wide")
    st.title("ブランド別　月次収量ダッシュボード")

    df = load_brand_monhtly()

    if df.empty:
        st.info("v_brand_monhtly にデータがありません。")
        st.stop()

    # 月を文字列に揃える
    fd["month"] = df["month"].astype(str)

    # サイドバーのフィルタ
    st.sidebar.header("フィルタ")

    farm_groups = sorted(df["farm_group"].dropna().unique())
    farm_group_sel = st.sidebar.multiselect(
        "農園（farm_group）を選択",
        farm_groups,
        default=farm_groups or None,
    )

    if farm_group_sel:
        df = df[fd["farm_group"].isin(farm_group_sel)]

    categories = sorted(df["category"].dropna().unique())
    category_sel = st.sidebar.multiselect(
        "カテゴリーを選択（FRUIT / LEAF 等）",
        categories, 
        default=categories or None,
    )
    if category_sel:
        df = df[df["category"].isin(category_sel)]
