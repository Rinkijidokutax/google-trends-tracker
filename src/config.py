import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email Configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

# SMTP Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# Google Trends Configuration
REGION = os.getenv("REGION", "US")

# Report Settings
STOCK_KEYWORDS = [
    "stock market",
    "trading",
    "investment",
    "S&P 500",
    "NASDAQ",
    "Dow Jones",
    "stock analysis",
    "day trading",
    "swing trading",
    "technical analysis",
    "fundamental analysis",
    "dividend stocks",
    "growth stocks",
    "ETF",
    "options trading",
    "IPO",
    "market crash",
    "bull market",
    "bear market",
    "inflation"
]

# Time periods to fetch data for
TIME_PERIODS = {
    "daily": "now 1-d",
    "weekly": "now 7-d",
    "monthly": "today 1-m"
}

# File paths
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")

# Create directories if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Logging configuration
LOG_FILE = os.path.join(LOG_DIR, "google_trends_tracker.log")

# Schedule settings
DAILY_REPORT_TIME = os.getenv("DAILY_REPORT_TIME", "08:00")
WEEKLY_REPORT_DAY = os.getenv("WEEKLY_REPORT_DAY", "MON")
WEEKLY_REPORT_TIME = os.getenv("WEEKLY_REPORT_TIME", "09:00")
MONTHLY_REPORT_DAY = int(os.getenv("MONTHLY_REPORT_DAY", 1))
MONTHLY_REPORT_TIME = os.getenv("MONTHLY_REPORT_TIME", "10:00")
