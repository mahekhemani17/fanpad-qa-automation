from playwright.sync_api import sync_playwright
from pages.fanclub_entry_page import FanclubEntryPage
from pages.otp_page import OTPPage
from pages.create_account_page import CreateAccountPage
from pages.payment_page import PaymentPage
from data.test_data import FAN, STRIPE
from utils.cleanup import delete_test_fan
import os
from dotenv import load_dotenv

load_dotenv()

def test_fanclub_fan_onboarding():
    # Cleanup before test so we always start fresh
    delete_test_fan()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()

        fanclub_url = os.getenv("FANCLUB_URL")

        # Step 1 - go to fanclub entry page
        entry_page = FanclubEntryPage(page, fanclub_url)
        entry_page.goto()

        # Step 2 - enter phone and submit
        entry_page.enter_phone(FAN["phone"])
        entry_page.submit_phone()
        print("✓ Phone submitted")

        # Step 3 - get OTP from Twilio and enter it
        otp_page = OTPPage(page)
        otp = otp_page.get_otp_from_twilio()
        otp_page.enter_otp(otp)
        otp_page.verify()
        print("✓ OTP verified")

        # Step 4 - fill account details
        create_page = CreateAccountPage(page)
        create_page.fill_details(FAN["username"], FAN["first_name"], FAN["email"])
        create_page.continue_to_payment()
        print("✓ Account details filled")

        # Step 5 - select subscription and pay
        payment_page = PaymentPage(page)
        payment_page.select_new_sub()
        payment_page.continue_to_stripe()
        payment_page.complete_stripe_payment(
            STRIPE["card"], STRIPE["expiry"], STRIPE["cvv"]
        )
        print("✓ Payment completed")

        # Step 6 - confirm success
        payment_page.assert_payment_success()
        print("✓ Welcome to the club page confirmed")

        browser.close()