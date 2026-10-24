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
    # A. Format the input as a raw 2D NumPy array to bypass Scikit-Learn's strict name checking
    # This prevents the silent crashes caused by Pandas column name mismatches
    input_data = np.array([[recency, frequency, monetary]])
    
    # B. Apply Preprocessing (Log Transform -> Scale)
    input_log = np.log1p(input_data)
    input_scaled = scaler.transform(input_log)
    
    # C. Generate Prediction
    cluster_id = kmeans_model.predict(input_scaled)[0]
    
    # D. DYNAMIC CLUSTER MAPPING
    # Inspect the trained model's mathematical centroids to find which ID represents which tier.
    # Feature index 2 is 'Monetary'. We sort the clusters by their average spend.
    centers = kmeans_model.cluster_centers_
    sorted_indices = np.argsort(centers[:, 2]) 
    
    segment_mapping = {
        sorted_indices[0]: 'Bronze (Lost/Low)',
        sorted_indices[1]: 'Silver (At Risk)',
        sorted_indices[2]: 'Gold (Loyal)',
        sorted_indices[3]: 'Platinum (Champions)'
    }
    
    predicted_segment = segment_mapping[cluster_id]
    
    # E. Define the Business Strategy Dictionary
    strategy_guide = {
        'Platinum (Champions)': {
            'icon': '💎',
            'advice': "**Marketing Strategy:** Do not offer discounts (they buy anyway). Offer early access to new products, VIP support, and loyalty rewards."
        },
        'Gold (Loyal)': {
            'icon': '🥇',
            'advice': "**Marketing Strategy:** Upsell higher-margin items. Encourage referrals with 'Bring a Friend' campaigns to leverage their loyalty."
        },
        'Silver (At Risk)': {
            'icon': '🥈',
            'advice': "**Marketing Strategy:** Send targeted 'Win-Back' discount codes. Send personalized emails asking for feedback to prevent churn."
        },
        'Bronze (Lost/Low)': {
            'icon': '🥉',
            'advice': "**Marketing Strategy:** Deprioritize marketing spend here. Only target during major clearance sales to clear out dead inventory."
        }
    }
    
    # F. Display Results
    st.divider()
    
    segment_info = strategy_guide[predicted_segment]
    
    st.markdown(f"### {segment_info['icon']} Predicted Segment: **{predicted_segment}**")
    
    # Display the targeted advice in a colored alert box
    if "Platinum" in predicted_segment:
        st.info(segment_info['advice'])
    elif "Gold" in predicted_segment:
        st.success(segment_info['advice'])
    elif "Silver" in predicted_segment:
        st.warning(segment_info['advice'])
    else:
        st.error(segment_info['advice'])
