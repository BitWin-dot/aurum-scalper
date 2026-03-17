# main.py

import time
import traceback

from deriv_api import DerivWS
from filters.session import SessionFilter
from filters.volatility import VolatilityFilter
from filters.spread import SpreadFilter
from risk_management import RiskManager
from trade_executor import TradeExecutor
from trade_manager import TradeManager
from telegram_bot import send_telegram_message
from strategies.confluence import confluence  # ✅ corrected: lowercase


# ================= CONFIG =================
SYMBOL = "frxXAUUSD"
TIMEFRAME = 60  # 1-minute candles
BALANCE = 1000  # adjust if needed
# ==========================================


def run_bot():

    print("🚀 Aurum Scalper Final Bot Started")
    send_telegram_message("🚀 Aurum Scalper Bot is LIVE")

    ws = DerivWS()  # fixed DerivWS initialization (env token inside deriv_api.py)

    ws.connect()
    ws.subscribe_candles(SYMBOL, TIMEFRAME)

    candles = []

    while True:
        try:
            data = ws.get_latest_candle()

            if not data:
                print("Waiting for live candles...")
                time.sleep(1)
                continue

            candles.append(data)

            # Keep only last 100 candles
            if len(candles) > 100:
                candles.pop(0)

            # Need enough data
            if len(candles) < 50:
                continue

            # ================= FILTERS =================
            if not SessionFilter.is_active():
                continue

            if not VolatilityFilter.is_volatile(candles):
                continue

            if not SpreadFilter.is_spread_ok():
                continue
            # ===========================================

            # ================= STRATEGY =================
            signal = confluence.generate_signal(candles)

            if signal not in ["BUY", "SELL"]:
                continue
            # ===========================================

            # ================= TRADE CONTROL ============
            if not TradeManager.can_trade():
                continue
            # ===========================================

            entry_price = candles[-1]['close']

            sl, tp1, tp2 = RiskManager.calculate_sl_tp(
                candles, entry_price, signal
            )

            sl_distance = abs(entry_price - sl)

            lot = RiskManager.calculate_position_size(
                BALANCE, sl_distance
            )

            if lot <= 0:
                continue

            # ================= EXECUTE ==================
            TradeExecutor.execute(
                ws,
                SYMBOL,
                signal,
                lot,
                sl,
                tp1,
                tp2
            )

            TradeManager.open_trade()
            # ===========================================

            time.sleep(5)  # prevent overtrading

        except Exception as e:
            print("ERROR:", e)
            traceback.print_exc()

            send_telegram_message(f"⚠️ Bot Error: {str(e)}")

            time.sleep(5)


# ================= RUN FOREVER =================
while True:
    try:
        run_bot()
    except Exception as e:
        print("CRASH RESTART:", e)
        time.sleep(5)
