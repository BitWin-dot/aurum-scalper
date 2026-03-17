# indicators/atr.py

class ATR:
    @staticmethod
    def calculate(candles, period=14):
        """
        ATR = Average True Range
        Measures volatility → used for SL & TP
        """

        if len(candles) < period + 1:
            return 0

        true_ranges = []

        for i in range(1, len(candles)):
            high = candles[i]['high']
            low = candles[i]['low']
            prev_close = candles[i - 1]['close']

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )

            true_ranges.append(tr)

        # Take last "period" TR values
        recent_tr = true_ranges[-period:]

        atr = sum(recent_tr) / period

        return atr
