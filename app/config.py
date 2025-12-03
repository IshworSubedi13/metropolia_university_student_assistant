import os
from typing import List

from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Gemini AI
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # Twilio
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

    # PDF
    PDF_PATH = os.getenv("PDF_PATH", "files/metropolia_manual.pdf")

    # Website URLs
    WEBSITE_URLS: List[str] = os.getenv("WEBSITE_URLS", "https://www.metropolia.fi/en").split(",")

    # Server
    PORT = int(os.getenv("PORT", "3000"))


config = Config()

