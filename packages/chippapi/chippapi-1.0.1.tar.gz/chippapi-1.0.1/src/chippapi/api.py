# src/chippapi/api.py

import requests
import chippapi

def chat(prompt, message_list=None, thread_id=None):
    if chippapi.api_key is None or chippapi.id is None:
        raise ValueError("API key and ID must be set before calling the chat function.")

    url = "https://api.chipp.ai/chat"
    headers = {
        "Authorization": f"Bearer {chippapi.api_key}",
        "Content-Type": "application/json"
    }
    if message_list is None:
        message_list = [{"senderType": "USER", "content": prompt}]
    else:
        message_list.append({"senderType": "USER", "content": prompt})

    data = {
        "applicationId": chippapi.id,
        "apiKey": chippapi.api_key,
        "messageList": message_list
    }
    if thread_id:
        data["threadId"] = thread_id

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()
