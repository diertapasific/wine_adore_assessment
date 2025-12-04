import pandas as pd

def filter_by_date(df, start_year, start_month, end_year, end_month):
    start = pd.Timestamp(year=start_year, month=start_month, day=1)
    end = pd.Timestamp(year=end_year, month=end_month, day=28)

    mask = (df["Dt_Customer"] >= start) & (df["Dt_Customer"] <= end)
    return df[mask]
