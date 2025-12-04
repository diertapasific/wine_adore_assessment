import streamlit as st
import pandas as pd
import plotly.express as px
from src.preprocessing import preprocess
from src.model import CustomerModel
from src.date_filter import filter_by_date
from src.insights import compute_insights
from src.recommender import generate_sales_recommendation

st.set_page_config(page_title="Wine Customer Sales Dashboard", layout="wide")

# Load data
df = pd.read_csv("data/customers.csv", sep="\t")
df = preprocess(df)

# Load model
model = CustomerModel()
model.load()
df = model.predict(df)

st.title("🍷 Wine Customer Insight Dashboard for Sales Team")
st.markdown("#### Understand customer segments, purchase patterns, and sales opportunities.")

# --- Sidebar Filters ---
st.sidebar.header("📅 Date Filter")
start_year = st.sidebar.selectbox("Start Year", sorted(df["Dt_Customer"].dt.year.unique()))
start_month = st.sidebar.selectbox("Start Month", list(range(1, 13)))
end_year = st.sidebar.selectbox("End Year", sorted(df["Dt_Customer"].dt.year.unique()))
end_month = st.sidebar.selectbox("End Month", list(range(1, 13)))

df_filtered = filter_by_date(df, start_year, start_month, end_year, end_month)

if df_filtered.empty:
    st.warning("No data available for the selected period.")
    st.stop()

# Compute insights
insights = compute_insights(df_filtered)

# --- Summary Metrics ---
st.subheader("📊 Key Sales Metrics")
colA, colB, colC, colD = st.columns(4)
colA.metric("Total Customers", len(df_filtered))
colB.metric("Avg Spend", f"${df_filtered['TotalSpend'].mean():.2f}")
colC.metric("Avg Recency (days)", f"{df_filtered['Recency'].mean():.1f}")
top_cluster = int(df_filtered['Cluster'].mode()[0])
colD.metric("Top Segment", f"Cluster {top_cluster}")

st.markdown("---")

# --- AI Reccomendations ---
st.header("💬 AI-Generated Sales Recommendations")

if st.button("Generate Recommendations"):
    with st.spinner("Analyzing segment and generating recommendations..."):
        rec = generate_sales_recommendation(df_filtered)
    st.write(rec)


# --- Product Preference ---
st.subheader("🍷 Product Category Spend Distribution")

prod_df = insights["product_pref"].reset_index().rename(
    columns={"index": "Product", "Total": "Spend"}
)

# Remove the "Mnt" prefix
prod_df["Product"] = prod_df["Product"].str.replace("Mnt", "", regex=True)

# Optional: make product names prettier
rename_map = {
    "Wines": "Wines",
    "Fruits": "Fruits",
    "MeatProducts": "Meat",
    "FishProducts": "Fish",
    "SweetProducts": "Sweet",
    "GoldProds": "Gold"
}
prod_df["Product"] = prod_df["Product"].map(rename_map)

fig_prod = px.bar(
    prod_df,
    x="Product",
    y="Spend",
    title="Total Spend by Product Category",
    text_auto=True
)

st.plotly_chart(fig_prod, use_container_width=True)

# --- Channel Usage ---
st.subheader("🛒 Sales Channel Performance")

channel_df = insights["channel_usage"].reset_index().rename(
    columns={"index": "Channel", "Avg": "Average"}
)

# Remove the "Num" prefix
channel_df["Channel"] = channel_df["Channel"].str.replace("Num", "", regex=True)

# Optional: rename channels for readability
channel_map = {
    "DealsPurchases": "Deals Purchases",
    "WebPurchases": "Web Purchases",
    "CatalogPurchases": "Catalog Purchases",
    "StorePurchases": "Store Purchases",
    "WebVisitsMonth": "Web Visits / Month",
}

channel_df["Channel"] = channel_df["Channel"].map(channel_map)

fig_channel = px.bar(
    channel_df,
    x="Channel",
    y="Average",
    title="Average Usage of Each Sales Channel",
    text_auto=True
)

st.plotly_chart(fig_channel, use_container_width=True)

# --- Spend by Age Group ---
st.subheader("👥 Spending by Age Group")
age_df = insights["spend_by_age"].reset_index().rename(columns={"index": "AgeGroup", "TotalSpend": "AvgSpend"})
fig_age = px.bar(age_df, x="AgeGroup", y="AvgSpend", title="Average Spend per Age Group", text_auto=True)
st.plotly_chart(fig_age, use_container_width=True)

# --- Cluster Summary ---
st.subheader("🔍 Customer Segment Summary (Clusters)")
st.dataframe(insights["cluster_summary"], use_container_width=True)
