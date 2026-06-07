import streamlit as st
from datetime import datetime
import joblib
import pandas as pd

if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []

st.set_page_config(
    page_title="AI Fraud Risk Analyzer",
    page_icon="🛡️",
    layout="wide"
)

# LOAD MODEL
model = joblib.load("models/fraud_model.pkl")

# SESSION STATE
if "page" not in st.session_state:
    st.session_state.page = "home"

# HOME PAGE
if st.session_state.page == "home":
    st.markdown(
        """
        <div style='text-align: center; padding-top: 100px;'>
            <h1 style='font-size: 70px;'>🛡️</h1>
            <h1 style='color: white;'>AI Fraud Risk Analyzer</h1>
            <h3 style='color: gray;'>Smart Transaction Risk Detection</h3>
            <p style='color: gray;'>Secure • Intelligent • Real-Time</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Get Started"):
        st.session_state.page = "details"
        st.rerun()

# DETAILS PAGE
elif st.session_state.page == "details":
    st.title("Account Setup")
    st.caption("Set up your account to begin secure transaction analysis.")

    user_name = st.text_input("Enter Your Name").strip()
    current_balance = st.text_input("Enter Current Balance").strip()

    if st.button("Continue"):
        if not user_name:
            st.error("Please enter your name.")
        elif not current_balance:
            st.error("Please enter your balance.")
        else:
            try:
                st.session_state.user_name = user_name
                st.session_state.current_balance = float(current_balance)
                st.session_state.page = "transaction"
                st.rerun()
            except ValueError:
                st.error("Please enter numbers only for balance.")

# TRANSACTION PAGE
elif st.session_state.page == "transaction":

    # CURRENT TIME
    now = datetime.now()
    current_hour = now.hour
    current_time = now.strftime("%I:%M %p")

    # GREETING
    if current_hour < 12:
        greeting = "Good Morning ☀️"
    elif current_hour < 17:
        greeting = "Good Afternoon 🌤️"
    else:
        greeting = "Good Evening 🌙"

    # HEADER
    col1, col2 = st.columns([5, 1])

    with col1:
        st.title(f"{greeting}, {st.session_state.user_name} 👋")
        st.write(f"🕒 Current Time: {current_time}")

    with col2:
        st.write("")
        st.write("")
        if st.button("Reset Account"):
            st.session_state.clear()
            st.rerun()
        
    st.divider()

    # TRANSACTION TYPE
    transaction_options = {
        "Send Money": "TRANSFER",
        "Make Payment": "PAYMENT",
        "Withdraw Money": "CASH_OUT"
    }

    selected_action = st.selectbox(
        "Transaction Type",
        list(transaction_options.keys())
    )

    transaction_type = transaction_options[selected_action]

    # TIME MODE
    time_mode = st.radio(
        "Transaction Time Mode",
        ["Real-Time Transaction", "Custom Transaction Analysis"]
    )

    if time_mode == "Real-Time Transaction":
        transaction_hour = current_hour
        st.info(f"Using live transaction time: {current_time}")

    else:
        custom_date = st.date_input("Select Transaction Date")
        custom_time = st.time_input("Select Transaction Time")
        transaction_hour = custom_time.hour

    # INPUTS
    transaction_amount = st.text_input("Transaction Amount")

    if selected_action != "Withdraw Money":
        recipient_name = st.text_input("Recipient Name")
        recipient_balance_before = st.text_input("Recipient Balance Before")
    else:
        recipient_name = ""
        recipient_balance_before = "0"

    # LIVE BALANCE PREVIEW
    sender_after = None

    if transaction_amount:
        try:
            amount_preview = float(transaction_amount)
            sender_before = st.session_state.current_balance
            sender_after = sender_before - amount_preview

            st.info(f"Sender Balance Before: ₹{sender_before:,.0f}")
            st.info(f"Sender Balance After: ₹{sender_after:,.0f}")

            if sender_after < 0:
                st.warning("⚠️ Warning: Transaction amount exceeds available balance.")

        except ValueError:
            st.warning("Please enter a valid numeric transaction amount.")

    # FRAUD CHECK
    if st.button("Check Fraud Risk"):
        try:
            amount = float(transaction_amount)

            oldbalanceOrg = st.session_state.current_balance
            newbalanceOrig = oldbalanceOrg - amount

            # INVALID TRANSACTION
            if newbalanceOrig < 0:
                st.error("❌ Invalid Transaction")
                st.markdown("### Risk Reasons:")
                st.warning("⚠️ Transaction exceeds available balance")

            else:
                oldbalanceDest = float(recipient_balance_before)

                if selected_action != "Withdraw Money":
                    newbalanceDest = oldbalanceDest + amount
                else:
                    newbalanceDest = 0

                input_data = pd.DataFrame([{
                    "step": transaction_hour,
                    "amount": amount,
                    "oldbalanceOrg": oldbalanceOrg,
                    "newbalanceOrig": newbalanceOrig,
                    "oldbalanceDest": oldbalanceDest,
                    "newbalanceDest": newbalanceDest,
                    "type_CASH_OUT": 1 if transaction_type == "CASH_OUT" else 0,
                    "type_DEBIT": 0,
                    "type_PAYMENT": 1 if transaction_type == "PAYMENT" else 0,
                    "type_TRANSFER": 1 if transaction_type == "TRANSFER" else 0
                }])
                prediction = model.predict(input_data)[0]
                risk_score = model.predict_proba(input_data)[0][1] * 100
                history_entry = {
                    "Date": datetime.now().strftime("%Y-%m-%d"),
                    "Type": transaction_type,
                    "Amount": amount,
                    "Recipient": recipient_name,
                    "Risk Score": f"{risk_score:.2f}%",
                    "Result": "Fraud" if prediction == 1 else "Legitimate"
                }

                st.session_state.transaction_history.append(history_entry)

                if prediction == 1:
                    st.error("🚨 Suspicious / Fraudulent Transaction Detected!")
                    st.write(f"## Risk Score: {risk_score:.2f}%")
                    st.markdown("## Risk Reasons:")

                    st.warning("⚠️ AI model detected suspicious transaction pattern")
                    st.warning("⚠️ Unusual transaction behavior")

                    if 0 <= transaction_hour <= 5:
                        st.warning("⚠️ Midnight anomaly detected")

                else:
                    st.markdown(f"""
<div style="
padding:20px;
border-radius:15px;
background-color:#0f5132;
border:2px solid #198754;
margin-top:15px;
">
<h2>✅ Legitimate Transaction</h2>
<h3>Risk Score: {risk_score:.2f}%</h3>
<p>AI model indicates low fraud risk.</p>
</div>
""", unsafe_allow_html=True)
            
        except ValueError:
            st.error("Please enter valid numeric values.")
            
    # TRANSACTION HISTORY
    st.divider()
    st.subheader("Transaction History")
    if st.session_state.transaction_history:
        history_df = pd.DataFrame(st.session_state.transaction_history)

        history_df.index = history_df.index + 1
        history_df = history_df[::-1]
        st.dataframe(history_df, use_container_width=True)
else:
    st.info("No transactions yet.")
