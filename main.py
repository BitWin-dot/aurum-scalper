# deriv_api.py - Aurum Scalper Deriv WebSocket & Buy Contracts
import websocket
import json
import threading
import requests

# --- Deriv WebSocket ---
class DerivWS:
    def __init__(self, api_token=""):
        self.api_token = api_token
        self.ws = None
        self.candle_handler = None
        self.symbol = "frxXAUUSD"
        self.interval = "1m"

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            if "candles" in data:
                for candle in data["candles"]:
                    if self.candle_handler:
                        self.candle_handler(candle)
        except Exception as e:
            print("WS message error:", e)

    def on_open(self, ws):
        subscribe_msg = {
            "ticks_history": self.symbol,
            "adjust_start_time":1,
            "count": 100,
            "end": "latest",
            "granularity": 60,  # 1-minute candles
            "subscribe": 1,
            "proposal": 1
        }
        ws.send(json.dumps(subscribe_msg))
        print(f"Subscribed to {self.symbol} 1-minute candles")

    def on_error(self, ws, error):
        print("WebSocket error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")

    def start(self):
        self.ws = websocket.WebSocketApp(
            f"wss://ws.binaryws.com/websockets/v3?app_id=1089&l=EN",
            header=[f"Authorization: Bearer {self.api_token}"],
            on_message=self.on_message,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close
        )
        t = threading.Thread(target=self.ws.run_forever)
        t.start()

# --- Buy Contract for live trading ---
def buy_contract(api_token, symbol, amount, contract_type, duration, duration_unit="t"):
    url = "https://api.deriv.com/buy"
    payload = {
        "buy": 1,
        "price": amount,
        "parameters": {
            "amount": amount,
            "basis": "stake",
            "contract_type": contract_type,  # "CALL" or "PUT"
            "currency": "USD",
            "symbol": symbol,
            "duration": duration,
            "duration_unit": duration_unit
        }
    }
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print("Deriv buy_contract error:", response.text)
            return None
    except Exception as e:
        print("Deriv buy_contract exception:", e)
        return None
