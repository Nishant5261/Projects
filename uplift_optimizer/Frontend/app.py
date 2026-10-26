import streamlit as st
import requests

st.set_page_config(page_title="Uplift Optimizer", layout="wide")
st.title("🎯 Causal ML: Marketing Uplift Optimizer")
st.write("Identifies the true causal impact of marketing interventions to eliminate wasted ad spend.")

# Replace with your AWS EC2 Public IPv4
API_URL = "http://13.201.185.7:5000/predict_uplift"

# 1. Educational UI for Non-Technical Users & Interns
with st.expander("🎓 Intern Onboarding Guide: How to Read this Dashboard", expanded=False):
    st.markdown("""
    **What are we doing here?**
    Instead of guessing who to send a discount code to, this AI predicts exactly how a customer's behavior will *change* if we send them an ad.
    
    **Glossary of Metrics:**
    *   **Organic Conversion Prob:** The chance this customer will buy today if we do absolutely nothing. (If this is high, don't send a discount—they are already going to buy!).
    *   **Incentivized Prob:** The chance they will buy *only if* we send them the ad/discount.
    *   **True Causal Uplift:** The actual mathematical difference the ad makes. (Incentivized minus Organic). We only want to spend marketing money on users with a high positive Uplift.
    """)

# 2. Industry-Standard Proxy Names for Criteo's Anonymized Features
feature_mapping = {
    "f0": {"name": "Recency (Days since last visit)", "max": 30.0, "val": 5.0, "step": 1.0},
    "f1": {"name": "Historical Click Rate (%)", "max": 100.0, "val": 12.5, "step": 0.5},
    "f2": {"name": "Past Purchase Frequency", "max": 50.0, "val": 3.0, "step": 1.0},
    "f3": {"name": "Time on Site (Minutes)", "max": 60.0, "val": 15.0, "step": 1.0},
    "f4": {"name": "Session Depth (Pages viewed)", "max": 20.0, "val": 4.0, "step": 1.0},
    "f5": {"name": "Cart Abandonment Score", "max": 10.0, "val": 2.5, "step": 0.1},
    "f6": {"name": "Ad Exposures (Last 7 days)", "max": 50.0, "val": 10.0, "step": 1.0},
    "f7": {"name": "Customer Lifetime Value Score", "max": 100.0, "val": 65.0, "step": 1.0},
    "f8": {"name": "Email Open Rate (%)", "max": 100.0, "val": 22.0, "step": 0.5},
    "f9": {"name": "Days Since Account Creation", "max": 365.0, "val": 120.0, "step": 1.0},
    "f10": {"name": "Avg. Order Value ($)", "max": 200.0, "val": 45.0, "step": 1.0},
    "f11": {"name": "Brand Affinity Score", "max": 10.0, "val": 7.0, "step": 0.1}
}

with st.sidebar.form("customer_data"):
    st.header("Customer Profile")
    st.caption("Adjust user behavior metrics to simulate causal impact.")
    
    # Generate business-readable sliders but store data in the f0-f11 format for the API
    f_data = {}
    for key, meta in feature_mapping.items():
        # The UI shows the business name, but the dictionary saves the f0-f11 key
        f_data[key] = st.slider(meta["name"], 0.0, meta["max"], meta["val"], step=meta["step"])
        
    submit = st.form_submit_button("Analyze Causal Impact")

if submit:
    try:
        with st.spinner("Running Dual-Model Engine..."):
            res = requests.post(API_URL, json=f_data)
            
            if res.status_code == 200:
                data = res.json()["data"]
                
                # Executive Metrics Display
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Organic Conversion Prob", f"{data['prob_organic']*100:.1f}%")
                    st.caption("Probability of buying without any ad.")
                with col2:
                    st.metric("Incentivized Prob", f"{data['prob_incentivized']*100:.1f}%")
                    st.caption("Probability of buying with the discount.")
                with col3:
                    st.metric("True Causal Uplift", f"{data['uplift_score']*100:+.1f}%", 
                              delta_color="normal" if data['uplift_score'] > 0 else "inverse")
                    st.caption("The exact margin gained by marketing.")
                
                st.divider()
                
                # Persona Routing & Business Logic
                st.subheader(f"🧠 Customer Persona: {data['customer_persona']}")
                
                if "Persuadable" in data['customer_persona']: 
                    st.success("✅ **Action:** Allocate Marketing Budget here. This ad directly causes new revenue that would not have happened otherwise.")
                elif "Sure Thing" in data['customer_persona']: 
                    st.warning("⚠️ **Action:** Withhold ad. They are highly likely to buy anyway. Sending a discount code burns your profit margin.")
                elif "Lost Cause" in data['customer_persona']: 
                    st.error("🚫 **Action:** Withhold ad. They are highly unlikely to convert regardless of the discount. Save the budget.")
                else: 
                    st.error("🛑 **Action:** Withhold ad. Marketing to this user actively annoys them and decreases their conversion likelihood.")
            else:
                st.error(f"API Error: {res.text}")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to AWS backend. Ensure your EC2 Port 8000 is open and Docker is running.")