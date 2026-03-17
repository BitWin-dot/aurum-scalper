import logging
from logging.handlers import RotatingFileHandler

# -------------------------------
# LOGGING CONFIGURATION
# -------------------------------
LOG_FILE = "aurum_scalper.log"
LOG_LEVEL = logging.INFO  # Change to DEBUG for more details

# Create a rotating file handler (max 5MB per file, keep 3 backups)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
file_handler.setLevel(LOG_LEVEL)
file_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
file_handler.setFormatter(file_formatter)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(file_formatter)

# Create logger
logger = logging.getLogger("AurumScalper")
logger.setLevel(LOG_LEVEL)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def info(message):
    logger.info(message)

def debug(message):
    logger.debug(message)

def warning(message):
    logger.warning(message)

def error(message):
    logger.error(message)
