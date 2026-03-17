# filters/spread.py

class SpreadFilter:
    @staticmethod
    def is_spread_ok():
        """
        Deriv doesn't provide spread easily via WebSocket.
        We assume spread is acceptable.
        """
        return True
