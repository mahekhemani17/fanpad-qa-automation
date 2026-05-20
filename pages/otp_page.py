from playwright.sync_api import Page
from twilio.rest import Client
import os
import time
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

class OTPPage:
    def __init__(self, page: Page):
        self.page = page
        self.otp_input = page.locator('input[formcontrolname="otp"]')
        self.verify_button = page.locator('button.verify-btn')

    def get_otp_from_twilio(self):
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        request_time = datetime.now(timezone.utc)
        
        wait = 15
        total_waited = 0
        max_wait = 120
        
        while total_waited < max_wait:
            print(f"Waiting {wait}s for OTP SMS...")
            time.sleep(wait)
            total_waited += wait
            
            messages = client.messages.list(to=os.getenv("TWILIO_PHONE_NUMBER"), limit=10)
            recent = [m for m in messages if m.date_sent and m.date_sent > request_time]
            
            if recent:
                otp = ''.join(filter(str.isdigit, recent[0].body))[:6]
                print(f"✓ OTP received: {otp}")
                return otp
            
            wait = min(wait * 2, max_wait - total_waited)
        
        raise AssertionError("✗ OTP not received within 2 minutes")

    def enter_otp(self, code: str):
        self.otp_input.fill(code)

    def verify(self):
        self.verify_button.click()