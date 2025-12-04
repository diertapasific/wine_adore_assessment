import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

class CustomerModel:

    def __init__(self, n_clusters=4):
        self.n_clusters = n_clusters
        self.scaler = None
        self.kmeans = None

    def fit(self, df):
        features = df[["Age", "Income", "TotalSpend", "Recency", "Frequency"]]

        self.scaler = StandardScaler()
        scaled = self.scaler.fit_transform(features)

        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        df["Cluster"] = self.kmeans.fit_predict(scaled)

        return df

    def predict(self, df):
        features = df[["Age", "Income", "TotalSpend", "Recency", "Frequency"]]
        scaled = self.scaler.transform(features)
        df["Cluster"] = self.kmeans.predict(scaled)
        return df

    def save(self):
        with open("models/scaler.pkl", "wb") as f:
            pickle.dump(self.scaler, f)
        with open("models/kmeans.pkl", "wb") as f:
            pickle.dump(self.kmeans, f)

    def load(self):
        with open("models/scaler.pkl", "rb") as f:
            self.scaler = pickle.load(f)
        with open("models/kmeans.pkl", "rb") as f:
            self.kmeans = pickle.load(f)
