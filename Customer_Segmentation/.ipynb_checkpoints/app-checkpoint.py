import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# --- 1. Page Configuration & Setup ---
st.set_page_config(page_title="Customer Segmentation App", page_icon="🎯", layout="centered")
st.title("🎯 E-Commerce Customer Segmentation")
st.write("Enter a customer's RFM metrics below to instantly predict their loyalty segment and generate a targeted marketing strategy.")

# --- 2. Load Pre-trained Assets ---
@st.cache_resource
def load_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Ensure these files are saved in the same directory as app.py
    scaler = joblib.load(os.path.join(base_dir, 'rfm_scaler.pkl'))
    kmeans_model = joblib.load(os.path.join(base_dir, 'kmeans_model.pkl'))
    return scaler, kmeans_model

try:
    scaler, kmeans_model = load_models()
except FileNotFoundError:
    st.error("⚠️ Model files not found. Please ensure 'rfm_scaler.pkl' and 'kmeans_model.pkl' are in the directory.")
    st.stop()

# --- 3. User Input Form ---
with st.form("customer_input_form"):
    st.subheader("Customer RFM Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        recency = st.number_input(
            "Recency (Days)", 
            min_value=0, 
            value=12, 
            help="Days since the customer's last purchase."
        )
        
    with col2:
        frequency = st.number_input(
            "Frequency (Orders)", 
            min_value=1, 
            value=4, 
            help="Total number of unique orders/invoices."
        )
        
    with col3:
        monetary = st.number_input(
            "Monetary ($)", 
            min_value=0.01, 
            value=250.00, 
            help="Total amount of money spent by the customer."
        )
        
    submit_button = st.form_submit_button(label="Predict Customer Segment")

# --- 4. Prediction & Strategy Logic ---
if submit_button:
    # A. Format the input to match the training data exactly
    input_data = pd.DataFrame({
        'Recency': [recency],
        'Frequency': [frequency],
        'Monetary': [monetary]
    })
    
    # B. Apply Preprocessing (Log Transform -> Scale)
    input_log = np.log1p(input_data)
    input_scaled = scaler.transform(input_log)
    
    # C. Generate Prediction
    cluster_id = kmeans_model.predict(input_scaled)[0]
    
    # Note: K-Means cluster IDs (0, 1, 2, 3) are assigned randomly during training. 
    # If your specific notebook run mapped them differently based on the monetary mean, 
    # update this dictionary to match your exact output.
    segment_mapping = {
        0: 'Bronze (Lost/Low)',
        1: 'Silver (At Risk)',
        2: 'Gold (Loyal)',
        3: 'Platinum (Champions)'
    }
    
    predicted_segment = segment_mapping.get(cluster_id, "Unknown Segment")
    
    # D. Define the Business Strategy Dictionary
    strategy_guide = {
        'Platinum (Champions)': {
            'color': 'blue',
            'icon': '💎',
            'advice': "**Marketing Strategy:** Do not offer discounts (they buy anyway). Offer early access to new products, VIP support, and loyalty rewards."
        },
        'Gold (Loyal)': {
            'color': 'green',
            'icon': '🥇',
            'advice': "**Marketing Strategy:** Upsell higher-margin items. Encourage referrals with 'Bring a Friend' campaigns to leverage their loyalty."
        },
        'Silver (At Risk)': {
            'color': 'orange',
            'icon': '🥈',
            'advice': "**Marketing Strategy:** Send targeted 'Win-Back' discount codes. Send personalized emails asking for feedback to prevent