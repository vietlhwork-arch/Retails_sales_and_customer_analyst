from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="AdventureWorks Analytics", layout="wide")

st.title("AdventureWorks Analytics")
st.caption("Retail sales, customer, product, and territory analysis")

processed = Path("data/processed/master_sales.csv")

@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

if not processed.exists():
    st.warning("Chưa thấy data/processed/master_sales.csv. Hãy chạy preprocessing trước.")
    st.stop()

df = load_data(processed)

def choose_col(options):
    for c in options:
        if c in df.columns:
            return c
    return None

sales_col = choose_col(["revenue", "profit", "orderquantity"])
time_col = choose_col(["order_month", "order_year", "orderdate"])
geo_col = choose_col(["country", "region", "continent", "territorykey"])
product_col = choose_col(["categoryname", "subcategoryname", "productname", "productkey"])

k1, k2, k3, k4 = st.columns(4)
k1.metric("Rows", f"{len(df):,}")
k2.metric("Columns", f"{df.shape[1]:,}")
if "revenue" in df.columns:
    k3.metric("Total Revenue", f"{df['revenue'].fillna(0).sum():,.2f}")
if "profit" in df.columns:
    k4.metric("Total Profit", f"{df['profit'].fillna(0).sum():,.2f}")

left, right = st.columns([1, 1])

with left:
    st.subheader("Revenue by Time")
    if time_col and sales_col:
        t = df.groupby(time_col, dropna=False, as_index=False)[sales_col].sum().sort_values(time_col)
        fig = px.line(t, x=time_col, y=sales_col, markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Không đủ cột thời gian/doanh thu.")

with right:
    st.subheader("Revenue by Geography")
    if geo_col and sales_col:
        g = df.groupby(geo_col, dropna=False, as_index=False)[sales_col].sum().sort_values(sales_col, ascending=False).head(10)
        fig = px.bar(g, x=geo_col, y=sales_col)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Không đủ cột địa lý/doanh thu.")

st.subheader("Top Products / Categories")
if product_col and sales_col:
    p = df.groupby(product_col, dropna=False, as_index=False)[sales_col].sum().sort_values(sales_col, ascending=False).head(10)
    st.dataframe(p, use_container_width=True)

st.subheader("Raw Preview")
st.dataframe(df.head(50), use_container_width=True)
