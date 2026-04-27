from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.blasts_page import BlastsPage
from data.test_data import ARTIST1
from utils.helpers import verify_sms_received, verify_email_received
import os
from dotenv import load_dotenv

load_dotenv()

def test_email_blast():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()

        login_page = LoginPage(page, ARTIST1["base_url"])
        dashboard_page = DashboardPage(page, ARTIST1["base_url"])
        login_page.goto()
        login_page.login(ARTIST1["email"], ARTIST1["password"])
        dashboard_page.assert_loaded()
        print("✓ Logged in as artist")

        blasts_page = BlastsPage(page, ARTIST1["base_url"])
        blasts_page.goto()
        print("✓ Blasts page loaded")

        blasts_page.select_email()
        blasts_page.fill_subject("This is a Test")
        blasts_page.fill_message("This is a Test")
        blasts_page.send_test()
        print("✓ Email test sent")

        browser.close()

def test_sms_blast():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()

        login_page = LoginPage(page, ARTIST1["base_url"])
        dashboard_page = DashboardPage(page, ARTIST1["base_url"])
        login_page.goto()
        login_page.login(ARTIST1["email"], ARTIST1["password"])
        dashboard_page.assert_loaded()
        print("✓ Logged in as artist")

        blasts_page = BlastsPage(page, ARTIST1["base_url"])
        blasts_page.goto()
        print("✓ Blasts page loaded")

        blasts_page.select_sms()
        blasts_page.fill_sms_message("This is a Test")
        blasts_page.send_test()
        print("✓ SMS test sent")

        browser.close()

def test_whatsapp_blast():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()

        login_page = LoginPage(page, ARTIST1["base_url"])
        dashboard_page = DashboardPage(page, ARTIST1["base_url"])
        login_page.goto()
        login_page.login(ARTIST1["email"], ARTIST1["password"])
        dashboard_page.assert_loaded()
        print("✓ Logged in as artist")

        blasts_page = BlastsPage(page, ARTIST1["base_url"])
        blasts_page.goto()
        print("✓ Blasts page loaded")

        blasts_page.select_whatsapp()
        blasts_page.fill_sms_message("This is a Test")
        blasts_page.send_test()
        print("✓ WhatsApp test sent")

        browser.close()

def test_real_email_blast():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()

        login_page = LoginPage(page, ARTIST1["base_url"])
        dashboard_page = DashboardPage(page, ARTIST1["base_url"])
        login_page.goto()
        login_page.login(ARTIST1["email"], ARTIST1["password"])
        dashboard_page.assert_loaded()
        print("✓ Logged in as artist")

        blasts_page = BlastsPage(page, ARTIST1["base_url"])
        blasts_page.goto()
        print("✓ Blasts page loaded")
        blasts_page.apply_event_filter()
        print("✓ Event filter applied")

        blasts_page.select_email()
        blasts_page.fill_subject("Welcome to the Journey")
        blasts_page.fill_message("ignored")
        blasts_page.send_real()
        blasts_page.assert_blast_queued()
        print("✓ Real email blast queued successfully")

        browser.close()

    # Verify email actually delivered via Mailgun
    verify_email_received(expected_subject="Welcome to the Journey", wait_seconds=480)
    print("✓ Email delivery confirmed via Mailgun")

def test_real_sms_blast():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()

        login_page = LoginPage(page, ARTIST1["base_url"])
        dashboard_page = DashboardPage(page, ARTIST1["base_url"])
        login_page.goto()
        login_page.login(ARTIST1["email"], ARTIST1["password"])
        dashboard_page.assert_loaded()
        print("✓ Logged in as artist")

        blasts_page = BlastsPage(page, ARTIST1["base_url"])
        blasts_page.goto()
        print("✓ Blasts page loaded")
        blasts_page.apply_event_filter()
        print("✓ Event filter applied")

        blasts_page.select_sms()
        blasts_page.fill_sms_message("This is a Test")
        blasts_page.send_real()
        blasts_page.assert_blast_queued()
        print("✓ Real SMS blast queued successfully")

        browser.close()

    # Verify SMS actually delivered via Twilio
    verify_sms_received(expected_text="This is a Test", wait_seconds=480)
    print("✓ SMS delivery confirmed via Twilio")