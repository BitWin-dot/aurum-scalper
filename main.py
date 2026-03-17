# main.py (Fast Test Mode for Railway)
import time
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

# Placeholder VWAP & RSI
def compute_vwap(candle):
    return (candle["high"] + candle["low"] + candle["close"]) / 3

def compute_rsi(candle):
    return 55  # placeholder

def handle_new_candle(candle):
    vwap = compute_vwap(candle)
    rsi = compute_rsi(candle)
    score = calculate_score(candle, vwap, rsi)
    if score >= 3:
        msg = f"🚀 Trade Signal! Score: {score} | Close:{candle['close']} High:{candle['high']} Low:{candle['low']}"
        print(msg)
        send_telegram(f"Aurum Scalper Test Message: {msg}")

if __name__ == "__main__":
    print("🚀 Aurum Scalper Bot Fast-Test Mode Starting...")

    # Simulate 5 candles instantly
    for i in range(5):
        fake_candle = {
            "open": 5000,
            "high": 5010,
            "low": 4995,
            "close": 5005,
            "volume": 1500,
            "prev_high": 5008,
            "prev_low": 4998
        }
        handle_new_candle(fake_candle)
        time.sleep(1)  # 1 second between simulated candles

    print("✅ Fast Test Complete")
