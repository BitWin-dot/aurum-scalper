import websocket
import json
import threading
import time

class DerivWS:
    def __init__(self, token):
        """
        Initialize WebSocket with your real Deriv API token.
        """
        self.token = token
        self.ws = None
        self.candle_handler = None
        self.symbol = "frxXAUUSD"
        self.interval = "1m"

    def start(self):
        """Start the WebSocket connection"""
        url = f"wss://ws.binaryws.com/websockets/v3?app_id=1089&l=EN"
        self.ws = websocket.WebSocketApp(
            url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error
        )
        thread = threading.Thread(target=self.ws.run_forever)
        thread.daemon = True
        thread.start()

    def on_open(self, ws):
        print("✅ Connected to Deriv WebSocket")
        # Subscribe to candles
        subscribe_msg = {
            "ticks_history": self.symbol,
            "subscribe": 1,
            "adjust_start_time": 1,
            "count": 1,
            "granularity": 60,
            "style": "candles"
        }
        self.ws.send(json.dumps(subscribe_msg))
        print(f"Subscribed to {self.symbol} {self.interval} candles")

    def on_message(self, ws, message):
        data = json.loads(message)
        try:
            if "candles" in data:
                candle = data["candles"][-1]
                if self.candle_handler:
                    self.candle_handler(candle)
        except Exception as e:
            print("Error handling candle:", e)

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")

    def on_error(self, ws, error):
        print("WebSocket error:", error)
