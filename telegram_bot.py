# telegram_bot.py

import requests
import logging

# Optional: you can configure logging here for Telegram errors
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def send_telegram_message(bot_token, chat_id, message):
    """
    Sends a message to a Telegram chat using a bot.

    Args:
        bot_token (str): Your Telegram Bot API token
        chat_id (str or int): The Telegram chat ID
        message (str): The message text to send
    """
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()  # Raise an error for bad HTTP responses
    except requests.exceptions.RequestException as e:
        logger.error(f"Telegram send error: {e}")
        # Optional: fallback or retry logic can be added here
