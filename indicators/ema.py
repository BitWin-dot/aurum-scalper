# indicators/ema.py

class EMA:
    @staticmethod
    def calculate(candles, period=50):
        if len(candles) < period:
            return candles[-1]['close']

        multiplier = 2 / (period + 1)

        ema = candles[-period]['close']

        for c in candles[-period + 1:]:
            price = c['close']
            ema = (price - ema) * multiplier + ema

        return ema
