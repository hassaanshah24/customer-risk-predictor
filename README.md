# Customer Risk Predictor

An end-to-end machine learning application for predicting potentially fraudulent insurance claims.

The project was built as a learning implementation of an enterprise-style AI/ML workflow, covering business problem analysis, supervised machine learning, model training, evaluation, inference, API development, UI integration, containerization, and cloud deployment.

---

# 1. Client Problem

### Fictional Client

**SafeShield Insurance**

### Business Scenario

An insurance company receives a large number of claims.

Some claims are legitimate while others may be fraudulent.

The company wants to identify potentially suspicious claims so that investigators can review them.

The system should use historical claims to learn patterns associated with fraud and then make a prediction for a new claim.

---

# 2. Business Requirement

The system should accept information about a new insurance claim and return:

* Whether the claim is predicted as potentially fraudulent
* Probability of fraud
* Probability of not being fraudulent

The result is intended to support investigation.

It is not intended to automatically declare that a customer committed fraud.

---

# 3. Problem Analysis

We first determine what kind of problem we have.

### Input

Each historical claim contains information such as:

* Claim amount
* Customer age
* Previous claims
* Vehicle age
* Policy age

### Historical Answer

Each historical claim also contains:

* `fraud = 0` → Not Fraud
* `fraud = 1` → Fraud

Because historical examples already contain the correct answer, this is a:

**Supervised Learning problem**

Because the answer is one of two categories:

* Fraud
* Not Fraud

this is a:

**Classification problem**

Therefore:

> Historical labelled data + categorical prediction = supervised classification.

---

# 4. Why AI / Machine Learning?

A simple rule-based system could contain rules such as:

```text
IF claim amount > 500000
THEN suspicious
```

However, real-world fraud detection may involve combinations of many variables.

Machine learning allows us to learn patterns from historical examples instead of manually writing every possible rule.

The model can then apply the learned pattern to a new claim.

---

# 5. Dataset

The project uses a small synthetic dataset for learning purposes.

Features:

| Feature           | Meaning                       |
| ----------------- | ----------------------------- |
| `claim_amount`    | Amount requested in the claim |
| `customer_age`    | Age of the customer           |
| `previous_claims` | Number of previous claims     |
| `vehicle_age`     | Age of the vehicle            |
| `policy_age`      | Age of the insurance policy   |

Label:

| Value | Meaning   |
| ----- | --------- |
| `0`   | Not Fraud |
| `1`   | Fraud     |

Dataset location:

```text
data/claims.csv
```

The dataset contains only 20 synthetic examples.

Therefore, it is suitable for learning the ML workflow but not for building a production fraud detection system.

---

# 6. Technology Decision

### Python

Used as the primary programming language because Python has a mature ecosystem for machine learning and data processing.

### Pandas

Used to load and manipulate the tabular dataset.

### scikit-learn

Used for machine learning because the problem is structured/tabular classification and scikit-learn provides the required algorithms and evaluation tools.

### Decision Tree

A Decision Tree was selected as the first model because it is relatively easy to understand.

Conceptually, the model learns decision paths such as:

```text
Is claim amount high?
        |
       Yes
        |
Are previous claims high?
        |
       Yes
        |
Potentially Fraud
```

The actual learned tree is determined by the training data.

### FastAPI

Used to expose the trained model through an HTTP API.

### HTML / CSS / JavaScript

Used to provide a simple human-facing interface.

### Docker

Used to package the application and its dependencies into a consistent container.

### Artifact Registry

Used to store the Docker container image in Google Cloud.

### Cloud Run

Used to run the containerized application as a managed cloud service.

---

# 7. Architecture

The application architecture is:

```text
                    User
                     |
                     v
              Web Browser / UI
                     |
                     v
                  FastAPI
                     |
                     v
             Saved ML Model
          risk_model.joblib
                     |
                     v
                Prediction
                     |
                     v
              FastAPI Response
                     |
                     v
                    UI
```

Cloud deployment adds:

```text
Local Application
       |
       v
     Docker
       |
       v
Container Image
       |
       v
Artifact Registry
       |
       v
   Cloud Run
       |
       v
Public HTTPS Application
```

---

# 8. Machine Learning Workflow

The training process is:

