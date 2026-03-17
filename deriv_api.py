# deriv_api.py

import websocket
import json
import threading
import logging

logger = logging.getLogger(__name__)

class DerivWS:
    def __init__(self, token):
        self.token = token
        self.ws = None
        self.url = "wss://ws.binaryws.com/websockets/v3?app_id=1089"

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        thread = threading.Thread(target=self.ws.run_forever)
        thread.daemon = True
        thread.start()

    def on_message(self, ws, message):
        data = json.loads(message)
        # handle messages here

    def on_error(self, ws, error):
        logger.error(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logger.warning("WebSocket closed")

    def subscribe_candles(self, symbol, interval):
        """
        Subscribe to Deriv 1-minute candles.
        NOTE: positional args, not keyword args.
        """
        if not self.ws:
            raise RuntimeError("WebSocket is not connected")

        request = {
            "ticks_history": symbol,
            "adjust_start_time": 1,
            "count": 1,
            "end": "latest",
            "granularity": interval,
            "style": "candles"
        }

        self.ws.send(json.dumps({"subscribe": 1, **request}))
        logger.info(f"Subscribed to {symbol} {interval}s candles")
