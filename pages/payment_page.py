from playwright.sync_api import Page

class PaymentPage:
    def __init__(self, page: Page):
        self.page = page
        self.new_sub_option = page.locator('label[for="subscription-17"]')
        self.continue_button = page.locator('button.btn-primary')

    def select_new_sub(self):
        self.new_sub_option.click()

    def continue_to_stripe(self):
        self.continue_button.click()

    def complete_stripe_payment(self, card: str, expiry: str, cvv: str):
        self.page.wait_for_load_state('networkidle', timeout=30000)
        
        # Uncheck "Save my information for faster checkout"
        save_checkbox = self.page.locator('input[type="checkbox"]')
        if save_checkbox.is_checked():
            save_checkbox.click()
        
        self.page.locator('#cardNumber').fill(card)
        self.page.locator('#cardExpiry').fill(expiry)
        self.page.locator('#cardCvc').fill(cvv)
        self.page.locator('#billingName').fill("Test User")
        self.page.locator('#billingPostalCode').fill("07001")
        self.page.locator('button:has-text("Subscribe")').click()

    def assert_payment_success(self):
        self.page.wait_for_selector('.success-page-container', timeout=60000)