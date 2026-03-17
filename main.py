# main.py - Aurum Scalper Full Production-Ready

import time
from deriv_api import DerivWS, buy_contract
import requests

# -------------------------------
# ✅ YOUR TOKENS / CHAT ID
DERIV_API_TOKEN = "gIUrsIg5H56ZNfC"
TELEGRAM_BOT_TOKEN = "8693765411:AAHql2ysRMOhvtgPuNf9JdyE6yfqfEowmjs"
TELEGRAM_CHAT_ID = "-5180694120"
# -------------------------------

# --- Telegram messaging ---
def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegram error:", e)

# Test Telegram
send_telegram_message("✅ Aurum Scalper Test Message: Telegram bot is working")

# --- Candle handler ---
def handle_candle(candle):
    try:
        print(f"Candle received: {candle}")  # Debug log

        # ---------------------------------------------
        # Here you can call your strategy scoring functions
        # Example placeholder:
        score = 3  # Replace with actual strategy logic
        if score >= 3:
            # Example trade execution
            amount = 1  # USD stake, adjust with risk management
            contract_type = "CALL"  # or "PUT" based on strategy
            duration = 1  # 1 tick / 1 minute
            result = buy_contract(DERIV_API_TOKEN, "frxXAUUSD", amount, contract_type, duration)
            if result:
                send_telegram_message(f"TRADE EXECUTED: {contract_type} | Result: {result}")
    except Exception as e:
        print("Candle handler error:", e)

# --- Start Deriv WebSocket ---
ws = DerivWS(api_token=DERIV_API_TOKEN)
ws.candle_handler = handle_candle
ws.start()
print("🚀 Aurum Scalper Bot Starting with Live Deriv Candles...")

# --- Main loop ---
try:
    while True:
        print("Bot loop running... waiting for live candles...")
        time.sleep(5)  # 5 seconds interval, adjust if needed
except KeyboardInterrupt:
    print("Bot stopped manually")
except Exception as e:
    print("Bot crashed:", e)
