# main.py
import json
import threading
from deriv_api import DerivWS
from strategies.liquidity_vwap import calculate_score

# Placeholder indicators
def compute_vwap(candle):
    # Replace with real VWAP calculation later
    return (candle["high"] + candle["low"] + candle["close"]) / 3

def compute_rsi(candle):
    # Replace with real RSI calculation later
    return 55  # placeholder

# Handle each new candle
def handle_new_candle(candle):
    """
    Process a new candle and check Liquidity Sweep + VWAP strategy
    """
    candle_data = {
        "open": candle["open"],
        "high": candle["high"],
        "low": candle["low"],
        "close": candle["close"],
        "volume": candle.get("volume", 0)
    }

    # Compute indicators
    vwap = compute_vwap(candle_data)
    rsi = compute_rsi(candle_data)

    # Calculate score
    score = calculate_score(candle_data, vwap, rsi)

    if score >= 3:
        print(f"🚀 Trade Signal Detected! Score: {score} | Close:{candle['close']} High:{candle['high']} Low:{candle['low']}")

# Start Deriv WebSocket in a separate thread
def start_bot():
    ws_client = DerivWS()

    # Patch ws_client to call handle_new_candle instead of printing full candles
    original_on_message = ws_client.on_message

    def new_on_message(ws, message):
        data = json.loads(message)
        if "candles" in data:
            latest = data["candles"][-1]
            handle_new_candle(latest)  # send to strategy
        if "error" in data:
            print("Deriv error:", data["error"])
    ws_client.on_message = new_on_message

    ws_client.start()

# Run bot
if __name__ == "__main__":
    print("🚀 Aurum Scalper Bot Starting...")
    threading.Thread(target=start_bot).start()
