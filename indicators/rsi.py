# indicators/rsi.py

class RSI:
    @staticmethod
    def calculate(candles, period=14):
        if len(candles) < period + 1:
            return 50  # neutral fallback

        gains = 0
        losses = 0

        for i in range(-period, 0):
            change = candles[i]['close'] - candles[i - 1]['close']

            if change > 0:
                gains += change
            else:
                losses -= change

        if losses == 0:
            return 100

        rs = gains / losses
        rsi = 100 - (100 / (1 + rs))

        return rsi
