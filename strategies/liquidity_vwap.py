# strategies/liquidity_vwap.py
from indicators.vwap import VWAP
from indicators.rsi import RSI
from indicators.volume import VolumeSpike

class LiquidityVWAPStrategy:
    """
    Strategy 1: Liquidity Sweep + VWAP Reversal
    Confluence scoring: enter trade if score >= 3
    """

    def __init__(self, candles):
        """
        candles: list of recent candles in format [{'open':..., 'high':..., 'low':..., 'close':..., 'volume':...}, ...]
        """
        self.candles = candles

    def calculate_score(self):
        """
        Returns a dict: {'score': int, 'signal': 'BUY'/'SELL'/None, 'sl': float, 'tp1': float, 'tp2': float}
        """
        score = 0
        signal = None
        sl = None
        tp1 = None
        tp2 = None

        if len(self.candles) < 5:
            return {'score': score, 'signal': None, 'sl': None, 'tp1': None, 'tp2': None}

        last_candle = self.candles[-1]
        prev_candle = self.candles[-2]

        # === 1. Liquidity Sweep ===
        equal_highs = max(c['high'] for c in self.candles[-5:])
        equal_lows = min(c['low'] for c in self.candles[-5:])
        sweep_buy = last_candle['low'] < equal_lows
        sweep_sell = last_candle['high'] > equal_highs
        if sweep_buy or sweep_sell:
            score += 1

        # === 2. Strong Displacement Candle ===
        body_size = abs(last_candle['close'] - last_candle['open'])
        candle_range = last_candle['high'] - last_candle['low']
        if candle_range == 0:
            return {'score': score, 'signal': None, 'sl': None, 'tp1': None, 'tp2': None}
        if body_size / candle_range >= 0.6:
            score += 1

        # === 3. VWAP Reclaim ===
        vwap_val = VWAP.calculate(self.candles)
        if last_candle['close'] > vwap_val:
            score += 1
            signal = 'BUY'
        elif last_candle['close'] < vwap_val:
            score += 1
            signal = 'SELL'

        # === 4. RSI Confirmation ===
        rsi_val = RSI.calculate(self.candles)
        if signal == 'BUY' and rsi_val > 50:
            score += 1
        elif signal == 'SELL' and rsi_val < 50:
            score += 1
        else:
            signal = None  # cancel if RSI disagrees

        # === 5. Volume Spike ===
        if VolumeSpike.detect(self.candles):
            score += 1

        # === Entry only if score >=3 ===
        if score < 3:
            signal = None

        # === Stop Loss & Take Profit ===
        if signal == 'BUY':
            sl = min(c['low'] for c in self.candles[-5:]) - 0.01
            tp1 = last_candle['close'] + (last_candle['close'] - sl) * 1  # 1R
            tp2 = last_candle['close'] + (last_candle['close'] - sl) * 2  # 2R
        elif signal == 'SELL':
            sl = max(c['high'] for c in self.candles[-5:]) + 0.01
            tp1 = last_candle['close'] - (sl - last_candle['close']) * 1
            tp2 = last_candle['close'] - (sl - last_candle['close']) * 2

        return {'score': score, 'signal': signal, 'sl': sl, 'tp1': tp1, 'tp2': tp2}
