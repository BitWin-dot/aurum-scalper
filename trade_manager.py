# trade_manager.py

class TradeManager:

    active_trade = False

    @staticmethod
    def can_trade():
        """
        Prevent multiple trades at once
        """
        return not TradeManager.active_trade

    @staticmethod
    def open_trade():
        TradeManager.active_trade = True

    @staticmethod
    def close_trade():
        TradeManager.active_trade = False
