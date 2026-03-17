import json
import websocket
from config import DERIV_TOKENS

class DerivWS:
    """
    Minimal Deriv WebSocket client for XAU/USD
    """
    def __init__(self, token_index=0):
        self.token = DERIV_TOKENS[token_index]
        self.ws = None
        self.subscribed = False

    def on_message(self, ws, message):
        data = json.loads(message)
        # For testing, print the candle data
        if "candles" in data:
            candle = data["candles"]
            print(f"Received candle: {candle}")

    def on_open(self, ws):
        print("Connected to Deriv WebSocket")
        # Subscribe to 1-minute XAU/USD candles
        subscribe_msg = {
            "ticks_history": "XAUUSD",
            "adjust_start_time": 1,
            "count": 1,
            "end": "latest",
            "start": 1,
            "style": "candles",
            "subscribe": 1
        }
        ws.send(json.dumps({
            "authorize": self.token
        }))
        ws.send(json.dumps(subscribe_msg))

    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def on_close(self, ws):
        print("WebSocket closed")

    def start(self):
        self.ws = websocket.WebSocketApp(
            "wss://ws.binaryws.com/websockets/v3?app_id=1089",
            on_message=self.on_message,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.run_forever()
