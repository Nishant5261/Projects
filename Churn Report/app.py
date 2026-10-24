import gradio as gr
import pandas as pd
import joblib

# Load the saved assets
model = joblib.load('xgboost_churn_model.pkl')
scaler = joblib.load('scaler.pkl')
expected_cols = joblib.load('feature_columns.pkl')

def predict_churn(tenure, complain, cashback, warehouse_dist, order_cat, app_hours, order_count, satisfaction):
    # Map 'Yes'/'No' to 1/0
    complain_val = 1 if complain == "Yes" else 0
    
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
    
    # Process and align data
    input_df = pd.DataFrame([input_data])
    input_encoded = pd.get_dummies(input_df)
    input_aligned = input_encoded.reindex(columns=expected_cols, fill_value=0)
    input_scaled = scaler.transform(input_aligned)
    
    # Predict
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1] * 100
    
    if prediction == 1:
        return f"⚠️ High Risk of Churn! (Probability: {probability:.2f}%)"
    else:
        return f"✅ Customer is Likely to Retain. (Churn Probability: {probability:.2f}%)"

# Build the Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🛒 E-Commerce Customer Churn Predictor")
    gr.Markdown("Enter customer details below to predict their likelihood of churning.")
    
    with gr.Row():
        with gr.Column():
            tenure = gr.Number(label="Tenure (Months)", value=5, minimum=0, maximum=100)
            complain = gr.Radio(["No", "Yes"], label="Logged a Complaint?", value="No")
            cashback = gr.Number(label="Average Cashback Amount ($)", value=150, minimum=0)
            warehouse_dist = gr.Number(label="Distance from Warehouse", value=15, minimum=1)
        
        with gr.Column():
            order_cat = gr.Dropdown(['Laptop & Accessory', 'Mobile Phone', 'Fashion', 'Grocery', 'Others'], label="Preferred Order Category", value="Laptop & Accessory")
            app_hours = gr.Number(label="Hours Spent on App", value=3, minimum=0, maximum=24)
            order_count = gr.Number(label="Total Order Count", value=4, minimum=1)
            satisfaction = gr.Slider(minimum=1, maximum=5, step=1, label="Satisfaction Score", value=3)
            
    submit_btn = gr.Button("Predict Churn Risk", variant="primary")
    output = gr.Textbox(label="Prediction Result")
    
    submit_btn.click(
        fn=predict_churn,
        inputs=[tenure, complain, cashback, warehouse_dist, order_cat, app_hours, order_count, satisfaction],
        outputs=output
    )

demo.launch(theme=gr.themes.Soft())
