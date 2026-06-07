# 🛡️ AI Fraud Risk Analyzer

### Smart Transaction Risk Detection using Machine Learning

An end-to-end AI-powered financial risk assessment system that analyzes transaction details and predicts the likelihood of fraudulent activity in real time.

Unlike traditional rule-based systems, this application uses a trained XGBoost machine learning model to evaluate transaction behavior and generate intelligent risk predictions.

---

## 🚀 Project Overview

Financial fraud continues to be one of the largest challenges in digital banking and online transactions.

This project simulates a real-world fraud analysis environment where users can:

- Create an account
- Simulate financial transactions
- Analyze transaction risk instantly
- View fraud probability scores
- Track transaction history
- Investigate historical transactions

The goal is not simply to classify fraud, but to demonstrate how machine learning can support financial risk assessment and decision-making.

---

## ✨ Key Features

### 🔐 Account Simulation
Users create a virtual account with a custom balance before performing transactions.

### 💳 Intelligent Transaction Analysis
Supports:

- Send Money
- Make Payment
- Withdraw Money

with real-time fraud evaluation.

### ⏰ Real-Time & Historical Analysis

Analyze:

- Current transactions
- Past transactions using custom date and time selection

This reflects real-world fraud investigation workflows.

### 🤖 AI-Powered Prediction Engine

Powered by:

- XGBoost Classifier
- Probability-Based Risk Scoring

Instead of hardcoded fraud rules.

### 📊 Risk Assessment

Generates:

- Fraud Prediction
- Risk Score
- Transaction Insights

### 📝 Transaction History

Stores and displays previous transaction analyses in an interactive dashboard.

### 🌙 Midnight Activity Detection

Additional warning mechanism for transactions occurring during high-risk hours.

---

## 🏗️ System Architecture


User Input
     ↓
Feature Engineering
     ↓
Validation Layer
     ↓
XGBoost Model
     ↓
Risk Prediction
     ↓
Risk Assessment
     ↓
Transaction History
🧠 Machine Learning Model
Algorithm

XGBoost Classifier

Dataset

PaySim Fraud Detection Dataset

Features Used
[
'step',
'amount',
'oldbalanceOrg',
'newbalanceOrig',
'oldbalanceDest',
'newbalanceDest',
'type_CASH_OUT',
'type_DEBIT',
'type_PAYMENT',
'type_TRANSFER'
]
Prediction Outputs
Legitimate Transaction
Fraudulent Transaction
Risk Score

Calculated using:

model.predict_proba()

to provide probability-based risk analysis.

🛠️ Technology Stack
Frontend
Streamlit
Machine Learning
XGBoost
Scikit-Learn
Data Processing
Pandas
NumPy
Model Serialization
Joblib
Development
Python
📂 Project Structure
AI-Fraud-Risk-Analyzer
│
├── app/
│   └── app.py
│
├── models/
│   └── fraud_model.pkl
│
├── notebooks/
│   └── 01_data_inspection.ipynb
│
├── requirements.txt
│
└── README.md
🎯 Why This Project Matters

Most beginner fraud detection projects stop at model training.

This project extends beyond model development by integrating:

Machine Learning
Risk Analytics
Interactive Dashboard Development
User Experience Design
Real-Time Prediction
Financial Decision Support

making it a complete end-to-end AI application.

🔮 Future Enhancements
Explainable AI using SHAP
Advanced Fraud Investigation Dashboard
Model Performance Analytics
Cloud Deployment
Multi-user Authentication
Fraud Trend Visualization
👩‍💻 Author

Gopika Ajith

B.Tech Artificial Intelligence & Data Science

Aspiring Data Scientist | Machine Learning Enthusiast | AI Developer

LinkedIn: (Add your LinkedIn URL)

GitHub: (Add your GitHub URL)

⭐ Project Status

Current Version: v1.0

Core Machine Learning System Completed ✅

Actively Improving User Experience, Explainability, and Deployment Features.