```text
CSV Dataset
    |
    v
Load with Pandas
    |
    v
Separate Features and Label
    |
    v
Train/Test Split
    |
    v
Train Decision Tree
    |
    v
Evaluate Model
    |
    v
Save Model
```

The prediction process is:

```text
New Claim
    |
    v
Load Saved Model
    |
    v
Model Prediction
    |
    v
Fraud / Not Fraud
    |
    v
Probability
```

---

# 9. Training

The dataset is divided into:

* Training data
* Testing data

In this project:

* Training rows: 16
* Testing rows: 4

The model learns from the training set and is evaluated on data that was held out during training.

The model uses:

```text
DecisionTreeClassifier
max_depth = 3
```

The trained model is saved as:

```text
models/risk_model.joblib
```

---

# 10. Evaluation

The model produced:

```text
Accuracy : 1.0
Precision: 1.0
Recall   : 1.0
```

Confusion matrix:

```text
[[2 0]
 [0 2]]
```

These results mean that all four test examples were classified correctly.

However, these numbers must not be interpreted as evidence that the model is production-ready.

The test set contains only four examples and the entire dataset contains only 20 synthetic examples.

A real fraud detection system would require a much larger and representative historical dataset and much more rigorous validation.

---

# 11. Inference

A new claim can be passed to the trained model.

Example:

```text
Claim amount:       900000
Customer age:       45
Previous claims:    6
Vehicle age:        10
Policy age:         1
```

The model returned:

```text
Prediction: Potential Fraud
Fraud Probability: 100%
Not Fraud Probability: 0%
```

The probability shown here represents the model's prediction based on the small synthetic training dataset.

It should not be interpreted as literal certainty that the claim is fraudulent.

---

# 12. API

FastAPI exposes the prediction functionality through:

```text
POST /predict
```

The API accepts:

```json
{
  "claim_amount": 900000,
  "customer_age": 45,
  "previous_claims": 6,
  "vehicle_age": 10,
  "policy_age": 1
}
```

and returns prediction information including:

```json
{
  "prediction": "Potential Fraud",
  "not_fraud_probability": 0.0,
  "fraud_probability": 1.0
}
```

---

# 13. User Interface

The application includes a browser-based interface.

The user enters:

* Claim amount
* Customer age
* Previous claims
* Vehicle age
* Policy age

and selects:

```text
Predict Risk
```

The UI then displays the model's prediction and probabilities.

This provides a human-facing way to test the complete application rather than relying only on terminal commands.

---

# 14. Docker

The application was containerized using Docker.

The container contains:

* Python
* FastAPI
* Uvicorn
* Pandas
* scikit-learn
* Joblib
* Application code
* Trained model
* UI

The application listens on port:

```text
8080
```

Docker allows the same packaged application to run consistently across environments.

---

# 15. Google Cloud Deployment

The Docker image was pushed to Google Artifact Registry.

Repository:

```text
customer-risk
```

Region:

```text
asia-south1
```

The application was then deployed to Google Cloud Run.

Cloud Run provides the managed environment in which the container runs and exposes the application through HTTPS.

Deployment architecture:

```text
Docker Image
     |
     v
Artifact Registry
     |
     v
Cloud Run
     |
     v
Customer Risk Predictor
```

The deployed application is available through its Cloud Run HTTPS URL.

---

# 16. Important Cloud Concepts Learned

### Artifact Registry

Think of Artifact Registry as a cloud warehouse for packaged application images.

We store the Docker image there so Google Cloud services can retrieve it.

### Cloud Run

Cloud Run is the place where the container actually runs.

So:

```text
Artifact Registry = stores the image

Cloud Run = runs the image
```

### Docker

Docker packages the application.

Therefore:

```text
Docker → package
Artifact Registry → store
Cloud Run → run
```

---

# 17. What This Deployment Is — and Is Not

This project demonstrates:

**Application deployment**

The FastAPI application contains the ML model and serves predictions.

It does NOT yet demonstrate the dedicated Vertex AI model lifecycle.

A later project will separately cover:

```text
Model
   |
   v
Vertex AI Model Registry
   |
   v
Vertex AI Endpoint
   |
   v
Online Prediction
   |
   v
Monitoring
```

Keeping these two deployment approaches separate makes the learning process clearer.

---

# 18. Limitations

