# strategies/trend_pullback.py
from indicators.ema import EMA
from indicators.rsi import RSI
from indicators.volume import VolumeSpike

class TrendPullbackStrategy:
    """
    Strategy 2: Trend Pullback Continuation
    Uses EMA trend + pullback + RSI + volume confirmation
    Trade only when score >= 3
    """

    def __init__(self, candles):
        self.candles = candles

    def calculate_score(self):
        score = 0
        signal = None
        sl = None
        tp1 = None
        tp2 = None

        if len(self.candles) < 20:
            return {'score': 0, 'signal': None, 'sl': None, 'tp1': None, 'tp2': None}

        last = self.candles[-1]

        # === 1. Trend Direction (EMA 50) ===
        ema_50 = EMA.calculate(self.candles, period=50)

        if last['close'] > ema_50:
            trend = "UP"
            score += 1
        elif last['close'] < ema_50:
            trend = "DOWN"
            score += 1
        else:
            return {'score': score, 'signal': None, 'sl': None, 'tp1': None, 'tp2': None}

        # === 2. Pullback to EMA zone ===
        # Check if recent candles touched EMA area
        pullback = False
        for c in self.candles[-5:]:
            if abs(c['close'] - ema_50) < 0.2:  # tolerance zone
                pullback = True
                break

        if pullback:
            score += 1
        else:
            return {'score': score, 'signal': None, 'sl': None, 'tp1': None, 'tp2': None}

        # === 3. Rejection / Continuation Candle ===
        body = abs(last['close'] - last['open'])
        rng = last['high'] - last['low']

        if rng == 0:
            return {'score': score, 'signal': None, 'sl': None, 'tp1': None, 'tp2': None}

        if body / rng >= 0.6:
            score += 1

        # === 4. RSI Confirmation ===
        rsi = RSI.calculate(self.candles)

        if trend == "UP" and rsi > 50:
            score += 1
            signal = "BUY"
        elif trend == "DOWN" and rsi < 50:
            score += 1
            signal = "SELL"
        else:
            signal = None

        # === 5. Volume Confirmation ===
        if VolumeSpike.detect(self.candles):
            score += 1

        # === Only trade if score >= 3 ===
        if score < 3:
            signal = None

        # === SL / TP ===
        if signal == "BUY":
            sl = min(c['low'] for c in self.candles[-5:]) - 0.01
            risk = last['close'] - sl
            tp1 = last['close'] + risk * 1
            tp2 = last['close'] + risk * 2

        elif signal == "SELL":
            sl = max(c['high'] for c in self.candles[-5:]) + 0.01
            risk = sl - last['close']
            tp1 = last['close'] - risk * 1
            tp2 = last['close'] - risk * 2

        return {
            'score': score,
            'signal': signal,
            'sl': sl,
            'tp1': tp1,
            'tp2': tp2
      }
