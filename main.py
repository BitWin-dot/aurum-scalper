import json
import websocket
from config import DERIV_TOKENS

class DerivWS:
    def __init__(self, token_index=0):
        self.token = DERIV_TOKENS[token_index]
        self.ws = None
        self.symbol = "frxXAUUSD"
        self.candle_handler = None
        self.first_candle_received = False

    def on_message(self, ws, message):
        data = json.loads(message)
        if "candles" in data:
            latest = data["candles"][-1]

            # Ignore initial backlog candle
            if not self.first_candle_received:
                self.first_candle_received = True
                return

            if self.candle_handler:
                self.candle_handler(latest)

        if "error" in data:
            print("Deriv error:", data["error"])

    def on_open(self, ws):
        print("✅ Connected to Deriv WebSocket")
        ws.send(json.dumps({"authorize": self.token}))

        subscribe_msg = {
            "ticks_history": self.symbol,
            "end": "latest",
            "count": 2,  # minimal backlog
            "granularity": 60,
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
        # run_forever handles reconnects internally
        self.ws.run_forever()
