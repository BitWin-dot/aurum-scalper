import requests
from config import TELEGRAM_TOKEN, CHAT_ID

def send(message: str):
    """
    Send a message to your Telegram group
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        r = requests.post(url, data=payload)
        if r.status_code != 200:
            print(f"Telegram send failed: {r.text}")
    except Exception as e:
        print(f"Telegram exception: {e}")
