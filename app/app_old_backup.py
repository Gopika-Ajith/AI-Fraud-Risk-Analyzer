import streamlit as st
import joblib

st.set_page_config(page_title="AI Fraud Risk Analyzer", layout="wide")

model = joblib.load("models/fraud_model.pkl")

if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

st.title("💳 AI Fraud Risk Analyzer")
st.write("Detect potentially fraudulent financial transactions using AI.")

st.header("Transaction Details")

amount = st.text_input(
    "Transaction Amount",
    key=f"amount_{st.session_state.reset_counter}"
)

oldbalanceOrg = st.text_input(
    "Sender Old Balance",
    key=f"oldbalanceOrg_{st.session_state.reset_counter}"
)

newbalanceOrig = st.text_input(
    "Sender New Balance",
    key=f"newbalanceOrig_{st.session_state.reset_counter}"
)

oldbalanceDest = st.text_input(
    "Receiver Old Balance",
    key=f"oldbalanceDest_{st.session_state.reset_counter}"
)

newbalanceDest = st.text_input(
    "Receiver New Balance",
    key=f"newbalanceDest_{st.session_state.reset_counter}"
)

transaction_type = st.selectbox(
    "Transaction Type",
    ["CASH_OUT", "PAYMENT", "CASH_IN", "TRANSFER", "DEBIT"],
    key=f"type_{st.session_state.reset_counter}"
)

col1, col2 = st.columns(2)

with col1:
    check = st.button("Check Fraud Risk")

with col2:
    reset = st.button("🔄 New Check")

if reset:
    st.session_state.reset_counter += 1
    st.rerun()

if check:
    try:
        amount = float(amount)
        oldbalanceOrg = float(oldbalanceOrg)
        newbalanceOrig = float(newbalanceOrig)
        oldbalanceDest = float(oldbalanceDest)
        newbalanceDest = float(newbalanceDest)

        type_cash_out = 1 if transaction_type == "CASH_OUT" else 0
        type_debit = 1 if transaction_type == "DEBIT" else 0
        type_payment = 1 if transaction_type == "PAYMENT" else 0
        type_transfer = 1 if transaction_type == "TRANSFER" else 0

        input_data = [[
            1,
            amount,
            oldbalanceOrg,
            newbalanceOrig,
            oldbalanceDest,
            newbalanceDest,
            type_cash_out,
            type_debit,
            type_payment,
            type_transfer
        ]]

        prediction = model.predict(input_data)[0]

        suspicious_rules = []

        if amount > oldbalanceOrg and transaction_type != "CASH_IN":
            suspicious_rules.append("Transaction amount exceeds sender balance")

        if newbalanceOrig > oldbalanceOrg and transaction_type != "CASH_IN":
            suspicious_rules.append("Impossible sender balance increase detected")

        if transaction_type == "DEBIT" and amount > 100000:
            suspicious_rules.append("Unusually high DEBIT transaction")

        if transaction_type == "TRANSFER" and amount > 500000:
            suspicious_rules.append("High-value transfer detected")

        if prediction == 1 or suspicious_rules:
            st.error("🚨 Suspicious / Fraudulent Transaction Detected!")

            if suspicious_rules:
                st.subheader("Risk Reasons:")
                for rule in suspicious_rules:
                    st.write(f"⚠️ {rule}")

        else:
            st.success("✅ Legitimate Transaction")

    except ValueError:
        st.warning("Please enter valid numbers in all fields.")