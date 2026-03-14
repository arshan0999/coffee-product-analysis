import streamlit as st
import pandas as pd
import plotly
import plotly.express as px

st.title("☕ Afficionado Coffee Product Analytics")

df = pd.read_csv("data/coffee.csv")

df = df.dropna()

df = df[df["transaction_qty"] > 0]
df = df[df["unit_price"] > 0]

df["revenue"] = df["transaction_qty"] * df["unit_price"]

total_revenue = df["revenue"].sum()

st.metric("Total Revenue", round(total_revenue,2))

# Sidebar Filters

category = st.sidebar.selectbox(
    "Select Category",
    df["product_category"].unique()
)

store = st.sidebar.selectbox(
    "Select Store",
    df["store_location"].unique()
)

top_n = st.sidebar.slider("Top N Products",5,20,10)

filtered = df[
    (df["product_category"] == category) &
    (df["store_location"] == store)
]

# Product Ranking

rank = filtered.groupby("product_detail")["revenue"].sum().reset_index()

rank = rank.sort_values(by="revenue", ascending=False).head(top_n)

fig = px.bar(rank, x="product_detail", y="revenue", title="Top Products by Revenue")

st.plotly_chart(fig)

# Category Pie

cat = filtered.groupby("product_type")["revenue"].sum().reset_index()

fig2 = px.pie(cat, names="product_type", values="revenue")

st.plotly_chart(fig2)

# Scatter

scatter = filtered.groupby("product_detail").agg({
    "transaction_qty":"sum",
    "revenue":"sum"
}).reset_index()

fig3 = px.scatter(
    scatter,
    x="transaction_qty",
    y="revenue",
    size="revenue",
    hover_name="product_detail",
    title="Popularity vs Revenue"
)

st.plotly_chart(fig3)

st.dataframe(scatter.sort_values(by="revenue", ascending=False))
