# risk_management.py

from indicators.atr import ATR


class RiskManager:

    RISK_PER_TRADE = 0.01  # 1% risk

    @staticmethod
    def calculate_position_size(balance, sl_distance):
        """
        Simple position sizing
        """
        if sl_distance == 0:
            return 0

        risk_amount = balance * RiskManager.RISK_PER_TRADE
        lot_size = risk_amount / sl_distance

        return round(lot_size, 2)

    @staticmethod
    def calculate_sl_tp(candles, entry_price, direction):
        """
        Uses ATR for realistic SL & TP
        """
        atr = ATR.calculate(candles)

        if atr == 0:
            atr = 0.5  # fallback

        if direction == "BUY":
            sl = entry_price - (atr * 1.5)
            tp1 = entry_price + (atr * 2)
            tp2 = entry_price + (atr * 3)

        elif direction == "SELL":
            sl = entry_price + (atr * 1.5)
            tp1 = entry_price - (atr * 2)
            tp2 = entry_price - (atr * 3)

        else:
            return None, None, None

        return sl, tp1, tp2
