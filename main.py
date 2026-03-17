# main.py — Aurum Scalper Telegram + Deriv Test Skeleton

import time
from config import DERIV_TOKENS, TELEGRAM_TOKEN, CHAT_ID
from telegram_bot import send
from deriv_api import DerivWS

def run_bot():
    """
    Test run:
    - Sends Telegram message to confirm bot connectivity
    - Connects to Deriv WebSocket and prints live XAU/USD candles
    """

    # 1️⃣ Send Telegram test message
    send("✅ Aurum Scalper Test Message: Telegram bot is working!")
    print("Telegram test message sent. Check your group.")

    # 2️⃣ Start Deriv WebSocket client
    deriv_client = DerivWS()
    print("Starting Deriv WebSocket...")
    
    # Run WebSocket in a separate thread so it doesn't block loop
    import threading
    ws_thread = threading.Thread(target=deriv_client.start)
    ws_thread.daemon = True
    ws_thread.start()

    # 3️⃣ Keep bot alive
    while True:
        print("Bot loop running... waiting for live candles...")
        time.sleep(5)  # placeholder interval for testing

if __name__ == "__main__":
    run_bot()
