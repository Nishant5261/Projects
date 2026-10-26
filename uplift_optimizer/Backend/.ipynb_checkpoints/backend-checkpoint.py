from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import xgboost as xgb
import traceback

app = FastAPI(title="Causal ML Uplift API")

try:
    models = joblib.load('uplift_model.pkl')
    model_c = models['control_model']
    model_t = models['treatment_model']
    feature_cols = models['features']
    model_type = models['type']  
    print(f"✅ Uplift T-Learner loaded successfully.")
except Exception as e:
    print(f"❌ Load error: {e}")
    model_c, model_t = None, None

class CustomerFeatures(BaseModel):
    f0: float; f1: float; f2: float; f3: float; f4: float; f5: float
    f6: float; f7: float; f8: float; f9: float; f10: float; f11: float

@app.post("/predict_uplift")
def predict(customer: CustomerFeatures):
    if model_c is None:
        return JSONResponse(status_code=500, content={"detail": "Model failed to load."})
    
    try:
        input_df = pd.DataFrame([customer.model_dump()])[feature_cols]
        
        if model_type == 'xgb':
            dmatrix_input = xgb.DMatrix(input_df)
            prob_control = float(model_c.predict(dmatrix_input)[0])
            prob_treat = float(model_t.predict(dmatrix_input)[0])
        else:
            prob_control = float(model_c.predict(input_df)[0])
            prob_treat = float(model_t.predict(input_df)[0])
            
        uplift_score = prob_treat - prob_control
        
        if uplift_score > 0.05: persona = "Persuadable (Send Discount)"
        elif uplift_score < -0.05: persona = "Sleeping Dog (Do Not Contact)"
        elif prob_control > 0.5: persona = "Sure Thing (Will buy anyway)"
        else: persona = "Lost Cause (Will not buy)"
        
        return JSONResponse({
            "status": "success",
            "data": {
                "uplift_score": round(uplift_score, 4),
                "prob_organic": round(prob_control, 4),
                "prob_incentivized": round(prob_treat, 4),
                "customer_persona": persona
            }
        })
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": str(e)})