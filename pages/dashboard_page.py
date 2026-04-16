from playwright.sync_api import Page

class DashboardPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.artist_heading = page.locator('h3:has-text("All-Time Stats")')
        self.logout_button = page.locator('a:has-text("Logout")')

    def assert_loaded(self):
        self.artist_heading.wait_for(timeout=10000)

    def logout(self):
        self.logout_button.click()

    def assert_redirected_to_dashboard(self):
        self.page.wait_for_url(f"{self.base_url}/dashboard", timeout=10000)