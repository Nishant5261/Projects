import streamlit as st
import requests

st.set_page_config(page_title="CLV Forecaster", layout="centered")
st.title("📈 CLV Forecaster Dashboard")
st.write("Enter the customer's behavioral metrics to predict their 12-month future revenue.")

API_URL = "http://backend:8000/predict_clv"

with st.form("clv_form"):
    st.subheader("Temporal Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        recency = st.number_input("Recency (Days)", min_value=0, value=15)
    with col2:
        model_recency = st.number_input("Model Recency", min_value=0, value=100)
    with col3:
        tenure = st.number_input("Customer Tenure", min_value=0, value=115)
        
    st.subheader("Monetary Features")
    col4, col5, col6 = st.columns(3)
    with col4:
        frequency = st.number_input("Repeat Frequency", min_value=0, value=5)
    with col5:
        monetary = st.number_input("Total Monetary ($)", min_value=0.0, value=500.0)
    with col6:
        avg_order = st.number_input("Avg Order Value ($)", min_value=0.0, value=100.0)
        
    submit = st.form_submit_button("Generate Forecast")

if submit:
    payload = {
        "recency": recency, "model_recency": model_recency, "customer_tenure": tenure,
        "frequency": frequency, "monetary": monetary, "avg_order_value": avg_order
    }
    
    try:
        with st.spinner("Querying API..."):
            res = requests.post(API_URL, json=payload)
            if res.status_code == 200:
                st.success("API Prediction Successful!")
                st.metric(label="Predicted Future Revenue", value=f"${res.json()['data']['predicted_usd']:,.2f}")
            else:
                st.error(f"API Error: {res.text}")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend API.")