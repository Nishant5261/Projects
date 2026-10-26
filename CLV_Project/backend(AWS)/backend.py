from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import time
import traceback

app = FastAPI(title="CLV API")

# Attempt to load the model globally, but set it to None if it fails
try:
    model = joblib.load('clv_model.pkl')
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Model load error: {e}")
    model = None

class Customer(BaseModel):
    recency: int = Field(..., ge=0)
    model_recency: int = Field(..., ge=0)
    customer_tenure: int = Field(..., ge=0)
    frequency: int = Field(..., ge=0)
    monetary: float = Field(..., ge=0.0)
    avg_order_value: float = Field(..., ge=0.0)

@app.post("/predict_clv")
def predict(customer: Customer):
    # 1. Check if the model actually loaded at startup
    if model is None:
        return JSONResponse(
            status_code=500, 
            content={"detail": "Model failed to load on server startup. Check terminal logs."}
        )

    try:
        start_time = time.time()
        input_df = pd.DataFrame([customer.model_dump()])
        
        pred = max(0.0, float(model.predict(input_df)[0]))
        
        return JSONResponse({
            "status": "success",
            "data": {"predicted_usd": round(pred, 2)},
            "metadata": {"processing_time_ms": round((time.time() - start_time) * 1000, 2)}
        })
        
    except Exception as e:
        # 2. Catch any prediction errors (like Pandas type mismatches) and return them to Swagger
        error_trace = traceback.format_exc()
        print(error_trace) # Prints full error to your terminal
        return JSONResponse(
            status_code=500, 
            content={
                "detail": "Prediction execution failed.",
                "error_message": str(e)
            }
        )
