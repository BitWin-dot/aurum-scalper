# main.py
import time
import asyncio

from deriv_api import DerivWS  # WebSocket connection
from trade_executor import TradeExecutor
from trade_manager import TradeManager
from risk_management import RiskManager
from telegram_bot import send_telegram_message
import strategies.confluence as confluence_module  # ✅ import full module instead of non-existent 'confluence'

# Your real tokens
DERIV_API_TOKEN = "gIUrsIg5H56ZNfC"
TELEGRAM_BOT_TOKEN = "8693765411:AAHql2ysRMOhvtgPuNf9JdyE6yfqfEowmjs"
TELEGRAM_CHAT_ID = "-5180694120"

# Bot configuration
SYMBOL = "frxXAUUSD"  # Gold/USD on Deriv
CANDLE_INTERVAL = "1m"

# Initialize core components
ws = DerivWS(DERIV_API_TOKEN)
executor = TradeExecutor()
manager = TradeManager()
risk = RiskManager()

# Send start notification
send_telegram_message(
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    "✅ Aurum Scalper Bot Started"
)

# Subscribe to live candles
ws.subscribe_candles(symbol=SYMBOL, interval=CANDLE_INTERVAL)
print(f"✅ Connected to Deriv WebSocket\nSubscribed to {SYMBOL} {CANDLE_INTERVAL} candles")

# Main async bot loop
async def bot_loop():
    while True:
        try:
            candles = ws.get_latest_candles(SYMBOL, CANDLE_INTERVAL)
            if candles:
                # Run your confluence strategy from the module
                signals = confluence_module.run_confluence_strategy(candles)

                for signal in signals:
                    # Risk checks before executing
                    if risk.is_trade_allowed(signal):
                        executor.execute_trade(signal)
                        manager.record_trade(signal)

            await asyncio.sleep(1)  # non-blocking delay

        except Exception as e:
            print("Bot loop error:", e)
            send_telegram_message(
                TELEGRAM_BOT_TOKEN,
                TELEGRAM_CHAT_ID,
                f"⚠ Bot loop error: {e}"
            )
            await asyncio.sleep(5)  # wait before retrying

# Run bot
asyncio.run(bot_loop())
