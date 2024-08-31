# tests/test.py

import chippapi
import logging
import requests

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Set the API key and ID
chippapi.api_key = "live_96a3ab56-ae9d-4dea-be4b-9bbb3710cfb6"
chippapi.id = 10068

# Test the chat function
try:
    response = chippapi.chat("How are you?")
    print(response)
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")