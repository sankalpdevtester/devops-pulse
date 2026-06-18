import requests
from src.models.webhook import Webhook

def trigger_webhook(webhook: Webhook):
    try:
        response = requests.request(webhook.method, webhook.url)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False