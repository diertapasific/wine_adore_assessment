# 🍷 [Wine Customer Insight Dashboard](https://wineadoreassessment-diertapasific.streamlit.app/)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat\&logo=Streamlit\&logoColor=white) ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat\&logo=scikit-learn\&logoColor=white)

> An interactive analytics platform designed to help sales teams understand customer segments, visualize purchasing behavior, and generate actionable, AI-driven sales strategies.

---

## 🚀 Demo
### [Streamlit App](https://wineadoreassessment-diertapasific.streamlit.app/)

## 📸 Dashboard Preview

<img width="1919" height="992" alt="image" src="https://github.com/user-attachments/assets/d42d7fc5-3687-4ca4-b168-7acdb1861468" />

---

## 🛠️ Installation & Setup

Follow these steps to get the dashboard running locally.

### 1. Clone the Repository

```bash
git clone https://github.com/diertapasific/wine_adore_assessment
cd wine_adore_assessment
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Secrets

This project uses the HuggingFace API for AI recommendations.

* Create a file named `.streamlit/secrets.toml` in your project root.
* Add your key to the file:

```toml
HF_API_KEY = "your_actual_huggingface_key_here"
```

### 4. Launch the App

```bash
streamlit run app.py
```

---

## ✨ Key Features

### 🎯 Precision Segmentation

Leverages **K-Means Clustering** to group customers based on demographics and purchasing history. Move beyond basic averages and understand your distinct customer personas.

### 📊 Rich Visualizations

Gain immediate insights through interactive charts:

* **Product Spend:** Which product are driving revenue?
* **Channel Analysis:** Web vs. Store vs. Catalog performance.
* **Demographics:** Spending habits broken down by age groups.

### 🤖 AI Sales Strategist

Integrated with **HuggingFace LLMs** to turn raw data into narrative advice.

* *Input:* Cluster statistics.
* *Output:* "Focus on promoting premium wines and offer exclusive offerings to customers with higher average incomes (>$50,000) to increase average total spend."

---

## 🧠 Approach & Methodology

For a data science assessment, it’s important to explain **why** each step was taken. This section outlines the rationale behind the dashboard's design.

1. **Data Preprocessing:**

   * Handled missing values in `Income` using median imputation.
   * Created `Customer_Age` and `Total_Spend` features to simplify dimensionality.
   * Removed outliers based on age (>100) and income caps to ensure cluster stability.

2. **Feature Encoding & Engineering:**

   * Converted categorical variables (Education, Marital Status) into numerical representations for clustering.
   * Ensured all features were normalized for distance-based algorithms.

3. **Clustering:**

   * Utilized **K-Means Clustering**.
   * Determined the optimal number of clusters ($k=4$) using the **Elbow Method** and **Silhouette Score** analysis.

4. **Visualization & Insight Generation:**

   * Interactive charts built in Streamlit allow sales teams to explore trends dynamically.
   * AI-driven narratives translate cluster statistics into actionable recommendations for marketing and sales strategies.

---

## 📂 Data & Processing
The project uses the **Customer Personality Analysis** dataset from Kaggle, providing demographics, purchasing history, and marketing response details.

* **Dataset Link:** [Kaggle: Customer Personality Analysis](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis)
* **Key Attributes:**

  * **User Profile:** Year of birth, Education, Marital Status, Income.
  * **Product Metrics:** Amount spent on Wine, Fruits, Meat, Fish, Sweets, and Gold.
  * **Interaction:** Number of web, store, and catalog purchases.

---

## 🗂️ Project Structure

```text
├── data/                  # Raw and processed datasets
├── models/                # Trained K-Means clustering model
├── src/
│   ├── preprocessing.py   # Data cleaning and feature engineering
│   ├── model.py           # K-Means clustering logic
│   ├── insights.py        # Functions for computing dashboards insights
│   ├── date_filter.py     # Functions to filter data by date
│   └── recommender.py     # HuggingFace LLM integration
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.txt             # Project documentation
```
