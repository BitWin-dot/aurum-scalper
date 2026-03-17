# strategies/session_breakout.py
from indicators.rsi import RSI
from indicators.volume import VolumeSpike

class SessionBreakoutStrategy:
    """
    Strategy 3: Session Breakout (London / New York)
    Trades breakout of recent range with momentum confirmation
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

        # === 1. Define Range (last 15 candles) ===
        range_high = max(c['high'] for c in self.candles[-15:])
        range_low = min(c['low'] for c in self.candles[-15:])

        # === 2. Breakout Detection ===
        breakout_up = last['close'] > range_high
        breakout_down = last['close'] < range_low

        if breakout_up or breakout_down:
            score += 1
        else:
            return {'score': score, 'signal': None, 'sl': None, 'tp1': None, 'tp2': None}

        # === 3. Strong Breakout Candle ===
        body = abs(last['close'] - last['open'])
        rng = last['high'] - last['low']

        if rng == 0:
            return {'score': score, 'signal': None, 'sl': None, 'tp1': None, 'tp2': None}

        if body / rng >= 0.6:
            score += 1

        # === 4. RSI Momentum Confirmation ===
        rsi = RSI.calculate(self.candles)

        if breakout_up and rsi > 55:
            score += 1
            signal = "BUY"
        elif breakout_down and rsi < 45:
            score += 1
            signal = "SELL"
        else:
            signal = None

        # === 5. Volume Spike Confirmation ===
        if VolumeSpike.detect(self.candles):
            score += 1

        # === Only trade if score >= 3 ===
        if score < 3:
            signal = None

        # === SL / TP ===
        if signal == "BUY":
            sl = range_low - 0.01
            risk = last['close'] - sl
            tp1 = last['close'] + risk * 1
            tp2 = last['close'] + risk * 2

        elif signal == "SELL":
            sl = range_high + 0.01
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
