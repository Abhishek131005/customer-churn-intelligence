from fastapi import FastAPI
from pydantic import BaseModel

from src.models.predict import predict_churn


app = FastAPI(
    title="Customer Churn Intelligence API",
    description=(
        "Machine learning API for customer churn "
        "prediction and revenue-risk estimation."
    ),
    version="1.0.0"
)


class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int

    PhoneService: str
    MultipleLines: str

    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str

    Contract: str
    PaperlessBilling: str
    PaymentMethod: str

    MonthlyCharges: float
    TotalCharges: float


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Customer Churn Intelligence API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/predict")
def predict(customer: CustomerData):

    customer_dict = customer.model_dump()

    result = predict_churn(
        customer_dict
    )

    return result