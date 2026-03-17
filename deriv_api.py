import json
import websocket
from config import DERIV_TOKENS

class DerivWS:
    """
    Deriv WebSocket client for Gold/USD CFD (frxXAUUSD)
    Streams 1-minute candles
    """

    def __init__(self, token_index=0):
        self.token = DERIV_TOKENS[token_index]
        self.ws = None
        self.symbol = "frxXAUUSD"  # Deriv symbol for Gold/USD CFD

    def on_message(self, ws, message):
        data = json.loads(message)

        # Candle data
        if "candles" in data:
            print("Candle:", json.dumps(data["candles"], indent=2))

        # Errors
        if "error" in data:
            print("Deriv error:", data["error"])

    def on_open(self, ws):
        print("✅ Connected to Deriv WebSocket")

        # 1) Authorize
        ws.send(json.dumps({"authorize": self.token}))

        # 2) Subscribe to 1-minute candles
        subscribe_msg = {
            "ticks_history": self.symbol,
            "end": "latest",
            "count": 100,
            "granularity": 60,  # 1-minute candles
            "style": "candles",
            "subscribe": 1
        }
        ws.send(json.dumps(subscribe_msg))
        print(f"Subscribed to {self.symbol} 1-minute candles")

    def on_error(self, ws, error):
        print("WebSocket error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")

    def start(self):
        self.ws = websocket.WebSocketApp(
            "wss://ws.binaryws.com/websockets/v3?app_id=1089",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.run_forever()
