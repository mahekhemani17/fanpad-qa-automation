from playwright.sync_api import Page
from twilio.rest import Client
import os
import time
from dotenv import load_dotenv

load_dotenv()

class OTPPage:
    def __init__(self, page: Page):
        self.page = page
        self.otp_input = page.locator('input[formcontrolname="otp"]')
        self.verify_button = page.locator('button.verify-btn')

    def get_otp_from_twilio(self):
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        time.sleep(10)  # wait for SMS to arrive
        messages = client.messages.list(to=os.getenv("TWILIO_PHONE_NUMBER"), limit=1)
        otp = ''.join(filter(str.isdigit, messages[0].body))
        return otp

    def enter_otp(self, code: str):
        self.otp_input.fill(code)

    def verify(self):
        self.verify_button.click()