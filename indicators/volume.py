# indicators/volume.py

class VolumeSpike:
    @staticmethod
    def detect(candles, lookback=10, multiplier=1.5):
        if len(candles) < lookback + 1:
            return False

        volumes = [c.get('volume', 1) for c in candles[-lookback - 1:-1]]
        avg_volume = sum(volumes) / len(volumes)

        current_volume = candles[-1].get('volume', 1)

        return current_volume > avg_volume * multiplier
