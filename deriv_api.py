# deriv_api.py
import json
import websocket
import threading
import time

class DerivWS:
    def __init__(self, token, symbol="frxXAUUSD", interval=60, on_candle=None):
        """
        token: Deriv API token (string)
        symbol: trading symbol, default frxXAUUSD
        interval: candle interval in seconds (60 = 1m)
        on_candle: callback function to handle new candles
        """
        self.token = token
        self.symbol = symbol
        self.interval = interval
        self.on_candle = on_candle
        self.ws = None
        self.thread = None
        self.stop_flag = False

    def _connect(self):
        url = f"wss://ws.binaryws.com/websockets/v3?app_id=1089"
        self.ws = websocket.WebSocketApp(
            url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        self.ws.run_forever()

    def start(self):
        self.stop_flag = False
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def _run(self):
        while not self.stop_flag:
            try:
                self._connect()
            except Exception as e:
                print(f"WebSocket crashed, reconnecting in 3s... Error: {e}")
                time.sleep(3)

    def stop(self):
        self.stop_flag = True
        if self.ws:
            self.ws.close()
        if self.thread:
            self.thread.join()

    # --- WebSocket callbacks ---
    def _on_open(self, ws):
        print("✅ Connected to Deriv WebSocket")
        self.subscribe_candles()

    def _on_message(self, ws, message):
        data = json.loads(message)
        if "candles" in data.get("tick", {}):
            candle = data["tick"]["candles"][-1]
            if self.on_candle:
                self.on_candle(candle)
        elif "tick" in data:
            # Some Deriv streams return 'tick' directly
            if self.on_candle:
                self.on_candle(data["tick"])

    def _on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")

    # --- Subscribe to candles ---
    def subscribe_candles(self):
        """
        Subscribe to live candles on Deriv
        """
        request = {
            "ticks_history": self.symbol,
            "adjust_start_time": 1,
            "count": 1,
            "end": "latest",
            "granularity": self.interval,
            "style": "candles",
        }
        subscribe = {
            "subscribe": request
        }
        self.ws.send(json.dumps(subscribe))
        print(f"Subscribed to {self.symbol} {self.interval//60}m candles")
