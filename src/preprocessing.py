import pandas as pd

def preprocess(df):
    # Fix column names with strange separators
    df.columns = [c.strip().replace("\t", "") for c in df.columns]

    # Convert date
    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], errors="coerce")

    # Age
    df["Age"] = 2025 - df["Year_Birth"]

    # Total spend
    df["TotalSpend"] = (
        df["MntWines"] +
        df["MntFruits"] +
        df["MntMeatProducts"] +
        df["MntFishProducts"] +
        df["MntSweetProducts"] +
        df["MntGoldProds"]
    )

    # Frequency = total purchases
    df["Frequency"] = (
        df["NumWebPurchases"] +
        df["NumCatalogPurchases"] +
        df["NumStorePurchases"]
    )

    # Total accepted campaign
    df["TotalAccepted"] = (
        df["AcceptedCmp1"] +
        df["AcceptedCmp2"] +
        df["AcceptedCmp3"] +
        df["AcceptedCmp4"] +
        df["AcceptedCmp5"]
    )

    # Fix income missing
    df["Income"] = df["Income"].fillna(df["Income"].median())

    # Remove rows without date
    df = df.dropna(subset=["Dt_Customer"])

    # Fill remaining missing fields
    df = df.fillna(0)

    return df
