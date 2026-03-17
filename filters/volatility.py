# filters/volatility.py

from indicators.atr import ATR


class VolatilityFilter:
    @staticmethod
    def is_volatile(candles, min_atr=0.2):
        """
        Ensure market has enough movement
        """
        atr = ATR.calculate(candles)

        if atr < min_atr:
            return False

        return True
