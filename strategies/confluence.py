# strategies/confluence.py

class ConfluenceEngine:
    """
    Combines all strategies and selects the best trade
    """

    @staticmethod
    def decide(strategies_results):
        """
        strategies_results: list of dicts from strategies
        Each dict format:
        {
            'score': int,
            'signal': 'BUY' or 'SELL' or None,
            'sl': float,
            'tp1': float,
            'tp2': float
        }
        """

        best_trade = None
        highest_score = 0

        buy_count = 0
        sell_count = 0

        # Count signals
        for result in strategies_results:
            if result['signal'] == 'BUY':
                buy_count += 1
            elif result['signal'] == 'SELL':
                sell_count += 1

        # === Avoid conflicting signals ===
        if buy_count > 0 and sell_count > 0:
            return None  # conflict → no trade

        # === Find best scoring strategy ===
        for result in strategies_results:
            if result['signal'] is not None and result['score'] > highest_score:
                highest_score = result['score']
                best_trade = result

        # === Final filter ===
        if best_trade and highest_score >= 3:
            return best_trade

        return None
