import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
)


# 1. Load historical claims
df = pd.read_csv("data/claims.csv")


# 2. Separate features from label
X = df[
    [
        "claim_amount",
        "customer_age",
        "previous_claims",
        "vehicle_age",
        "policy_age",
    ]
]

y = df["fraud"]


# 3. Split historical data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)


# 4. Create the ML model
model = DecisionTreeClassifier(
    max_depth=3,
    random_state=42,
)


# 5. Train the model
model.fit(X_train, y_train)

print("Training complete.")
print("Training rows:", len(X_train))
print("Test rows:", len(X_test))


# 6. Make predictions on unseen test data
y_pred = model.predict(X_test)


# 7. Evaluate predictions
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
matrix = confusion_matrix(y_test, y_pred)


print("\nEvaluation")
print("----------")
print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)

print("\nConfusion Matrix")
print(matrix)

# 8. Save the trained model
joblib.dump(model, "models/risk_model.joblib")

print("\nModel saved to models/risk_model.joblib")