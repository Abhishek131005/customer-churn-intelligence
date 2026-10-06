import os

import requests


API_URL = os.getenv(
    "CHURN_API_URL",
    "http://127.0.0.1:8000"
)


def predict_customer(customer_data):
    """
    Send customer data to the FastAPI prediction service.

    In local development, requests are sent to localhost.
    In production, CHURN_API_URL points to the deployed
    Render API.
    """

    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=customer_data,
            timeout=60
        )

        response.raise_for_status()

        return response.json()

    except requests.Timeout as exc:
        raise RuntimeError(
            "The prediction service is taking longer than expected. "
            "Please try again in a moment."
        ) from exc

    except requests.RequestException as exc:
        raise RuntimeError(
            "Unable to connect to the prediction service."
        ) from exc


def check_api_health():
    """
    Check whether the prediction API is available.
    """

    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=30
        )

        return response.status_code == 200

    except requests.RequestException:
        return False