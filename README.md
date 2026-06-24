# RetailPulse: End-to-End Retail Analytics & Forecasting Platform

RetailPulse is a modular, predictive analytics platform designed to turn historical transaction logs into actionable business insights. The platform integrates customer value analytics, recommendation engines, time-series forecasting, and inventory optimization under a single, unified Streamlit dashboard.

---

## 🚀 Key Modules & Real-World Results

Here is a summary of the predictions and statistical models deployed in this project:

### 1. Customer Segmentation
* **Approach:** RFM (Recency, Frequency, Monetary) feature extraction followed by **K-Means Clustering** and **PCA dimensionality reduction** (with DBSCAN comparison).
* **Metrics:** Achieved a **Silhouette Score of 0.42** for K-Means.
* **Outcome:** Grouped customers into 4 distinct business segments (VIP, Loyal, Churn Risk, Low-Value) to allow targeted marketing campaigns.

### 2. Customer Churn Prediction
* **Approach:** Ensembled classifier combining **XGBoost, Random Forest, and CatBoost** to identify clients with no activity in 90 days.
* **Metrics:** **72.35% F1-score** and **89.31% ROC-AUC** on the validation set.
* **Outcome:** Enables proactively flagging at-risk customers directly in the UI.

### 3. Customer Lifetime Value (CLV)
* **Approach:** Built an **XGBoost Regressor** to predict the future monetary value of customers.
* **Metrics:** Achieved an **R² score of 98.52%** and a Mean Absolute Error (MAE) of **0.104**.
* **Outcome:** Provides regression forecasts of future revenue and maps customers into value tiers (Low, Medium, High, Very High Value).

### 4. Demand Forecasting
* **Approach:** Built an ensemble of **XGBoost, Prophet, and PyTorch LSTM** models to project future sales volumes.
* **Metrics:** The ensemble model achieved a **19.97% SMAPE** (Symmetric Mean Absolute Percentage Error).
* **Outcome:** Provides reliable future inventory demand predictions.

### 5. Market Basket Analysis (Recommendations)
* **Approach:** Association rule mining using the **Apriori Algorithm** to find product affinities.
* **Metrics:** Discovered strong rules with a maximum Lift score of **17.84**.
* **Outcome:** Recommends cross-sell items based on historical shopping cart behavior.

### 6. Inventory Optimization
* **Approach:** Runs **ABC Inventory Analysis** (prioritizing items based on value contribution) and calculates **Economic Order Quantity (EOQ)**, **Safety Stock**, and **Reorder Points**.
* **Outcome:** Automatically flags low-stock warnings and critical inventory items.

---

## 🛠️ Installation & Setup

Follow these steps to run the dashboard application locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/devparmar16/retail_pulse.git
cd retail_pulse
```

### 2. Configure Your Virtual Environment
If you are setting up a fresh environment, run:
```bash
# Windows
python -m venv zidio_env
.\zidio_env\Scripts\activate

# Mac/Linux
python3 -m venv zidio_env
source zidio_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard
Launch the application from the root directory:
```bash
streamlit run dashboard/streamlit_app.py
```

---

## 📂 Project Structure

```
├── dashboard/               # Streamlit application
│   ├── streamlit_app.py     # Main landing page & KPI scorecard
│   ├── pages/               # Individual analytical pages (1 to 7)
│   └── utils/               # Data loaders and path resolution helpers
├── dataset/                 # Raw datasets (PDF documentation, sales data)
├── notebooks/               # Jupyter Notebook development pipeline
│   ├── data/processed/      # Generated metrics & clean CSV tables
│   ├── eda/                 # Exploratory Data Analysis notebooks
│   ├── feature_engineer/    # Feature extraction notebooks
│   ├── model/               # Model training and optimization notebooks
│   └── models/              # Serialized model checkpoints (.pkl files)
├── requirements.txt         # Core dependencies for the dashboard
└── README.md                # Project documentation
```

---

## 📈 Experiment Tracking with MLflow

All modeling runs, parameters, and evaluation metrics are logged locally using **MLflow** into `mlflow.db`. 

To launch the MLflow tracking dashboard and compare hyperparameter tuning results:
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
Open [http://localhost:5000](http://localhost:5000) in your browser to inspect model runs.
