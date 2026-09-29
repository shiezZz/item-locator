"""
config.py
Single source of truth for paths, secrets, and tunable constants.
Everything else imports from here instead of reading os.environ directly.
"""

import os 
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "item_locator.db")
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "item_images")
os.makedirs(IMAGES_DIR, exist_ok=True)

GMAIL_SENDER = os.environ.get("GMAIL_SENDER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

CODE_EXPIRY_SECONDS = 15 * 60
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_SECONDS = 10 * 60