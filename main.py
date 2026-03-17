# main.py - Aurum Scalper Real Trading (Deriv)
import json
import time
import requests
from deriv_api import DerivWS

# --- Telegram Config ---
TELEGRAM_BOT_TOKEN = "8693765411:AAHql2ysRMOhvtgPuNf9JdyE6yfqfEowmjs"
TELEGRAM_CHAT_ID = "-5180694120"

# --- Trade Settings ---
RISK_PERCENT = 1.0  # risk 1% of account balance per trade
TP_MULTIPLIER_1 = 1.0  # 1R
TP_MULTIPLIER_2 = 2.0  # 2R
MAX_CONSECUTIVE_LOSSES = 3
DAILY_DRAWDOWN_LIMIT = 5.0  # percent
MAX_TRADES_PER_SESSION = 10

# --- Globals ---
open_trades = []
consecutive_losses = 0
daily_drawdown = 0
session_trade_count = 0

# --- Candle tracking for VWAP/RSI ---
VWAP_PERIOD = 20
RSI_PERIOD = 14
candle_window = []
close_prices = []

# --- Strategy import ---
from strategies.liquidity_vwap import calculate_score

# --- Telegram helper ---
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram send error:", e)

# --- Indicator calculations ---
def compute_vwap(candles):
    total_vp = 0
    total_volume = 0
    for c in candles:
        typical_price = (c["high"] + c["low"] + c["close"]) / 3
        total_vp += typical_price * c.get("volume", 1)
        total_volume += c.get("volume", 1)
    return total_vp / total_volume if total_volume != 0 else 0

def compute_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50
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

# --- Trade execution via Deriv API ---
def execute_trade(direction, entry_price, sl, tp1, tp2, lot_size):
    trade = {
        "direction": direction,
        "entry": entry_price,
        "sl": sl,
        "tp1": tp1,
        "tp2": tp2,
        "lot": lot_size,
        "status": "open"
    }
    open_trades.append(trade)

    msg = f"TRADE OPENED\nDirection: {direction}\nEntry: {entry_price}\nSL: {sl}\nTP1: {tp1}\nTP2: {tp2}\nLot: {lot_size}"
    print(msg)
    send_telegram(f"Aurum Scalper Live: {msg}")

# --- Handle new candle ---
def handle_new_candle(candle):
    global candle_window, close_prices, session_trade_count, consecutive_losses, daily_drawdown

    # Update candle window & close prices
    candle_data = {
        "open": candle["open"],
        "high": candle["high"],
        "low": candle["low"],
        "close": candle["close"],
        "volume": candle.get("volume", 0),
        "prev_high": candle.get("prev_high", candle["high"] - 5),
        "prev_low": candle.get("prev_low", candle["low"] + 5)
    }

    candle_window.append(candle_data)
    if len(candle_window) > VWAP_PERIOD:
        candle_window.pop(0)

    close_prices.append(candle_data["close"])
    if len(close_prices) > RSI_PERIOD + 1:
        close_prices.pop(0)

    # Compute indicators
    vwap = compute_vwap(candle_window)
    rsi = compute_rsi(close_prices, RSI_PERIOD)

    # Calculate score
    score = calculate_score(candle_data, vwap, rsi)

    # Risk / trade filters
    if score >= 3 and session_trade_count < MAX_TRADES_PER_SESSION:
        # Example placeholders for SL / TP / Lot size
        direction = "BUY" if candle_data["close"] > vwap else "SELL"
        stop_loss = candle_data["low"] - 10 if direction == "BUY" else candle_data["high"] + 10
        tp1 = candle_data["close"] + TP_MULTIPLIER_1 * abs(candle_data["close"] - stop_loss) if direction == "BUY" else candle_data["close"] - TP_MULTIPLIER_1 * abs(candle_data["close"] - stop_loss)
        tp2 = candle_data["close"] + TP_MULTIPLIER_2 * abs(candle_data["close"] - stop_loss) if direction == "BUY" else candle_data["close"] - TP_MULTIPLIER_2 * abs(candle_data["close"] - stop_loss)
        lot_size = 0.01  # placeholder, implement dynamic lot sizing later

        execute_trade(direction, candle_data["close"], stop_loss, tp1, tp2, lot_size)
        session_trade_count += 1

# --- Start Bot ---
def start_bot():
    ws_client = DerivWS()
    ws_client.candle_handler = handle_new_candle
    print("🚀 Aurum Scalper Real Trading Bot Starting...")
    ws_client.start()

if __name__ == "__main__":
    start_bot()
