# filters/session.py

from datetime import datetime


class SessionFilter:
    @staticmethod
    def is_active():
        """
        Trade only during London + New York sessions
        """
        hour = datetime.utcnow().hour

        # London (6–15) + NY (12–20 overlap)
        if 6 <= hour <= 20:
            return True

        return False
