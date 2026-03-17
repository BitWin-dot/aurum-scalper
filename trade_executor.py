# trade_executor.py

from telegram import send_telegram_message


class TradeExecutor:

    @staticmethod
    def execute(ws, symbol, direction, lot, sl, tp1, tp2):
        """
        Executes trade using Deriv WebSocket
        """

        try:
            contract_type = "CALL" if direction == "BUY" else "PUT"

            proposal = {
                "proposal": 1,
                "amount": lot,
                "basis": "stake",
                "contract_type": contract_type,
                "currency": "USD",
                "duration": 1,
                "duration_unit": "m",
                "symbol": symbol
            }

            ws.send(proposal)

            send_telegram_message(
                f"""
🚀 Trade Executed
Symbol: {symbol}
Direction: {direction}
Lot: {lot}

SL: {sl}
TP1: {tp1}
TP2: {tp2}
"""
            )

            print("Trade executed successfully")

        except Exception as e:
            print("Execution error:", e)
