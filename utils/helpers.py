import os
import time
from twilio.rest import Client
from dotenv import load_dotenv
import requests
from base64 import b64encode

load_dotenv()

def verify_email_received(expected_subject: str = None, wait_seconds: int = 480):
    print(f"Waiting {wait_seconds} seconds for email to arrive...")
    time.sleep(wait_seconds)
    
    api_key = os.getenv("MAILGUN_API_KEY")
    domain = os.getenv("MAILGUN_DOMAIN")
    base_url = os.getenv("MAILGUN_BASE_URL")
    recipient = os.getenv("TEST_EMAIL")
    
    auth = b64encode(f"api:{api_key}".encode()).decode()
    
    response = requests.get(
        f"{base_url}/{domain}/events",
        headers={"Authorization": f"Basic {auth}"},
        params={
            "event": "delivered",
            "to": recipient,
            "limit": 1
        }
    )
    
    data = response.json()
    items = data.get("items", [])
    
    if not items:
        raise AssertionError(f"✗ No email delivered to {recipient}")
    
    latest = items[0]
    subject = latest.get("message", {}).get("headers", {}).get("subject", "")
    print(f"✓ Email delivered to {recipient}, subject: {subject}")
    
    if expected_subject and expected_subject not in subject:
        raise AssertionError(f"✗ Email subject mismatch. Got: {subject}")
    
    return subject

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