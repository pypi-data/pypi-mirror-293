# src/chippapi/api.py

import requests
import chippapi

def chat(prompt):
    if chippapi.api_key is None or chippapi.id is None:
        raise ValueError("API key and ID must be set before calling the chat function.")

    url = "https://api.chipp.ai/chat"
    headers = {
        "Authorization": f"Bearer {chippapi.api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "id": chippapi.id,
        "prompt": prompt
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()
