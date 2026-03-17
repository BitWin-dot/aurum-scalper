# main.py — Aurum Scalper Telegram Test Skeleton

import time
from config import DERIV_TOKENS, TELEGRAM_TOKEN, CHAT_ID
from telegram_bot import send

def run_bot():
    """
    Simple test run:
    Sends a Telegram message to confirm bot connectivity
    """
    # Send test message
    send("✅ Aurum Scalper Test Message: Telegram bot is working!")

    print("Bot is running... check Telegram for test message.")
    
    # Keep the bot alive (placeholder loop for future strategy execution)
    while True:
        print("Bot loop running... (placeholder)")
        time.sleep(5)  # 5-second interval for testing

if __name__ == "__main__":
    run_bot()
