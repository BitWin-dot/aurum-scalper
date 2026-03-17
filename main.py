# main.py - Aurum Scalper Production (Live Deriv Candles)
import json
from deriv_api import DerivWS
from strategies.liquidity_vwap import calculate_score
import requests

# --- Telegram Config ---
TELEGRAM_BOT_TOKEN = "8693765411:AAHql2ysRMOhvtgPuNf9JdyE6yfqfEowmjs"
TELEGRAM_CHAT_ID = "-5180694120"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram send error:", e)

# Placeholder indicators (replace with real VWAP & RSI later)
def compute_vwap(candle):
    return (candle["high"] + candle["low"] + candle["close"]) / 3

def compute_rsi(candle):
    return 55  # placeholder

def handle_new_candle(candle):
    """
    Process new live Deriv candle and check Liquidity Sweep + VWAP strategy
    """
    candle_data = {
        "open": candle["open"],
        "high": candle["high"],
        "low": candle["low"],
        "close": candle["close"],
        "volume": candle.get("volume", 0),
        "prev_high": candle.get("prev_high", candle["high"] - 5),
        "prev_low": candle.get("prev_low", candle["low"] + 5)
    }

    vwap = compute_vwap(candle_data)
    rsi = compute_rsi(candle_data)
    score = calculate_score(candle_data, vwap, rsi)

    if score >= 3:
        msg = f"🚀 Trade Signal! Score: {score} | Close:{candle['close']} High:{candle['high']} Low:{candle['low']}"
        print(msg)
        send_telegram(f"Aurum Scalper Live: {msg}")

def start_bot():
    ws_client = DerivWS()
    ws_client.candle_handler = handle_new_candle
    print("🚀 Aurum Scalper Bot Starting with Live Deriv Candles...")
    ws_client.start()

if __name__ == "__main__":
    start_bot()
