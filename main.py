# main.py - Aurum Scalper Minimal Stable Version

import time
from deriv_api import DerivWS
import requests

# -------------------------------
# ✅ TOKENS
DERIV_API_TOKEN = "gIUrsIg5H56ZNfC"
TELEGRAM_BOT_TOKEN = "8693765411:AAHql2ysRMOhvtgPuNf9JdyE6yfqfEowmjs"
TELEGRAM_CHAT_ID = "-5180694120"
# -------------------------------

# Telegram function
def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegram error:", e)

# Test Telegram
send_telegram_message("✅ Aurum Scalper Minimal Bot Running")

# Candle handler
def handle_candle(candle):
    try:
        print(f"Candle received: {candle}")  # Debug log
    except Exception as e:
        print("Candle handler error:", e)

# Start Deriv WebSocket
ws = DerivWS(api_token=DERIV_API_TOKEN)
ws.candle_handler = handle_candle
ws.start()
print("🚀 Aurum Scalper Minimal Bot Started")

# Main loop
try:
    while True:
        print("Waiting for live candles...")
        time.sleep(5)
except KeyboardInterrupt:
    print("Bot stopped manually")
except Exception as e:
    print("Bot crashed:", e)
