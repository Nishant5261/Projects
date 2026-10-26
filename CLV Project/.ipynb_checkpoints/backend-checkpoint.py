`from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import time

app = FastAPI(title="CLV API")

# Load the LightGBM model directly from the joblib file
try:
    model = joblib.load('clv_model.pkl')
except Exception as e:
    print("Model load error:", e)

class Customer(BaseModel):
    recency: int = Field(..., ge=0)
    model_recency: int = Field(..., ge=0)
    customer_tenure: int = Field(..., ge=0)
    frequency: int = Field(..., ge=0)
    monetary: float = Field(..., ge=0.0)
    avg_order_value: float = Field(..., ge=0.0)

@app.get("/")
def hello():
    return JSONResponse({
        "status": "success",
        "content": "Welcome to CLV model api"})

@app.post("/predict_clv")
def predict(customer: Customer):
    start_time = time.time()
    input_df = pd.DataFrame([customer.model_dump()])
    
    pred = max(0.0, float(model.predict(input_df)[0]))
    
    return JSONResponse({
        "status": "success",
        "data": {"predicted_usd": round(pred, 2)},
        "metadata": {"processing_time_ms": round((time.time() - start_time) * 1000, 2)}
    })