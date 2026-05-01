from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import locators

class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.total_balance_widget = page.locator(locators.DASHBOARD_PAGE["total_balance_widget"])

    def is_visible(self):
        expect(self.page).to_have_url("/dashboard")
        expect(self.total_balance_widget).to_be_visible()

    def navigate(self):
        super().navigate("/dashboard")
