# liquidity_vwap.py

def calculate_score(candle, vwap, rsi):
    """
    Calculates the Liquidity Sweep + VWAP score based on your 5-point scoring system.
    Returns an integer score (0–5)
    """

    score = 0

    # 1️⃣ Liquidity sweep: check if candle wick exceeds previous high/low
    if "prev_high" in candle and candle["high"] > candle["prev_high"]:
        score += 1
    elif "prev_low" in candle and candle["low"] < candle["prev_low"]:
        score += 1

    # 2️⃣ Strong displacement candle
    body = abs(candle["close"] - candle["open"])
    range_ = candle["high"] - candle["low"]
    if range_ > 1.5 * body:
        score += 1

    # 3️⃣ Price reclaims VWAP
    if candle["close"] > vwap:
        score += 1  # bullish reclaim
    elif candle["close"] < vwap:
        score += 1  # bearish reclaim

    # 4️⃣ RSI confirmation
    if rsi > 50 and candle["close"] > vwap:
        score += 1
    elif rsi < 50 and candle["close"] < vwap:
        score += 1

    # 5️⃣ Volume spike
    if "volume" in candle and candle["volume"] > 1000:  # placeholder threshold
        score += 1

    return score
