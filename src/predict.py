import joblib
import pandas as pd


# 1. Load the trained model
model = joblib.load("models/risk_model.joblib")


# 2. Create a new insurance claim with the same feature names
new_claim = pd.DataFrame([{
    "claim_amount": 900000,
    "customer_age": 45,
    "previous_claims": 6,
    "vehicle_age": 10,
    "policy_age": 1,
}])


# 3. Make prediction
prediction = model.predict(new_claim)[0]


# 4. Get prediction probabilities
probabilities = model.predict_proba(new_claim)[0]

not_fraud_probability = probabilities[0]
fraud_probability = probabilities[1]


# 5. Display result
if prediction == 1:
    result = "Potential Fraud"
else:
    result = "Not Fraud"


print("Prediction:", result)
print(f"Not Fraud Probability: {not_fraud_probability:.2%}")
print(f"Fraud Probability: {fraud_probability:.2%}")