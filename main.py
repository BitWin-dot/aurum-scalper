# main.py

import time
import threading
from config import DERIV_API_TOKEN, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, SYMBOL, CANDLE_INTERVAL
from deriv_api import DerivWS
from trade_executor import TradeExecutor
from trade_manager import TradeManager
from risk_management import RiskManager
from telegram_bot import send_telegram_message
from logger import Logger

# Import all strategies
from strategies.confluence import Confluence
from strategies.breakout import Breakout
from strategies.liquidity_vwap import LiquidityVWAP
from strategies.trend_pullback import TrendPullback

# ------------------------
# Initialize logger
# ------------------------
logger = Logger()

# ------------------------
# Initialize Telegram
# ------------------------
def notify_startup():
    try:
        send_telegram_message(f"✅ Aurum Scalper Bot Started")
    except Exception as e:
        logger.error(f"Telegram notification failed: {e}")

notify_startup()

# ------------------------
# Initialize WebSocket
# ------------------------
ws = DerivWS(DERIV_API_TOKEN)

def connect_ws():
    connected = ws.connect()
    if not connected:
        logger.error("WebSocket connection failed")
        raise RuntimeError("Could not connect to Deriv WebSocket")
    logger.info("Connected to Deriv WebSocket")

connect_ws()

# ------------------------
# Subscribe to candles
# ------------------------
try:
    ws.subscribe_candles(SYMBOL, CANDLE_INTERVAL)
    logger.info(f"Subscribed to {SYMBOL} {CANDLE_INTERVAL} candles")
except Exception as e:
    logger.error(f"Failed to subscribe candles: {e}")
    raise

# ------------------------
# Initialize Risk Manager, Trade Manager, Executor
# ------------------------
risk_manager = RiskManager()
trade_executor = TradeExecutor(ws)
trade_manager = TradeManager(trade_executor, risk_manager)

# ------------------------
# Initialize Strategies
# ------------------------
strategies = [
    Confluence(),
    Breakout(),
    LiquidityVWAP(),
    TrendPullback()
]

# ------------------------
# Main Loop
# ------------------------
def main_loop():
    logger.info("Starting main trading loop...")
    while True:
        try:
            candle = ws.get_latest_candle(SYMBOL)
            if candle is None:
                time.sleep(1)
                continue

            # Run each strategy on latest candle
            for strategy in strategies:
                signal = strategy.generate_signal(candle)
                if signal:
                    trade_manager.handle_signal(signal)

            # Optional: small sleep to reduce CPU usage
            time.sleep(0.5)

        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            try:
                send_telegram_message(f"⚠️ Bot Error: {e}")
            except Exception as tg_e:
                logger.error(f"Failed to send Telegram error: {tg_e}")
            time.sleep(5)

# Run main loop in separate thread to allow async tasks
thread = threading.Thread(target=main_loop)
thread.start()
