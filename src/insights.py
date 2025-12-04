import pandas as pd

def compute_insights(df):
    if df.empty:
        return {
            "product_pref": pd.DataFrame(),
            "channel_usage": pd.DataFrame(),
            "spend_by_age": pd.DataFrame(),
            "cluster_summary": pd.DataFrame()
        }

    # Product preference summary
    product_cols = [
        "MntWines", "MntFruits", "MntMeatProducts",
        "MntFishProducts", "MntSweetProducts", "MntGoldProds"
    ]
    product_pref = df[product_cols].sum().sort_values(ascending=False)
    product_pref = pd.DataFrame(product_pref, columns=["Total"])

    # Channel usage
    channel_cols = [
        "NumWebPurchases",
        "NumCatalogPurchases",
        "NumStorePurchases",
        "NumWebVisitsMonth"
    ]
    channel_usage = df[channel_cols].mean().sort_values(ascending=False)
    channel_usage = pd.DataFrame(channel_usage, columns=["Avg"])

    # Spend by age group
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[18, 30, 40, 50, 60, 99],
        labels=["18-30", "30-40", "40-50", "50-60", "60+"]
    )
    spend_by_age = df.groupby("AgeGroup")["TotalSpend"].mean()

    # Cluster summary
    cluster_summary = df.groupby("Cluster").agg({
        "Age": "mean",
        "Income": "mean",
        "TotalSpend": "mean",
        "Recency": "mean",
        "Frequency": "mean"
    }).round(2)

    return {
        "product_pref": product_pref,
        "channel_usage": channel_usage,
        "spend_by_age": spend_by_age,
        "cluster_summary": cluster_summary
    }
