# Aurum Scalper Configuration

# Deriv API tokens (we'll fill later)
DERIV_TOKENS = [
    "YOUR_DERIV_API_TOKEN_1",
    # Add more if needed
]

# Telegram
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

# Risk settings
RISK_PER_TRADE = 0.01  # 1% risk
MAX_DRAWDOWN = 0.05    # 5% daily
MAX_CONSECUTIVE_LOSSES = 3
MAX_TRADES_PER_DAY = 10

# Trade R:R
TP1 = 1.0  # 1R
TP2 = 2.0  # 2R

# Filters
ATR_PERIOD = 14
ATR_MIN = 0.2
SPREAD_LIMIT = 0.3
