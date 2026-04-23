import os
from dotenv import load_dotenv
import time

load_dotenv()

ARTIST1 = {
    "email": os.getenv("ARTIST1_EMAIL"),
    "password": os.getenv("ARTIST1_PASSWORD"),
    "base_url": os.getenv("ARTIST_BASE_URL"),
}

FAN = {
    "phone": os.getenv("TWILIO_PHONE_NUMBER"),
    "otp": "000000",
    "username": f"testfan{int(time.time())}",
    "first_name": "Test",
    "email": os.getenv("TEST_EMAIL"),
}

STRIPE = {
    "card": os.getenv("STRIPE_TEST_CARD"),
    "expiry": os.getenv("STRIPE_TEST_EXPIRY"),
    "cvv": os.getenv("STRIPE_TEST_CVV"),
    "name": os.getenv("STRIPE_TEST_NAME"),
    "zip": os.getenv("STRIPE_TEST_ZIP"),
}
