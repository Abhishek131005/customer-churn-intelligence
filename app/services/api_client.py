import os
import requests


API_URL = os.getenv(
    "CHURN_API_URL",
    "http://127.0.0.1:8000"
)


def predict_customer(customer_data):
    response = requests.post(
        f"{API_URL}/predict",
        json=customer_data,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def check_api_health():
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=3
        )

        return response.status_code == 200

    except requests.RequestException:
        return False