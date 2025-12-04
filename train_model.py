import pandas as pd
from src.preprocessing import preprocess
from src.model import CustomerModel

print("Loading data...")
df = pd.read_csv("data/customers.csv", sep="\t")

print("Preprocessing...")
df = preprocess(df)

print("Training model...")
model = CustomerModel(n_clusters=4)
df = model.fit(df)

print("Saving model...")
model.save()

df.to_csv("data/processed.csv", index=False)

print("Done.")
