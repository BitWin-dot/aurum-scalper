# main.py
import json
from deriv_api import DerivWS
from strategies.liquidity_vwap import calculate_score

# Placeholder indicators
def compute_vwap(candle):
    return (candle["high"] + candle["low"] + candle["close"]) / 3

def compute_rsi(candle):
    return 55  # placeholder

# Handle each new candle
def handle_new_candle(candle):
    candle_data = {
        "open": candle["open"],
        "high": candle["high"],
        "low": candle["low"],
        "close": candle["close"],
        "volume": candle.get("volume", 0)
    }

    vwap = compute_vwap(candle_data)
    rsi = compute_rsi(candle_data)

    score = calculate_score(candle_data, vwap, rsi)

    if score >= 3:
        print(f"🚀 Trade Signal Detected! Score: {score} | Close:{candle['close']} High:{candle['high']} Low:{candle['low']}")

def start_bot():
    ws_client = DerivWS()
    ws_client.candle_handler = handle_new_candle  # attach handler

    print("🚀 Aurum Scalper Bot Starting...")
    ws_client.start()

if __name__ == "__main__":
    start_bot()
