from playwright.sync_api import Page

class FanclubEntryPage:
    def __init__(self, page: Page, fanclub_url: str):
        self.page = page
        self.fanclub_url = fanclub_url
        self.phone_input = page.locator('#phone')
        self.send_code_button = page.locator('button.send-btn')

    def goto(self):
        self.page.goto(self.fanclub_url)

    def enter_phone(self, phone: str):
        self.phone_input.fill(phone)

    def submit_phone(self):
        self.send_code_button.click()