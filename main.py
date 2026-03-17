# main.py - Aurum Scalper Production (Live Candles + Real VWAP & RSI)
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

# --- Global lists to track candles for VWAP and RSI ---
candle_window = []  # store last 20 candles
close_prices = []   # store last 14 closes for RSI

VWAP_PERIOD = 20
RSI_PERIOD = 14

def compute_vwap(candles):
    """
    Compute VWAP from a list of candles.
    VWAP = sum(price*volume)/sum(volume)
    """
    total_vp = 0
    total_volume = 0
    for c in candles:
        typical_price = (c["high"] + c["low"] + c["close"]) / 3
        total_vp += typical_price * c.get("volume", 1)
        total_volume += c.get("volume", 1)
    return total_vp / total_volume if total_volume != 0 else 0

def compute_rsi(prices, period=14):
    """
    Compute RSI(14) from list of closes
    """
    if len(prices) < period + 1:
        return 50  # neutral until enough data
    gains, losses = 0, 0
    for i in range(-period, -1):
        delta = prices[i+1] - prices[i]
        if delta > 0:
            gains += delta
        else:
            losses += abs(delta)
    if losses == 0:
        return 100
    rs = gains / losses
    rsi = 100 - (100 / (1 + rs))
    return rsi

def handle_new_candle(candle):
    """
    Process new live Deriv candle with real VWAP & RSI
    """
    global candle_window, close_prices

    candle_data = {
        "open": candle["open"],
        "high": candle["high"],
        "low": candle["low"],
        "close": candle["close"],
        "volume": candle.get("volume", 0),
        "prev_high": candle.get("prev_high", candle["high"] - 5),
        "prev_low": candle.get("prev_low", candle["low"] + 5)
    }

    # Update candle window
    candle_window.append(candle_data)
    if len(candle_window) > VWAP_PERIOD:
        candle_window.pop(0)

    # Update close prices for RSI
    close_prices.append(candle_data["close"])
    if len(close_prices) > RSI_PERIOD + 1:
        close_prices.pop(0)

    vwap = compute_vwap(candle_window)
    rsi = compute_rsi(close_prices, RSI_PERIOD)

    score = calculate_score(candle_data, vwap, rsi)

    if score >= 3:
        msg = f"🚀 Trade Signal! Score: {score} | Close:{candle['close']} High:{candle['high']} Low:{candle['low']} | VWAP:{vwap:.2f} RSI:{rsi:.2f}"
        print(msg)
        send_telegram(f"Aurum Scalper Live: {msg}")

def start_bot():
    ws_client = DerivWS()
    ws_client.candle_handler = handle_new_candle
    print("🚀 Aurum Scalper Bot Starting with Real VWAP & RSI...")
    ws_client.start()

if __name__ == "__main__":
    start_bot()
