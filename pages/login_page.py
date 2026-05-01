from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import locators

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_field = page.locator(locators.LOGIN_PAGE["email_field"])
        self.password_field = page.locator(locators.LOGIN_PAGE["password_field"])
        self.login_button = page.locator(locators.LOGIN_PAGE["login_button"])
        self.register_tab = page.locator(locators.LOGIN_PAGE["register_tab"])
        self.sign_in_tab = page.locator(locators.LOGIN_PAGE["sign_in_tab"])
        self.error_message = page.locator(locators.LOGIN_PAGE["error_message"])
        self.sign_up_button = page.locator(locators.LOGIN_PAGE["sign_up_button"])

    def navigate(self):
        super().navigate("/login")

    def login(self, email, password):
        self.email_field.fill(email)
        self.password_field.fill(password)
        self.login_button.click()

    def register(self, email, password):
        self.register_tab.click()
        self.email_field.fill(email)
        self.password_field.fill(password)
        self.sign_up_button.click()

    def switch_to_register(self):
        self.register_tab.click()

    def get_error_text(self):
        return self.error_message.inner_text()

    def is_field_invalid(self, field_name: str):
        field = self.email_field if field_name == "email" else self.password_field
        return field.evaluate("el => !el.checkValidity()")
