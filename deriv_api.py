import json
import websocket
from config import DERIV_TOKENS

class DerivWS:
    """
    Deriv WebSocket client
    Automatically finds Gold/USD CFD and subscribes to 1-minute candles
    """

    def __init__(self, token_index=0):
        self.token = DERIV_TOKENS[token_index]
        self.ws = None
        self.gold_symbol = None

    def on_message(self, ws, message):
        data = json.loads(message)

        # Look for active symbols response
        if data.get("msg_type") == "active_symbols":
            for item in data["active_symbols"]:
                # We only want CFD/forex products
                if item.get("market") == "forex" or item.get("market") == "commodities":
                    sym = item.get("symbol")
                    if sym and "GOLD" in sym.upper():
                        self.gold_symbol = sym
                        print(f"✅ Found Gold symbol: {sym}")
                        self.subscribe_candles(sym)
                        break

        # Candle data
        if "candles" in data:
            print("Candle:", json.dumps(data["candles"], indent=2))

        if "error" in data:
            print("Deriv error:", data["error"])

    def on_open(self, ws):
        print("Connected to Deriv WebSocket")

        # 1) Authorize
        ws.send(json.dumps({"authorize": self.token}))

        # 2) Request active symbols filtered by market type
        ws.send(json.dumps({"active_symbols": "brief"}))  # WebSocket API will return all symbols, we filter in code

    def subscribe_candles(self, symbol):
        subscribe_msg = {
            "ticks_history": symbol,
            "end": "latest",
            "count": 100,
            "granularity": 60,
            "style": "candles",
            "subscribe": 1
        }
        self.ws.send(json.dumps(subscribe_msg))
        print(f"Subscribed to {symbol} 1-minute candles")

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
