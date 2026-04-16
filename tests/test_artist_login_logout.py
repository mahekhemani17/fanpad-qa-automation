import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from data.test_data import ARTIST

def test_artist_login_and_logout():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()

        login_page = LoginPage(page, ARTIST["base_url"])
        dashboard_page = DashboardPage(page, ARTIST["base_url"])

        # Step 1 - go to login page
        login_page.goto()

        # Step 2 - log in
        login_page.login(ARTIST["email"], ARTIST["password"])

        # Step 3 - confirm dashboard loaded
        dashboard_page.assert_loaded()
        print("✓ Dashboard loaded successfully")

        # Step 4 - log out
        dashboard_page.logout()
        print("✓ Logged out successfully")

        # Step 5 - confirm redirected back to login
        login_page.assert_redirected_to_login()
        print("✓ Redirected back to login page")

        browser.close()