This project has significant limitations.

### Dataset

The dataset is synthetic and extremely small.

A production model would require real, representative historical data.

### Model evaluation

Only four examples were used for testing.

Therefore, the perfect evaluation scores are not statistically meaningful for production.

### Feature quality

The model uses only five simple features.

Real fraud detection would likely require many more relevant signals.

### Data quality

Real systems must handle:

* Missing values
* Incorrect values
* Outliers
* Duplicate records
* Changing data distributions

### Fraud imbalance

Real fraud datasets may contain far fewer fraudulent claims than legitimate claims.

Accuracy alone would therefore be insufficient.

### Security

The demo API is publicly accessible.

A production insurance application would require authentication, authorization, secure secrets, logging, monitoring, and other security controls.

### Responsible AI

A real insurance system would also need appropriate privacy, fairness, explainability, human oversight, and regulatory controls.

---

# 19. When To Use This Approach

A supervised classification model is appropriate when:

* Historical labelled examples exist
* The desired output is a category
* The problem can be represented using structured features
* The objective is to predict an outcome for new examples

Examples include:

* Fraud detection
* Customer churn prediction
* Spam detection
* Loan default classification
* Risk classification

---

# 20. When NOT To Use This Approach

This approach is not automatically appropriate for every AI problem.

For example:

### Need to answer questions from private documents

Use a RAG architecture.

### Need an open-ended conversational assistant

Consider an LLM such as Gemini.

### Need the system to call external tools and perform actions

Consider tool calling or agents.

### Need a continuous numeric prediction

Use regression rather than classification.

### Need complex image understanding

A computer vision/deep learning approach may be more appropriate.

The business requirement should determine the technology.

---

# 21. Key Lessons

The most important lessons from Project 1 are:

1. Features are the inputs given to a model.
2. A label is the answer the model learns to predict.
3. Historical labelled data usually points toward supervised learning.
4. A categorical target points toward classification.
5. Structured/tabular data is a common ML use case.
6. Training and inference are different stages.
7. A trained model can be saved and loaded later.
8. Evaluation must be performed on data not used for training.
9. Perfect metrics on a tiny synthetic dataset do not prove production quality.
10. FastAPI can turn a model into a usable service.
11. A UI makes the system observable and testable by humans.
12. Docker packages the application.
13. Artifact Registry stores the container image.
14. Cloud Run runs the container.
15. Application deployment and Vertex AI model deployment are separate concepts.
16. Technology should be selected based on the business problem.

---

# 22. Project Structure

```text
customer-risk-predictor/
│
├── data/
│   └── claims.csv
│
├── src/
│   ├── train.py
│   └── predict.py
│
├── models/
│   └── risk_model.joblib
│
├── app/
│   ├── main.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── app.js
│
├── tests/
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# 23. Final End-to-End Flow

The complete project can be summarized as:

```text
Business Problem
       |
       v
Fraud Detection
       |
       v
Supervised Classification
       |
       v
Synthetic Historical Data
       |
       v
Pandas
       |
       v
scikit-learn
       |
       v
Decision Tree
       |
       v
Model Evaluation
       |
       v
Saved Model
       |
       v
FastAPI
       |
       v
Web UI
       |
       v
Docker
       |
       v
Artifact Registry
       |
       v
Cloud Run
       |
       v
Deployed AI Application
```

---

# 24. Project Status

| Area              | Status   |
| ----------------- | -------- |
| Business problem  | Complete |
| Problem analysis  | Complete |
| Dataset           | Complete |
| Model training    | Complete |
| Evaluation        | Complete |
| Inference         | Complete |
| FastAPI           | Complete |
| UI                | Complete |
| Docker            | Complete |
| Artifact Registry | Complete |
| Cloud Run         | Complete |
| Documentation     | Complete |
| Knowledge card    | Next     |
| Git commit        | Next     |

---

# 25. Project Conclusion

Customer Risk Predictor is the first project in the AI/ML learning path.

Its purpose was not to create a production fraud detector.

Its purpose was to establish the complete foundation:

**business problem → ML problem → model → evaluation → API → UI → container → cloud**

This foundation will be reused in later projects when learning neural networks, generative AI, RAG, Vertex AI, MLOps, monitoring, CI/CD, and production AI systems.
