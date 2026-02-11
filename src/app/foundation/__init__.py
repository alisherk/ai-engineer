from openai import OpenAI
import requests

from src.app.settings import get_settings

settings = get_settings()

def push(message: str):
    """Push a message to the user using Pushover"""
    data = {
        "token": settings.pushover_key,
        "user": settings.pushover_user,
        "message": message,
    }
    response = requests.post(settings.pushover_api, data=data)
    response.raise_for_status()

push("Hello from Career Ego!")

