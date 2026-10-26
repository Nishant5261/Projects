import streamlit as st
import requests

st.set_page_config(page_title="Uplift Optimizer", layout="wide")
st.title("🎯 Causal ML: Marketing Uplift Optimizer")
st.write("Identifies the true causal impact of marketing interventions to eliminate wasted ad spend.")

# Replace with your AWS EC2 Public IPv4
API_URL = "http://13.201.185.7:5000/predict_uplift"

with st.sidebar.form("customer_data"):
    st.header("Customer Profile")
    st.caption("Criteo Anonymized Features")
    f_data = {f"f{i}": st.slider(f"Feature {i}", 0.0, 10.0, 1.0) for i in range(12)}
    submit = st.form_submit_button("Analyze Causal Impact")

if submit:
    try:
        with st.spinner("Running Dual-Model Engine..."):
            res = requests.post(API_URL, json=f_data)
            
            if res.status_code == 200:
                data = res.json()["data"]
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Organic Conversion Prob", f"{data['prob_organic']*100:.1f}%")
                col2.metric("Incentivized Prob", f"{data['prob_incentivized']*100:.1f}%")
                col3.metric("True Causal Uplift", f"{data['uplift_score']*100:+.1f}%", 
                            delta_color="normal" if data['uplift_score'] > 0 else "inverse")
                
                st.subheader(f"🧠 Customer Persona: {data['customer_persona']}")
                
                if "Persuadable" in data['customer_persona']: 
                    st.success("Action: Allocate Marketing Budget here. This intervention directly causes revenue.")
                elif "Sure Thing" in data['customer_persona']: 
                    st.warning("Action: Withhold ad. They will buy anyway. Targeting wastes margin.")
                elif "Lost Cause" in data['customer_persona']: 
                    st.error("Action: Withhold ad. Highly unlikely to convert regardless of discount.")
                else: 
                    st.error("Action: Withhold ad. Marketing to this user actively decreases conversion likelihood.")
            else:
                st.error(f"API Error: {res.text}")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to AWS backend. Ensure your EC2 Port 8000 is open and Docker is running.")