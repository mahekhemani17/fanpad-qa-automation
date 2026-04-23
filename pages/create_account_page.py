from playwright.sync_api import Page

class CreateAccountPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator('#userName')
        self.first_name_input = page.locator('#firstName')
        self.email_input = page.locator('#regEmail')
        self.discord_input = page.locator('#discord')
        self.birthday_input = page.locator('#birthday')
        self.continue_button = page.locator('button:has-text("Continue")')

    def fill_details(self, username: str, first_name: str, email: str = None):
        self.username_input.fill(username)
        self.first_name_input.fill(first_name)
        if email:
            self.email_input.fill(email)

    def continue_to_payment(self):
        self.continue_button.click()