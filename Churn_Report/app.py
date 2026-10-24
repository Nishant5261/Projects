import streamlit as st
import pandas as pd
import joblib
import os

# 1. Load the saved models and scalers efficiently
@st.cache_resource
def load_assets():
    # Find the exact folder where app.py is currently located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Attach that folder path to the filenames
    model = joblib.load(os.path.join(base_dir, 'xgboost_churn_model.pkl'))
    scaler = joblib.load(os.path.join(base_dir, 'scaler.pkl'))
    expected_cols = joblib.load(os.path.join(base_dir, 'feature_columns.pkl'))
    
    return model, scaler, expected_cols

model, scaler, expected_cols = load_assets()

# ... (keep the rest of your UI code exactly the same) ...

model, scaler, expected_cols = load_assets()

# 2. Set up the Streamlit UI
st.set_page_config(page_title="Customer Churn Predictor", layout="centered")
st.title("🛒 E-Commerce Customer Churn Predictor")
st.write("Enter customer details below to predict their likelihood of churning.")

# 3. Create the input form
with st.form("prediction_form"):
    st.subheader("Customer Behavior & Metrics")
    
    col1, col2 = st.columns(2)
    with col1:
        tenure = st.number_input("Tenure (Months)", min_value=0, max_value=100, value=5)
        complain = st.selectbox("Logged a Complaint?", ["No", "Yes"])
        cashback = st.number_input("Average Cashback Amount ($)", min_value=0.0, max_value=500.0, value=150.0)
        warehouse_dist = st.number_input("Distance from Warehouse", min_value=1, max_value=100, value=15)
    
    with col2:
        order_cat = st.selectbox("Preferred Order Category", ['Laptop & Accessory', 'Mobile Phone', 'Fashion', 'Grocery', 'Others'])
        app_hours = st.number_input("Hours Spent on App", min_value=0, max_value=24, value=3)
        order_count = st.number_input("Total Order Count", min_value=1, max_value=50, value=4)
        satisfaction = st.slider("Satisfaction Score", 1, 5, 3)

    submit_button = st.form_submit_button("Predict Churn Risk")

# 4. Process the Input and Predict
if submit_button:
    # Map text input to binary
    complain_val = 1 if complain == "Yes" else 0
    
    # Reconstruct the expected dataset structure (filling unasked features with EDA medians)
    input_data = {
        'Tenure': tenure,
        'WarehouseToHome': warehouse_dist,
        'HourSpendOnApp': app_hours,
        'OrderAmountHikeFromlastYear': 15, 
        'DaySinceLastOrder': 3,            
        'CouponUsed': 1,                   
        'OrderCount': order_count,
        'Complain': complain_val,
        'CashbackAmount': cashback,
        'SatisfactionScore': satisfaction,
        'PreferedOrderCat': order_cat,
        'PreferredLoginDevice': 'Mobile',  
        'PreferredPaymentMode': 'Credit Card', 
        'MaritalStatus': 'Married',        
        'CityTier': 1,                     
        'Gender': 'Male',                  
        'NumberOfAddress': 2,              
        'NumberOfDeviceRegistered': 3      
    }
    
    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])
    
    # One-Hot Encode the categorical inputs
    input_encoded = pd.get_dummies(input_df)
    
    # Align the new columns with the exact columns the model expects (fills missing with 0)
    input_aligned = input_encoded.reindex(columns=expected_cols, fill_value=0)
    
    # Scale the data using the saved standard scaler
    input_scaled = scaler.transform(input_aligned)
    
    # Generate Predictions
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1] * 100
    
    # Display the final results
    st.divider()
    if prediction == 1:
        st.error(f"⚠️ **High Risk of Churn!** (Probability: {probability:.2f}%)")
        st.write("This customer exhibits behaviors closely aligning with historical churn patterns.")
    else:
        st.success(f"✅ **Customer is Likely to Retain.** (Churn Probability: {probability:.2f}%)")
        st.write("This customer is showing healthy engagement metrics.")
