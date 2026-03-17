# main.py

import time
from deriv_api import DerivWS
from trade_executor import TradeExecutor
from trade_manager import TradeManager
from telegram_bot import send_telegram_message
from strategies.confluence import confluence  # ✅ matches your structure

# -------------------------------
# CONFIG
# -------------------------------
DERIV_API_TOKEN = "gIUrsIg5H56ZNfC"
SYMBOL = "frxXAUUSD"
LOT_SIZE = 1.0
SL = 10  # example stop loss
TP1 = 20  # example take profit 1
TP2 = 40  # example take profit 2
CANDLE_INTERVAL = "1m"

# -------------------------------
# INITIALIZE WEBSOCKET
# -------------------------------
try:
    ws = DerivWS(DERIV_API_TOKEN)
    print("✅ Connected to Deriv WebSocket")
except Exception as e:
    print("❌ WebSocket connection failed:", e)
    send_telegram_message(f"❌ WebSocket connection failed: {e}")
    exit(1)

# -------------------------------
# SUBSCRIBE TO LIVE CANDLES
# -------------------------------
try:
    ws.subscribe_candles(symbol=SYMBOL, interval=CANDLE_INTERVAL)
    print(f"Subscribed to {SYMBOL} {CANDLE_INTERVAL} candles")
except Exception as e:
    print("❌ Candle subscription failed:", e)
    send_telegram_message(f"❌ Candle subscription failed: {e}")
    exit(1)

# -------------------------------
# INITIALIZE TRADE MANAGER
# -------------------------------
trade_manager = TradeManager(ws, TradeExecutor)

# -------------------------------
# BOT LOOP
# -------------------------------
print("🚀 Aurum Scalper Bot Started")
send_telegram_message("🚀 Aurum Scalper Bot Started")

while True:
    try:
        # Get the latest candles
        candles = ws.get_latest_candles(SYMBOL, interval=CANDLE_INTERVAL, count=10)
        if not candles:
            time.sleep(1)
            continue

        # Generate signal from confluence strategy
        signal = confluence.generate_signal(candles)
        if signal:
            print(f"Signal detected: {signal}")
            trade_manager.manage_trade(
                symbol=SYMBOL,
                signal=signal,
                lot=LOT_SIZE,
                sl=SL,
                tp1=TP1,
                tp2=TP2
            )

        time.sleep(1)  # 1 second loop for minimal latency

    except Exception as e:
        print("⚠️ Bot loop error:", e)
        send_telegram_message(f"⚠️ Bot loop error: {e}")
        time.sleep(5)
