import requests
from .config import MepostConfig


def send_request(method: str, endpoint: str, data=None, config=None):
    url = f"{config.base_url}{endpoint}"
    headers = {
        "Authorization": config.api_key,
        "Content-Type": "application/json"
    }
    response = requests.request(method, url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()
