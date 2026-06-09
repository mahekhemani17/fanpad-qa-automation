import os
import time
from twilio.rest import Client
from dotenv import load_dotenv
import requests
from base64 import b64encode
from datetime import datetime, timezone

load_dotenv()

def verify_email_received(expected_subject: str = None, max_wait: int = 480):
    print(f"Checking for email delivery (max {max_wait}s with exponential backoff)...")
    
    api_key = os.getenv("MAILGUN_API_KEY")
    domain = os.getenv("MAILGUN_DOMAIN")
    base_url = os.getenv("MAILGUN_BASE_URL")
    recipient = os.getenv("TEST_EMAIL")
    auth = b64encode(f"api:{api_key}".encode()).decode()
    
    wait = 60
    total_waited = 0
    
    while total_waited < max_wait:
        print(f"Waiting {wait}s before checking Mailgun...")
        time.sleep(wait)
        total_waited += wait
        
        response = requests.get(
            f"{base_url}/{domain}/events",
            headers={"Authorization": f"Basic {auth}"},
            params={"event": "delivered", "to": recipient, "limit": 10}
        )
        
        data = response.json()
        items = data.get("items", [])
        
        if expected_subject:
            matching = [i for i in items if expected_subject in i.get("message", {}).get("headers", {}).get("subject", "")]
            if matching:
                subject = matching[0].get("message", {}).get("headers", {}).get("subject", "")
                print(f"✓ Email found with subject: {subject}")
                return subject
        elif items:
            return items[0].get("message", {}).get("headers", {}).get("subject", "")
        
        wait = min(wait * 2, max_wait - total_waited)
    
    raise AssertionError(f"✗ No email delivered to {recipient} within {max_wait}s")


def verify_sms_received(expected_text: str = None, max_wait: int = 480):
    print(f"Checking for SMS delivery (max {max_wait}s with exponential backoff)...")
    request_time = datetime.now(timezone.utc)
    
    wait = 60
    total_waited = 0
    
    while total_waited < max_wait:
        print(f"Waiting {wait}s before checking Twilio...")
        time.sleep(wait)
        total_waited += wait
        
        try:
            client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
            messages = client.messages.list(to=os.getenv("TWILIO_PHONE_NUMBER"), limit=10)
            recent = [m for m in messages if m.date_sent and m.date_sent > request_time]
            
            if recent:
                latest = recent[0]
                print(f"✓ SMS received after {total_waited}s: {latest.body}")
                if expected_text and expected_text not in latest.body:
                    raise AssertionError(f"✗ SMS content mismatch. Got: {latest.body}")
                return latest.body
        except AssertionError:
            raise
        except Exception as e:
            print(f"Warning: Twilio check failed ({e}), retrying next interval...")
        
        wait = min(wait * 2, max_wait - total_waited)
    
    raise AssertionError(f"✗ No SMS received within {max_wait}s")


def send_completion_email(passed: int, failed: int, duration: str, failed_tests: list = []):
    api_key = os.getenv("MAILGUN_API_KEY")
    domain = os.getenv("MAILGUN_DOMAIN")
    base_url = os.getenv("MAILGUN_BASE_URL")
    auth = b64encode(f"api:{api_key}".encode()).decode()
    
    status = "ALL PASSED" if failed == 0 else f"{failed} FAILED"
    
    failed_section = ""
    if failed_tests:
        failed_section = "\nFailed Tests:\n" + "\n".join(f"  - {t}" for t in failed_tests)
    
    recipients = [
        "mahek.hemani@gmail.com",
        "abhishek@vennhp.com",
        "maulin@fanpad.xyz",
        "Vekariya.J@vennhp.com",
        "sudip@fanpad.xyz"
    ]
    
    response = requests.post(
        f"{base_url}/{domain}/messages",
        headers={"Authorization": f"Basic {auth}"},
        data={
            "from": "FanPad QA Automation <team@fanpad.net>",
            "to": recipients,
            "subject": f"FanPad QA Automation Run Complete — {status}",
            "text": f"""QA Automation Run Complete

Status: {status}
Tests Passed: {passed}
Tests Failed: {failed}
Duration: {duration}{failed_section}

Environment: QA
Timestamp: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

View full results in the terminal logs.
"""
        }
    )
    
    if response.status_code == 200:
        print(f"✓ Completion email sent to team")
    else:
        print(f"✗ Failed to send completion email: {response.status_code}")