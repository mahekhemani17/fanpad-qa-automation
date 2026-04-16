from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.email_input = page.locator('#txtEmailAddress')
        self.password_input = page.locator('#txtPassword')
        self.login_button = page.locator('button:has-text("Login")')
        self.success_toast = page.locator('text=Logged in successfully')

    def goto(self):
        self.page.goto(f"{self.base_url}/login")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def assert_login_success(self):
        self.success_toast.wait_for(timeout=10000)

    def assert_redirected_to_login(self):
        self.page.wait_for_url(f"{self.base_url}/login", timeout=10000)