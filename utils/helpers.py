import os
import time
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def verify_sms_received(expected_text: str = None, wait_seconds: int = 30):
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    print(f"Waiting {wait_seconds} seconds for SMS to arrive...")
    time.sleep(wait_seconds)
    messages = client.messages.list(to=os.getenv("TWILIO_PHONE_NUMBER"), limit=1)
    if not messages:
        raise AssertionError("✗ No SMS received on Twilio number")
    latest = messages[0]
    print(f"✓ SMS received: {latest.body}")
    if expected_text and expected_text not in latest.body:
        raise AssertionError(f"✗ SMS content mismatch. Got: {latest.body}")
    return latest.body