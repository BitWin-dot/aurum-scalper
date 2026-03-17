# indicators/vwap.py

class VWAP:
    @staticmethod
    def calculate(candles):
        """
        VWAP = sum(price * volume) / sum(volume)
        price = typical price = (high + low + close) / 3
        """

        total_pv = 0
        total_volume = 0

        for c in candles:
            high = c.get('high', 0)
            low = c.get('low', 0)
            close = c.get('close', 0)
            volume = c.get('volume', 1)  # fallback

            typical_price = (high + low + close) / 3

            total_pv += typical_price * volume
            total_volume += volume

        if total_volume == 0:
            return close

        return total_pv / total_volume
