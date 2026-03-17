# main.py - Aurum Scalper Fully Live Trading with Deriv
import time
import requests
from datetime import datetime, timezone
from deriv_api import DerivWS, buy_contract  # buy_contract added for live execution
from strategies.liquidity_vwap import calculate_score

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

# --- Deriv Config ---
DERIV_API_TOKEN = "gIUrsIg5H56ZNfC"
SYMBOL = "frxXAUUSD"

# --- Trade Settings ---
RISK_PERCENT = 1.0
TP_MULTIPLIER_1 = 1.0
TP_MULTIPLIER_2 = 2.0
MAX_CONSECUTIVE_LOSSES = 3
DAILY_DRAWDOWN_LIMIT = 5.0
MAX_TRADES_PER_SESSION = 10
MAX_SPREAD = 2.0
MIN_ATR = 5.0
TRADES_PER_HOUR_LIMIT = 3

# --- Globals ---
open_trades = []
consecutive_losses = 0
daily_drawdown = 0
session_trade_count = 0
hourly_trade_count = {}
last_hour = datetime.now().hour

# --- Candle tracking ---
VWAP_PERIOD = 20
RSI_PERIOD = 14
ATR_PERIOD = 14
candle_window = []
close_prices = []

# --- Indicators ---
def compute_vwap(candles):
    total_vp, total_volume = 0, 0
    for c in candles:
        typical_price = (c["high"] + c["low"] + c["close"]) / 3
        total_vp += typical_price * c.get("volume", 1)
        total_volume += c.get("volume", 1)
    return total_vp / total_volume if total_volume else 0

def compute_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50
    gains, losses = 0,0
    for i in range(-period,-1):
        delta = prices[i+1] - prices[i]
        if delta>0: gains += delta
        else: losses += abs(delta)
    if losses == 0: return 100
    rs = gains / losses
    return 100 - (100/(1+rs))

def compute_atr(candles, period=14):
    if len(candles) < period+1: return 0
    trs = []
    for i in range(-period,0):
        high, low, prev_close = candles[i]["high"], candles[i]["low"], candles[i-1]["close"]
        trs.append(max(high-low, abs(high-prev_close), abs(low-prev_close)))
    return sum(trs)/len(trs)

# --- Lot sizing ---
def calculate_lot_size(account_balance, entry, stop_loss):
    risk_amount = account_balance * (RISK_PERCENT/100)
    distance = abs(entry - stop_loss)
    if distance==0: return 0.01
    return max(0.01, round(risk_amount/distance,2))

# --- Trade Execution ---
def execute_trade(direction, entry_price, sl, tp1, tp2, lot_size):
    global session_trade_count, hourly_trade_count, last_hour

    now_hour = datetime.now().hour
    if now_hour != last_hour:
        hourly_trade_count[now_hour] = 0
        last_hour = now_hour
    hourly_trade_count[now_hour] = hourly_trade_count.get(now_hour,0)+1
    if hourly_trade_count[now_hour] > TRADES_PER_HOUR_LIMIT:
        print("Hourly trade limit reached, skipping trade.")
        return

    # --- Place live Deriv contract ---
    contract_type = "CALL" if direction=="BUY" else "PUT"
    try:
        result = buy_contract(DERIV_API_TOKEN, SYMBOL, lot_size, contract_type, duration=5, duration_unit="t") 
        print("Deriv Contract Result:", result)
    except Exception as e:
        print("Deriv trade error:", e)
        return

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
    session_trade_count += 1

    msg = (
        f"TRADE OPENED\nDirection: {direction}\nEntry: {entry_price}\n"
        f"SL: {sl}\nTP1: {tp1}\nTP2: {tp2}\nLot: {lot_size}\nRisk: {RISK_PERCENT}%"
    )
    print(msg)
    send_telegram(f"Aurum Scalper Live: {msg}")

# --- Manage Open Trades ---
def check_open_trades(current_price):
    global open_trades
    for trade in open_trades[:]:
        if trade["status"]=="open":
            if (trade["direction"]=="BUY" and current_price>=trade["tp1"]) or \
               (trade["direction"]=="SELL" and current_price<=trade["tp1"]):
                trade["status"]="tp1_done"
                send_telegram(f"Partial TP hit (50%) at {trade['tp1']}")
        if trade["status"]=="tp1_done":
            if (trade["direction"]=="BUY" and current_price>=trade["tp2"]) or \
               (trade["direction"]=="SELL" and current_price<=trade["tp2"]):
                trade["status"]="closed"
                send_telegram(f"Final TP hit at {trade['tp2']} - Trade Closed")
                open_trades.remove(trade)

# --- Session Filter ---
def is_london_ny_session():
    utc_hour = datetime.utcnow().hour
    return (7<=utc_hour<=16)  # London+NY overlap approx

# --- Candle Handler ---
def handle_new_candle(candle, account_balance=10000, spread=1.0):
    global candle_window, close_prices, session_trade_count

    candle_data = {"open":candle["open"],"high":candle["high"],"low":candle["low"],"close":candle["close"],"volume":candle.get("volume",0)}
    candle_window.append(candle_data)
    if len(candle_window)>VWAP_PERIOD:
        candle_window.pop(0)
    close_prices.append(candle_data["close"])
    if len(close_prices)>RSI_PERIOD+1:
        close_prices.pop(0)

    vwap = compute_vwap(candle_window)
    rsi = compute_rsi(close_prices, RSI_PERIOD)
    atr = compute_atr(candle_window, ATR_PERIOD)
    score = calculate_score(candle_data,vwap,rsi)

    if not is_london_ny_session(): return
    if spread>MAX_SPREAD or atr<MIN_ATR: return
    check_open_trades(candle_data["close"])

    if score>=3 and session_trade_count<MAX_TRADES_PER_SESSION:
        direction="BUY" if candle_data["close"]>vwap else "SELL"
        stop_loss = candle_data["low"]-10 if direction=="BUY" else candle_data["high"]+10
        tp1 = candle_data["close"] + TP_MULTIPLIER_1*abs(candle_data["close"]-stop_loss) if direction=="BUY" else candle_data["close"] - TP_MULTIPLIER_1*abs(candle_data["close"]-stop_loss)
        tp2 = candle_data["close"] + TP_MULTIPLIER_2*abs(candle_data["close"]-stop_loss) if direction=="BUY" else candle_data["close"] - TP_MULTIPLIER_2*abs(candle_data["close"]-stop_loss)
        lot_size = calculate_lot_size(account_balance, candle_data["close"], stop_loss)
        execute_trade(direction, candle_data["close"], stop_loss, tp1, tp2, lot_size)

# --- Start Bot ---
def start_bot():
    ws_client = DerivWS()
    ws_client.candle_handler = handle_new_candle
    print("🚀 Aurum Scalper Fully Live Trading Starting...")
    ws_client.start()

if __name__=="__main__":
    start_bot()
