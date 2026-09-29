from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / "models" / "risk_model.joblib"
STATIC_DIR = BASE_DIR / "static"


model = joblib.load(MODEL_PATH)


app = FastAPI(
    title="Customer Risk Predictor",
    description="Insurance claim fraud prediction API",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


class Claim(BaseModel):
    claim_amount: float
    customer_age: int
    previous_claims: int
    vehicle_age: int
    policy_age: int


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/predict")
def predict(claim: Claim):

    data = pd.DataFrame([{
        "claim_amount": claim.claim_amount,
        "customer_age": claim.customer_age,
        "previous_claims": claim.previous_claims,
        "vehicle_age": claim.vehicle_age,
        "policy_age": claim.policy_age,
    }])

    prediction = model.predict(data)[0]

    probabilities = model.predict_proba(data)[0]

    not_fraud_probability = probabilities[0]
    fraud_probability = probabilities[1]

    if prediction == 1:
        result = "Potential Fraud"
    else:
        result = "Not Fraud"

    return {
        "prediction": result,
        "not_fraud_probability": round(
            float(not_fraud_probability), 4
        ),
        "fraud_probability": round(
            float(fraud_probability), 4
        ),
    }