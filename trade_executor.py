# trade_executor.py

from deriv_api import DerivWS
from telegram_bot import send_telegram_message  # ✅ fixed import

class TradeExecutor:

    @staticmethod
    def execute(ws: DerivWS, symbol: str, signal: str, lot: float, sl: float, tp1: float, tp2: float):
        """
        Execute a trade on Deriv and send a Telegram notification.
        ws     : Deriv WebSocket object
        symbol : trading symbol, e.g., "frxXAUUSD"
        signal : "BUY" or "SELL"
        lot    : position size
        sl     : stop loss
        tp1    : first take profit
        tp2    : second take profit
        """
        try:
            # Prepare contract parameters
            contract_type = "CALL" if signal == "BUY" else "PUT"

            # Send trade via WebSocket
            ws.buy_contract(
                symbol=symbol,
                contract_type=contract_type,
                amount=lot,
                stop_loss=sl,
                take_profit=[tp1, tp2]
            )

            # Telegram alert
            message = (
                f"💹 Trade Executed:\n"
                f"Signal: {signal}\n"
                f"Symbol: {symbol}\n"
                f"Lot: {lot}\n"
                f"SL: {sl}\n"
                f"TP1: {tp1}, TP2: {tp2}"
            )
            send_telegram_message(message)

        except Exception as e:
            print("Trade execution failed:", e)
            send_telegram_message(f"⚠️ Trade execution failed: {e}")
