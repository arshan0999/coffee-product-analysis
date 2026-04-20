import streamlit as st
import pandas as pd
import plotly.express as px

st.title("☕ Afficionado Coffee Product Analytics")

# Load Data
df = pd.read_csv("data/coffee.csv")

# Data Cleaning
df = df.dropna()
df = df[df["transaction_qty"] > 0]
df = df[df["unit_price"] > 0]

# Create Revenue Column
df["revenue"] = df["transaction_qty"] * df["unit_price"]

# =======================
# SIDEBAR FILTERS
# =======================

category = st.sidebar.selectbox(
    "Select Category",
    df["product_category"].unique()
)

store = st.sidebar.selectbox(
    "Select Store",
    df["store_location"].unique()
)

top_n = st.sidebar.slider("Top N Products", 5, 20, 10)

# =======================
# APPLY FILTERS (IMPORTANT FIX)
# =======================

filtered = df[
    (df["product_category"] == category) &
    (df["store_location"] == store)
]

# =======================
# TOTAL REVENUE (FIXED)
# =======================

total_revenue = filtered["revenue"].sum()
st.metric("Total Revenue", round(total_revenue, 2))

# =======================
# TOP N PRODUCTS (FIXED)
# =======================

rank = (
    filtered.groupby("product_detail")["revenue"]
    .sum()
    .reset_index()
    .sort_values(by="revenue", ascending=False)
    .head(top_n)
)

fig = px.bar(
    rank,
    x="product_detail",
    y="revenue",
    title=f"Top {top_n} Products by Revenue"
)

st.plotly_chart(fig)

# =======================
# CATEGORY PIE
# =======================

cat = (
    filtered.groupby("product_type")["revenue"]
    .sum
)
