import json
import websocket
from config import DERIV_TOKENS

class DerivWS:
    """
    Deriv WebSocket client for Gold/USD CFD (frxGOLD) 1-minute candles
    """

    def __init__(self, token_index=0):
        self.token = DERIV_TOKENS[token_index]
        self.ws = None

    def on_message(self, ws, message):
        data = json.loads(message)
        # Check for candle data
        if "history" in data or "candles" in data:
            print("Candle data received:", json.dumps(data, indent=2))
        elif "error" in data:
            print("Deriv error:", data["error"])

    def on_open(self, ws):
        print("✅ Connected to Deriv WebSocket")

        # Step 1 — Authorize
        auth_msg = {
            "authorize": self.token
        }
        ws.send(json.dumps(auth_msg))

        # Step 2 — Subscribe to Gold/USD 1-minute candles
        subscribe_msg = {
            "ticks_history": "frxGOLD",  # Gold/USD CFD on Deriv
            "end": "latest",
            "count": 100,
            "granularity": 60,  # 1-minute candles
            "style": "candles",
            "subscribe": 1
        }
        ws.send(json.dumps(subscribe_msg))
        print("Subscribed to frxGOLD 1-minute candles")

    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
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
