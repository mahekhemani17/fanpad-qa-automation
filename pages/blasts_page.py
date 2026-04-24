from playwright.sync_api import Page

class BlastsPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.filter_button = page.locator('span.filter-text')
        self.event_dropdown = page.locator('#ddlArtistEvent')
        self.search_button = page.locator('button:has-text("Search")')
        self.apply_button = page.locator('button:has-text("Apply")')
        self.email_button = page.locator('#btnEmailSelect')
        self.sms_button = page.locator('#btnSMSSelect')
        self.whatsapp_button = page.locator('#btnWhatsAppSelect')
        self.subject_input = page.locator('input[placeholder="e.g. Welcome!"]')
        self.message_editor = page.locator('.ck-editor__editable')
        self.sms_message_input = page.locator('input[placeholder*="You"]').first
        self.send_test_button = page.locator('button.send-test-btn')
        self.send_button = page.locator('button.footer-btn:has-text("Send")')

    def goto(self):
        self.page.goto(f"{self.base_url}/messages")

    def apply_event_filter(self):
        self.filter_button.click()
        self.page.locator('button[data-bs-target="#collapseSeven"]').click()
        self.page.wait_for_selector('#ddlArtistEvent', state='visible', timeout=10000)
        self.event_dropdown.select_option(label="Source testing the data | HGyderabd | 2026-05-07")
        self.search_button.click()
        self.apply_button.click()

    def select_email(self):
        self.email_button.click()

    def select_sms(self):
        self.sms_button.click()

    def select_whatsapp(self):
        self.whatsapp_button.click()

    def fill_subject(self, subject: str):
        self.subject_input.fill(subject)

    def fill_message(self, message: str):
        self.message_editor.click()
        self.page.wait_for_timeout(500)
        self.page.evaluate("""
            document.querySelector('.ck-editor__editable').ckeditorInstance.setData('<p>Hi there,</p><p>Welcome!</p><p>I am so excited to have you here.</p><p>Whether you have been following for a while or just discovered me, your support truly means everything.</p><p>You can expect exclusive updates, behind-the-scenes content, and a closer look at everything I am working on. I cannot wait to take you along for the ride.</p><p>I would love to hear from you.</p><p>With gratitude,</p><p>Jon</p>');
        """)
        self.page.wait_for_timeout(500)

    def fill_sms_message(self, message: str):
        self.sms_message_input.fill(message)

    def send_test(self):
        self.send_test_button.click()

    def send_real(self):
        self.page.on("dialog", lambda dialog: dialog.accept())
        self.send_button.click()

    def assert_test_sent(self):
        success = self.page.locator('text=Test message sent')
        success.wait_for(timeout=10000)

    def assert_blast_queued(self):
        success = self.page.locator('text=added to queue')
        success.wait_for(timeout=15000)