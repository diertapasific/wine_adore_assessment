import requests
import pandas as pd
import json
import numpy as np
import streamlit as st


HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_API_KEY = st.secrets["HF_API_KEY"]

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def safe_mean(series):
    return float(series.mean()) if not series.empty else 0.0

def safe_mode(series):
    return int(series.mode()[0]) if not series.empty else -1

def generate_sales_recommendation(df: pd.DataFrame) -> str:
    """
    Send summary of FILTERED dataset to LLM and get recommendations.
    """

    # --- Product clean names ---
    product_map = {
        "MntWines": "Wines",
        "MntFruits": "Fruits",
        "MntMeatProducts": "Meat Products",
        "MntFishProducts": "Fish Products",
        "MntSweetProducts": "Sweet Products",
        "MntGoldProds": "Gold Products"
    }

    # --- Channel clean names ---
    channel_map = {
        "NumWebPurchases": "Web Purchases",
        "NumCatalogPurchases": "Catalog Purchases",
        "NumStorePurchases": "Store Purchases"
    }

    # ---- SAFE SUMMARY ----
    summary = {
        "customer_count": len(df),
        "avg_income": safe_mean(df["Income"]),
        "avg_recency": safe_mean(df["Recency"]),
        "avg_total_spend": safe_mean(df["TotalSpend"]),
    }

    # ---- TOP PRODUCT ----
    if len(df) > 0:
        top_product_col = df[[
            "MntWines","MntFruits","MntMeatProducts",
            "MntFishProducts","MntSweetProducts","MntGoldProds"
        ]].sum().idxmax()
        summary["top_product"] = product_map.get(top_product_col, top_product_col)
    else:
        summary["top_product"] = "None"

    # ---- TOP CHANNEL ----
    if len(df) > 0:
        top_channel_col = df[[
            "NumWebPurchases","NumCatalogPurchases","NumStorePurchases"
        ]].mean().idxmax()
        summary["top_channel"] = channel_map.get(top_channel_col, top_channel_col)
    else:
        summary["top_channel"] = "None"

    summary["top_cluster"] = safe_mode(df["Cluster"])

    # ---- PROMPT ----
    prompt = f"""
You are a Sales Strategy Assistant for a wine retail company.

Based on the following *filtered customer segment data summary* (these values come from the selected range on the dashboard):

- Total Customers in This Segment: {summary['customer_count']}
- Average Income: {summary['avg_income']:.2f}
- Average Recency (days since last purchase): {summary['avg_recency']:.2f}
- Average Total Spend: {summary['avg_total_spend']:.2f}
- Top Purchased Product Category: {summary['top_product']}
- Most Used Sales Channel: {summary['top_channel']}
- Dominant Customer Cluster: {summary['top_cluster']}

Generate **5 short, actionable, data-driven sales recommendations**.  
Format as bullet points. Keep it concise and clear.
"""

    # ---- LLM CALL ----
    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful data-driven sales advisor."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    response = requests.post(HF_API_URL, headers=headers, json=payload)

    # ---- PARSE RESPONSE ----
    try:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception:
        print("Error:", response.text)
        return "⚠️ LLM Error: Could not generate recommendation."
